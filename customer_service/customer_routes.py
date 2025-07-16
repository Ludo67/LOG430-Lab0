import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from shared_data.customer_dao import CustomerDAO
from customer_service import CustomerService
from shared_data.models import Client as ClientModel
from api.auth import verify_api_key
from api.schemas import Client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def router(service: CustomerService) -> APIRouter:
    r = APIRouter(prefix="/clients", tags=["👤 Clients"])

    @r.post("/", summary="➕ Créer un client", response_model=Client, status_code=201, dependencies=[Depends(verify_api_key)])
    def creer_client(client: Client):
        """
        Crée un nouveau client.

        **Paramètres** :
        - `client`: les détails du client à enregistrer

        **Exemple de réponse** :
        ```json
        {
            "id": 1,
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@example.com"
            "adresse": "123 Rue Exemple"
        }
        ```
        """
        logger.info(f"Création d'un nouveau client: {client.nom} {client.prenom}")
        client_model: ClientModel = service.creer_client(client)
        return Client.from_orm(client_model)

    @r.get("/{client_id}", summary="🔍 Récupérer un client", response_model=Client, status_code=200, dependencies=[Depends(verify_api_key)])
    def recuperer_client(client_id: int):
        """
        Récupère un client par son ID.

        **Paramètre** :
        - `client_id`: identifiant du client

        **Exemple de réponse** :
        ```json
        {
            "id": 1,
            "nom": "Dupont",
            "prenom": "Jean"
        }
        ```
        """
        logger.info(f"Récupération du client avec ID: {client_id}")
        return service.recuperer_client(client_id)

    return r