"""
dashboard.py
A small Flask app that ties together the data loader, preprocessing,
classifier, and signal logic modules, and displays the results.
"""

import os
from flask import Flask, render_template_string, request
from data_loader import load_csv
from preprocessing import preprocess
from classifier import CongestionClassifier
from signal_logic import get_signal_duration

app = Flask(__name__)

# Load, preprocess, and train once at startup
raw = load_csv("traffic_data.csv")
data = preprocess(raw)
clf = CongestionClassifier()
accuracy, report = clf.train(data)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>Smart Traffic Management Dashboard</title>
  <style>
    body { font-family: Arial, Helvetica, sans-serif; padding: 30px; background: #f5f6f8; color: #222; }
    h2 { margin-bottom: 4px; }
    .subtitle { color: #666; margin-bottom: 16px; }
    .accuracy-badge {
      display: inline-block; background: #1d9e75; color: white;
      padding: 6px 14px; border-radius: 6px; font-size: 15px; margin-bottom: 20px;
    }
    table { border-collapse: collapse; width: 100%; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    th, td { padding: 10px 14px; text-align: left; border-bottom: 1px solid #e5e5e5; }
    th { background: #2c2c2a; color: white; }
    tr:nth-child(even) { background: #fafafa; }
    .badge { padding: 4px 10px; border-radius: 12px; font-size: 13px; color: white; }
    .badge-low { background: #3b6d11; }
    .badge-moderate { background: #ba7517; }
    .badge-high { background: #a32d2d; }
  </style>
</head>
<body>
  <h2>Smart Traffic Management System</h2>
  <p class="subtitle">Prototype dashboard - simulated traffic data, not live sensors.</p>
  <span class="accuracy-badge">Model test accuracy: {{ accuracy }}</span>

  <form method="get" style="margin: 16px 0;">
    <label for="junction" style="margin-right: 8px;">Filter by junction:</label>
    <select name="junction" id="junction" onchange="this.form.submit()" style="padding: 6px; border-radius: 4px;">
      {% for j in junctions %}
      <option value="{{ j }}" {% if j == selected %}selected{% endif %}>{{ j }}</option>
      {% endfor %}
    </select>
  </form>

  <table>
    <thead>
      <tr>
        <th>Timestamp</th>
        <th>Junction</th>
        <th>Vehicle Count</th>
        <th>Congestion</th>
        <th>Recommended Signal (sec)</th>
      </tr>
    </thead>
    <tbody>
      {% for row in rows %}
      <tr>
        <td>{{ row.timestamp }}</td>
        <td>{{ row.junction_name }}</td>
        <td>{{ row.vehicle_count }}</td>
        <td><span class="badge {{ row.badge_class }}">{{ row.congestion_category }}</span></td>
        <td>{{ row.signal_duration }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""

BADGE_CLASS = {"Low": "badge-low", "Moderate": "badge-moderate", "High": "badge-high"}


@app.route("/")
def index():
    junction_filter = request.args.get("junction", "All")
    if junction_filter != "All":
        subset = data[data["junction_name"] == junction_filter]
    else:
        subset = data
    sample = subset.sample(min(15, len(subset)), random_state=1).sort_values("timestamp")
    rows = []
    for _, r in sample.iterrows():
        rows.append({
            "timestamp": r["timestamp"],
            "junction_name": r["junction_name"],
            "vehicle_count": r["vehicle_count"],
            "congestion_category": r["congestion_category"],
            "signal_duration": get_signal_duration(r["congestion_category"]),
            "badge_class": BADGE_CLASS[r["congestion_category"]],
        })
    junctions = ["All"] + sorted(data["junction_name"].unique().tolist())
    return render_template_string(
        TEMPLATE, rows=rows, accuracy=f"{accuracy:.2%}",
        junctions=junctions, selected=junction_filter
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=False, host="0.0.0.0", port=port)
