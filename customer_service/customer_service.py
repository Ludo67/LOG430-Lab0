import logging
from shared_data.customer_dao import CustomerDAO
from shared_data.models import Client
from sqlalchemy.orm import Session
logging.basicConfig(
    level=logging.INFO,  # Change à DEBUG ou ERROR selon les besoins
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

class CustomerService:
    def __init__(self, dao: CustomerDAO):
        self.dao = dao
        self.session: Session = dao.session

    def creer_client(self, client: Client):
        """Crée un nouveau client dans la base de données."""
        if self.dao.get_by_id(client.id):
            logger.error(f"Client ID {client.id} déjà existant.")
            raise ValueError("Client déjà existant")
        
        logger.info(f"Création du client ID {client.id} avec nom {client.nom} et prénom {client.prenom}.")
        return self.dao.insert(client)

    def recuperer_client(self, client_id: int):
        """Récupère un client par son ID."""
        logger.info(f"Récupération du client avec ID: {client_id}")
        return self.dao.get_by_id(client_id)
