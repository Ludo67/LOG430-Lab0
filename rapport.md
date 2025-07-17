# LOG430 - Étape 1
```
Nom: Ludovic Marcoux Hoyos
Groupe: 02
Session: Été 2025
```

## Description
Ce projet est une application gèrant le stock, les commandesm, les transferts, les client et les ventes d'une compagnie. 

## L'architecture

# Architecture du système

Le système est conçu selon une architecture à base de microservices conteneurisés via Docker Compose, favorisant la modularité, l'évolutivité et la scalabilité horizontale.

## 1. Couche `shared_data`

Chaque microservice gère sa propriété accès aux données via SQLAlchemy, connecté à une base PostgreSQL commune.

- **Modèles** :
  - `Produit`, `Vente`, `Client`, `Panier`, `ProduitPanier`, etc.
  - Organisés dans chaque microservice (`stock_service`, `customer_service`, etc.)

- **DAO** :
  - Chaque entité dispose d'un DAO (ex: `ProduitDAO`) avec des méthodes comme `get_by_id`, `rechercher`, `update`, etc.

## 2. Services

Cette couche encapsule la logique métier spécifique à chaque microservice.

- **`StockService`**
- **`RestockService`**
- **`ReportingService`**
- **`CustomerService`**
- **`CartService`**

Chaque service fait appel à ses DAO pour appliquer la logique d'affaires.

## 3. Couche `API` (FastAPI)

Chaque microservice expose une API REST documentée via Swagger (OpenAPI 3.0), et utilise :

- Authentification par `X-API-Key`
- Logging structuré
- Instrumentation Prometheus via `prometheus_fastapi_instrumentator`
- Middleware CORS

## 4. API Gateway (KrakenD)

- Centralise toutes les routes REST via `krakend.json`
- Transmet les en-têtes (`X-API-Key`) aux microservices backend
- Compatible avec Swagger UI pour une interface unifiée

## 5. Observabilité

- **Prometheus** : collecte les métriques depuis chaque microservice
- **Grafana** : visualisation des dashboards (latence, disponibilité, instance)
- **Requêtes Prometheus** :
  - `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[1m]))`
  - `rate(http_requests_total{status!~"4..|5.."}[1m])`
  - `sum by (instance) (rate(http_requests_total[1m]))`

---

# Besoins fonctionnels et non-fonctionnels

## ✅ Besoins fonctionnels

Le système permet la gestion de stock, la vente, le panier client et le reporting via une interface REST.

### 1. Gestion du stock
- `GET /stock/` : liste des produits
- `POST /stock/vente` / `annulation`
- `PUT /stock/update/:produit_id/magasin/:magasin_id`

### 2. Réapprovisionnement
- `POST /restock/transferer`
- `GET /restock/stock_par_magasin`

### 3. Tableau de bord / Reporting
- `GET /reporting/ventes`, `/ruptures`, `/dashboard`

### 4. Gestion client
- `POST /clients/`, `GET /clients/{client_id}`

### 5. Panier
- `POST /panier/`, `/panier/{id}/produit`, `/panier/{id}/checkout`
- `GET /panier/panier/{id}`

---

## ✅ Besoins non-fonctionnels

### 🔧 Architecture
- Microservices FastAPI
- Base de données PostgreSQL commune
- Communication via Docker internal network

### 🔍 Testabilité
- Tests unitaires des DAO et services
- Tests d’intégration des routes FastAPI

### 🧰 Observabilité
- Prometheus scrappe `/metrics` de chaque service
- Dashboards Grafana pour :
  - Latence 95e percentile
  - Taux de réussite des requêtes
  - Répartition de charge

### 🚀 Performance
- Load testing avec `k6`
- API Gateway avec KrakenD (future option : Kong)
- Scalabilité horizontale testée avec `cart_service_1` et `cart_service_2`

### 📅 Déploiement
- Docker Compose (multi-service)
- Script d’initialisation de la base (`init_db.py`, `seed_db.py`)

### 🔄 Swagger unifié
- Swagger UI connecté à KrakenD via `swagger-config.yaml`

## Justification des décisions d'architecture. (ADR)

## 1 - Choix de la base de données, [ADR](docs/ADR/ADR-BD.md)

### Statut : Accepté
### Date : 2025-06-09
### Décision 
    Utilisation de SQLite comme base de données relationnelle locale.

### Contexte
    Le système de gestion de stock devait persister les produits, magasins et ventes. Les exigences précisaient qu’aucun serveur HTTP ou API REST n'était requis, et que la base devait fonctionner localement sur la VM.

### Choix possibles

    JSON/CSV : trop fragile pour la cohérence transactionnelle.

    MongoDB (NoSQL) et PostgreSQL: trop complexe pour un usage local et non nécessaire.

    SQLite : simple, léger, intégré avec Python, supporte les contraintes (clés primaires composées, jointures).

### Conséquences

    Facile à intégrer sans configuration serveur.

    Compatible avec le module sqlite3 natif.

    Limite la scalabilité en cas d’accès concurrent élevé

## 2 - Séparation des responsabilités, [ADR](docs/ADR/ADR-Separation.md)

### Statut : Accepté
### Date : 2025-06-09
### Décision
    Utilisation d’une architecture en 3 couches (présentation, service, accès aux données).
### Contexte :
    Le projet devait s'étendre dans les labos suivants, notamment pour prendre en charge de nouveaux UC (UC4–UC7 qui n'ont pas été implémentées encore à cette étape). La modularité et la testabilité devenaient cruciales.

### Choix possibles

    Application monolithique dans un seul fichier (rapide, mais non maintenable).

    Architecture MVC : autre option possible et interessante (plus utile pour utilisation web)

    Architecture en couches : claire, modulaire, évolutive.

### Conséquences

    Le dossier presentation_layer gère l'IHM en console.

    Le dossier service_layer isole la logique métier.

    Le dossier data_access_layer encapsule les opérations SQLite.

    Les tests peuvent être faits indépendamment sur chaque couche.

## Choix technologiques

🐍 Python

    Pourquoi ? Langage simple, lisible, et très populaire pour les projets éducatifs et prototypes.

    Avantage clé : Écosystème riche (librairies, frameworks), rapidité de développement, excellente compatibilité avec les outils de test, de CI/CD, et de conteneurisation.

🗃️ SQLite

    Pourquoi ? Base de données légère et embarquée, parfaite pour les applications simples sans serveur SGBD.

    Avantage clé : Aucune configuration serveur, fichier local produits.db, idéal pour déploiement rapide ou démonstration.

🧱 SQLAlchemy (ORM)

    Pourquoi ? Permet d’interagir avec la base de données via des objets Python plutôt qu’avec du SQL brut.

    Avantage clé : Abstraction de la logique SQL, rend la couche DAO testable en mémoire avec SQLite, tout en restant compatible avec d'autres SGBD.

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


## Diagrammes

### Vue Logique

![diagramme de classe](out/docs/UML/class_diagram/vue_logique.png)

### Vue d'implémentation

![diagramme processus](out/docs/UML/implementation/implementation.png)

### Vue de deploiement

![diagramme de deploiement](out/docs/UML/deployment/deployment.png)

### Vue d'implémentation

![diagramme d'implémentation](out/docs/UML/implementation/implementation.png)

### Vue de cas d'utilisation

![diagramme de cas d'utilisation](out/docs/UML/use_cases/VueCasUtilisation.png)

## Diagrammes de séquence (processus)

### Annuler vente
![diagramme sequence annulation vente](out/docs/UML/sequence_diagrams/annulation_vente/sequence_diagram_annulation.png)
### Enregistrer vente
![diagramme sequence enregistrement vente](out/docs/UML/sequence_diagrams/enregistrer_vente/sequence_diagram_vente.png)
### Reapprovisionnement
![diagramme sequence restock](out/docs/UML/sequence_diagrams/restock/sequence_diagram_restock.png)
### Rechercher produit
![diagramme sequence rechercher](out/docs/UML/sequence_diagrams/recherche_produit/sequence_diagram_recherche.png)
### Voir stock
![diagramme sequence consulter stock](out/docs/UML/sequence_diagrams/voir_stock/sequence_diagram_stock.png)
### Afficher tableau de bord
![diagramme sequence tableau](out/docs/UML/sequence_diagrams/tableau_de_bord/sequence_diagram_tableau_bord.png)

## Instruction d'installation et d'execution

### Cloner
Git bash: `git clone https://github.com/Ludo67/LOG430-Lab0.git`

### Installer .venv.
Installer un .venv. voir (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

### Installer dépendances
`pip install -r requirements.txt`

### setup projet(terminal)
`make build`
`make init-db`
`make seed-db`
`make up`

### Executer les tests unitaires

Terminal: `make test-` + nom du service

## Instruction pour l'environnement de production

Dans la machine virtuelle, voici des commandes à utiliser.

### Télécharger la plus nouvelle version sur docker hub

`docker pull ludo678/my-app:latest`

# 📦 CI/CD Pipeline – Description des étapes

Ce pipeline GitHub Actions automatise les étapes de **linting**, **tests**, **build Docker**, et **publication** sur Docker Hub lors d’un `push` ou `pull_request` sur n’importe quelle branche.

---

## ⚙️ Déclencheurs

```yaml
on:
  push:
    branches: [ "*" ]
  pull_request:
    branches: [ "*" ]


