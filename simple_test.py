#!/usr/bin/env python3
"""
Test simple pour créer la base de données
"""
import sqlite3
import os

def create_database():
    print("🔄 Création de la base de données...")
    
    # Supprimer l'ancienne base si elle existe
    if os.path.exists('jeunact_members.db'):
        os.remove('jeunact_members.db')
        print("🗑️ Ancienne base supprimée")
    
    # Créer la nouvelle base avec le bon schéma
    conn = sqlite3.connect('jeunact_members.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_number TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT,
            whatsapp TEXT,
            instagram TEXT,
            linkedin TEXT,
            bio TEXT,
            photo TEXT,
            integration_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Base de données créée avec succès!")
    
    # Vérifier la structure
    conn = sqlite3.connect('jeunact_members.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(members)")
    columns = cursor.fetchall()
    
    print("\n📋 Structure de la table:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
    
    return True

if __name__ == '__main__':
    create_database()
