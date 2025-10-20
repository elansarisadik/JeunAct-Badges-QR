#!/usr/bin/env python3
"""
Script de déploiement automatisé pour JeunAct Badges QR
"""

import os
import subprocess
import sys
import secrets
import string

def generate_secret_key():
    """Génère une clé secrète sécurisée"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(50))

def check_requirements():
    """Vérifie que tous les fichiers requis sont présents"""
    required_files = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    print("✅ Tous les fichiers requis sont présents")
    return True

def setup_git():
    """Initialise git si nécessaire"""
    if not os.path.exists('.git'):
        print("📁 Initialisation de Git...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
        print("✅ Git initialisé")
    else:
        print("✅ Git déjà initialisé")

def deploy_railway():
    """Déploie sur Railway"""
    print("🚀 Déploiement sur Railway...")
    
    # Installation de Railway CLI si nécessaire
    try:
        subprocess.run(['railway', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installation de Railway CLI...")
        subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
    
    # Login et déploiement
    subprocess.run(['railway', 'login'], check=True)
    subprocess.run(['railway', 'link'], check=True)
    
    # Configuration des variables d'environnement
    secret_key = generate_secret_key()
    subprocess.run(['railway', 'variables', 'set', f'SECRET_KEY={secret_key}'], check=True)
    subprocess.run(['railway', 'variables', 'set', 'FLASK_ENV=production'], check=True)
    
    # Déploiement
    subprocess.run(['railway', 'up'], check=True)
    
    print("✅ Déployé sur Railway!")
    print("🌐 Votre application sera disponible à l'URL fournie par Railway")

def deploy_heroku():
    """Déploie sur Heroku"""
    print("🚀 Déploiement sur Heroku...")
    
    # Vérification de Heroku CLI
    try:
        subprocess.run(['heroku', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Heroku CLI non installé. Installez-le depuis https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Création de l'app Heroku
    app_name = input("Nom de votre app Heroku (ou appuyez sur Entrée pour auto-générer): ").strip()
    if not app_name:
        app_name = f"jeunact-badges-{secrets.token_hex(4)}"
    
    try:
        subprocess.run(['heroku', 'create', app_name], check=True)
    except subprocess.CalledProcessError:
        print(f"⚠️  L'app {app_name} existe peut-être déjà")
    
    # Configuration des variables d'environnement
    secret_key = generate_secret_key()
    subprocess.run(['heroku', 'config:set', f'SECRET_KEY={secret_key}'], check=True)
    subprocess.run(['heroku', 'config:set', 'FLASK_ENV=production'], check=True)
    subprocess.run(['heroku', 'config:set', f'PRODUCTION_URL=https://{app_name}.herokuapp.com'], check=True)
    
    # Déploiement
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Deploy to Heroku'], check=True)
    subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
    
    print(f"✅ Déployé sur Heroku!")
    print(f"🌐 Votre application est disponible à: https://{app_name}.herokuapp.com")

def main():
    print("🎯 Script de Déploiement JeunAct Badges QR")
    print("=" * 50)
    
    if not check_requirements():
        sys.exit(1)
    
    setup_git()
    
    print("\n🚀 Choisissez votre plateforme de déploiement:")
    print("1. Railway (Recommandé - Gratuit)")
    print("2. Heroku (Classique)")
    print("3. Quitter")
    
    choice = input("\nVotre choix (1-3): ").strip()
    
    if choice == '1':
        deploy_railway()
    elif choice == '2':
        deploy_heroku()
    elif choice == '3':
        print("👋 Au revoir!")
    else:
        print("❌ Choix invalide!")

if __name__ == "__main__":
    main()
