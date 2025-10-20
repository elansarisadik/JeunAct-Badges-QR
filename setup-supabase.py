#!/usr/bin/env python3
"""
Configuration automatisée Supabase pour QR Code Jeunact
"""

import requests
import json
import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def create_supabase_project():
    """Créer un projet Supabase via API"""
    print("🚀 Configuration Supabase pour QR Code Jeunact")
    print("=" * 50)
    
    print("📋 Étapes manuelles requises:")
    print("1. Allez sur https://supabase.com")
    print("2. Créez un nouveau projet")
    print("3. Notez l'URL de connexion PostgreSQL")
    print("4. Activez l'API REST")
    print()
    
    # Demander les informations Supabase
    project_url = input("🌐 Entrez l'URL de votre projet Supabase (ex: https://xyz.supabase.co): ").strip()
    api_key = input("🔑 Entrez votre clé API Supabase (anon key): ").strip()
    
    if not project_url or not api_key:
        print("❌ URL et clé API requis")
        return None
    
    return {
        'project_url': project_url,
        'api_key': api_key
    }

def create_database_tables(project_url, api_key):
    """Créer les tables via l'API Supabase"""
    print("📊 Création des tables de base de données...")
    
    # Headers pour l'API Supabase
    headers = {
        'apikey': api_key,
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # SQL pour créer les tables
    create_tables_sql = """
    -- Créer la table members
    CREATE TABLE IF NOT EXISTS members (
        id SERIAL PRIMARY KEY,
        member_number VARCHAR(20) UNIQUE NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        role VARCHAR(20) NOT NULL,
        position VARCHAR(50),
        email VARCHAR(120),
        whatsapp VARCHAR(20),
        instagram VARCHAR(100),
        linkedin VARCHAR(200),
        tiktok VARCHAR(100),
        portfolio VARCHAR(200),
        photo VARCHAR(200),
        integration_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Créer les index
    CREATE INDEX IF NOT EXISTS idx_member_number ON members(member_number);
    CREATE INDEX IF NOT EXISTS idx_full_name ON members(full_name);
    CREATE INDEX IF NOT EXISTS idx_role ON members(role);
    
    -- Activer RLS (Row Level Security)
    ALTER TABLE members ENABLE ROW LEVEL SECURITY;
    
    -- Créer une politique pour permettre l'accès public (pour l'API)
    CREATE POLICY "Allow public access" ON members FOR ALL USING (true);
    """
    
    try:
        # Exécuter le SQL via l'API
        response = requests.post(
            f"{project_url}/rest/v1/rpc/exec_sql",
            headers=headers,
            json={'sql': create_tables_sql}
        )
        
        if response.status_code == 200:
            print("✅ Tables créées avec succès")
            return True
        else:
            print(f"⚠️  Erreur API: {response.status_code}")
            print("💡 Créez manuellement les tables dans l'éditeur SQL Supabase")
            return False
            
    except Exception as e:
        print(f"❌ Erreur création tables: {e}")
        print("💡 Créez manuellement les tables dans l'éditeur SQL Supabase")
        return False

def test_database_connection(project_url, api_key):
    """Tester la connexion à la base de données"""
    print("🔌 Test de connexion à la base de données...")
    
    headers = {
        'apikey': api_key,
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Tester l'accès à la table members
        response = requests.get(
            f"{project_url}/rest/v1/members?select=count",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Connexion à la base de données réussie")
            return True
        else:
            print(f"⚠️  Erreur connexion: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test connexion: {e}")
        return False

def generate_database_url(project_url):
    """Générer l'URL de connexion PostgreSQL"""
    print("🔗 Génération de l'URL de connexion...")
    
    # Extraire l'ID du projet de l'URL
    project_id = project_url.replace('https://', '').replace('.supabase.co', '')
    
    # Demander le mot de passe de la base de données
    db_password = input("🔐 Entrez le mot de passe de votre base de données Supabase: ").strip()
    
    if not db_password:
        print("❌ Mot de passe requis")
        return None
    
    # Construire l'URL PostgreSQL
    database_url = f"postgresql://postgres:{db_password}@db.{project_id}.supabase.co:5432/postgres"
    
    print(f"✅ URL de connexion générée:")
    print(f"   {database_url}")
    
    return database_url

def save_configuration(database_url, project_url, api_key):
    """Sauvegarder la configuration"""
    print("💾 Sauvegarde de la configuration...")
    
    # Créer un fichier .env.local avec la configuration
    env_content = f"""# Configuration Supabase pour QR Code Jeunact
DATABASE_URL={database_url}
SUPABASE_URL={project_url}
SUPABASE_ANON_KEY={api_key}
SUPABASE_PROJECT_ID={project_url.replace('https://', '').replace('.supabase.co', '')}
"""
    
    with open('.env.local', 'w') as f:
        f.write(env_content)
    
    print("✅ Configuration sauvegardée dans .env.local")
    
    # Mettre à jour wrangler.toml
    try:
        with open('wrangler.toml', 'r') as f:
            wrangler_content = f.read()
        
        # Remplacer l'URL de base de données
        wrangler_content = wrangler_content.replace(
            'postgresql://postgres:password@db.project-ref.supabase.co:5432/postgres',
            database_url
        )
        
        with open('wrangler.toml', 'w') as f:
            f.write(wrangler_content)
        
        print("✅ wrangler.toml mis à jour")
        
    except Exception as e:
        print(f"⚠️  Erreur mise à jour wrangler.toml: {e}")

def main():
    print("🚀 Configuration Supabase pour QR Code Jeunact")
    print("=" * 50)
    
    # Créer le projet Supabase
    config = create_supabase_project()
    if not config:
        sys.exit(1)
    
    # Créer les tables
    if not create_database_tables(config['project_url'], config['api_key']):
        print("⚠️  Continuez avec la création manuelle des tables")
    
    # Tester la connexion
    if not test_database_connection(config['project_url'], config['api_key']):
        print("⚠️  Vérifiez votre configuration Supabase")
    
    # Générer l'URL de connexion
    database_url = generate_database_url(config['project_url'])
    if not database_url:
        sys.exit(1)
    
    # Sauvegarder la configuration
    save_configuration(database_url, config['project_url'], config['api_key'])
    
    print("\n🎉 Configuration Supabase terminée !")
    print("✅ Votre base de données est prête pour Cloudflare Workers")
    print("\n📋 Prochaines étapes:")
    print("1. Exécutez: python migrate-to-supabase.py")
    print("2. Exécutez: bash deploy-cloudflare.sh")
    print("3. Votre application sera disponible 24/7 !")

if __name__ == "__main__":
    main()
