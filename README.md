# Synthetic Environmental Proficiency Analysis

This project is a publication-safe demonstration of how synthetic interlaboratory VOC emission results can be analyzed and visualized for proficiency-testing and QA-QC workflows.

## Research question

How can synthetic interlaboratory VOC emission results be analyzed and visualized to demonstrate proficiency-testing metrics and measurement variability?

## Scope and data safety

All data in this repository are fully synthetic and generated from scratch. No actual proficiency-testing participant data, actual 2025 or 2026 data, participant identities, institution names, sample IDs, chamber results, assigned values, participant values, raw internal files, internal reports, or figures generated from real data are included. The deliberately failing cases exist only to demonstrate metric behavior. This repository does not reproduce any specific official proficiency test and is not an official evaluation tool.

The chamber and sampling-volume effects are artificial assumptions used to make variance behavior visible. They do not represent measured chamber behavior or any real laboratory process.

## Contents

- `data/synthetic_participants.csv`: 20 synthetic labs × 2 analytes, one result per lab/analyte.
- `data/synthetic_sampling_experiment.csv`: balanced 5 chamber × 5 sampling volume × 2 analyte × 5 replicate experiment (250 rows).
- `src/`: deterministic data generation, proficiency metrics, sampling analysis, and plotting code.
- `tests/`: boundary and structural tests.
- `figures/`: generated demonstration figures.

## Reproduce

```text
python -m pip install -r requirements.txt
python src/generate_synthetic_data.py
python src/visualization.py
pytest
```

The scripts use a fixed random seed. The proficiency decision rules are analyte-level only: `z_pass` is true when `abs(z_score) <= 2`, and `error_pass` is true when `abs(error_pct) <= 30`. No joint multivariate acceptance rule is created.

## License

MIT License. See `LICENSE`.
