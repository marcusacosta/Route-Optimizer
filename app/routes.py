import time, psutil, logging
from flask import Blueprint, request, jsonify
from .optimizer import optimize_route

optimizer_bp = Blueprint("optimizer", __name__)

@optimizer_bp.route("/optimize", methods=["POST"])
def optimize_route_api():
    start_ts = time.time()
    proc      = psutil.Process()
    cpu_before= proc.cpu_percent(interval=None)
    mem_before= proc.memory_info().rss

    data       = request.get_json()
    origin     = data["origin"]
    destinations = data["destinations"]
    tod        = data["time_of_day"]
    lvl        = data["traffic_level"]

    route, eta = optimize_route(origin, destinations, tod, lvl)

    cpu_after  = proc.cpu_percent(interval=None)
    mem_after  = proc.memory_info().rss
    elapsed    = time.time() - start_ts

    logging.info(
        "Optimize: %.3fs | ΔCPU: %.1f%% | ΔMem: %.1fKiB",
        elapsed,
        cpu_after - cpu_before,
        (mem_after - mem_before) / 1024,
    )

    return jsonify({"optimized_route": route, "estimated_time": eta})
