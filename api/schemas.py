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
