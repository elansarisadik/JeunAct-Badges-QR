#!/usr/bin/env python3
"""
Script pour gérer les photos des membres JeunAct
Corrige automatiquement les problèmes de noms de fichiers
"""

import sqlite3
import os
import shutil
from pathlib import Path

def clean_filename(filename):
    """Nettoie le nom de fichier en supprimant les espaces et caractères spéciaux"""
    # Supprime les espaces en début et fin
    filename = filename.strip()
    # Remplace les espaces par des underscores
    filename = filename.replace(' ', '_')
    # Supprime les caractères spéciaux
    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
    return filename

def list_photos_with_issues():
    """Liste les photos qui ont des problèmes de nommage"""
    photos_dir = Path("static/photos")
    if not photos_dir.exists():
        print("❌ Le dossier static/photos n'existe pas!")
        return []
    
    issues = []
    for file in photos_dir.iterdir():
        if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            original_name = file.name
            clean_name = clean_filename(original_name)
            if original_name != clean_name:
                issues.append((original_name, clean_name))
    
    return issues

def fix_photo_filenames():
    """Corrige automatiquement les noms de fichiers problématiques"""
    issues = list_photos_with_issues()
    
    if not issues:
        print("✅ Aucun problème de nommage détecté!")
        return
    
    print(f"🔧 {len(issues)} fichier(s) avec des problèmes de nommage détecté(s):")
    
    conn = sqlite3.connect('instance/jeunact_members.db')
    cursor = conn.cursor()
    
    for original_name, clean_name in issues:
        print(f"  📁 {original_name} → {clean_name}")
        
        # Renomme le fichier
        old_path = Path("static/photos") / original_name
        new_path = Path("static/photos") / clean_name
        
        try:
            shutil.move(str(old_path), str(new_path))
            print(f"    ✅ Fichier renommé")
            
            # Met à jour la base de données
            old_photo_path = f"photos/{original_name}"
            new_photo_path = f"photos/{clean_name}"
            
            cursor.execute('UPDATE member SET photo = ? WHERE photo = ?', 
                         (new_photo_path, old_photo_path))
            
            if cursor.rowcount > 0:
                print(f"    ✅ Base de données mise à jour ({cursor.rowcount} membre(s))")
            
        except Exception as e:
            print(f"    ❌ Erreur: {e}")
    
    conn.commit()
    conn.close()
    print("🎉 Correction terminée!")

def add_new_photo(photo_path, member_id=None):
    """Ajoute une nouvelle photo et la nettoie automatiquement"""
    if not os.path.exists(photo_path):
        print(f"❌ Le fichier {photo_path} n'existe pas!")
        return None
    
    # Génère un nom propre
    original_name = os.path.basename(photo_path)
    clean_name = clean_filename(original_name)
    
    # Copie le fichier vers static/photos
    destination = Path("static/photos") / clean_name
    shutil.copy2(photo_path, destination)
    
    photo_db_path = f"photos/{clean_name}"
    print(f"✅ Photo ajoutée: {photo_db_path}")
    
    # Si un member_id est fourni, met à jour directement
    if member_id:
        conn = sqlite3.connect('instance/jeunact_members.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE member SET photo = ? WHERE id = ?', 
                      (photo_db_path, member_id))
        conn.commit()
        conn.close()
        print(f"✅ Photo assignée au membre ID {member_id}")
    
    return photo_db_path

def show_current_status():
    """Affiche le statut actuel des photos"""
    print("📊 Statut actuel des photos:")
    print("=" * 50)
    
    # Photos disponibles
    photos_dir = Path("static/photos")
    if photos_dir.exists():
        photos = [f.name for f in photos_dir.iterdir() 
                 if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']]
        print(f"📸 Photos disponibles ({len(photos)}):")
        for photo in sorted(photos):
            print(f"  • {photo}")
    else:
        print("❌ Dossier static/photos introuvable")
    
    # Membres et leurs photos
    conn = sqlite3.connect('instance/jeunact_members.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, full_name, photo FROM member ORDER BY id')
    members = cursor.fetchall()
    conn.close()
    
    print(f"\n👥 Membres ({len(members)}):")
    for member in members:
        member_id, name, photo = member
        if photo:
            photo_exists = (photos_dir / photo.replace('photos/', '')).exists()
            status = "✅" if photo_exists else "❌"
            print(f"  ID {member_id}: {name} - {photo} {status}")
        else:
            print(f"  ID {member_id}: {name} - Pas de photo")

def main():
    print("🖼️  Gestionnaire de photos JeunAct")
    print("=" * 50)
    
    while True:
        print("\n🛠️  Options disponibles:")
        print("1. Voir le statut actuel")
        print("2. Corriger automatiquement les noms de fichiers")
        print("3. Ajouter une nouvelle photo")
        print("4. Quitter")
        
        choice = input("\nChoisissez une option (1-4): ").strip()
        
        if choice == '1':
            show_current_status()
        
        elif choice == '2':
            fix_photo_filenames()
        
        elif choice == '3':
            photo_path = input("Chemin vers la nouvelle photo: ").strip()
            member_id = input("ID du membre (optionnel, appuyez sur Entrée pour ignorer): ").strip()
            member_id = int(member_id) if member_id.isdigit() else None
            add_new_photo(photo_path, member_id)
        
        elif choice == '4':
            print("👋 Au revoir!")
            break
        
        else:
            print("❌ Option invalide!")

if __name__ == "__main__":
    main()
