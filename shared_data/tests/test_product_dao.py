"""Tests unitaires pour la couche d'accès aux données ProduitDAO."""
import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from shared_data.models import Base, Produit
from shared_data.product_dao import ProduitDAO


class TestProduitDAO(unittest.TestCase):
    """Tests pour les opérations DAO sur les produits."""

    def setUp(self):
        """Initialise une base SQLite en mémoire avec une session active."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        session_cls = sessionmaker(bind=engine)
        self.session = session_cls()
        self.dao = ProduitDAO(self.session)

    def tearDown(self):
        """Ferme la session SQLAlchemy après chaque test."""
        self.session.close()

    def test_insertion_et_recuperation(self):
        """Vérifie qu’un produit inséré peut être récupéré par son ID."""
        produit = Produit(
            id=1,
            nom="Test Produit",
            categorie="Test",
            prix=10.0,
            quantite=5,
            magasin_id=1
        )
        self.session.add(produit)
        self.session.commit()

        resultat = self.dao.get_by_id(1, 1)
        self.assertEqual(resultat.nom, "Test Produit")

    def test_recherche(self):
        """Vérifie qu’un produit peut être trouvé par mot-clé."""
        produit = Produit(
            id=2,
            nom="Souris Test",
            categorie="Périphérique",
            prix=15.0,
            quantite=10,
            magasin_id=1
        )
        self.session.add(produit)
        self.session.commit()

        resultats = self.dao.rechercher("souris")
        self.assertTrue(any("Souris" in r.nom for r in resultats))

    def test_structure_base(self):
        """Vérifie que la table 'produits' est bien créée."""
        table_names = self.session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='produits';")
        ).fetchall()
        self.assertEqual(len(table_names), 1)


if __name__ == "__main__":
    unittest.main()
