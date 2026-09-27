"""Generate publication-safe synthetic demonstration figures."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:  # pragma: no cover - exercised only when native plotting DLLs are unavailable
    plt = None
    sns = None

from sampling_variability import summarize_chambers, summarize_sampling_variability

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FIGURE_DIR = ROOT / "figures"


def _save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / name, dpi=180)
    plt.close(fig)


def _fallback_generate(participants: pd.DataFrame, sampling: pd.DataFrame) -> list[Path]:
    """Create simple PNG charts when matplotlib's optional native backend is unavailable."""
    from PIL import Image, ImageDraw

    outputs = []
    width, height = 1000, 600
    margin = 80

    def chart(name: str, title: str, x_label: str, y_label: str, points, y_min, y_max, refs=()):
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        draw.text((margin, 25), title, fill="#1d3557")
        draw.line((margin, height - margin, width - 30, height - margin), fill="#333", width=2)
        draw.line((margin, 50, margin, height - margin), fill="#333", width=2)
        for ref in refs:
            y = height - margin - (ref - y_min) / (y_max - y_min) * (height - margin - 50)
            draw.line((margin, y, width - 30, y), fill="#e76f51", width=2)
            draw.text((margin + 5, y - 18), str(ref), fill="#e76f51")
        for i, (x, y, color) in enumerate(points):
            px = margin + (x / max(1, len(points) - 1)) * (width - margin - 40)
            py = height - margin - (y - y_min) / (y_max - y_min) * (height - margin - 50)
            draw.ellipse((px - 6, py - 6, px + 6, py + 6), fill=color)
            if name in {"tvoc_z_scores.png", "toluene_z_scores.png"}:
                draw.text((px - 8, height - margin + 8), f"{i + 1}", fill="#555")
        draw.text((width // 2 - 50, height - 35), x_label, fill="#333")
        draw.text((10, height // 2), y_label, fill="#333")
        path = FIGURE_DIR / name
        image.save(path)
        outputs.append(path)

    for analyte, filename in [("TVOC", "tvoc_z_scores.png"), ("Toluene", "toluene_z_scores.png")]:
        subset = participants[participants["analyte"] == analyte].reset_index(drop=True)
        points = [(i, row.z_score, "#2a9d8f" if row.z_pass else "#e76f51") for i, row in subset.iterrows()]
        chart(filename, f"{analyte} participant Z-scores", "Synthetic laboratory", "Z-score", points, -3, 3, (-2, 2))

    points = []
    for i, row in participants.reset_index(drop=True).iterrows():
        points.append((i, row.error_pct, "#457b9d" if row.analyte == "TVOC" else "#f4a261"))
    chart("error_rate.png", "Participant error rate", "Synthetic laboratory", "Error (%)", points, -50, 50, (-30, 30))

    tvoc = participants[participants.analyte == "TVOC"].sort_values("lab_id").reset_index(drop=True)
    tol = participants[participants.analyte == "Toluene"].sort_values("lab_id").reset_index(drop=True)
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((margin, 25), "Paired synthetic results by laboratory", fill="#1d3557")
    draw.line((margin, height - margin, width - 30, height - margin), fill="#333", width=2)
    draw.line((margin, 50, margin, height - margin), fill="#333", width=2)
    for x, y in zip(tvoc.participant_result, tol.participant_result):
        px = margin + (x - 90) / 70 * (width - margin - 40)
        py = height - margin - (y - 30) / 35 * (height - margin - 50)
        draw.ellipse((px - 6, py - 6, px + 6, py + 6), fill="#457b9d")
    draw.text((width // 2 - 40, height - 35), "TVOC result", fill="#333")
    draw.text((10, height // 2), "Toluene result", fill="#333")
    path = FIGURE_DIR / "paired_tvoc_toluene.png"; image.save(path); outputs.append(path)

    summary = summarize_sampling_variability(sampling)
    for name, title, grouping, value_col in [
        ("sampling_volume_variability.png", "Synthetic sampling-volume variability", "sampling_volume", "sd_value"),
        ("chamber_comparison.png", "Synthetic chamber comparison", "chamber", "mean_value"),
    ]:
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        draw.text((margin, 25), title, fill="#1d3557")
        source = summary if grouping == "sampling_volume" else summarize_chambers(sampling)
        max_value = float(source[value_col].max()) * 1.15
        groups = list(source[grouping].unique())
        for i, group in enumerate(groups):
            subset = source[source[grouping] == group]
            for j, (_, row) in enumerate(subset.iterrows()):
                x = margin + (i + 0.25 + j * 0.5) / max(1, len(groups)) * (width - margin - 40)
                bar = row[value_col] / max_value * (height - margin - 80)
                draw.rectangle((x, height - margin - bar, x + 35, height - margin), fill="#457b9d" if j == 0 else "#e9c46a")
            draw.text((margin + i / max(1, len(groups)) * (width - margin - 40), height - margin + 8), str(group), fill="#555")
        path = FIGURE_DIR / name; image.save(path); outputs.append(path)
    return outputs


def generate_figures() -> list[Path]:
    FIGURE_DIR.mkdir(exist_ok=True)
    participants = pd.read_csv(DATA_DIR / "synthetic_participants.csv")
    sampling = pd.read_csv(DATA_DIR / "synthetic_sampling_experiment.csv")
    if plt is None or sns is None:
        return _fallback_generate(participants, sampling)
    sns.set_theme(style="whitegrid", context="notebook")
    outputs = []

    for analyte, filename in [("TVOC", "tvoc_z_scores.png"), ("Toluene", "toluene_z_scores.png")]:
        subset = participants[participants["analyte"] == analyte]
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.scatterplot(data=subset, x="lab_id", y="z_score", hue="z_pass", palette={True: "#2a9d8f", False: "#e76f51"}, s=75, ax=ax)
        ax.axhline(2, color="#e76f51", linestyle="--", label="z = ±2")
        ax.axhline(-2, color="#e76f51", linestyle="--")
        ax.set(title=f"{analyte} participant Z-scores", xlabel="Synthetic laboratory", ylabel="Z-score")
        ax.tick_params(axis="x", rotation=60)
        _save(fig, filename); outputs.append(FIGURE_DIR / filename)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(data=participants, x="lab_id", y="error_pct", hue="analyte", style="analyte", s=70, ax=ax)
    ax.axhline(30, color="#e76f51", linestyle="--", label="±30% reference")
    ax.axhline(-30, color="#e76f51", linestyle="--")
    ax.set(title="Participant error rate", xlabel="Synthetic laboratory", ylabel="Error (%)")
    ax.tick_params(axis="x", rotation=60)
    _save(fig, "error_rate.png"); outputs.append(FIGURE_DIR / "error_rate.png")

    pivot = participants.pivot(index="lab_id", columns="analyte", values="participant_result").reset_index()
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.scatterplot(data=pivot, x="TVOC", y="Toluene", s=80, color="#457b9d", ax=ax)
    ax.set(title="Paired synthetic results by laboratory", xlabel="TVOC result", ylabel="Toluene result")
    _save(fig, "paired_tvoc_toluene.png"); outputs.append(FIGURE_DIR / "paired_tvoc_toluene.png")

    summary = summarize_sampling_variability(sampling)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=summary, x="sampling_volume", y="sd_value", hue="analyte", marker="o", ax=ax)
    ax.set(title="Synthetic sampling-volume variability", xlabel="Sampling volume", ylabel="Observed SD")
    _save(fig, "sampling_volume_variability.png"); outputs.append(FIGURE_DIR / "sampling_volume_variability.png")

    chamber = summarize_chambers(sampling)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=chamber, x="chamber", y="mean_value", hue="analyte", errorbar=None, ax=ax)
    ax.set(title="Synthetic chamber comparison", xlabel="Synthetic chamber", ylabel="Mean measured value")
    _save(fig, "chamber_comparison.png"); outputs.append(FIGURE_DIR / "chamber_comparison.png")
    return outputs


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    print("Generated:")
    for path in generate_figures():
        print(path)
