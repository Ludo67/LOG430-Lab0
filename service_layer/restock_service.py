"""Service de gestion du réapprovisionnement entre magasins."""

from sqlalchemy.orm import Session
from data_access_layer.product_dao import ProduitDAO
from data_access_layer.models import Produit


class RestockService:
    """Service permettant le transfert de stock entre magasins."""

    def __init__(self, dao: ProduitDAO):
        """Initialise le service avec un DAO de produit."""
        self.dao = dao
        self.session: Session = dao.session

    def get_stock_par_magasin(self, magasin_id: int):
        """Retourne les produits d'un magasin donné."""
        return self.session.query(Produit).filter_by(magasin_id=magasin_id).all()

    def transferer_stock(
        self,
        produit_id: int,
        quantite: int,
        magasin_source: int,
        magasin_cible: int
    ):
        """
        Transfère une quantité d'un produit d'un magasin source vers un magasin cible.

        Args:
            produit_id (int): Identifiant du produit.
            quantite (int): Quantité à transférer.
            magasin_source (int): ID du magasin source.
            magasin_cible (int): ID du magasin cible.

        Raises:
            ValueError: Si le stock est insuffisant dans le magasin source.
        """
        source = self.session.query(Produit).filter_by(
            id=produit_id, magasin_id=magasin_source
        ).first()

        if not source or source.quantite < quantite:
            raise ValueError("Stock insuffisant dans le magasin source")

        # Décrémenter le stock du magasin source
        source.quantite -= quantite

        # Ajouter au stock du magasin cible
        cible = self.session.query(Produit).filter_by(
            id=produit_id, magasin_id=magasin_cible
        ).first()

        if cible:
            cible.quantite += quantite
        else:
            nouveau_produit = Produit(
                id=source.id,
                magasin_id=magasin_cible,
                nom=source.nom,
                categorie=source.categorie or "Inconnue",
                prix=source.prix,
                quantite=quantite,
            )
            self.session.add(nouveau_produit)

        self.session.commit()
