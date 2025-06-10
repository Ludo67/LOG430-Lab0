"""Point d'entrée principal de l'application."""


from service_layer.restock_service import RestockService
from service_layer.reporting_service import ReportingService
from service_layer.stock_service import StockService
from data_access_layer.product_dao import ProduitDAO


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


def main():
    """Point d'entrée de l'application."""
    dao = ProduitDAO()
    stock_service = StockService(dao)
    reappro_service = RestockService(dao)
    reporting_service = ReportingService(dao)

    while True:
        afficher_menu()
        choix = input("Choix: ")

        try:
            if choix == "1":
                terme = input("Terme de recherche: ")
                resultats = stock_service.rechercher_produit(terme)
                for produit in resultats:
                    print(produit)

            elif choix == "2":
                produit_id = input("ID du produit vendu: ")
                quantite = int(input("Quantité vendue: "))
                magasin_id = int(input("ID du magasin: "))
                stock_service.enregistrer_vente(produit_id, quantite, magasin_id)

            elif choix == "3":
                produit_id = input("ID du produit à annuler: ")
                quantite = int(input("Quantité à restaurer: "))
                magasin_id = int(input("ID du magasin: "))
                stock_service.annuler_vente(produit_id, quantite, magasin_id)

            elif choix == "4":
                stock = stock_service.lister_stock()
                for produit in stock:
                    print(produit)

            elif choix == "5":
                source = input("ID du magasin source: ")
                destination = input("ID du magasin destination: ")
                produit_id = input("ID du produit: ")
                quantite = int(input("Quantité à transférer: "))
                reappro_service.transferer_stock(produit_id, quantite, source, destination)

            elif choix == "6":
                reporting_service.generer_tableau_de_bord()

            elif choix == "7":
                print("Au revoir !")
                break

            else:
                print("Choix invalide. Veuillez réessayer.")

        except ValueError as err:
            print(f"Erreur : {err}")

if __name__ == "__main__":
    main()
