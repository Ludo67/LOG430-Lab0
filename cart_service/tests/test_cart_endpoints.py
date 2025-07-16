from fastapi.testclient import TestClient
from main import app
from shared_data.database import SessionLocal
from shared_data.models import Client, Produit

client = TestClient(app)
HEADERS = {"x-api-key": "topsecret123"}

def inserer_client_et_produits():
    """Ajoute un client et deux produits dans la base de données pour les tests."""
    session = SessionLocal()
    client_test = Client(
        id=3,
        nom="Testeur",
        prenom="Panier",
        email="panier@test.com",
        adresse="123 Test Rue"
    )

    produit_1 = Produit(id=1, nom="Produit A", prix=10.0, quantite=10, magasin_id=1, categorie="Informatique")
    produit_2 = Produit(id=2, nom="Produit B", prix=15.0, quantite=50, magasin_id=1, categorie="Informatique")

    session.merge(client_test) 
    session.merge(produit_1)
    session.merge(produit_2)
    session.commit()
    session.close()


def test_workflow_checkout_panier():
    inserer_client_et_produits()

    # Créer un panier
    response_panier = client.post("/panier/", json={"client_id": 3}, headers=HEADERS)
    assert response_panier.status_code == 201
    panier_id = response_panier.json()["id"]

    # Ajouter deux produits au panier
    produits = [
        {"id": 1, "magasin_id": 1, "quantite": 2},
        {"id": 2, "magasin_id": 1, "quantite": 1}
    ]
    for prod in produits:
        response_add = client.post(f"/panier/{panier_id}/produit", json=prod, headers=HEADERS)
        assert response_add.status_code == 200

    # Faire le checkout
    response_checkout = client.post(f"/panier/panier/{panier_id}/checkout", headers=HEADERS)
    assert response_checkout.status_code == 200