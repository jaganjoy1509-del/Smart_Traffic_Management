"""
data_loader.py
Reads the traffic CSV file into a pandas DataFrame.
This is deliberately simple: one function, one job.
"""

import pandas as pd


def load_csv(path):
    """Load the traffic dataset from a CSV file path and return a DataFrame."""
    df = pd.read_csv(path)
    return df


if __name__ == "__main__":
    # Quick manual check when running this file directly
    data = load_csv("traffic_data.csv")
    print(data.head())
    print(f"\nLoaded {len(data)} rows")
