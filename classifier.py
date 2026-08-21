"""
classifier.py
Trains a Random Forest classifier to predict congestion category
from vehicle_count and hour of day. Random Forest was chosen (per
the literature review, Chapter II) for its balance of accuracy and
interpretability.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


class CongestionClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.trained = False

    def train(self, df):
        """Train the model on preprocessed data. Returns test accuracy."""
        X = df[["vehicle_count", "hour"]]
        y = df["congestion_category"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )

        self.model.fit(X_train, y_train)
        self.trained = True

        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        return accuracy, report

    def predict(self, vehicle_count, hour):
        """Predict congestion category for a single record."""
        if not self.trained:
            raise RuntimeError("Model must be trained before predicting.")
        return self.model.predict([[vehicle_count, hour]])[0]


if __name__ == "__main__":
    from data_loader import load_csv
    from preprocessing import preprocess

    raw = load_csv("traffic_data.csv")
    data = preprocess(raw)

    clf = CongestionClassifier()
    accuracy, report = clf.train(data)

    print(f"Test accuracy: {accuracy:.4f}\n")
    print(report)

    # Sample predictions
    print("Sample predictions:")
    for count, hour in [(15, 2), (60, 13), (110, 18)]:
        pred = clf.predict(count, hour)
        print(f"  vehicle_count={count}, hour={hour} -> {pred}")
