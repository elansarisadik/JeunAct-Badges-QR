# Configuration pour PythonAnywhere
# Fichier WSGI pour le déploiement

import sys
import os

# Ajouter le chemin du projet
path = '/home/votre-username/JeunAct-Badges-QR'
if path not in sys.path:
    sys.path.append(path)

# Importer l'application Flask
from app import app as application

# Configuration pour la production
if __name__ == "__main__":
    application.run()


