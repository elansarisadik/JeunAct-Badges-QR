#!/usr/bin/env python3
"""
Version simplifiée de l'application JeunAct pour test rapide
"""
import sqlite3
import json
from datetime import datetime

# Créer la base de données
def init_db():
    conn = sqlite3.connect('jeunact_members.db')
    cursor = conn.cursor()
    
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
    
    conn.commit()
    conn.close()
    print("✅ Base de données initialisée")

# Ajouter un membre de test
def add_test_member():
    conn = sqlite3.connect('jeunact_members.db')
    cursor = conn.cursor()
    
    # Vérifier si des membres existent déjà
    cursor.execute("SELECT COUNT(*) FROM members")
    count = cursor.fetchone()[0]
    
    if count == 0:
        cursor.execute('''
            INSERT INTO members (member_number, full_name, role, email, whatsapp, instagram, linkedin, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'MEM001',
            'Jean Dupont',
            'Bureau',
            'jean.dupont@jeunact.org',
            '33123456789',
            'jean_dupont',
            'https://linkedin.com/in/jean-dupont',
            'Président de l\'association JeunAct, passionné par l\'engagement des jeunes.'
        ))
        
        cursor.execute('''
            INSERT INTO members (member_number, full_name, role, email, whatsapp, instagram, linkedin, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'MEM002',
            'Marie Martin',
            'Membre',
            'marie.martin@jeunact.org',
            '33987654321',
            'marie_martin',
            'https://linkedin.com/in/marie-martin',
            'Membre active de JeunAct, spécialisée dans l\'organisation d\'événements.'
        ))
        
        conn.commit()
        print("✅ Membres de test ajoutés")
    
    conn.close()

if __name__ == '__main__':
    print("🚀 Initialisation de l'application JeunAct...")
    init_db()
    add_test_member()
    print("✅ Application prête !")
    print("\n📋 Pour tester l'application complète :")
    print("1. Installez les dépendances : pip install flask flask-sqlalchemy qrcode pillow")
    print("2. Lancez l'application : python app.py")
    print("3. Ouvrez http://localhost:5000 dans votre navigateur")
    print("\n🎯 Fonctionnalités disponibles :")
    print("- Gestion des membres")
    print("- Génération de QR codes")
    print("- Pages de profil avec liens sociaux")
    print("- Interface d'administration")
