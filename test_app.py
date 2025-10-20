#!/usr/bin/env python3
"""
Script de test pour vérifier l'application JeunAct
"""
import sys
import os

def test_imports():
    """Teste si tous les modules nécessaires sont disponibles"""
    print("🔍 Test des imports...")
    
    try:
        import flask
        print("✅ Flask disponible")
    except ImportError:
        print("❌ Flask non disponible - Installez avec: pip install flask")
        return False
    
    try:
        import flask_sqlalchemy
        print("✅ Flask-SQLAlchemy disponible")
    except ImportError:
        print("❌ Flask-SQLAlchemy non disponible - Installez avec: pip install flask-sqlalchemy")
        return False
    
    try:
        import qrcode
        print("✅ QRCode disponible")
    except ImportError:
        print("❌ QRCode non disponible - Installez avec: pip install qrcode")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow disponible")
    except ImportError:
        print("❌ Pillow non disponible - Installez avec: pip install pillow")
        return False
    
    return True

def test_database():
    """Teste la création de la base de données"""
    print("\n🗄️ Test de la base de données...")
    
    try:
        import sqlite3
        conn = sqlite3.connect('jeunact_members.db')
        cursor = conn.cursor()
        
        # Créer la table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ajouter un membre de test
        cursor.execute('''
            INSERT OR IGNORE INTO members (member_number, full_name, role, email, whatsapp, instagram, linkedin, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'MEM001',
            'Jean Dupont',
            'Bureau',
            'jean.dupont@jeunact.org',
            '33123456789',
            'jean_dupont',
            'https://linkedin.com/in/jean-dupont',
            'Président de l\'association JeunAct'
        ))
        
        conn.commit()
        conn.close()
        print("✅ Base de données créée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def main():
    print("🚀 Test de l'application JeunAct\n")
    
    # Test des imports
    if not test_imports():
        print("\n❌ Certains modules manquent. Installez-les avec:")
        print("pip install flask flask-sqlalchemy qrcode pillow")
        return False
    
    # Test de la base de données
    if not test_database():
        print("\n❌ Problème avec la base de données")
        return False
    
    print("\n✅ Tous les tests sont passés !")
    print("\n🎯 Pour lancer l'application:")
    print("1. Ouvrez un terminal")
    print("2. Naviguez vers le dossier QR-Code")
    print("3. Lancez: python app.py")
    print("4. Ouvrez http://localhost:5000 dans votre navigateur")
    
    return True

if __name__ == '__main__':
    main()
