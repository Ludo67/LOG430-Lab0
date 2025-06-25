"""Point d'entrée principal de l'application."""

from service_layer.restock_service import RestockService
from service_layer.reporting_service import ReportingService
from service_layer.stock_service import StockService
from data_access_layer.product_dao import ProduitDAO
from data_access_layer.database import SessionLocal


def get_db():
    """Gestion de la session SQLAlchemy."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def afficher_menu():
    """Affiche le menu principal."""
    print("\nMenu:")
    print("1. Rechercher un produit")
    print("2. Enregistrer une vente")
    print("3. Annuler une vente")
    print("4. Consulter le stock")
    print("5. Réapprovisionnement entre magasins")
    print("6. Tableau de bord")
    print("7. Quitter")


def rechercher_produit(service_stock):
    """Gère la recherche de produits dans le stock."""
    terme = input("Terme de recherche: ")
    resultats = service_stock.rechercher_produit(terme)
    for produit in resultats:
        print(produit)


def enregistrer_vente(service_stock):
    """Enregistre une vente de produit."""
    produit_id = input("ID du produit vendu: ")
    quantite = int(input("Quantité vendue: "))
    magasin_id = int(input("ID du magasin: "))
    service_stock.enregistrer_vente(produit_id, quantite, magasin_id)


def annuler_vente(service_stock):
    """Annule une vente de produit et restaure le stock."""
    produit_id = input("ID du produit à annuler: ")
    quantite = int(input("Quantité à restaurer: "))
    magasin_id = int(input("ID du magasin: "))
    service_stock.annuler_vente(produit_id, quantite, magasin_id)


def consulter_stock(service_stock):
    """Affiche le stock actuel de tous les produits."""
    stock = service_stock.lister_stock()
    for produit in stock:
        print(produit)


def reapprovisionnement(service_restock):
    """Gère le réapprovisionnement entre magasins."""
    source = input("ID du magasin source: ")
    destination = input("ID du magasin destination: ")
    produit_id = input("ID du produit: ")
    quantite = int(input("Quantité à transférer: "))
    service_restock.transferer_stock(produit_id, quantite, source, destination)


def tableau_de_bord(service_reporting):
    """Affiche le tableau de bord des ventes et des ruptures de stock."""
    service_reporting.generer_tableau_de_bord()
    ruptures = service_reporting.get_out_of_stock()
    if ruptures:
        print("📉 Produits en rupture de stock :")
        for produit in ruptures:
            print(f"- {produit.nom} (magasin {produit.magasin_id})")
    else:
        print("✅ Aucun produit en rupture de stock.")


def main():
    """Point d'entrée de l'application."""
    dao = ProduitDAO(session=SessionLocal())
    service_stock = StockService(dao)
    service_restock = RestockService(dao)
    service_reporting = ReportingService(dao)

    actions = {
        "1": lambda: rechercher_produit(service_stock),
        "2": lambda: enregistrer_vente(service_stock),
        "3": lambda: annuler_vente(service_stock),
        "4": lambda: consulter_stock(service_stock),
        "5": lambda: reapprovisionnement(service_restock),
        "6": lambda: tableau_de_bord(service_reporting),
    }

    while True:
        afficher_menu()
        choix = input("Choix: ")

        if choix == "7":
            print("Au revoir !")
            break

        action = actions.get(choix)
        if action:
            try:
                action()
            except ValueError as err:
                print(f"Erreur : {err}")
        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
