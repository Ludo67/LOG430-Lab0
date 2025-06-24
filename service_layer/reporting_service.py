"""Service de génération de rapports et de tableau de bord."""

import sqlite3

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
        """Retourne un rapport structuré du tableau de bord."""
        with sqlite3.connect(self.dao.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 1. Rapport consolidé des ventes
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
            ventes_consolidees = [
                {
                    "produit_id": row["id"],
                    "nom": row["nom"],
                    "categorie": row["categorie"],
                    "magasin_id": row["magasin_id"],
                    "ventes": row["ventes"],
                    "prix_unitaire": row["prix_unitaire"],
                    "chiffre_affaires": row["chiffre_affaires"]
                }
                for row in cursor.fetchall()
            ]

            # 2. Produits en rupture de stock
            ruptures = conn.execute("""
                SELECT id, nom, magasin_id FROM produits WHERE quantite <= 0
            """).fetchall()
            produits_rupture = [
                {"id": row["id"], "nom": row["nom"], "magasin_id": row["magasin_id"]}
                for row in ruptures
            ]

            # 3. Produits en surstock
            surplus = conn.execute("""
                SELECT id, nom, quantite, magasin_id FROM produits WHERE quantite > 30
            """).fetchall()
            produits_surstock = [
                {"id": row["id"], "nom": row["nom"], "quantite": row["quantite"], "magasin_id": row["magasin_id"]}
                for row in surplus
            ]

            # 4. Chiffre d'affaires global
            result = conn.execute("""
                SELECT SUM(v.quantite * p.prix) AS total
                FROM ventes v
                JOIN produits p ON v.produit_id = p.id AND v.magasin_id = p.magasin_id
            """).fetchone()
            chiffre_affaires_total = result["total"] if result and result["total"] is not None else 0

            # 5. Tendances hebdomadaires
            cursor.execute("""
                SELECT strftime('%Y-%W', timestamp) AS semaine,
                    produit_id,
                    SUM(quantite) AS total_hebdo
                FROM ventes
                GROUP BY semaine, produit_id
                ORDER BY semaine DESC
                LIMIT 10
            """)
            tendances_hebdo = [
                {
                    "semaine": row["semaine"],
                    "produit_id": row["produit_id"],
                    "ventes_hebdo": row["total_hebdo"]
                }
                for row in cursor.fetchall()
            ]

        return {
            "ventes_consolidees": ventes_consolidees,
            "produits_rupture": produits_rupture,
            "produits_surstock": produits_surstock,
            "chiffre_affaires_total": chiffre_affaires_total,
            "tendances_hebdomadaires": tendances_hebdo
        }

