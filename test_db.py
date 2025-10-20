#!/usr/bin/env python3
"""
Script de test pour vérifier la base de données
"""
import sqlite3
import os

def test_database():
    print("🔍 Test de la base de données...")
    
    if not os.path.exists('jeunact_members.db'):
        print("❌ Base de données non trouvée")
        return False
    
    try:
        conn = sqlite3.connect('jeunact_members.db')
        cursor = conn.cursor()
        
        # Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(members)")
        columns = cursor.fetchall()
        
        print("📋 Colonnes de la table 'members':")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Vérifier si integration_date existe
        column_names = [col[1] for col in columns]
        if 'integration_date' in column_names:
            print("✅ Colonne 'integration_date' trouvée!")
        else:
            print("❌ Colonne 'integration_date' manquante")
            return False
        
        conn.close()
        print("✅ Base de données OK!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == '__main__':
    test_database()
