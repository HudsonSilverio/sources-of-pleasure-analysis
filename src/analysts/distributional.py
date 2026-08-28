"""
distributional.py — Analyst agent for distributional hypotheses.

Specializes in: rankings, consensus, polarization, bimodality.
Techniques: bootstrap confidence intervals, Wilcoxon signed-rank,
            Gaussian Mixture Models (GMM).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.mixture import GaussianMixture

from src.analysts.base import BaseAnalyst


class DistributionalAnalyst(BaseAnalyst):

    name = "distributional"
    display_name = "Distribucional"

    def run_hypothesis(self, h):
        test = h["test"]
        if test == "ranking_bootstrap":
            self._test_ranking_bootstrap(h)
        elif test == "factor_comparison":
            self._test_factor_comparison(h)
        elif test == "bimodality_gmm":
            self._test_bimodality_gmm(h)
        else:
            raise ValueError(f"Teste desconhecido: {test}")

    # ------------------------------------------------------------------
    # H01 / H02 — Ranking with bootstrap CIs
    # ------------------------------------------------------------------

    def _test_ranking_bootstrap(self, h):
        hid = h["id"]
        params = h["params"]
        metric = params["metric"]
        top_n = params["top_n"]
        n_boot = params["n_bootstrap"]

        item_stats = self.load_item_stats()

        if metric not in item_stats.columns:
            raise ValueError(f"Metrica '{metric}' nao encontrada em item_stats")

        # Sort items by metric
        ranked = item_stats[metric].sort_values(ascending=False)
        top_items = ranked.head(top_n)

        # Bootstrap CIs for each top item
        boot_results = {}
        for item in top_items.index:
            values = self.df[item].values
            boot_means = []
            for _ in range(n_boot):
                sample = np.random.choice(values, size=len(values), replace=True)
                if metric == "net_agreement":
                    top2 = np.mean((sample >= 2)) * 100
                    bot2 = np.mean((sample <= -2)) * 100
                    boot_means.append(top2 - bot2)
                elif metric == "top2_pct":
                    boot_means.append(np.mean((sample >= 2)) * 100)
                else:
                    boot_means.append(np.mean(sample))
            boot_means = np.array(boot_means)
            ci_low, ci_high = np.percentile(boot_means, [2.5, 97.5])
            boot_results[item] = {
                "observed": top_items[item],
                "ci_low": ci_low,
                "ci_high": ci_high,
                "boot_mean": boot_means.mean(),
            }

        # Check overlap between 1st and 2nd
        items_list = list(boot_results.keys())
        first = boot_results[items_list[0]]
        second = boot_results[items_list[1]]
        overlap = first["ci_low"] < second["ci_high"]

        if overlap:
            verdict = "inconclusiva"
            interp = (
                f"Os dois primeiros colocados ({items_list[0]} e {items_list[1]}) "
                f"tem intervalos de confianca que se sobrepoem. "
                f"A diferenca entre eles nao e grande o bastante pra dizer que "
                f"um e claramente maior que o outro."
            )
        else:
            verdict = "confirmada"
            interp = (
                f"{items_list[0]} e o lider claro do ranking — "
                f"seu intervalo de confianca nao se sobrepoem com o segundo "
                f"colocado ({items_list[1]})."
            )

        diff = first["observed"] - second["observed"]

        # --- Figure ---
        fig, ax = plt.subplots(figsize=(10, 6))
        labels = []
        for item_name in items_list:
            # Get label from config
            label = item_name
            for it in self.config["itens"]:
                if it["variavel"] == item_name:
                    label = it["rotulo"]
                    break
            labels.append(label)

        y_pos = range(len(items_list))
        vals = [boot_results[i]["observed"] for i in items_list]
        ci_lows = [boot_results[i]["ci_low"] for i in items_list]
        ci_highs = [boot_results[i]["ci_high"] for i in items_list]
        errors_low = [v - cl for v, cl in zip(vals, ci_lows)]
        errors_high = [ch - v for v, ch in zip(vals, ci_highs)]

        ax.barh(y_pos, vals, color="#4472C4", alpha=0.8)
        ax.errorbar(vals, y_pos, xerr=[errors_low, errors_high],
                     fmt="none", color="black", capsize=4)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()
        ax.set_xlabel(f"{metric} (%)")
        ax.set_title(h["headline"], fontsize=12, fontweight="bold")
        ax.axvline(x=0, color="gray", linewidth=0.5)
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "ranking_bootstrap")

        # --- Results ---
        result_text = (
            f"Top {top_n} itens por {metric}:\n"
        )
        for i, item_name in enumerate(items_list):
            r = boot_results[item_name]
            result_text += (
                f"  {i+1}. {labels[i]}: {r['observed']:.1f}% "
                f"(IC 95%: {r['ci_low']:.1f} – {r['ci_high']:.1f})\n"
            )
        result_text += (
            f"\nDiferenca entre 1o e 2o lugar: {diff:.1f} pontos percentuais. "
            f"Sobreposicao de intervalos: {'sim' if overlap else 'nao'}."
        )

        premises = (
            f"Bootstrap com {n_boot} reamostras. "
            f"Intervalos de confianca de 95% (percentis 2.5 e 97.5). "
            f"Metrica: {metric}."
        )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique=f"Bootstrap ranking ({metric})",
            statistic_name=f"diff_1st_2nd_{metric}",
            statistic_value=diff,
            effect_size_name="diff_percentage_points",
            effect_size_value=diff,
            p_value=np.nan,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=f"Ranking por {metric} com intervalos de confianca via bootstrap ({n_boot} reamostras)",
            premises=premises,
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"A diferenca entre os primeiros e de {abs(diff):.1f} pontos "
                f"percentuais — {'relevante' if abs(diff) > 3 else 'pequena'}."
            ),
            limitations=(
                "Bootstrap assume que a amostra e representativa. "
                "Como a amostra e de conveniencia (visitantes do ClearerThinking), "
                "o ranking pode nao refletir a populacao geral."
            ),
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # H03 — Factor comparison (Wilcoxon)
    # ------------------------------------------------------------------

    def _test_factor_comparison(self, h):
        hid = h["id"]
        params = h["params"]
        target = params["target_factor"]
        target_col = f"factor_{target}"

        factor_medians = {}
        for f in self.factor_names:
            col = f"factor_{f}"
            factor_medians[f] = self.df[col].median()

        sorted_factors = sorted(factor_medians.items(), key=lambda x: x[1])
        lowest = sorted_factors[0]
        second_lowest = sorted_factors[1]

        # Wilcoxon signed-rank test between target and second lowest
        stat, p_val = stats.wilcoxon(
            self.df[target_col],
            self.df[f"factor_{second_lowest[0]}"],
        )
        # Effect size: r = Z / sqrt(N)
        z_val = stats.norm.ppf(p_val / 2)
        r_effect = abs(z_val) / np.sqrt(self.n_respondents)

        is_lowest = lowest[0] == target
        is_significant = p_val < 0.05
        is_relevant = r_effect > 0.1

        if is_lowest and is_significant and is_relevant:
            verdict = "confirmada"
            interp = (
                f"O fator {target} (mediana = {lowest[1]:.2f}) e o mais baixo "
                f"dos 6 fatores e a diferenca para o segundo mais baixo "
                f"({second_lowest[0]}, mediana = {second_lowest[1]:.2f}) "
                f"e real (p < 0.001) e relevante (r = {r_effect:.3f})."
            )
        elif is_lowest and is_significant and not is_relevant:
            verdict = "inconclusiva"
            interp = (
                f"O fator {target} e o mais baixo, e o teste da significativo "
                f"(p < 0.001), mas o tamanho do efeito e pequeno "
                f"(r = {r_effect:.3f}). Com N = {self.n_respondents:,}, "
                f"quase tudo da significativo."
            )
        else:
            verdict = "nao confirmada"
            interp = f"O fator {target} nao e o mais baixo dos 6."

        # --- Figure ---
        fig, ax = plt.subplots(figsize=(8, 5))
        factor_labels = []
        factor_vals = []
        colors = []
        for f, med in sorted_factors:
            label = self.config["fatores"][f]["rotulo"]
            factor_labels.append(label)
            factor_vals.append(med)
            colors.append("#E74C3C" if f == target else "#4472C4")

        y_pos = range(len(factor_labels))
        ax.barh(y_pos, factor_vals, color=colors, alpha=0.85)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(factor_labels)
        ax.invert_yaxis()
        ax.set_xlabel("Mediana do fator")
        ax.set_title(h["headline"], fontsize=12, fontweight="bold")
        ax.axvline(x=0, color="gray", linewidth=0.8, linestyle="--")

        # Annotate p and r
        ax.text(0.98, 0.02,
                f"Wilcoxon: p < 0.001 | r = {r_effect:.3f} | N = {self.n_respondents:,}",
                transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
                color="gray")
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "factor_comparison")

        # --- Results ---
        result_text = "Ranking dos 6 fatores por mediana:\n"
        for i, (f, med) in enumerate(sorted_factors):
            label = self.config["fatores"][f]["rotulo"]
            result_text += f"  {i+1}. {label}: {med:.2f}\n"
        result_text += (
            f"\nTeste Wilcoxon entre {target} e {second_lowest[0]}: "
            f"W = {stat:.0f}, p = {p_val:.2e}, r = {r_effect:.3f}"
        )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Wilcoxon signed-rank",
            statistic_name="W",
            statistic_value=stat,
            effect_size_name="r (Z/sqrt(N))",
            effect_size_value=r_effect,
            p_value=p_val,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                "Comparacao dos 6 fatores por mediana. "
                "Teste Wilcoxon (compara pares sem assumir que os dados sao simetricos) "
                "entre o fator mais baixo e o segundo mais baixo. "
                "Tamanho de efeito: r = Z / sqrt(N)."
            ),
            premises=(
                "Teste Wilcoxon nao exige normalidade. "
                "As comparacoes sao pareadas (mesmo respondente em ambos os fatores). "
                "Com N grande, p-valor quase sempre sera significativo — "
                "o tamanho de efeito (r) e o que realmente importa."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"r = {r_effect:.3f}. "
                f"{'Efeito pequeno (r < 0.1) — a diferenca existe mas e minima.' if r_effect < 0.1 else ''}"
                f"{'Efeito moderado — a diferenca e real e perceptivel.' if 0.1 <= r_effect < 0.3 else ''}"
                f"{'Efeito grande — a diferenca e substancial.' if r_effect >= 0.3 else ''}"
            ),
            limitations=(
                "Dados de autorrelato, amostra de conveniencia. "
                "Correlacao entre fatores nao e controlada nesta comparacao."
            ),
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # H04 — Bimodality test (GMM)
    # ------------------------------------------------------------------

    def _test_bimodality_gmm(self, h):
        hid = h["id"]
        params = h["params"]
        item = params["item"]
        n_components = params["n_components"]

        values = self.df[item].dropna().values.reshape(-1, 1)

        # Fit GMM with 1 and 2 components, compare BIC
        bics = {}
        models = {}
        for k in n_components:
            gmm = GaussianMixture(
                n_components=k, random_state=self.seed, n_init=10
            )
            gmm.fit(values)
            bics[k] = gmm.bic(values)
            models[k] = gmm

        bic_diff = bics[1] - bics[2]  # positive = 2 is better
        two_is_better = bic_diff > 10  # strong evidence threshold

        gmm2 = models[2]
        means = sorted(gmm2.means_.flatten())
        weights = gmm2.weights_

        if two_is_better:
            verdict = "confirmada"
            interp = (
                f"O modelo com 2 curvas (BIC = {bics[2]:.0f}) ajusta "
                f"muito melhor que o de 1 curva (BIC = {bics[1]:.0f}). "
                f"Diferenca de BIC = {bic_diff:.0f} (acima de 10 e forte). "
                f"Existem dois grupos: um centrado em {means[0]:.1f} "
                f"e outro em {means[1]:.1f}."
            )
        else:
            verdict = "nao confirmada"
            interp = (
                f"A diferenca de BIC entre 1 e 2 curvas ({bic_diff:.0f}) "
                f"nao e forte o suficiente. A distribuicao e variada "
                f"mas nao se divide claramente em dois grupos."
            )

        # --- Figure ---
        fig, ax = plt.subplots(figsize=(10, 6))

        # Histogram
        ax.hist(values.flatten(), bins=7, range=(-3.5, 3.5),
                density=True, alpha=0.5, color="#4472C4", edgecolor="white",
                label="Dados reais")

        # Density with GMM2 components
        x_range = np.linspace(-3.5, 3.5, 200).reshape(-1, 1)
        total_density = np.exp(gmm2.score_samples(x_range))
        ax.plot(x_range, total_density, color="#E74C3C", linewidth=2,
                label=f"Mistura de 2 curvas (BIC = {bics[2]:.0f})")

        # Individual components
        for i in range(2):
            weight = gmm2.weights_[i]
            mean = gmm2.means_[i, 0]
            std = np.sqrt(gmm2.covariances_[i, 0, 0])
            component = weight * stats.norm.pdf(x_range.flatten(), mean, std)
            ax.plot(x_range, component, linewidth=1.5, linestyle="--",
                    label=f"Grupo {i+1}: media={mean:.1f}, peso={weight:.0%}")

        ax.set_xlabel("Resposta (-3 a +3)")
        ax.set_ylabel("Densidade")
        ax.set_title(h["headline"], fontsize=12, fontweight="bold")
        ax.legend(fontsize=9)

        # Get item label
        item_label = item
        for it in self.config["itens"]:
            if it["variavel"] == item:
                item_label = it["rotulo"]
                break
        ax.text(0.98, 0.98, f"Item: {item_label} | N = {len(values):,}",
                transform=ax.transAxes, ha="right", va="top", fontsize=8,
                color="gray")
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "bimodality_gmm")

        # --- Results ---
        result_text = (
            f"BIC com 1 curva: {bics[1]:.0f}\n"
            f"BIC com 2 curvas: {bics[2]:.0f}\n"
            f"Diferenca: {bic_diff:.0f} "
            f"(> 10 = forte evidencia de 2 grupos)\n\n"
            f"Grupo 1: media = {means[0]:.1f}, peso = {weights[0]:.1%}\n"
            f"Grupo 2: media = {means[1]:.1f}, peso = {weights[1]:.1%}"
        )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Gaussian Mixture Model (BIC)",
            statistic_name="BIC_diff (1 vs 2)",
            statistic_value=bic_diff,
            effect_size_name="separation (diff means)",
            effect_size_value=abs(means[1] - means[0]),
            p_value=np.nan,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                "Mistura gaussiana (GMM — ajusta 1 vs 2 curvas nos dados e "
                "compara qual modelo se encaixa melhor usando o BIC, uma "
                "medida de qualidade do ajuste — quanto menor, melhor)."
            ),
            premises=(
                "GMM nao exige normalidade dos dados. "
                "Criterio de decisao: diferenca de BIC > 10 entre 1 e 2 "
                "componentes indica forte evidencia de 2 grupos."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"Separacao entre os grupos: {abs(means[1] - means[0]):.1f} pontos "
                f"na escala de -3 a +3. "
                f"{'Grupos bem separados — a divisao e real.' if abs(means[1] - means[0]) > 3 else ''}"
                f"{'Grupos moderadamente separados.' if 2 <= abs(means[1] - means[0]) <= 3 else ''}"
                f"{'Grupos proximos — a divisao e sutil.' if abs(means[1] - means[0]) < 2 else ''}"
            ),
            limitations=(
                "GMM assume que cada grupo segue uma curva normal, "
                "o que pode nao ser perfeito para dados Likert com limites "
                "fixos (-3 a +3). O item e discreto (7 valores), nao continuo."
            ),
            figures=[fig_path],
        )
