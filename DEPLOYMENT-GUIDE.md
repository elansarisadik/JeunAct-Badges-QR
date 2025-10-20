# 🚀 Guide de Déploiement Manuel - QR Code Jeunact Cloudflare

## ✅ État Actuel
- ✅ Wrangler CLI installé
- ✅ Bucket R2 "jeunact-photos" créé
- ✅ Configuration wrangler.toml prête
- ⏳ Authentification Cloudflare en cours

## 📋 Étapes Restantes

### 1. Authentification Cloudflare
```bash
wrangler login
```
- Ouvrez le lien dans votre navigateur
- Connectez-vous à votre compte Cloudflare
- Autorisez l'accès

### 2. Créer le Namespace KV
```bash
wrangler kv:namespace create "MEMBERS_KV"
```
- Notez l'ID retourné (ex: abc123def456)
- Répétez pour le preview:
```bash
wrangler kv:namespace create "MEMBERS_KV" --preview
```

### 3. Configurer Supabase
1. Allez sur https://supabase.com
2. Créez un nouveau projet
3. Notez l'URL de connexion PostgreSQL
4. Activez l'API REST

### 4. Mettre à jour wrangler.toml
Remplacez dans wrangler.toml :
- `your-kv-namespace-id` → ID du namespace KV
- `your-preview-kv-namespace-id` → ID du namespace preview
- `your-secret-key-here` → Clé secrète forte
- `postgresql://postgres:password@db.project-ref.supabase.co:5432/postgres` → Votre URL Supabase

### 5. Déployer
```bash
wrangler deploy --env production
```

## 🔧 Configuration Supabase Rapide

### Créer les tables SQL
```sql
CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    member_number VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    position VARCHAR(50),
    email VARCHAR(120),
    whatsapp VARCHAR(20),
    instagram VARCHAR(100),
    linkedin VARCHAR(200),
    tiktok VARCHAR(100),
    portfolio VARCHAR(200),
    photo VARCHAR(200),
    integration_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_member_number ON members(member_number);
CREATE INDEX idx_full_name ON members(full_name);
```

### Migration des données
```bash
python migrate-to-supabase.py
```

## 🎯 Résultat Final
- Application disponible 24/7
- SLA 99.9% garanti
- Performance optimale
- Coût gratuit jusqu'à 100k requêtes/jour
