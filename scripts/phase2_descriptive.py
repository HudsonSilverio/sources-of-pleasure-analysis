"""
Phase 2 — Descriptive analysis.
Calculates comprehensive descriptive statistics for all 37 items and 6 factors,
generates exploratory charts, and writes the descriptive report.
"""

import yaml
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_CSV = PROJECT_ROOT / "data" / "processed" / "clean.csv"
CONFIG_YAML = PROJECT_ROOT / "config" / "instrument.yaml"
REPORT_PATH = PROJECT_ROOT / "outputs" / "reports" / "phase2_descriptive.md"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures" / "exploratory" / "phase2"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Load config and data
# ---------------------------------------------------------------------------
with open(CONFIG_YAML, encoding="utf-8") as f:
    config = yaml.safe_load(f)

df = pd.read_csv(CLEAN_CSV)
N = len(df)
print(f"Dataset carregado: {N} linhas")

ITEM_COLS = [item["variavel"] for item in config["itens"]]
ITEM_LABELS = {item["variavel"]: item["rotulo"] for item in config["itens"]}
FACTOR_COLS = [f"factor_{name}" for name in config["fatores"]]
FACTOR_LABELS = {f"factor_{name}": fdef["rotulo"] for name, fdef in config["fatores"].items()}
SCALE_VALUES = list(range(-3, 4))

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def shannon_entropy(series, possible_values=SCALE_VALUES):
    """Shannon entropy of a discrete distribution (base 2)."""
    counts = series.value_counts()
    total = counts.sum()
    probs = np.array([counts.get(v, 0) / total for v in possible_values])
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))


def max_entropy(n_categories):
    """Maximum possible entropy for n categories (uniform distribution)."""
    return np.log2(n_categories)


def bimodality_coefficient(series):
    """
    Bimodality coefficient: BC = (skew^2 + 1) / (kurtosis_excess + 3*(n-1)^2/((n-2)*(n-3)))
    BC > 0.555 suggests bimodality.
    """
    n = len(series)
    skew = series.skew()
    kurt = series.kurtosis()  # excess kurtosis
    numerator = skew**2 + 1
    denominator = kurt + (3 * (n - 1)**2) / ((n - 2) * (n - 3))
    if denominator == 0:
        return np.nan
    return numerator / denominator


def trimmed_mean(series, proportion=0.05):
    """Trimmed mean removing proportion from each tail."""
    return stats.trim_mean(series.dropna().values, proportion)


def compute_descriptive_stats(series, is_likert=True):
    """Compute all descriptive statistics for a single variable."""
    s = series.dropna()
    n = len(s)
    result = {}

    # --- Central tendency ---
    result["n"] = n
    result["mean"] = s.mean()
    result["median"] = s.median()
    result["mode"] = s.mode().iloc[0] if len(s.mode()) > 0 else np.nan
    result["trimmed_mean_5"] = trimmed_mean(s, 0.05)

    # --- Dispersion ---
    result["std"] = s.std()
    result["variance"] = s.var()
    result["mad"] = (s - s.median()).abs().median()  # MAD
    result["iqr"] = s.quantile(0.75) - s.quantile(0.25)
    result["range"] = s.max() - s.min()
    result["cv"] = (s.std() / abs(s.mean()) * 100) if abs(s.mean()) > 0.01 else np.nan

    # --- Position ---
    result["min"] = s.min()
    result["max"] = s.max()
    result["q1"] = s.quantile(0.25)
    result["q2"] = s.quantile(0.50)
    result["q3"] = s.quantile(0.75)
    for p in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
        result[f"p{p}"] = s.quantile(p / 100)

    # --- Shape ---
    result["skewness"] = s.skew()
    result["kurtosis"] = s.kurtosis()  # excess kurtosis

    # Normality tests
    if n >= 20:
        try:
            stat_sw, p_sw = stats.shapiro(s.sample(min(5000, n), random_state=42))
            result["shapiro_wilk_stat"] = stat_sw
            result["shapiro_wilk_p"] = p_sw
        except Exception:
            result["shapiro_wilk_stat"] = np.nan
            result["shapiro_wilk_p"] = np.nan

        try:
            stat_da, p_da = stats.normaltest(s)
            result["dagostino_stat"] = stat_da
            result["dagostino_p"] = p_da
        except Exception:
            result["dagostino_stat"] = np.nan
            result["dagostino_p"] = np.nan

        try:
            ad_result = stats.anderson(s, dist="norm")
            result["anderson_darling_stat"] = ad_result.statistic
        except Exception:
            result["anderson_darling_stat"] = np.nan

    # --- Precision ---
    result["sem"] = s.std() / np.sqrt(n)
    result["ci95_lower"] = result["mean"] - 1.96 * result["sem"]
    result["ci95_upper"] = result["mean"] + 1.96 * result["sem"]

    # --- Outliers ---
    z_scores = (s - s.mean()) / s.std()
    result["outliers_zscore"] = int((z_scores.abs() > 3).sum())

    modified_z = 0.6745 * (s - s.median()) / result["mad"] if result["mad"] > 0 else pd.Series([0]*n)
    result["outliers_modified_z"] = int((modified_z.abs() > 3.5).sum()) if result["mad"] > 0 else 0

    iqr_lower = result["q1"] - 1.5 * result["iqr"]
    iqr_upper = result["q3"] + 1.5 * result["iqr"]
    result["outliers_iqr"] = int(((s < iqr_lower) | (s > iqr_upper)).sum())

    result["unique_values"] = s.nunique()

    # --- Diagnostics ---
    result["mean_median_diff"] = result["mean"] - result["median"]
    result["std_mad_ratio"] = result["std"] / result["mad"] if result["mad"] > 0 else np.nan

    # --- Missing ---
    result["missing_n"] = int(series.isna().sum())
    result["missing_pct"] = series.isna().mean() * 100

    # --- Likert-specific ---
    if is_likert:
        result["ceiling_pct"] = (s == 3).mean() * 100
        result["floor_pct"] = (s == -3).mean() * 100
        result["top2_pct"] = (s >= 2).mean() * 100
        result["bottom2_pct"] = (s <= -2).mean() * 100
        result["net_agreement"] = result["top2_pct"] - result["bottom2_pct"]
        result["entropy"] = shannon_entropy(s)
        result["entropy_max"] = max_entropy(len(SCALE_VALUES))
        result["entropy_normalized"] = result["entropy"] / result["entropy_max"]
        result["bimodality_coeff"] = bimodality_coefficient(s)

        # Frequencies
        for v in SCALE_VALUES:
            result[f"freq_{v}"] = int((s == v).sum())
            result[f"freq_pct_{v}"] = (s == v).mean() * 100

    return result


# ---------------------------------------------------------------------------
# Compute statistics
# ---------------------------------------------------------------------------
print("\nCalculando estatisticas descritivas para 37 itens...")
item_stats = {}
for col in ITEM_COLS:
    item_stats[col] = compute_descriptive_stats(df[col], is_likert=True)

print("Calculando estatisticas descritivas para 6 fatores...")
factor_stats = {}
for col in FACTOR_COLS:
    factor_stats[col] = compute_descriptive_stats(df[col], is_likert=False)

# ---------------------------------------------------------------------------
# Build summary DataFrames
# ---------------------------------------------------------------------------
items_df = pd.DataFrame(item_stats).T
items_df.index.name = "variable"
items_df["label"] = items_df.index.map(ITEM_LABELS)

factors_df = pd.DataFrame(factor_stats).T
factors_df.index.name = "variable"
factors_df["label"] = factors_df.index.map(FACTOR_LABELS)

print(f"\nEstatisticas calculadas: {len(items_df.columns)} medidas por item, "
      f"{len(factors_df.columns)} medidas por fator")

# ---------------------------------------------------------------------------
# Save computed statistics as reusable CSVs
# ---------------------------------------------------------------------------
STATS_DIR = PROJECT_ROOT / "data" / "processed"
items_csv = STATS_DIR / "phase2_item_stats.csv"
factors_csv = STATS_DIR / "phase2_factor_stats.csv"

items_df.to_csv(items_csv)
factors_df.to_csv(factors_csv)
print(f"\nEstatisticas salvas:")
print(f"  {items_csv}")
print(f"  {factors_csv}")

# ---------------------------------------------------------------------------
# CHARTS
# ---------------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "figure.dpi": 150,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 10,
})

print("\nGerando graficos exploratórios...")


def save_fig(fig, name):
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  Salvo: {path.name}")


# --- Chart 1: Items ranked by mean ---
fig, ax = plt.subplots(figsize=(12, 12))
fig.suptitle("Quais fontes de prazer sao mais valorizadas?",
             fontsize=14, fontweight="bold", y=0.98)
sorted_items = items_df.sort_values("mean", ascending=True)
colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in sorted_items["mean"]]
bars = ax.barh(range(len(sorted_items)), sorted_items["mean"], color=colors, height=0.7)
ax.set_yticks(range(len(sorted_items)))
ax.set_yticklabels([sorted_items["label"].iloc[i] for i in range(len(sorted_items))], fontsize=9)
ax.set_xlabel("Media (-3 a +3)")
ax.axvline(x=0, color="black", linewidth=0.8)
# CI error bars
for i, (idx, row) in enumerate(sorted_items.iterrows()):
    ax.plot([row["ci95_lower"], row["ci95_upper"]], [i, i], color="black", linewidth=1, alpha=0.5)
ax.set_title(f"N = {N} | Barras = media | Linhas = IC 95%", fontsize=9, color="gray")
save_fig(fig, "01_items_ranked_by_mean")


# --- Chart 2: Factors ranked by mean ---
fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Qual categoria de prazer domina?",
             fontsize=14, fontweight="bold")
sorted_factors = factors_df.sort_values("mean", ascending=True)
colors = ["#3498db" for _ in sorted_factors.index]
ax.barh(range(len(sorted_factors)), sorted_factors["mean"], color=colors, height=0.5)
ax.set_yticks(range(len(sorted_factors)))
ax.set_yticklabels([sorted_factors["label"].iloc[i] for i in range(len(sorted_factors))], fontsize=11)
ax.set_xlabel("Media (-3 a +3)")
ax.axvline(x=0, color="black", linewidth=0.8)
for i, (idx, row) in enumerate(sorted_factors.iterrows()):
    ax.plot([row["ci95_lower"], row["ci95_upper"]], [i, i], color="black", linewidth=1.5, alpha=0.5)
    ax.text(row["mean"] + 0.05, i, f'{row["mean"]:.2f}', va="center", fontsize=10)
ax.set_title(f"N = {N} | Barras = media | Linhas = IC 95%", fontsize=9, color="gray")
save_fig(fig, "02_factors_ranked_by_mean")


# --- Chart 3: Frequency heatmap ---
fig, ax = plt.subplots(figsize=(14, 12))
fig.suptitle("Como as pessoas distribuiram suas respostas?",
             fontsize=14, fontweight="bold", y=0.98)
sorted_by_mean = items_df.sort_values("mean", ascending=False)
freq_matrix = []
for idx in sorted_by_mean.index:
    row_pcts = [sorted_by_mean.loc[idx, f"freq_pct_{v}"] for v in SCALE_VALUES]
    freq_matrix.append(row_pcts)
freq_matrix = np.array(freq_matrix)
im = ax.imshow(freq_matrix, aspect="auto", cmap="YlOrRd", vmin=0, vmax=50)
ax.set_xticks(range(7))
ax.set_xticklabels([str(v) for v in SCALE_VALUES])
ax.set_xlabel("Resposta (-3 = Discordo totalmente ... +3 = Concordo totalmente)")
ax.set_yticks(range(len(sorted_by_mean)))
ax.set_yticklabels([sorted_by_mean["label"].iloc[i] for i in range(len(sorted_by_mean))], fontsize=8)
# Add text annotations
for i in range(len(sorted_by_mean)):
    for j in range(7):
        val = freq_matrix[i, j]
        color = "white" if val > 25 else "black"
        ax.text(j, i, f"{val:.0f}%", ha="center", va="center", fontsize=7, color=color)
plt.colorbar(im, ax=ax, label="% de respondentes", shrink=0.8)
ax.set_title("Ordenado por media (maior no topo) | Valores = % de respondentes", fontsize=9, color="gray")
save_fig(fig, "03_frequency_heatmap")


# --- Chart 4: Factor histograms ---
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
fig.suptitle("Os fatores tem distribuicao normal ou enviesada?",
             fontsize=14, fontweight="bold")
for i, col in enumerate(FACTOR_COLS):
    ax = axes[i // 3, i % 3]
    data = df[col].dropna()
    ax.hist(data, bins=30, color="#3498db", edgecolor="white", alpha=0.8)
    ax.axvline(data.mean(), color="red", linestyle="--", linewidth=1.5, label=f"Media={data.mean():.2f}")
    ax.axvline(data.median(), color="orange", linestyle="-.", linewidth=1.5, label=f"Mediana={data.median():.2f}")
    ax.set_title(FACTOR_LABELS[col], fontsize=11)
    ax.set_xlabel("Score")
    ax.legend(fontsize=8)
    skew_val = factors_df.loc[col, "skewness"]
    ax.text(0.95, 0.95, f"skew={skew_val:.2f}", transform=ax.transAxes,
            ha="right", va="top", fontsize=8, color="gray")
plt.tight_layout()
save_fig(fig, "04_factor_histograms")


# --- Chart 5: Items ranked by SD (polarization) ---
fig, ax = plt.subplots(figsize=(12, 12))
fig.suptitle("Quais fontes de prazer geram mais discordancia entre as pessoas?",
             fontsize=14, fontweight="bold", y=0.98)
sorted_sd = items_df.sort_values("std", ascending=True)
colors = ["#e67e22" if v > sorted_sd["std"].median() else "#95a5a6" for v in sorted_sd["std"]]
ax.barh(range(len(sorted_sd)), sorted_sd["std"], color=colors, height=0.7)
ax.set_yticks(range(len(sorted_sd)))
ax.set_yticklabels([sorted_sd["label"].iloc[i] for i in range(len(sorted_sd))], fontsize=9)
ax.set_xlabel("Desvio Padrao")
ax.axvline(x=sorted_sd["std"].median(), color="black", linewidth=0.8, linestyle="--", alpha=0.5)
ax.set_title("Laranja = acima da mediana (mais polarizador) | Cinza = abaixo", fontsize=9, color="gray")
save_fig(fig, "05_items_ranked_by_sd")


# --- Chart 6: Net agreement (diverging bars) ---
fig, ax = plt.subplots(figsize=(12, 12))
fig.suptitle("Qual o saldo liquido de concordancia de cada fonte de prazer?",
             fontsize=14, fontweight="bold", y=0.98)
sorted_net = items_df.sort_values("net_agreement", ascending=True)
colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in sorted_net["net_agreement"]]
ax.barh(range(len(sorted_net)), sorted_net["net_agreement"], color=colors, height=0.7)
ax.set_yticks(range(len(sorted_net)))
ax.set_yticklabels([sorted_net["label"].iloc[i] for i in range(len(sorted_net))], fontsize=9)
ax.set_xlabel("Net Agreement (Top-2 box - Bottom-2 box, em pontos percentuais)")
ax.axvline(x=0, color="black", linewidth=0.8)
ax.set_title("Verde = mais gente concorda | Vermelho = mais gente discorda", fontsize=9, color="gray")
save_fig(fig, "06_net_agreement")


# --- Chart 7: Ceiling and floor effects ---
fig, ax = plt.subplots(figsize=(12, 12))
fig.suptitle("Onde a escala nao captura diferencas? (efeitos de teto e piso)",
             fontsize=14, fontweight="bold", y=0.98)
sorted_ceil = items_df.sort_values("ceiling_pct", ascending=True)
y_pos = range(len(sorted_ceil))
ax.barh(y_pos, sorted_ceil["ceiling_pct"], height=0.4, color="#3498db",
        label="Teto (% no +3)", align="edge")
ax.barh([y - 0.4 for y in y_pos], -sorted_ceil["floor_pct"].values, height=0.4,
        color="#e74c3c", label="Piso (% no -3)", align="edge")
ax.set_yticks(y_pos)
ax.set_yticklabels([sorted_ceil["label"].iloc[i] for i in range(len(sorted_ceil))], fontsize=9)
ax.set_xlabel("% de respondentes")
ax.axvline(x=0, color="black", linewidth=0.8)
ax.axvline(x=25, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)
ax.axvline(x=-25, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)
ax.legend(loc="lower right")
ax.set_title("Linhas tracejadas = limiar de 25% (efeito substancial)", fontsize=9, color="gray")
save_fig(fig, "07_ceiling_floor_effects")


# --- Chart 8: Skewness ---
fig, ax = plt.subplots(figsize=(12, 12))
fig.suptitle("Quais fontes de prazer tem distribuicao assimetrica e para que lado?",
             fontsize=14, fontweight="bold", y=0.98)
sorted_skew = items_df.sort_values("skewness", ascending=True)
colors = ["#9b59b6" if abs(v) > 1 else ("#3498db" if abs(v) > 0.5 else "#95a5a6")
          for v in sorted_skew["skewness"]]
ax.barh(range(len(sorted_skew)), sorted_skew["skewness"], color=colors, height=0.7)
ax.set_yticks(range(len(sorted_skew)))
ax.set_yticklabels([sorted_skew["label"].iloc[i] for i in range(len(sorted_skew))], fontsize=9)
ax.set_xlabel("Skewness (negativo = maioria concorda | positivo = maioria discorda)")
ax.axvline(x=0, color="black", linewidth=0.8)
ax.axvline(x=-1, color="gray", linewidth=0.8, linestyle="--", alpha=0.3)
ax.axvline(x=1, color="gray", linewidth=0.8, linestyle="--", alpha=0.3)
ax.set_title("Roxo = |skew| > 1 (substancial) | Azul = |skew| > 0.5 | Cinza = simetrico",
             fontsize=9, color="gray")
save_fig(fig, "08_skewness")


# --- Chart 9: Entropy ---
fig, ax = plt.subplots(figsize=(12, 12))
fig.suptitle("Onde ha consenso vs. dispersao total nas respostas?",
             fontsize=14, fontweight="bold", y=0.98)
sorted_ent = items_df.sort_values("entropy_normalized", ascending=True)
colors = ["#e67e22" if v > 0.85 else ("#2ecc71" if v < 0.7 else "#95a5a6")
          for v in sorted_ent["entropy_normalized"]]
ax.barh(range(len(sorted_ent)), sorted_ent["entropy_normalized"], color=colors, height=0.7)
ax.set_yticks(range(len(sorted_ent)))
ax.set_yticklabels([sorted_ent["label"].iloc[i] for i in range(len(sorted_ent))], fontsize=9)
ax.set_xlabel("Entropia normalizada (0 = consenso total | 1 = dispersao uniforme)")
ax.axvline(x=0.85, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)
ax.set_title("Verde = consenso forte | Cinza = moderado | Laranja = alta dispersao",
             fontsize=9, color="gray")
save_fig(fig, "09_entropy")


# --- Chart 10: Bimodality ---
fig, ax = plt.subplots(figsize=(12, 12))
fig.suptitle("Quais fontes de prazer dividem as pessoas em dois grupos?",
             fontsize=14, fontweight="bold", y=0.98)
sorted_bim = items_df.sort_values("bimodality_coeff", ascending=True)
colors = ["#e74c3c" if v > 0.555 else "#95a5a6" for v in sorted_bim["bimodality_coeff"]]
ax.barh(range(len(sorted_bim)), sorted_bim["bimodality_coeff"], color=colors, height=0.7)
ax.set_yticks(range(len(sorted_bim)))
ax.set_yticklabels([sorted_bim["label"].iloc[i] for i in range(len(sorted_bim))], fontsize=9)
ax.set_xlabel("Coeficiente de Bimodalidade")
ax.axvline(x=0.555, color="red", linewidth=1, linestyle="--", alpha=0.7)
ax.set_title("Vermelho = BC > 0.555 (candidato a bimodal) | Linha vermelha = limiar",
             fontsize=9, color="gray")
save_fig(fig, "10_bimodality")


# ---------------------------------------------------------------------------
# REPORT
# ---------------------------------------------------------------------------
print("\nGerando relatorio...")


def fmt(val, decimals=2):
    """Format a number for the report."""
    if pd.isna(val):
        return "N/A"
    if isinstance(val, (int, np.integer)):
        return str(val)
    return f"{val:.{decimals}f}"


# Build the report
report_lines = []
report_lines.append("# Fase 2 — Analise Descritiva\n")
report_lines.append(f"**Dataset:** `data/processed/clean.csv` — {N:,} respondentes completos\n")
report_lines.append("**Premissa declarada:** itens Likert de 7 pontos (-3 a +3) tratados como")
report_lines.append("intervalares, convencao aceita na literatura para escalas de 7+ pontos.")
report_lines.append("Onde distribuicoes forem muito assimetricas, preferir Spearman nas fases seguintes.\n")

# --- Main findings ---
report_lines.append("---\n")
report_lines.append("## Leitura principal\n")

# Top 5 / Bottom 5 by mean
sorted_by_mean = items_df.sort_values("mean", ascending=False)
report_lines.append("### Fontes de prazer mais valorizadas (top 5 por media)")
report_lines.append("| Rank | Item | Media | IC 95% | Net Agreement |")
report_lines.append("|------|------|-------|--------|---------------|")
for i, (idx, row) in enumerate(sorted_by_mean.head(5).iterrows()):
    report_lines.append(
        f"| {i+1} | {row['label']} | {fmt(row['mean'])} | "
        f"[{fmt(row['ci95_lower'])}, {fmt(row['ci95_upper'])}] | "
        f"{fmt(row['net_agreement'], 1)}% |"
    )

report_lines.append("\n### Fontes de prazer menos valorizadas (bottom 5 por media)")
report_lines.append("| Rank | Item | Media | IC 95% | Net Agreement |")
report_lines.append("|------|------|-------|--------|---------------|")
for i, (idx, row) in enumerate(sorted_by_mean.tail(5).iloc[::-1].iterrows()):
    report_lines.append(
        f"| {37-i} | {row['label']} | {fmt(row['mean'])} | "
        f"[{fmt(row['ci95_lower'])}, {fmt(row['ci95_upper'])}] | "
        f"{fmt(row['net_agreement'], 1)}% |"
    )

# Most polarizing
sorted_by_sd = items_df.sort_values("std", ascending=False)
report_lines.append("\n### Itens mais polarizadores (top 5 por desvio padrao)")
report_lines.append("| Item | DP | MAD | Entropia norm. | Bimodalidade |")
report_lines.append("|------|-----|-----|----------------|-------------|")
for i, (idx, row) in enumerate(sorted_by_sd.head(5).iterrows()):
    bim_flag = " **BIMODAL**" if row["bimodality_coeff"] > 0.555 else ""
    report_lines.append(
        f"| {row['label']} | {fmt(row['std'])} | {fmt(row['mad'])} | "
        f"{fmt(row['entropy_normalized'])} | {fmt(row['bimodality_coeff'])}{bim_flag} |"
    )

# Ceiling effects
ceiling_items = items_df[items_df["ceiling_pct"] > 25].sort_values("ceiling_pct", ascending=False)
report_lines.append(f"\n### Efeitos de teto (itens com > 25% no +3): {len(ceiling_items)}")
if len(ceiling_items) > 0:
    report_lines.append("| Item | % no +3 | Media |")
    report_lines.append("|------|---------|-------|")
    for idx, row in ceiling_items.iterrows():
        report_lines.append(f"| {row['label']} | {fmt(row['ceiling_pct'], 1)}% | {fmt(row['mean'])} |")
else:
    report_lines.append("Nenhum item com efeito de teto substancial.")

# Floor effects
floor_items = items_df[items_df["floor_pct"] > 25].sort_values("floor_pct", ascending=False)
report_lines.append(f"\n### Efeitos de piso (itens com > 25% no -3): {len(floor_items)}")
if len(floor_items) > 0:
    report_lines.append("| Item | % no -3 | Media |")
    report_lines.append("|------|---------|-------|")
    for idx, row in floor_items.iterrows():
        report_lines.append(f"| {row['label']} | {fmt(row['floor_pct'], 1)}% | {fmt(row['mean'])} |")
else:
    report_lines.append("Nenhum item com efeito de piso substancial.")

# Skewed items
skewed_items = items_df[items_df["skewness"].abs() > 1].sort_values("skewness")
report_lines.append(f"\n### Itens com assimetria substancial (|skewness| > 1): {len(skewed_items)}")
if len(skewed_items) > 0:
    report_lines.append("| Item | Skewness | Direcao |")
    report_lines.append("|------|----------|---------|")
    for idx, row in skewed_items.iterrows():
        direction = "maioria concorda" if row["skewness"] < 0 else "maioria discorda"
        report_lines.append(f"| {row['label']} | {fmt(row['skewness'])} | {direction} |")

# Bimodal items
bimodal_items = items_df[items_df["bimodality_coeff"] > 0.555].sort_values("bimodality_coeff", ascending=False)
report_lines.append(f"\n### Itens candidatos a bimodais (BC > 0.555): {len(bimodal_items)}")
if len(bimodal_items) > 0:
    report_lines.append("| Item | BC | Skewness | DP |")
    report_lines.append("|------|-----|----------|-----|")
    for idx, row in bimodal_items.iterrows():
        report_lines.append(
            f"| {row['label']} | {fmt(row['bimodality_coeff'])} | "
            f"{fmt(row['skewness'])} | {fmt(row['std'])} |"
        )
else:
    report_lines.append("Nenhum item com coeficiente de bimodalidade acima do limiar.")

# --- Factors summary ---
report_lines.append("\n---\n")
report_lines.append("## Fatores\n")
report_lines.append("| Fator | Media | Mediana | DP | Skewness | Kurtosis | IC 95% |")
report_lines.append("|-------|-------|---------|-----|----------|----------|--------|")
for col in FACTOR_COLS:
    r = factor_stats[col]
    report_lines.append(
        f"| {FACTOR_LABELS[col]} | {fmt(r['mean'])} | {fmt(r['median'])} | "
        f"{fmt(r['std'])} | {fmt(r['skewness'])} | {fmt(r['kurtosis'])} | "
        f"[{fmt(r['ci95_lower'])}, {fmt(r['ci95_upper'])}] |"
    )

# --- Full item table ---
report_lines.append("\n---\n")
report_lines.append("## Tabela completa — 37 itens\n")

# Table 1: Central tendency and dispersion
report_lines.append("### Tendencia central e dispersao\n")
report_lines.append("| Item | Media | Mediana | Moda | Trim.Mean | DP | Var | MAD | IQR | CV | SEM | IC 95% |")
report_lines.append("|------|-------|---------|------|-----------|-----|-----|-----|-----|----|-----|--------|")
for idx, row in sorted_by_mean.iterrows():
    cv_str = fmt(row["cv"], 1) if not pd.isna(row["cv"]) else "N/A*"
    report_lines.append(
        f"| {row['label']} | {fmt(row['mean'])} | {fmt(row['median'])} | "
        f"{fmt(row['mode'], 0)} | {fmt(row['trimmed_mean_5'])} | {fmt(row['std'])} | "
        f"{fmt(row['variance'])} | {fmt(row['mad'])} | {fmt(row['iqr'])} | "
        f"{cv_str} | {fmt(row['sem'], 3)} | [{fmt(row['ci95_lower'])}, {fmt(row['ci95_upper'])}] |"
    )
report_lines.append("\n*N/A: CV indefinido quando media ≈ 0.\n")

# Table 2: Position
report_lines.append("### Posicao (percentis)\n")
report_lines.append("| Item | Min | P1 | P5 | P10 | Q1 | Q2 | Q3 | P90 | P95 | P99 | Max |")
report_lines.append("|------|-----|----|----|-----|----|----|----|----|-----|-----|-----|")
for idx, row in sorted_by_mean.iterrows():
    report_lines.append(
        f"| {row['label']} | {fmt(row['min'],0)} | {fmt(row['p1'])} | {fmt(row['p5'])} | "
        f"{fmt(row['p10'])} | {fmt(row['q1'])} | {fmt(row['q2'])} | {fmt(row['q3'])} | "
        f"{fmt(row['p90'])} | {fmt(row['p95'])} | {fmt(row['p99'])} | {fmt(row['max'],0)} |"
    )

# Table 3: Shape and normality
report_lines.append("\n### Forma e normalidade\n")
report_lines.append("**Nota:** com N = {:,}, todos os testes de normalidade rejeitam H0.".format(N))
report_lines.append("O que importa e a **magnitude** do desvio, nao o p-valor.\n")
report_lines.append("| Item | Skewness | Kurtosis | Shapiro-W | D'Agostino | Anderson-D | Mean-Med | DP/MAD |")
report_lines.append("|------|----------|----------|-----------|------------|------------|----------|--------|")
for idx, row in sorted_by_mean.iterrows():
    report_lines.append(
        f"| {row['label']} | {fmt(row['skewness'])} | {fmt(row['kurtosis'])} | "
        f"{fmt(row['shapiro_wilk_stat'], 4)} | {fmt(row['dagostino_stat'], 1)} | "
        f"{fmt(row['anderson_darling_stat'], 1)} | {fmt(row['mean_median_diff'])} | "
        f"{fmt(row['std_mad_ratio'])} |"
    )

# Table 4: Frequencies
report_lines.append("\n### Frequencias de resposta (%) \n")
report_lines.append("| Item | -3 | -2 | -1 | 0 | +1 | +2 | +3 | Piso% | Teto% |")
report_lines.append("|------|----|----|----|----|----|----|-----|-------|-------|")
for idx, row in sorted_by_mean.iterrows():
    report_lines.append(
        f"| {row['label']} | "
        + " | ".join(f"{fmt(row[f'freq_pct_{v}'], 1)}" for v in SCALE_VALUES)
        + f" | {fmt(row['floor_pct'], 1)} | {fmt(row['ceiling_pct'], 1)} |"
    )

# Table 5: Likert-specific indicators
report_lines.append("\n### Indicadores Likert\n")
report_lines.append("| Item | Top-2% | Bottom-2% | Net Agr. | Entropia | Ent.Norm | BC | Outliers IQR | Outliers Z | Outliers ModZ |")
report_lines.append("|------|--------|-----------|----------|----------|----------|----|-------------|------------|---------------|")
for idx, row in sorted_by_mean.iterrows():
    bc_flag = " *" if row["bimodality_coeff"] > 0.555 else ""
    report_lines.append(
        f"| {row['label']} | {fmt(row['top2_pct'], 1)} | {fmt(row['bottom2_pct'], 1)} | "
        f"{fmt(row['net_agreement'], 1)} | {fmt(row['entropy'])} | {fmt(row['entropy_normalized'])} | "
        f"{fmt(row['bimodality_coeff'])}{bc_flag} | {fmt(row['outliers_iqr'], 0)} | "
        f"{fmt(row['outliers_zscore'], 0)} | {fmt(row['outliers_modified_z'], 0)} |"
    )
report_lines.append("\n\\* BC > 0.555 = candidato a bimodal\n")

# --- Factors full table ---
report_lines.append("---\n")
report_lines.append("## Tabela completa — 6 fatores\n")
report_lines.append("| Fator | Media | Mediana | Moda | Trim.Mean | DP | Var | MAD | IQR | Skew | Kurt | SEM | IC 95% | Outliers IQR |")
report_lines.append("|-------|-------|---------|------|-----------|-----|-----|-----|-----|------|------|-----|--------|-------------|")
for col in FACTOR_COLS:
    r = factor_stats[col]
    report_lines.append(
        f"| {FACTOR_LABELS[col]} | {fmt(r['mean'])} | {fmt(r['median'])} | "
        f"{fmt(r['mode'])} | {fmt(r['trimmed_mean_5'])} | {fmt(r['std'])} | "
        f"{fmt(r['variance'])} | {fmt(r['mad'])} | {fmt(r['iqr'])} | "
        f"{fmt(r['skewness'])} | {fmt(r['kurtosis'])} | {fmt(r['sem'], 3)} | "
        f"[{fmt(r['ci95_lower'])}, {fmt(r['ci95_upper'])}] | {fmt(r['outliers_iqr'], 0)} |"
    )

# --- Charts list ---
report_lines.append("\n---\n")
report_lines.append("## Graficos exploratórios\n")
report_lines.append("Todos em `outputs/figures/exploratory/phase2/`:\n")
chart_list = [
    ("01_items_ranked_by_mean.png", "Quais fontes de prazer sao mais valorizadas?"),
    ("02_factors_ranked_by_mean.png", "Qual categoria de prazer domina?"),
    ("03_frequency_heatmap.png", "Como as pessoas distribuiram suas respostas?"),
    ("04_factor_histograms.png", "Os fatores tem distribuicao normal ou enviesada?"),
    ("05_items_ranked_by_sd.png", "Quais fontes de prazer geram mais discordancia?"),
    ("06_net_agreement.png", "Qual o saldo liquido de concordancia de cada item?"),
    ("07_ceiling_floor_effects.png", "Onde a escala nao captura diferencas?"),
    ("08_skewness.png", "Quais itens tem distribuicao assimetrica e para que lado?"),
    ("09_entropy.png", "Onde ha consenso vs. dispersao total?"),
    ("10_bimodality.png", "Quais itens dividem as pessoas em dois grupos?"),
]
for fname, question in chart_list:
    report_lines.append(f"- `{fname}` — {question}")

report_lines.append("\n---\n")
report_lines.append(f"*Gerado a partir de `data/processed/clean.csv` — N = {N:,}*\n")

# Write report
report_text = "\n".join(report_lines)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report_text)

print(f"\nFase 2 concluida!")
print(f"  Relatorio: {REPORT_PATH}")
print(f"  Graficos: {FIG_DIR}")
