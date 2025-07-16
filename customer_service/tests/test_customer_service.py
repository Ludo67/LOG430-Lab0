from http import client
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared_data.models import Base, Client
from shared_data.customer_dao import CustomerDAO
from customer_service import CustomerService


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_customer_service_create(session):

    dao = CustomerDAO(session)
    service = CustomerService(dao)

    client = service.creer_client(Client(
        nom="Durand", prenom="Paul", email="paul.durand@example.com", adresse="456 Avenue Exemple"
    ))

    assert client.nom == "Durand"
    assert client.email.endswith("@example.com")
    assert client.prenom == "Paul"
    assert client.adresse == "456 Avenue Exemple"