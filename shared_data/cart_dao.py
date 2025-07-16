from sqlalchemy.orm import Session
from shared_data.models import Panier, ProduitPanier
from api.schemas import ProduitSimple

class CartDAO:
    def __init__(self, session: Session):
        self.session = session

    def creer_panier(self, panier: Panier):
        self.session.add(panier)
        self.session.commit()
        self.session.refresh(panier)
        return panier

    def get_by_id(self, panier_id: int):
        return self.session.query(Panier).filter(Panier.id == panier_id).first()

    def ajouter_produit(self, panier: Panier, produit: ProduitPanier):
        produit_associe = ProduitPanier(
            panier_id=panier.id,
            produit_id=produit.produit_id,
            magasin_id=produit.magasin_id,
            quantite=produit.quantite
        )
        self.session.add(produit_associe)
        self.session.commit()
        self.session.refresh(produit_associe)
        return produit_associe
    
    def get_panier(self, panier_id: int) -> Panier:
        return self.session.query(Panier).filter(Panier.id == panier_id).first()
