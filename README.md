# 🚀 QR Code Jeunact - Cloudflare Workers

Application Flask de gestion des membres avec génération de QR codes, déployée sur Cloudflare Workers pour une disponibilité 24/7.

## ✨ Fonctionnalités

- 📱 Génération de QR codes pour les membres
- 👥 Gestion des membres (Bureau/Membres)
- 🔗 Profils avec réseaux sociaux
- 📊 Interface d'administration
- ☁️ Déploiement Cloudflare Workers 24/7

## 🚀 Déploiement Rapide

### Via GitHub (Recommandé)

1. **Fork ce repository**
2. **Connectez GitHub à Cloudflare** :
   - Allez sur [dash.cloudflare.com](https://dash.cloudflare.com)
   - Workers & Pages → Create application
   - Connect to Git → Sélectionnez ce repository
3. **Configurez les variables d'environnement** :
   - `DATABASE_URL` : URL PostgreSQL Supabase
   - `SECRET_KEY` : Clé secrète Flask
   - `PRODUCTION_URL` : URL de votre application

### Déploiement Local

```bash
# Installer Wrangler
npm install -g wrangler

# Se connecter
wrangler login

# Déployer
wrangler deploy
```

## 🗄️ Base de données

Cette application utilise **Supabase PostgreSQL** :

1. Créez un projet sur [supabase.com](https://supabase.com)
2. Exécutez le SQL dans `supabase-schema.sql`
3. Configurez `DATABASE_URL` dans les variables d'environnement

## 📁 Structure

```
├── app.py              # Application Flask principale
├── worker.py           # Version Cloudflare Workers
├── config.py           # Configuration
├── wrangler.toml       # Configuration Cloudflare
├── requirements.txt    # Dépendances Python
├── package.json        # Dépendances Node.js
└── templates/          # Templates HTML
```

## 🔧 Configuration

### Variables d'environnement requises

- `DATABASE_URL` : URL PostgreSQL Supabase
- `SECRET_KEY` : Clé secrète Flask
- `PRODUCTION_URL` : URL de production

### Services Cloudflare

- **Workers** : Hébergement de l'application
- **R2** : Stockage des photos
- **KV** : Cache (optionnel)

## 📊 Monitoring

- **Logs** : `wrangler tail`
- **Analytics** : Dashboard Cloudflare
- **Uptime** : SLA 99.9% garanti

## 🎯 Avantages Cloudflare Workers

- ✅ **Disponibilité 24/7** (SLA 99.9%)
- ✅ **Performance optimale** (Edge Computing)
- ✅ **Scalabilité automatique**
- ✅ **Protection DDoS** intégrée
- ✅ **Coût optimisé** (gratuit jusqu'à 100k requêtes/jour)

## 📞 Support

- **Documentation** : [developers.cloudflare.com/workers](https://developers.cloudflare.com/workers/)
- **Communauté** : Discord Cloudflare
- **Issues** : GitHub Issues

---

**🚀 Déployé avec ❤️ sur Cloudflare Workers**