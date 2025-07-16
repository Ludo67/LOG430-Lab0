import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared_data.models import Base, Panier, ProduitPanier
from shared_data.cart_dao import CartDAO

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_insert_panier_et_produits(session):
    dao = CartDAO(session)

    panier = Panier(client_id=1)
    panier = dao.creer_panier(panier)

    produit1 = ProduitPanier(produit_id=1, magasin_id=1, quantite=2)
    produit2 = ProduitPanier(produit_id=2, magasin_id=1, quantite=1)
    dao.ajouter_produit(panier, produit1)
    dao.ajouter_produit(panier, produit2)

    result = dao.get_panier(panier.id)
    assert result is not None
    assert len(result.produits_associes) == 2
    assert result.produits_associes[0].quantite == 2
    assert result.produits_associes[1].quantite == 1

