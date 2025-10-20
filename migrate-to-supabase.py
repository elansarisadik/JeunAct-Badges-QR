#!/usr/bin/env python3
"""
Script de migration des données SQLite vers Supabase PostgreSQL
QR Code Jeunact - Migration Cloudflare
"""

import sqlite3
import psycopg2
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def connect_sqlite():
    """Connexion à la base SQLite existante"""
    try:
        conn = sqlite3.connect('instance/jeunact_members.db')
        return conn
    except Exception as e:
        print(f"❌ Erreur connexion SQLite: {e}")
        return None

def connect_postgresql(database_url):
    """Connexion à Supabase PostgreSQL"""
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"❌ Erreur connexion PostgreSQL: {e}")
        return None

def create_postgresql_tables(conn):
    """Créer les tables dans PostgreSQL"""
    cursor = conn.cursor()
    
    # Créer la table members
    create_table_sql = """
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
    """
    
    # Créer les index
    create_indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_member_number ON members(member_number);",
        "CREATE INDEX IF NOT EXISTS idx_full_name ON members(full_name);",
        "CREATE INDEX IF NOT EXISTS idx_role ON members(role);"
    ]
    
    try:
        cursor.execute(create_table_sql)
        for index_sql in create_indexes_sql:
            cursor.execute(index_sql)
        conn.commit()
        print("✅ Tables PostgreSQL créées avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur création tables: {e}")
        conn.rollback()
        return False

def migrate_data(sqlite_conn, postgres_conn):
    """Migrer les données de SQLite vers PostgreSQL"""
    sqlite_cursor = sqlite_conn.cursor()
    postgres_cursor = postgres_conn.cursor()
    
    try:
        # Récupérer toutes les données de SQLite
        sqlite_cursor.execute("SELECT * FROM member")
        members = sqlite_cursor.fetchall()
        
        print(f"📊 {len(members)} membres trouvés dans SQLite")
        
        # Préparer la requête d'insertion PostgreSQL
        insert_sql = """
        INSERT INTO members (
            member_number, full_name, role, position, email, whatsapp,
            instagram, linkedin, tiktok, portfolio, photo, integration_date, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (member_number) DO UPDATE SET
            full_name = EXCLUDED.full_name,
            role = EXCLUDED.role,
            position = EXCLUDED.position,
            email = EXCLUDED.email,
            whatsapp = EXCLUDED.whatsapp,
            instagram = EXCLUDED.instagram,
            linkedin = EXCLUDED.linkedin,
            tiktok = EXCLUDED.tiktok,
            portfolio = EXCLUDED.portfolio,
            photo = EXCLUDED.photo,
            integration_date = EXCLUDED.integration_date,
            created_at = EXCLUDED.created_at
        """
        
        # Migrer chaque membre
        migrated_count = 0
        for member in members:
            try:
                # Convertir les données (SQLite -> PostgreSQL)
                member_data = (
                    member[1],  # member_number
                    member[2],  # full_name
                    member[3],  # role
                    member[4],  # position
                    member[5],  # email
                    member[6],  # whatsapp
                    member[7],  # instagram
                    member[8],  # linkedin
                    member[9],  # tiktok
                    member[10], # portfolio
                    member[11], # photo
                    member[12], # integration_date
                    member[13]  # created_at
                )
                
                postgres_cursor.execute(insert_sql, member_data)
                migrated_count += 1
                
            except Exception as e:
                print(f"⚠️  Erreur migration membre {member[1]}: {e}")
                continue
        
        postgres_conn.commit()
        print(f"✅ {migrated_count} membres migrés avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur migration: {e}")
        postgres_conn.rollback()
        return False

def verify_migration(postgres_conn):
    """Vérifier que la migration s'est bien passée"""
    cursor = postgres_conn.cursor()
    
    try:
        # Compter les membres
        cursor.execute("SELECT COUNT(*) FROM members")
        count = cursor.fetchone()[0]
        
        # Afficher quelques exemples
        cursor.execute("SELECT member_number, full_name, role FROM members LIMIT 5")
        examples = cursor.fetchall()
        
        print(f"📊 Vérification: {count} membres dans PostgreSQL")
        print("📋 Exemples de membres migrés:")
        for example in examples:
            print(f"   • {example[0]} - {example[1]} ({example[2]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")
        return False

def main():
    print("🚀 Migration SQLite vers Supabase PostgreSQL")
    print("=" * 50)
    
    # Vérifier que l'URL de base de données est fournie
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ Variable DATABASE_URL non définie")
        print("💡 Ajoutez votre URL Supabase dans .env ou wrangler.toml")
        sys.exit(1)
    
    # Connexions
    print("🔌 Connexion aux bases de données...")
    sqlite_conn = connect_sqlite()
    postgres_conn = connect_postgresql(database_url)
    
    if not sqlite_conn or not postgres_conn:
        print("❌ Impossible de se connecter aux bases de données")
        sys.exit(1)
    
    try:
        # Créer les tables PostgreSQL
        if not create_postgresql_tables(postgres_conn):
            sys.exit(1)
        
        # Migrer les données
        if not migrate_data(sqlite_conn, postgres_conn):
            sys.exit(1)
        
        # Vérifier la migration
        if not verify_migration(postgres_conn):
            sys.exit(1)
        
        print("\n🎉 Migration terminée avec succès !")
        print("✅ Vos données sont maintenant dans Supabase PostgreSQL")
        print("🚀 Prêt pour le déploiement Cloudflare Workers")
        
    finally:
        # Fermer les connexions
        if sqlite_conn:
            sqlite_conn.close()
        if postgres_conn:
            postgres_conn.close()

if __name__ == "__main__":
    main()
