from flask import Blueprint, request, jsonify
import time, logging, psutil
from .utils import validate_payload, format_eta, reverse_geocode
from .optimizer import optimize_route

optimizer_bp = Blueprint("optimizer", __name__)

@optimizer_bp.route("/", methods=["GET"])
def home():
    return "Flask is working!"

@optimizer_bp.route("/optimize", methods=["POST"])
def optimize_route_api():
    start_ts = time.time()
    proc     = psutil.Process()
    cpu_b    = proc.cpu_percent(None)
    mem_b    = proc.memory_info().rss

    data = request.get_json()
    try:
        validate_payload(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    origin       = data["origin"]
    destinations = data["destinations"]
    tod          = data["time_of_day"]
    lvl          = data["traffic_level"]

    coords_route, eta_min = optimize_route(origin, destinations, tod, lvl)

    # convert coords to street names
    named_route = [ reverse_geocode(pt) for pt in coords_route ]

    cpu_a   = proc.cpu_percent(None)
    mem_a   = proc.memory_info().rss
    elapsed = time.time() - start_ts
    logging.info("Optimize: %.3fs | ΔCPU: %.1f%% | ΔMem: %.1fKiB",
                 elapsed, cpu_a - cpu_b, (mem_a - mem_b)/1024)

    return jsonify({
      "optimized_route": named_route,
      "estimated_time": format_eta(eta_min)
    })
