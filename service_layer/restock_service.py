"""Service de gestion du réapprovisionnement entre magasins."""

import logging
from sqlalchemy.orm import Session
from data_access_layer.product_dao import ProduitDAO
from data_access_layer.models import Produit

logging.basicConfig(
    level=logging.INFO,  # Change à DEBUG ou ERROR selon les besoins
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class RestockService:
    """Service permettant le transfert de stock entre magasins."""

    def __init__(self, dao: ProduitDAO):
        """Initialise le service avec un DAO de produit."""
        self.dao = dao
        self.session: Session = dao.session

    def get_stock_par_magasin(self, magasin_id: int):
        """Retourne les produits d'un magasin donné."""
        logger.info(f"Récupération du stock pour le magasin ID: {magasin_id}")
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
            logger.error(f"Stock insuffisant pour le produit ID: {produit_id} dans le magasin ID: {magasin_source}")
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

        logger.info(f"Transfert de {quantite} unités du produit ID: {produit_id} du magasin ID: {magasin_source} vers le magasin ID: {magasin_cible}")
        self.session.commit()
