# Configuration PythonAnywhere pour QR Code Jeunact

## 🚀 Déploiement sur PythonAnywhere (GRATUIT et 24/7)

### Avantages PythonAnywhere :
- ✅ **Gratuit** jusqu'à 3 applications web
- ✅ **Disponible 24/7** même PC éteint
- ✅ **Simple** à configurer
- ✅ **Support Python/Flask** natif
- ✅ **Base de données SQLite** incluse
- ✅ **Domaine personnalisé** possible

### Étapes de déploiement :

#### 1. Créer un compte PythonAnywhere
1. Allez sur [pythonanywhere.com](https://pythonanywhere.com)
2. Créez un compte gratuit
3. Confirmez votre email

#### 2. Uploader votre code
1. Dans le dashboard, cliquez sur "Files"
2. Créez un dossier : `JeunAct-Badges-QR`
3. Uploadez tous vos fichiers :
   - `app.py`
   - `config.py`
   - `requirements.txt`
   - `wsgi.py`
   - `templates/` (dossier complet)
   - `static/` (dossier complet)

#### 3. Installer les dépendances
1. Allez dans "Consoles" → "Bash"
2. Naviguez vers votre dossier :
   ```bash
   cd JeunAct-Badges-QR
   ```
3. Installez les dépendances :
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

#### 4. Configurer l'application web
1. Allez dans "Web" → "Add a new web app"
2. Choisissez "Manual configuration"
3. Choisissez "Python 3.10"
4. Dans "Source code" : `/home/votre-username/JeunAct-Badges-QR`
5. Dans "WSGI configuration file" : `/home/votre-username/JeunAct-Badges-QR/wsgi.py`

#### 5. Configurer les variables d'environnement
1. Dans "Web" → votre application
2. Allez dans "Environment variables"
3. Ajoutez :
   - `PRODUCTION_URL` = `https://votre-username.pythonanywhere.com`
   - `SECRET_KEY` = `JeunAct2024_QR_Code_SuperSecretKey`

#### 6. Redémarrer l'application
1. Cliquez sur "Reload" dans la section Web
2. Votre application sera disponible sur : `https://votre-username.pythonanywhere.com`

### 🎯 Résultat final :
- ✅ Application disponible 24/7
- ✅ QR codes pointent vers la vraie URL
- ✅ Profils accessibles depuis n'importe où
- ✅ Gratuit et permanent

### 📱 Test des QR codes :
1. Ajoutez des membres via `/admin`
2. Générez les QR codes via `/generate_qr/<id>`
3. Scannez avec votre téléphone
4. Le profil s'affiche sur l'URL permanente !

---

**🚀 PythonAnywhere est la solution parfaite pour votre besoin !**


