"""
signal_logic.py
Converts a predicted congestion category into a recommended green
signal duration. Deliberately rule-based (not ML) so the decision
is transparent and explainable - see NFR6 in Chapter III.
"""

SIGNAL_DURATIONS = {
    "Low": 20,       # seconds
    "Moderate": 45,
    "High": 75,
}


def get_signal_duration(category):
    """Return the recommended green-light duration in seconds."""
    return SIGNAL_DURATIONS.get(category, 30)  # default fallback


if __name__ == "__main__":
    for cat in ["Low", "Moderate", "High"]:
        print(f"{cat} congestion -> {get_signal_duration(cat)}s green signal")
