# JeunAct - Badges QR - Déploiement GitHub Pages

## 🚀 Déploiement Automatique sur GitHub Pages

Ce projet est configuré pour être déployé automatiquement sur GitHub Pages sans avoir besoin de services externes comme Vercel ou Render.

### 📋 Prérequis

- Un compte GitHub
- Un repository GitHub (public ou privé avec GitHub Pro)
- Python 3.9+ installé localement

### 🔧 Configuration Initiale

1. **Fork ou Clone ce repository**
   ```bash
   git clone https://github.com/votre-username/QR-Code.git
   cd QR-Code
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer GitHub Pages**
   - Allez dans Settings > Pages de votre repository
   - Source: "GitHub Actions"
   - Le workflow se déclenchera automatiquement

### 🎯 Utilisation

#### Interface d'Administration Simple

```bash
python admin_simple.py
```

Cette interface vous permet de :
- ✅ Voir tous les membres
- ✅ Ajouter un nouveau membre
- ✅ Modifier un membre existant
- ✅ Supprimer un membre
- ✅ Générer les pages statiques
- ✅ Déployer automatiquement

#### Déploiement Manuel

```bash
# Générer les pages statiques
python static_generator.py

# Ou utiliser le script de déploiement
python deploy_local.py
```

### 📁 Structure du Projet

```
QR-Code/
├── data/
│   └── members.json          # Base de données JSON
├── member/
│   ├── 1.html               # Pages des membres (générées)
│   └── 2.html
├── static/
│   ├── photos/              # Photos des membres
│   └── ...
├── templates/
│   ├── member_profile.html  # Template des profils
│   └── ...
├── .github/workflows/
│   └── deploy.yml           # GitHub Actions
├── data_manager.py          # Gestionnaire de données
├── static_generator.py      # Générateur de pages
├── admin_simple.py          # Interface d'administration
└── index.html               # Page d'accueil
```

### 🔄 Workflow de Déploiement

1. **Ajout/Modification d'un membre** via `admin_simple.py`
2. **Génération automatique** des pages statiques
3. **Commit et Push** vers GitHub
4. **Déploiement automatique** via GitHub Actions
5. **Site accessible** sur `https://votre-username.github.io/QR-Code`

### 🌐 URLs des Pages

- **Page d'accueil**: `https://votre-username.github.io/QR-Code/`
- **Profil membre**: `https://votre-username.github.io/QR-Code/member/1.html`
- **QR Code**: Pointe vers la page du membre

### 📱 Fonctionnalités

- ✅ **Pages statiques** compatibles GitHub Pages
- ✅ **Base de données JSON** (pas de serveur requis)
- ✅ **QR Codes** générés automatiquement
- ✅ **Interface d'administration** simple
- ✅ **Déploiement automatique** via GitHub Actions
- ✅ **Design responsive** et moderne
- ✅ **Réseaux sociaux** intégrés

### 🛠️ Personnalisation

#### Modifier l'URL de base

Dans `static_generator.py`, ligne 12 :
```python
self.base_url = "https://votre-username.github.io/QR-Code"
```

#### Ajouter des champs personnalisés

1. Modifier `data/members.json`
2. Mettre à jour `templates/member_profile.html`
3. Régénérer les pages : `python static_generator.py`

### 🔒 Sécurité

- **Mot de passe admin**: `JeunAct2024Admin` (à changer en production)
- **Données sensibles**: Stockées localement dans JSON
- **Accès**: Interface d'administration protégée

### 🐛 Dépannage

#### Problème de déploiement
```bash
# Vérifier les logs GitHub Actions
# Vérifier que tous les fichiers sont commités
git status
git add .
git commit -m "Fix deployment"
git push
```

#### Problème de génération
```bash
# Vérifier les dépendances
pip install -r requirements.txt

# Régénérer manuellement
python static_generator.py
```

#### Problème d'affichage
- Vérifier que les photos sont dans `static/photos/`
- Vérifier les chemins dans `data/members.json`

### 📞 Support

Pour toute question ou problème :
1. Vérifier les logs GitHub Actions
2. Tester localement avec `python admin_simple.py`
3. Vérifier la configuration GitHub Pages

### 🎉 Félicitations !

Votre site JeunAct est maintenant déployé sur GitHub Pages ! 

- 🌐 **URL**: `https://votre-username.github.io/QR-Code`
- 📱 **QR Codes**: Fonctionnels et pointent vers les profils
- 🔧 **Administration**: Simple et efficace
- 🚀 **Déploiement**: Automatique et gratuit
