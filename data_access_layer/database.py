"""Initialisation de la base de données et création de la session SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Connexion à la base SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./stock.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Base déclarative
Base = declarative_base()

# Session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Crée toutes les tables dans la base de données."""
    Base.metadata.create_all(bind=engine)
