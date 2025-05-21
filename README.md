# LOG430-Lab0

## Description

Ce projet simple illustre :
- Une application Python imprimant "Hello World!"
- Des tests unitaires automatisés
- Un workflow CI/CD avec GitHub Actions
- Un conteneur Docker construit et publié automatiquement sur Docker Hub

## Instructions

0.Cloner le projet
   git clone https://github.com/Ludo67/LOG430-Lab0.git
1.Assurez-vous que Python 3 est installé :
   python3 --version

2.Exécutez depuis la ligne de commande :
    python hello_world.py

3.Pour exécuter les tests unitaires :
    python -m unittest discover -s . -p "*.py"
4.Lancer avec Docker
   docker build -t myapp .
   docker run myapp
   docker-compose up --build


## Structure du projet
LOG430-Labo/
.
├── .github/
│   └── workflows/
│       └── pipeline.yml        # Déclenche les tests, build, et push Docker
│
├── Dockerfile                  # Instructions pour construire l’image de l’application
├── docker-compose.yaml         # Optionnel, pour exécuter l'application avec d'autres services
│
├── hello_world.py              # Script principal Python : affiche "Hello World!"
├── test_hello_world.py         # Fichier de tests unitaires avec unittest
│
├── .gitignore                  # Fichiers/dossiers à ignorer par Git
└── README.md                   # Documentation du projet

Rôles des fichiers

   .github/workflows/ci-cd.yml
      Gère le pipeline CI/CD : exécution des tests, construction de l’image Docker, push vers Docker Hub.

   Dockerfile
      Contient les instructions nécessaires pour empaqueter l’application dans une image Docker.

   docker-compose.yaml
      Permet de lancer facilement l'application (et éventuellement d'autres services).

   hello_world.py
      Contient la logique de base de l’application : une simple impression console.

   test_hello_world.py
      Vérifie automatiquement que le script fonctionne comme attendu.

   .gitignore
      Empêche certains fichiers temporaires (cache, logs, etc.) d’être ajoutés à Git.

   README.md
      Donne toutes les informations nécessaires : description, exécution, structure.
