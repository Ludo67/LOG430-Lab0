from typing import Optional
from pydantic import BaseModel

class VenteRequest(BaseModel):
    produit_id: str
    quantite: int
    magasin_id: int

class AnnulationRequest(BaseModel):
    produit_id: str
    quantite: int
    magasin_id: int

class TransfertRequest(BaseModel):
    produit_id: str
    quantite: int
    magasin_source: int
    magasin_destination: int

class MiseAJourProduitDTO(BaseModel):
    nom: Optional[str]
    categorie: Optional[str]
    prix: Optional[float]
    quantite: Optional[int]

class NouveauProduitDTO(BaseModel):
    id: int
    nom: str
    categorie: str
    quantite: int
    prix: float
    magasin_id: int

class Client(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    adresse: str

    class Config:
        from_attributes = True