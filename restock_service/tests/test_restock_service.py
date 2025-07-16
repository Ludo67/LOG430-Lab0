"""Tests unitaires pour RestockService."""
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared_data.models import Base, Produit
from shared_data.product_dao import ProduitDAO
from restock_service import RestockService


class TestRestockService(unittest.TestCase):
    """Tests pour le service de réapprovisionnement."""

    def setUp(self):
        """Prépare la base de données et les objets requis."""
        engine = create_engine("sqlite:///:memory:")
        session_cls = sessionmaker(bind=engine)
        self.session = session_cls()
        Base.metadata.create_all(engine)

        # Produit existant dans le magasin source seulement
        produit = Produit(
            id=1,
            nom="Clavier",
            categorie="Informatique",
            prix=50.0,
            quantite=10,
            magasin_id=1,
        )
        self.session.add(produit)
        self.session.commit()

        self.dao = ProduitDAO(self.session)
        self.service = RestockService(self.dao)

    def test_transferer_stock(self):
        """Teste un transfert de stock avec création d’un nouveau produit."""
        self.service.transferer_stock(
            produit_id=1,
            quantite=5,
            magasin_source=1,
            magasin_cible=2
        )
        source = self.session.query(Produit).filter_by(id=1, magasin_id=1).first()
        cible = self.session.query(Produit).filter_by(id=1, magasin_id=2).first()

        self.assertEqual(source.quantite, 5)
        self.assertIsNotNone(cible)
        self.assertEqual(cible.quantite, 5)
        self.assertEqual(cible.nom, "Clavier")

    def tearDown(self):
        """Ferme la session SQLAlchemy après chaque test."""
        self.session.close()
