import math

def haversine(coord1, coord2):
    """Great-circle distance in km."""
    R = 6371  # Earth radius (km)
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def traffic_multiplier(time_of_day, traffic_level):
    """
    Simple model:
      – rush hours (7-9 & 16-18) = +50 % baseline
      – traffic_level 0-3 adds up to +30 %
    """
    rush = 1.5 if 7 <= time_of_day <= 9 or 16 <= time_of_day <= 18 else 1.0
    congestion = 1 + (traffic_level * 0.1)        # 0, 0.1, 0.2, 0.3
    return rush * congestion

def optimize_route(origin, destinations, time_of_day, traffic_level):
    # same nearest-neighbor logic
    unvisited = destinations[:]
    route = [origin]
    current = origin

    while unvisited:
        nearest = min(unvisited, key=lambda p: haversine(current, p))
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    # crude ETA: 50 km/h base speed, scaled by traffic multiplier
    total_km = sum(haversine(route[i], route[i+1]) for i in range(len(route)-1))
    multiplier = traffic_multiplier(time_of_day, traffic_level)
    eta_hours = (total_km / 50) * multiplier
    eta_min    = round(eta_hours * 60, 1)
    return route, eta_min    # ← TWO values
