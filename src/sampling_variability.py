"""Analysis helpers for the synthetic chamber sampling experiment."""

from __future__ import annotations

import pandas as pd


def summarize_sampling_variability(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize measured-value variability by analyte and sampling volume."""
    return (
        data.groupby(["analyte", "sampling_volume"], as_index=False)
        .agg(mean_value=("measured_value", "mean"), sd_value=("measured_value", "std"), n=("measured_value", "size"))
        .sort_values(["analyte", "sampling_volume"])
    )


def summarize_chambers(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize chamber means for the synthetic experiment."""
    return (
        data.groupby(["analyte", "chamber"], as_index=False)
        .agg(mean_value=("measured_value", "mean"), sd_value=("measured_value", "std"), n=("measured_value", "size"))
        .sort_values(["analyte", "chamber"])
    )
