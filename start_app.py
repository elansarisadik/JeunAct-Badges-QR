#!/usr/bin/env python3
"""
Script de démarrage qui force la recréation de la base de données
"""
import os
import sqlite3
from app import app, db, Member

def force_recreate_database():
    """Force la recréation de la base de données avec le bon schéma"""
    print("🔄 Recréation forcée de la base de données...")
    
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
    print("✅ Base de données recréée avec le bon schéma")
    
    # Vérifier la structure
    conn = sqlite3.connect('jeunact_members.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(members)")
    columns = cursor.fetchall()
    
    print("📋 Structure de la table:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
    return True

if __name__ == '__main__':
    print("🚀 Démarrage de l'application JeunAct")
    print("=" * 50)
    
    # Recréer la base de données
    force_recreate_database()
    
    # Démarrer l'application
    print("\n🌐 Lancement du serveur web...")
    print("📱 Accédez à http://localhost:5000")
    print("🔧 Administration: http://localhost:5000/admin")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
