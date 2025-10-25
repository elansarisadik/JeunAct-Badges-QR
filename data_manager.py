import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class DataManager:
    """Gestionnaire de données JSON pour remplacer SQLite"""
    
    def __init__(self, data_file: str = "data/members.json"):
        self.data_file = data_file
        self.ensure_data_file()
    
    def ensure_data_file(self):
        """S'assure que le fichier de données existe"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            self.save_data({"members": [], "next_id": 1})
    
    def load_data(self) -> Dict:
        """Charge les données depuis le fichier JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"members": [], "next_id": 1}
    
    def save_data(self, data: Dict):
        """Sauvegarde les données dans le fichier JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_all_members(self) -> List[Dict]:
        """Récupère tous les membres"""
        data = self.load_data()
        return data.get("members", [])
    
    def get_member_by_id(self, member_id: int) -> Optional[Dict]:
        """Récupère un membre par son ID"""
        members = self.get_all_members()
        for member in members:
            if member.get("id") == member_id:
                return member
        return None
    
    def add_member(self, member_data: Dict) -> Dict:
        """Ajoute un nouveau membre"""
        data = self.load_data()
        members = data.get("members", [])
        next_id = data.get("next_id", 1)
        
        # Générer le numéro de membre
        member_count = len(members)
        member_number = f"MEM{member_count + 1:03d}"
        
        new_member = {
            "id": next_id,
            "member_number": member_number,
            **member_data,
            "created_at": datetime.now().isoformat()
        }
        
        members.append(new_member)
        data["members"] = members
        data["next_id"] = next_id + 1
        
        self.save_data(data)
        return new_member
    
    def update_member(self, member_id: int, member_data: Dict) -> Optional[Dict]:
        """Met à jour un membre existant"""
        data = self.load_data()
        members = data.get("members", [])
        
        for i, member in enumerate(members):
            if member.get("id") == member_id:
                # Préserver l'ID et le numéro de membre
                updated_member = {**member, **member_data}
                updated_member["id"] = member_id
                updated_member["member_number"] = member.get("member_number")
                members[i] = updated_member
                data["members"] = members
                self.save_data(data)
                return updated_member
        
        return None
    
    def delete_member(self, member_id: int) -> bool:
        """Supprime un membre"""
        data = self.load_data()
        members = data.get("members", [])
        
        for i, member in enumerate(members):
            if member.get("id") == member_id:
                del members[i]
                data["members"] = members
                self.save_data(data)
                return True
        
        return False
    
    def generate_member_number(self) -> str:
        """Génère un numéro de membre unique"""
        members = self.get_all_members()
        member_count = len(members)
        return f"MEM{member_count + 1:03d}"
