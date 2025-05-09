import math
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# set up a free OpenStreetMap geocoder
_geolocator = Nominatim(user_agent="route_optimizer")
_reverse = RateLimiter(_geolocator.reverse, min_delay_seconds=1)

def haversine(coord1, coord2):
    """Great-circle distance between two (lat, lon) points in km."""
    R = 6371
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def traffic_multiplier(time_of_day, traffic_level):
    """Compute rush-hour + congestion multiplier."""
    rush  = 1.5 if 7 <= time_of_day <= 9 or 16 <= time_of_day <= 18 else 1.0
    extra = 1 + (traffic_level * 0.1)
    return rush * extra

def format_eta(eta_min: float) -> str:
    """Convert minutes (float) to H h M m S s."""
    total_seconds = int(eta_min * 60)
    h, rem = divmod(total_seconds, 3600)
    m, s   = divmod(rem, 60)
    parts = []
    if h: parts.append(f"{h} h")
    if m: parts.append(f"{m} m")
    if s or not parts: parts.append(f"{s} s")
    return " ".join(parts)

def reverse_geocode(coord: list|tuple) -> str:
    """
    Turn (lat, lon) into a human-readable address.
    Caches at 1 request/sec to avoid OSM rate limits.
    """
    location = _reverse(coord, exactly_one=True, timeout=10)
    # pick the road/highway component if available
    if location and 'road' in location.raw['address']:
        return location.raw['address']['road']
    return location.address or f"{coord[0]}, {coord[1]}"
