import os
import json
from datetime import datetime
from data_manager import DataManager
from jinja2 import Environment, FileSystemLoader

class StaticGenerator:
    """Générateur de pages statiques pour GitHub Pages"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.template_env = Environment(loader=FileSystemLoader('templates'))
        self.base_url = "https://elansarisadq.github.io/JeunAct-Association"
    
    def generate_member_pages(self):
        """Génère les pages HTML statiques pour tous les membres"""
        members = self.data_manager.get_all_members()
        
        # Créer le dossier member s'il n'existe pas
        os.makedirs('member', exist_ok=True)
        
        for member in members:
            self.generate_single_member_page(member)
        
        print(f"✅ {len(members)} pages de membres générées")
    
    def generate_single_member_page(self, member):
        """Génère une page HTML statique pour un membre"""
        template = self.template_env.get_template('member_profile_static.html')
        
        # Préparer les données pour le template
        member_data = {
            'member': member,
            'url_for': self.url_for_static,
            'static': 'static'
        }
        
        # Générer le HTML
        html_content = template.render(**member_data)
        
        # Sauvegarder dans le fichier
        filename = f"member/{member['id']}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 Page générée: {filename}")
    
    def url_for_static(self, endpoint, filename=None, _external=True):
        """Simule url_for('static', filename=filename) pour les templates statiques"""
        if endpoint == 'static':
            return f"{self.base_url}/static/{filename}"
        return f"{self.base_url}/{endpoint}"
    
    def generate_index_page(self):
        """Génère la page d'accueil avec la liste des membres"""
        members = self.data_manager.get_all_members()
        
        # Lire le template index.html
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer le JavaScript pour charger les membres
        members_json = json.dumps(members, ensure_ascii=False)
        
        # Script pour charger les membres depuis les données JSON
        script_content = f"""
    // Charger et afficher les membres
    async function loadMembers() {{
        try {{
            const members = {members_json};
            const membersList = document.getElementById('membersList');
            
            membersList.innerHTML = '';
            
            members.forEach(member => {{
                const memberCard = `
                    <div class="col-lg-4 col-md-6 mb-4">
                        <div class="card member-card">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start mb-3">
                                    <h5 class="card-title mb-0" style="color: white;">${{member.full_name}}</h5>
                                    <span class="badge" style="background: ${{member.role === 'Bureau' ? 'linear-gradient(135deg, #FFD700, #FFA500); color: #000000;' : 'rgba(255,255,255,0.2); color: white;'}} border: 2px solid rgba(255,255,255,0.3); font-size: 0.8rem; padding: 8px 12px; border-radius: 20px;">
                                        ${{member.role === 'Bureau' && member.position ? member.position : member.role}}
                                    </span>
                                </div>
                                <p class="mb-2" style="color: rgba(255,255,255,0.8);">
                                    <i class="fas fa-hashtag me-1"></i>#${{member.member_number}}
                                </p>
                                ${{member.email ? `<p class="mb-2" style="color: rgba(255,255,255,0.8);">
                                    <i class="fas fa-envelope me-1" style="color: #EA4335;"></i>${{member.email}}
                                </p>` : ''}}
                                <div class="d-flex flex-wrap gap-2 mb-3">
                                    ${{member.whatsapp ? `<span class="badge" style="background: #25D366; color: white; border: none;">
                                        <i class="fab fa-whatsapp me-1"></i>WhatsApp
                                    </span>` : ''}}
                                    ${{member.instagram ? `<span class="badge" style="background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); color: white; border: none;">
                                        <i class="fab fa-instagram me-1"></i>Instagram
                                    </span>` : ''}}
                                    ${{member.linkedin ? `<span class="badge" style="background: #0077b5; color: white; border: none;">
                                        <i class="fab fa-linkedin me-1"></i>LinkedIn
                                    </span>` : ''}}
                                </div>
                                <div class="btn-group w-100" role="group">
                                    <a href="member/${{member.id}}.html" 
                                       class="btn btn-sm" target="_blank" style="background: white; color: #8B1538; border: none; font-weight: 500;">
                                        <i class="fas fa-eye me-1"></i>Voir
                                    </a>
                                    <button type="button" 
                                            class="btn btn-sm" 
                                            style="background: rgba(255,255,255,0.9); color: #8B1538; border: none; font-weight: 500;"
                                            onclick="generateQR(${{member.id}})">
                                        <i class="fas fa-qrcode me-1"></i>QR
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                membersList.innerHTML += memberCard;
            }});
        }} catch (error) {{
            console.error('Erreur lors du chargement des membres:', error);
        }}
    }}

    // Générer QR code
    function generateQR(memberId) {{
        // Rediriger vers l'interface admin pour générer le QR
        window.open('admin-simple.html', '_blank');
    }}

    // Charger les membres au chargement de la page
    document.addEventListener('DOMContentLoaded', loadMembers);
        """
        
        # Remplacer le script existant
        import re
        pattern = r'<script>.*?</script>'
        new_content = re.sub(pattern, f'<script>{script_content}</script>', content, flags=re.DOTALL)
        
        # Sauvegarder le fichier modifié
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("📄 Page d'accueil mise à jour")
    
    def generate_all(self):
        """Génère toutes les pages statiques"""
        print("🚀 Génération des pages statiques...")
        
        # Générer les pages des membres
        self.generate_member_pages()
        
        # Générer la page d'accueil
        self.generate_index_page()
        
        print("✅ Génération terminée !")

if __name__ == '__main__':
    generator = StaticGenerator()
    generator.generate_all()
