"""
test_traffic_system.py
Unit and integration tests for the smart traffic management prototype.
Run with: pytest test_traffic_system.py -v
"""

import pandas as pd
import pytest

from data_loader import load_csv
from preprocessing import clean, add_features, assign_labels, preprocess
from classifier import CongestionClassifier
from signal_logic import get_signal_duration


# ---------- Unit tests: data_loader ----------

def test_load_csv_returns_dataframe():
    df = load_csv("traffic_data.csv")
    assert isinstance(df, pd.DataFrame)


def test_load_csv_has_expected_columns():
    df = load_csv("traffic_data.csv")
    expected = {"timestamp", "junction_name", "vehicle_count"}
    assert expected.issubset(set(df.columns))


def test_load_csv_not_empty():
    df = load_csv("traffic_data.csv")
    assert len(df) > 0


# ---------- Unit tests: preprocessing ----------

def test_clean_removes_negative_counts():
    df = pd.DataFrame({
        "timestamp": ["2026-08-01 00:00", "2026-08-01 01:00"],
        "junction_name": ["A", "B"],
        "vehicle_count": [10, -5],
    })
    cleaned = clean(df)
    assert (cleaned["vehicle_count"] >= 0).all()
    assert len(cleaned) == 1


def test_clean_drops_missing_values():
    df = pd.DataFrame({
        "timestamp": ["2026-08-01 00:00", None],
        "junction_name": ["A", "B"],
        "vehicle_count": [10, 20],
    })
    cleaned = clean(df)
    assert len(cleaned) == 1


def test_add_features_creates_hour_column():
    df = pd.DataFrame({
        "timestamp": ["2026-08-01 14:30"],
        "junction_name": ["A"],
        "vehicle_count": [50],
    })
    result = add_features(df)
    assert "hour" in result.columns
    assert result["hour"].iloc[0] == 14


@pytest.mark.parametrize("count,expected", [
    (10, "Low"),
    (35, "Low"),
    (36, "Moderate"),
    (75, "Moderate"),
    (76, "High"),
    (150, "High"),
])
def test_assign_labels_thresholds(count, expected):
    df = pd.DataFrame({"vehicle_count": [count]})
    result = assign_labels(df)
    assert result["congestion_category"].iloc[0] == expected


# ---------- Unit tests: signal_logic ----------

@pytest.mark.parametrize("category,expected_duration", [
    ("Low", 20),
    ("Moderate", 45),
    ("High", 75),
])
def test_get_signal_duration_known_categories(category, expected_duration):
    assert get_signal_duration(category) == expected_duration


def test_get_signal_duration_unknown_category_uses_default():
    assert get_signal_duration("Unknown") == 30


# ---------- Unit tests: classifier ----------

def test_classifier_raises_if_predict_before_train():
    clf = CongestionClassifier()
    with pytest.raises(RuntimeError):
        clf.predict(50, 10)


def test_classifier_trains_and_predicts():
    raw = load_csv("traffic_data.csv")
    data = preprocess(raw)
    clf = CongestionClassifier()
    accuracy, report = clf.train(data)
    assert 0.0 <= accuracy <= 1.0
    prediction = clf.predict(100, 18)
    assert prediction in {"Low", "Moderate", "High"}


# ---------- Integration test: full pipeline ----------

def test_full_pipeline_end_to_end():
    raw = load_csv("traffic_data.csv")
    processed = preprocess(raw)
    assert "congestion_category" in processed.columns

    clf = CongestionClassifier()
    accuracy, _ = clf.train(processed)
    assert accuracy > 0.5  # sanity check: better than random guessing

    sample_row = processed.iloc[0]
    category = clf.predict(sample_row["vehicle_count"], sample_row["hour"])
    duration = get_signal_duration(category)
    assert duration in {20, 45, 75}
