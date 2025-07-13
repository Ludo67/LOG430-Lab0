from fastapi.testclient import TestClient
from presentation_layer.main import app

client = TestClient(app)
API_KEY = "topsecret123"
HEADERS = {"X-API-Key": API_KEY}

def test_get_all_stock():
    response = client.get("/stock/", headers=HEADERS)
    assert response.status_code == 200

def test_get_stock_par_magasin():
    response = client.get("/stock/stock_par_magasin", params={"magasin_id": 1}, headers=HEADERS)
    assert response.status_code in (200, 404)

def test_rechercher_produit():
    response = client.get("/stock/rechercher", params={"terme": "test"}, headers=HEADERS)
    assert response.status_code == 200

def test_enregistrer_vente():
    test_annuler_vente()  # Assure we start with a clean slate
    response = client.post("/stock/vente", json={
        "produit_id": "1",
        "quantite": 1,
        "magasin_id": 1
    }, headers=HEADERS)
    assert response.status_code in (200, 400)

def test_annuler_vente():
    response = client.post("/stock/annulation", json={
        "produit_id": "1",
        "quantite": 1,
        "magasin_id": 1
    }, headers=HEADERS)
    assert response.status_code in (200, 400)

def test_reapprovisionnement():
    response = client.post("/restock/transferer", json={
        "produit_id": "1",
        "quantite": 1,
        "magasin_source": "1",
        "magasin_destination": "2"
    }, headers=HEADERS)
    assert response.status_code in (200, 400)

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

# def test_maj_produits():
#     client.post("/stock/annuler_vente", json={
#         "produit_id": "1",
#         "quantite": 1,
#         "magasin_id": 1
#     }, headers=HEADERS)

#     response = client.put(
#         "/stock/1/magasin/1",
#         json={"quantite": 50, "prix": 49.99},
#         headers=HEADERS
#     )

#     assert response.status_code == 200
