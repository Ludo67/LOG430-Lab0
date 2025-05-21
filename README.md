# LOG430-Lab0

## Description

Ce projet simple illustre :
- Une application Python imprimant "Hello World!"
- Des tests unitaires automatisés
- Un workflow CI/CD avec GitHub Actions
- Un conteneur Docker construit et publié automatiquement sur Docker Hub

## Instructions

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
├── .github/workflows/       # Workflows GitHub Actions (CI/CD)
├── Dockerfile               # Construction de l'image Docker
├── docker-compose.yaml      # Configuration multi-conteneur (facultative ici)
├── hello_world.py           # Code principal Python
├── README.md                # Ce fichier
└── .gitignore               # Fichiers ignorés par Git
