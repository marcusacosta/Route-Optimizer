"""
Optimizer module for calculating routes and ETAs.
"""

from .utils import haversine, traffic_multiplier


def optimize_route(origin, destinations, time_of_day, traffic_level):
    # Copy the destinations list so we don't modify the original
    unvisited = destinations[:]
    route = [origin]
    current = origin

    # Greedy nearest-neighbor algorithm
    while unvisited:
        nearest = min(unvisited, key=lambda p: haversine(current, p))
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    # Calculate total distance
    total_km = sum(
        haversine(route[i], route[i + 1])
        for i in range(len(route) - 1)
    )

    # Apply traffic multiplier to compute ETA
    multiplier = traffic_multiplier(time_of_day, traffic_level)
    eta_hours = (total_km / 50.0) * multiplier  # base speed 50 km/h
    eta_min = round(eta_hours * 60, 1)

    return route, eta_min
