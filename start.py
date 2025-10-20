#!/usr/bin/env python3
"""
Script de démarrage simple pour GitHub Pages
"""
import os
import sys
import subprocess

def main():
    """Démarre l'application Flask"""
    try:
        # Vérifier si Python est disponible
        python_version = sys.version_info
        print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Installer les dépendances si nécessaire
        print("Installation des dépendances...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # Démarrer l'application
        print("Démarrage de l'application Flask...")
        os.system("python app.py")
        
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
