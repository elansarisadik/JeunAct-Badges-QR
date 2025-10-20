# JeunAct - Système de Badges QR

Système complet de gestion de badges QR pour l'association JeunAct, permettant de scanner un QR code et d'accéder aux informations complètes des membres.

## Fonctionnalités

✅ **Gestion des Membres** : Ajout, modification et suppression des membres
✅ **QR Codes Personnalisés** : Génération automatique de QR codes pour chaque membre
✅ **Profils Complets** : Pages de profil avec toutes les informations du membre
✅ **Réseaux Sociaux** : Liens directs vers WhatsApp, Instagram, LinkedIn
✅ **Email Direct** : Ouverture automatique de l'application mail
✅ **Design Responsive** : Interface moderne et adaptée mobile
✅ **Base de Données** : Stockage sécurisé des informations

## Installation

### Prérequis
- Python 3.7+
- pip

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Configuration
1. Copiez le fichier `.env.example` vers `.env`
2. Modifiez la clé secrète dans le fichier `.env`

### Lancement
```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## Utilisation

### Administration
1. Accédez à `/admin` pour gérer les membres
2. Cliquez sur "Ajouter un Membre" pour créer un nouveau profil
3. Remplissez les informations (nom, rôle, contacts, réseaux sociaux)
4. Sauvegardez le membre

### Génération de QR Codes
1. Dans la liste des membres, cliquez sur "QR" pour un membre
2. Le QR code sera généré et affiché
3. Imprimez ou sauvegardez le QR code pour le badge

### Scan des QR Codes
1. Scannez le QR code avec n'importe quel appareil
2. L'utilisateur sera redirigé vers la page de profil du membre
3. Tous les liens de contact seront directement accessibles

## Structure du Projet

```
QR-Code/
├── app.py                 # Application principale Flask
├── config.py             # Configuration
├── requirements.txt      # Dépendances Python
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── admin.html
│   ├── member_profile.html
│   ├── add_member.html
│   ├── edit_member.html
│   └── qr_display.html
└── README.md
```

## Déploiement

### Heroku
1. Créez un compte Heroku
2. Installez Heroku CLI
3. Créez un nouveau projet Heroku
4. Configurez les variables d'environnement
5. Déployez avec `git push heroku main`

### VPS/Cloud
1. Installez Python et les dépendances sur votre serveur
2. Configurez un serveur web (Nginx + Gunicorn)
3. Configurez un domaine et SSL
4. Déployez l'application

## Base de Données

L'application utilise SQLite par défaut (fichier `jeunact_members.db`). Pour la production, vous pouvez configurer PostgreSQL ou MySQL en modifiant `SQLALCHEMY_DATABASE_URI` dans `config.py`.

## Personnalisation

- **Design** : Modifiez les styles dans `templates/base.html`
- **Champs** : Ajoutez de nouveaux champs dans le modèle `Member` dans `app.py`
- **Fonctionnalités** : Étendez l'application selon vos besoins

## Support

Pour toute question ou problème, contactez l'équipe de développement JeunAct.
