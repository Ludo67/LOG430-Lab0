import logging
from shared_data.models import Panier, ProduitPanier
from datetime import datetime
from sqlalchemy.orm import Session
from shared_data.cart_dao import CartDAO

logging.basicConfig(
    level=logging.INFO,  # Change à DEBUG ou ERROR selon les besoins
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

class CartService:
    def __init__(self, dao: CartDAO):
        self.dao = dao
        self.session: Session = dao.session

    def creer_panier(self, client_id: int):
        """Crée un nouveau panier pour un client."""
        if self.dao.get_by_id(client_id):
            logger.error(f"Panier pour le client ID {client_id} déjà existant.")
            raise ValueError("Panier déjà existant")
        
        logger.info(f"Création du panier pour le client ID {client_id}.")
        nouveau = Panier(client_id=client_id, date_creation=datetime.utcnow())
        return self.dao.creer_panier(nouveau)

    def ajouter_produit(self, panier_id: int, produit: ProduitPanier) -> Panier:
        logger.info(f"Ajout du produit ({produit.produit_id}, magasin {produit.magasin_id}) au panier ID {panier_id}.")
        panier = self.dao.get_by_id(panier_id)
        if not panier:
            raise ValueError(f"Panier {panier_id} introuvable")
        return self.dao.ajouter_produit(panier, produit)
