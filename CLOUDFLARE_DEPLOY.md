# Guide de déploiement Cloudflare Workers

## Prérequis

1. Compte Cloudflare avec Workers activé
2. Wrangler CLI installé : `npm install -g wrangler`
3. Base de données PostgreSQL externe (Cloudflare Workers ne supporte pas SQLite)

## Configuration

### 1. Installation de Wrangler

```bash
npm install -g wrangler
```

### 2. Authentification Cloudflare

```bash
wrangler login
```

### 3. Configuration de la base de données

Cloudflare Workers nécessite une base de données externe. Options recommandées :
- **Supabase** (gratuit jusqu'à 500MB)
- **PlanetScale** (gratuit jusqu'à 1GB)
- **Railway** (gratuit jusqu'à 1GB)
- **Neon** (gratuit jusqu'à 3GB)

### 4. Configuration des variables d'environnement

Modifiez le fichier `wrangler.toml` :

```toml
name = "qr-code-jeunact"
main = "worker.py"
compatibility_date = "2023-12-01"

[env.production]
vars = { 
  ENVIRONMENT = "production",
  SECRET_KEY = "votre-clé-secrète-très-longue",
  PRODUCTION_URL = "https://qr-code-jeunact.votre-domaine.workers.dev",
  DATABASE_URL = "postgresql://user:password@host:port/database"
}

# Configuration pour la base de données KV (optionnel)
[[kv_namespaces]]
binding = "MEMBERS_KV"
id = "votre-kv-namespace-id"
preview_id = "votre-preview-kv-namespace-id"
```

### 5. Déploiement

```bash
# Déploiement en production
wrangler deploy

# Déploiement en preview
wrangler deploy --env staging
```

## Configuration avancée

### Base de données KV (Alternative)

Si vous préférez utiliser Cloudflare KV au lieu d'une base de données PostgreSQL :

1. Créez un namespace KV :
```bash
wrangler kv:namespace create "MEMBERS_KV"
```

2. Ajoutez l'ID dans `wrangler.toml`

3. Modifiez le code pour utiliser KV au lieu de SQLAlchemy

### Domaine personnalisé

1. Dans le dashboard Cloudflare, allez dans Workers & Pages
2. Sélectionnez votre worker
3. Allez dans Settings > Triggers
4. Ajoutez votre domaine personnalisé

## Monitoring et logs

```bash
# Voir les logs en temps réel
wrangler tail

# Voir les logs d'une requête spécifique
wrangler tail --format=pretty
```

## Avantages de Cloudflare Workers

- **Performance** : Exécution à la périphérie (edge computing)
- **Coût** : Gratuit jusqu'à 100,000 requêtes/jour
- **Sécurité** : Protection DDoS intégrée
- **CDN** : Distribution mondiale automatique
- **SSL** : Certificats SSL automatiques

## Limitations

- Pas de système de fichiers persistant
- Limite de 10ms CPU par requête (plan gratuit)
- Nécessite une base de données externe
- Pas de WebSockets en temps réel

## Support

- Documentation Cloudflare Workers : https://developers.cloudflare.com/workers/
- Communauté : https://discord.gg/cloudflaredev
