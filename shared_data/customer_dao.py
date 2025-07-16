from sqlalchemy.orm import Session
from shared_data.models import Client as ClientModel
# from api.schemas import Client as ClientSchema

class CustomerDAO:
    def __init__(self, session: Session):
        """
        Initialise le DAO avec une session SQLAlchemy.
        :param session: Session SQLAlchemy active.
        """
        self.session = session
    def get_by_id(self, client_id: int):
        """Récupère un client par son ID."""
        return self.session.query(ClientModel).filter(ClientModel.id == client_id).first()

    def insert(self, client: ClientModel):
        """
        Insère un nouveau client.
        :param client: Un objet Client ou un dictionnaire avec les champs requis.
        """
        client_model = ClientModel(
            nom=client.nom,
            prenom=client.prenom,
            email=client.email,
            adresse=client.adresse,
            id=client.id
        )
        self.session.add(client_model)
        self.session.commit()
        self.session.refresh(client_model)
        return client_model