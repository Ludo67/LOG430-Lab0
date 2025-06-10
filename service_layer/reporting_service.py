"""Service de génération de rapports et de tableau de bord."""

class ReportingService:
    """Service fournissant des rapports de ventes et de stock."""

    def __init__(self, dao):
        """Initialise le service avec un accès DAO."""
        self.dao = dao

    def afficher_tableau_de_bord(self):
        """Affiche un résumé des ventes par magasin."""
        ventes = self.dao.get_ventes_par_magasin()

        if not ventes:
            print("Aucune vente enregistrée.")
            return

        print("\n=== Ventes par magasin ===")
        for magasin, total in ventes.items():
            print(f"Magasin {magasin}: {total} ventes")

    def rapport_ventes(self):
        """Retourne la liste des ventes groupées par magasin et produit."""
        cursor = self.dao.conn.execute("""
            SELECT magasin_id, produit_id, SUM(quantite) as total_vendu
            FROM ventes
            GROUP BY magasin_id, produit_id
        """)
        return [dict(row) for row in cursor.fetchall()]

    def produits_en_rupture(self, seuil=5):
        """Retourne les produits dont le stock est inférieur ou égal au seuil."""
        cursor = self.dao.conn.execute("""
            SELECT * FROM produits
            WHERE quantite <= ?
        """, (seuil,))
        return [dict(row) for row in cursor.fetchall()]

    def generer_tableau_de_bord(self):
        """Affiche le tableau de bord complet avec plusieurs rapports."""
        cursor = self.dao.conn.cursor()

        print("\n--- Rapport consolidé des ventes ---")
        cursor.execute("""
            SELECT p.id, p.nom, p.magasin_id,
                   SUM(v.quantite * p.prix) AS chiffre_affaires,
                   SUM(v.quantite) AS ventes,
                   p.prix AS prix_unitaire,
                   p.categorie AS categorie
            FROM ventes v
            JOIN produits p ON v.produit_id = p.id AND v.magasin_id = p.magasin_id
            GROUP BY p.id, p.magasin_id
        """)
        produits = cursor.fetchall()
        for produit in produits:
            print(
                f"[{produit['magasin_id']}] {produit['nom']} | "
                f"{produit['ventes']} ventes | CA: {produit['chiffre_affaires']:.2f} $"
            )

        print("\n--- Produits en rupture de stock ---")
        ruptures = self.dao.conn.execute("""
            SELECT id, nom, magasin_id FROM produits WHERE quantite <= 0
        """).fetchall()
        for produit in ruptures:
            print(f"[{produit['magasin_id']}] {produit['nom']} (id={produit['id']})")

        print("\n--- Produits en surstock ---")
        surplus = self.dao.conn.execute("""
            SELECT id, nom, quantite, magasin_id FROM produits WHERE quantite > 30
        """).fetchall()
        for produit in surplus:
            print(f"[{produit['magasin_id']}] {produit['nom']} ({produit['quantite']} en stock)")

        print("\n--- Chiffre d'affaires global ---")
        result = self.dao.conn.execute("""
            SELECT SUM(v.quantite * p.prix)
            FROM ventes v
            JOIN produits p ON v.produit_id = p.id AND v.magasin_id = p.magasin_id
        """).fetchone()
        total = result[0] if result and result[0] is not None else 0
        print(f"\n💰 Chiffre d'affaires total : {total:.2f} $")

        print("\n--- Tendances hebdomadaires ---")
        cursor.execute("""
            SELECT strftime('%Y-%W', timestamp) AS semaine,
                   produit_id,
                   SUM(quantite) AS total_hebdo
            FROM ventes
            GROUP BY semaine, produit_id
            ORDER BY semaine DESC
            LIMIT 10
        """)
        tendances = cursor.fetchall()
        for ligne in tendances:
            print(
                f"Semaine {ligne['semaine']} | Produit {ligne['produit_id']} : "
                f"{ligne['total_hebdo']} ventes"
            )
