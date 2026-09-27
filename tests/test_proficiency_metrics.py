import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from generate_synthetic_data import generate_participants, generate_sampling_experiment
from proficiency_metrics import error_pass, error_pct, z_pass, z_score


def test_proficiency_structure_and_determinism():
    first = generate_participants()
    second = generate_participants()
    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 40
    assert first["lab_id"].nunique() == 20
    assert first.groupby(["lab_id", "analyte"]).size().eq(1).all()
    assert set(first.columns) == {"lab_id", "analyte", "assigned_value", "proficiency_sd", "participant_result", "z_score", "z_pass", "error_pct", "error_pass"}
    assert not first.isna().any().any()


def test_metric_boundaries_are_inclusive():
    assert z_pass(2) and z_pass(-2)
    assert not z_pass(2.0001) and not z_pass(-2.0001)
    assert error_pass(30) and error_pass(-30)
    assert not error_pass(30.0001) and not error_pass(-30.0001)
    assert z_score(120, 100, 10) == 2
    assert error_pct(130, 100) == 30


def test_sampling_structure():
    data = generate_sampling_experiment()
    assert len(data) == 250
    assert data["chamber"].nunique() == 5
    assert data["sampling_volume"].nunique() == 5
    assert data["analyte"].nunique() == 2
    assert data.groupby(["chamber", "sampling_volume", "analyte"]).size().eq(5).all()
    assert not data["run_id"].duplicated().any()
