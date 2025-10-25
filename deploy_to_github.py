#!/usr/bin/env python3
"""
Script de déploiement direct vers GitHub
Usage: python deploy_to_github.py
"""

import os
import subprocess
import json

def update_urls_in_files():
    """Met à jour les URLs dans tous les fichiers"""
    print("🔄 Mise à jour des URLs...")
    
    # URL de base pour le repository
    base_url = "https://elans.github.io/JeunAct-Association"
    
    # Fichiers à modifier
    files_to_update = [
        'static_generator.py',
        'templates/member_profile_static.html',
        'app_json.py'
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remplacer l'URL
                content = content.replace('https://votre-username.github.io/QR-Code', base_url)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ {file_path} mis à jour")
            except Exception as e:
                print(f"   ❌ Erreur avec {file_path}: {e}")

def generate_static_pages():
    """Génère les pages statiques"""
    print("\n🔄 Génération des pages statiques...")
    
    try:
        from static_generator import StaticGenerator
        generator = StaticGenerator()
        generator.generate_all()
        print("   ✅ Pages statiques générées")
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def create_gitignore():
    """Crée un .gitignore approprié"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite3

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print("   ✅ .gitignore créé")

def create_readme():
    """Crée un README pour le repository"""
    readme_content = """# JeunAct Association - Badges QR

Système de badges QR pour les membres de l'association JeunAct.

## 🚀 Déploiement Automatique

Ce site est déployé automatiquement sur GitHub Pages :
- **URL** : https://elans.github.io/JeunAct-Association/
- **Déploiement** : Automatique via GitHub Actions

## 🔧 Administration

Pour gérer les membres :

```bash
python admin_simple.py
```

## 📱 Fonctionnalités

- ✅ Pages statiques compatibles GitHub Pages
- ✅ Base de données JSON (pas de serveur requis)
- ✅ QR Codes générés automatiquement
- ✅ Interface d'administration simple
- ✅ Déploiement automatique
- ✅ Design responsive et moderne

## 🌐 URLs

- **Site principal** : https://elans.github.io/JeunAct-Association/
- **Profil membre** : https://elans.github.io/JeunAct-Association/member/1.html
- **QR Code** : Pointe vers la page du membre

## 🔒 Sécurité

- Mot de passe admin : `JeunAct2024Admin`
- Données stockées localement dans JSON
- Interface d'administration protégée
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("   ✅ README.md créé")

def main():
    """Lance le déploiement"""
    print("🚀 DÉPLOIEMENT JEUNACT ASSOCIATION")
    print("=" * 50)
    
    # 1. Mettre à jour les URLs
    update_urls_in_files()
    
    # 2. Créer les fichiers de configuration
    create_gitignore()
    create_readme()
    
    # 3. Générer les pages statiques
    if not generate_static_pages():
        print("❌ Échec de la génération des pages")
        return
    
    print("\n✅ PRÉPARATION TERMINÉE !")
    print("\n📝 Instructions pour GitHub :")
    print("1. Créer un nouveau repository sur GitHub")
    print("2. Nom : 'JeunAct-Association'")
    print("3. Description : 'Système de badges QR pour l'association JeunAct'")
    print("4. Public ou Privé (selon votre choix)")
    print("5. Ne pas initialiser avec README (on en a déjà un)")
    print("\n🔧 Commandes Git :")
    print("git init")
    print("git add .")
    print("git commit -m 'Initial commit - JeunAct Association'")
    print("git branch -M main")
    print("git remote add origin https://github.com/elans/JeunAct-Association.git")
    print("git push -u origin main")
    print("\n🌐 Après le push, votre site sera accessible sur :")
    print("https://elans.github.io/JeunAct-Association/")

if __name__ == '__main__':
    main()
