#!/usr/bin/env python3
"""
Script pour corriger définitivement le problème de base de données
"""
import os
import sqlite3

def fix_database():
    print("🔧 Correction du problème de base de données...")
    
    # 1. Supprimer toutes les bases de données existantes
    for file in os.listdir('.'):
        if file.endswith('.db'):
            os.remove(file)
            print(f"🗑️ Supprimé: {file}")
    
    # 2. Créer la nouvelle base avec le bon schéma
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
    print("✅ Nouvelle base de données créée")
    
    # 3. Vérifier la structure
    conn = sqlite3.connect('jeunact_members.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(members)")
    columns = cursor.fetchall()
    
    print("\n📋 Structure de la table 'members':")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Vérifier si integration_date existe
    column_names = [col[1] for col in columns]
    if 'integration_date' in column_names:
        print("\n✅ Colonne 'integration_date' présente!")
        print("🎉 Base de données corrigée avec succès!")
        return True
    else:
        print("\n❌ Problème: colonne 'integration_date' manquante")
        return False
    
    conn.close()

if __name__ == '__main__':
    print("🚀 Correction de la base de données JeunAct")
    print("=" * 50)
    
    if fix_database():
        print("\n✅ Problème résolu! Vous pouvez maintenant lancer l'application:")
        print("   python app.py")
    else:
        print("\n❌ Échec de la correction")
