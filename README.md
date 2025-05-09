# Route Optimizer API

A Flask-based web service that computes the shortest “greedy” route through multiple waypoints and provides a traffic-aware ETA, returning human-readable street names for each waypoint. Ideal for backend-focused portfolios, this project demonstrates:

* Graph algorithms (Haversine + nearest-neighbor heuristic)
* Simple traffic modeling (rush-hour & congestion)
* Reverse geocoding to map coordinates to street names (using Geopy/Nominatim)
* ETA formatting (hours, minutes, seconds)
* Performance instrumentation (timing, CPU & memory via `psutil`)
* Input validation and error handling
* Full test coverage with `pytest`
* One-click deploy on Render / Railway / Fly.io

---

## 🛠️ Technologies & Tools

* **Languages**: Python
* **Frameworks**: Flask
* **Libraries & Tools**:

  * `psutil` for performance metrics
  * `pytest` for testing
  * `geopy` for reverse geocoding
  * `gunicorn` for deployment
* **APIs & Services**: OpenStreetMap Nominatim via Geopy
* **Hosting**: Render
* **Algorithms**: Haversine formula, Nearest-neighbor heuristic

---

## 🚀 Features

* **`/optimize`** endpoint accepts JSON payload:

  * **`origin`**: `[lat, lon]`
  * **`destinations`**: `[[lat, lon], …]`
  * **`time_of_day`**: hour in 24h (e.g. `8.5` = 8:30 AM)
  * **`traffic_level`**: integer `0–3`
* **Reverse Geocoding**: Converts each coordinate into a street name or address using Geopy’s Nominatim (OpenStreetMap). Rate-limited to 1 request/sec to respect API usage.
* **Nearest-neighbor routing** using Haversine great-circle distance
* **ETA calculation** at 50 km/h base, scaled by:

  * Rush-hour × 1.5 (7–9 AM & 4–6 PM)
  * +10% per congestion level
* **ETA Formatting**: Converts minutes into a readable string format: `H h M m S s`.
* **Performance Logging** via `psutil`:

  * Execution time (s)
  * ΔCPU % & ΔMemory (KiB)
* **Input Validation**: Ensures correct JSON structure, returns HTTP 400 with error details.
* **Health Check** endpoint (`/`)

---

## 📦 Integration & Usage

### Local Setup

```bash
git clone git@github.com:<your-username>/route-optimizer.git
cd route-optimizer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Dependencies

* All core dependencies in `requirements.txt` including:

  ```
  Flask
  psutil
  pytest
  geopy
  gunicorn
  ```

---

## 🏃 Running Locally

```bash
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
    "Market Street",
    "Grant Avenue",
    "Van Ness Avenue"
  ],
  "estimated_time": "0 h 14 m 36 s"
}
```

---

## 🔍 Testing

```bash
export PYTHONPATH=.
pytest --maxfail=1 --disable-warnings -q
```

Expected:

```
4 passed in 0.06s
```

---

## 📊 Performance Logging

Live log sample:

```
2025-05-08 12:34:56 INFO Optimize: 0.023s | ΔCPU: 2.1% | ΔMem: 512.0KiB
```

---

## ☁️ Deployment

### Deploy on Render

1. Connect the GitHub repo.
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn run:app --workers 2 --bind 0.0.0.0:$PORT`

### Smoke Test

```bash
curl -X POST https://<your-app>.onrender.com/optimize \
  -H 'Content-Type: application/json' \
  -d '{"origin":[37.77,-122.42],"destinations":[[37.78,-122.43]],"time_of_day":12,"traffic_level":1}'
```