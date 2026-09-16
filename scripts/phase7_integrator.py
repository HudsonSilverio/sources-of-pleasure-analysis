"""
phase7_integrator.py — Runner for Phase 7 (Senior Integrator).

Loads config, data, and Phase 5/6 results. Runs the SeniorIntegrator
to audit all analyst findings, cross-reference hypotheses, and compile
candidate insights for Phase 8.

Usage:
    python scripts/phase7_integrator.py
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import yaml
import pandas as pd

from src.integrator import SeniorIntegrator

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data" / "processed"
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "reports"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures" / "exploratory" / "phase7"

SEED = 42

# ---------------------------------------------------------------------------
# Load config
# ---------------------------------------------------------------------------
print("Carregando configuracao...")

with open(CONFIG_DIR / "instrument.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

with open(CONFIG_DIR / "hypotheses.yaml", "r", encoding="utf-8") as f:
    hypotheses_raw = yaml.safe_load(f)["hypotheses"]

# Add ID to each hypothesis
hypotheses = {}
for hid, hdata in hypotheses_raw.items():
    hdata["id"] = hid
    hypotheses[hid] = hdata

print(f"  {len(hypotheses)} hipoteses carregadas")

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
print("Carregando dados...")

clean_df = pd.read_csv(DATA_DIR / "clean.csv")
print(f"  clean.csv: {len(clean_df):,} linhas x {len(clean_df.columns)} colunas")

results_df = pd.read_csv(DATA_DIR / "phase56_results.csv")
print(f"  phase56_results.csv: {len(results_df)} hipoteses")

# ---------------------------------------------------------------------------
# Ensure output dirs exist
# ---------------------------------------------------------------------------
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Run integrator
# ---------------------------------------------------------------------------
integrator = SeniorIntegrator(
    clean_df=clean_df,
    config=config,
    hypotheses=hypotheses,
    results_df=results_df,
    data_dir=DATA_DIR,
    output_dir=OUTPUT_DIR,
    fig_dir=FIG_DIR,
    seed=SEED,
)

findings = integrator.run_all()

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print(f"\n{'='*60}")
print(f"  FASE 7 COMPLETA")
print(f"{'='*60}")

print(f"\n  Verificacoes realizadas:")
print(f"    Bugs computacionais: {len(findings['bugs'])}")
print(f"    Auditorias de veredito: {len(findings['audit'])}")
print(f"    Spot-checks: {len(findings['spotchecks'])}")
print(f"    Cruzamentos: {len(findings['crossrefs'])}")
print(f"    Convergencias: {len(findings['convergences'])}")
print(f"    Insights emergentes: {len(findings['emergent'])}")
print(f"    Candidatos a insight: {len(findings['candidates'])}")

total = (
    len(findings["bugs"])
    + len(findings["audit"])
    + len(findings["spotchecks"])
    + len(findings["crossrefs"])
    + len(findings["convergences"])
    + len(findings["emergent"])
)
print(f"\n  Total de verificacoes: {total}")

print(f"\n  Saidas geradas:")
print(f"    Relatorio: {OUTPUT_DIR / 'phase7_integration.md'}")
print(f"    Audit CSV: {DATA_DIR / 'phase7_audit.csv'}")
print(f"    Graficos: {FIG_DIR}")

print(f"\n  Candidatos a insight (Fase 8):")
for c in findings["candidates"]:
    print(f"    {c['id']}: {c['headline']} [{c['strength']}]")
