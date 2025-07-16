"""Tests unitaires pour ReportingService."""
import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared_data.models import Base, Produit, Vente
from shared_data.product_dao import ProduitDAO
from reporting_service import ReportingService


class TestReportingService(unittest.TestCase):
    """Tests pour le service de reporting."""

    def setUp(self):
        """Crée une base SQLite en mémoire avec des produits et ventes."""
        engine = create_engine("sqlite:///:memory:")
        session_cls = sessionmaker(bind=engine)
        self.session = session_cls()
        Base.metadata.create_all(engine)

        # DAO et Service
        self.dao = ProduitDAO(self.session)
        self.service = ReportingService(self.dao)

        # Données de test
        produit = Produit(
            id=1,
            nom="Clavier",
            categorie="Informatique",
            prix=50.0,
            quantite=10,
            magasin_id=1,
        )
        vente = Vente(
            produit_id=1,
            magasin_id=1,
            quantite=3,
            timestamp=datetime.now(),
        )

        self.session.add(produit)
        self.session.add(vente)
        self.session.commit()

    def tearDown(self):
        """Ferme la session SQLAlchemy après chaque test."""
        self.session.close()

    def test_rapport_ventes(self):
        """Vérifie que le rapport de ventes retourne les bons agrégats."""
        resultats = self.service.rapport_ventes()
        self.assertEqual(len(resultats), 1)
        self.assertEqual(resultats[0]["total_vendu"], 3)

    def test_produits_en_rupture(self):
        """Vérifie la détection de rupture de stock."""
        self.session.query(Produit).filter_by(id=1).update({"quantite": 0})
        self.session.commit()
        ruptures = self.service.produits_en_rupture(seuil=0)
        self.assertTrue(any(p["id"] == 1 for p in ruptures))

if __name__ == "__main__":
    unittest.main()
