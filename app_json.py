from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import qrcode
import io
import base64
import os
import json
from data_manager import DataManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Initialisation du gestionnaire de données
data_manager = DataManager()

# Fonctions d'authentification
def is_admin():
    """Vérifie si l'utilisateur est connecté en tant qu'admin"""
    return session.get('is_admin', False)

def require_admin(f):
    """Décorateur pour protéger les routes admin"""
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash('Accès refusé. Connexion administrateur requise.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        # Mot de passe admin simple (à changer en production)
        if password == 'JeunAct2024Admin':
            session['is_admin'] = True
            flash('Connexion réussie !', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Mot de passe incorrect.', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@require_admin
def admin():
    members = data_manager.get_all_members()
    return render_template('admin.html', members=members)

@app.route('/member/<int:member_id>')
def member_profile(member_id):
    member = data_manager.get_member_by_id(member_id)
    if not member:
        flash('Membre non trouvé.', 'error')
        return redirect(url_for('index'))
    return render_template('member_profile.html', member=member)

@app.route('/add_member', methods=['GET', 'POST'])
@require_admin
def add_member():
    if request.method == 'POST':
        # Préparation des données du membre
        member_data = {
            'full_name': request.form['full_name'],
            'role': request.form['role'],
            'email': request.form.get('email'),
            'whatsapp': request.form.get('whatsapp'),
            'instagram': request.form.get('instagram'),
            'tiktok': request.form.get('tiktok'),
            'linkedin': request.form.get('linkedin'),
            'portfolio': request.form.get('portfolio'),
            'photo': request.form.get('photo'),
            'position': request.form.get('position') if request.form['role'] == 'Bureau' else None
        }
        
        # Gestion de la date d'intégration
        if request.form.get('integration_date'):
            member_data['integration_date'] = request.form['integration_date']
        
        try:
            new_member = data_manager.add_member(member_data)
            flash(f'Le membre "{new_member["full_name"]}" a été ajouté avec succès !', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            flash(f'Erreur lors de l\'ajout: {str(e)}', 'error')
    
    return render_template('add_member.html')

@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
@require_admin
def edit_member(member_id):
    member = data_manager.get_member_by_id(member_id)
    if not member:
        flash('Membre non trouvé.', 'error')
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        # Préparation des données mises à jour
        updated_data = {
            'full_name': request.form['full_name'],
            'role': request.form['role'],
            'email': request.form.get('email'),
            'whatsapp': request.form.get('whatsapp'),
            'instagram': request.form.get('instagram'),
            'tiktok': request.form.get('tiktok'),
            'linkedin': request.form.get('linkedin'),
            'portfolio': request.form.get('portfolio'),
            'photo': request.form.get('photo'),
            'position': request.form.get('position') if request.form['role'] == 'Bureau' else None
        }
        
        # Gestion de la date d'intégration
        if request.form.get('integration_date'):
            updated_data['integration_date'] = request.form['integration_date']
        
        try:
            updated_member = data_manager.update_member(member_id, updated_data)
            if updated_member:
                flash(f'Les informations du membre "{updated_member["full_name"]}" ont été mises à jour avec succès !', 'success')
            else:
                flash('Erreur lors de la mise à jour.', 'error')
            return redirect(url_for('admin'))
        except Exception as e:
            flash(f'Erreur lors de la modification: {str(e)}', 'error')
    
    return render_template('edit_member.html', member=member)

@app.route('/delete_member/<int:member_id>')
@require_admin
def delete_member(member_id):
    member = data_manager.get_member_by_id(member_id)
    if not member:
        flash('Membre non trouvé.', 'error')
        return redirect(url_for('admin'))
    
    try:
        if data_manager.delete_member(member_id):
            flash(f'Le membre "{member["full_name"]}" a été supprimé avec succès !', 'success')
        else:
            flash('Erreur lors de la suppression.', 'error')
    except Exception as e:
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/generate_qr/<int:member_id>')
@require_admin
def generate_qr(member_id):
    member = data_manager.get_member_by_id(member_id)
    if not member:
        flash('Membre non trouvé.', 'error')
        return redirect(url_for('admin'))
    
    # URL de base pour la production (GitHub Pages)
    base_url = "https://elansarisadq.github.io/JeunAct-Association"
    profile_url = f"{base_url}/member/{member_id}.html"
    
    # Génération du QR code
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

# API pour récupérer les membres (pour la page d'accueil)
@app.route('/api/members')
def api_members():
    members = data_manager.get_all_members()
    return jsonify({"members": members})

if __name__ == '__main__':
    # Configuration pour la production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
