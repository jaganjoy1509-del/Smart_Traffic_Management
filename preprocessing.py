"""
preprocessing.py
Cleans the raw traffic data and engineers the 'hour' feature the
classifier needs. Also assigns the congestion label used for training,
based on vehicle_count thresholds decided from the dataset's own
distribution (documented in Chapter VI - Testing).
"""

import pandas as pd


def clean(df):
    """Drop rows with missing/invalid values."""
    df = df.dropna()
    df = df[df["vehicle_count"] >= 0]
    return df


def add_features(df):
    """Add an 'hour' column extracted from the timestamp."""
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    return df


def assign_labels(df, low_max=35, moderate_max=75):
    """
    Assign a congestion category based on vehicle_count.
    Thresholds are simple, documented rules (not hidden magic numbers) -
    Low: <= low_max, Moderate: <= moderate_max, High: above that.
    """
    df = df.copy()

    def label(count):
        if count <= low_max:
            return "Low"
        elif count <= moderate_max:
            return "Moderate"
        else:
            return "High"

    df["congestion_category"] = df["vehicle_count"].apply(label)
    return df


def preprocess(df):
    """Run the full preprocessing pipeline."""
    df = clean(df)
    df = add_features(df)
    df = assign_labels(df)
    return df


if __name__ == "__main__":
    from data_loader import load_csv

    raw = load_csv("traffic_data.csv")
    processed = preprocess(raw)
    print(processed.head())
    print("\nCategory counts:")
    print(processed["congestion_category"].value_counts())
