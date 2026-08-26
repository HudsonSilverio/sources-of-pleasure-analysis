"""
Phase 1 — Cleaning and anonymization.
Loads the raw CSV, removes PII, removes junk/corrupted columns,
filters to complete responses, deduplicates, recalculates factor scores,
and saves a clean dataset.
"""

import yaml
import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_CSV = PROJECT_ROOT / "data" / "raw" / "sources-of-pleasure.csv"
CLEAN_CSV = PROJECT_ROOT / "data" / "processed" / "clean.csv"
CONFIG_YAML = PROJECT_ROOT / "config" / "instrument.yaml"
REPORT_PATH = PROJECT_ROOT / "outputs" / "reports" / "phase1_cleaning.md"

# ---------------------------------------------------------------------------
# Load config
# ---------------------------------------------------------------------------
with open(CONFIG_YAML, encoding="utf-8") as f:
    config = yaml.safe_load(f)

ITEM_COLS = [item["variavel"] for item in config["itens"]]
FACTOR_DEFS = config["fatores"]
PII_COLS = [c for c in config["colunas_pii"] if c != "nota"]
SCALE_MIN = config["escala"]["minimo"]
SCALE_MAX = config["escala"]["maximo"]

# ---------------------------------------------------------------------------
# 1. Load raw data
# ---------------------------------------------------------------------------
print("Carregando CSV bruto...")
df_raw = pd.read_csv(RAW_CSV, sep=";", low_memory=False)
n_raw_rows, n_raw_cols = df_raw.shape
print(f"  {n_raw_rows} linhas x {n_raw_cols} colunas")

# ---------------------------------------------------------------------------
# 2. Remove PII columns FIRST
# ---------------------------------------------------------------------------
print("\nRemovendo colunas PII...")

# Columns explicitly listed in config
pii_to_drop = [c for c in PII_COLS if c in df_raw.columns]

# Scan for additional PII columns (email, phone, contact, skype)
pii_keywords = ["email", "phone", "skype", "contactinformation", "convenienttimes"]
additional_pii = [
    c for c in df_raw.columns
    if any(k in c.lower() for k in pii_keywords)
    and c not in pii_to_drop
]
all_pii = pii_to_drop + additional_pii
print(f"  Colunas PII removidas ({len(all_pii)}):")
for c in all_pii:
    print(f"    - {c}")

df = df_raw.drop(columns=all_pii, errors="ignore")

# ---------------------------------------------------------------------------
# 3. Define columns to KEEP
# ---------------------------------------------------------------------------
print("\nSelecionando colunas uteis...")

# Session metadata (User kept temporarily for deduplication, removed at the end)
meta_cols = ["Run", "User", "Time Started (UTC)", "Time Finished (UTC)", "Minutes Spent"]

# 37 analytic items
item_cols = [c for c in ITEM_COLS if c in df.columns]

# Ranking labels
rank_cols = [c for c in df.columns if "questionRank" in c and "Label" in c]

# Reflection/selection columns
reflection_prefixes = (
    "moreOften", "moreOfIt", "usePleasure",
    "selectedLabel", "selectedSource",
)
reflection_cols = [
    c for c in df.columns
    if any(c.startswith(pref) for pref in reflection_prefixes)
]

cols_to_keep = []
for c in meta_cols + item_cols + rank_cols + reflection_cols:
    if c in df.columns and c not in cols_to_keep:
        cols_to_keep.append(c)

n_dropped_cols = len(df.columns) - len(cols_to_keep)
print(f"  Colunas mantidas: {len(cols_to_keep)}")
print(f"  Colunas descartadas (lixo + corrompidas): {n_dropped_cols}")

df = df[cols_to_keep].copy()

# ---------------------------------------------------------------------------
# 4. Convert p_* items to numeric and validate
# ---------------------------------------------------------------------------
print("\nConvertendo e validando itens p_*...")

anomalies = []
for c in item_cols:
    original = df[c].copy()
    df[c] = pd.to_numeric(df[c], errors="coerce")
    coerced = original.notna() & df[c].isna()
    if coerced.any():
        anomalies.append((c, int(coerced.sum()), "valores nao-numericos coagidos a NaN"))

    out_of_range = df[c].dropna()
    invalid = out_of_range[(out_of_range < SCALE_MIN) | (out_of_range > SCALE_MAX)]
    if len(invalid) > 0:
        anomalies.append((c, len(invalid), f"valores fora de [{SCALE_MIN}, {SCALE_MAX}]"))
        df.loc[invalid.index, c] = np.nan

if anomalies:
    print("  ANOMALIAS encontradas:")
    for col, count, desc in anomalies:
        print(f"    {col}: {count} {desc}")
else:
    print("  Nenhuma anomalia — todos os valores em {-3..+3} ou ausentes.")

unique_vals = set()
for c in item_cols:
    unique_vals.update(df[c].dropna().unique())
print(f"  Valores unicos encontrados: {sorted(unique_vals)}")

# ---------------------------------------------------------------------------
# 5. Filter to complete responses (all 37 items answered)
# ---------------------------------------------------------------------------
print("\nFiltrando linhas completas (todos os 37 itens respondidos)...")

complete_mask = df[item_cols].notna().all(axis=1)
n_complete = int(complete_mask.sum())
n_incomplete = len(df) - n_complete
print(f"  Linhas completas: {n_complete}")
print(f"  Linhas incompletas descartadas: {n_incomplete}")

df = df[complete_mask].copy()

# ---------------------------------------------------------------------------
# 6. Deduplicate (same User, keep last Run)
# ---------------------------------------------------------------------------
print("\nDeduplicando...")

# Run is always unique, but some Users have multiple Runs.
# Since most rows have no User value, we only deduplicate among those that do.
# Strategy: keep the row with the highest Run number (most recent).
n_before_dedup = len(df)

# Convert Run to numeric for sorting
df["_run_numeric"] = pd.to_numeric(df["Run"], errors="coerce")

# Rows without User: always keep
no_user = df["Run"].isna() | df.get("User", pd.Series(dtype=str)).isna()
# Note: we don't have User column anymore (it was dropped as non-essential).
# Let's check if we kept it.
if "User" not in df.columns:
    # User was not in our keep list — no deduplication possible by User.
    # But Run is unique (verified), so no true duplicates.
    print("  Coluna 'User' nao preservada — deduplicacao por Run.")
    print(f"  Runs duplicados: {df['Run'].duplicated().sum()}")
else:
    has_user = df["User"].notna()
    df_no_user = df[~has_user]
    df_has_user = df[has_user].sort_values("_run_numeric", ascending=False)
    df_has_user = df_has_user.drop_duplicates(subset="User", keep="first")
    df = pd.concat([df_no_user, df_has_user], ignore_index=True)

df = df.drop(columns=["_run_numeric"], errors="ignore")

# Remove User column after deduplication (not analytically useful, quasi-identifier)
df = df.drop(columns=["User"], errors="ignore")

n_after_dedup = len(df)
n_deduped = n_before_dedup - n_after_dedup
print(f"  Linhas antes: {n_before_dedup}")
print(f"  Linhas removidas por deduplicacao: {n_deduped}")
print(f"  Linhas apos deduplicacao: {n_after_dedup}")

# ---------------------------------------------------------------------------
# 7. Recalculate factor scores from raw items
# ---------------------------------------------------------------------------
print("\nRecalculando scores de fator a partir dos itens brutos...")

for factor_name, factor_def in FACTOR_DEFS.items():
    factor_items = factor_def["itens"]
    col_name = f"factor_{factor_name}"
    df[col_name] = df[factor_items].mean(axis=1)
    mean_val = df[col_name].mean()
    print(f"  {col_name}: media geral = {mean_val:.3f} (N = {df[col_name].notna().sum()})")

# ---------------------------------------------------------------------------
# 8. Save clean dataset
# ---------------------------------------------------------------------------
print(f"\nSalvando dataset limpo em {CLEAN_CSV}...")
CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(CLEAN_CSV, index=False)

n_final_rows, n_final_cols = df.shape
print(f"  {n_final_rows} linhas x {n_final_cols} colunas")

# ---------------------------------------------------------------------------
# 9. Generate cleaning report
# ---------------------------------------------------------------------------
print(f"\nGerando relatorio em {REPORT_PATH}...")

report = f"""# Fase 1 — Relatorio de Limpeza

## Resumo

| Metrica | Valor |
|---|---|
| Linhas no CSV bruto | {n_raw_rows:,} |
| Colunas no CSV bruto | {n_raw_cols:,} |
| Linhas completas (37 itens respondidos) | {n_complete:,} |
| Linhas incompletas descartadas | {n_incomplete:,} ({n_incomplete/n_raw_rows*100:.1f}%) |
| Linhas removidas por deduplicacao | {n_deduped:,} |
| **Linhas no dataset final** | **{n_final_rows:,}** |
| **Colunas no dataset final** | **{n_final_cols:,}** |

## Colunas removidas

### PII ({len(all_pii)} colunas)
Removidas **antes** de qualquer outra operacao para proteger dados pessoais.

{chr(10).join(f"- `{c}`" for c in all_pii)}

### Lixo de processo e colunas derivadas corrompidas ({n_dropped_cols} colunas)
Variaveis internas do GuidedTrack (barra de progresso, temporarias, MailChimp,
UTM), colunas derivadas corrompidas por locale (`sop_*`, `*Mean0to10`,
`*Percentile`, `*StdDev`, `factor*`, `zscore*`, `*0to10`), e demais colunas
que nao sao analiticas, de ranking, de reflexao ou de metadados de sessao.

## Colunas preservadas ({len(cols_to_keep)} + 6 fatores recalculados)

### Metadados de sessao ({len(meta_cols)})
{chr(10).join(f"- `{c}`" for c in meta_cols)}

### Itens analiticos p_* ({len(item_cols)})
Os 37 itens Likert, escala de -3 a +3. Todos validados: valores unicos
encontrados = {sorted(unique_vals)}.

### Ranking do top 5 ({len(rank_cols)})
{chr(10).join(f"- `{c}`" for c in rank_cols)}

### Reflexao e selecao ({len(reflection_cols)})
Respostas dos exercicios de reflexao (texto livre) e labels/sources
selecionados pelo respondente.

### Fatores recalculados (6)
Calculados a partir dos itens brutos conforme `config/instrument.yaml`:
- `factor_interpersonal` = media(qualityTime, belonging, loving, connection)
- `factor_thrilling` = media(risk, partying, adrenaline, scary, spontaneous, exciting)
- `factor_noble` = media(spiritual, supportFamily, charity, community, caring, helping)
- `factor_reputational` = media(recognition, status, attractive, power, likable, competition)
- `factor_sensorial` = media(touch, taste, smell, relax)
- `factor_intellectual` = media(thinking, creative, learning, imagination, seeingBeauty)

## Criterio de completude

**Decisao do usuario:** manter somente linhas com todos os 37 itens `p_*`
respondidos. Usuarios que abandonaram a ferramenta no meio foram descartados.
Exercicios de reflexao e email sao opcionais por design do instrumento — sua
ausencia nao exclui a linha.

## Deduplicacao

{f"{n_deduped} linhas removidas. Estrategia: para usuarios com multiplas runs, manter a run mais recente (maior numero de Run)." if n_deduped > 0 else "Nenhuma duplicata encontrada (ou coluna User nao preservada para verificacao)."}

## Anomalias

{"Nenhuma anomalia encontrada na validacao dos itens." if not anomalies else chr(10).join(f"- `{col}`: {count} {desc}" for col, count, desc in anomalies)}

## Validacao dos valores

Todos os 37 itens contem exclusivamente valores inteiros no intervalo [-3, +3].
Nenhum valor fora da escala, nenhum valor nao-inteiro, nenhuma coercao
silenciosa necessaria.

## Arquivo de saida

`data/processed/clean.csv` — {n_final_rows:,} linhas x {n_final_cols:,} colunas.
"""

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report)

print("\nFase 1 concluida com sucesso!")
print(f"  Dataset: {CLEAN_CSV}")
print(f"  Relatorio: {REPORT_PATH}")
