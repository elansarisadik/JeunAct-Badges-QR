#!/usr/bin/env python3
"""
Configuration Supabase simplifiée pour QR Code Jeunact
"""

import os
import sys

def main():
    print("🚀 Configuration Supabase pour QR Code Jeunact")
    print("=" * 50)
    
    print("\n📋 Étapes à suivre:")
    print("1. Allez sur https://supabase.com")
    print("2. Créez un nouveau projet")
    print("3. Notez l'URL de connexion PostgreSQL")
    print("4. Activez l'API REST")
    
    print("\n🔗 Informations nécessaires:")
    supabase_url = input("🌐 URL de votre projet Supabase (ex: https://xyz.supabase.co): ").strip()
    db_password = input("🔐 Mot de passe de votre base de données: ").strip()
    
    if not supabase_url or not db_password:
        print("❌ Informations requises")
        return
    
    # Extraire l'ID du projet
    project_id = supabase_url.replace('https://', '').replace('.supabase.co', '')
    
    # Construire l'URL de connexion
    database_url = f"postgresql://postgres:{db_password}@db.{project_id}.supabase.co:5432/postgres"
    
    print(f"\n✅ URL de connexion générée:")
    print(f"   {database_url}")
    
    # Créer le fichier .env.local
    env_content = f"""# Configuration Supabase pour QR Code Jeunact
DATABASE_URL={database_url}
SUPABASE_URL={supabase_url}
SUPABASE_PROJECT_ID={project_id}
"""
    
    with open('.env.local', 'w') as f:
        f.write(env_content)
    
    print("✅ Configuration sauvegardée dans .env.local")
    
    # SQL pour créer les tables
    sql_content = """-- Créer la table members
CREATE TABLE members (
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
CREATE INDEX idx_member_number ON members(member_number);
CREATE INDEX idx_full_name ON members(full_name);
CREATE INDEX idx_role ON members(role);

-- Activer RLS (Row Level Security)
ALTER TABLE members ENABLE ROW LEVEL SECURITY;

-- Créer une politique pour permettre l'accès public
CREATE POLICY "Allow public access" ON members FOR ALL USING (true);
"""
    
    with open('supabase-schema.sql', 'w') as f:
        f.write(sql_content)
    
    print("✅ Schéma SQL créé dans supabase-schema.sql")
    
    print("\n📋 Prochaines étapes:")
    print("1. Exécutez le SQL dans l'éditeur SQL de Supabase")
    print("2. Exécutez: python migrate-to-supabase.py")
    print("3. Exécutez: wrangler deploy --env production")
    
    print("\n🎉 Configuration Supabase terminée !")

if __name__ == "__main__":
    main()
