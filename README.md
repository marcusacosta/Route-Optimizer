# Route Optimizer API

A Flask-based web service that computes the shortest “greedy” route through multiple waypoints and provides a traffic-aware ETA. Ideal for backend-focused portfolios, this project demonstrates:

* Graph algorithms (Haversine + nearest-neighbor heuristic)
* Simple traffic modeling (rush-hour & congestion)
* Performance instrumentation (timing, CPU & memory via `psutil`)
* Input validation and error handling
* Full test coverage with `pytest`
* One-click deploy on Render / Railway / Fly.io

---

## 🗂️ Repository Structure

```text
route-optimizer/
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── routes.py         # HTTP routes, validation & logging
│   ├── optimizer.py      # Core routing & ETA logic
│   └── utils.py          # Helper functions & payload validation
├── tests/
│   ├── test_optimizer.py # Unit tests for haversine, multiplier & optimizer
│   └── test_api.py       # Endpoint integration tests
├── run.py                # App entrypoint
├── requirements.txt      # Python dependencies
├── pytest.ini            # pytest configuration (adds project to PYTHONPATH)
└── README.md             # ← You are here
```

---

## 🚀 Features

* **`/optimize`** endpoint accepts JSON payload:

  * **`origin`**: `[lat, lon]`
  * **`destinations`**: `[[lat, lon], …]`
  * **`time_of_day`**: hour in 24h (e.g. `8.5` = 8:30 AM)
  * **`traffic_level`**: integer `0–3`
* **Input validation** with clear error messages (HTTP 400)
* **Nearest-neighbor routing** using Haversine great-circle distance
* **ETA calculation** at 50 km/h base, scaled by:

  * Rush-hour × 1.5 (7–9 AM & 4–6 PM)
  * + 10 % per congestion level
* **Performance logging** via `psutil`:

  * Execution time (s)
  * ΔCPU % & ΔMemory (KiB)
* **Health check** endpoint (`/`)
* **Fully tested** with `pytest` (zero failing tests)

---

## 🛠️ Local Setup

### 1. Clone & Virtual Environment

```bash
git clone git@github.com:<your-username>/route-optimizer.git
cd route-optimizer
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Pin Dev Dependencies

```bash
pip install pytest
echo "pytest" >> requirements.txt
```

---

## 🏃 Running Locally

```bash
# Start in debug mode on http://127.0.0.1:5000
python3 run.py
```

### Test with `curl`

```bash
curl -X POST http://127.0.0.1:5000/optimize \
  -H 'Content-Type: application/json' \
  -d '{
        "origin": [37.77, -122.42],
        "destinations": [[37.78, -122.43], [37.76, -122.41]],
        "time_of_day": 8,
        "traffic_level": 2
      }'
```

Example response:

```json
{
  "optimized_route": [
    [37.77, -122.42],
    [37.78, -122.43],
    [37.76, -122.41]
  ],
  "estimated_time": 14.6
}
```
