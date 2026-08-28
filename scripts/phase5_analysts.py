"""
phase5_analysts.py — Coordinator script for Phase 5.

Reads hypotheses.yaml, loads data, distributes hypotheses to the right
analyst agent, runs all analyses, collects results into phase56_results.csv.

Usage:
    python scripts/phase5_analysts.py
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import yaml
import pandas as pd

from src.analysts.distributional import DistributionalAnalyst
from src.analysts.relational import RelationalAnalyst
from src.analysts.structural import StructuralAnalyst
from src.analysts.segmentation import SegmentationAnalyst
from src.analysts.predictive import PredictiveAnalyst

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data" / "processed"
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "reports"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures" / "exploratory" / "phase56"

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

# ---------------------------------------------------------------------------
# Group hypotheses by analyst
# ---------------------------------------------------------------------------
analyst_groups = {}
for hid, hdata in hypotheses.items():
    analyst = hdata["analyst"]
    if analyst not in analyst_groups:
        analyst_groups[analyst] = []
    analyst_groups[analyst].append(hdata)

print(f"\nDistribuicao:")
for analyst, hyps in analyst_groups.items():
    ids = [h["id"] for h in hyps]
    print(f"  {analyst}: {', '.join(ids)}")

# ---------------------------------------------------------------------------
# Analyst registry
# ---------------------------------------------------------------------------
ANALYST_CLASSES = {
    "distributional": DistributionalAnalyst,
    "relational": RelationalAnalyst,
    "structural": StructuralAnalyst,
    "segmentation": SegmentationAnalyst,
    "predictive": PredictiveAnalyst,
}

# ---------------------------------------------------------------------------
# Run each analyst
# ---------------------------------------------------------------------------
all_results = []

FIG_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for analyst_name, hyps in analyst_groups.items():
    if analyst_name not in ANALYST_CLASSES:
        print(f"\n  AVISO: analista '{analyst_name}' nao implementado, pulando.")
        continue

    AnalystClass = ANALYST_CLASSES[analyst_name]
    analyst = AnalystClass(
        hypotheses=hyps,
        clean_df=clean_df,
        config=config,
        data_dir=DATA_DIR,
        output_dir=OUTPUT_DIR,
        fig_dir=FIG_DIR,
        seed=SEED,
    )

    results = analyst.run_all()
    all_results.extend(results)

# ---------------------------------------------------------------------------
# Save consolidated results
# ---------------------------------------------------------------------------
results_df = pd.DataFrame(all_results)
results_csv = DATA_DIR / "phase56_results.csv"
results_df.to_csv(results_csv, index=False)

print(f"\n{'='*60}")
print(f"  FASE 5 COMPLETA")
print(f"{'='*60}")
print(f"  Hipoteses analisadas: {len(all_results)}")
print(f"  Resultados consolidados: {results_csv}")
print(f"\n  Vereditos:")
for _, row in results_df.iterrows():
    print(f"    {row['hypothesis_id']}: {row['verdict']}")

print(f"\n  Relatorios gerados:")
for analyst_name in analyst_groups:
    report = OUTPUT_DIR / f"analyst_{analyst_name}.md"
    if report.exists():
        print(f"    {report}")

print(f"\n  Graficos em: {FIG_DIR}")
