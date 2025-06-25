"""Service de génération de rapports et de tableau de bord avec SQLAlchemy."""

from sqlalchemy import func, text
from sqlalchemy.orm import Session
from data_access_layer.models import Produit, Vente


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
            return

        print("\n=== Ventes par magasin ===")
        for magasin, total in ventes.items():
            print(f"Magasin {magasin}: {total} ventes")

    def rapport_ventes(self):
        """Retourne la liste des ventes groupées par magasin et produit."""
        session: Session = self.dao.session
        resultats = session.query(
            Vente.magasin_id,
            Vente.produit_id,
            func.sum(Vente.quantite).label("total_vendu")
        ).group_by(Vente.magasin_id, Vente.produit_id).all()

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
        return [p.__dict__ for p in produits]

    def generer_tableau_de_bord(self):
        """Affiche le tableau de bord complet avec plusieurs rapports."""
        session: Session = self.dao.session

        print("\n--- Rapport consolidé des ventes ---")
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

        for produit in ventes:
            print(
                f"[{produit.magasin_id}] {produit.nom} | "
                f"{produit.ventes} ventes | CA: {produit.chiffre_affaires:.2f} $"
            )

        print("\n--- Produits en rupture de stock ---")
        ruptures = session.query(Produit).filter(Produit.quantite <= 0).all()
        for produit in ruptures:
            print(f"[{produit.magasin_id}] {produit.nom} (id={produit.id})")

        print("\n--- Produits en surstock ---")
        surplus = session.query(Produit).filter(Produit.quantite > 30).all()
        for produit in surplus:
            print(f"[{produit.magasin_id}] {produit.nom} ({produit.quantite} en stock)")

        print("\n--- Chiffre d'affaires global ---")
        total = session.query(
            func.sum(Vente.quantite * Produit.prix)
        ).join(
            Produit,
            (Vente.produit_id == Produit.id) &
            (Vente.magasin_id == Produit.magasin_id)
        ).scalar() or 0
        print(f"\n💰 Chiffre d'affaires total : {total:.2f} $")

        print("\n--- Tendances hebdomadaires ---")
        tendances = session.query(
            func.strftime('%Y-%W', Vente.timestamp).label("semaine"),
            Vente.produit_id,
            func.sum(Vente.quantite).label("total_hebdo")
        ).group_by(
            text("semaine"), Vente.produit_id
        ).order_by(
            text("semaine DESC")
        ).limit(10).all()

        for ligne in tendances:
            print(
                f"Semaine {ligne.semaine} | Produit {ligne.produit_id} : "
                f"{ligne.total_hebdo} ventes"
            )

    def get_out_of_stock(self):
        """Retourne la liste des produits dont la quantité est à zéro."""
        return self.dao.session.query(Produit).filter(Produit.quantite == 0).all()
