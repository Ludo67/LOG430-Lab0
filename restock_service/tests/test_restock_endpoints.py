from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
API_KEY = "topsecret123"
HEADERS = {"X-API-Key": API_KEY}

def test_reapprovisionnement():
    response = client.post("/restock/transferer", json={
        "produit_id": "1",
        "quantite": 1,
        "magasin_source": "1",
        "magasin_destination": "2"
    }, headers=HEADERS)
    assert response.status_code in (200, 400)
