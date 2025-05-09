import pytest
from app.optimizer import haversine, traffic_multiplier, optimize_route

def test_haversine_zero():
    # same point → distance 0
    assert haversine((0,0), (0,0)) == pytest.approx(0.0)

def test_traffic_multiplier_rush():
    # during rush hour + traffic_level 2
    m = traffic_multiplier(8, 2)
    # rush 1.5 × (1 + 0.2) = 1.8
    assert m == pytest.approx(1.8)

def test_optimize_route_returns_two_values():
    origin = (0,0)
    dests  = [(0,1), (1,0)]
    route, eta = optimize_route(origin, dests, time_of_day=0, traffic_level=0)
    assert isinstance(route, list) and isinstance(eta, float)
    assert route[0] == origin
    assert set(route[1:]) == set(dests)
    assert eta >= 0
