#!/usr/bin/env python3
"""
Script de debug pour l'application JeunAct
"""
import sys
import os

print("🔍 Debug de l'application JeunAct")
print("=" * 50)

# Test des imports
print("1. Test des imports...")
try:
    from flask import Flask
    print("✅ Flask importé")
except ImportError as e:
    print(f"❌ Erreur Flask: {e}")
    sys.exit(1)

try:
    from flask_sqlalchemy import SQLAlchemy
    print("✅ Flask-SQLAlchemy importé")
except ImportError as e:
    print(f"❌ Erreur Flask-SQLAlchemy: {e}")
    sys.exit(1)

# Test de l'application
print("\n2. Test de l'application...")
try:
    from app import app, db
    print("✅ Application importée")
except Exception as e:
    print(f"❌ Erreur import app: {e}")
    sys.exit(1)

# Test de la base de données
print("\n3. Test de la base de données...")
try:
    with app.app_context():
        db.create_all()
        print("✅ Base de données créée")
        
        # Vérifier la structure
        from app import Member
        print("✅ Modèle Member importé")
        
        # Lister les colonnes
        import sqlite3
        conn = sqlite3.connect('jeunact_members.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(members)")
        columns = cursor.fetchall()
        print("📋 Colonnes de la table:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        conn.close()
        
except Exception as e:
    print(f"❌ Erreur base de données: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Debug terminé")
