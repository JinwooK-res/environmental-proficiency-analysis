# Synthetic Environmental Proficiency Analysis

A reproducible, publication-safe demonstration of environmental laboratory proficiency-testing and QA/QC analysis using fully synthetic TVOC and toluene data.

The project shows how interlaboratory results, proficiency metrics, and controlled measurement variability can be structured, tested, and visualized without exposing any real participant or institutional data.

## Research Question

**How can synthetic interlaboratory VOC emission results be analyzed and visualized to demonstrate proficiency-testing metrics and measurement variability?**

## Synthetic Data and Publication Safety

All data in this repository are generated from scratch and are fully synthetic.

The repository does **not** contain:

- actual proficiency-testing participant data
- actual 2025 or 2026 proficiency-test results
- participant or institution identities
- real sample IDs
- actual chamber measurements
- real assigned values or participant results
- internal spreadsheets, notebooks, reports, or source figures

A small number of deliberately failing synthetic cases are included only to demonstrate how proficiency metrics behave around acceptance thresholds.

The synthetic chamber and sampling-volume effects are also artificial assumptions designed to make measurement-variability patterns visible. They do not represent measured chamber behavior or any specific laboratory process.

This repository does not reproduce any specific official proficiency test and is not an official evaluation tool.

## Analysis Design

The proficiency dataset contains:

- 20 synthetic laboratories
- TVOC and toluene
- one result per laboratory and analyte
- 40 total observations

For each analyte, a fixed synthetic assigned value and proficiency standard deviation are used across laboratories.

The following metrics are calculated:

```text
z_score = (participant_result - assigned_value) / proficiency_sd

error_pct = (participant_result - assigned_value) / assigned_value × 100
```

Demonstration decision rules:

```text
z_pass     = |z_score| <= 2
error_pass = |error_pct| <= 30%
```

These criteria are evaluated separately. No joint multivariate acceptance rule is created.

## Synthetic Sampling Experiment

Measurement variability is demonstrated using a balanced synthetic design:

```text
5 chambers
× 5 sampling volumes
× 2 analytes
× 5 replicates
= 250 observations
```

The synthetic measurement model combines:

- analyte-specific baseline values
- fixed artificial chamber effects
- sampling-volume-dependent variability
- random measurement noise

Lower sampling volumes are intentionally assigned greater synthetic measurement variability for demonstration purposes.

## Visualizations

The repository generates six public-facing figures:

- TVOC laboratory Z-scores with ±2 reference limits
- Toluene laboratory Z-scores with ±2 reference limits
- error-rate distribution with ±30% reference limits
- paired TVOC vs. toluene laboratory results
- sampling-volume variability
- chamber comparison

All figures are derived exclusively from the synthetic datasets.

## Project Structure

```text
environmental-proficiency-analysis/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── data/
│   ├── synthetic_participants.csv
│   └── synthetic_sampling_experiment.csv
├── figures/
│   ├── tvoc_z_scores.png
│   ├── toluene_z_scores.png
│   ├── error_rate.png
│   ├── paired_tvoc_toluene.png
│   ├── sampling_volume_variability.png
│   └── chamber_comparison.png
├── src/
│   ├── __init__.py
│   ├── generate_synthetic_data.py
│   ├── proficiency_metrics.py
│   ├── sampling_variability.py
│   └── visualization.py
└── tests/
    └── test_proficiency_metrics.py
```

## Reproduce

Create and activate a Python environment, then install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Generate the synthetic datasets:

```powershell
python src/generate_synthetic_data.py
```

Generate all figures:

```powershell
python src/visualization.py
```

Run the validation tests:

```powershell
python -m pytest
```

The synthetic-data generator uses a fixed random seed so that the public demonstration can be reproduced consistently.

## Validation

The test suite checks:

- deterministic synthetic-data generation
- 20 unique synthetic laboratories
- exactly one result per laboratory and analyte
- Z-score boundary behavior at ±2
- error-rate boundary behavior at ±30%
- balanced 250-row sampling design
- five replicates per chamber × volume × analyte combination
- unique run IDs
- absence of missing values

## Limitations

This repository is a methodological demonstration rather than an empirical interlaboratory study.

In particular:

- synthetic distributions do not represent actual participant performance
- deliberately failing cases are inserted for illustration
- chamber effects are artificial
- sampling-volume variability is imposed by the synthetic model
- the project does not estimate real laboratory quality or proficiency
- the results should not be interpreted as evidence about any specific institution or official proficiency-testing program

## License

MIT License. See [`LICENSE`](LICENSE).