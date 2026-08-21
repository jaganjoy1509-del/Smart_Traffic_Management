# Smart Traffic Management System (Prototype)

MCA Project — University of Mysore — Jagan R (MCA23527)

A software prototype demonstrating AI-assisted traffic congestion classification
and rule-based signal-timing recommendation, using simulated traffic-volume data.

## Modules
- `generate_dataset.py` — generates simulated traffic data
- `data_loader.py` — loads the CSV dataset
- `preprocessing.py` — cleans data, engineers features, assigns congestion labels
- `classifier.py` — Random Forest congestion classifier
- `signal_logic.py` — rule-based signal-timing recommendation
- `dashboard.py` — Flask dashboard displaying live results
- `test_traffic_system.py` — automated test suite (19 tests)

## Run it
```
pip install pandas scikit-learn flask
python generate_dataset.py
python dashboard.py
```
Then open http://localhost:5050

## Run tests
```
pip install pytest
pytest test_traffic_system.py -v
```
