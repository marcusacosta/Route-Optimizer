import time
import logging
import psutil
from flask import Blueprint, request, jsonify
from .utils import validate_payload
from .optimizer import optimize_route

# Blueprint for optimizer routes
optimizer_bp = Blueprint("optimizer", __name__)

@optimizer_bp.route("/", methods=["GET"])
def home():
    """Simple health check endpoint."""
    return "Flask is working!"

@optimizer_bp.route("/optimize", methods=["POST"])
def optimize_route_api():
    """
    Endpoint to compute optimized route and ETA.

    Logs performance metrics (execution time, CPU and memory deltas).
    Validates input payload using utils.validate_payload.
    """
    # Start performance measurement
    start_ts = time.time()
    proc = psutil.Process()
    cpu_before = proc.cpu_percent(interval=None)
    mem_before = proc.memory_info().rss

    # Parse and validate request payload
    data = request.get_json()
    try:
        validate_payload(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    origin = data["origin"]
    destinations = data["destinations"]
    time_of_day = data["time_of_day"]
    traffic_level = data["traffic_level"]

    # Run optimization logic
    route, eta = optimize_route(origin, destinations, time_of_day, traffic_level)

    # Measure performance after computation
    cpu_after = proc.cpu_percent(interval=None)
    mem_after = proc.memory_info().rss
    elapsed = time.time() - start_ts

    # Log performance metrics
    logging.info(
        "Optimize: %.3fs | ΔCPU: %.1f%% | ΔMem: %.1fKiB",
        elapsed,
        cpu_after - cpu_before,
        (mem_after - mem_before) / 1024,
    )

    # Return JSON response
    return jsonify({
        "optimized_route": route,
        "estimated_time": eta
    })
