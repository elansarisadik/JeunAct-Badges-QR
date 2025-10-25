#!/usr/bin/env python3
"""
Script de déploiement local pour générer les pages statiques
Usage: python deploy_local.py
"""

import os
import sys
from static_generator import StaticGenerator

def main():
    print("🚀 Déploiement local - Génération des pages statiques")
    print("=" * 60)
    
    # Vérifier que les dossiers nécessaires existent
    required_dirs = ['templates', 'static', 'data']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print(f"❌ Dossier manquant: {dir_name}")
            sys.exit(1)
    
    # Vérifier que le fichier de données existe
    if not os.path.exists('data/members.json'):
        print("❌ Fichier de données manquant: data/members.json")
        sys.exit(1)
    
    try:
        # Générer les pages statiques
        generator = StaticGenerator()
        generator.generate_all()
        
        print("\n✅ Déploiement local terminé avec succès !")
        print("\n📁 Fichiers générés:")
        print("   - index.html (page d'accueil)")
        print("   - member/*.html (pages des membres)")
        print("\n🌐 Pour tester localement:")
        print("   - Ouvrez index.html dans votre navigateur")
        print("   - Ou utilisez: python -m http.server 8000")
        
    except Exception as e:
        print(f"❌ Erreur lors du déploiement: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
