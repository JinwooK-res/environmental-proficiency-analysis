"""Metric calculations for synthetic proficiency-testing results."""

from __future__ import annotations

import numpy as np
import pandas as pd


def add_proficiency_metrics(results: pd.DataFrame) -> pd.DataFrame:
    """Return results with z-score and two independent pass/fail metrics."""
    required = {"assigned_value", "proficiency_sd", "participant_result"}
    missing = required.difference(results.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    out = results.copy()
    out["z_score"] = (
        out["participant_result"] - out["assigned_value"]
    ) / out["proficiency_sd"]
    out["z_pass"] = out["z_score"].abs() <= 2
    out["error_pct"] = (
        (out["participant_result"] - out["assigned_value"])
        / out["assigned_value"]
        * 100
    )
    out["error_pass"] = out["error_pct"].abs() <= 30
    return out


def z_score(participant_result: float, assigned_value: float, proficiency_sd: float) -> float:
    return (participant_result - assigned_value) / proficiency_sd


def z_pass(value: float) -> bool:
    return bool(np.abs(value) <= 2)


def error_pct(participant_result: float, assigned_value: float) -> float:
    return (participant_result - assigned_value) / assigned_value * 100


def error_pass(value: float) -> bool:
    return bool(np.abs(value) <= 30)
