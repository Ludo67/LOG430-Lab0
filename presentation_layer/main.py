"""Interface console pour gérer les produits en stock."""

from service_layer.stock_service import StockService

def afficher_menu():
    """Affiche le menu principal."""
    print("\nMenu:")
    print("1. Rechercher un produit")
    print("2. Enregistrer une vente")
    print("3. Annuler une vente")
    print("4. Consulter le stock")
    print("5. Quitter")

def main():
    """Boucle principale d'interaction utilisateur."""
    service = StockService()
    while True:
        afficher_menu()
        choix = input("Choix: ")

        try:
            if choix == "1":
                terme = input("Entrez nom, id ou catégorie: ")
                resultats = service.rechercher_produit(terme)
                for produit in resultats:
                    print(
                        f"ID: {produit['id']} | Nom: {produit['nom']} | "
                        f"Catégorie: {produit['categorie']} | Prix: {produit['prix']} | "
                        f"Stock: {produit['quantite']}"
                    )

            elif choix == "2":
                produit_id = input("ID produit: ")
                quantite = int(input("Quantité vendue: "))
                service.enregistrer_vente(produit_id, quantite)
                print("Vente enregistrée avec succès.")

            elif choix == "3":
                produit_id = input("ID produit: ")
                quantite = int(input("Quantité à annuler: "))
                service.annuler_vente(produit_id, quantite)
                print("Retour enregistré avec succès.")

            elif choix == "4":
                stock = service.lister_stock()
                if not stock:
                    print("Aucun produit en stock.")
                    continue

                for produit in stock:
                    print(
                        f"ID: {produit['id']} | Nom: {produit['nom']} | "
                        f"Catégorie: {produit['categorie']} | Prix: {produit['prix']} | "
                        f"Stock: {produit['quantite']}"
                    )

            elif choix == "5":
                print("Au revoir !")
                break

        except (KeyError, RuntimeError, LookupError) as erreur:
            print(f"Erreur de traitement : {erreur}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramme interrompu.")
