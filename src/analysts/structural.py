"""
structural.py — Analyst agent for structural hypotheses.

Specializes in: item groupings, factor structure of standalone items.
Techniques: Spearman correlation matrix, network visualization.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

from src.analysts.base import BaseAnalyst


class StructuralAnalyst(BaseAnalyst):

    name = "structural"
    display_name = "Estrutural"

    def run_hypothesis(self, h):
        test = h["test"]
        if test == "standalone_correlations":
            self._test_standalone_correlations(h)
        else:
            raise ValueError(f"Teste desconhecido: {test}")

    # ------------------------------------------------------------------
    # H10 — Standalone item correlations
    # ------------------------------------------------------------------

    def _test_standalone_correlations(self, h):
        hid = h["id"]
        params = h["params"]
        threshold_notable = params["threshold_notable"]
        threshold_new_group = params["threshold_new_group"]

        items = self.standalone_items
        item_labels = {}
        for it in self.config["itens"]:
            if it["variavel"] in items:
                item_labels[it["variavel"]] = it["rotulo"]

        # Compute correlation matrix for standalone items
        corr_matrix = self.df[items].corr(method="spearman")

        # Find notable pairs
        notable_pairs = []
        strong_pairs = []
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                rho = corr_matrix.iloc[i, j]
                _, p_val = stats.spearmanr(
                    self.df[items[i]], self.df[items[j]]
                )
                pair = {
                    "item1": items[i],
                    "item2": items[j],
                    "label1": item_labels.get(items[i], items[i]),
                    "label2": item_labels.get(items[j], items[j]),
                    "rho": rho,
                    "p_value": p_val,
                }
                if abs(rho) >= threshold_notable:
                    notable_pairs.append(pair)
                if abs(rho) >= threshold_new_group:
                    strong_pairs.append(pair)

        n_notable = len(notable_pairs)
        n_strong = len(strong_pairs)

        if n_strong > 0:
            verdict = "confirmada"
            interp = (
                f"Encontramos {n_strong} par(es) com correlacao muito forte "
                f"(rho > {threshold_new_group}), suficiente para considerar "
                f"um novo agrupamento."
            )
        elif n_notable > 0:
            verdict = "inconclusiva"
            interp = (
                f"Encontramos {n_notable} par(es) com correlacao moderada "
                f"(rho > {threshold_notable}), mas nenhum forte o bastante "
                f"(rho > {threshold_new_group}) para criar um novo grupo. "
                f"Existem conexoes, mas nao um grupo coeso."
            )
        else:
            verdict = "nao confirmada"
            interp = (
                f"Nenhum par de itens avulsos tem correlacao acima de "
                f"{threshold_notable}. Cada item e realmente independente."
            )

        # --- Figure 1: Heatmap ---
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        ax = axes[0]
        labels = [item_labels.get(it, it) for it in items]
        im = ax.imshow(corr_matrix.values, cmap="RdBu_r", vmin=-0.5, vmax=0.5,
                       aspect="auto")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=9)
        # Annotate values
        for i in range(len(items)):
            for j in range(len(items)):
                val = corr_matrix.iloc[i, j]
                color = "white" if abs(val) > 0.3 else "black"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                        fontsize=9, color=color)
        ax.set_title("Correlacoes entre itens avulsos", fontsize=11)
        fig.colorbar(im, ax=ax, shrink=0.8)

        # --- Figure 2: Network ---
        ax = axes[1]
        n_items = len(items)
        angles = np.linspace(0, 2 * np.pi, n_items, endpoint=False)
        x_pos = np.cos(angles)
        y_pos = np.sin(angles)

        # Draw edges
        for i in range(n_items):
            for j in range(i + 1, n_items):
                rho = corr_matrix.iloc[i, j]
                if abs(rho) >= 0.10:
                    width = abs(rho) * 5
                    color = "#E74C3C" if rho < 0 else "#27AE60"
                    alpha = min(abs(rho) * 2, 0.9)
                    ax.plot([x_pos[i], x_pos[j]], [y_pos[i], y_pos[j]],
                            color=color, linewidth=width, alpha=alpha)

        # Draw nodes
        ax.scatter(x_pos, y_pos, s=800, color="#4472C4", zorder=5,
                   edgecolors="white", linewidth=2)
        for i, label in enumerate(labels):
            ax.annotate(label, (x_pos[i], y_pos[i]),
                        textcoords="offset points", xytext=(0, 18),
                        ha="center", fontsize=9, fontweight="bold")

        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title("Rede de conexoes\n(verde = positiva, vermelho = negativa)",
                      fontsize=11)

        fig.suptitle(h["headline"], fontsize=13, fontweight="bold", y=1.02)
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "standalone_correlations")

        # --- Results ---
        result_text = "Matriz de correlacao dos 6 itens avulsos:\n\n"
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                rho = corr_matrix.iloc[i, j]
                marker = ""
                if abs(rho) >= threshold_new_group:
                    marker = " *** (muito forte)"
                elif abs(rho) >= threshold_notable:
                    marker = " ** (moderada)"
                result_text += (
                    f"  {item_labels.get(items[i], items[i])} × "
                    f"{item_labels.get(items[j], items[j])}: "
                    f"rho = {rho:.3f}{marker}\n"
                )

        result_text += (
            f"\nPares com rho > {threshold_notable}: {n_notable}\n"
            f"Pares com rho > {threshold_new_group}: {n_strong}"
        )

        strongest_rho = 0.0
        if n_notable > 0:
            strongest_rho = max(p["rho"] for p in notable_pairs)

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Spearman correlation matrix (standalone items)",
            statistic_name="n_notable_pairs",
            statistic_value=n_notable,
            effect_size_name="strongest_rho",
            effect_size_value=strongest_rho,
            p_value=np.nan,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                "Matriz de correlacao Spearman entre os 6 itens avulsos "
                "(que nao pertencem a nenhum fator). Visualizacao em heatmap "
                "e rede de conexoes. "
                f"Limite para 'conexao moderada': rho > {threshold_notable}. "
                f"Limite para considerar novo grupo: rho > {threshold_new_group}."
            ),
            premises=(
                "Spearman nao exige normalidade. "
                "Esta analise NAO tenta corrigir os 6 fatores — "
                "apenas explora se os itens avulsos tem conexoes entre si."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"Correlacao mais forte entre avulsos: {strongest_rho:.3f}. "
                f"{'Sao conexoes reais mas nao formam um fator coeso.' if strongest_rho < threshold_new_group else 'Forte o bastante para sugerir um agrupamento.'}"
            ),
            limitations=(
                "Com apenas 6 itens, uma analise fatorial nao seria confiavel. "
                "A analise se limita a correlacoes entre pares."
            ),
            figures=[fig_path],
        )
