#!/usr/bin/env python3
"""
Script de préparation pour PythonAnywhere
QR Code Jeunact
"""

import os
import shutil

def prepare_for_pythonanywhere():
    print("🚀 Préparation pour PythonAnywhere")
    print("=" * 40)
    
    # Vérifier les fichiers nécessaires
    required_files = [
        'app.py',
        'config.py', 
        'requirements.txt',
        'wsgi.py',
        'templates',
        'static'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    print("✅ Tous les fichiers nécessaires sont présents")
    
    # Créer le fichier .env avec l'URL PythonAnywhere
    username = input("👤 Entrez votre nom d'utilisateur PythonAnywhere: ").strip()
    
    if not username:
        print("❌ Nom d'utilisateur requis")
        return False
    
    env_content = f"""# Configuration pour PythonAnywhere
PRODUCTION_URL=https://{username}.pythonanywhere.com
SECRET_KEY=JeunAct2024_QR_Code_SuperSecretKey_ChangeInProduction
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"✅ Fichier .env créé avec l'URL: https://{username}.pythonanywhere.com")
    
    # Créer un fichier de déploiement
    deploy_content = f"""# Instructions de déploiement PythonAnywhere

## 1. Uploader les fichiers
Uploadez ces fichiers dans votre dossier PythonAnywhere :
- app.py
- config.py
- requirements.txt
- wsgi.py
- .env
- templates/ (dossier complet)
- static/ (dossier complet)

## 2. Installer les dépendances
```bash
cd JeunAct-Badges-QR
pip3.10 install --user -r requirements.txt
```

## 3. Configurer l'application web
- Source code: /home/{username}/JeunAct-Badges-QR
- WSGI file: /home/{username}/JeunAct-Badges-QR/wsgi.py

## 4. Variables d'environnement
- PRODUCTION_URL: https://{username}.pythonanywhere.com
- SECRET_KEY: JeunAct2024_QR_Code_SuperSecretKey_ChangeInProduction

## 5. Redémarrer l'application
Cliquez sur "Reload" dans la section Web

## 🎉 Votre application sera disponible sur :
https://{username}.pythonanywhere.com
"""
    
    with open('DEPLOY_INSTRUCTIONS.txt', 'w') as f:
        f.write(deploy_content)
    
    print("✅ Instructions de déploiement créées dans DEPLOY_INSTRUCTIONS.txt")
    
    print("\n🎉 Préparation terminée !")
    print("📋 Prochaines étapes:")
    print("1. Allez sur pythonanywhere.com")
    print("2. Créez un compte gratuit")
    print("3. Suivez les instructions dans DEPLOY_INSTRUCTIONS.txt")
    
    return True

if __name__ == "__main__":
    prepare_for_pythonanywhere()


