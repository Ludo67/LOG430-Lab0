"""Tests unitaires pour StockService."""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_access_layer.models import Base, Produit
from data_access_layer.product_dao import ProduitDAO
from service_layer.stock_service import StockService


class TestStockService(unittest.TestCase):
    """Tests pour les opérations métiers de gestion de stock."""

    def setUp(self):
        """Initialise une base SQLite en mémoire avec un produit de test."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        session_cls = sessionmaker(bind=engine)
        self.session = session_cls()

        # DAO et service
        self.dao = ProduitDAO(self.session)
        self.service = StockService(self.dao)

        # Produit de test
        produit = Produit(
            id="S001",
            nom="ServiceProduit",
            categorie="Test",
            prix=20.0,
            quantite=10,
            magasin_id=1,
        )
        self.session.add(produit)
        self.session.commit()

    def tearDown(self):
        """Ferme la session SQLAlchemy après chaque test."""
        self.session.close()

    def test_enregistrement_vente(self):
        """Vérifie que la vente diminue correctement le stock."""
        self.service.enregistrer_vente("S001", 3, 1)
        produit = self.dao.get_by_id("S001", 1)
        self.assertEqual(produit.quantite, 7)

    def test_annulation_vente(self):
        """Vérifie que l'annulation d'une vente augmente la quantité en stock."""
        self.service.annuler_vente("S001", 2, 1)
        produit = self.dao.get_by_id("S001", 1)
        self.assertEqual(produit.quantite, 12)

    def test_vente_stock_insuffisant(self):
        """Doit lever une exception si la quantité demandée dépasse le stock."""
        with self.assertRaises(ValueError):
            self.service.enregistrer_vente("S001", 999, 1)

    def test_recherche_service(self):
        """Doit retrouver un produit via une recherche par mot-clé."""
        resultats = self.service.rechercher_produit("Service")
        self.assertTrue(any("Service" in p.nom for p in resultats))


if __name__ == "__main__":
    unittest.main()
