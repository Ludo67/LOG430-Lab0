from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
API_KEY = "topsecret123"
HEADERS = {"X-API-Key": API_KEY}

def test_get_rapport_ventes():
    response = client.get("/reporting/ventes", headers=HEADERS)
    assert response.status_code == 200

def test_get_ruptures():
    response = client.get("/reporting/ruptures", headers=HEADERS)
    assert response.status_code == 200

def test_get_dashboard():
    with TestClient(app) as client:
        response = client.get("/reporting/dashboard", headers=HEADERS)
        assert response.status_code == 200