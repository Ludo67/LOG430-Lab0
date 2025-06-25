"""Initialisation des tables"""

from data_access_layer.database import engine
from data_access_layer.models import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")
