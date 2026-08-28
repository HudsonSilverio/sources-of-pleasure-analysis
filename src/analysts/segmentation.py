"""
segmentation.py — Analyst agent for segmentation hypotheses.

Specializes in: grouping people by pleasure profile, finding "types".
Techniques: Shannon entropy, K-Means, hierarchical clustering, GMM,
            silhouette analysis, Mann-Whitney U, Cohen's d.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from src.analysts.base import BaseAnalyst


class SegmentationAnalyst(BaseAnalyst):

    name = "segmentation"
    display_name = "Segmentacao"

    def run_hypothesis(self, h):
        test = h["test"]
        if test == "entropy_groups":
            self._test_entropy_groups(h)
        elif test == "clustering_validation":
            self._test_clustering_validation(h)
        elif test == "quartile_comparison":
            self._test_quartile_comparison(h)
        elif test == "group_comparison":
            self._test_group_comparison(h)
        elif test == "profile_search":
            self._test_profile_search(h)
        else:
            raise ValueError(f"Teste desconhecido: {test}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _cohens_d(self, group1, group2):
        """Compute Cohen's d effect size."""
        n1, n2 = len(group1), len(group2)
        var1, var2 = group1.var(), group2.var()
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        if pooled_std == 0:
            return 0.0
        return (group1.mean() - group2.mean()) / pooled_std

    def _compare_groups_all_factors(self, group1_df, group2_df, label1, label2):
        """Compare two groups across all 6 factors. Returns results list."""
        comparisons = []
        for f in self.factor_names:
            col = f"factor_{f}"
            g1 = group1_df[col]
            g2 = group2_df[col]
            stat, p_val = stats.mannwhitneyu(g1, g2, alternative="two-sided")
            d = self._cohens_d(g1, g2)
            comparisons.append({
                "fator": f,
                "rotulo": self.config["fatores"][f]["rotulo"],
                "media_g1": g1.mean(),
                "media_g2": g2.mean(),
                "diff": g1.mean() - g2.mean(),
                "cohens_d": d,
                "U": stat,
                "p_value": p_val,
            })

        # FDR correction
        from statsmodels.stats.multitest import multipletests
        p_vals = [c["p_value"] for c in comparisons]
        reject, p_corr, _, _ = multipletests(p_vals, method="fdr_bh")
        for i, c in enumerate(comparisons):
            c["p_corrected"] = p_corr[i]
            c["significant"] = reject[i]

        return comparisons

    def _radar_chart(self, ax, categories, values_list, labels, colors, title=""):
        """Draw a radar chart comparing profiles."""
        n = len(categories)
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
        angles += angles[:1]  # close the polygon

        for vals, label, color in zip(values_list, labels, colors):
            vals_closed = vals + vals[:1]
            ax.plot(angles, vals_closed, color=color, linewidth=2, label=label)
            ax.fill(angles, vals_closed, color=color, alpha=0.1)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=9)
        ax.set_title(title, fontsize=11, pad=20)
        ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=8)

    # ------------------------------------------------------------------
    # H11 — Entropy groups (specialists vs generalists)
    # ------------------------------------------------------------------

    def _test_entropy_groups(self, h):
        hid = h["id"]

        profiles = self.load_respondent_profiles()

        gen = profiles[profiles["group_entropy"] == "generalista"]
        esp = profiles[profiles["group_entropy"] == "especialista"]

        # Compare mean_overall between groups
        stat, p_val = stats.mannwhitneyu(
            gen["mean_overall"], esp["mean_overall"], alternative="two-sided"
        )
        d = self._cohens_d(gen["mean_overall"], esp["mean_overall"])

        significant = p_val < 0.05
        relevant = abs(d) > 0.2

        if significant and relevant:
            higher = "generalistas" if gen["mean_overall"].mean() > esp["mean_overall"].mean() else "especialistas"
            verdict = "confirmada"
            interp = (
                f"Os {higher} reportam mais prazer geral "
                f"(d = {d:.3f}, p < 0.001). "
                f"Generalistas: media = {gen['mean_overall'].mean():.2f}, "
                f"Especialistas: media = {esp['mean_overall'].mean():.2f}."
            )
        elif significant:
            verdict = "inconclusiva"
            interp = (
                f"A diferenca e significativa (p < 0.001) mas o efeito e pequeno "
                f"(d = {d:.3f}). Com N = {self.n_respondents:,}, quase tudo "
                f"da significativo."
            )
        else:
            verdict = "nao confirmada"
            interp = "Nao ha diferenca no prazer geral entre generalistas e especialistas."

        # --- Figure ---
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Histogram of entropy
        ax = axes[0]
        ax.hist(profiles["entropy_normalized"], bins=50, color="#4472C4",
                alpha=0.7, edgecolor="white")
        median_val = profiles["entropy_normalized"].median()
        ax.axvline(x=median_val, color="#E74C3C", linewidth=2, linestyle="--",
                   label=f"Mediana = {median_val:.3f}")
        ax.set_xlabel("Entropia normalizada (0 = especialista, 1 = generalista)")
        ax.set_ylabel("Frequencia")
        ax.set_title("Distribuicao da diversidade de prazer", fontsize=11)
        ax.legend()

        # Compare mean overall
        ax = axes[1]
        data = [gen["mean_overall"].values, esp["mean_overall"].values]
        bp = ax.boxplot(data, labels=["Generalistas", "Especialistas"],
                        patch_artist=True)
        bp["boxes"][0].set_facecolor("#27AE60")
        bp["boxes"][1].set_facecolor("#E74C3C")
        ax.set_ylabel("Prazer medio geral")
        ax.set_title(f"Cohen's d = {d:.3f}", fontsize=11)

        fig.suptitle(h["headline"], fontsize=13, fontweight="bold", y=1.02)
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "entropy_groups")

        result_text = (
            f"Generalistas: N = {len(gen):,}, prazer medio = {gen['mean_overall'].mean():.2f}\n"
            f"Especialistas: N = {len(esp):,}, prazer medio = {esp['mean_overall'].mean():.2f}\n"
            f"Mann-Whitney U = {stat:.0f}, p = {p_val:.2e}\n"
            f"Cohen's d = {d:.3f}"
        )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Shannon entropy + Mann-Whitney U",
            statistic_name="U",
            statistic_value=stat,
            effect_size_name="cohens_d",
            effect_size_value=d,
            p_value=p_val,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                "Entropia de Shannon dos 6 scores de fator (mede se o perfil "
                "de prazer e equilibrado ou concentrado). Divisao pela mediana "
                "em generalistas e especialistas. Mann-Whitney U para comparar "
                "o prazer medio geral entre os dois grupos."
            ),
            premises=(
                "Entropia ja calculada na Fase 2 (respondent_profiles). "
                "Mann-Whitney nao exige normalidade."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"|d| = {abs(d):.3f}. "
                f"{'Efeito pequeno (d < 0.2).' if abs(d) < 0.2 else ''}"
                f"{'Efeito moderado.' if 0.2 <= abs(d) < 0.5 else ''}"
                f"{'Efeito grande.' if abs(d) >= 0.5 else ''}"
            ),
            limitations=(
                "A divisao pela mediana e arbitraria. "
                "Amostra de conveniencia."
            ),
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # H12 — Clustering validation
    # ------------------------------------------------------------------

    def _test_clustering_validation(self, h):
        hid = h["id"]
        params = h["params"]
        methods = params["methods"]
        k_min, k_max = params["k_range"]
        n_boot = params["n_bootstrap"]
        threshold = params["threshold_silhouette"]

        X = self.df[self.factor_cols].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Run methods for each k
        sil_results = {}
        best_sil = -1
        best_k = None
        best_method = None
        best_labels = None

        for method in methods:
            sil_results[method] = {}
            for k in range(k_min, k_max + 1):
                if method == "kmeans":
                    model = KMeans(n_clusters=k, random_state=self.seed, n_init=10)
                    labels = model.fit_predict(X_scaled)
                elif method == "hierarchical":
                    model = AgglomerativeClustering(n_clusters=k)
                    labels = model.fit_predict(X_scaled)
                elif method == "gmm":
                    model = GaussianMixture(n_components=k, random_state=self.seed, n_init=5)
                    labels = model.fit_predict(X_scaled)
                else:
                    continue

                sil = silhouette_score(X_scaled, labels)
                sil_results[method][k] = sil

                if sil > best_sil:
                    best_sil = sil
                    best_k = k
                    best_method = method
                    best_labels = labels

        # Bootstrap stability for best solution
        stabilities = []
        for _ in range(min(n_boot, 50)):  # cap at 50 for speed
            idx = np.random.choice(len(X_scaled), size=len(X_scaled), replace=True)
            X_boot = X_scaled[idx]
            if best_method == "kmeans":
                m = KMeans(n_clusters=best_k, random_state=None, n_init=5)
            elif best_method == "gmm":
                m = GaussianMixture(n_components=best_k, random_state=None, n_init=3)
            else:
                m = AgglomerativeClustering(n_clusters=best_k)
            boot_labels = m.fit_predict(X_boot)
            stabilities.append(silhouette_score(X_boot, boot_labels))

        stability_mean = np.mean(stabilities)
        stability_std = np.std(stabilities)

        is_spectrum = best_sil < threshold

        if is_spectrum:
            verdict = "confirmada"
            interp = (
                f"O melhor agrupamento encontrado ({best_method}, k={best_k}) "
                f"tem silhouette = {best_sil:.3f} — abaixo do limite de {threshold}. "
                f"Nenhum metodo encontrou grupos claros. "
                f"Prazer e um espectro, nao tipos separados."
            )
        else:
            verdict = "nao confirmada"
            interp = (
                f"O agrupamento {best_method} com k={best_k} tem "
                f"silhouette = {best_sil:.3f}, acima do limite. "
                f"Existem grupos distinguiveis."
            )

        # --- Figure ---
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Silhouette by k
        ax = axes[0]
        for method, sils in sil_results.items():
            ks = sorted(sils.keys())
            vals = [sils[k] for k in ks]
            ax.plot(ks, vals, marker="o", label=method, linewidth=2)
        ax.axhline(y=threshold, color="#E74C3C", linewidth=1.5, linestyle="--",
                   label=f"Limite = {threshold}")
        ax.set_xlabel("Numero de grupos (k)")
        ax.set_ylabel("Silhouette (qualidade da separacao)")
        ax.set_title("Qualidade do agrupamento por metodo", fontsize=11)
        ax.legend(fontsize=9)

        # Radar of best cluster profiles
        ax = axes[1]
        if best_labels is not None and best_k is not None:
            ax = fig.add_subplot(122, projection="polar")
            categories = [self.config["fatores"][f]["rotulo"] for f in self.factor_names]
            cluster_profiles = []
            cluster_labels = []
            colors = plt.cm.Set2(np.linspace(0, 1, best_k))
            for cl in range(best_k):
                mask = best_labels == cl
                profile = self.df[self.factor_cols][mask].mean().values.tolist()
                cluster_profiles.append(profile)
                cluster_labels.append(f"Grupo {cl+1} (N={mask.sum():,})")
            self._radar_chart(ax, categories, cluster_profiles,
                              cluster_labels, [c for c in colors],
                              title=f"Perfis (k={best_k}, sil={best_sil:.3f})")

        fig.suptitle(h["headline"], fontsize=13, fontweight="bold", y=1.02)
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "clustering_validation")

        result_text = "Silhouette por metodo e k:\n"
        for method, sils in sil_results.items():
            for k, sil in sorted(sils.items()):
                marker = " ← melhor" if method == best_method and k == best_k else ""
                result_text += f"  {method} k={k}: {sil:.3f}{marker}\n"
        result_text += (
            f"\nMelhor: {best_method} k={best_k}, silhouette = {best_sil:.3f}\n"
            f"Estabilidade (bootstrap): {stability_mean:.3f} ± {stability_std:.3f}"
        )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique=f"K-Means + Hierarchical + GMM (k={k_min}-{k_max})",
            statistic_name="best_silhouette",
            statistic_value=best_sil,
            effect_size_name="silhouette",
            effect_size_value=best_sil,
            p_value=np.nan,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                f"Tres metodos de agrupamento (K-Means, hierarquico, mistura "
                f"gaussiana) com k de {k_min} a {k_max}. Silhouette mede a "
                f"qualidade da separacao (0 = sem separacao, 1 = perfeita). "
                f"Estabilidade verificada com {n_boot} sub-amostras."
            ),
            premises=(
                "Dados padronizados (z-score) antes do agrupamento. "
                f"Limite para 'grupos claros': silhouette > {threshold}."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"Silhouette = {best_sil:.3f} — "
                f"{'muito fraco, sem grupos naturais.' if best_sil < 0.20 else ''}"
                f"{'fraco, grupos mal definidos.' if 0.20 <= best_sil < 0.25 else ''}"
                f"{'moderado, alguns grupos.' if 0.25 <= best_sil < 0.50 else ''}"
                f"{'forte, grupos claros.' if best_sil >= 0.50 else ''}"
            ),
            limitations=(
                "Agrupamento depende da escolha de variaveis e metodo. "
                "Silhouette < 0.25 nao prova que grupos nao existem — "
                "apenas que estes metodos nao os encontram nestes dados."
            ),
            figures=[fig_path],
        )

        # Save best labels for H15 reuse
        self._best_labels = best_labels
        self._best_k = best_k

    # ------------------------------------------------------------------
    # H13 — Quartile comparison (Thrilling Q1 vs Q4)
    # ------------------------------------------------------------------

    def _test_quartile_comparison(self, h):
        hid = h["id"]
        params = h["params"]
        factor = params["factor"]
        factor_col = f"factor_{factor}"

        q25 = self.df[factor_col].quantile(0.25)
        q75 = self.df[factor_col].quantile(0.75)

        low_group = self.df[self.df[factor_col] <= q25]
        high_group = self.df[self.df[factor_col] >= q75]

        label_high = f"Top 25% {factor}"
        label_low = f"Bottom 25% {factor}"

        comparisons = self._compare_groups_all_factors(
            high_group, low_group, label_high, label_low
        )

        n_significant = sum(1 for c in comparisons
                            if c["significant"] and c["fator"] != factor)
        max_d = max(abs(c["cohens_d"]) for c in comparisons if c["fator"] != factor)

        if n_significant >= 3 and max_d > 0.3:
            verdict = "confirmada"
            interp = (
                f"Quem busca emocao forte difere em {n_significant} dos outros "
                f"5 fatores. O maior efeito e d = {max_d:.3f}. "
                f"O perfil de prazer e realmente diferente."
            )
        elif n_significant >= 1:
            verdict = "inconclusiva"
            interp = (
                f"Diferencas em {n_significant} fator(es), mas os efeitos "
                f"sao pequenos (max d = {max_d:.3f})."
            )
        else:
            verdict = "nao confirmada"
            interp = "Nenhuma diferenca significativa nos outros fatores."

        # --- Figure (radar) ---
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="polar")
        categories = [self.config["fatores"][f]["rotulo"] for f in self.factor_names]
        prof_high = [high_group[f"factor_{f}"].mean() for f in self.factor_names]
        prof_low = [low_group[f"factor_{f}"].mean() for f in self.factor_names]
        self._radar_chart(ax, categories, [prof_high, prof_low],
                          [f"Top 25% (N={len(high_group):,})",
                           f"Bottom 25% (N={len(low_group):,})"],
                          ["#E74C3C", "#4472C4"])
        fig.suptitle(h["headline"], fontsize=13, fontweight="bold")
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "quartile_comparison")

        result_text = f"Comparacao Top 25% vs Bottom 25% do fator {factor}:\n\n"
        for c in comparisons:
            sig = "***" if c["significant"] else ""
            result_text += (
                f"  {c['rotulo']}: d = {c['cohens_d']:.3f}, "
                f"p_corr = {c['p_corrected']:.4f} {sig}\n"
            )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Mann-Whitney U + Cohen's d + FDR",
            statistic_name="n_significant_factors",
            statistic_value=n_significant,
            effect_size_name="max_cohens_d",
            effect_size_value=max_d,
            p_value=np.nan,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                f"Divisao da amostra em Top 25% e Bottom 25% do fator {factor}. "
                "Mann-Whitney U (compara grupos sem assumir normalidade) para "
                "cada um dos outros 5 fatores. Cohen's d mede o tamanho da "
                "diferenca. Correcao FDR para multiplas comparacoes."
            ),
            premises=(
                f"Top 25%: N = {len(high_group):,}. "
                f"Bottom 25%: N = {len(low_group):,}. "
                "Mann-Whitney nao exige normalidade."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"Maior efeito: d = {max_d:.3f}. "
                f"d < 0.2 = trivial, 0.2-0.5 = pequeno, 0.5-0.8 = medio, > 0.8 = grande."
            ),
            limitations=(
                "Quartis sao uma divisao arbitraria. "
                "Amostra de conveniencia. "
                "Correlacao, nao causalidade."
            ),
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # H14 — Group comparison (spiritual high vs low)
    # ------------------------------------------------------------------

    def _test_group_comparison(self, h):
        hid = h["id"]
        params = h["params"]
        item = params["item"]
        cut_high = params["cut_high"]
        cut_low = params["cut_low"]

        high_group = self.df[self.df[item] >= cut_high]
        low_group = self.df[self.df[item] <= cut_low]

        item_label = item
        for it in self.config["itens"]:
            if it["variavel"] == item:
                item_label = it["rotulo"]
                break

        comparisons = self._compare_groups_all_factors(
            high_group, low_group,
            f"{item_label} alto", f"{item_label} baixo"
        )

        n_significant = sum(1 for c in comparisons if c["significant"])
        max_d = max(abs(c["cohens_d"]) for c in comparisons) if comparisons else 0

        if n_significant >= 3 and max_d > 0.3:
            verdict = "confirmada"
            interp = (
                f"Quem pontua alto em {item_label} difere em {n_significant} "
                f"dos 6 fatores. O perfil de prazer e realmente diferente."
            )
        elif n_significant >= 1:
            verdict = "inconclusiva"
            interp = (
                f"Diferencas em {n_significant} fator(es), mas com efeitos "
                f"modestos (max d = {max_d:.3f})."
            )
        else:
            verdict = "nao confirmada"
            interp = "Nenhuma diferenca significativa entre os grupos."

        # --- Figure ---
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Radar
        ax_radar = fig.add_subplot(121, projection="polar")
        categories = [self.config["fatores"][f]["rotulo"] for f in self.factor_names]
        prof_high = [high_group[f"factor_{f}"].mean() for f in self.factor_names]
        prof_low = [low_group[f"factor_{f}"].mean() for f in self.factor_names]
        self._radar_chart(ax_radar, categories, [prof_high, prof_low],
                          [f"Alto (N={len(high_group):,})",
                           f"Baixo (N={len(low_group):,})"],
                          ["#8E44AD", "#F39C12"])

        # Effect sizes
        ax = fig.add_subplot(122)
        labels = [c["rotulo"] for c in comparisons]
        d_vals = [c["cohens_d"] for c in comparisons]
        colors = ["#E74C3C" if c["significant"] else "#BDC3C7" for c in comparisons]
        ax.barh(labels, d_vals, color=colors, alpha=0.85)
        ax.set_xlabel("Cohen's d (tamanho da diferenca)")
        ax.set_title("Diferencas por fator", fontsize=11)
        ax.axvline(x=0, color="gray", linewidth=0.8)
        ax.axvline(x=0.2, color="#E74C3C", linewidth=0.8, linestyle=":",
                   alpha=0.5)
        ax.axvline(x=-0.2, color="#E74C3C", linewidth=0.8, linestyle=":",
                   alpha=0.5)

        fig.suptitle(h["headline"], fontsize=13, fontweight="bold", y=1.02)
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "group_comparison")

        result_text = (
            f"Grupo alto ({item_label} >= {cut_high}): N = {len(high_group):,}\n"
            f"Grupo baixo ({item_label} <= {cut_low}): N = {len(low_group):,}\n\n"
        )
        for c in comparisons:
            sig = "***" if c["significant"] else ""
            result_text += (
                f"  {c['rotulo']}: d = {c['cohens_d']:.3f}, "
                f"p_corr = {c['p_corrected']:.4f} {sig}\n"
            )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Mann-Whitney U + Cohen's d + FDR",
            statistic_name="n_significant_factors",
            statistic_value=n_significant,
            effect_size_name="max_cohens_d",
            effect_size_value=max_d,
            p_value=np.nan,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                f"Divisao por pontuacao no item {item_label}: "
                f"alto (>= {cut_high}) vs baixo (<= {cut_low}). "
                "Mann-Whitney U + Cohen's d para cada fator. Correcao FDR."
            ),
            premises=(
                f"Alto: N = {len(high_group):,}, Baixo: N = {len(low_group):,}. "
                "Mann-Whitney nao exige normalidade."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"Maior efeito: d = {max_d:.3f}. "
                f"d < 0.2 = trivial, 0.2-0.5 = pequeno, > 0.5 = medio."
            ),
            limitations=(
                "Pontos de corte arbitrarios. "
                "Correlacao, nao causalidade. "
                "Amostra de conveniencia."
            ),
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # H15 — Profile search (intellectual-dominant cluster)
    # ------------------------------------------------------------------

    def _test_profile_search(self, h):
        hid = h["id"]
        params = h["params"]
        dominant = params["dominant_factor"]
        k_min, k_max = params["k_range"]

        X = self.df[self.factor_cols].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        found = False
        found_k = None
        found_cluster = None
        found_profile = None
        found_n = 0

        for k in range(k_min, k_max + 1):
            km = KMeans(n_clusters=k, random_state=self.seed, n_init=10)
            labels = km.fit_predict(X_scaled)

            for cl in range(k):
                mask = labels == cl
                cluster_df = self.df[self.factor_cols][mask]
                means = cluster_df.mean()

                # Check if dominant factor is highest AND others are below global mean
                global_means = self.df[self.factor_cols].mean()
                dom_col = f"factor_{dominant}"
                is_dominant = means[dom_col] == means.max()
                others_below = all(
                    means[f"factor_{f}"] < global_means[f"factor_{f}"]
                    for f in self.factor_names if f != dominant
                )

                if is_dominant and others_below and mask.sum() >= 50:
                    found = True
                    found_k = k
                    found_cluster = cl
                    found_profile = means.values.tolist()
                    found_n = mask.sum()
                    break
            if found:
                break

        if found:
            verdict = "confirmada"
            interp = (
                f"Encontrado um grupo de {found_n:,} pessoas (k={found_k}) "
                f"com {dominant} como fator dominante e todos os outros "
                f"abaixo da media geral."
            )
        else:
            verdict = "nao confirmada"
            interp = (
                f"Nenhum agrupamento (k={k_min} a {k_max}) produziu um grupo "
                f"com {dominant} dominante e o resto abaixo da media. "
                f"O perfil 'puramente intelectual' nao aparece como um tipo separado."
            )

        # --- Figure ---
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="polar")
        categories = [self.config["fatores"][f]["rotulo"] for f in self.factor_names]
        global_profile = self.df[self.factor_cols].mean().values.tolist()
        profiles = [global_profile]
        labels = [f"Media geral (N={self.n_respondents:,})"]
        colors = ["#BDC3C7"]

        if found:
            profiles.append(found_profile)
            labels.append(f"Grupo intelectual (N={found_n:,})")
            colors.append("#8E44AD")

        self._radar_chart(ax, categories, profiles, labels, colors)
        fig.suptitle(h["headline"], fontsize=13, fontweight="bold")
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "profile_search")

        result_text = (
            f"Busca por perfil '{dominant}-dominante' em k={k_min} a {k_max}:\n"
            f"{'Encontrado' if found else 'Nao encontrado'}."
        )
        if found:
            result_text += f"\n  k = {found_k}, grupo {found_cluster}, N = {found_n:,}"
            for f, val in zip(self.factor_names, found_profile):
                result_text += f"\n  {f}: {val:.2f}"

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique=f"K-Means profile search (k={k_min}-{k_max})",
            statistic_name="cluster_size",
            statistic_value=found_n if found else 0,
            effect_size_name="n/a",
            effect_size_value=np.nan,
            p_value=np.nan,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                f"K-Means com k de {k_min} a {k_max}. Para cada solucao, "
                f"procurar um grupo onde o fator {dominant} seja o mais alto "
                f"e todos os outros fiquem abaixo da media geral. "
                f"Criterio minimo: pelo menos 50 pessoas no grupo."
            ),
            premises=(
                "Dados padronizados. "
                "A busca por um perfil especifico e exploratoria — "
                "o grupo pode nao existir como tipo natural."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"{'Grupo com ' + str(found_n) + ' pessoas — pequeno mas real.' if found else 'Perfil nao encontrado — pode nao existir como tipo separado.'}"
            ),
            limitations=(
                "Buscar um perfil pre-definido e enviesado. "
                "O grupo pode ser um artefato do agrupamento. "
                "Resultado depende do k escolhido."
            ),
            figures=[fig_path],
        )
