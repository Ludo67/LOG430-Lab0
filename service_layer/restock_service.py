"""Service de gestion du réapprovisionnement entre magasins."""

from data_access_layer.product_dao import ProduitDAO


class RestockService:
    """Service permettant le transfert de stock entre magasins."""

    def __init__(self, dao: ProduitDAO):
        """Initialise le service avec un DAO de produit."""
        self.dao = dao

    def get_stock_par_magasin(self, magasin_id: int):
        """Retourne les produits d'un magasin donné."""
        return self.dao.get_by_magasin(magasin_id)

    def transferer_stock(
        self,
        produit_id: int,
        quantite: int,
        magasin_source: int,
        magasin_cible: int
    ):
        """
        Transfère une quantité d'un produit d'un magasin source vers un magasin cible.

        Args:
            produit_id (int): Identifiant du produit.
            quantite (int): Quantité à transférer.
            magasin_source (int): ID du magasin source.
            magasin_cible (int): ID du magasin cible.

        Raises:
            ValueError: Si le stock est insuffisant dans le magasin source.
        """
        source = self.dao.get_by_id(produit_id, magasin_source)
        if not source or int(source["quantite"]) < quantite:
            raise ValueError("Stock insuffisant dans le magasin source")

        source["quantite"] = int(source["quantite"]) - quantite
        self.dao.update(source)

        cible = self.dao.get_by_id(produit_id, magasin_cible)
        if cible:
            cible["quantite"] = int(cible["quantite"]) + quantite
            self.dao.update(cible)
        else:
            nouveau_produit = {
                "id": source["id"],
                "nom": source["nom"],
                "categorie": (
                    source["categorie"]
                    if "categorie" in source and source["categorie"]
                    else "Inconnue"
                ),
                "quantite": quantite,
                "prix": float(source["prix"]),
                "magasin_id": magasin_cible
            }
            self.dao.insert(nouveau_produit)
