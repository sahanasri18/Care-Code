"""Hospitals module tests: seed, search, nearby, details."""
from app.services.hospital_seed import SEED_HOSPITALS

PASSWORD = "Str0ng!Pass"


def test_seed_data_present(client):
    resp = client.get("/api/v1/hospitals")
    assert resp.status_code == 200
    assert resp.json()["total"] == len(SEED_HOSPITALS)


def test_search_by_name(client):
    resp = client.get("/api/v1/hospitals", params={"q": "apollo"})
    assert resp.status_code == 200
    assert resp.json()["total"] >= 4
    for item in resp.json()["items"]:
        assert "apollo" in item["name"].lower()


def test_search_by_city(client):
    resp = client.get("/api/v1/hospitals", params={"city": "chennai"})
    assert resp.status_code == 200
    for item in resp.json()["items"]:
        assert item["city"].lower() == "chennai"


def test_pagination(client):
    resp = client.get("/api/v1/hospitals", params={"page": 1, "page_size": 5})
    body = resp.json()
    assert len(body["items"]) == 5
    assert body["page"] == 1
    assert body["page_size"] == 5


def test_cities_list(client):
    resp = client.get("/api/v1/hospitals/cities")
    assert resp.status_code == 200
    assert "Chennai" in resp.json()["cities"]


def test_states_list(client):
    resp = client.get("/api/v1/hospitals/states")
    assert resp.status_code == 200
    states = resp.json()["states"]
    assert len(states) >= 36
    for required in ["Tamil Nadu", "Kerala", "Delhi", "Manipur", "Lakshadweep"]:
        assert required in states


def test_filter_by_state(client):
    resp = client.get("/api/v1/hospitals", params={"state": "Tamil Nadu"})
    assert resp.status_code == 200
    assert resp.json()["total"] > 50
    for item in resp.json()["items"]:
        assert item["state"] == "Tamil Nadu"


def test_seed_has_all_states(client):
    resp = client.get("/api/v1/hospitals", params={"page_size": 1})
    assert resp.status_code == 200
    assert resp.json()["total"] > 400


def test_nearby_sorted_by_distance(client):
    # Bengaluru city centre (MG Road).
    resp = client.get("/api/v1/hospitals/nearby", params={"lat": 12.975, "lng": 77.604, "radius_km": 30})
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) > 0
    distances = [i["distance_km"] for i in items]
    assert distances == sorted(distances)
    assert all("distance_km" in i for i in items)


def test_nearby_faraway_radius_empty(client):
    resp = client.get("/api/v1/hospitals/nearby", params={"lat": 64.0, "lng": -21.0, "radius_km": 10})
    assert resp.status_code == 200
    assert resp.json() == []


def test_hospital_detail(client):
    hospital_id = client.get("/api/v1/hospitals", params={"page_size": 1}).json()["items"][0]["id"]
    resp = client.get(f"/api/v1/hospitals/{hospital_id}")
    assert resp.status_code == 200
    assert resp.json()["name"]
    assert resp.json()["departments"]


def test_hospital_detail_404(client):
    resp = client.get("/api/v1/hospitals/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


def test_hospitals_are_public(client):
    assert client.get("/api/v1/hospitals").status_code == 200
