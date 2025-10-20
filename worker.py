from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import qrcode
import io
import base64
import os
import json
from dotenv import load_dotenv
from config import Config

# Configuration pour Cloudflare Workers
def create_app():
    app = Flask(__name__)
    
    # Configuration des variables d'environnement pour Cloudflare
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuration de la base de données pour Cloudflare
    # Cloudflare Workers utilise généralement des bases de données externes
    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    else:
        # Pour Cloudflare, utiliser une base de données externe (PostgreSQL recommandé)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/database'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    return app

app = create_app()
db = SQLAlchemy(app)

# Fonction pour générer automatiquement les numéros de membre
def generate_member_number():
    """Génère automatiquement un numéro de membre unique"""
    try:
        member_count = Member.query.count()
        next_number = member_count + 1
        return f"MEM{next_number:03d}"
    except Exception as e:
        # En cas d'erreur, retourner un numéro par défaut
        return f"MEM001"

# Modèle de données pour les membres
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_number = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'Bureau' ou 'Membre'
    position = db.Column(db.String(50), nullable=True)  # Poste au bureau
    email = db.Column(db.String(120), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    instagram = db.Column(db.String(100), nullable=True)
    linkedin = db.Column(db.String(200), nullable=True)
    tiktok = db.Column(db.String(100), nullable=True)
    portfolio = db.Column(db.String(200), nullable=True)
    photo = db.Column(db.String(200), nullable=True)
    integration_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Member {self.full_name}>'

# Routes principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    try:
        members = Member.query.all()
        return render_template('admin.html', members=members)
    except Exception as e:
        flash(f'Erreur lors du chargement des membres: {str(e)}', 'error')
        return render_template('admin.html', members=[])

@app.route('/member/<int:member_id>')
def member_profile(member_id):
    try:
        member = Member.query.get_or_404(member_id)
        return render_template('member_profile.html', member=member)
    except Exception as e:
        flash(f'Erreur lors du chargement du profil: {str(e)}', 'error')
        return redirect(url_for('admin'))

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        try:
            integration_date = None
            if request.form.get('integration_date'):
                integration_date = datetime.strptime(request.form['integration_date'], '%Y-%m-%d').date()
            
            member = Member(
                member_number=generate_member_number(),
                full_name=request.form['full_name'],
                role=request.form['role'],
                email=request.form.get('email'),
                whatsapp=request.form.get('whatsapp'),
                instagram=request.form.get('instagram'),
                tiktok=request.form.get('tiktok'),
                linkedin=request.form.get('linkedin'),
                portfolio=request.form.get('portfolio'),
                photo=request.form.get('photo'),
                integration_date=integration_date,
                position=request.form.get('position') if request.form['role'] == 'Bureau' else None
            )
            
            db.session.add(member)
            db.session.commit()
            flash(f'Le membre "{request.form["full_name"]}" a été ajouté avec succès !', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout: {str(e)}', 'error')
    
    return render_template('add_member.html')

@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    try:
        member = Member.query.get_or_404(member_id)
        
        if request.method == 'POST':
            member.full_name = request.form['full_name']
            member.role = request.form['role']
            member.position = request.form.get('position') if request.form['role'] == 'Bureau' else None
            member.email = request.form.get('email')
            member.whatsapp = request.form.get('whatsapp')
            member.instagram = request.form.get('instagram')
            member.tiktok = request.form.get('tiktok')
            member.linkedin = request.form.get('linkedin')
            member.portfolio = request.form.get('portfolio')
            member.photo = request.form.get('photo')
            
            if request.form.get('integration_date'):
                member.integration_date = datetime.strptime(request.form['integration_date'], '%Y-%m-%d').date()
            
            db.session.commit()
            flash(f'Les informations du membre "{member.full_name}" ont été mises à jour avec succès !', 'success')
            return redirect(url_for('admin'))
        
        return render_template('edit_member.html', member=member)
    except Exception as e:
        flash(f'Erreur lors de la modification: {str(e)}', 'error')
        return redirect(url_for('admin'))

@app.route('/delete_member/<int:member_id>')
def delete_member(member_id):
    try:
        member = Member.query.get_or_404(member_id)
        db.session.delete(member)
        db.session.commit()
        flash(f'Le membre "{member.full_name}" a été supprimé avec succès !', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/generate_qr/<int:member_id>')
def generate_qr(member_id):
    try:
        member = Member.query.get_or_404(member_id)
        
        # Utiliser l'URL de production configurée
        base_url = Config.get_base_url()
        profile_url = f"{base_url}/member/{member_id}"
        
        # Génération du QR code avec texte personnalisé
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(profile_url)
        qr.make(fit=True)
        
        # Création de l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Conversion en base64 pour l'affichage
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return render_template('qr_display.html', member=member, qr_code=img_str, profile_url=profile_url)
    except Exception as e:
        flash(f'Erreur lors de la génération du QR code: {str(e)}', 'error')
        return redirect(url_for('admin'))

# Fonction pour Cloudflare Workers
def handle_request(request):
    """Point d'entrée pour Cloudflare Workers"""
    try:
        # Initialiser la base de données si nécessaire
        with app.app_context():
            db.create_all()
        
        # Traiter la requête Flask
        with app.test_request_context(request.url, method=request.method, data=request.body):
            response = app.full_dispatch_request()
            
            return Response(
                response.get_data(),
                status=response.status_code,
                headers=dict(response.headers)
            )
    except Exception as e:
        return Response(
            json.dumps({'error': str(e)}),
            status=500,
            headers={'Content-Type': 'application/json'}
        )

# Configuration pour le développement local
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Configuration pour la production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
