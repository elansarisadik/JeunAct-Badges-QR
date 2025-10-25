#!/usr/bin/env python3
"""
Interface d'administration simple pour gérer les membres
Usage: python admin_simple.py
"""

import os
import sys
from data_manager import DataManager
from datetime import datetime

class AdminInterface:
    def __init__(self):
        self.data_manager = DataManager()
    
    def show_menu(self):
        """Affiche le menu principal"""
        print("\n" + "="*50)
        print("🔧 ADMINISTRATION JEUNACT - BADGES QR")
        print("="*50)
        print("1. 📋 Voir tous les membres")
        print("2. ➕ Ajouter un membre")
        print("3. ✏️  Modifier un membre")
        print("4. 🗑️  Supprimer un membre")
        print("5. 🔄 Générer les pages statiques")
        print("6. 🚀 Déployer (générer + commit)")
        print("0. ❌ Quitter")
        print("="*50)
    
    def list_members(self):
        """Affiche la liste des membres"""
        members = self.data_manager.get_all_members()
        
        if not members:
            print("❌ Aucun membre trouvé.")
            return
        
        print(f"\n📋 Liste des membres ({len(members)}):")
        print("-" * 80)
        for member in members:
            role_badge = "👑" if member.get('role') == 'Bureau' else "👤"
            position = f" ({member.get('position', '')})" if member.get('position') else ""
            print(f"{role_badge} {member.get('full_name', 'N/A')}{position}")
            print(f"   ID: {member.get('id')} | Numéro: {member.get('member_number')}")
            print(f"   Email: {member.get('email', 'Non renseigné')}")
            print("-" * 80)
    
    def add_member(self):
        """Ajoute un nouveau membre"""
        print("\n➕ AJOUT D'UN NOUVEAU MEMBRE")
        print("-" * 40)
        
        # Informations obligatoires
        full_name = input("Nom complet: ").strip()
        if not full_name:
            print("❌ Le nom est obligatoire.")
            return
        
        print("\nRôle:")
        print("1. Bureau")
        print("2. Membre")
        role_choice = input("Choix (1-2): ").strip()
        role = "Bureau" if role_choice == "1" else "Membre"
        
        position = None
        if role == "Bureau":
            position = input("Poste au bureau: ").strip()
        
        # Informations optionnelles
        email = input("Email (optionnel): ").strip() or None
        whatsapp = input("WhatsApp (optionnel): ").strip() or None
        instagram = input("Instagram (optionnel): ").strip() or None
        linkedin = input("LinkedIn (optionnel): ").strip() or None
        tiktok = input("TikTok (optionnel): ").strip() or None
        portfolio = input("Portfolio (optionnel): ").strip() or None
        photo = input("Nom du fichier photo (optionnel): ").strip() or None
        
        # Date d'intégration
        integration_date = input("Date d'intégration (YYYY-MM-DD, optionnel): ").strip()
        if not integration_date:
            integration_date = datetime.now().strftime('%Y-%m-%d')
        
        # Préparation des données
        member_data = {
            'full_name': full_name,
            'role': role,
            'email': email,
            'whatsapp': whatsapp,
            'instagram': instagram,
            'linkedin': linkedin,
            'tiktok': tiktok,
            'portfolio': portfolio,
            'photo': photo,
            'position': position,
            'integration_date': integration_date
        }
        
        try:
            new_member = self.data_manager.add_member(member_data)
            print(f"\n✅ Membre ajouté avec succès !")
            print(f"   ID: {new_member['id']}")
            print(f"   Numéro: {new_member['member_number']}")
            print(f"   Nom: {new_member['full_name']}")
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout: {e}")
    
    def edit_member(self):
        """Modifie un membre existant"""
        print("\n✏️ MODIFICATION D'UN MEMBRE")
        print("-" * 40)
        
        # Afficher la liste des membres
        members = self.data_manager.get_all_members()
        if not members:
            print("❌ Aucun membre trouvé.")
            return
        
        print("\nMembres disponibles:")
        for member in members:
            print(f"ID {member['id']}: {member['full_name']} ({member['member_number']})")
        
        try:
            member_id = int(input("\nID du membre à modifier: "))
        except ValueError:
            print("❌ ID invalide.")
            return
        
        member = self.data_manager.get_member_by_id(member_id)
        if not member:
            print("❌ Membre non trouvé.")
            return
        
        print(f"\nModification de: {member['full_name']}")
        print("(Appuyez sur Entrée pour conserver la valeur actuelle)")
        
        # Modification des champs
        new_name = input(f"Nom complet [{member['full_name']}]: ").strip()
        if new_name:
            member['full_name'] = new_name
        
        print("\nRôle:")
        print("1. Bureau")
        print("2. Membre")
        role_choice = input(f"Choix (1-2) [actuel: {member['role']}]: ").strip()
        if role_choice:
            member['role'] = "Bureau" if role_choice == "1" else "Membre"
        
        if member['role'] == "Bureau":
            new_position = input(f"Poste au bureau [{member.get('position', '')}]: ").strip()
            if new_position:
                member['position'] = new_position
        
        # Autres champs
        new_email = input(f"Email [{member.get('email', '')}]: ").strip()
        if new_email:
            member['email'] = new_email
        
        new_whatsapp = input(f"WhatsApp [{member.get('whatsapp', '')}]: ").strip()
        if new_whatsapp:
            member['whatsapp'] = new_whatsapp
        
        new_instagram = input(f"Instagram [{member.get('instagram', '')}]: ").strip()
        if new_instagram:
            member['instagram'] = new_instagram
        
        new_linkedin = input(f"LinkedIn [{member.get('linkedin', '')}]: ").strip()
        if new_linkedin:
            member['linkedin'] = new_linkedin
        
        new_tiktok = input(f"TikTok [{member.get('tiktok', '')}]: ").strip()
        if new_tiktok:
            member['tiktok'] = new_tiktok
        
        new_portfolio = input(f"Portfolio [{member.get('portfolio', '')}]: ").strip()
        if new_portfolio:
            member['portfolio'] = new_portfolio
        
        new_photo = input(f"Photo [{member.get('photo', '')}]: ").strip()
        if new_photo:
            member['photo'] = new_photo
        
        try:
            updated_member = self.data_manager.update_member(member_id, member)
            if updated_member:
                print(f"\n✅ Membre modifié avec succès !")
            else:
                print("❌ Erreur lors de la modification.")
        except Exception as e:
            print(f"❌ Erreur lors de la modification: {e}")
    
    def delete_member(self):
        """Supprime un membre"""
        print("\n🗑️ SUPPRESSION D'UN MEMBRE")
        print("-" * 40)
        
        # Afficher la liste des membres
        members = self.data_manager.get_all_members()
        if not members:
            print("❌ Aucun membre trouvé.")
            return
        
        print("\nMembres disponibles:")
        for member in members:
            print(f"ID {member['id']}: {member['full_name']} ({member['member_number']})")
        
        try:
            member_id = int(input("\nID du membre à supprimer: "))
        except ValueError:
            print("❌ ID invalide.")
            return
        
        member = self.data_manager.get_member_by_id(member_id)
        if not member:
            print("❌ Membre non trouvé.")
            return
        
        confirm = input(f"\n⚠️  Êtes-vous sûr de vouloir supprimer {member['full_name']} ? (oui/non): ").strip().lower()
        if confirm in ['oui', 'o', 'yes', 'y']:
            try:
                if self.data_manager.delete_member(member_id):
                    print(f"✅ Membre {member['full_name']} supprimé avec succès !")
                else:
                    print("❌ Erreur lors de la suppression.")
            except Exception as e:
                print(f"❌ Erreur lors de la suppression: {e}")
        else:
            print("❌ Suppression annulée.")
    
    def generate_static_pages(self):
        """Génère les pages statiques"""
        print("\n🔄 GÉNÉRATION DES PAGES STATIQUES")
        print("-" * 40)
        
        try:
            from static_generator import StaticGenerator
            generator = StaticGenerator()
            generator.generate_all()
            print("✅ Pages statiques générées avec succès !")
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
    
    def deploy(self):
        """Déploie l'application (génère + commit)"""
        print("\n🚀 DÉPLOIEMENT")
        print("-" * 40)
        
        # Générer les pages statiques
        self.generate_static_pages()
        
        # Instructions pour le commit
        print("\n📝 Pour finaliser le déploiement:")
        print("1. git add .")
        print("2. git commit -m 'Update members and regenerate static pages'")
        print("3. git push origin main")
        print("\n🌐 Les pages seront automatiquement déployées sur GitHub Pages")
    
    def run(self):
        """Lance l'interface d'administration"""
        while True:
            self.show_menu()
            choice = input("\nVotre choix: ").strip()
            
            if choice == "1":
                self.list_members()
            elif choice == "2":
                self.add_member()
            elif choice == "3":
                self.edit_member()
            elif choice == "4":
                self.delete_member()
            elif choice == "5":
                self.generate_static_pages()
            elif choice == "6":
                self.deploy()
            elif choice == "0":
                print("\n👋 Au revoir !")
                break
            else:
                print("❌ Choix invalide.")
            
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == '__main__':
    admin = AdminInterface()
    admin.run()
