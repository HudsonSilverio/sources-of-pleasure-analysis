"""
predictive.py — Analyst agent for predictive hypotheses.

Specializes in: what predicts what, regression, relative importance.
Techniques: linear regression with train/test split, multiple regression
            with standardized coefficients.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler

from src.analysts.base import BaseAnalyst


class PredictiveAnalyst(BaseAnalyst):

    name = "predictive"
    display_name = "Preditivo"

    def run_hypothesis(self, h):
        test = h["test"]
        if test == "regression_train_test":
            self._test_regression_train_test(h)
        elif test == "multiple_regression":
            self._test_multiple_regression(h)
        else:
            raise ValueError(f"Teste desconhecido: {test}")

    # ------------------------------------------------------------------
    # H16 — Regression train/test (adrenaline → relaxation)
    # ------------------------------------------------------------------

    def _test_regression_train_test(self, h):
        hid = h["id"]
        params = h["params"]
        predictors = params["predictors"]
        target = params["target"]
        test_size = params.get("test_size", 0.3)

        pred_labels = [self._item_label(p) for p in predictors]
        target_label = self._item_label(target)

        X = self.df[predictors].values
        y = self.df[target].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.seed
        )

        model = LinearRegression()
        model.fit(X_train, y_train)

        r2_train = model.score(X_train, y_train)
        y_pred = model.predict(X_test)
        r2_test = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        # Also run reverse: target → predictors (for each)
        reverse_r2 = {}
        for pred in predictors:
            X_rev = self.df[[target]].values
            y_rev = self.df[pred].values
            Xr_train, Xr_test, yr_train, yr_test = train_test_split(
                X_rev, y_rev, test_size=test_size, random_state=self.seed
            )
            mr = LinearRegression().fit(Xr_train, yr_train)
            reverse_r2[pred] = r2_score(yr_test, mr.predict(Xr_test))

        # Check if coefficients are negative (opposing paths)
        all_negative = all(c < 0 for c in model.coef_)
        any_negative = any(c < 0 for c in model.coef_)

        if all_negative and r2_test > 0.01:
            verdict = "confirmada"
            interp = (
                f"Todos os itens de adrenalina tem coeficiente negativo na "
                f"previsao de {target_label}. Quem gosta de emocao forte "
                f"tende a gostar menos de relaxamento. R² = {r2_test:.3f}."
            )
        elif any_negative and r2_test > 0.005:
            verdict = "inconclusiva"
            interp = (
                f"Alguns itens de adrenalina tem efeito negativo, mas o "
                f"poder de previsao e muito fraco (R² = {r2_test:.3f})."
            )
        else:
            verdict = "nao confirmada"
            interp = (
                f"Os itens de adrenalina nao preveem {target_label} "
                f"na direcao esperada (R² = {r2_test:.3f})."
            )

        # --- Figure ---
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Coefficients
        ax = axes[0]
        colors = ["#E74C3C" if c < 0 else "#27AE60" for c in model.coef_]
        ax.barh(pred_labels, model.coef_, color=colors, alpha=0.85)
        ax.set_xlabel("Coeficiente (peso na previsao)")
        ax.set_title(f"Previsao de '{target_label}'", fontsize=11)
        ax.axvline(x=0, color="gray", linewidth=0.8)
        for i, (label, coef) in enumerate(zip(pred_labels, model.coef_)):
            ax.text(coef, i, f"  {coef:.3f}", va="center", fontsize=9)

        # Predicted vs actual
        ax = axes[1]
        ax.scatter(y_test, y_pred, alpha=0.1, s=10, color="#4472C4")
        ax.plot([-3, 3], [-3, 3], color="#E74C3C", linewidth=1.5, linestyle="--")
        ax.set_xlabel(f"Valor real ({target_label})")
        ax.set_ylabel("Valor previsto")
        ax.set_title(f"R² teste = {r2_test:.3f} | MAE = {mae:.2f}", fontsize=11)

        fig.suptitle(h["headline"], fontsize=13, fontweight="bold", y=1.02)
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "regression")

        result_text = (
            f"Modelo: {target_label} ~ {' + '.join(pred_labels)}\n"
            f"R² treino: {r2_train:.4f}\n"
            f"R² teste: {r2_test:.4f}\n"
            f"MAE teste: {mae:.2f}\n\n"
            f"Coeficientes:\n"
        )
        for label, coef in zip(pred_labels, model.coef_):
            result_text += f"  {label}: {coef:.4f}\n"
        result_text += f"  Intercepto: {model.intercept_:.4f}\n"
        result_text += f"\nModelo reverso (relaxamento → adrenalina):\n"
        for pred, r2 in reverse_r2.items():
            result_text += f"  {self._item_label(pred)}: R² = {r2:.4f}\n"

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
                f"teste ({test_size:.0%}). Verifica se itens de adrenalina "
                f"preveem relaxamento (e vice-versa). "
                f"R² mede quanto da variacao o modelo explica."
            ),
            premises=(
                "Regressao linear assume relacao linear. "
                "Divisao treino/teste evita resultado inflado."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"R² = {r2_test:.3f} — "
                f"{'previsao muito fraca. Os dois caminhos existem mas sao quase independentes.' if r2_test < 0.05 else ''}"
                f"{'previsao fraca mas detectavel.' if 0.05 <= r2_test < 0.15 else ''}"
                f"{'previsao moderada.' if r2_test >= 0.15 else ''}"
            ),
            limitations=(
                "R² baixo nao significa que nao existe relacao — "
                "significa que outros fatores tambem influenciam. "
                "Correlacao nao e causalidade."
            ),
            figures=[fig_path],
        )

    # ------------------------------------------------------------------
    # H17 — Multiple regression (factors → mean overall)
    # ------------------------------------------------------------------

    def _test_multiple_regression(self, h):
        hid = h["id"]
        params = h["params"]
        target = params["target"]

        profiles = self.load_respondent_profiles()

        if target == "mean_overall":
            y = profiles["mean_overall"].values
            target_label = "prazer medio geral"
        else:
            y = self.df[target].values
            target_label = target

        X = self.df[self.factor_cols].values
        factor_labels = [self.config["fatores"][f]["rotulo"] for f in self.factor_names]

        # Standardize for comparable coefficients
        scaler_X = StandardScaler()
        scaler_y = StandardScaler()
        X_std = scaler_X.fit_transform(X)
        y_std = scaler_y.fit_transform(y.reshape(-1, 1)).flatten()

        model = LinearRegression()
        model.fit(X_std, y_std)

        # Raw model for R²
        model_raw = LinearRegression()
        model_raw.fit(X, y)
        r2 = model_raw.score(X, y)

        # Standardized coefficients (beta weights)
        betas = model.coef_

        # Sort by absolute value
        sorted_idx = np.argsort(np.abs(betas))[::-1]
        top_factor = factor_labels[sorted_idx[0]]
        top_beta = betas[sorted_idx[0]]

        # Note about circularity
        verdict = "confirmada"
        interp = (
            f"O fator que mais contribui para o prazer geral e "
            f"'{top_factor}' (beta = {top_beta:.3f}). "
            f"R² total = {r2:.3f} — os 6 fatores explicam {r2*100:.1f}% "
            f"da variacao no prazer geral. "
            f"NOTA: como os fatores fazem parte dos 37 itens, "
            f"essa analise mostra pesos relativos, nao uma descoberta "
            f"independente."
        )

        # --- Figure ---
        fig, ax = plt.subplots(figsize=(8, 5))
        sorted_labels = [factor_labels[i] for i in sorted_idx]
        sorted_betas = [betas[i] for i in sorted_idx]
        colors = ["#E74C3C" if i == 0 else "#4472C4" for i in range(len(sorted_betas))]

        ax.barh(range(len(sorted_labels)), sorted_betas, color=colors, alpha=0.85)
        ax.set_yticks(range(len(sorted_labels)))
        ax.set_yticklabels(sorted_labels)
        ax.invert_yaxis()
        ax.set_xlabel("Beta padronizado (peso relativo)")
        ax.set_title(h["headline"], fontsize=12, fontweight="bold")
        ax.axvline(x=0, color="gray", linewidth=0.8)

        for i, beta in enumerate(sorted_betas):
            ax.text(beta, i, f"  {beta:.3f}", va="center", fontsize=9)

        ax.text(0.98, 0.02,
                f"R² = {r2:.3f} | N = {self.n_respondents:,}\n"
                f"Nota: fatores sao parte dos 37 itens (circularidade parcial)",
                transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
                color="gray")
        fig.tight_layout()
        fig_path = self._save_fig(fig, hid, "multiple_regression")

        result_text = (
            f"Modelo: {target_label} ~ 6 fatores\n"
            f"R² = {r2:.4f}\n\n"
            f"Betas padronizados (maiores = mais peso):\n"
        )
        for i in sorted_idx:
            result_text += f"  {factor_labels[i]}: {betas[i]:.4f}\n"

        self._add_result(
            hypothesis_id=hid, verdict=verdict,
            technique="Multiple Regression (standardized betas)",
            statistic_name="R2",
            statistic_value=r2,
            effect_size_name="top_beta",
            effect_size_value=abs(top_beta),
            p_value=np.nan,
            p_corrected=np.nan,
            interpretation=interp,
        )

        self._add_report_section(
            hid, h["title"], h.get("headline", ""),
            technique=(
                "Regressao multipla com coeficientes padronizados (betas). "
                "Padronizar permite comparar o peso de cada fator na mesma "
                "escala — o maior beta e o fator que mais contribui."
            ),
            premises=(
                "Variaveis padronizadas (media 0, desvio 1). "
                "IMPORTANTE: os fatores sao medias de subconjuntos dos 37 itens, "
                "e o prazer geral e a media de todos os 37. Entao existe "
                "circularidade parcial — o R² alto nao e uma descoberta "
                "independente, mas os pesos relativos sao informativos."
            ),
            result_text=result_text,
            verdict=verdict,
            interpretation=interp,
            relevance=(
                f"O fator '{top_factor}' tem o maior peso. "
                f"Isso indica que, entre os 6 tipos de prazer, "
                f"este e o que mais 'puxa' a media geral pra cima ou pra baixo."
            ),
            limitations=(
                "Circularidade parcial: fatores sao parte da media geral. "
                "R² alto e esperado por construcao. "
                "O valor real esta nos pesos relativos, nao no R² absoluto."
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
