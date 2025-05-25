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

Rôles des fichiers

   .github/workflows/ci-cd.yml
      Gère le pipeline CI/CD : exécution des tests, construction de l’image Docker, push vers Docker Hub.

   Dockerfile
      Contient les instructions nécessaires pour empaqueter l’application dans une image Docker.

   docker-compose.yaml
      Permet de lancer facilement l'application (et éventuellement d'autres services).

   hello_world.py
      Contient la logique de base de l’application : une simple impression console.
      
   .gitignore
      Empêche certains fichiers temporaires (cache, logs, etc.) d’être ajoutés à Git.

   README.md
      Donne toutes les informations nécessaires : description, exécution, structure.

## Analyse des besoins
    ### Fonctionnels

        - Ajouter, modifier, supprimer et consulter produit

        - Réaliser vente et retour
        
        - Consulter l'état du stock

    ### Non-Fonctionnels

        - Facile d'utilisation (via la console)

        - Données sauvegardées entre les exécutions

        - Rapiditité des réponses (<3s)

## Choix technologiques

    - Language (Python):
        Simple à utiliser, comprendre et apprendre.

        Fiable et rapide

    - Base de données (SQLite):
        Base locale, Fiable, Transactionnelle,
        Simple d'utilsation et d'implémentation
    
    - Librairies (Dataclasses, JSON):
        Fiables, simples et peut coûteux

        Pas besoin d'installation externe

    - Outils de diagrammes (PlantUML):
        Gratuit, compatible avec UML et implémenté directement dans VSCode

        Facile à utiliser