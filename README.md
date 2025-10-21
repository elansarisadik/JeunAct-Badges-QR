# 🚀 QR Code Jeunact

Application Flask de gestion des membres avec génération de QR codes pour l'association JeunAct.

## ✨ Fonctionnalités

- 📱 Génération de QR codes pour les membres
- 👥 Gestion des membres (Bureau/Membres)
- 🔗 Profils avec réseaux sociaux
- 📊 Interface d'administration
- 🖼️ Gestion des photos de profil

## 🚀 Installation et utilisation

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
# Cloner le repository
git clone https://github.com/elansarisadik/JeunAct-Badges-QR.git
cd JeunAct-Badges-QR

# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier de configuration
cp env.example .env

# Éditer .env avec vos paramètres
# PRODUCTION_URL=https://votre-domaine.com
```

### Lancement
```bash
python app.py
```

L'application sera disponible sur : http://localhost:5000

## 🔧 Configuration

### Variables d'environnement (.env)

- `PRODUCTION_URL` : URL de production pour les QR codes
- `SECRET_KEY` : Clé secrète Flask
- `DATABASE_URL` : URL de base de données (optionnel, utilise SQLite par défaut)

## 📁 Structure du projet

```
├── app.py              # Application Flask principale
├── config.py           # Configuration
├── requirements.txt    # Dépendances Python
├── templates/          # Templates HTML
├── static/             # Fichiers statiques (CSS, images)
└── instance/           # Base de données SQLite
```

## 🎯 Utilisation

1. **Accueil** : Page principale avec informations
2. **Admin** : Interface d'administration (`/admin`)
3. **Ajouter membre** : Formulaire d'ajout (`/add_member`)
4. **Profil membre** : Page de profil (`/member/<id>`)
5. **QR Code** : Génération de QR code (`/generate_qr/<id>`)

## 📱 QR Codes

Les QR codes générés pointent vers les profils des membres et contiennent toutes les informations de contact.

## 🗄️ Base de données

L'application utilise SQLite par défaut, mais peut être configurée pour utiliser PostgreSQL ou MySQL.

---

**🚀 Développé avec ❤️ pour JeunAct**