# LOG430-Lab0 – Application de gestion de stock

## 📋 Description

Ce projet illustre :
- Une application Python en ligne de commande organisée en trois couches : présentation, service, accès aux données
- Une base de données SQLite locale pour la persistance
- Des tests unitaires pour les couches DAO et service
- Un workflow CI/CD avec GitHub Actions
- Une conteneurisation complète avec Docker et Docker Compose

---

## 📂 Structure du projet

```
├── data_access_layer/
│   ├── __init__.py
│   ├── product_dao.py        # Opérations CRUD sur les produits
│   ├── init_db.py            # Initialisation de la BD SQLite
│   ├── schema.py             # Schéma SQL (création des tables)
│   └── produits.db           # Base de données SQLite
│
├── service_layer/
│   ├── __init__.py
│   └── stock_service.py      # Logique métier : ventes, retours, recherche
│
├── presentation_layer/
│   ├── __init__.py
│   └── main.py               # Interface console et menu utilisateur
│
├── tests/
│   ├── __init__.py
│   ├── test_dao.py           # Tests unitaires DAO
│   └── test_stock_service.py # Tests unitaires service
│
├── Dockerfile
├── docker-compose.yaml
├── .github/workflows/ci-cd.yml
├── .gitignore
└── README.md
```

---

## ▶️ Instructions d’exécution

### 0. Cloner le projet
```bash
git clone https://github.com/Ludo67/LOG430-Lab0.git
cd LOG430-Lab0
```

### 1. Prérequis
- Python 3.8+
- Docker
- Docker Compose

### 2. Exécution locale
```bash
python data_access_layer/init_db.py     # Initialise la base de données
python presentation_layer/main.py       # Lance le menu console
```

### 3. Exécuter les tests unitaires
```bash
python -m unittest discover -s tests
```

### 4. Exécuter avec Docker
```bash
docker-compose up --build
```

📝 Note : L’application utilise `input()`, ce qui nécessite une exécution interactive dans Docker (ex. `docker run -it`).

---

## 🐳 Fichiers clés

- `Dockerfile` : construit l’image Python de l’application.
- `docker-compose.yaml` : orchestre l’exécution via un service `stock-app`.
- `.github/workflows/ci-cd.yml` : pipeline CI/CD avec tests + push vers DockerHub.
- `produits.db` : base SQLite initialisée par `init_db.py`.

---

## ✅ Fonctionnalités

- Recherche de produit par mot-clé
- Enregistrement d'une vente (stock - N)
- Annulation d'une vente (stock + N)
- Consultation de l'inventaire

---

## 🧪 Technologies

🐍 Python

    Pourquoi ? Langage simple, lisible, et très populaire pour les projets éducatifs et prototypes.

    Avantage clé : Écosystème riche (librairies, frameworks), rapidité de développement, excellente compatibilité avec les outils de test, de CI/CD, et de conteneurisation.

🗃️ SQLite

    Pourquoi ? Base de données légère et embarquée, parfaite pour les applications simples sans serveur SGBD.

    Avantage clé : Aucune configuration serveur, fichier local produits.db, idéal pour déploiement rapide ou démonstration.

📦 Architecture à trois couches (DAO / Service / Présentation)

    Pourquoi ? Séparation claire des responsabilités (accès aux données, logique métier, interface utilisateur).

    Avantage clé : Facilite les tests, la maintenance, et l’évolution vers des architectures plus complexes (ex: API REST, Frontend).

🧪 unittest (module Python standard)

    Pourquoi ? Intégré à Python, facile à configurer, compatible avec les pipelines CI.

    Avantage clé : Permet l’automatisation rapide des tests sans dépendance externe.

🐳 Docker + Docker Compose

    Pourquoi ? Facilite le déploiement, l’isolation de l’environnement, et la portabilité du projet.

    Avantage clé : Une seule commande (docker-compose up) suffit pour lancer toute l’application, peu importe l’environnement hôte.

⚙️ GitHub Actions (CI/CD)

    Pourquoi ? Intégration directe avec GitHub pour automatiser les tests, la construction Docker et les déploiements.

    Avantage clé : Automatisation fiable et gratuite pour projets open source, renforce la qualité du code.
