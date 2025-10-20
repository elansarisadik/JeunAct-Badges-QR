# Configuration Supabase pour Cloudflare Workers

## Étapes de configuration

### 1. Créer un projet Supabase
1. Allez sur https://supabase.com
2. Créez un nouveau projet
3. Notez l'URL de connexion PostgreSQL

### 2. Configuration de la base de données
```sql
-- Créer la table members
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

-- Créer un index pour les recherches
CREATE INDEX idx_member_number ON members(member_number);
CREATE INDEX idx_full_name ON members(full_name);
```

### 3. Variables d'environnement
```bash
# Dans wrangler.toml
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
```

### 4. Migration des données existantes
Si vous avez des données dans SQLite, utilisez ce script :

```python
# migrate_to_supabase.py
import sqlite3
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

# Connexion SQLite
sqlite_conn = sqlite3.connect('instance/jeunact_members.db')

# Connexion PostgreSQL (Supabase)
postgres_url = "postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres"
postgres_engine = create_engine(postgres_url)

# Lire les données
df = pd.read_sql_query("SELECT * FROM member", sqlite_conn)

# Écrire dans PostgreSQL
df.to_sql('members', postgres_engine, if_exists='replace', index=False)

print("Migration terminée !")
```

## Avantages Supabase
- **Gratuit** jusqu'à 500MB
- **PostgreSQL** complet
- **API REST** automatique
- **Interface web** pour gérer les données
- **Backup automatique**
- **SSL** inclus
