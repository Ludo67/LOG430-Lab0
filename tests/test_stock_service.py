"""Tests unitaires pour StockService."""
import unittest
from service_layer.stock_service import StockService
from data_access_layer.product_dao import ProduitDAO


class TestStockService(unittest.TestCase):
    """Tests pour les opérations métiers de gestion de stock."""

    def setUp(self):
        """Prépare un DAO mémoire et un StockService avec un produit test."""
        self.dao = ProduitDAO(":memory:")
        self.service = StockService(self.dao)
        self.dao.update({
            "id": "S001", "nom": "ServiceProduit", "categorie": "Test",
            "prix": 20.0, "quantite": 10
        })

    def test_enregistrement_vente(self):
        """Vérifie que la vente diminue correctement le stock."""
        self.service.enregistrer_vente("S001", 3)
        produit = self.dao.get_by_id("S001")
        self.assertEqual(produit["quantite"], 7)

    def test_annulation_vente(self):
        """Vérifie que l'annulation d'une vente augmente la quantité en stock."""
        self.service.annuler_vente("S001", 2)
        produit = self.dao.get_by_id("S001")
        self.assertEqual(produit["quantite"], 12)

    def test_vente_stock_insuffisant(self):
        """Doit lever une exception si la quantité demandée dépasse le stock."""
        with self.assertRaises(ValueError):
            self.service.enregistrer_vente("S001", 999)

    def test_recherche_service(self):
        """Doit retrouver un produit via une recherche par mot-clé."""
        resultats = self.service.rechercher_produit("Service")
        self.assertTrue(len(resultats) >= 1)

    def tearDown(self):
        """Ferme la connexion au DAO après chaque test."""
        self.dao.close()
