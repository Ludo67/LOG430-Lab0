"""Tests unitaires pour ProduitDAO."""

import unittest
from data_access_layer.product_dao import ProduitDAO

class TestProduitDAO(unittest.TestCase):
    """Tests pour les opérations DAO sur les produits."""

    def setUp(self):
        """Initialise une base en mémoire et vide la table."""
        self.dao = ProduitDAO(":memory:")

    def test_insertion_et_recuperation(self):
        """Vérifie qu'un produit inséré peut être récupéré."""
        produit = {
            "id": "T001",
            "nom": "Test Produit",
            "categorie": "Test",
            "prix": 10.0,
            "quantite": 5
        }
        self.dao.update(produit)
        resultat = self.dao.get_by_id("T001")
        self.assertEqual(resultat["nom"], "Test Produit")

    def test_recherche(self):
        """Vérifie qu'un produit peut être retrouvé par mot-clé."""
        self.dao.update({
            "id": "T002", "nom": "Souris Test", "categorie": "Périphérique",
            "prix": 15.0, "quantite": 10
        })
        resultats = self.dao.rechercher("souris")
        self.assertTrue(any("Souris" in r["nom"] for r in resultats))

    def test_structure_base(self):
        """Vérifie que la table produits existe bien."""
        tables = self.dao.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='produits'"
        ).fetchall()
        self.assertEqual(len(tables), 1)

    def tearDown(self):
        """Ferme la connexion après les tests."""
        self.dao.close()
