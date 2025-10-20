#!/usr/bin/env python3
"""
Script pour mettre à jour la base de données avec les nouveaux champs
"""
import sqlite3
from datetime import datetime

def update_database():
    """Met à jour la base de données pour ajouter les nouveaux champs"""
    print("🔄 Mise à jour de la base de données...")
    
    try:
        conn = sqlite3.connect('instance/jeunact_members.db')
        cursor = conn.cursor()
        
        # Vérifier les colonnes existantes
        cursor.execute("PRAGMA table_info(member)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Ajouter la colonne integration_date si elle n'existe pas
        if 'integration_date' not in columns:
            cursor.execute("ALTER TABLE member ADD COLUMN integration_date DATE")
            print("✅ Colonne 'integration_date' ajoutée")
            
            # Mettre à jour les membres existants avec une date d'intégration par défaut
            cursor.execute("SELECT id, created_at FROM member WHERE integration_date IS NULL")
            members = cursor.fetchall()
            
            for member_id, created_at in members:
                if created_at:
                    try:
                        created_date = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f').date()
                        cursor.execute("UPDATE member SET integration_date = ? WHERE id = ?", 
                                     (created_date, member_id))
                    except ValueError:
                        cursor.execute("UPDATE member SET integration_date = ? WHERE id = ?", 
                                     (datetime.now().date(), member_id))
            
            print(f"✅ {len(members)} membres mis à jour avec une date d'intégration")
        else:
            print("✅ Colonne 'integration_date' existe déjà")
        
        # Ajouter la colonne tiktok si elle n'existe pas
        if 'tiktok' not in columns:
            cursor.execute("ALTER TABLE member ADD COLUMN tiktok VARCHAR(100)")
            print("✅ Colonne 'tiktok' ajoutée")
        else:
            print("✅ Colonne 'tiktok' existe déjà")
        
        # Ajouter la colonne portfolio si elle n'existe pas
        if 'portfolio' not in columns:
            cursor.execute("ALTER TABLE member ADD COLUMN portfolio VARCHAR(200)")
            print("✅ Colonne 'portfolio' ajoutée")
        else:
            print("✅ Colonne 'portfolio' existe déjà")
        
        # Ajouter la colonne position si elle n'existe pas
        if 'position' not in columns:
            cursor.execute("ALTER TABLE member ADD COLUMN position VARCHAR(50)")
            print("✅ Colonne 'position' ajoutée")
        else:
            print("✅ Colonne 'position' existe déjà")
        
        conn.commit()
        conn.close()
        print("✅ Base de données mise à jour avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Mise à jour de la base de données JeunAct")
    print("=" * 50)
    
    if update_database():
        print("\n🎉 Mise à jour terminée!")
        print("Nouveaux champs ajoutés:")
        print("  - TikTok (nom d'utilisateur)")
        print("  - Portfolio (lien vers site web)")
        print("  - Date d'intégration")
        print("  - Position (poste au bureau)")
    else:
        print("\n❌ Échec de la mise à jour")
        print("Vérifiez les permissions de la base de données")