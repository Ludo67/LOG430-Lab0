"""Service de gestion des opérations sur le stock avec SQLAlchemy."""
import logging
from sqlalchemy.orm import Session
from data_access_layer.product_dao import ProduitDAO
from data_access_layer.models import Produit, Vente

logging.basicConfig(
    level=logging.INFO,  # Change à DEBUG ou ERROR selon les besoins
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class StockService:
    """Service permettant la gestion des produits en stock et des ventes."""

    def __init__(self, dao: ProduitDAO):
        """Initialise le service avec un DAO de produit."""
        self.dao = dao
        self.session: Session = dao.session

    def rechercher_produit(self, terme: str):
        """Recherche un produit par mot-clé."""
        logger.info(f"Recherche de produit avec le terme: {terme}")
        return self.dao.rechercher(terme)

    def enregistrer_vente(self, produit_id: int, quantite: int, magasin_id: int):
        """Enregistre une vente en décrémentant le stock et en loguant l'opération."""
        produit = self.dao.get_by_id(produit_id, magasin_id)
        if not produit:
            logger.error(f"Produit ID {produit_id} introuvable dans le magasin ID {magasin_id}.")
            raise ValueError("Produit introuvable")

        if produit.quantite < quantite:
            logger.error(f"Stock insuffisant pour le produit ID {produit_id} dans le magasin ID {magasin_id}.")
            raise ValueError("Stock insuffisant")

        produit.quantite -= quantite
        logger.info(f"Vente enregistrée pour le produit ID {produit_id}, quantité: {quantite}, magasin ID: {magasin_id}.")
        self.dao.update(produit)
        self._log_vente(produit_id, quantite, magasin_id)

    def mettre_a_jour_produit(self, produit_id: int, magasin_id: int, champs: dict):
        produit = self.dao.update_product(produit_id, magasin_id, champs)
        if not produit:
            logger.error(f"Produit ID {produit_id} introuvable dans le magasin ID {magasin_id}.")
            raise ValueError("Produit introuvable")
        logger.info(f"Produit ID {produit_id} mis à jour dans le magasin ID {magasin_id}.")
        return produit

    def ajouter_produit(self, id: int, nom: str, categorie: str, quantite: int, prix: float, magasin_id: int):
        if self.dao.get_by_id(id, magasin_id):
            logger.error(f"Produit ID {id} déjà existant dans le magasin ID {magasin_id}.")
            raise ValueError("Produit déjà existant")

        logger.info(f"Ajout du produit ID {id} dans le magasin ID {magasin_id}.")
        nouveau = Produit(id=id, nom=nom, categorie=categorie, quantite=quantite, prix=prix, magasin_id=magasin_id)
        self.dao.insert(nouveau)

    def annuler_vente(self, produit_id: int, quantite: int, magasin_id: int):
        """Annule une vente en restaurant le stock du produit."""
        produit = self.dao.get_by_id(produit_id, magasin_id)
        if not produit:
            logger.error(f"Produit ID {produit_id} introuvable dans le magasin ID {magasin_id}.")
            raise ValueError("Produit introuvable")

        produit.quantite += quantite
        logger.info(f"Annulation de vente pour le produit ID {produit_id}, quantité: {quantite}, magasin ID: {magasin_id}.")
        self.dao.update(produit)

    def lister_stock(self):
        """Retourne tous les produits en stock."""
        logger.info("Récupération de tous les produits en stock.")
        return self.session.query(Produit).filter(Produit.quantite > 0).all()

    def _log_vente(self, produit_id: int, quantite: int, magasin_id: int):
        """Ajoute une entrée de vente dans la base de données."""
        vente = Vente(produit_id=produit_id, quantite=quantite, magasin_id=magasin_id)
        logger.info(f"Enregistrement de la vente: produit ID {produit_id}, quantité {quantite}, magasin ID {magasin_id}.")
        self.session.add(vente)
        self.session.commit()
