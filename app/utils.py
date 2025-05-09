
import math

def haversine(coord1, coord2):
    """Great-circle distance between two (lat, lon) points in km."""
    R = 6371
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def traffic_multiplier(time_of_day, traffic_level):
    """Compute a rush-hour + congestion multiplier."""
    rush  = 1.5 if 7 <= time_of_day <= 9 or 16 <= time_of_day <= 18 else 1.0
    extra = 1 + traffic_level * 0.1
    return rush * extra

def validate_payload(data):
    """Ensure required keys are present and types look right."""
    required = ("origin", "destinations", "time_of_day", "traffic_level")
    for key in required:
        if key not in data:
            raise ValueError(f"Missing '{key}' in request JSON")
    if (not isinstance(data["destinations"], list) or
        not all(isinstance(pt, list) and len(pt)==2 for pt in data["destinations"])):
        raise ValueError("‘destinations’ must be a list of [lat, lon] pairs")
    # you can add more checks here…
