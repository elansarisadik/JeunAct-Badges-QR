#!/usr/bin/env python3
"""
Script pour corriger et gérer les photos des membres JeunAct
"""

import sqlite3
import os
from pathlib import Path

def list_available_photos():
    """Liste toutes les photos disponibles dans static/photos"""
    photos_dir = Path("static/photos")
    if not photos_dir.exists():
        print("❌ Le dossier static/photos n'existe pas!")
        return []
    
    photos = []
    for file in photos_dir.iterdir():
        if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            photos.append(file.name)
    
    print("📸 Photos disponibles dans static/photos:")
    for i, photo in enumerate(photos, 1):
        print(f"  {i}. {photo}")
    
    return photos

def show_current_members():
    """Affiche les membres actuels et leurs photos"""
    conn = sqlite3.connect('instance/jeunact_members.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, full_name, photo FROM member ORDER BY id')
    members = cursor.fetchall()
    
    print("\n👥 Membres actuels:")
    for member in members:
        member_id, name, photo = member
        photo_status = "✅" if photo and photo.startswith('photos/') else "❌"
        print(f"  ID {member_id}: {name} - Photo: {photo} {photo_status}")
    
    conn.close()
    return members

def update_member_photo(member_id, photo_filename):
    """Met à jour la photo d'un membre"""
    if not photo_filename.startswith('photos/'):
        photo_filename = f"photos/{photo_filename}"
    
    conn = sqlite3.connect('instance/jeunact_members.db')
    cursor = conn.cursor()
    
    cursor.execute('UPDATE member SET photo = ? WHERE id = ?', (photo_filename, member_id))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"✅ Photo mise à jour pour le membre ID {member_id}: {photo_filename}")
    else:
        print(f"❌ Aucun membre trouvé avec l'ID {member_id}")
    
    conn.close()

def main():
    print("🔧 Script de gestion des photos JeunAct")
    print("=" * 50)
    
    # Lister les photos disponibles
    available_photos = list_available_photos()
    
    # Afficher les membres actuels
    members = show_current_members()
    
    if not members:
        print("\n❌ Aucun membre trouvé dans la base de données!")
        return
    
    print("\n🛠️  Options disponibles:")
    print("1. Mettre à jour la photo d'un membre existant")
    print("2. Voir les détails complets d'un membre")
    print("3. Quitter")
    
    while True:
        choice = input("\nChoisissez une option (1-3): ").strip()
        
        if choice == '1':
            try:
                member_id = int(input("Entrez l'ID du membre: "))
                if not any(m[0] == member_id for m in members):
                    print("❌ ID de membre invalide!")
                    continue
                
                print("\nPhotos disponibles:")
                for i, photo in enumerate(available_photos, 1):
                    print(f"  {i}. {photo}")
                
                photo_choice = input("Choisissez une photo (numéro ou nom): ").strip()
                
                if photo_choice.isdigit():
                    photo_index = int(photo_choice) - 1
                    if 0 <= photo_index < len(available_photos):
                        selected_photo = available_photos[photo_index]
                    else:
                        print("❌ Numéro de photo invalide!")
                        continue
                else:
                    selected_photo = photo_choice
                
                update_member_photo(member_id, selected_photo)
                
            except ValueError:
                print("❌ Veuillez entrer un numéro valide!")
        
        elif choice == '2':
            try:
                member_id = int(input("Entrez l'ID du membre: "))
                member = next((m for m in members if m[0] == member_id), None)
                if member:
                    print(f"\n📋 Détails du membre ID {member[0]}:")
                    print(f"  Nom: {member[1]}")
                    print(f"  Photo: {member[2]}")
                else:
                    print("❌ Membre non trouvé!")
            except ValueError:
                print("❌ Veuillez entrer un numéro valide!")
        
        elif choice == '3':
            print("👋 Au revoir!")
            break
        
        else:
            print("❌ Option invalide!")

if __name__ == "__main__":
    main()
