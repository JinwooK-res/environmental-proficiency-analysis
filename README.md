# Synthetic Environmental Proficiency Analysis

A reproducible, publication-safe demonstration of environmental laboratory proficiency-testing and QA/QC analysis using fully synthetic TVOC and toluene data.

## Research Question

**How can synthetic interlaboratory VOC emission results be analyzed and visualized to demonstrate proficiency-testing metrics and measurement variability?**

## Synthetic Data Notice

All data in this repository are fully synthetic and generated from scratch.

The repository does not include real participant data, institution names, sample IDs, actual 2025/2026 results, internal spreadsheets, notebooks, reports, or figures derived from real data.

A small number of failing cases are deliberately included only to demonstrate metric behavior.

The chamber and sampling-volume effects are artificial assumptions used to make variability patterns visible. They do not represent measured chamber behavior or any real laboratory process.

Visualizations are independently designed for the synthetic demonstration and do not reproduce the presentation or result patterns of the original internal analyses.

This repository does not reproduce any specific official proficiency test and is not an official evaluation tool.

## Analysis Design

The proficiency dataset contains:

- 20 synthetic laboratories
- TVOC and toluene
- one result per laboratory and analyte
- 40 total observations

Metrics:

```text
z_score = (participant_result - assigned_value) / proficiency_sd
error_pct = (participant_result - assigned_value) / assigned_value × 100

z_pass     = |z_score| <= 2
error_pass = |error_pct| <= 30%
```

These criteria are evaluated separately.

## Synthetic Sampling Experiment

Balanced design:

```text
5 chambers
× 5 sampling volumes
× 2 analytes
× 5 replicates
= 250 observations
```

Lower sampling volumes are assigned greater synthetic variability for demonstration purposes.

## Visualizations

The project generates:

- TVOC Z-scores with ±2 limits
- Toluene Z-scores with ±2 limits
- error-rate plot with ±30% limits
- paired TVOC vs. toluene results
- sampling-volume variability
- chamber comparison

## Reproduce

```powershell
python -m pip install -r requirements.txt
python src/generate_synthetic_data.py
python src/visualization.py
python -m pytest
```

## Limitations

This is a methodological demonstration, not an empirical interlaboratory study.

Synthetic distributions, chamber effects, failing cases, and variability patterns should not be interpreted as evidence about real laboratories or official proficiency-testing programs.

## License

MIT License. See [`LICENSE`](LICENSE).