"""remplissage de la base de données avec des données d'exemple."""
from datetime import datetime
from data_access_layer.database import SessionLocal
from data_access_layer.models import Produit, Vente

# Données exemples
produits = [
    Produit(id=1, nom="Clavier", categorie="Informatique", prix=39.99, quantite=15, magasin_id=1),
    Produit(id=2, nom="Souris", categorie="Informatique", prix=19.99, quantite=25, magasin_id=1),
    Produit(id=3, nom="Écran", categorie="Informatique", prix=129.99, quantite=10, magasin_id=2),
    Produit(id=4, nom="Stylo", categorie="Papeterie", prix=1.99, quantite=100, magasin_id=2),
    Produit(id=5, nom="Cahier", categorie="Papeterie", prix=4.50, quantite=50, magasin_id=1),
]

ventes = [
    Vente(produit_id=1, quantite=2, magasin_id=1, timestamp=datetime.now()),
    Vente(produit_id=2, quantite=5, magasin_id=1, timestamp=datetime.now()),
    Vente(produit_id=3, quantite=1, magasin_id=2, timestamp=datetime.now()),
    Vente(produit_id=5, quantite=10, magasin_id=1, timestamp=datetime.now()),
]

def seed():
    """Remplit la DB avec des données d'exemple."""
    session = SessionLocal()
    session.query(Produit).delete()
    session.query(Vente).delete()
    session.commit()
    session.add_all(produits)
    session.add_all(ventes)
    session.commit()
    session.close()
    print("✅ Données insérées avec succès.")

if __name__ == "__main__":
    seed()
