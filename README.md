# VOC Proficiency Evaluation

Python scripts for evaluating synthetic VOC proficiency-testing data and examining measurement variability.

The repository uses synthetic TVOC and toluene data and does not contain results from actual laboratories or proficiency-testing programs.

## Overview

The repository includes two examples:

- proficiency evaluation using z-scores and relative error
- variability analysis across chamber and sampling-volume conditions

## Proficiency Evaluation

The synthetic proficiency dataset contains results for 20 laboratories and two analytes:

- TVOC
- Toluene

This gives 40 observations in total.

The following metrics are calculated:

```text
z_score = (participant_result - assigned_value) / proficiency_sd

error_pct = (participant_result - assigned_value)
            / assigned_value × 100
```

For this example, the criteria are:

```text
|z_score| <= 2
|error_pct| <= 30%
```

The two criteria are evaluated independently.

## Sampling Variability

A separate synthetic dataset is used to examine variability across chamber and sampling-volume conditions.

The dataset contains:

```text
5 chambers
× 5 sampling volumes
× 2 analytes
× 5 replicates
= 250 observations
```

Lower sampling volumes are simulated with greater measurement variability.

## Outputs

The scripts generate:

- TVOC z-score plot
- toluene z-score plot
- relative-error plot
- TVOC–toluene comparison
- sampling-volume variability plot
- chamber comparison

## Repository Structure

```text
.
├── data/
├── figures/
├── src/
├── tests/
├── README.md
└── requirements.txt
```

## Usage

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Generate the synthetic data:

```bash
python src/generate_synthetic_data.py
```

Generate the figures:

```bash
python src/visualization.py
```

Run the tests:

```bash
python -m pytest
```

## Data

All data included in this repository are synthetic.

The simulated results, chamber effects, sampling-volume effects, and outlying observations are provided only for demonstration of the analysis workflow.

## Limitations

This repository is an analysis example and does not represent an actual interlaboratory study or an official proficiency-testing procedure.

## License

MIT License. See `LICENSE`.
