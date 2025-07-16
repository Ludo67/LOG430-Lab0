from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
API_KEY = "topsecret123"
HEADERS = {"X-API-Key": API_KEY}

def test_create_client():
    payload = {
        "id": 1,
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@example.com",
        "adresse": "123 Rue Exemple"
    }

    response = client.post("/clients/", json=payload, headers=HEADERS)

    assert response.status_code == 201
    data = response.json()

    assert data["id"] == 1
    assert data["nom"] == "Dupont"
    assert data["prenom"] == "Jean"
    assert data["email"] == "jean.dupont@example.com"
    assert data["adresse"] == "123 Rue Exemple"
    assert "id" in data and isinstance(data["id"], int)
