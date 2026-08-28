"""
base.py — Base class for analyst agents.

Every analyst inherits from BaseAnalyst and implements run_hypothesis().
The base handles: loading data, iterating hypotheses, saving figures,
generating the markdown report, and collecting results for the CSV.
"""

from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class BaseAnalyst:
    """Standard interface for all analyst agents."""

    name = "base"           # override in subclass (e.g. "distributional")
    display_name = "Base"   # human-readable name for reports

    def __init__(self, hypotheses, clean_df, config, data_dir, output_dir,
                 fig_dir, seed=42):
        """
        Parameters
        ----------
        hypotheses : list[dict]
            Hypothesis entries from hypotheses.yaml assigned to this analyst.
        clean_df : pd.DataFrame
            The cleaned dataset (from data/processed/clean.csv).
        config : dict
            Parsed instrument.yaml.
        data_dir : Path
            Path to data/processed/ (to load phase2/3 artifacts).
        output_dir : Path
            Path to outputs/reports/.
        fig_dir : Path
            Path to outputs/figures/exploratory/phase56/.
        seed : int
            Random seed for reproducibility.
        """
        self.hypotheses = hypotheses
        self.df = clean_df
        self.config = config
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.fig_dir = Path(fig_dir)
        self.seed = seed
        self.results = []           # rows for phase56_results.csv
        self.report_sections = []   # markdown sections, one per hypothesis
        self.n_respondents = len(clean_df)

        np.random.seed(seed)

        # Extract useful column lists from config
        self.item_cols = [it["variavel"] for it in config["itens"]]
        self.factor_cols = [f"factor_{f}" for f in config["fatores"]]
        self.factor_names = list(config["fatores"].keys())
        self.standalone_items = config.get("itens_sem_fator", [])

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run_all(self):
        """Run all hypotheses assigned to this analyst."""
        print(f"\n{'='*60}")
        print(f"  Analista: {self.display_name}")
        print(f"  Hipoteses: {len(self.hypotheses)}")
        print(f"{'='*60}")

        for h in self.hypotheses:
            hid = h["id"]
            print(f"\n  >>> {hid}: {h['title']}")
            try:
                self.run_hypothesis(h)
            except Exception as e:
                print(f"  !!! ERRO em {hid}: {e}")
                self._add_result(
                    hypothesis_id=hid,
                    verdict="erro",
                    technique="—",
                    statistic_name="—",
                    statistic_value=np.nan,
                    effect_size_name="—",
                    effect_size_value=np.nan,
                    p_value=np.nan,
                    p_corrected=np.nan,
                    interpretation=f"Erro durante execucao: {e}",
                )
                self._add_report_section(
                    hid, h["title"], h.get("headline", ""),
                    technique="—",
                    premises="—",
                    result_text=f"Erro durante execucao: {e}",
                    verdict="erro",
                    interpretation="Nao foi possivel analisar.",
                    relevance="—",
                    limitations="—",
                    figures=[],
                )

        self._write_report()
        return self.results

    def run_hypothesis(self, h):
        """Run a single hypothesis. Override in each subclass."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement run_hypothesis()"
        )

    # ------------------------------------------------------------------
    # Result helpers
    # ------------------------------------------------------------------

    def _add_result(self, hypothesis_id, verdict, technique,
                    statistic_name, statistic_value,
                    effect_size_name, effect_size_value,
                    p_value, p_corrected, interpretation):
        """Append one row to the results table."""
        self.results.append({
            "hypothesis_id": hypothesis_id,
            "analyst": self.name,
            "verdict": verdict,
            "technique": technique,
            "statistic_name": statistic_name,
            "statistic_value": round(statistic_value, 4)
                if pd.notna(statistic_value) else np.nan,
            "effect_size_name": effect_size_name,
            "effect_size_value": round(effect_size_value, 4)
                if pd.notna(effect_size_value) else np.nan,
            "p_value": p_value,
            "p_corrected": p_corrected,
            "interpretation": interpretation,
        })

    # ------------------------------------------------------------------
    # Report helpers
    # ------------------------------------------------------------------

    def _add_report_section(self, hypothesis_id, title, headline,
                            technique, premises, result_text,
                            verdict, interpretation, relevance,
                            limitations, figures):
        """Append one hypothesis section to the report."""
        verdict_emoji = {
            "confirmada": "[CONFIRMADA]",
            "nao confirmada": "[NAO CONFIRMADA]",
            "inconclusiva": "[INCONCLUSIVA]",
            "erro": "[ERRO]",
        }.get(verdict, f"[{verdict.upper()}]")

        fig_links = ""
        if figures:
            fig_links = "\n**Graficos:**\n"
            for fig_path in figures:
                fig_links += f"- `{fig_path}`\n"

        section = f"""
---

### {hypothesis_id} — {title}

**Manchete:** {headline}

**Veredito:** {verdict_emoji}

**Tecnica utilizada:** {technique}

**Premissas verificadas:** {premises}

**Resultado:** {result_text}

**Interpretacao:** {interpretation}

**Relevancia (o efeito importa na pratica?):** {relevance}

**Limitacoes:** {limitations}
{fig_links}"""

        self.report_sections.append(section)

    def _write_report(self):
        """Write the full analyst report to markdown."""
        report_path = self.output_dir / f"analyst_{self.name}.md"

        header = f"""# Relatorio do Analista {self.display_name}

**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Hipoteses analisadas:** {len(self.hypotheses)}
**Respondentes:** N = {self.n_respondents:,}
**Seed aleatoria:** {self.seed}

## Resumo de vereditos

| Hipotese | Titulo | Veredito |
|----------|--------|----------|"""

        for h, r in zip(self.hypotheses, self.results):
            header += f"\n| {r['hypothesis_id']} | {h['title']} | {r['verdict']} |"

        body = "\n\n## Analises detalhadas\n"
        body += "\n".join(self.report_sections)

        footer = f"""

---

*Relatorio gerado automaticamente por `src/analysts/{self.name}.py`*
*Dados: Sources of Pleasure (ClearerThinking.org) — N = {self.n_respondents:,}*
"""

        report_path.write_text(header + body + footer, encoding="utf-8")
        print(f"\n  Relatorio salvo: {report_path}")

    # ------------------------------------------------------------------
    # Figure helpers
    # ------------------------------------------------------------------

    def _save_fig(self, fig, hypothesis_id, suffix=""):
        """Save a figure and return its path (relative to project root)."""
        self.fig_dir.mkdir(parents=True, exist_ok=True)
        name = f"{hypothesis_id}_{suffix}.png" if suffix else f"{hypothesis_id}.png"
        path = self.fig_dir / name
        fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        rel = path.relative_to(self.fig_dir.parents[3])  # relative to project root
        print(f"    Grafico: {rel}")
        return str(rel)

    # ------------------------------------------------------------------
    # Data loading helpers (phase 2/3 artifacts)
    # ------------------------------------------------------------------

    def load_item_stats(self):
        """Load phase2_item_stats.csv."""
        return pd.read_csv(self.data_dir / "phase2_item_stats.csv", index_col=0)

    def load_factor_stats(self):
        """Load phase2_factor_stats.csv."""
        return pd.read_csv(self.data_dir / "phase2_factor_stats.csv", index_col=0)

    def load_respondent_profiles(self):
        """Load phase2_respondent_profiles.csv."""
        return pd.read_csv(
            self.data_dir / "phase2_respondent_profiles.csv", index_col=0
        )

    def load_corr_items(self):
        """Load phase3_corr_items.csv (37x37 Spearman matrix)."""
        return pd.read_csv(self.data_dir / "phase3_corr_items.csv", index_col=0)

    def load_corr_factors(self):
        """Load phase3_corr_factors.csv (6x6 Spearman matrix)."""
        return pd.read_csv(self.data_dir / "phase3_corr_factors.csv", index_col=0)
