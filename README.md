# Route Optimizer API

A Flask-based web service that computes the shortest “greedy” route through multiple waypoints and provides a traffic-aware ETA. Ideal for backend-focused portfolios, this project demonstrates:

- Graph algorithms (Haversine + nearest-neighbor heuristic)  
- Simple traffic modeling (rush-hour & congestion)  
- Performance instrumentation (timing, CPU & memory via `psutil`)  
- Full test coverage with `pytest`  
- One-click deploy on Render / Railway / Fly.io  

---

## 🗂️ Repository Structure

```text
route-optimizer/
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── routes.py         # HTTP routes & logging
│   ├── optimizer.py      # Distance, traffic & optimization logic
├── tests/
│   ├── test_optimizer.py # Unit tests for core logic
│   └── test_api.py       # Endpoint integration tests
├── run.py                # App entrypoint
├── requirements.txt      # Python dependencies
├── pytest.ini            # pytest configuration
└── README.md             # ← You are here
