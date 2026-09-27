"""Generate deterministic, fully synthetic proficiency and sampling data."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from proficiency_metrics import add_proficiency_metrics

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SEED = 20260927


def generate_participants() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    labs = [f"SYN-LAB-{i:02d}" for i in range(1, 21)]
    specs = {"TVOC": (120.0, 12.0), "Toluene": (48.0, 6.0)}
    rows = []
    for analyte, (assigned, sd) in specs.items():
        scores = rng.normal(0, 0.72, len(labs))
        scores = np.clip(scores, -1.85, 1.85)
        scores[2] = 2.35 if analyte == "TVOC" else -2.25
        scores[15] = -2.15 if analyte == "TVOC" else 2.30
        for lab, score in zip(labs, scores):
            rows.append({
                "lab_id": lab,
                "analyte": analyte,
                "assigned_value": assigned,
                "proficiency_sd": sd,
                "z_score_source": float(score),
                "participant_result": assigned + float(score) * sd,
            })
    out = add_proficiency_metrics(pd.DataFrame(rows))
    return out[["lab_id", "analyte", "assigned_value", "proficiency_sd", "participant_result", "z_score", "z_pass", "error_pct", "error_pass"]]


def generate_sampling_experiment() -> pd.DataFrame:
    rng = np.random.default_rng(SEED + 1)
    baselines = {"TVOC": 120.0, "Toluene": 48.0}
    chamber_effects = {f"CH-{i}": effect for i, effect in enumerate([-2.4, -0.9, 0.0, 1.3, 2.1], start=1)}
    volumes = [10, 25, 50, 100, 200]
    rows = []
    run = 1
    for chamber, chamber_effect in chamber_effects.items():
        for volume in volumes:
            noise_sd = 5.2 / np.sqrt(volume / 10)
            for analyte, baseline in baselines.items():
                for replicate in range(1, 6):
                    rows.append({
                        "run_id": f"RUN-{run:03d}",
                        "chamber": chamber,
                        "sampling_volume": volume,
                        "analyte": analyte,
                        "replicate": replicate,
                        "measured_value": baseline + chamber_effect + rng.normal(0, noise_sd),
                    })
                    run += 1
    return pd.DataFrame(rows)


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    participants = generate_participants()
    sampling = generate_sampling_experiment()
    participants.to_csv(DATA_DIR / "synthetic_participants.csv", index=False)
    sampling.to_csv(DATA_DIR / "synthetic_sampling_experiment.csv", index=False)
    print(f"Wrote synthetic_participants.csv: {participants.shape}")
    print(f"Wrote synthetic_sampling_experiment.csv: {sampling.shape}")


if __name__ == "__main__":
    main()
