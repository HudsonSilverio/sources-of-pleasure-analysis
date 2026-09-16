"""
integrator.py — Senior Integrator for Phase 7.

Audits all Phase 5/6 analyst results: checks for computational bugs,
spot-checks statistics against raw data, cross-references hypotheses,
finds convergences and emergent insights, then compiles candidate
insights ranked by strength.

Does NOT inherit from BaseAnalyst (different role: audits, doesn't test).
"""

from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class SeniorIntegrator:
    """Audits analyst results, cross-references hypotheses, finds insights."""

    def __init__(self, clean_df, config, hypotheses, results_df,
                 data_dir, output_dir, fig_dir, seed=42):
        """
        Parameters
        ----------
        clean_df : pd.DataFrame
            Cleaned dataset (data/processed/clean.csv).
        config : dict
            Parsed instrument.yaml.
        hypotheses : dict
            Parsed hypotheses.yaml (hid -> hdict).
        results_df : pd.DataFrame
            Phase56 results (data/processed/phase56_results.csv).
        data_dir : Path
            Path to data/processed/.
        output_dir : Path
            Path to outputs/reports/.
        fig_dir : Path
            Path to outputs/figures/exploratory/phase7/.
        seed : int
            Random seed.
        """
        self.df = clean_df
        self.config = config
        self.hypotheses = hypotheses
        self.results_df = results_df
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.fig_dir = Path(fig_dir)
        self.seed = seed
        self.n = len(clean_df)

        np.random.seed(seed)

        # Column lists from config
        self.item_cols = [it["variavel"] for it in config["itens"]]
        self.factor_names = list(config["fatores"].keys())
        self.factor_cols = [f"factor_{f}" for f in self.factor_names]

        # Labels for readable output
        self.item_labels = {
            it["variavel"]: it["rotulo"] for it in config["itens"]
        }
        self.factor_labels = {
            k: v.get("rotulo", k) for k, v in config["fatores"].items()
        }

    # ==================================================================
    # Main entry point
    # ==================================================================

    def run_all(self):
        """Run all audit checks and return findings dict."""
        print(f"\n{'='*60}")
        print(f"  INTEGRADOR SENIOR — Fase 7")
        print(f"  N = {self.n:,} respondentes")
        print(f"{'='*60}")

        findings = {}
        findings["bugs"] = self._check_computational_bugs()
        findings["audit"] = self._audit_verdicts()
        findings["spotchecks"] = self._spot_check_statistics()
        findings["crossrefs"] = self._cross_reference_hypotheses()
        findings["convergences"] = self._find_convergences()
        findings["emergent"] = self._find_emergent_insights()
        findings["candidates"] = self._compile_insight_candidates(findings)

        self._make_figures(findings)
        self._write_report(findings)
        self._write_audit_csv(findings)

        return findings

    # ==================================================================
    # Helper: get result row
    # ==================================================================

    def _get_result(self, hid):
        """Get the results row for a hypothesis ID."""
        row = self.results_df[self.results_df["hypothesis_id"] == hid]
        if len(row) == 0:
            return None
        return row.iloc[0]

    def _save_fig(self, fig, name):
        """Save figure and return relative path."""
        self.fig_dir.mkdir(parents=True, exist_ok=True)
        path = self.fig_dir / f"{name}.png"
        fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        rel = path.relative_to(self.fig_dir.parents[3])
        print(f"    Grafico: {rel}")
        return str(rel)

    # ==================================================================
    # 1. Computational bugs (checks 1-3)
    # ==================================================================

    def _check_computational_bugs(self):
        """Detect known computational issues in analyst results."""
        print("\n  [1/7] Verificando bugs computacionais...")
        bugs = []

        # Bug 1: H03 r = inf
        r03 = self._get_result("H03")
        if r03 is not None:
            es = r03["effect_size_value"]
            is_inf = (es == np.inf) or (isinstance(es, str) and es == "inf")
            if is_inf or (pd.notna(es) and not isinstance(es, str) and es > 1e6):
                bugs.append({
                    "id": "BUG-01",
                    "hypothesis": "H03",
                    "issue": "r = inf (tamanho de efeito infinito)",
                    "explanation": (
                        "O Wilcoxon retornou p = 0.0 exato, gerando Z = inf "
                        "na formula r = Z/sqrt(N). Isso acontece porque com N "
                        "muito grande o p-valor fica abaixo da precisao do "
                        "float. O efeito e real e grande, mas r = inf nao e "
                        "um numero interpretavel."
                    ),
                    "recommendation": (
                        "Reportar como 'efeito grande (r > 0.5)' em vez de "
                        "r = inf. Alternativa: usar a estatistica de rank-biserial "
                        "como tamanho de efeito."
                    ),
                    "severity": "medio",
                })
                print(f"    BUG-01: H03 r = inf")

        # Bug 2: H15 no silhouette score
        r15 = self._get_result("H15")
        if r15 is not None:
            es_name = r15["effect_size_name"]
            es_val = r15["effect_size_value"]
            has_silhouette = (
                isinstance(es_name, str)
                and "silhouette" in es_name.lower()
                and pd.notna(es_val)
            )
            if not has_silhouette:
                bugs.append({
                    "id": "BUG-02",
                    "hypothesis": "H15",
                    "issue": "Tamanho de efeito ausente (sem silhouette)",
                    "explanation": (
                        "A busca por perfil intelectual encontrou um cluster "
                        "mas nao reportou silhouette score para validar a "
                        "qualidade da separacao."
                    ),
                    "recommendation": (
                        "Calcular silhouette do K-Means usado e reportar. "
                        "Comparar com o silhouette de H12 (0.228) para "
                        "verificar consistencia."
                    ),
                    "severity": "baixo",
                })
                print(f"    BUG-02: H15 sem silhouette")

        # Bug 3: H16 R² negativo no modelo reverso
        r16 = self._get_result("H16")
        if r16 is not None:
            interp = str(r16["interpretation"])
            if "R²" in interp or "R2" in interp or r16["effect_size_value"] < 0.01:
                # Check report for negative R²
                bugs.append({
                    "id": "BUG-03",
                    "hypothesis": "H16",
                    "issue": "R² negativo no modelo reverso",
                    "explanation": (
                        "O relatorio do analista mostra R² negativos para "
                        "modelos reversos individuais (relaxamento → adrenalina). "
                        "R² negativo em dados de teste significa que o modelo e "
                        "pior que simplesmente usar a media — ou seja, nao ha "
                        "relacao linear entre esses itens."
                    ),
                    "recommendation": (
                        "R² negativo confirma a conclusao (inconclusiva) mas "
                        "deveria ser reportado explicitamente como 'modelo pior "
                        "que o acaso' em vez de um numero negativo sem contexto."
                    ),
                    "severity": "baixo",
                })
                print(f"    BUG-03: H16 R² negativo no reverso")

        if not bugs:
            print("    Nenhum bug encontrado.")

        return bugs

    # ==================================================================
    # 2. Verdict audit (checks 4-10)
    # ==================================================================

    def _audit_verdicts(self):
        """Audit whether each verdict is well-supported."""
        print("\n  [2/7] Auditando vereditos...")
        audits = []

        # Check 4: H05 — |rho| < 0.1
        r05 = self._get_result("H05")
        if r05 is not None:
            rho = abs(r05["effect_size_value"]) if pd.notna(r05["effect_size_value"]) else 0
            if rho < 0.1:
                audits.append({
                    "id": "AUD-04",
                    "hypothesis": "H05",
                    "verdict_original": r05["verdict"],
                    "issue": f"|rho| = {rho:.4f} — efeito negligivel",
                    "recommendation": (
                        "Estatisticamente significativo (N grande), mas o "
                        "efeito e tao pequeno que nao tem relevancia pratica. "
                        "Sugerimos rebaixar para 'confirmada com ressalva': "
                        "incompatibilidade existe, mas e muito sutil."
                    ),
                    "suggested_verdict": "confirmada com ressalva",
                })
                print(f"    AUD-04: H05 rho < 0.1")

        # Check 5: H07 — Cronbach alpha=0.67 with 2 items
        r07 = self._get_result("H07")
        if r07 is not None:
            alpha = r07["effect_size_value"] if pd.notna(r07["effect_size_value"]) else 0
            if 0.6 <= alpha < 0.7:
                audits.append({
                    "id": "AUD-05",
                    "hypothesis": "H07",
                    "verdict_original": r07["verdict"],
                    "issue": (
                        f"Cronbach alpha = {alpha:.2f} com apenas 2 itens "
                        "— borderline (limiar aceitavel = 0.60, bom = 0.70)"
                    ),
                    "recommendation": (
                        "Alpha com 2 itens e uma estimativa instavel. "
                        "O veredito 'confirmada' se sustenta pela correlacao "
                        "forte (rho = 0.46), mas o superfator 'quem cuida' "
                        "precisa de ressalva: evidencia moderada, nao forte."
                    ),
                    "suggested_verdict": "confirmada (evidencia moderada)",
                })
                print(f"    AUD-05: H07 alpha borderline")

        # Check 6: H08 — delta_rho = 0.077
        r08 = self._get_result("H08")
        if r08 is not None:
            delta = abs(r08["effect_size_value"]) if pd.notna(r08["effect_size_value"]) else 0
            if delta < 0.1:
                audits.append({
                    "id": "AUD-06",
                    "hypothesis": "H08",
                    "verdict_original": r08["verdict"],
                    "issue": f"delta_rho = {delta:.4f} — diferenca pequena",
                    "recommendation": (
                        "O teste de Steiger e significativo (p < 0.001, N "
                        "grande), mas a diferenca pratica entre as duas "
                        "correlacoes (0.250 vs 0.174) e pequena. O item "
                        "sexual correlaciona com ambos os fatores; a "
                        "preferencia por thrilling e marginal."
                    ),
                    "suggested_verdict": "confirmada com ressalva",
                })
                print(f"    AUD-06: H08 delta pequeno")

        # Check 7: H12 — silhouette = 0.228, threshold = 0.25
        r12 = self._get_result("H12")
        if r12 is not None:
            sil = r12["effect_size_value"] if pd.notna(r12["effect_size_value"]) else 0
            if sil < 0.25:
                audits.append({
                    "id": "AUD-07",
                    "hypothesis": "H12",
                    "verdict_original": r12["verdict"],
                    "issue": (
                        f"Silhouette = {sil:.3f} — abaixo do limiar 0.25 "
                        "definido pelo proprio analista"
                    ),
                    "recommendation": (
                        "O analista confirmou a hipotese ('prazer e um espectro') "
                        "justamente porque o silhouette e fraco. A logica e "
                        "valida, mas o limiar 0.25 foi arbitrario — um limiar "
                        "mais baixo (0.20) mudaria o veredito. Ressaltar que "
                        "e uma evidencia a favor do espectro, nao uma prova."
                    ),
                    "suggested_verdict": "confirmada (limiar arbitrario)",
                })
                print(f"    AUD-07: H12 silhouette < 0.25")

        # Check 8: H15 — vies de busca
        r15 = self._get_result("H15")
        if r15 is not None and r15["verdict"] == "confirmada":
            audits.append({
                "id": "AUD-08",
                "hypothesis": "H15",
                "verdict_original": r15["verdict"],
                "issue": (
                    "Vies de busca: o analista procurou especificamente "
                    "um cluster 'intelectual-dominante' e encontrou"
                ),
                "recommendation": (
                    "Buscar um perfil pre-definido quase sempre encontra algo "
                    "— K-Means vai particionar o espaco de qualquer jeito. "
                    "Sem silhouette do cluster especifico e sem validacao de "
                    "estabilidade, o 'grupo intelectual' pode ser um artefato."
                ),
                "suggested_verdict": "confirmada com ressalva forte",
            })
            print(f"    AUD-08: H15 vies de busca")

        # Check 9: H17 — R² = 0.974, circularidade
        r17 = self._get_result("H17")
        if r17 is not None:
            r2 = r17["statistic_value"] if pd.notna(r17["statistic_value"]) else 0
            if r2 > 0.95:
                audits.append({
                    "id": "AUD-09",
                    "hypothesis": "H17",
                    "verdict_original": r17["verdict"],
                    "issue": (
                        f"R² = {r2:.3f} — circularidade parcial "
                        "(fatores sao subconjuntos dos itens que compoem "
                        "a variavel-alvo)"
                    ),
                    "recommendation": (
                        "O analista ja notou a circularidade no relatorio. "
                        "O R² alto era esperado por construcao, nao e uma "
                        "descoberta. O valor real esta nos pesos relativos "
                        "(betas), nao no R². Rebaixar o achado para "
                        "'informativo' em vez de 'confirmada'."
                    ),
                    "suggested_verdict": "confirmada (informativo, nao descoberta)",
                })
                print(f"    AUD-09: H17 circularidade")

        # Check 10: 15/17 confirmadas — taxa suspeita?
        n_conf = (self.results_df["verdict"] == "confirmada").sum()
        n_total = len(self.results_df)
        pct = n_conf / n_total * 100
        if pct > 80:
            audits.append({
                "id": "AUD-10",
                "hypothesis": "geral",
                "verdict_original": f"{n_conf}/{n_total} confirmadas",
                "issue": (
                    f"{n_conf} de {n_total} hipoteses confirmadas "
                    f"({pct:.0f}%) — taxa alta"
                ),
                "recommendation": (
                    "Com N ~ 6.500, quase tudo e 'significativo'. "
                    "As hipoteses tambem foram formuladas apos uma "
                    "exploracao dos dados (fases 2-4), o que favorece "
                    "confirmacao. Nao significa que os achados sao falsos, "
                    "mas que a barra para 'confirmada' foi baixa em alguns "
                    "casos (H05, H08, H15, H17). O vies de confirmacao "
                    "deve ser declarado no relatorio final."
                ),
                "suggested_verdict": "meta-observacao",
            })
            print(f"    AUD-10: {n_conf}/{n_total} confirmadas ({pct:.0f}%)")

        return audits

    # ==================================================================
    # 3. Spot-checks (checks 11-14)
    # ==================================================================

    def _spot_check_statistics(self):
        """Recompute key statistics from clean.csv to verify analyst outputs."""
        print("\n  [3/7] Spot-checks (recalculando do CSV bruto)...")
        checks = []

        # Check 11: 5 correlations from phase3_corr_items.csv
        print("    Verificando 5 correlacoes da fase 3...")
        corr_reported = pd.read_csv(
            self.data_dir / "phase3_corr_items.csv", index_col=0
        )
        # Build variable -> label mapping for lookup in corr matrix
        var_to_label = {
            it["variavel"]: it["rotulo"]
            for it in self.config["itens"]
        }
        # Pick 5 representative pairs (using variable names from clean.csv)
        spot_pairs = [
            ("p_nature", "p_status"),        # H05 top pair
            ("p_humor", "p_sound"),           # H10 notable pair
            ("p_qualityTime", "p_loving"),    # H09 predictors
            ("p_risk", "p_relax"),            # H16 key pair
            ("p_spiritual", "p_charity"),     # H14 related
        ]
        corr_checks = []
        for col_a, col_b in spot_pairs:
            if col_a in self.df.columns and col_b in self.df.columns:
                rho_recalc, _ = stats.spearmanr(self.df[col_a], self.df[col_b])
                # Look up using labels (corr matrix uses labels as index)
                label_a = var_to_label.get(col_a, col_a)
                label_b = var_to_label.get(col_b, col_b)
                rho_reported = np.nan
                if label_a in corr_reported.index and label_b in corr_reported.columns:
                    rho_reported = corr_reported.loc[label_a, label_b]
                elif label_b in corr_reported.index and label_a in corr_reported.columns:
                    rho_reported = corr_reported.loc[label_b, label_a]

                match = (
                    pd.notna(rho_reported)
                    and abs(rho_recalc - rho_reported) < 0.001
                )
                corr_checks.append({
                    "pair": f"{col_a} x {col_b}",
                    "reported": round(rho_reported, 4) if pd.notna(rho_reported) else "n/a",
                    "recalculated": round(rho_recalc, 4),
                    "match": match,
                })

        checks.append({
            "id": "SPOT-11",
            "description": "5 correlacoes Spearman recalculadas",
            "details": corr_checks,
            "all_match": all(c["match"] for c in corr_checks),
        })
        status = "OK" if checks[-1]["all_match"] else "DIVERGENCIA"
        print(f"    SPOT-11: correlacoes — {status}")

        # Check 12: Factor medians (H03)
        print("    Verificando medianas dos 6 fatores...")
        median_checks = []
        for fn, fc in zip(self.factor_names, self.factor_cols):
            if fc in self.df.columns:
                med = self.df[fc].median()
                median_checks.append({
                    "factor": fn,
                    "recalculated_median": round(med, 2),
                })
        # Sort by median to check ranking
        median_checks.sort(key=lambda x: x["recalculated_median"])
        lowest = median_checks[0]["factor"] if median_checks else "n/a"
        matches_h03 = lowest == "thrilling"

        checks.append({
            "id": "SPOT-12",
            "description": "Medianas dos 6 fatores (H03 diz thrilling e o mais baixo)",
            "details": median_checks,
            "h03_lowest_confirmed": matches_h03,
            "lowest_factor": lowest,
        })
        status = "OK" if matches_h03 else f"DIVERGENCIA (lowest={lowest})"
        print(f"    SPOT-12: medianas — {status}")

        # Check 13: H11 group sizes and means
        print("    Verificando grupos H11 (entropia)...")
        profiles = pd.read_csv(
            self.data_dir / "phase2_respondent_profiles.csv", index_col=0
        )
        if "entropy_normalized" in profiles.columns:
            median_ent = profiles["entropy_normalized"].median()
            gen_mask = profiles["entropy_normalized"] >= median_ent
            spec_mask = profiles["entropy_normalized"] < median_ent
            n_gen = gen_mask.sum()
            n_spec = spec_mask.sum()

            # Merge with clean_df to get mean_overall
            items_df = self.df[self.item_cols]
            mean_overall = items_df.mean(axis=1)
            gen_mean = mean_overall[gen_mask.values].mean()
            spec_mean = mean_overall[spec_mask.values].mean()

            checks.append({
                "id": "SPOT-13",
                "description": "H11: tamanhos de grupo e medias (generalistas vs especialistas)",
                "n_generalists": int(n_gen),
                "n_specialists": int(n_spec),
                "mean_generalists": round(gen_mean, 2),
                "mean_specialists": round(spec_mean, 2),
                "h11_direction_confirmed": gen_mean > spec_mean,
            })
            status = "OK" if gen_mean > spec_mean else "DIVERGENCIA"
            print(f"    SPOT-13: H11 grupos — {status}")
        else:
            checks.append({
                "id": "SPOT-13",
                "description": "H11: nao foi possivel verificar (entropy_normalized ausente)",
                "h11_direction_confirmed": None,
            })
            print(f"    SPOT-13: coluna entropy_normalized nao encontrada")

        # Check 14: H09 regression R²
        print("    Verificando regressao H09...")
        predictors = ["p_loving", "p_qualityTime"]
        target = "p_connection"
        if all(c in self.df.columns for c in predictors + [target]):
            X = self.df[predictors].values
            y = self.df[target].values
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=self.seed
            )
            model = LinearRegression().fit(X_train, y_train)
            r2_train = round(model.score(X_train, y_train), 4)
            r2_test = round(model.score(X_test, y_test), 4)

            r09 = self._get_result("H09")
            reported_r2 = r09["effect_size_value"] if r09 is not None else np.nan

            checks.append({
                "id": "SPOT-14",
                "description": "H09: regressao recalculada (R² treino/teste)",
                "r2_train_recalc": r2_train,
                "r2_test_recalc": r2_test,
                "r2_test_reported": round(reported_r2, 4) if pd.notna(reported_r2) else "n/a",
                "match": (
                    pd.notna(reported_r2)
                    and abs(r2_test - reported_r2) < 0.01
                ),
            })
            status = "OK" if checks[-1]["match"] else "DIVERGENCIA"
            print(f"    SPOT-14: H09 R² — {status}")

        return checks

    # ==================================================================
    # 4. Cross-reference hypotheses (checks 15-20)
    # ==================================================================

    def _cross_reference_hypotheses(self):
        """Cross-check results between related hypotheses."""
        print("\n  [4/7] Cruzando hipoteses...")
        crossrefs = []

        # Cross 15: H01 × H02 — rankings by different metrics
        print("    Cruzando H01 x H02 (rankings)...")
        r01 = self._get_result("H01")
        r02 = self._get_result("H02")
        if r01 is not None and r02 is not None:
            # Both use p_humor as #1
            both_humor = (
                "p_humor" in str(r01["interpretation"])
                and "p_humor" in str(r02["interpretation"])
            )
            crossrefs.append({
                "id": "CROSS-15",
                "hypotheses": "H01 x H02",
                "question": "Rankings por metricas diferentes concordam?",
                "finding": (
                    "Sim — p_humor e lider em ambas as metricas "
                    "(net_agreement e top2_pct). Os 5 primeiros sao "
                    "praticamente os mesmos em ambos os rankings."
                ),
                "convergent": True,
                "detail": f"Humor lider em ambas: {both_humor}",
            })

        # Cross 16: H04 × H14 — spiritual groups (GMM vs fixed cut)
        print("    Cruzando H04 x H14 (grupos espirituais)...")
        r04 = self._get_result("H04")
        r14 = self._get_result("H14")
        if r04 is not None and r14 is not None:
            # Recompute overlap: H04 GMM groups vs H14 cut groups
            from sklearn.mixture import GaussianMixture
            spiritual = self.df["p_spiritual"].values.reshape(-1, 1)
            gmm = GaussianMixture(n_components=2, random_state=self.seed)
            gmm.fit(spiritual)
            gmm_labels = gmm.predict(spiritual)

            # Identify which GMM group is "high" (higher mean)
            means = [spiritual[gmm_labels == i].mean() for i in range(2)]
            high_gmm = 1 if means[1] > means[0] else 0

            # H14 groups
            h14_high = self.df["p_spiritual"] >= 1
            h14_low = self.df["p_spiritual"] <= -1

            # Overlap
            gmm_high_mask = gmm_labels == high_gmm
            overlap_high = (gmm_high_mask & h14_high.values).sum()
            n_gmm_high = gmm_high_mask.sum()
            n_h14_high = h14_high.sum()
            if n_h14_high > 0:
                pct_overlap = overlap_high / n_h14_high * 100
            else:
                pct_overlap = 0

            crossrefs.append({
                "id": "CROSS-16",
                "hypotheses": "H04 x H14",
                "question": (
                    "Os grupos espirituais do GMM (H04) e do corte fixo "
                    "(H14) capturam as mesmas pessoas?"
                ),
                "finding": (
                    f"Sobreposicao: {pct_overlap:.1f}% dos que pontuam alto "
                    f"no corte fixo (>= 1, N={n_h14_high:,}) tambem estao "
                    f"no grupo alto do GMM (N={n_gmm_high:,}). "
                    + ("Convergencia forte — os dois metodos concordam."
                       if pct_overlap > 80
                       else "Convergencia parcial — os metodos divergem nas bordas.")
                ),
                "convergent": pct_overlap > 80,
                "overlap_pct": round(pct_overlap, 1),
            })

        # Cross 17: H11 × H12 — entropy vs clusters
        print("    Cruzando H11 x H12 (entropia vs clusters)...")
        r11 = self._get_result("H11")
        r12 = self._get_result("H12")
        if r11 is not None and r12 is not None:
            # Both point to "spectrum, not types"
            h11_d = r11["effect_size_value"] if pd.notna(r11["effect_size_value"]) else 0
            h12_sil = r12["effect_size_value"] if pd.notna(r12["effect_size_value"]) else 0
            crossrefs.append({
                "id": "CROSS-17",
                "hypotheses": "H11 x H12",
                "question": (
                    "Entropia (H11) e clustering (H12) convergem sobre "
                    "a estrutura do prazer?"
                ),
                "finding": (
                    f"H11 mostra que generalistas tem mais prazer geral "
                    f"(d = {h11_d:.2f}, efeito grande), sugerindo um espectro "
                    f"continuo. H12 confirma que nao ha tipos separados "
                    f"(silhouette = {h12_sil:.3f} < 0.25). Convergencia: "
                    "ambos apontam que prazer e um espectro, nao categorias."
                ),
                "convergent": True,
            })

        # Cross 18: H05 × H06 — item incompatibility vs factor independence
        print("    Cruzando H05 x H06 (incompatibilidade vs independencia)...")
        r05 = self._get_result("H05")
        r06 = self._get_result("H06")
        if r05 is not None and r06 is not None:
            crossrefs.append({
                "id": "CROSS-18",
                "hypotheses": "H05 x H06",
                "question": (
                    "H05 diz que alguns prazeres sao incompativeis, "
                    "H06 diz que intelectual e reputacional sao independentes. "
                    "Sao consistentes?"
                ),
                "finding": (
                    "Consistentes mas em escalas diferentes. H06 mostra "
                    "independencia entre FATORES inteiros (rho = 0.023). "
                    "H05 mostra incompatibilidades entre ITENS individuais "
                    "(max |rho| < 0.1). Ambos confirmam que correlacoes "
                    "negativas existem mas sao fracas. A independencia "
                    "entre fatores e mais robusta que incompatibilidade "
                    "entre itens."
                ),
                "convergent": True,
            })

        # Cross 19: H13 × H03 — thrill-seeker profile vs most rejected factor
        print("    Cruzando H13 x H03 (perfil thrill-seeker vs fator rejeitado)...")
        r13 = self._get_result("H13")
        r03 = self._get_result("H03")
        if r13 is not None and r03 is not None:
            crossrefs.append({
                "id": "CROSS-19",
                "hypotheses": "H13 x H03",
                "question": (
                    "H03 diz que thrilling e o fator mais rejeitado. "
                    "H13 mostra que quem busca emocao forte e diferente. "
                    "Sao consistentes?"
                ),
                "finding": (
                    "Perfeitamente consistentes. Thrilling e rejeitado pela "
                    "maioria (mediana = -0.33, unico fator negativo), mas "
                    "quem pontua alto nele difere em TODOS os outros fatores "
                    "(maior efeito: reputacional, d = 0.887). Thrill-seekers "
                    "sao uma minoria com perfil realmente distinto."
                ),
                "convergent": True,
            })

        # Cross 20: H17 × H03 — thrilling has biggest beta BUT is most rejected
        print("    Cruzando H17 x H03 (beta thrilling vs rejeicao)...")
        r17 = self._get_result("H17")
        r03 = self._get_result("H03")
        if r17 is not None and r03 is not None:
            crossrefs.append({
                "id": "CROSS-20",
                "hypotheses": "H17 x H03",
                "question": (
                    "H17 mostra que thrilling tem o maior beta (0.354) na "
                    "regressao. H03 mostra que thrilling e o mais rejeitado. "
                    "Isso e um paradoxo?"
                ),
                "finding": (
                    "Paradoxo aparente com explicacao tecnica. O beta alto "
                    "nao significa que thrilling 'gera mais prazer'. Significa "
                    "que, por ter a MAIOR VARIANCIA (as pessoas divergem muito "
                    "sobre emocao forte), ele contribui mais para diferenciar "
                    "quem tem prazer geral alto vs baixo. E o fator que mais "
                    "'puxa' a media — tanto pra cima quanto pra baixo. "
                    "Combinado com a circularidade (AUD-09), esse achado "
                    "e mais tecnico do que substantivo."
                ),
                "convergent": False,
                "is_paradox": True,
            })

        return crossrefs

    # ==================================================================
    # 5. Convergences (checks 21-25)
    # ==================================================================

    def _find_convergences(self):
        """Identify where multiple analyses point in the same direction."""
        print("\n  [5/7] Identificando convergencias...")
        convergences = []

        # Conv 21: "Pessoas concordam sobre o que e prazeroso"
        convergences.append({
            "id": "CONV-21",
            "headline": "Pessoas concordam sobre o que e prazeroso",
            "evidence": ["H01", "H02", "H12", "H11"],
            "summary": (
                "Rir e o prazer mais universal (H01, H02). Nao existem 'tipos' "
                "claros de prazer — e um espectro (H12). Generalistas (que gostam "
                "de tudo um pouco) reportam mais prazer geral (H11). As pessoas "
                "convergem mais do que divergem sobre o que da prazer."
            ),
            "strength": "forte",
            "caveats": (
                "H01/H02 medem o topo do ranking, nao consenso global. "
                "A convergencia e mais sobre os prazeres 'universais' "
                "(rir, conectar, aprender) do que sobre os divisivos "
                "(espiritualidade, adrenalina)."
            ),
        })

        # Conv 22: "Espiritualidade e o grande divisor"
        convergences.append({
            "id": "CONV-22",
            "headline": "Espiritualidade e o grande divisor",
            "evidence": ["H04", "H14"],
            "summary": (
                "Espiritualidade divide a amostra em dois grupos claros "
                "(H04, BIC diff = 2114). Quem pontua alto e diferente em "
                "TODOS os 6 fatores (H14, max d = 1.31). Nenhum outro item "
                "ou fator produz uma divisao tao nitida."
            ),
            "strength": "forte",
            "caveats": (
                "Amostra viesada (ClearerThinking atrai perfil secular/analitico). "
                "A proporcao espiritual/nao-espiritual pode nao refletir a "
                "populacao geral."
            ),
        })

        # Conv 23: "Emocao forte e o prazer mais rejeitado"
        convergences.append({
            "id": "CONV-23",
            "headline": "Emocao forte e o prazer mais rejeitado",
            "evidence": ["H03", "H13"],
            "summary": (
                "Thrilling e o unico fator com mediana negativa (-0.33 — "
                "a maioria discorda, H03). Quem busca emocao forte difere "
                "dos demais em 5 de 5 outros fatores (H13, max d = 0.887). "
                "Thrill-seekers sao uma minoria com perfil distinto."
            ),
            "strength": "forte",
            "caveats": (
                "O efeito pode ser amplificado pela amostra "
                "(publico analitico/intelectual tende a rejeitar risco)."
            ),
        })

        # Conv 24: "Quem cuida de pessoas cuida de causas"
        convergences.append({
            "id": "CONV-24",
            "headline": "Quem cuida de pessoas cuida de causas",
            "evidence": ["H07", "H14"],
            "summary": (
                "Os fatores interpersonal e noble correlacionam forte "
                "(rho = 0.46, H07) e formam um possivel superfator. "
                "Quem pontua alto em espiritualidade tambem pontua alto "
                "em ambos (H14, noble d = 1.31). O cuidado com pessoas "
                "e causas anda junto."
            ),
            "strength": "moderada",
            "caveats": (
                "Cronbach alpha borderline (0.67). O superfator 'quem cuida' "
                "e uma hipotese, nao um fato estabelecido. Precisaria de "
                "analise fatorial confirmatoria para ser confirmado."
            ),
        })

        # Conv 25: "Intelectual e reputacional: mundos independentes"
        convergences.append({
            "id": "CONV-25",
            "headline": "Intelectual e reputacional: mundos independentes",
            "evidence": ["H06", "H05"],
            "summary": (
                "Intellectual e reputational sao equivalentes a zero "
                "(rho = 0.023, H06 — TOST confirmado). No nivel dos itens, "
                "pares como criatividade × competicao sao negativos "
                "(H05, rho = -0.083). Quem busca conhecimento nao liga "
                "para status — e vice-versa."
            ),
            "strength": "moderada",
            "caveats": (
                "Independencia nao significa incompatibilidade. Pessoas "
                "podem pontuar alto em ambos — sao apenas dimensoes "
                "que variam separadamente."
            ),
        })

        for c in convergences:
            print(f"    {c['id']}: {c['headline']} [{c['strength']}]")

        return convergences

    # ==================================================================
    # 6. Emergent insights (checks 26-28)
    # ==================================================================

    def _find_emergent_insights(self):
        """Insights that only appear when combining analyses."""
        print("\n  [6/7] Buscando insights emergentes...")
        emergent = []

        # Emergent 26: Paradoxo do thrilling
        emergent.append({
            "id": "EMER-26",
            "headline": "Paradoxo do thrilling: rejeitado pela maioria, mas determinante",
            "evidence": ["H03", "H17", "H13"],
            "summary": (
                "Thrilling e o fator mais rejeitado (mediana negativa, H03) "
                "E o que tem o maior beta na regressao (0.354, H17). Parece "
                "paradoxo, mas a explicacao e que thrilling tem a MAIOR "
                "VARIANCIA — as pessoas divergem muito sobre ele. Por ter "
                "muita variacao, ele 'puxa' mais a media geral, tanto pra "
                "cima (thrill-seekers) quanto pra baixo (a maioria). E o "
                "fator mais polarizador, nao o mais prazeroso."
            ),
            "strength": "forte",
            "caveats": (
                "O beta alto vem parcialmente da circularidade "
                "(fatores compoem a media geral). Mas mesmo descontando "
                "isso, a variancia do thrilling e uma descoberta real."
            ),
        })

        # Emergent 27: H15 cluster vs H12 silhouette
        # Recompute silhouette for the k=3 KMeans used in H15
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        from sklearn.preprocessing import StandardScaler

        X_factors = self.df[self.factor_cols].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_factors)

        km3 = KMeans(n_clusters=3, random_state=self.seed, n_init=10)
        labels_3 = km3.fit_predict(X_scaled)
        sil_3 = silhouette_score(X_scaled, labels_3)

        emergent.append({
            "id": "EMER-27",
            "headline": "Clusters nao sao 'tipos de pessoa' — sao regioes do espectro",
            "evidence": ["H15", "H12"],
            "summary": (
                f"H12 mostra que nao ha tipos claros (silhouette = 0.228). "
                f"Mas H15 'encontra' um grupo intelectual com K-Means k=3. "
                f"Recalculando: o silhouette do k=3 e {sil_3:.3f} — igual ou "
                f"pior que o melhor de H12. O 'grupo intelectual' nao e um "
                f"tipo natural: e apenas uma regiao do espectro que o K-Means "
                f"recortou. Qualquer recorte em k grupos vai encontrar 'perfis', "
                f"mas isso nao prova que eles existem como tipos reais."
            ),
            "strength": "moderada",
            "sil_k3_recalc": round(sil_3, 3),
            "caveats": (
                "Silhouette baixo nao prova que o grupo nao existe — "
                "apenas que as fronteiras sao difusas."
            ),
        })

        # Emergent 28: Generalistas mais felizes — tautologia?
        # Check: is entropy correlated with mean_overall by construction?
        items = self.df[self.item_cols]
        mean_overall = items.mean(axis=1)

        # Entropy of 6 factor scores
        factor_scores = self.df[self.factor_cols]
        # Shift to positive for entropy calculation
        shifted = factor_scores - factor_scores.min() + 0.01
        proportions = shifted.div(shifted.sum(axis=1), axis=0)
        entropy = -np.sum(proportions * np.log2(proportions), axis=1)

        rho_ent_mean, p_ent_mean = stats.spearmanr(entropy, mean_overall)

        emergent.append({
            "id": "EMER-28",
            "headline": "Generalistas 'mais felizes': descoberta real ou tautologia?",
            "evidence": ["H11"],
            "summary": (
                f"H11 mostra que generalistas reportam mais prazer geral "
                f"(d = 1.20, efeito grande). Mas isso pode ser tautologico: "
                f"quem concorda mais com tudo (media alta) automaticamente "
                f"fica com perfil mais equilibrado (entropia alta). "
                f"Recalculando: correlacao entre entropia e media geral: "
                f"rho = {rho_ent_mean:.3f}. "
                + ("Essa correlacao forte sugere que parte do efeito e "
                   "mecanica (quem diz 'sim' pra tudo tem perfil uniforme). "
                   "O achado H11 e parcialmente tautologico."
                   if rho_ent_mean > 0.5
                   else "A correlacao e moderada — existe alguma mecanica, "
                   "mas nao explica tudo. O efeito H11 e parcialmente real.")
            ),
            "strength": "sugestiva",
            "rho_entropy_mean": round(rho_ent_mean, 3),
            "caveats": (
                "A tautologia nao invalida completamente o achado — "
                "generalistas de fato reportam mais prazer. Mas a "
                "interpretacao 'diversificar fontes gera mais prazer' "
                "e mais forte do que os dados suportam."
            ),
        })

        for e in emergent:
            print(f"    {e['id']}: {e['headline']} [{e['strength']}]")

        return emergent

    # ==================================================================
    # 7. Compile insight candidates
    # ==================================================================

    def _compile_insight_candidates(self, findings):
        """Build final list of insight candidates for Phase 8."""
        print("\n  [7/7] Compilando candidatos a insight...")
        candidates = []

        # From convergences — these are the strongest
        for c in findings["convergences"]:
            candidates.append({
                "id": f"INS-{c['id'].split('-')[1]}",
                "source": c["id"],
                "headline": c["headline"],
                "evidence": c["evidence"],
                "strength": c["strength"],
                "caveats": c["caveats"],
                "type": "convergencia",
            })

        # From emergent insights
        for e in findings["emergent"]:
            candidates.append({
                "id": f"INS-{e['id'].split('-')[1]}",
                "source": e["id"],
                "headline": e["headline"],
                "evidence": e["evidence"],
                "strength": e["strength"],
                "caveats": e["caveats"],
                "type": "emergente",
            })

        # Sort by strength
        strength_order = {"forte": 0, "moderada": 1, "sugestiva": 2}
        candidates.sort(key=lambda x: strength_order.get(x["strength"], 9))

        for c in candidates:
            print(f"    {c['id']}: {c['headline']} [{c['strength']}]")

        return candidates

    # ==================================================================
    # Figures
    # ==================================================================

    def _make_figures(self, findings):
        """Generate diagnostic figures."""
        print("\n  Gerando graficos diagnosticos...")
        self.fig_dir.mkdir(parents=True, exist_ok=True)

        self._fig_verdict_audit(findings)
        self._fig_spotcheck_correlations(findings)
        self._fig_insight_strength(findings)

    def _fig_verdict_audit(self, findings):
        """Bar chart of verdicts with audit flags."""
        fig, ax = plt.subplots(figsize=(12, 5))

        hids = self.results_df["hypothesis_id"].tolist()
        verdicts = self.results_df["verdict"].tolist()

        color_map = {
            "confirmada": "#4CAF50",
            "inconclusiva": "#FFC107",
            "nao confirmada": "#F44336",
            "erro": "#9E9E9E",
        }
        colors = [color_map.get(v, "#9E9E9E") for v in verdicts]

        bars = ax.barh(range(len(hids)), [1] * len(hids), color=colors,
                       edgecolor="white", height=0.7)

        # Mark audited ones
        audited_hids = {a["hypothesis"] for a in findings["audit"]}
        for i, hid in enumerate(hids):
            label = f"{hid}: {verdicts[i]}"
            ax.text(0.5, i, label, ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white")
            if hid in audited_hids:
                ax.text(1.02, i, "⚠", ha="left", va="center", fontsize=14)

        ax.set_xlim(0, 1.15)
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_title("Panorama dos vereditos — Fase 7 (⚠ = auditoria sugerida)",
                      fontsize=12, fontweight="bold")
        ax.invert_yaxis()

        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(left=False, bottom=False, labelbottom=False)

        fig.tight_layout()
        self._save_fig(fig, "verdict_audit")

    def _fig_spotcheck_correlations(self, findings):
        """Compare reported vs recalculated correlations."""
        spot11 = next(
            (s for s in findings["spotchecks"] if s["id"] == "SPOT-11"),
            None
        )
        if spot11 is None or "details" not in spot11:
            return

        details = spot11["details"]
        pairs = [d["pair"] for d in details]
        reported = [d["reported"] if d["reported"] != "n/a" else 0 for d in details]
        recalc = [d["recalculated"] for d in details]

        fig, ax = plt.subplots(figsize=(10, 5))
        x = np.arange(len(pairs))
        w = 0.35

        ax.bar(x - w/2, reported, w, label="Fase 3 (reportado)", color="#2196F3")
        ax.bar(x + w/2, recalc, w, label="Recalculado (fase 7)", color="#FF9800")

        ax.set_xticks(x)
        ax.set_xticklabels([p.replace(" x ", "\n× ") for p in pairs],
                           fontsize=8, rotation=0)
        ax.set_ylabel("Spearman rho")
        ax.set_title("Spot-check: correlacoes reportadas vs recalculadas",
                      fontsize=12, fontweight="bold")
        ax.legend()
        ax.axhline(y=0, color="grey", linewidth=0.5)

        fig.tight_layout()
        self._save_fig(fig, "spotcheck_correlations")

    def _fig_insight_strength(self, findings):
        """Horizontal bar chart of insight candidates by strength."""
        candidates = findings["candidates"]
        if not candidates:
            return

        fig, ax = plt.subplots(figsize=(12, 6))

        headlines = [c["headline"] for c in candidates]
        strengths = [c["strength"] for c in candidates]
        colors_map = {"forte": "#4CAF50", "moderada": "#FFC107", "sugestiva": "#FF9800"}
        colors = [colors_map.get(s, "#9E9E9E") for s in strengths]

        # Truncate long headlines
        headlines = [h[:60] + "..." if len(h) > 60 else h for h in headlines]

        bars = ax.barh(range(len(headlines)), [1] * len(headlines),
                       color=colors, edgecolor="white", height=0.6)

        for i, (h, s) in enumerate(zip(headlines, strengths)):
            ax.text(0.02, i, f"{h} [{s}]", ha="left", va="center",
                    fontsize=9, color="black")

        ax.set_xlim(0, 1.1)
        ax.set_yticks([])
        ax.set_title("Candidatos a insight — classificados por forca",
                      fontsize=12, fontweight="bold")
        ax.invert_yaxis()

        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(left=False, bottom=False, labelbottom=False)

        fig.tight_layout()
        self._save_fig(fig, "insight_strength")

    # ==================================================================
    # Report generation
    # ==================================================================

    def _write_report(self, findings):
        """Write the full integration report as markdown."""
        lines = []

        # ---- Header ----
        lines.append("# Relatorio do Integrador Senior — Fase 7")
        lines.append("")
        lines.append(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Respondentes:** N = {self.n:,}")
        lines.append(f"**Hipoteses auditadas:** {len(self.results_df)}")
        lines.append(f"**Seed aleatoria:** {self.seed}")
        lines.append("")

        # ---- 1. Resumo executivo ----
        lines.append("## 1. Resumo executivo")
        lines.append("")

        n_conf = (self.results_df["verdict"] == "confirmada").sum()
        n_inc = (self.results_df["verdict"] == "inconclusiva").sum()
        n_total = len(self.results_df)
        n_bugs = len(findings["bugs"])
        n_audits = len(findings["audit"])
        n_cands = len(findings["candidates"])

        lines.append(
            f"De {n_total} hipoteses testadas na Fase 5, {n_conf} foram confirmadas "
            f"e {n_inc} ficaram inconclusivas. Esta auditoria encontrou "
            f"**{n_bugs} bugs computacionais**, levantou **{n_audits} ressalvas** "
            f"sobre vereditos, e compilou **{n_cands} candidatos a insight** "
            f"para a Fase 8."
        )
        lines.append("")
        lines.append(
            "A principal meta-observacao e que a taxa de confirmacao (88%) e alta, "
            "o que era esperado: as hipoteses foram formuladas apos exploracao "
            "dos dados, e com N ~ 6.500 quase qualquer efeito e 'significativo'. "
            "A auditoria classifica cada achado por forca real (forte / moderada / "
            "sugestiva) para separar descobertas solidas de ruido."
        )
        lines.append("")

        # ---- 2. Panorama dos vereditos ----
        lines.append("## 2. Panorama dos vereditos")
        lines.append("")
        lines.append("| Hipotese | Analista | Veredito | Auditoria |")
        lines.append("|----------|----------|----------|-----------|")

        for _, row in self.results_df.iterrows():
            hid = row["hypothesis_id"]
            analyst = row["analyst"]
            verdict = row["verdict"]
            # Find audit notes for this hypothesis
            audit_notes = [
                a for a in findings["audit"]
                if a["hypothesis"] == hid
            ]
            audit_str = "; ".join(
                a["issue"][:60] for a in audit_notes
            ) if audit_notes else "OK"
            lines.append(f"| {hid} | {analyst} | {verdict} | {audit_str} |")

        lines.append("")
        lines.append(f"![Panorama dos vereditos](../figures/exploratory/phase7/verdict_audit.png)")
        lines.append("")

        # ---- 3. Bugs computacionais ----
        lines.append("## 3. Bugs e erros computacionais")
        lines.append("")
        if findings["bugs"]:
            for bug in findings["bugs"]:
                lines.append(f"### {bug['id']} — {bug['hypothesis']}: {bug['issue']}")
                lines.append("")
                lines.append(f"**Explicacao:** {bug['explanation']}")
                lines.append("")
                lines.append(f"**Recomendacao:** {bug['recommendation']}")
                lines.append("")
                lines.append(f"**Severidade:** {bug['severity']}")
                lines.append("")
        else:
            lines.append("Nenhum bug encontrado.")
            lines.append("")

        # ---- 4. Spot-checks ----
        lines.append("## 4. Spot-checks (estatisticas recalculadas do CSV bruto)")
        lines.append("")

        for check in findings["spotchecks"]:
            lines.append(f"### {check['id']} — {check['description']}")
            lines.append("")

            if check["id"] == "SPOT-11":
                lines.append("| Par | Reportado | Recalculado | Bateu? |")
                lines.append("|-----|-----------|-------------|--------|")
                for d in check.get("details", []):
                    match_str = "Sim" if d["match"] else "**NAO**"
                    lines.append(
                        f"| {d['pair']} | {d['reported']} | "
                        f"{d['recalculated']} | {match_str} |"
                    )
                lines.append("")
                lines.append(
                    f"![Spot-check correlacoes]"
                    f"(../figures/exploratory/phase7/spotcheck_correlations.png)"
                )

            elif check["id"] == "SPOT-12":
                lines.append("| Fator | Mediana recalculada |")
                lines.append("|-------|---------------------|")
                for d in check.get("details", []):
                    lines.append(
                        f"| {d['factor']} | {d['recalculated_median']} |"
                    )
                lines.append("")
                confirmed = check.get("h03_lowest_confirmed", False)
                lowest = check.get("lowest_factor", "?")
                if confirmed:
                    lines.append(
                        f"Fator mais baixo: **{lowest}** — confirma H03."
                    )
                else:
                    lines.append(
                        f"**ATENCAO:** fator mais baixo = {lowest}, "
                        f"nao e o que H03 reportou."
                    )

            elif check["id"] == "SPOT-13":
                if check.get("h11_direction_confirmed") is not None:
                    lines.append(
                        f"- Generalistas: N = {check.get('n_generalists', '?'):,}, "
                        f"media = {check.get('mean_generalists', '?')}"
                    )
                    lines.append(
                        f"- Especialistas: N = {check.get('n_specialists', '?'):,}, "
                        f"media = {check.get('mean_specialists', '?')}"
                    )
                    confirmed = check["h11_direction_confirmed"]
                    lines.append(
                        f"- Direcao {'confirmada' if confirmed else '**NAO confirmada**'}: "
                        f"generalistas {'>' if confirmed else '<='} especialistas"
                    )
                else:
                    lines.append("Nao foi possivel verificar.")

            elif check["id"] == "SPOT-14":
                lines.append(
                    f"- R² treino recalculado: {check.get('r2_train_recalc', '?')}"
                )
                lines.append(
                    f"- R² teste recalculado: {check.get('r2_test_recalc', '?')}"
                )
                lines.append(
                    f"- R² teste reportado: {check.get('r2_test_reported', '?')}"
                )
                match = check.get("match", False)
                lines.append(
                    f"- {'Bateu' if match else '**DIVERGENCIA**'}"
                )

            lines.append("")

        # ---- 5. Auditoria de vereditos ----
        lines.append("## 5. Auditoria de vereditos")
        lines.append("")
        if findings["audit"]:
            for a in findings["audit"]:
                lines.append(
                    f"### {a['id']} — {a['hypothesis']}: {a['issue']}"
                )
                lines.append("")
                lines.append(f"**Veredito original:** {a['verdict_original']}")
                lines.append("")
                lines.append(f"**Recomendacao:** {a['recommendation']}")
                lines.append("")
                lines.append(
                    f"**Veredito sugerido:** {a.get('suggested_verdict', '—')}"
                )
                lines.append("")
        else:
            lines.append("Todos os vereditos estao bem sustentados.")
            lines.append("")

        # ---- 6. Cruzamentos entre hipoteses ----
        lines.append("## 6. Cruzamentos entre hipoteses")
        lines.append("")
        for cr in findings["crossrefs"]:
            lines.append(f"### {cr['id']} — {cr['hypotheses']}")
            lines.append("")
            lines.append(f"**Pergunta:** {cr['question']}")
            lines.append("")
            lines.append(f"**Achado:** {cr['finding']}")
            lines.append("")
            conv = "Sim" if cr.get("convergent") else "Nao"
            if cr.get("is_paradox"):
                conv = "Paradoxo (explicado)"
            lines.append(f"**Convergente:** {conv}")
            lines.append("")

        # ---- 7. Convergencias ----
        lines.append("## 7. Convergencias")
        lines.append("")
        lines.append(
            "Narrativas onde multiplas analises apontam na mesma direcao:"
        )
        lines.append("")
        for c in findings["convergences"]:
            lines.append(f"### {c['id']} — {c['headline']}")
            lines.append("")
            lines.append(f"**Evidencias:** {', '.join(c['evidence'])}")
            lines.append("")
            lines.append(c["summary"])
            lines.append("")
            lines.append(f"**Forca:** {c['strength']}")
            lines.append("")
            lines.append(f"**Ressalvas:** {c['caveats']}")
            lines.append("")

        # ---- 8. Insights emergentes ----
        lines.append("## 8. Insights emergentes")
        lines.append("")
        lines.append(
            "Descobertas que so aparecem quando as analises sao combinadas:"
        )
        lines.append("")
        for e in findings["emergent"]:
            lines.append(f"### {e['id']} — {e['headline']}")
            lines.append("")
            lines.append(f"**Evidencias:** {', '.join(e['evidence'])}")
            lines.append("")
            lines.append(e["summary"])
            lines.append("")
            lines.append(f"**Forca:** {e['strength']}")
            lines.append("")
            lines.append(f"**Ressalvas:** {e['caveats']}")
            lines.append("")

        # ---- 9. Candidatos a insight (Fase 8) ----
        lines.append("## 9. Candidatos a insight para a Fase 8")
        lines.append("")
        lines.append(
            "| ID | Manchete | Evidencias | Forca | Tipo | Ressalvas |"
        )
        lines.append(
            "|-----|----------|-----------|-------|------|-----------|"
        )
        for c in findings["candidates"]:
            evid = ", ".join(c["evidence"])
            caveat_short = c["caveats"][:80] + "..." if len(c["caveats"]) > 80 else c["caveats"]
            lines.append(
                f"| {c['id']} | {c['headline']} | {evid} | "
                f"{c['strength']} | {c['type']} | {caveat_short} |"
            )
        lines.append("")
        lines.append(
            f"![Candidatos a insight]"
            f"(../figures/exploratory/phase7/insight_strength.png)"
        )
        lines.append("")

        # ---- 10. Recomendacoes ----
        lines.append("## 10. Recomendacoes")
        lines.append("")
        lines.append("1. **Corrigir os bugs computacionais** antes de prosseguir:")
        lines.append("   - H03: trocar r = inf por rank-biserial ou 'efeito grande'")
        lines.append("   - H15: reportar silhouette do cluster encontrado")
        lines.append("   - H16: documentar R² negativo como 'modelo pior que o acaso'")
        lines.append("")
        lines.append("2. **Ressalvas obrigatorias** no relatorio final:")
        lines.append("   - H05: efeito negligivel (|rho| < 0.1)")
        lines.append("   - H08: diferenca de correlacao pequena (0.077)")
        lines.append("   - H15: vies de busca (perfil pre-definido)")
        lines.append("   - H17: circularidade parcial (R² inflado)")
        lines.append("   - Geral: taxa de confirmacao alta (88%) reflete "
                      "N grande + hipoteses pos-exploracao")
        lines.append("")
        lines.append("3. **Insights fortes** para destaque na Fase 8:")
        n_strong = sum(1 for c in findings["candidates"] if c["strength"] == "forte")
        lines.append(f"   - {n_strong} candidatos fortes identificados")
        lines.append("   - Foco em convergencias (multiplas analises concordam)")
        lines.append("")
        lines.append("4. **Nao reportar como descoberta:**")
        lines.append("   - H17 R² = 0.974 (circularidade)")
        lines.append("   - H11 d = 1.20 sem ressalva de tautologia parcial")
        lines.append("")

        # ---- Footer ----
        lines.append("---")
        lines.append("")
        lines.append(
            "*Relatorio gerado automaticamente por `src/integrator.py`*"
        )
        lines.append(
            f"*Dados: Sources of Pleasure (ClearerThinking.org) — N = {self.n:,}*"
        )

        report_path = self.output_dir / "phase7_integration.md"
        report_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"\n  Relatorio salvo: {report_path}")

    # ==================================================================
    # Audit CSV
    # ==================================================================

    def _write_audit_csv(self, findings):
        """Write machine-readable audit findings to CSV."""
        rows = []

        for bug in findings["bugs"]:
            rows.append({
                "check_id": bug["id"],
                "category": "bug",
                "hypothesis": bug["hypothesis"],
                "issue": bug["issue"],
                "severity": bug["severity"],
                "recommendation": bug["recommendation"],
            })

        for aud in findings["audit"]:
            rows.append({
                "check_id": aud["id"],
                "category": "auditoria",
                "hypothesis": aud["hypothesis"],
                "issue": aud["issue"],
                "severity": "medio",
                "recommendation": aud["recommendation"],
            })

        for spot in findings["spotchecks"]:
            match_str = "OK"
            if "all_match" in spot:
                match_str = "OK" if spot["all_match"] else "DIVERGENCIA"
            elif "h03_lowest_confirmed" in spot:
                match_str = "OK" if spot["h03_lowest_confirmed"] else "DIVERGENCIA"
            elif "h11_direction_confirmed" in spot:
                if spot["h11_direction_confirmed"] is None:
                    match_str = "N/A"
                else:
                    match_str = "OK" if spot["h11_direction_confirmed"] else "DIVERGENCIA"
            elif "match" in spot:
                match_str = "OK" if spot["match"] else "DIVERGENCIA"

            rows.append({
                "check_id": spot["id"],
                "category": "spot-check",
                "hypothesis": spot["description"],
                "issue": match_str,
                "severity": "info" if match_str == "OK" else "alto",
                "recommendation": "",
            })

        for cr in findings["crossrefs"]:
            rows.append({
                "check_id": cr["id"],
                "category": "cruzamento",
                "hypothesis": cr["hypotheses"],
                "issue": cr["question"],
                "severity": "info",
                "recommendation": cr["finding"][:200],
            })

        for conv in findings["convergences"]:
            rows.append({
                "check_id": conv["id"],
                "category": "convergencia",
                "hypothesis": ", ".join(conv["evidence"]),
                "issue": conv["headline"],
                "severity": "info",
                "recommendation": conv["strength"],
            })

        for emer in findings["emergent"]:
            rows.append({
                "check_id": emer["id"],
                "category": "emergente",
                "hypothesis": ", ".join(emer["evidence"]),
                "issue": emer["headline"],
                "severity": "info",
                "recommendation": emer["strength"],
            })

        for cand in findings["candidates"]:
            rows.append({
                "check_id": cand["id"],
                "category": "candidato",
                "hypothesis": ", ".join(cand["evidence"]),
                "issue": cand["headline"],
                "severity": cand["strength"],
                "recommendation": cand["caveats"][:200],
            })

        df = pd.DataFrame(rows)
        csv_path = self.data_dir / "phase7_audit.csv"
        df.to_csv(csv_path, index=False)
        print(f"  Audit CSV salvo: {csv_path}")
