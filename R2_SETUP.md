# Configuration Cloudflare R2 pour les photos

## Étapes de configuration

### 1. Créer un bucket R2
```bash
# Installer Wrangler si pas déjà fait
npm install -g wrangler

# Créer un bucket
wrangler r2 bucket create jeunact-photos

# Lister les buckets
wrangler r2 bucket list
```

### 2. Configuration dans wrangler.toml
```toml
[[r2_buckets]]
binding = "PHOTOS_BUCKET"
bucket_name = "jeunact-photos"
preview_bucket_name = "jeunact-photos-preview"
```

### 3. Code pour upload des photos
```python
# Dans votre application Flask
import requests
import base64
from cloudflare import Cloudflare

class PhotoUploader:
    def __init__(self, account_id, api_token):
        self.cf = Cloudflare(token=api_token)
        self.account_id = account_id
    
    def upload_photo(self, file_data, filename):
        """Upload une photo vers R2"""
        try:
            # Upload vers R2
            response = self.cf.accounts.r2.buckets.objects.put(
                account_id=self.account_id,
                bucket_name="jeunact-photos",
                object_name=f"photos/{filename}",
                data=file_data
            )
            
            # Retourner l'URL publique
            return f"https://jeunact-photos.your-domain.com/photos/{filename}"
        except Exception as e:
            print(f"Erreur upload: {e}")
            return None
```

### 4. Configuration du domaine personnalisé
```bash
# Ajouter un domaine personnalisé pour R2
wrangler r2 bucket domain jeunact-photos photos.your-domain.com
```

## Avantages Cloudflare R2
- **Gratuit** jusqu'à 10GB/mois
- **Pas de frais de sortie** (contrairement à AWS S3)
- **CDN intégré**
- **API compatible S3**
- **Sécurité enterprise-grade**
