import csv
import random
from datetime import datetime, timedelta

random.seed(42)

junctions = ["MG Road Junction", "Silk Board Junction", "Hebbal Flyover"]
start = datetime(2026, 8, 1, 0, 0)

rows = []
for day in range(7):
    for hour in range(24):
        for jn in junctions:
            ts = start + timedelta(days=day, hours=hour)
            # base traffic pattern: low at night, peaks at 8-10am and 5-8pm
            if 8 <= hour <= 10 or 17 <= hour <= 20:
                base = random.randint(70, 130)
            elif 0 <= hour <= 5:
                base = random.randint(5, 25)
            else:
                base = random.randint(30, 70)
            # add small junction-specific bias
            bias = {"MG Road Junction": 10, "Silk Board Junction": 20, "Hebbal Flyover": 0}[jn]
            vehicle_count = max(0, base + bias + random.randint(-10, 10))
            rows.append([ts.strftime("%Y-%m-%d %H:%M"), jn, vehicle_count])

with open("traffic_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "junction_name", "vehicle_count"])
    writer.writerows(rows)

print(f"Generated {len(rows)} rows")
