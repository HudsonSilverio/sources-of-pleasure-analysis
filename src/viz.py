"""
viz.py — Statista-inspired visualization style system.

Single source of truth for chart styling across the project.
All final figures use create_statista_figure() for consistent layout:
dark header with discovery-title, white chart area, source footer.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ======================================================================
# Color palette
# ======================================================================

COLORS = {
    # Layout
    "dark_bg": "#003045",
    "bg_white": "#FFFFFF",

    # Brand blues
    "primary": "#0666E5",
    "light_blue": "#82B2F2",
    "pale_blue": "#BDD7F6",

    # Accents
    "accent_red": "#E8443A",
    "accent_warm": "#FF8C42",
    "accent_green": "#2ECC71",

    # Text
    "text_dark": "#1A1A2E",
    "text_light": "#FFFFFF",
    "text_muted": "#6B7280",
    "text_subtitle": "#B0C4D8",

    # Chart elements
    "grid": "#E5E7EB",
    "bar_positive": "#0666E5",
    "bar_negative": "#E8443A",
    "bar_highlight": "#FF8C42",
    "bar_neutral": "#82B2F2",
    "bar_secondary": "#BDD7F6",
    "scatter_dot": "#0666E5",
}

# ======================================================================
# Typography
# ======================================================================

FONT_FAMILY = "Arial"

FONT = {
    "title": {"family": FONT_FAMILY, "size": 16, "weight": "bold",
              "color": COLORS["text_light"]},
    "subtitle": {"family": FONT_FAMILY, "size": 11, "weight": "normal",
                 "color": COLORS["text_subtitle"]},
    "axis_label": {"family": FONT_FAMILY, "size": 10, "weight": "normal",
                   "color": COLORS["text_dark"]},
    "data_label": {"family": FONT_FAMILY, "size": 9, "weight": "normal",
                   "color": COLORS["text_dark"]},
    "source": {"family": FONT_FAMILY, "size": 8, "weight": "normal",
               "color": COLORS["text_muted"]},
    "annotation": {"family": FONT_FAMILY, "size": 10, "weight": "bold",
                   "color": COLORS["text_dark"]},
}

# ======================================================================
# Paths
# ======================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FINAL_FIG_DIR = PROJECT_ROOT / "outputs" / "figures" / "final"

# ======================================================================
# Source line
# ======================================================================

SOURCE_LINE = (
    "Source: Sources of Pleasure assessment, ClearerThinking.org — "
    "N = 6,587 respondents"
)

# ======================================================================
# Figure factory
# ======================================================================

def create_statista_figure(title, subtitle="", figsize=(8, 9)):
    """
    Create a figure with Statista-inspired layout.

    Returns (fig, ax) where ax is the main chart area.
    The dark header and source footer are rendered via fig.text.

    Parameters
    ----------
    title : str
        Discovery headline (displayed in white on dark header).
    subtitle : str
        Short context line below the title.
    figsize : tuple
        Figure size in inches (width, height).

    Returns
    -------
    fig, ax : matplotlib Figure and main Axes.
    """
    fig, ax = plt.subplots(figsize=figsize)

    # White background for entire figure
    fig.patch.set_facecolor(COLORS["bg_white"])

    # --- Dark header band ---
    header_height = 0.14 if subtitle else 0.10
    header = mpatches.FancyBboxPatch(
        (0, 1 - header_height), 1, header_height,
        transform=fig.transFigure, facecolor=COLORS["dark_bg"],
        edgecolor="none", zorder=10,
        boxstyle="square,pad=0",
    )
    fig.patches.append(header)

    # Title text
    fig.text(
        0.04, 1 - 0.035, title,
        fontsize=FONT["title"]["size"],
        fontweight=FONT["title"]["weight"],
        fontfamily=FONT["title"]["family"],
        color=FONT["title"]["color"],
        transform=fig.transFigure,
        va="top", ha="left", zorder=11,
        wrap=True,
    )

    # Subtitle text
    if subtitle:
        fig.text(
            0.04, 1 - header_height + 0.02, subtitle,
            fontsize=FONT["subtitle"]["size"],
            fontweight=FONT["subtitle"]["weight"],
            fontfamily=FONT["subtitle"]["family"],
            color=FONT["subtitle"]["color"],
            transform=fig.transFigure,
            va="top", ha="left", zorder=11,
        )

    # --- Source footer ---
    fig.text(
        0.04, 0.02, SOURCE_LINE,
        fontsize=FONT["source"]["size"],
        fontweight=FONT["source"]["weight"],
        fontfamily=FONT["source"]["family"],
        color=FONT["source"]["color"],
        transform=fig.transFigure,
        va="bottom", ha="left",
    )

    # --- Adjust axes to fit between header and footer ---
    ax.set_position([0.12, 0.08, 0.82, 0.90 - header_height - 0.04])
    ax.set_facecolor(COLORS["bg_white"])

    # Clean up spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["grid"])
    ax.spines["bottom"].set_color(COLORS["grid"])

    # Tick styling
    ax.tick_params(
        colors=COLORS["text_dark"],
        labelsize=FONT["data_label"]["size"],
    )

    return fig, ax


def save_final_figure(fig, name):
    """Save figure to outputs/figures/final/ at high resolution."""
    FINAL_FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = FINAL_FIG_DIR / f"{name}.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"    Grafico salvo: {path}")
    return str(path)
