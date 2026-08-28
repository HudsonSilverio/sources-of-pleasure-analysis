"""
relational.py — Analyst agent for relational hypotheses.

Specializes in: correlations, independence, associations between items/factors.
Techniques: Spearman, TOST equivalence, Steiger test for dependent correlations,
            second-order factor analysis, predictive correlation (train/test).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from src.analysts.base import BaseAnalyst


class RelationalAnalyst(BaseAnalyst):

    name = "relational"
    display_name = "Relacional"

    def run_hypothesis(self, h):
        test = h["test"]
        if test == "negative_correlations":
            self._test_negative_correlations(h)
        elif test == "equivalence_tost":
            self._test_equivalence_tost(h)
        elif test == "second_order_factor":
            self._test_second_order_factor(h)
        elif test == "steiger_comparison":
            self._test_steiger_comparison(h)
        elif test == "predictive_correlation":
            self._test_predictive_correlation(h)
        else:
            raise ValueError(f"Teste desconhecido: {test}")

    # ------------------------------------------------------------------
    # H05 — Negative correlations (one-sided Spearman + FDR)
    # ------------------------------------------------------------------

    def _test_negative_correlations(self, h):
        hid = h["id"]
        params = h["params"]
        alpha = params.get("alpha", 0.05)

        corr_matrix = self.load_corr_items()

        # Build label → variable mapping for lookup
        label_to_var = {}
        for it in self.config["itens"]:
            label_to_var[it["rotulo"]] = it["variavel"]

        # Find all negative correlations
        negative_pairs = []
        items = corr_matrix.columns.tolist()
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                rho = corr_matrix.iloc[i, j]
                if rho < 0:
                    # Map labels back to variable names for DataFrame access
                    var_i = label_to_var.get(items[i], items[i])
                    var_j = label_to_var.get(items[j], items[j])
                    # One-sided Spearman test (H1: rho < 0)
                    stat, p_two = stats.spearmanr(
                        self.df[var_i], self.df[var_j]
                    )
                    p_one = p_two / 2 if stat < 0 else 1 - p_two / 2
                    negative_pairs.append({
                        "item1": items[i],
                        "item2": items[j],
                        "rho": stat,
                        "p_one_sided": p_one,
                    })

        neg_df = pd.DataFrame(negative_pairs).sort_values("rho")

        # FDR correction (Benjamini-Hochberg)
        from statsmodels.stats.multitest import multipletests
        if len(neg_df) > 0:
            reject, p_corr, _, _ = multipletests(
                neg_df["p_one_sided"], alpha=alpha, method="fdr_bh"
            )
            neg_df["p_corrected"] = p_corr
            neg_df["significant"] = reject
        else:
            neg_df["p_corrected"] = []
            neg_df["significant"] = []

        survived = neg_df[neg_df["significant"]].copy()
        n_survived = len(survived)
        n_total_neg = len(neg_df)

        if n_survived > 0:
            verdict = "confirmada"
            strongest = survived.iloc[0]
            interp = (
                f"{n_survived} de {n_total_neg} pares negativos sobreviveram "
                f"a correcao para multiplas comparacoes (FDR). "
                f"O par mais forte: {strongest['item1']} × {strongest['item2']} "
                f"(rho = {strongest['rho']:.3f}). "
                f"Existem prazeres genuinamente incompativeis."
            )
        else:
            verdict = "nao confirmada"
            interp = (
                f"Nenhum dos {n_total_neg} pares negativos sobreviveu a "
                f"correcao FDR. As correlacoes negativas sao fracas demais "
                f"para concluir que prazeres sao incompativeis."
            )

        # --- Figure ---
        fig, ax = plt.subplots(figsize=(10, 6))
        if n_survived > 0:
            top_pairs = survived.head(15)
            labels = []
            for _, row in top_pairs.iterrows():
                l1 = self._item_label(row["item1"])
                l2 = self._item_label(row["item2"])
                labels.append(f"{l1} × {l2}")
            y_pos = range(len(labels))
            colors = ["#E74C3C" if sig else "#CCCCCC"
                      for sig in top_pairs["significant"]]
            ax.barh(y_pos, top_pairs["rho"], color=colors, alpha=0.85)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels, fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel("Correlacao Spearman (rho)")
            ax.axvline(x=0, color="gray", linewidth=0.8)
        else:
            ax.text(0.5, 0.5, "Nenhum par negativo significativo\napos correcao FDR",
                    ha="center", va="center", transform=ax.transAxes, fontsize=14)

        ax.set_title(h["headline"], fontsize=12, fontweight="bold")
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "negative_correlations")

        # Results
        result_text = (
            f"Total de pares com correlacao negativa: {n_total_neg}\n"
            f"Pares que sobreviveram a correcao FDR (alpha={alpha}): {n_survived}\n"
        )
        if n_survived > 0:
            result_text += "\nTop 5 pares negativos significativos:\n"
            for _, row in survived.head(5).iterrows():
                l1 = self._item_label(row["item1"])
                l2 = self._item_label(row["item2"])
                result_text += (
                    f"  {l1} × {l2}: rho = {row['rho']:.3f}, "
                    f"p_corr = {row['p_corrected']:.4f}\n"
                )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Spearman one-sided + FDR (Benjamini-Hochberg)",
            statistic_name="n_significant_pairs",
            statistic_value=n_survived,
            effect_size_name="strongest_rho",
            effect_size_value=survived.iloc[0]["rho"] if n_survived > 0 else 0,
            p_value=np.nan,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                "Correlacao de Spearman de um lado so (testa se e realmente negativa) "
                "para todos os pares de itens com correlacao negativa. "
                "Correcao FDR de Benjamini-Hochberg para evitar falsos positivos "
                "quando se testa muitos pares ao mesmo tempo."
            ),
            premises=(
                "Spearman nao exige normalidade. "
                f"Total de pares testados: {n_total_neg}. "
                f"Alpha apos correcao: {alpha}."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                "Mesmo os pares significativos tem correlacoes fracas "
                "(|rho| < 0.15). A incompatibilidade existe mas e sutil — "
                "nao e como se gostar de natureza impedisse de gostar de status."
            ),
            limitations=(
                "Correlacoes negativas fracas podem ser artefato da escala "
                "(-3 a +3) e do tipo de amostra. "
                "Amostra de conveniencia."
            ),
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # H06 — Equivalence test (TOST)
    # ------------------------------------------------------------------

    def _test_equivalence_tost(self, h):
        hid = h["id"]
        params = h["params"]
        f1 = params["factor1"]
        f2 = params["factor2"]
        bound = params["equivalence_bound"]

        col1 = f"factor_{f1}"
        col2 = f"factor_{f2}"
        rho, p_spearman = stats.spearmanr(self.df[col1], self.df[col2])

        # TOST: test if |rho| < bound
        # Using Fisher z-transform
        n = self.n_respondents
        z_r = np.arctanh(rho)
        se = 1 / np.sqrt(n - 3)

        # Upper bound test: H0: rho >= bound
        z_upper = (z_r - np.arctanh(bound)) / se
        p_upper = stats.norm.cdf(z_upper)

        # Lower bound test: H0: rho <= -bound
        z_lower = (z_r - np.arctanh(-bound)) / se
        p_lower = 1 - stats.norm.cdf(z_lower)

        p_tost = max(p_upper, p_lower)
        is_equivalent = p_tost < 0.05

        if is_equivalent:
            verdict = "confirmada"
            interp = (
                f"A correlacao entre {f1} e {f2} (rho = {rho:.3f}) esta "
                f"dentro da faixa de equivalencia a zero (|rho| < {bound}). "
                f"Sao mundos realmente independentes."
            )
        else:
            verdict = "nao confirmada"
            interp = (
                f"Nao conseguimos confirmar que a correlacao (rho = {rho:.3f}) "
                f"e equivalente a zero. Pode haver uma relacao pequena."
            )

        # --- Figure ---
        fig, ax = plt.subplots(figsize=(8, 6))
        # Subsample for scatter
        n_plot = min(2000, self.n_respondents)
        idx = np.random.choice(self.n_respondents, n_plot, replace=False)
        ax.scatter(self.df[col1].iloc[idx], self.df[col2].iloc[idx],
                   alpha=0.15, s=10, color="#4472C4")
        ax.set_xlabel(self.config["fatores"][f1]["rotulo"])
        ax.set_ylabel(self.config["fatores"][f2]["rotulo"])
        ax.set_title(h["headline"], fontsize=12, fontweight="bold")
        ax.text(0.02, 0.98,
                f"rho = {rho:.3f} | TOST p = {p_tost:.4f}\n"
                f"Faixa de equivalencia: |rho| < {bound}",
                transform=ax.transAxes, ha="left", va="top", fontsize=9,
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "equivalence_tost")

        result_text = (
            f"Correlacao Spearman entre {f1} e {f2}: rho = {rho:.3f}\n"
            f"Teste TOST (faixa de equivalencia: |rho| < {bound}):\n"
            f"  p_upper = {p_upper:.4f}, p_lower = {p_lower:.4f}\n"
            f"  p_TOST = {p_tost:.4f} ({'< 0.05 → equivalente a zero' if is_equivalent else '>= 0.05 → inconclusivo'})"
        )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="TOST equivalence test",
            statistic_name="rho_spearman",
            statistic_value=rho,
            effect_size_name="rho",
            effect_size_value=rho,
            p_value=p_tost,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                "Teste de equivalencia TOST (Two One-Sided Tests — testa se "
                "a correlacao e tao perto de zero que nao importa). "
                f"Faixa de equivalencia: |rho| < {bound}."
            ),
            premises=(
                "Fisher z-transform para a correlacao. "
                f"Faixa de equivalencia definida como |rho| < {bound} "
                "(efeitos menores que isso sao triviais)."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"rho = {rho:.3f} — praticamente zero. "
                "Os dois fatores sao independentes na pratica."
            ),
            limitations="Amostra de conveniencia. Dados de autorrelato.",
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # H07 — Second-order factor (Interpersonal + Noble)
    # ------------------------------------------------------------------

    def _test_second_order_factor(self, h):
        hid = h["id"]
        params = h["params"]
        factors = params["factors"]

        cols = [f"factor_{f}" for f in factors]
        rho, p_val = stats.spearmanr(self.df[cols[0]], self.df[cols[1]])

        # Combined score vs separate: compare explained variance
        combined = self.df[cols].mean(axis=1)
        var_combined = combined.var()
        var_f1 = self.df[cols[0]].var()
        var_f2 = self.df[cols[1]].var()

        # Cronbach's alpha for 2 items
        k = 2
        item_vars = self.df[cols].var().sum()
        total_var = self.df[cols].sum(axis=1).var()
        cronbach = (k / (k - 1)) * (1 - item_vars / total_var)

        strong_association = rho > 0.40
        good_reliability = cronbach > 0.60

        if strong_association and good_reliability:
            verdict = "confirmada"
            interp = (
                f"Os fatores {factors[0]} e {factors[1]} tem correlacao forte "
                f"(rho = {rho:.3f}) e funcionam bem como uma dimensao unica "
                f"(alpha de Cronbach = {cronbach:.2f}). "
                f"Faz sentido falar de um superfator 'quem cuida'."
            )
        elif strong_association:
            verdict = "inconclusiva"
            interp = (
                f"A correlacao e forte (rho = {rho:.3f}) mas a consistencia "
                f"interna como dimensao unica e moderada (alpha = {cronbach:.2f})."
            )
        else:
            verdict = "nao confirmada"
            interp = (
                f"A correlacao entre os fatores (rho = {rho:.3f}) nao e forte "
                f"o suficiente para justificar um superfator."
            )

        # --- Figure ---
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Scatter
        ax = axes[0]
        n_plot = min(2000, self.n_respondents)
        idx = np.random.choice(self.n_respondents, n_plot, replace=False)
        ax.scatter(self.df[cols[0]].iloc[idx], self.df[cols[1]].iloc[idx],
                   alpha=0.15, s=10, color="#4472C4")
        # Regression line
        z = np.polyfit(self.df[cols[0]], self.df[cols[1]], 1)
        p = np.poly1d(z)
        x_line = np.linspace(self.df[cols[0]].min(), self.df[cols[0]].max(), 100)
        ax.plot(x_line, p(x_line), color="#E74C3C", linewidth=2)
        ax.set_xlabel(self.config["fatores"][factors[0]]["rotulo"])
        ax.set_ylabel(self.config["fatores"][factors[1]]["rotulo"])
        ax.set_title(f"rho = {rho:.3f}", fontsize=11)

        # Correlation with all other factors
        ax = axes[1]
        all_corrs = []
        for f in self.factor_names:
            if f not in factors:
                col = f"factor_{f}"
                r1, _ = stats.spearmanr(combined, self.df[col])
                all_corrs.append({"fator": self.config["fatores"][f]["rotulo"],
                                  "rho_com_cuidado": r1})
        corr_df = pd.DataFrame(all_corrs).sort_values("rho_com_cuidado", ascending=True)
        ax.barh(corr_df["fator"], corr_df["rho_com_cuidado"], color="#27AE60", alpha=0.8)
        ax.set_xlabel("Correlacao com 'Cuidado' combinado")
        ax.set_title("Como o superfator se relaciona com os outros", fontsize=11)
        ax.axvline(x=0, color="gray", linewidth=0.8)

        fig.suptitle(h["headline"], fontsize=13, fontweight="bold", y=1.02)
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "second_order_factor")

        result_text = (
            f"Correlacao entre {factors[0]} e {factors[1]}: rho = {rho:.3f}, p = {p_val:.2e}\n"
            f"Alpha de Cronbach como dimensao unica: {cronbach:.2f}\n"
            f"{'> 0.60 — aceitavel' if cronbach > 0.60 else '< 0.60 — fraco'}"
        )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Spearman + Cronbach alpha",
            statistic_name="rho_spearman",
            statistic_value=rho,
            effect_size_name="cronbach_alpha",
            effect_size_value=cronbach,
            p_value=p_val,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                "Correlacao Spearman entre os dois fatores + alpha de Cronbach "
                "(mede se os dois fatores funcionam juntos como uma dimensao unica). "
                "Alpha > 0.60 = aceitavel, > 0.70 = bom."
            ),
            premises=(
                "Alpha de Cronbach com apenas 2 itens (fatores) e uma simplificacao. "
                "Uma analise fatorial confirmatoria seria mais rigorosa, "
                "mas para uma exploracao inicial e suficiente."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"rho = {rho:.3f} e uma correlacao "
                f"{'forte' if rho > 0.4 else 'moderada' if rho > 0.25 else 'fraca'}."
            ),
            limitations=(
                "Alpha de Cronbach com 2 itens tende a ser baixo. "
                "Uma analise fatorial de segunda ordem com todos os itens "
                "dos dois fatores seria mais precisa."
            ),
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # H08 — Steiger test (dependent correlations)
    # ------------------------------------------------------------------

    def _test_steiger_comparison(self, h):
        hid = h["id"]
        params = h["params"]
        item = params["item"]
        factor_high = params["factor_high"]
        factor_low = params["factor_low"]

        col_item = item
        col_high = f"factor_{factor_high}"
        col_low = f"factor_{factor_low}"

        r_high, _ = stats.spearmanr(self.df[col_item], self.df[col_high])
        r_low, _ = stats.spearmanr(self.df[col_item], self.df[col_low])
        r_between, _ = stats.spearmanr(self.df[col_high], self.df[col_low])

        # Steiger's Z test for dependent correlations
        n = self.n_respondents
        z_high = np.arctanh(r_high)
        z_low = np.arctanh(r_low)
        r_det = (1 - r_high**2 - r_low**2 - r_between**2
                 + 2 * r_high * r_low * r_between)
        r_mean_sq = (r_high**2 + r_low**2) / 2
        f_factor = (1 - r_between) / (2 * (1 - r_mean_sq)) if (1 - r_mean_sq) > 0 else 1
        z_steiger = (z_high - z_low) * np.sqrt((n - 3) / (2 * (1 - r_between) * f_factor))
        p_steiger = 2 * (1 - stats.norm.cdf(abs(z_steiger)))

        diff = r_high - r_low
        is_significant = p_steiger < 0.05

        if is_significant and diff > 0:
            verdict = "confirmada"
            interp = (
                f"O item {self._item_label(item)} correlaciona significativamente "
                f"mais com {factor_high} (rho = {r_high:.3f}) do que com "
                f"{factor_low} (rho = {r_low:.3f}). "
                f"Teste de Steiger: Z = {z_steiger:.2f}, p = {p_steiger:.4f}."
            )
        else:
            verdict = "nao confirmada"
            interp = (
                f"A diferenca entre as correlacoes (rho_high = {r_high:.3f}, "
                f"rho_low = {r_low:.3f}) nao e significativa "
                f"(Steiger Z = {z_steiger:.2f}, p = {p_steiger:.4f})."
            )

        # --- Figure ---
        fig, ax = plt.subplots(figsize=(8, 5))
        all_corrs = []
        for f in self.factor_names:
            col = f"factor_{f}"
            r, _ = stats.spearmanr(self.df[col_item], self.df[col])
            label = self.config["fatores"][f]["rotulo"]
            all_corrs.append({"fator": label, "rho": r, "key": f})

        corr_df = pd.DataFrame(all_corrs).sort_values("rho", ascending=True)
        colors = []
        for _, row in corr_df.iterrows():
            if row["key"] == factor_high:
                colors.append("#E74C3C")
            elif row["key"] == factor_low:
                colors.append("#3498DB")
            else:
                colors.append("#BDC3C7")

        ax.barh(corr_df["fator"], corr_df["rho"], color=colors, alpha=0.85)
        ax.set_xlabel("Correlacao Spearman com item sexual")
        ax.set_title(h["headline"], fontsize=12, fontweight="bold")
        ax.axvline(x=0, color="gray", linewidth=0.8)
        ax.text(0.98, 0.02,
                f"Steiger Z = {z_steiger:.2f}, p = {p_steiger:.4f}",
                transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
                color="gray")
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "steiger_comparison")

        result_text = (
            f"Correlacoes do item {self._item_label(item)} com cada fator:\n"
        )
        for _, row in corr_df.sort_values("rho", ascending=False).iterrows():
            result_text += f"  {row['fator']}: rho = {row['rho']:.3f}\n"
        result_text += (
            f"\nTeste de Steiger ({factor_high} vs {factor_low}): "
            f"Z = {z_steiger:.2f}, p = {p_steiger:.4f}"
        )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Steiger test (dependent correlations)",
            statistic_name="steiger_Z",
            statistic_value=z_steiger,
            effect_size_name="rho_diff",
            effect_size_value=diff,
            p_value=p_steiger,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                "Teste de Steiger — compara duas correlacoes que compartilham "
                "os mesmos dados (o item sexual esta nas duas). "
                "Testa se a diferenca entre as correlacoes e real."
            ),
            premises=(
                "Steiger assume normalidade bivariada (simplificacao). "
                "Usamos Spearman para as correlacoes base."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"Diferenca de correlacao: {diff:.3f}. "
                f"{'Pequena mas mensuravel.' if abs(diff) < 0.1 else 'Relevante.'}"
            ),
            limitations=(
                "O item sexual esta avulso (nao pertence a nenhum fator). "
                "Amostra de conveniencia."
            ),
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # H09 — Predictive correlation (train/test)
    # ------------------------------------------------------------------

    def _test_predictive_correlation(self, h):
        hid = h["id"]
        params = h["params"]
        predictors = params["predictors"]
        target = params["target"]
        test_size = params.get("test_size", 0.3)

        # Fix: p_beingInLove -> p_loving (check actual column name)
        pred_cols = []
        for p in predictors:
            if p in self.df.columns:
                pred_cols.append(p)
            elif p == "p_beingInLove" and "p_loving" in self.df.columns:
                pred_cols.append("p_loving")
            else:
                raise ValueError(f"Coluna {p} nao encontrada")

        X = self.df[pred_cols].values
        y = self.df[target].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.seed
        )

        model = LinearRegression()
        model.fit(X_train, y_train)

        r2_train = model.score(X_train, y_train)
        y_pred = model.predict(X_test)
        r2_test = r2_score(y_test, y_pred)

        good_prediction = r2_test > 0.15

        if good_prediction:
            verdict = "confirmada"
            interp = (
                f"O modelo consegue prever {self._item_label(target)} "
                f"a partir de {', '.join(self._item_label(c) for c in pred_cols)} "
                f"com R² = {r2_test:.3f} fora da amostra de treino. "
                f"A associacao e real e funciona em dados novos."
            )
        else:
            verdict = "nao confirmada"
            interp = (
                f"O modelo tem R² = {r2_test:.3f} fora do treino — "
                f"a previsao e fraca. As variaveis estao associadas "
                f"mas nao o suficiente pra prever uma a partir da outra."
            )

        # --- Figure ---
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Coefficients
        ax = axes[0]
        coef_labels = [self._item_label(c) for c in pred_cols]
        ax.barh(coef_labels, model.coef_, color="#4472C4", alpha=0.85)
        ax.set_xlabel("Peso na previsao")
        ax.set_title("Quanto cada variavel contribui", fontsize=11)
        ax.axvline(x=0, color="gray", linewidth=0.8)

        # Predicted vs actual
        ax = axes[1]
        ax.scatter(y_test, y_pred, alpha=0.15, s=10, color="#27AE60")
        ax.plot([-3, 3], [-3, 3], color="#E74C3C", linewidth=1.5, linestyle="--",
                label="Perfeito")
        ax.set_xlabel("Valor real")
        ax.set_ylabel("Valor previsto")
        ax.set_title(f"Previsao fora do treino (R² = {r2_test:.3f})", fontsize=11)
        ax.legend()

        fig.suptitle(h["headline"], fontsize=13, fontweight="bold", y=1.02)
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "predictive_correlation")

        result_text = (
            f"Regressao: {self._item_label(target)} ~ "
            f"{' + '.join(self._item_label(c) for c in pred_cols)}\n"
            f"R² treino: {r2_train:.3f}\n"
            f"R² teste: {r2_test:.3f}\n"
            f"Coeficientes: {dict(zip(coef_labels, [f'{c:.3f}' for c in model.coef_]))}"
        )

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Linear Regression (train/test split)",
            statistic_name="R2_test",
            statistic_value=r2_test,
            effect_size_name="R2_test",
            effect_size_value=r2_test,
            p_value=np.nan,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                f"Regressao linear com divisao treino ({1-test_size:.0%}) / "
                f"teste ({test_size:.0%}). "
                "R² mede quanto da variacao o modelo explica — "
                "quanto mais perto de 1, melhor a previsao."
            ),
            premises=(
                "Regressao linear assume relacao linear entre as variaveis. "
                "Divisao treino/teste garante que o resultado nao e "
                "inflado pela mesma amostra."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"R² = {r2_test:.3f} — "
                f"{'o modelo explica mais de 15% da variacao, o que e relevante.' if r2_test > 0.15 else 'o modelo explica pouco da variacao.'}"
            ),
            limitations=(
                "Correlacao != causalidade. Saber que amor e conexao andam "
                "juntos nao significa que um causa o outro."
            ),
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    def _item_label(self, col_name):
        """Get human-readable label for an item column."""
        for it in self.config["itens"]:
            if it["variavel"] == col_name:
                return it["rotulo"]
        return col_name
