import pytest
from shared_data.database import SessionLocal, Base, engine
from shared_data.customer_dao import CustomerDAO
from shared_data.models import Client

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_creer_et_get_client(db):
    dao = CustomerDAO(db)
    nouveau_client = Client(
        id=2,
        nom="Martin",
        prenom="Alice",
        email="alice.martin@example.com",
        adresse="789 Boulevard Test"
    )
    client_enregistre = dao.insert(nouveau_client)
    assert client_enregistre.id == 2
