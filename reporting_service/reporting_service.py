"""Service de génération de rapports et de tableau de bord avec SQLAlchemy."""

import logging
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from shared_data.models import Produit, Vente
from sqlalchemy.sql import func, text

logging.basicConfig(
    level=logging.INFO,  # Change à DEBUG ou ERROR selon les besoins
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class ReportingService:
    """Service fournissant des rapports de ventes et de stock."""

    def __init__(self, dao):
        """Initialise le service avec un accès DAO."""
        self.dao = dao

    def afficher_tableau_de_bord(self):
        """Affiche un résumé des ventes par magasin."""
        ventes = self.dao.get_ventes_par_magasin()

        if not ventes:
            print("Aucune vente enregistrée.")
            logger.warning("Aucune vente enregistrée.")
            return

        print("\n=== Ventes par magasin ===")
        for magasin, total in ventes.items():
            print(f"Magasin {magasin}: {total} ventes")
        logger.info("Affichage du tableau de bord des ventes par magasin.")

    def rapport_ventes(self):
        """Retourne la liste des ventes groupées par magasin et produit."""
        session: Session = self.dao.session
        resultats = session.query(
            Vente.magasin_id,
            Vente.produit_id,
            func.sum(Vente.quantite).label("total_vendu")
        ).group_by(Vente.magasin_id, Vente.produit_id).all()

        logger.info("Génération du rapport des ventes par magasin et produit.")
        return [
            {
                "magasin_id": r.magasin_id,
                "produit_id": r.produit_id,
                "total_vendu": r.total_vendu
            }
            for r in resultats
        ]

    def produits_en_rupture(self, seuil=5):
        """Retourne les produits dont le stock est inférieur ou égal au seuil."""
        session: Session = self.dao.session
        produits = session.query(Produit).filter(Produit.quantite <= seuil).all()
        logger.info(f"Récupération des produits en rupture de stock (seuil: {seuil}).")
        return [p.__dict__ for p in produits]

    def generer_tableau_de_bord(self):
        """Retourne le tableau de bord consolidé sous forme de dictionnaire."""
        session: Session = self.dao.session

        # Rapport des ventes
        ventes = session.query(
            Produit.id,
            Produit.nom,
            Produit.magasin_id,
            func.sum(Vente.quantite * Produit.prix).label("chiffre_affaires"),
            func.sum(Vente.quantite).label("ventes"),
            Produit.prix,
            Produit.categorie
        ).join(
            Produit,
            (Vente.produit_id == Produit.id) &
            (Vente.magasin_id == Produit.magasin_id)
        ).group_by(Produit.id, Produit.magasin_id).all()

        ventes_list = [
            {
                "produit_id": v.id,
                "nom": v.nom,
                "magasin_id": v.magasin_id,
                "ventes": v.ventes,
                "chiffre_affaires": float(v.chiffre_affaires),
                "prix": float(v.prix),
                "categorie": v.categorie,
            } for v in ventes
        ]

        ruptures = session.query(Produit).filter(Produit.quantite <= 0).all()
        ruptures_list = [
            {
                "produit_id": p.id,
                "nom": p.nom,
                "magasin_id": p.magasin_id
            } for p in ruptures
        ]

        surplus = session.query(Produit).filter(Produit.quantite > 30).all()
        surplus_list = [
            {
                "produit_id": p.id,
                "nom": p.nom,
                "magasin_id": p.magasin_id,
                "quantite": p.quantite
            } for p in surplus
        ]

        chiffre_affaires_total = session.query(
            func.sum(Vente.quantite * Produit.prix)
        ).join(
            Produit,
            (Vente.produit_id == Produit.id) &
            (Vente.magasin_id == Produit.magasin_id)
        ).scalar() or 0

        tendances = session.query(
            func.to_char(Vente.timestamp, 'IYYY-IW').label("semaine"),
            Vente.produit_id,
            func.sum(Vente.quantite).label("total_hebdo")
        ).group_by(
            text("semaine"), Vente.produit_id
        ).order_by(
            text("semaine DESC")
        ).limit(10).all()

        tendances_list = [
            {
                "semaine": ligne.semaine,
                "produit_id": ligne.produit_id,
                "total_hebdo": ligne.total_hebdo
            } for ligne in tendances
        ]

        logger.info("Génération du tableau de bord consolidé.")

        return {
            "ventes": ventes_list,
            "ruptures": ruptures_list,
            "surplus": surplus_list,
            "chiffre_affaires_total": float(chiffre_affaires_total),
            "tendances_hebdomadaires": tendances_list
        }


    def get_out_of_stock(self):
        """Retourne la liste des produits dont la quantité est à zéro."""
        logger.info("Récupération des produits en rupture de stock (quantité = 0).")
        return self.dao.session.query(Produit).filter(Produit.quantite == 0).all()
