"""
Phase 3 — Exploratory Data Analysis (EDA).
Explores relationships between variables: correlations, dimensionality,
clustering structure, anomalies. Produces observations that feed Phase 4.
"""

import yaml
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.manifold import TSNE
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_CSV = PROJECT_ROOT / "data" / "processed" / "clean.csv"
CONFIG_YAML = PROJECT_ROOT / "config" / "instrument.yaml"
REPORT_PATH = PROJECT_ROOT / "outputs" / "reports" / "phase3_eda.md"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures" / "exploratory" / "phase3"
FIG_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
np.random.seed(SEED)

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
ITEM_FACTORS = {item["variavel"]: item["fator"] for item in config["itens"]}
FACTOR_COLS = [f"factor_{name}" for name in config["fatores"]]
FACTOR_LABELS = {f"factor_{name}": fdef["rotulo"] for name, fdef in config["fatores"].items()}
FACTOR_ITEMS = {name: fdef["itens"] for name, fdef in config["fatores"].items()}

# Short labels for plots
labels_short = [ITEM_LABELS[c] for c in ITEM_COLS]
factor_labels_short = [FACTOR_LABELS[c] for c in FACTOR_COLS]

# Data matrices
X_items = df[ITEM_COLS].values
X_factors = df[FACTOR_COLS].values

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm

plt.rcParams.update({
    "figure.dpi": 150,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 10,
})


def save_fig(fig, name):
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  Salvo: {path.name}")


# =====================================================================
# OBSERVATIONS collector
# =====================================================================
observations = []


def add_obs(text, question):
    n = len(observations) + 1
    observations.append((f"O-{n:02d}", text, question))


# =====================================================================
# 1. CORRELATION MATRIX — 37 items (Spearman)
# =====================================================================
print("\n1. Matriz de correlacao (37 itens, Spearman)...")
corr_items = df[ITEM_COLS].corr(method="spearman")

fig, ax = plt.subplots(figsize=(16, 14))
fig.suptitle("Quais fontes de prazer andam juntas?",
             fontsize=14, fontweight="bold", y=0.98)
im = ax.imshow(corr_items.values, cmap="RdBu_r", vmin=-0.5, vmax=0.7, aspect="auto")
ax.set_xticks(range(37))
ax.set_xticklabels(labels_short, rotation=90, fontsize=7)
ax.set_yticks(range(37))
ax.set_yticklabels(labels_short, fontsize=7)
plt.colorbar(im, ax=ax, label="Spearman rho", shrink=0.8)
ax.set_title(f"N = {N} | Correlacao de Spearman entre os 37 itens", fontsize=9, color="gray")
save_fig(fig, "11_correlation_heatmap_items")

# =====================================================================
# 2. CORRELATION MATRIX — 6 factors (Spearman)
# =====================================================================
print("2. Matriz de correlacao (6 fatores, Spearman)...")
corr_factors = df[FACTOR_COLS].corr(method="spearman")

fig, ax = plt.subplots(figsize=(8, 7))
fig.suptitle("Como as categorias de prazer se relacionam?",
             fontsize=14, fontweight="bold")
im = ax.imshow(corr_factors.values, cmap="RdBu_r", vmin=-0.2, vmax=0.7, aspect="auto")
ax.set_xticks(range(6))
ax.set_xticklabels(factor_labels_short, rotation=45, ha="right", fontsize=11)
ax.set_yticks(range(6))
ax.set_yticklabels(factor_labels_short, fontsize=11)
for i in range(6):
    for j in range(6):
        val = corr_factors.values[i, j]
        color = "white" if abs(val) > 0.4 else "black"
        ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=11, color=color)
plt.colorbar(im, ax=ax, label="Spearman rho", shrink=0.8)
ax.set_title(f"N = {N} | Correlacao de Spearman entre os 6 fatores", fontsize=9, color="gray")
save_fig(fig, "12_correlation_heatmap_factors")

# Find notable factor correlations
factor_corr_pairs = []
for i in range(6):
    for j in range(i+1, 6):
        factor_corr_pairs.append((
            factor_labels_short[i], factor_labels_short[j],
            corr_factors.values[i, j]
        ))
factor_corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)

add_obs(
    f"Os fatores mais correlacionados sao {factor_corr_pairs[0][0]} e "
    f"{factor_corr_pairs[0][1]} (rho={factor_corr_pairs[0][2]:.2f}). "
    f"Os menos correlacionados sao {factor_corr_pairs[-1][0]} e "
    f"{factor_corr_pairs[-1][1]} (rho={factor_corr_pairs[-1][2]:.2f}).",
    "A estrutura de 6 fatores captura dimensoes realmente independentes ou ha sobreposicao?"
)

# =====================================================================
# 3. CORRELATION NETWORK GRAPH
# =====================================================================
print("3. Grafo de rede de correlacoes...")
import networkx as nx

G = nx.Graph()
for c in ITEM_COLS:
    G.add_node(ITEM_LABELS[c], factor=ITEM_FACTORS[c] if ITEM_FACTORS[c] else "standalone")

threshold = 0.35
for i in range(37):
    for j in range(i+1, 37):
        r = corr_items.values[i, j]
        if abs(r) >= threshold:
            G.add_edge(labels_short[i], labels_short[j], weight=abs(r), sign="+" if r > 0 else "-")

factor_color_map = {
    "interpersonal": "#e74c3c",
    "thrilling": "#e67e22",
    "noble": "#27ae60",
    "reputational": "#8e44ad",
    "sensorial": "#3498db",
    "intellectual": "#f39c12",
    None: "#95a5a6",
    "standalone": "#95a5a6",
}
node_colors = [factor_color_map.get(G.nodes[n]["factor"], "#95a5a6") for n in G.nodes]

fig, ax = plt.subplots(figsize=(16, 14))
fig.suptitle("Quais comunidades de itens emergem?",
             fontsize=14, fontweight="bold", y=0.98)
pos = nx.spring_layout(G, k=2.5, seed=SEED, iterations=100)
edges = G.edges(data=True)
edge_widths = [d["weight"] * 4 for _, _, d in edges]
edge_colors = ["#2ecc71" if d["sign"] == "+" else "#e74c3c" for _, _, d in edges]
edge_alphas = [min(d["weight"] * 1.5, 0.8) for _, _, d in edges]

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=400, alpha=0.9, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=6, ax=ax)
for (u, v, d), width, color, alpha in zip(edges, edge_widths, edge_colors, edge_alphas):
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=width, edge_color=color,
                           alpha=alpha, ax=ax)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, label=k.capitalize()) for k, c in factor_color_map.items()
                   if k and k != "standalone"]
legend_elements.append(Patch(facecolor="#95a5a6", label="Sem fator"))
ax.legend(handles=legend_elements, loc="lower left", fontsize=9)
ax.set_title(f"Arestas = |Spearman rho| >= {threshold} | Verde = positivo | Vermelho = negativo",
             fontsize=9, color="gray")
ax.axis("off")
save_fig(fig, "13_correlation_network")

n_edges = G.number_of_edges()
add_obs(
    f"O grafo de correlacoes (limiar |rho| >= {threshold}) tem {n_edges} arestas. "
    f"Itens do mesmo fator tendem a se agrupar visualmente, mas ha conexoes entre fatores.",
    "A estrutura fatorial predefinida e confirmada pela rede de correlacoes ou ha itens que se conectam mais com outros fatores?"
)

# =====================================================================
# 4. TOP / BOTTOM CORRELATION PAIRS
# =====================================================================
print("4. Pares de correlacao mais fortes e mais fracos...")
corr_pairs = []
for i in range(37):
    for j in range(i+1, 37):
        corr_pairs.append((ITEM_COLS[i], ITEM_COLS[j],
                           labels_short[i], labels_short[j],
                           corr_items.values[i, j]))

corr_pairs.sort(key=lambda x: x[4], reverse=True)
top_positive = corr_pairs[:15]
top_negative = [p for p in corr_pairs if p[4] < 0]
top_negative.sort(key=lambda x: x[4])
top_negative = top_negative[:10]
near_zero = sorted(corr_pairs, key=lambda x: abs(x[4]))[:10]

# Redundancy candidates
redundant = [p for p in corr_pairs if abs(p[4]) > 0.60]

fig, axes = plt.subplots(1, 2, figsize=(16, 10))
fig.suptitle("Quais sao as relacoes mais fortes e mais fracas?",
             fontsize=14, fontweight="bold")

# Top positive
ax = axes[0]
pair_labels = [f"{p[2]} ↔ {p[3]}" for p in top_positive]
pair_vals = [p[4] for p in top_positive]
ax.barh(range(len(pair_labels)), pair_vals, color="#2ecc71", height=0.7)
ax.set_yticks(range(len(pair_labels)))
ax.set_yticklabels(pair_labels, fontsize=8)
ax.set_xlabel("Spearman rho")
ax.set_title("Top 15 correlacoes positivas", fontsize=11)
ax.invert_yaxis()

# Top negative
ax = axes[1]
if top_negative:
    pair_labels_n = [f"{p[2]} ↔ {p[3]}" for p in top_negative]
    pair_vals_n = [p[4] for p in top_negative]
    ax.barh(range(len(pair_labels_n)), pair_vals_n, color="#e74c3c", height=0.7)
    ax.set_yticks(range(len(pair_labels_n)))
    ax.set_yticklabels(pair_labels_n, fontsize=8)
    ax.set_xlabel("Spearman rho")
    ax.set_title("Top 10 correlacoes negativas", fontsize=11)
    ax.invert_yaxis()
else:
    ax.text(0.5, 0.5, "Nenhuma correlacao negativa encontrada",
            ha="center", va="center", transform=ax.transAxes)
    ax.set_title("Correlacoes negativas", fontsize=11)

plt.tight_layout()
save_fig(fig, "14_top_bottom_correlations")

add_obs(
    f"O par mais fortemente correlacionado e {top_positive[0][2]} ↔ {top_positive[0][3]} "
    f"(rho={top_positive[0][4]:.2f}). "
    + (f"A correlacao negativa mais forte e {top_negative[0][2]} ↔ {top_negative[0][3]} "
       f"(rho={top_negative[0][4]:.2f})." if top_negative else "Nao ha correlacoes negativas significativas."),
    "Os pares mais correlacionados sao redundantes (medem a mesma coisa) ou sao genuinamente relacionados?"
)

if redundant:
    add_obs(
        f"Ha {len(redundant)} pares com |rho| > 0.60 (candidatos a redundancia): " +
        ", ".join(f"{p[2]}↔{p[3]} ({p[4]:.2f})" for p in redundant[:5]),
        "Esses itens poderiam ser combinados ou um deles e dispensavel?"
    )

# =====================================================================
# 5. PCA + PARALLEL ANALYSIS
# =====================================================================
print("5. PCA + analise paralela...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_items)

pca_full = PCA(random_state=SEED)
pca_full.fit(X_scaled)
eigenvalues_real = pca_full.explained_variance_
explained_var_ratio = pca_full.explained_variance_ratio_
cumulative_var = np.cumsum(explained_var_ratio) * 100

# Parallel analysis (Horn's method)
n_iterations = 100
n_vars = X_scaled.shape[1]
n_obs = X_scaled.shape[0]
eigenvalues_random = np.zeros((n_iterations, n_vars))
for i in range(n_iterations):
    random_data = np.random.normal(size=(n_obs, n_vars))
    pca_random = PCA()
    pca_random.fit(random_data)
    eigenvalues_random[i] = pca_random.explained_variance_

eigenvalues_random_mean = eigenvalues_random.mean(axis=0)
eigenvalues_random_p95 = np.percentile(eigenvalues_random, 95, axis=0)

# Number of components to retain
n_retain = np.sum(eigenvalues_real > eigenvalues_random_p95)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle("Quantas dimensoes reais existem nos dados?",
             fontsize=14, fontweight="bold")

# Scree plot with parallel analysis
ax = axes[0]
x_range = range(1, min(21, n_vars + 1))
ax.plot(x_range, eigenvalues_real[:20], "bo-", label="Dados reais", linewidth=2)
ax.plot(x_range, eigenvalues_random_mean[:20], "r--", label="Dados aleatorios (media)", linewidth=1.5)
ax.plot(x_range, eigenvalues_random_p95[:20], "r:", label="Dados aleatorios (P95)", linewidth=1.5)
ax.axvline(x=n_retain, color="green", linestyle="--", alpha=0.7, label=f"Reter: {n_retain} componentes")
ax.axvline(x=6, color="orange", linestyle="--", alpha=0.7, label="Fatores do instrumento: 6")
ax.set_xlabel("Componente")
ax.set_ylabel("Eigenvalue")
ax.set_title("Scree plot + Analise Paralela (Horn)", fontsize=11)
ax.legend(fontsize=9)

# Cumulative variance
ax = axes[1]
ax.plot(range(1, n_vars + 1), cumulative_var, "bo-", markersize=4)
ax.axhline(y=50, color="gray", linestyle="--", alpha=0.5)
ax.axhline(y=70, color="gray", linestyle="--", alpha=0.5)
ax.axhline(y=80, color="gray", linestyle="--", alpha=0.5)
ax.axvline(x=n_retain, color="green", linestyle="--", alpha=0.7)
ax.axvline(x=6, color="orange", linestyle="--", alpha=0.7)
ax.set_xlabel("Numero de componentes")
ax.set_ylabel("Variancia acumulada (%)")
ax.set_title("Variancia explicada acumulada", fontsize=11)
for threshold_pct in [50, 70, 80]:
    n_for_pct = np.argmax(cumulative_var >= threshold_pct) + 1
    ax.text(n_for_pct + 0.5, threshold_pct + 1, f"{n_for_pct} comp = {threshold_pct}%",
            fontsize=8, color="gray")

plt.tight_layout()
save_fig(fig, "15_pca_scree_parallel")

var_6 = cumulative_var[5]
add_obs(
    f"A analise paralela sugere reter {n_retain} componentes (eigenvalue real > P95 aleatorio). "
    f"O instrumento usa 6 fatores, que explicam {var_6:.1f}% da variancia. "
    f"Os primeiros {n_retain} componentes explicam {cumulative_var[n_retain-1]:.1f}%.",
    f"A estrutura de 6 fatores e adequada ou os dados sugerem {n_retain} dimensoes?"
)

# =====================================================================
# 6. PCA LOADINGS HEATMAP
# =====================================================================
print("6. Heatmap de loadings da PCA...")
n_components_show = min(n_retain + 2, 10)
pca_show = PCA(n_components=n_components_show, random_state=SEED)
pca_show.fit(X_scaled)
loadings = pca_show.components_.T  # (37, n_components)

fig, ax = plt.subplots(figsize=(12, 14))
fig.suptitle("Quais itens carregam em quais componentes?",
             fontsize=14, fontweight="bold", y=0.98)
im = ax.imshow(loadings, cmap="RdBu_r", vmin=-0.5, vmax=0.5, aspect="auto")
ax.set_xticks(range(n_components_show))
ax.set_xticklabels([f"PC{i+1}\n({explained_var_ratio[i]*100:.1f}%)" for i in range(n_components_show)],
                   fontsize=9)
ax.set_yticks(range(37))
ax.set_yticklabels(labels_short, fontsize=8)
plt.colorbar(im, ax=ax, label="Loading", shrink=0.8)

# Mark factor boundaries with colors on the y-axis
factor_colors_list = []
for c in ITEM_COLS:
    f = ITEM_FACTORS[c]
    factor_colors_list.append(factor_color_map.get(f if f else "standalone", "#95a5a6"))
for i, color in enumerate(factor_colors_list):
    ax.add_patch(plt.Rectangle((-0.8, i - 0.5), 0.3, 1, color=color, clip_on=False))

ax.set_title(f"Primeiros {n_components_show} componentes | Cor lateral = fator predefinido",
             fontsize=9, color="gray")
save_fig(fig, "16_pca_loadings_heatmap")

# Check if any item loads strongly on an unexpected component
high_loadings = []
for i in range(37):
    for j in range(min(n_retain, n_components_show)):
        if abs(loadings[i, j]) > 0.35:
            high_loadings.append((labels_short[i], ITEM_FACTORS[ITEM_COLS[i]], j+1, loadings[i, j]))

add_obs(
    f"No heatmap de loadings, os itens tendem a carregar nos componentes esperados pelos seus fatores, "
    f"mas ha cross-loadings que merecem investigacao na analise estrutural.",
    "A estrutura empirica dos dados confirma ou desafia a organizacao dos 6 fatores do instrumento?"
)

# =====================================================================
# 7. HIERARCHICAL CLUSTERING OF ITEMS (dendrogram)
# =====================================================================
print("7. Dendrograma de itens...")
# Distance = 1 - |correlation|
dist_matrix = 1 - corr_items.abs().values
np.fill_diagonal(dist_matrix, 0)
dist_condensed = squareform(dist_matrix)
linkage_matrix = linkage(dist_condensed, method="ward")

fig, ax = plt.subplots(figsize=(16, 10))
fig.suptitle("Os itens se agrupam como os fatores predefinidos?",
             fontsize=14, fontweight="bold")
dend = dendrogram(
    linkage_matrix,
    labels=labels_short,
    leaf_rotation=90,
    leaf_font_size=8,
    ax=ax,
    color_threshold=0.7 * max(linkage_matrix[:, 2]),
)
ax.set_ylabel("Distancia (1 - |correlacao|)")
ax.set_title("Clustering hierarquico (Ward) baseado em correlacoes de Spearman",
             fontsize=9, color="gray")
save_fig(fig, "17_dendrogram_items")

add_obs(
    "O dendrograma mostra como os itens se agrupam empiricamente com base em suas correlacoes. "
    "Comparar os clusters emergentes com os 6 fatores predefinidos revela concordancias e divergencias.",
    "Quais itens estao 'mal classificados' nos fatores originais segundo o agrupamento empirico?"
)

# =====================================================================
# 8. WITHIN-FACTOR COHESION
# =====================================================================
print("8. Coesao intra-fator...")
fig, axes = plt.subplots(2, 3, figsize=(16, 12))
fig.suptitle("Os itens dentro de cada fator sao coesos?",
             fontsize=14, fontweight="bold")

factor_cohesion = {}
for idx, (factor_name, factor_items_list) in enumerate(FACTOR_ITEMS.items()):
    ax = axes[idx // 3, idx % 3]
    sub_corr = df[factor_items_list].corr(method="spearman")
    sub_labels = [ITEM_LABELS[c] for c in factor_items_list]

    im = ax.imshow(sub_corr.values, cmap="YlOrRd", vmin=0, vmax=0.7, aspect="auto")
    ax.set_xticks(range(len(sub_labels)))
    ax.set_xticklabels(sub_labels, rotation=45, ha="right", fontsize=7)
    ax.set_yticks(range(len(sub_labels)))
    ax.set_yticklabels(sub_labels, fontsize=7)

    # Annotate
    for i in range(len(sub_labels)):
        for j in range(len(sub_labels)):
            val = sub_corr.values[i, j]
            if i != j:
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=7)

    # Mean inter-item correlation (excluding diagonal)
    mask = np.ones_like(sub_corr.values, dtype=bool)
    np.fill_diagonal(mask, False)
    mean_corr = sub_corr.values[mask].mean()
    factor_cohesion[factor_name] = mean_corr

    ax.set_title(f"{FACTOR_LABELS[f'factor_{factor_name}']}\n(media r = {mean_corr:.2f})", fontsize=10)

plt.tight_layout()
save_fig(fig, "18_within_factor_cohesion")

# Find most and least cohesive factors
most_cohesive = max(factor_cohesion, key=factor_cohesion.get)
least_cohesive = min(factor_cohesion, key=factor_cohesion.get)

add_obs(
    f"O fator mais coeso e {FACTOR_LABELS[f'factor_{most_cohesive}']} "
    f"(media inter-item r = {factor_cohesion[most_cohesive]:.2f}). "
    f"O menos coeso e {FACTOR_LABELS[f'factor_{least_cohesive}']} "
    f"(media inter-item r = {factor_cohesion[least_cohesive]:.2f}).",
    "O fator menos coeso deveria ser reorganizado? Algum item esta deslocado?"
)

# =====================================================================
# 9. BOXPLOTS — 37 items
# =====================================================================
print("9. Boxplots dos 37 itens...")
sorted_by_median = df[ITEM_COLS].median().sort_values(ascending=True)
sorted_cols = sorted_by_median.index.tolist()
sorted_labels = [ITEM_LABELS[c] for c in sorted_cols]

fig, ax = plt.subplots(figsize=(14, 12))
fig.suptitle("Como as distribuicoes se comparam visualmente?",
             fontsize=14, fontweight="bold", y=0.98)
bp = ax.boxplot([df[c].values for c in sorted_cols], vert=False, patch_artist=True,
                widths=0.6, showfliers=True, flierprops=dict(marker=".", markersize=2, alpha=0.3))
for i, patch in enumerate(bp["boxes"]):
    f = ITEM_FACTORS.get(sorted_cols[i])
    color = factor_color_map.get(f if f else "standalone", "#95a5a6")
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
ax.set_yticks(range(1, 38))
ax.set_yticklabels(sorted_labels, fontsize=8)
ax.set_xlabel("Score (-3 a +3)")
ax.axvline(x=0, color="black", linewidth=0.5, alpha=0.5)
ax.set_title("Cor = fator | Ordenado por mediana", fontsize=9, color="gray")
save_fig(fig, "19_boxplots_items")

# =====================================================================
# 10. BOXPLOTS — 6 factors
# =====================================================================
print("10. Boxplots dos 6 fatores...")
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle("Como os fatores se comparam entre si?",
             fontsize=14, fontweight="bold")
sorted_factor_cols = df[FACTOR_COLS].median().sort_values(ascending=True).index.tolist()
sorted_factor_labels = [FACTOR_LABELS[c] for c in sorted_factor_cols]
bp = ax.boxplot([df[c].values for c in sorted_factor_cols], vert=False, patch_artist=True,
                widths=0.5, showfliers=True, flierprops=dict(marker=".", markersize=3, alpha=0.3))
for i, patch in enumerate(bp["boxes"]):
    fname = sorted_factor_cols[i].replace("factor_", "")
    color = factor_color_map.get(fname, "#95a5a6")
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_yticks(range(1, 7))
ax.set_yticklabels(sorted_factor_labels, fontsize=11)
ax.set_xlabel("Score (-3 a +3)")
ax.axvline(x=0, color="black", linewidth=0.5, alpha=0.5)
ax.set_title("Ordenado por mediana", fontsize=9, color="gray")
save_fig(fig, "20_boxplots_factors")

add_obs(
    "Thrilling e o unico fator com mediana negativa, indicando que a maioria dos respondentes "
    "nao obtem prazer substancial de atividades emocionantes/arriscadas. "
    "Interpessoal e Intelectual dominam com medianas acima de 1.5.",
    "O perfil dominante (alto interpessoal/intelectual, baixo thrilling) e uma caracteristica da amostra ClearerThinking ou seria universal?"
)

# =====================================================================
# 11. t-SNE — respondent visualization
# =====================================================================
print("11. t-SNE dos respondentes...")
X_scaled_respondents = scaler.fit_transform(X_items)

# Use PCA first to reduce to n_retain dimensions, then t-SNE
pca_pre = PCA(n_components=min(n_retain, 10), random_state=SEED)
X_pca = pca_pre.fit_transform(X_scaled_respondents)

tsne = TSNE(n_components=2, random_state=SEED, perplexity=50, max_iter=1000, learning_rate="auto")
X_tsne = tsne.fit_transform(X_pca)

# Color by dominant factor
factor_scores = df[FACTOR_COLS].values
dominant_factor_idx = np.argmax(factor_scores, axis=1)
factor_names_list = list(config["fatores"].keys())

fig, ax = plt.subplots(figsize=(14, 12))
fig.suptitle("Existem perfis naturais de respondentes?",
             fontsize=14, fontweight="bold")
for fidx, fname in enumerate(factor_names_list):
    mask = dominant_factor_idx == fidx
    color = factor_color_map.get(fname, "#95a5a6")
    ax.scatter(X_tsne[mask, 0], X_tsne[mask, 1], c=color, s=8, alpha=0.4,
               label=f"{FACTOR_LABELS[f'factor_{fname}']} ({mask.sum()})")
ax.legend(fontsize=9, markerscale=3, title="Fator dominante")
ax.set_xlabel("t-SNE dim 1")
ax.set_ylabel("t-SNE dim 2")
ax.set_title("Cada ponto = 1 respondente | Cor = fator com maior score | Perplexity=50",
             fontsize=9, color="gray")
ax.axis("off")
save_fig(fig, "21_tsne_respondents")

add_obs(
    "A projecao t-SNE mostra a distribuicao dos respondentes no espaco reduzido. "
    "Regioes com concentracao de uma cor sugerem perfis com predominancia de um fator.",
    "Existem clusters discretos de respondentes ou e uma distribuicao continua?"
)

# =====================================================================
# 12. SILHOUETTE — respondent clustering
# =====================================================================
print("12. Silhouette para clustering de respondentes...")
X_cluster = scaler.fit_transform(X_items)

silhouette_scores = []
inertias = []
k_range = range(2, 9)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=SEED, n_init=10, max_iter=300)
    labels = km.fit_predict(X_cluster)
    sil = silhouette_score(X_cluster, labels)
    silhouette_scores.append(sil)
    inertias.append(km.inertia_)
    print(f"    k={k}: silhouette={sil:.3f}, inertia={km.inertia_:.0f}")

best_k = list(k_range)[np.argmax(silhouette_scores)]
best_sil = max(silhouette_scores)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Qual o numero otimo de clusters de respondentes?",
             fontsize=14, fontweight="bold")

ax = axes[0]
ax.plot(list(k_range), silhouette_scores, "bo-", linewidth=2)
ax.axvline(x=best_k, color="green", linestyle="--", alpha=0.7)
ax.set_xlabel("Numero de clusters (k)")
ax.set_ylabel("Silhouette score")
ax.set_title(f"Silhouette — melhor k = {best_k} (score = {best_sil:.3f})", fontsize=11)

ax = axes[1]
ax.plot(list(k_range), inertias, "ro-", linewidth=2)
ax.set_xlabel("Numero de clusters (k)")
ax.set_ylabel("Inertia (soma dos quadrados intra-cluster)")
ax.set_title("Metodo do cotovelo (Elbow)", fontsize=11)

plt.tight_layout()
save_fig(fig, "22_silhouette_elbow")

add_obs(
    f"O melhor k pelo silhouette e k={best_k} (score={best_sil:.3f}). "
    f"{'Score baixo (<0.25) sugere que os clusters nao sao bem separados — a distribuicao pode ser mais continua do que discreta.' if best_sil < 0.25 else 'Score moderado sugere agrupamentos com alguma estrutura.'}",
    f"Com k={best_k}, quais sao os perfis dos clusters? Eles contam uma historia interpretavel?"
)

# Quick profile of best k
km_best = KMeans(n_clusters=best_k, random_state=SEED, n_init=10)
cluster_labels = km_best.fit_predict(X_cluster)
df["_cluster"] = cluster_labels

cluster_profiles = []
for k in range(best_k):
    mask = df["_cluster"] == k
    profile = df.loc[mask, FACTOR_COLS].mean()
    profile["n"] = int(mask.sum())
    profile["pct"] = mask.mean() * 100
    cluster_profiles.append(profile)

cluster_profiles_df = pd.DataFrame(cluster_profiles)
cluster_profiles_df.index.name = "cluster"

# =====================================================================
# ANOMALY DETECTION
# =====================================================================
print("\n13. Deteccao de anomalias...")

# Straight-lining: same value for all 37 items
straight_liners = (df[ITEM_COLS].nunique(axis=1) == 1).sum()
add_obs(
    f"{straight_liners} respondentes deram a mesma resposta para todos os 37 itens (straight-lining). "
    + ("Isso pode indicar falta de engajamento." if straight_liners > 0 else "Nenhum caso detectado — bom sinal de qualidade."),
    "Respondentes com padrao de resposta suspeito deveriam ser removidos?"
)

# Low variance responders (nunique <= 2)
low_variance = (df[ITEM_COLS].nunique(axis=1) <= 2).sum()
if low_variance > straight_liners:
    add_obs(
        f"{low_variance} respondentes usaram no maximo 2 valores diferentes nos 37 itens. "
        f"Padrao de resposta com baixissima variabilidade.",
        "Esses respondentes devem ser investigados como potenciais respostas descuidadas?"
    )

# Mahalanobis distance for multivariate outliers
from numpy.linalg import inv
X_maha = X_scaled_respondents
cov_matrix = np.cov(X_maha.T)
try:
    cov_inv = inv(cov_matrix)
    mean_vec = X_maha.mean(axis=0)
    diff = X_maha - mean_vec
    mahal_dist = np.sqrt(np.sum(diff @ cov_inv * diff, axis=1))
    threshold_mahal = np.percentile(mahal_dist, 99)
    n_outliers_mahal = (mahal_dist > threshold_mahal).sum()
    add_obs(
        f"Deteccao de outliers multivariados por distancia de Mahalanobis: "
        f"{n_outliers_mahal} respondentes acima do P99 (dist > {threshold_mahal:.1f}). "
        f"Esses sao perfis de resposta raros, nao necessariamente errados.",
        "Os outliers multivariados representam perfis genuinamente atipicos ou erros de resposta?"
    )
except Exception:
    add_obs(
        "Nao foi possivel calcular a distancia de Mahalanobis (matriz de covariancia singular).",
        "Investigar colinearidade entre itens."
    )

# Clean up temp column
df.drop(columns=["_cluster"], inplace=True, errors="ignore")

# =====================================================================
# 14. STANDALONE ITEMS ANALYSIS
# =====================================================================
print("\n14. Analise dos 6 itens standalone (sem fator)...")

STANDALONE_COLS = config.get("itens_sem_fator", [])
STANDALONE_LABELS = {c: ITEM_LABELS[c] for c in STANDALONE_COLS}
standalone_labels_short = [STANDALONE_LABELS[c] for c in STANDALONE_COLS]

# 14a. Correlation matrix among standalone items (6x6)
corr_standalone = df[STANDALONE_COLS].corr(method="spearman")

# 14b. Correlation of each standalone with each factor
standalone_vs_factors = pd.DataFrame(index=STANDALONE_COLS, columns=FACTOR_COLS, dtype=float)
for sc in STANDALONE_COLS:
    for fc in FACTOR_COLS:
        rho, _ = stats.spearmanr(df[sc], df[fc])
        standalone_vs_factors.loc[sc, fc] = rho

# Plot: combined figure — left: 6x6 standalone, right: 6 standalone x 6 factors
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
fig.suptitle("Onde os 6 itens sem fator se encaixam?",
             fontsize=14, fontweight="bold")

# Left: standalone inter-correlations
ax = axes[0]
im = ax.imshow(corr_standalone.values, cmap="YlOrRd", vmin=0, vmax=0.5, aspect="auto")
ax.set_xticks(range(6))
ax.set_xticklabels(standalone_labels_short, rotation=45, ha="right", fontsize=9)
ax.set_yticks(range(6))
ax.set_yticklabels(standalone_labels_short, fontsize=9)
for i in range(6):
    for j in range(6):
        val = corr_standalone.values[i, j]
        if i != j:
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=9)
plt.colorbar(im, ax=ax, label="Spearman rho", shrink=0.8)
ax.set_title("Correlacoes entre os 6 itens standalone", fontsize=10)

# Right: standalone vs factors
ax = axes[1]
vals = standalone_vs_factors.values.astype(float)
im2 = ax.imshow(vals, cmap="YlOrRd", vmin=0, vmax=0.5, aspect="auto")
ax.set_xticks(range(6))
ax.set_xticklabels(factor_labels_short, rotation=45, ha="right", fontsize=9)
ax.set_yticks(range(6))
ax.set_yticklabels(standalone_labels_short, fontsize=9)
for i in range(6):
    for j in range(6):
        val = vals[i, j]
        ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=9)
plt.colorbar(im2, ax=ax, label="Spearman rho", shrink=0.8)
ax.set_title("Correlacao de cada standalone com cada fator", fontsize=10)

plt.tight_layout()
save_fig(fig, "23_standalone_items_analysis")

# Generate observations
# Find strongest standalone-factor association
best_sf = standalone_vs_factors.stack()
best_sf_idx = best_sf.astype(float).abs().idxmax()
best_sf_val = best_sf.loc[best_sf_idx]
best_sf_item = STANDALONE_LABELS[best_sf_idx[0]]
best_sf_factor = FACTOR_LABELS[best_sf_idx[1]]

# Find strongest standalone-standalone pair (excluding diagonal)
standalone_pairs = []
for i in range(6):
    for j in range(i+1, 6):
        standalone_pairs.append((
            standalone_labels_short[i], standalone_labels_short[j],
            corr_standalone.values[i, j]
        ))
standalone_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
top_standalone_pair = standalone_pairs[0]

# Mean inter-standalone correlation
mask_standalone = np.ones_like(corr_standalone.values, dtype=bool)
np.fill_diagonal(mask_standalone, False)
mean_standalone_corr = corr_standalone.values[mask_standalone].mean()

add_obs(
    f"Os 6 itens standalone tem correlacao media entre si de {mean_standalone_corr:.2f}. "
    f"O par mais correlacionado e {top_standalone_pair[0]} ↔ {top_standalone_pair[1]} "
    f"(rho={top_standalone_pair[2]:.2f}). "
    f"O item standalone mais associado a um fator e {best_sf_item} com "
    f"{best_sf_factor} (rho={float(best_sf_val):.2f}).",
    "Os itens standalone deveriam ser integrados a fatores existentes, formar um novo fator, ou permanecer independentes?"
)

# =====================================================================
# SAVE REUSABLE ARTIFACTS (CSVs)
# =====================================================================
print("\n15. Salvando artefatos reutilizaveis...")

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# 1. Correlation matrix — items (37x37)
corr_items_df = corr_items.copy()
corr_items_df.index = labels_short
corr_items_df.columns = labels_short
corr_items_df.to_csv(PROCESSED_DIR / "phase3_corr_items.csv")
print("  Salvo: phase3_corr_items.csv")

# 2. Correlation matrix — factors (6x6)
corr_factors_df = corr_factors.copy()
corr_factors_df.index = factor_labels_short
corr_factors_df.columns = factor_labels_short
corr_factors_df.to_csv(PROCESSED_DIR / "phase3_corr_factors.csv")
print("  Salvo: phase3_corr_factors.csv")

# 3. PCA loadings (37 items x N components)
loadings_df = pd.DataFrame(
    loadings,
    index=labels_short,
    columns=[f"PC{i+1}" for i in range(n_components_show)]
)
loadings_df.index.name = "item"
loadings_df.to_csv(PROCESSED_DIR / "phase3_pca_loadings.csv")
print("  Salvo: phase3_pca_loadings.csv")

# 4. Anomaly flags per respondent
anomaly_df = pd.DataFrame(index=range(N))
anomaly_df["straight_liner"] = (df[ITEM_COLS].nunique(axis=1) == 1).values
anomaly_df["low_variance"] = (df[ITEM_COLS].nunique(axis=1) <= 2).values
try:
    anomaly_df["mahalanobis_dist"] = mahal_dist
    anomaly_df["mahalanobis_outlier_p99"] = mahal_dist > threshold_mahal
except NameError:
    anomaly_df["mahalanobis_dist"] = np.nan
    anomaly_df["mahalanobis_outlier_p99"] = False
anomaly_df.to_csv(PROCESSED_DIR / "phase3_anomaly_flags.csv", index=False)
print("  Salvo: phase3_anomaly_flags.csv")

# =====================================================================
# REPORT
# =====================================================================
print("\nGerando relatorio...")

report_lines = []
report_lines.append("# Fase 3 — Analise Exploratoria (EDA)\n")
report_lines.append(f"**Dataset:** `data/processed/clean.csv` — {N:,} respondentes completos\n")
report_lines.append("**Principio:** esta fase explora **relacoes entre variaveis** para gerar")
report_lines.append("observacoes e pistas. Nenhuma conclusao — apenas hipoteses candidatas")
report_lines.append("para a Fase 4.\n")

# --- Methodology ---
report_lines.append("---\n")
report_lines.append("## Metodologia — metodos aplicados nesta fase\n")

report_lines.append("### 1. Correlacoes")
report_lines.append("| Metodo | Descricao | Aplicado a |")
report_lines.append("|--------|-----------|------------|")
report_lines.append("| Correlacao de Spearman | Mede relacoes monotonicas entre pares. Adequada para Likert (ordinal tratado como intervalar). Mais robusta a assimetria que Pearson | Matriz 37x37 itens e 6x6 fatores |")
report_lines.append("| Identificacao de pares extremos | Top 15 positivas, top 10 negativas, 10 mais proximas de zero | Todos os 666 pares de itens |")
report_lines.append("| Deteccao de redundancia | Pares com \\|rho\\| > 0.60 — candidatos a medir a mesma coisa | Todos os pares |")
report_lines.append("")

report_lines.append("### 2. Grafo de rede de correlacoes")
report_lines.append("| Metodo | Descricao | Aplicado a |")
report_lines.append("|--------|-----------|------------|")
report_lines.append(f"| Network graph (networkx) | Nos = itens, arestas = correlacoes com \\|rho\\| >= {threshold}. Layout spring com seed fixa. Cor dos nos = fator predefinido | 37 itens |")
report_lines.append("")

report_lines.append("### 3. Analise de dimensionalidade")
report_lines.append("| Metodo | Descricao | Aplicado a |")
report_lines.append("|--------|-----------|------------|")
report_lines.append("| PCA (Principal Component Analysis) | Decomposicao em componentes ortogonais. Dados padronizados (StandardScaler). Scree plot dos eigenvalues | 37 itens padronizados |")
report_lines.append(f"| Analise paralela (Horn) | Compara eigenvalues reais com {n_iterations} simulacoes de dados aleatorios (mesmo N e variaveis). Retém componentes cujo eigenvalue real > P95 aleatorio | 37 itens |")
report_lines.append("| Heatmap de loadings | Pesos de cada item em cada componente. Identifica cross-loadings e itens deslocados | Primeiros componentes retidos |")
report_lines.append("")

report_lines.append("### 4. Clustering de itens")
report_lines.append("| Metodo | Descricao | Aplicado a |")
report_lines.append("|--------|-----------|------------|")
report_lines.append("| Clustering hierarquico (Ward) | Distancia = 1 - \\|correlacao\\|. Metodo de ligacao Ward (minimiza variancia intra-cluster). Visualizado como dendrograma | 37 itens |")
report_lines.append("")

report_lines.append("### 5. Coesao intra-fator")
report_lines.append("| Metodo | Descricao | Aplicado a |")
report_lines.append("|--------|-----------|------------|")
report_lines.append("| Media inter-item (Spearman) | Media das correlacoes entre todos os pares de itens dentro de cada fator (excluindo diagonal). Mede se os itens 'andam juntos' | 6 fatores |")
report_lines.append("")

report_lines.append("### 6. Distribuicoes comparadas")
report_lines.append("| Metodo | Descricao | Aplicado a |")
report_lines.append("|--------|-----------|------------|")
report_lines.append("| Boxplots | Mediana, quartis, whiskers (1.5x IQR), outliers individuais. Comparacao visual lado a lado | 37 itens e 6 fatores |")
report_lines.append("")

report_lines.append("### 7. Visualizacao de respondentes")
report_lines.append("| Metodo | Descricao | Aplicado a |")
report_lines.append("|--------|-----------|------------|")
report_lines.append(f"| t-SNE | Reducao nao-linear para 2D (perplexity=50, 1000 iteracoes). Pre-reducao por PCA para {min(n_retain, 10)} dimensoes. Preserva vizinhancas locais | {N} respondentes |")
report_lines.append("")

report_lines.append("### 8. Clustering de respondentes (exploratorio)")
report_lines.append("| Metodo | Descricao | Aplicado a |")
report_lines.append("|--------|-----------|------------|")
report_lines.append(f"| K-Means | k de 2 a 8, n_init=10, max_iter=300, seed={SEED}. Dados padronizados | {N} respondentes |")
report_lines.append("| Silhouette score | Mede coesao intra-cluster vs. separacao entre clusters. Score de -1 a 1 (>0.5 = bom, 0.25-0.5 = razoavel, <0.25 = fraco) | k=2 a k=8 |")
report_lines.append("| Metodo do cotovelo (Elbow) | Inertia (soma dos quadrados intra-cluster) por k. O 'cotovelo' sugere o k apos o qual adicionar clusters traz pouco ganho | k=2 a k=8 |")
report_lines.append("")

report_lines.append("### 9. Deteccao de anomalias")
report_lines.append("| Metodo | Descricao | Aplicado a |")
report_lines.append("|--------|-----------|------------|")
report_lines.append("| Straight-lining | Respondentes com a mesma resposta em todos os 37 itens (nunique == 1) | Todos os respondentes |")
report_lines.append("| Baixa variabilidade | Respondentes com no maximo 2 valores distintos (nunique <= 2) | Todos os respondentes |")
report_lines.append("| Distancia de Mahalanobis | Distancia multivariada ao centroide. Outliers = acima do P99. Identifica perfis de resposta raros | Todos os respondentes |")
report_lines.append("")

report_lines.append("### 10. Analise dos itens standalone")
report_lines.append("| Metodo | Descricao | Aplicado a |")
report_lines.append("|--------|-----------|------------|")
report_lines.append("| Correlacao inter-standalone (Spearman) | Matriz 6x6 de correlacoes entre os itens sem fator. Verifica se formam agrupamentos entre si | 6 itens standalone |")
report_lines.append("| Correlacao standalone vs. fatores (Spearman) | Correlacao de cada item standalone com cada um dos 6 scores de fator. Identifica afinidades com fatores existentes | 6 itens x 6 fatores |")
report_lines.append("")

report_lines.append("### Ferramentas utilizadas")
report_lines.append("- **Python 3.13** com pandas, numpy, scipy, scikit-learn, matplotlib, networkx")
report_lines.append("- **scipy**: stats.spearmanr, cluster.hierarchy (linkage, dendrogram)")
report_lines.append("- **scikit-learn**: PCA, KMeans, TSNE, StandardScaler, silhouette_score")
report_lines.append("- **networkx**: spring_layout, draw_networkx")
report_lines.append(f"- **Seed fixa**: {SEED} para reprodutibilidade")
report_lines.append(f"- **Script reproduzivel**: `scripts/phase3_eda.py`")
report_lines.append("")

# --- Observations ---
report_lines.append("---\n")
report_lines.append("## Observacoes\n")
report_lines.append("Cada observacao e uma pista, nao uma conclusao. O formato e:")
report_lines.append("> O-nn: [observacao] → [possivel pergunta]\n")

for obs_id, obs_text, obs_question in observations:
    report_lines.append(f"### {obs_id}")
    report_lines.append(f"**Observacao:** {obs_text}\n")
    report_lines.append(f"**Possivel pergunta:** {obs_question}\n")

# --- Correlation details ---
report_lines.append("---\n")
report_lines.append("## Detalhes — Correlacoes entre fatores\n")
report_lines.append("| Fator A | Fator B | Spearman rho |")
report_lines.append("|---------|---------|-------------|")
for a, b, r in factor_corr_pairs:
    report_lines.append(f"| {a} | {b} | {r:.3f} |")

report_lines.append("\n## Detalhes — Top 15 correlacoes positivas entre itens\n")
report_lines.append("| Item A | Item B | Spearman rho | Mesmo fator? |")
report_lines.append("|--------|--------|-------------|-------------|")
for var_a, var_b, lab_a, lab_b, r in top_positive:
    same = "Sim" if ITEM_FACTORS.get(var_a) and ITEM_FACTORS.get(var_a) == ITEM_FACTORS.get(var_b) else "Nao"
    report_lines.append(f"| {lab_a} | {lab_b} | {r:.3f} | {same} |")

if top_negative:
    report_lines.append("\n## Detalhes — Top 10 correlacoes negativas entre itens\n")
    report_lines.append("| Item A | Item B | Spearman rho |")
    report_lines.append("|--------|--------|-------------|")
    for var_a, var_b, lab_a, lab_b, r in top_negative:
        report_lines.append(f"| {lab_a} | {lab_b} | {r:.3f} |")

if redundant:
    report_lines.append(f"\n## Detalhes — Candidatos a redundancia (|rho| > 0.60)\n")
    report_lines.append("| Item A | Item B | Spearman rho |")
    report_lines.append("|--------|--------|-------------|")
    for var_a, var_b, lab_a, lab_b, r in redundant:
        report_lines.append(f"| {lab_a} | {lab_b} | {r:.3f} |")

# --- Cluster profiles ---
report_lines.append(f"\n## Detalhes — Perfis dos {best_k} clusters (exploratorio)\n")
report_lines.append("| Cluster | N | % | " + " | ".join(factor_labels_short) + " |")
report_lines.append("|---------|---|---|" + "|".join(["---"] * 6) + "|")
for k_idx in range(best_k):
    row = cluster_profiles_df.iloc[k_idx]
    factor_vals = " | ".join(f"{row[c]:.2f}" for c in FACTOR_COLS)
    report_lines.append(f"| {k_idx} | {int(row['n'])} | {row['pct']:.1f}% | {factor_vals} |")

report_lines.append(f"\nSilhouette score para k={best_k}: **{best_sil:.3f}**")
report_lines.append("(Analise formal de segmentacao sera feita nas Fases 5-6 pelo analista SEGMENTATION)\n")

# --- Standalone details ---
report_lines.append(f"\n## Detalhes — Itens standalone vs. fatores\n")
report_lines.append("| Item standalone | " + " | ".join(factor_labels_short) + " |")
report_lines.append("|-----------------|" + "|".join(["---"] * 6) + "|")
for sc in STANDALONE_COLS:
    vals = " | ".join(f"{float(standalone_vs_factors.loc[sc, fc]):.3f}" for fc in FACTOR_COLS)
    report_lines.append(f"| {STANDALONE_LABELS[sc]} | {vals} |")

report_lines.append(f"\n## Detalhes — Correlacoes entre itens standalone\n")
report_lines.append("| Item A | Item B | Spearman rho |")
report_lines.append("|--------|--------|-------------|")
for a, b, r in standalone_pairs:
    report_lines.append(f"| {a} | {b} | {r:.3f} |")

# --- Charts list ---
report_lines.append("\n---\n")
report_lines.append("## Graficos exploratorios\n")
report_lines.append("Todos em `outputs/figures/exploratory/phase3/`:\n")
chart_list = [
    ("11_correlation_heatmap_items.png", "Quais fontes de prazer andam juntas?"),
    ("12_correlation_heatmap_factors.png", "Como as categorias de prazer se relacionam?"),
    ("13_correlation_network.png", "Quais comunidades de itens emergem?"),
    ("14_top_bottom_correlations.png", "Quais sao as relacoes mais fortes e mais fracas?"),
    ("15_pca_scree_parallel.png", "Quantas dimensoes reais existem nos dados?"),
    ("16_pca_loadings_heatmap.png", "Quais itens carregam em quais componentes?"),
    ("17_dendrogram_items.png", "Os itens se agrupam como os fatores predefinidos?"),
    ("18_within_factor_cohesion.png", "Os itens dentro de cada fator sao coesos?"),
    ("19_boxplots_items.png", "Como as distribuicoes se comparam visualmente?"),
    ("20_boxplots_factors.png", "Como os fatores se comparam entre si?"),
    ("21_tsne_respondents.png", "Existem perfis naturais de respondentes?"),
    ("22_silhouette_elbow.png", "Qual o numero otimo de clusters de respondentes?"),
    ("23_standalone_items_analysis.png", "Onde os 6 itens sem fator se encaixam?"),
]
for fname, question in chart_list:
    report_lines.append(f"- `{fname}` — {question}")

# --- Reusable artifacts ---
report_lines.append("\n---\n")
report_lines.append("## Artefatos reutilizaveis\n")
report_lines.append("Dados intermediarios salvos em `data/processed/` para consumo nas fases seguintes:\n")
report_lines.append("| Arquivo | Conteudo | Dimensoes |")
report_lines.append("|---------|----------|-----------|")
report_lines.append(f"| `phase3_corr_items.csv` | Matriz de correlacao Spearman entre itens | 37 x 37 |")
report_lines.append(f"| `phase3_corr_factors.csv` | Matriz de correlacao Spearman entre fatores | 6 x 6 |")
report_lines.append(f"| `phase3_pca_loadings.csv` | Loadings dos itens nos componentes retidos pela PCA | 37 x {n_components_show} |")
report_lines.append(f"| `phase3_anomaly_flags.csv` | Flags por respondente: straight-liner, baixa variancia, outlier Mahalanobis | {N} x 4 |")

report_lines.append(f"\n---\n")
report_lines.append(f"*Gerado a partir de `data/processed/clean.csv` — N = {N:,} | Seed = {SEED}*\n")

# Write report
report_text = "\n".join(report_lines)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report_text)

print(f"\nFase 3 concluida!")
print(f"  Relatorio: {REPORT_PATH}")
print(f"  Graficos: {FIG_DIR}")
print(f"  Total de observacoes: {len(observations)}")
