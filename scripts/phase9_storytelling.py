"""
phase9_storytelling.py — Data storytelling and visualization (Phase 9).

Generates 8 Statista-style charts (one per insight) and a narrative
markdown document with plain-language explanations.

Usage:
    python scripts/phase9_storytelling.py
"""

import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from scipy import stats
from sklearn.mixture import GaussianMixture

from src.viz import (
    COLORS, FONT, SOURCE_LINE,
    create_statista_figure, save_final_figure,
)

# ---------------------------------------------------------------------------
# Paths & config
# ---------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data" / "processed"
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "reports"
SEED = 42

np.random.seed(SEED)

print("Carregando dados...")
clean_df = pd.read_csv(DATA_DIR / "clean.csv")
item_stats = pd.read_csv(DATA_DIR / "phase2_item_stats.csv", index_col=0)
factor_stats = pd.read_csv(DATA_DIR / "phase2_factor_stats.csv", index_col=0)
profiles = pd.read_csv(DATA_DIR / "phase2_respondent_profiles.csv", index_col=0)

with open(CONFIG_DIR / "instrument.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

item_labels = {it["variavel"]: it["rotulo"] for it in config["itens"]}
factor_labels = {k: v.get("rotulo", k) for k, v in config["fatores"].items()}
item_cols = [it["variavel"] for it in config["itens"]]
factor_names = list(config["fatores"].keys())
factor_cols = [f"factor_{f}" for f in factor_names]

N = len(clean_df)
print(f"  N = {N:,}")

# Track generated figures for narrative
figures = {}


# =========================================================================
# I01 — Rir e o prazer mais universal
# =========================================================================
def chart_i01():
    print("\n  I01: Ranking de prazeres...")
    top = item_stats.sort_values("net_agreement", ascending=False).head(10)

    labels = [item_labels.get(idx, idx) for idx in top.index]
    values = top["net_agreement"].values

    fig, ax = create_statista_figure(
        title="Laughing is the most universal source of pleasure",
        subtitle="Top 10 items by net agreement (% agree minus % disagree)",
    )

    colors = [COLORS["primary"] if i == 0 else COLORS["light_blue"]
              for i in range(len(values))]

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, values, color=colors, height=0.65, edgecolor="none")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9, fontfamily="Arial")
    ax.invert_yaxis()
    ax.set_xlabel("")

    # Data labels
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(val + 0.8, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", ha="left",
                fontsize=9, fontfamily="Arial", color=COLORS["text_dark"])

    ax.set_xlim(0, max(values) + 8)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(left=False, bottom=False, labelbottom=False)
    ax.xaxis.set_visible(False)

    path = save_final_figure(fig, "I01_ranking")
    figures["I01"] = path


# =========================================================================
# I02 — Espiritualidade e o grande divisor
# =========================================================================
def chart_i02():
    print("\n  I02: Espiritualidade bimodal...")
    spiritual = clean_df["p_spiritual"].values

    fig, ax = create_statista_figure(
        title="Spirituality splits people into two clear groups",
        subtitle="Distribution of responses to 'Spiritual / religious feelings'",
    )

    # Histogram
    counts, bins, patches = ax.hist(
        spiritual, bins=7, range=(-3.5, 3.5),
        color=COLORS["pale_blue"], edgecolor=COLORS["bg_white"],
        linewidth=1.5, alpha=0.8, zorder=2,
    )

    # Fit GMM for overlay curves
    gmm = GaussianMixture(n_components=2, random_state=SEED)
    gmm.fit(spiritual.reshape(-1, 1))
    x_range = np.linspace(-3.5, 3.5, 200)

    # Sort components by mean
    order = np.argsort(gmm.means_.flatten())
    means = gmm.means_.flatten()[order]
    stds = np.sqrt(gmm.covariances_.flatten()[order])
    weights = gmm.weights_[order]

    # Scale curves to histogram
    bin_width = bins[1] - bins[0]
    scale = N * bin_width

    for i, (m, s, w, color, label) in enumerate(zip(
        means, stds, weights,
        [COLORS["accent_red"], COLORS["primary"]],
        [f"Reject ({weights[0]*100:.0f}%)", f"Embrace ({weights[1]*100:.0f}%)"],
    )):
        curve = w * stats.norm.pdf(x_range, m, s) * scale
        ax.plot(x_range, curve, color=color, linewidth=2.5, zorder=3)
        # Annotate peak
        peak_y = w * stats.norm.pdf(m, m, s) * scale
        side = "left" if i == 0 else "right"
        ax.annotate(
            label, xy=(m, peak_y),
            xytext=(m + (-1.2 if i == 0 else 1.2), peak_y * 0.85),
            fontsize=10, fontweight="bold", color=color,
            fontfamily="Arial",
            arrowprops=dict(arrowstyle="-", color=color, lw=1),
            ha=side, va="center",
        )

    ax.set_xlabel("Score (-3 = totally disagree, +3 = totally agree)",
                  fontsize=9, color=COLORS["text_muted"])
    ax.set_ylabel("")
    ax.set_xlim(-3.8, 3.8)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False, labelleft=False)

    path = save_final_figure(fig, "I02_spirituality")
    figures["I02"] = path


# =========================================================================
# I03 — Emocao forte e o prazer mais rejeitado
# =========================================================================
def chart_i03():
    print("\n  I03: Fatores por mediana...")
    medians = {}
    for fn in factor_names:
        fc = f"factor_{fn}"
        if fc in clean_df.columns:
            medians[fn] = clean_df[fc].median()

    # Sort by median
    sorted_factors = sorted(medians.items(), key=lambda x: x[1])
    labels = [factor_labels.get(fn, fn) for fn, _ in sorted_factors]
    values = [v for _, v in sorted_factors]

    fig, ax = create_statista_figure(
        title="Thrill-seeking is the only type of pleasure most people reject",
        subtitle="Median score for each of the 6 pleasure factors",
    )

    colors = [COLORS["accent_red"] if v < 0 else COLORS["primary"]
              for v in values]

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, values, color=colors, height=0.6, edgecolor="none")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10, fontfamily="Arial")
    ax.invert_yaxis()

    # Zero line
    ax.axvline(x=0, color=COLORS["text_dark"], linewidth=0.8, zorder=1)

    # Data labels
    for bar, val in zip(bars, values):
        offset = 0.08 if val >= 0 else -0.08
        ha = "left" if val >= 0 else "right"
        ax.text(val + offset, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}", va="center", ha=ha,
                fontsize=10, fontweight="bold", fontfamily="Arial",
                color=COLORS["text_dark"])

    ax.set_xlim(min(values) - 0.5, max(values) + 0.5)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(left=False, bottom=False, labelbottom=False)
    ax.xaxis.set_visible(False)

    path = save_final_figure(fig, "I03_thrilling_rejected")
    figures["I03"] = path


# =========================================================================
# I04 — Paradoxo do thrilling
# =========================================================================
def chart_i04():
    print("\n  I04: Paradoxo do thrilling...")
    # Medians
    medians = {}
    for fn in factor_names:
        fc = f"factor_{fn}"
        if fc in clean_df.columns:
            medians[fn] = clean_df[fc].median()

    # Betas from H17 (hardcoded from analyst report — verified)
    betas = {
        "thrilling": 0.354,
        "noble": 0.301,
        "reputational": 0.287,
        "sensorial": 0.242,
        "intellectual": 0.224,
        "interpersonal": 0.192,
    }

    # Sort by beta descending
    sorted_factors = sorted(betas.items(), key=lambda x: x[1], reverse=True)
    labels = [factor_labels.get(fn, fn) for fn, _ in sorted_factors]
    beta_vals = [b for _, b in sorted_factors]
    median_vals = [medians.get(fn, 0) for fn, _ in sorted_factors]

    # Normalize medians to 0-1 range for visual comparison
    med_min, med_max = min(median_vals), max(median_vals)
    med_norm = [(v - med_min) / (med_max - med_min) for v in median_vals]

    fig, ax = create_statista_figure(
        title="The thrill paradox: most rejected, but most influential",
        subtitle="Comparing popularity (median) vs. statistical weight (beta) for each factor",
        figsize=(8, 9),
    )

    y_pos = np.arange(len(labels))
    bar_width = 0.35

    bars1 = ax.barh(y_pos - bar_width / 2, beta_vals, bar_width,
                     color=COLORS["primary"], label="Weight (beta)",
                     edgecolor="none")
    bars2 = ax.barh(y_pos + bar_width / 2, med_norm, bar_width,
                     color=COLORS["light_blue"], label="Popularity (normalized median)",
                     edgecolor="none")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10, fontfamily="Arial")
    ax.invert_yaxis()

    # Highlight thrilling row
    ax.axhspan(-0.5, 0.5, color=COLORS["accent_red"], alpha=0.08, zorder=0)

    # Annotation
    ax.annotate(
        "Highest weight\nbut lowest popularity",
        xy=(beta_vals[0], 0),
        xytext=(0.5, 1.8),
        fontsize=9, fontfamily="Arial", color=COLORS["accent_red"],
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=COLORS["accent_red"], lw=1.5),
        ha="center",
    )

    ax.legend(loc="lower right", fontsize=9, frameon=False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.tick_params(left=False)
    ax.set_xlabel("")

    path = save_final_figure(fig, "I04_paradox")
    figures["I04"] = path


# =========================================================================
# I05 — Quem cuida de pessoas cuida de causas
# =========================================================================
def chart_i05():
    print("\n  I05: Scatter interpersonal vs noble...")
    fig, ax = create_statista_figure(
        title="People who care about loved ones also care about causes",
        subtitle="Each dot is one person — interpersonal vs. noble pleasure factors",
        figsize=(8, 9),
    )

    # Sample for readability
    sample = clean_df.sample(n=2000, random_state=SEED)
    x = sample["factor_interpersonal"]
    y = sample["factor_noble"]

    ax.scatter(x, y, s=8, alpha=0.25, color=COLORS["scatter_dot"],
               edgecolors="none", zorder=2)

    # Trend line
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_line, p(x_line), color=COLORS["accent_red"], linewidth=2,
            zorder=3)

    # Rho annotation
    rho, _ = stats.spearmanr(clean_df["factor_interpersonal"],
                              clean_df["factor_noble"])
    ax.text(
        0.95, 0.05,
        f"Spearman rho = {rho:.2f}\n(strong positive correlation)",
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=10, fontfamily="Arial", fontweight="bold",
        color=COLORS["accent_red"],
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  edgecolor=COLORS["accent_red"], alpha=0.9),
    )

    ax.set_xlabel("Interpersonal (caring about people)", fontsize=10,
                  fontfamily="Arial", color=COLORS["text_dark"])
    ax.set_ylabel("Noble (caring about causes)", fontsize=10,
                  fontfamily="Arial", color=COLORS["text_dark"])

    path = save_final_figure(fig, "I05_caring")
    figures["I05"] = path


# =========================================================================
# I06 — Intelectual e reputacional: independentes
# =========================================================================
def chart_i06():
    print("\n  I06: Scatter intellectual vs reputational...")
    fig, ax = create_statista_figure(
        title="Curiosity and status-seeking have nothing to do with each other",
        subtitle="Each dot is one person — intellectual vs. reputational factors",
        figsize=(8, 9),
    )

    sample = clean_df.sample(n=2000, random_state=SEED)
    x = sample["factor_intellectual"]
    y = sample["factor_reputational"]

    ax.scatter(x, y, s=8, alpha=0.25, color=COLORS["text_muted"],
               edgecolors="none", zorder=2)

    rho, _ = stats.spearmanr(clean_df["factor_intellectual"],
                              clean_df["factor_reputational"])
    ax.text(
        0.95, 0.05,
        f"Spearman rho = {rho:.3f}\n(practically zero — independent)",
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=10, fontfamily="Arial", fontweight="bold",
        color=COLORS["text_muted"],
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  edgecolor=COLORS["text_muted"], alpha=0.9),
    )

    ax.set_xlabel("Intellectual (thinking, learning, creating)", fontsize=10,
                  fontfamily="Arial", color=COLORS["text_dark"])
    ax.set_ylabel("Reputational (status, recognition, power)", fontsize=10,
                  fontfamily="Arial", color=COLORS["text_dark"])

    path = save_final_figure(fig, "I06_independent")
    figures["I06"] = path


# =========================================================================
# I07 — Nao existem tipos de pessoa
# =========================================================================
def chart_i07():
    print("\n  I07: Silhouette scores...")
    # Data from H12 analyst report (verified)
    data = [
        ("Hierarchical k=2", 0.228),
        ("K-Means k=2", 0.218),
        ("GMM k=2", 0.193),
        ("K-Means k=3", 0.152),
        ("K-Means k=4", 0.152),
        ("K-Means k=5", 0.143),
        ("GMM k=3", 0.123),
        ("Hierarchical k=3", 0.103),
        ("GMM k=4", 0.113),
    ]

    labels = [d[0] for d in data]
    scores = [d[1] for d in data]

    fig, ax = create_statista_figure(
        title="No clear 'types of people' — pleasure is a spectrum",
        subtitle="Silhouette scores for all clustering attempts (higher = clearer groups)",
    )

    y_pos = np.arange(len(labels))
    colors = [COLORS["light_blue"] for _ in scores]

    bars = ax.barh(y_pos, scores, color=colors, height=0.6, edgecolor="none")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9, fontfamily="Arial")
    ax.invert_yaxis()

    # Threshold line
    ax.axvline(x=0.25, color=COLORS["accent_red"], linewidth=2,
               linestyle="--", zorder=3)
    ax.text(0.255, -0.5, "Minimum for\nclear groups",
            fontsize=9, fontfamily="Arial", color=COLORS["accent_red"],
            fontweight="bold", va="top")

    # Data labels
    for bar, val in zip(bars, scores):
        ax.text(val + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va="center", ha="left",
                fontsize=9, fontfamily="Arial", color=COLORS["text_dark"])

    ax.set_xlim(0, 0.35)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.tick_params(left=False)

    path = save_final_figure(fig, "I07_spectrum")
    figures["I07"] = path


# =========================================================================
# I08 — Generalistas reportam mais prazer
# =========================================================================
def chart_i08():
    print("\n  I08: Generalistas vs especialistas...")
    # Recalculate from data
    if "entropy_normalized" in profiles.columns:
        median_ent = profiles["entropy_normalized"].median()
        gen_mask = profiles["entropy_normalized"] >= median_ent
        spec_mask = profiles["entropy_normalized"] < median_ent
    else:
        gen_mask = pd.Series([True] * len(clean_df))
        spec_mask = pd.Series([False] * len(clean_df))

    items_df = clean_df[item_cols]
    mean_overall = items_df.mean(axis=1)
    gen_mean = mean_overall[gen_mask.values].mean()
    spec_mean = mean_overall[spec_mask.values].mean()
    n_gen = gen_mask.sum()
    n_spec = spec_mask.sum()

    fig, ax = create_statista_figure(
        title="Generalists report more overall pleasure than specialists",
        subtitle="Average pleasure score by profile type (scale: -3 to +3)",
        figsize=(8, 6),
    )

    labels = ["Generalists", "Specialists"]
    values = [gen_mean, spec_mean]
    colors = [COLORS["primary"], COLORS["light_blue"]]

    # Give more room at bottom for labels and caveat
    ax.set_position([0.12, 0.16, 0.76, 0.56])

    bars = ax.bar([0, 1], values, color=colors, width=0.5, edgecolor="none")

    # Data labels on top
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.03,
                f"{val:.2f}", ha="center", va="bottom",
                fontsize=14, fontweight="bold", fontfamily="Arial",
                color=COLORS["text_dark"])

    # N labels inside bars
    for bar, n_val in zip(bars, [n_gen, n_spec]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                f"N = {n_val:,}", ha="center", va="center",
                fontsize=9, fontfamily="Arial", color="white",
                fontweight="bold")

    ax.set_xticks([0, 1])
    ax.set_xticklabels(labels, fontsize=11, fontfamily="Arial")
    ax.set_ylim(0, max(values) * 1.25)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(left=False, bottom=False, labelleft=False)
    ax.yaxis.set_visible(False)

    # Cohen's d annotation
    ax.text(
        0.5, max(values) * 1.15,
        "Cohen's d = 1.20 (large effect)",
        ha="center", va="center",
        fontsize=10, fontfamily="Arial", fontweight="bold",
        color=COLORS["accent_warm"],
    )

    # Caveat
    fig.text(
        0.5, 0.06,
        "Note: partly mechanical — people who agree more "
        "with everything naturally have a balanced profile",
        ha="center", va="top",
        fontsize=8, fontfamily="Arial", fontstyle="italic",
        color=COLORS["text_muted"],
    )

    path = save_final_figure(fig, "I08_generalists")
    figures["I08"] = path


# =========================================================================
# Generate all charts
# =========================================================================
print("\nGerando graficos finais...")

chart_i01()
chart_i02()
chart_i03()
chart_i04()
chart_i05()
chart_i06()
chart_i07()
chart_i08()

print(f"\n  {len(figures)} graficos gerados em outputs/figures/final/")


# =========================================================================
# Narrative document
# =========================================================================
print("\nGerando documento narrativo...")

NARRATIVE = f"""# De onde vem o prazer? — 8 descobertas sobre o que faz as pessoas felizes

**Data:** {datetime.now().strftime('%Y-%m-%d')}
**Dados:** Sources of Pleasure (ClearerThinking.org) — N = {N:,} respondentes

---

> Este documento apresenta 8 descobertas sobre as fontes de prazer humano,
> baseadas em respostas de quase 7.000 pessoas a 37 perguntas sobre o que
> lhes da prazer. Cada grafico conta uma parte da historia — comecamos pelo
> que todo mundo concorda e terminamos com os paradoxos que so aparecem
> quando olhamos os dados de varios angulos ao mesmo tempo.

---

## 1. Rir e o prazer mais universal

![I01](../figures/final/I01_ranking.png)

### O que este grafico mostra

Das 37 fontes de prazer avaliadas, **rir e ter humor** e a que mais pessoas
concordam que lhes da prazer. 77% dos respondentes marcaram "concordo" ou
"concordo totalmente" nesse item — mais do que qualquer outro.

O top 5 e revelador: rir, conexao pessoal profunda, explorar ideias,
aprender e tempo de qualidade com quem se ama. Sao prazeres simples,
acessiveis e universais — nao luxos ou aventuras.

### Como chegamos a essa conclusao

Calculamos a "concordancia liquida" de cada item (% que concorda menos %
que discorda) e usamos bootstrap (1.000 reamostras) para construir
intervalos de confianca. O intervalo do humor nao se sobrepoem com o
segundo colocado — a lideranca e estatisticamente real.

### O que isso significa

Se voce quer mais prazer na vida, as respostas mais populares nao envolvem
dinheiro, aventura ou status. Envolvem rir, conectar-se com pessoas e
alimentar a curiosidade. Essas sao as fontes de prazer em que a
humanidade mais concorda.

### Ressalvas

A amostra vem do ClearerThinking.org — provavelmente pessoas mais
analiticas e curiosas que a media. Em outra populacao, o ranking poderia
mudar. E a diferenca entre os 5 primeiros e pequena (2-5 pontos
percentuais).

---

## 2. Espiritualidade racha a sala ao meio

![I02](../figures/final/I02_spirituality.png)

### O que este grafico mostra

Enquanto a maioria dos itens tem uma distribuicao "normal" (a maioria das
pessoas no meio, poucos nos extremos), **espiritualidade** e completamente
diferente. O grafico mostra dois grupos claros: cerca de 36% das pessoas
rejeitam fortemente (concentradas nas notas -3 e -2) e 64% se posicionam
do neutro ao positivo.

Nao existe meio-termo suave — a distribuicao tem dois picos separados,
nao uma curva unica.

### Como chegamos a essa conclusao

Ajustamos um modelo estatístico (mistura gaussiana) que tenta encaixar 1
ou 2 "curvas de sino" nos dados. Com 2 curvas o ajuste e dramaticamente
melhor (BIC diff = 2.114 — qualquer valor acima de 10 ja e forte).
Alem disso, quem pontua alto em espiritualidade difere em TODOS os 6
tipos de prazer (o maior efeito: d = 1.31 no fator "nobre").

### O que isso significa

Espiritualidade e o grande divisor. E o unico item que cria dois grupos
realmente distintos. Quem valoriza espiritualidade tende a valorizar mais
TUDO — cuidar dos outros, sensacoes, ideias. E um perfil de prazer
completamente diferente.

### Ressalvas

A amostra do ClearerThinking provavelmente tem menos pessoas religiosas
que a populacao geral. A proporcao 36/64 pode nao se aplicar a todo mundo.

---

## 3. Emocao forte e o unico prazer que a maioria rejeita

![I03](../figures/final/I03_thrilling_rejected.png)

### O que este grafico mostra

Dos 6 grandes tipos de prazer, **"emocionante" (thrilling) e o unico com
mediana negativa**. Isso significa que mais da metade das pessoas
discordam que adrenalina, risco e sustos lhes dao prazer.

Todos os outros fatores — interpessoal, intelectual, sensorial, nobre e
ate reputacional — tem mediana positiva.

### Como chegamos a essa conclusao

Calculamos a mediana de cada fator (a media dos itens que compoem cada
grupo) e comparamos com um teste estatistico (Wilcoxon). A diferenca
entre thrilling e o segundo mais baixo (reputacional) e grande e
estatisticamente real.

### O que isso significa

Buscar adrenalina, correr riscos e se assustar por diversao nao sao
fontes de prazer para a maioria. Enquanto a maioria concorda que rir,
pensar e amar dao prazer, a emocao forte e polarizadora — uns amam,
a maioria rejeita.

### Ressalvas

A amostra pode exagerar esse efeito — o publico do ClearerThinking
provavelmente e mais intelectual e menos aventureiro que a populacao
geral.

---

## 4. O paradoxo: o prazer mais rejeitado e o que mais diferencia as pessoas

![I04](../figures/final/I04_paradox.png)

### O que este grafico mostra

Este grafico compara duas coisas para cada tipo de prazer: **quanto as
pessoas gostam** (popularidade) e **quanto ele pesa na formula do prazer
geral** (peso estatistico/beta).

O resultado surpreendente: **thrilling e o menos popular MAS tem o maior
peso**. E o fator que mais "puxa" o prazer geral — tanto pra cima quanto
pra baixo.

### Como chegamos a essa conclusao

Este insight so aparece quando combinamos tres analises diferentes:
a rejeicao do thrilling (H03), o beta da regressao (H17) e o perfil
dos thrill-seekers (H13). Nenhuma analise sozinha revela o paradoxo.

### O que isso significa

Thrilling nao e o "motor" do prazer — e o **termometro que mais varia**.
Como as pessoas divergem muito sobre emocao forte (uns amam, a maioria
odeia), esse fator e o que mais diferencia quem tem prazer geral alto
de quem tem baixo. Quem busca adrenalina tende a gostar de tudo mais
tambem; quem rejeita tende a ser mais seletivo.

### Ressalvas

O peso (beta) vem de uma regressao com circularidade parcial — os
fatores fazem parte da formula do prazer geral. Os pesos relativos sao
informativos, mas o R² alto (0.974) nao e uma descoberta independente.

---

## 5. Quem cuida de pessoas tambem cuida de causas

![I05](../figures/final/I05_caring.png)

### O que este grafico mostra

Cada ponto e uma pessoa. O eixo horizontal mede quanto ela valoriza
prazeres interpessoais (tempo de qualidade, pertencer, amar) e o eixo
vertical mede quanto valoriza prazeres "nobres" (caridade, comunidade,
ajudar). A linha vermelha mostra a tendencia.

**Quem pontua alto em um, pontua alto no outro.** A correlacao e forte
(rho = 0.46).

### Como chegamos a essa conclusao

Calculamos a correlacao de Spearman entre os dois fatores e testamos se
eles funcionam como uma dimensao unica (alpha de Cronbach = 0.67 —
aceitavel). O grupo espiritual pontua alto em ambos, reforcando a
conexao.

### O que isso significa

Parece existir uma dimensao latente de "cuidado" — pessoas que se
importam com seus entes queridos tambem tendem a se importar com
causas maiores. Nao sao coisas separadas: quem cuida, cuida de tudo.

### Ressalvas

A correlacao 0.46 e forte mas nao fortissima — os dois fatores ainda
tem variancia propria. O "superfator cuidador" e uma hipotese, nao um
fato confirmado.

---

## 6. Gostar de pensar nao tem nada a ver com querer status

![I06](../figures/final/I06_independent.png)

### O que este grafico mostra

Compare este grafico com o anterior. Enquanto interpessoal e nobre
mostram um padrao claro (pra cima e pra direita), **intelectual e
reputacional formam uma nuvem sem direcao nenhuma**. A correlacao e
praticamente zero (rho = 0.023).

### Como chegamos a essa conclusao

Usamos um teste de equivalencia (TOST) que nao apenas mostra que a
correlacao nao e significativa — mostra que ela e **significativamente
igual a zero**. Isso e mais forte que "nao encontramos relacao": e
"provamos que nao ha relacao".

### O que isso significa

Gostar de pensar, criar e aprender nao faz voce buscar nem evitar
status, reconhecimento ou poder. As duas coisas simplesmente nao tem
relacao. Isso desafia a intuicao de que "intelectuais desprezam status"
— na verdade, as duas dimensoes variam de forma completamente
independente.

### Ressalvas

Independencia nao e incompatibilidade. Existem pessoas que pontuam alto
em ambos — elas apenas nao sao mais comuns do que o acaso prediria.

---

## 7. Nao existem "tipos de pessoa" no prazer

![I07](../figures/final/I07_spectrum.png)

### O que este grafico mostra

Tentamos agrupar as pessoas em "tipos" usando tres metodos diferentes
de agrupamento (K-Means, hierarquico e mistura gaussiana) com 2 a 8
grupos. O grafico mostra a qualidade de cada tentativa (silhouette —
quanto maior, mais claros os grupos).

**Nenhuma tentativa superou o limiar minimo** (linha vermelha tracejada
em 0.25). Os grupos sao sempre difusos e mal definidos.

### Como chegamos a essa conclusao

Rodamos 21 combinacoes de metodo × numero de grupos e verificamos a
estabilidade com 100 sub-amostras. O melhor resultado (0.228) ainda e
fraco. Um analista tambem tentou buscar especificamente um "grupo
intelectual" — encontrou, mas com silhouette ainda pior (0.152).

### O que isso significa

E tentador pensar que existem "o intelectual", "o aventureiro", "o
cuidador" como tipos fixos de pessoa. Mas os dados nao sustentam isso.
O prazer e um espectro continuo — as pessoas se distribuem gradualmente,
sem fronteiras naturais. Quando um algoritmo "encontra" grupos, as
bordas sao tao difusas que nao faz sentido chamar de tipos.

### Ressalvas

Silhouette baixo nao prova que tipos nao existem — apenas que esses
metodos nao os encontram nestes dados. Com variaveis demograficas
(idade, genero, pais), talvez surgissem padroes mais claros.

---

## 8. Quem gosta de tudo um pouco reporta mais prazer — mas cuidado com essa conclusao

![I08](../figures/final/I08_generalists.png)

### O que este grafico mostra

Dividimos as pessoas em dois grupos: **generalistas** (perfil
equilibrado, gostam de varios tipos de prazer) e **especialistas**
(perfil concentrado, focam em poucos tipos). Os generalistas reportam
significativamente mais prazer geral (media 1.21 vs 0.58).

A diferenca e grande (d = 1.20 — um dos maiores efeitos encontrados
nesta analise).

### Como chegamos a essa conclusao

Usamos a entropia de Shannon (uma medida de o quanto o perfil de prazer
e equilibrado vs concentrado) para dividir as pessoas pela mediana.
Depois comparamos o prazer medio geral entre os dois grupos.

### O que isso significa

A primeira leitura seria: "diversifique suas fontes de prazer e voce
sera mais feliz". Mas essa interpretacao e mais forte do que os dados
permitem.

**O problema:** quem diz "concordo" pra tudo (media alta) automaticamente
fica com perfil equilibrado (entropia alta). A correlacao entre entropia
e media geral e 0.64 — forte e parcialmente mecanica. Parte do efeito
e real, mas parte e um artefato matematico.

### Ressalvas

Nao podemos afirmar que diversificar fontes de prazer CAUSA mais
satisfacao. Pode ser que pessoas naturalmente mais satisfeitas
simplesmente concordem mais com tudo. Sao dados de um unico momento,
sem acompanhamento ao longo do tempo.

---

## Nota final

Estas descobertas vem de um questionario online respondido por quase
7.000 pessoas no site ClearerThinking.org. A amostra provavelmente
e mais analitica, curiosa e secular que a populacao geral — o que pode
influenciar os rankings e proporcoes.

Todos os numeros sao associacoes, nao causas. "Quem busca adrenalina
tambem valoriza status" nao significa que uma coisa causa a outra.

Os insights fortes (I01-I04) sao sustentados por multiplas analises
convergentes. Os moderados (I05-I07) tem evidencia solida mas com
ressalvas. O sugestivo (I08) tem um efeito grande mas parcialmente
tautologico.

---

*Narrativa gerada por `scripts/phase9_storytelling.py`*
*Pipeline: Fases 0-9 | Dados: Sources of Pleasure (ClearerThinking.org) — N = {N:,}*
"""

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
narrative_path = OUTPUT_DIR / "phase9_narrative.md"
narrative_path.write_text(NARRATIVE.strip(), encoding="utf-8")
print(f"\n  Narrativa salva: {narrative_path}")

# =========================================================================
# Summary
# =========================================================================
print(f"\n{'='*60}")
print(f"  FASE 9 COMPLETA")
print(f"{'='*60}")
print(f"\n  Graficos finais: {len(figures)}")
for name, path in figures.items():
    print(f"    {name}: {path}")
print(f"\n  Narrativa: {narrative_path}")
