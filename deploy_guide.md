# Guide de Déploiement - JeunAct Badges QR

## 🚀 Déploiement en Ligne

### Option 1: Railway (Recommandé - Gratuit et Simple)

#### Étape 1: Préparation
1. Créez un compte sur [Railway.app](https://railway.app)
2. Connectez votre compte GitHub

#### Étape 2: Configuration du Projet
1. Créez un nouveau projet sur Railway
2. Connectez votre repository GitHub
3. Railway détectera automatiquement votre application Flask

#### Étape 3: Variables d'Environnement
Dans Railway, ajoutez ces variables d'environnement :
```
FLASK_ENV=production
SECRET_KEY=votre-clé-secrète-très-longue-et-complexe
```

#### Étape 4: Déploiement
Railway déploiera automatiquement votre application !

### Option 2: Heroku (Classique)

#### Étape 1: Installation Heroku CLI
1. Téléchargez Heroku CLI depuis [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
2. Installez et connectez-vous

#### Étape 2: Préparation
```bash
# Dans votre dossier QR-Code
heroku create jeunact-badges-qr
```

#### Étape 3: Variables d'Environnement
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=votre-clé-secrète-très-longue-et-complexe
```

#### Étape 4: Déploiement
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Option 3: Vercel (Avec modifications)

Vercel nécessite quelques modifications pour Flask.

## 🔧 Configuration Requise

### 1. Modifier l'URL des QR Codes
Le fichier `app.py` doit être modifié pour utiliser l'URL de production.

### 2. Base de Données
- Railway/Heroku utilisent PostgreSQL en production
- Modification nécessaire du fichier de configuration

### 3. Fichiers Statiques
- Les photos doivent être stockées dans un service cloud (AWS S3, Cloudinary)
- Ou utiliser un stockage persistant

## 📱 Test des QR Codes

Une fois déployé :
1. Générez un QR code depuis l'interface admin
2. Scannez le QR code avec votre téléphone
3. Vérifiez que vous êtes redirigé vers le profil du membre

## 🌐 URL de Production

Après déploiement, votre URL sera :
- Railway: `https://votre-projet.railway.app`
- Heroku: `https://jeunact-badges-qr.herokuapp.com`

Les QR codes pointeront automatiquement vers cette URL.
