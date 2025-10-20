import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///jeunact_members.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration spécifique pour Cloudflare Workers
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'sslmode': 'require' if os.environ.get('DATABASE_URL') else None
        }
    }
    
    # URL de base pour les QR codes et redirections
    @staticmethod
    def get_base_url():
        """Retourne l'URL de base selon l'environnement"""
        # Si une URL de production est définie, l'utiliser
        if os.environ.get('PRODUCTION_URL'):
            return os.environ.get('PRODUCTION_URL')
        
        # Détecter si on est sur Cloudflare Workers
        if os.environ.get('CLOUDFLARE_WORKER'):
            return os.environ.get('CLOUDFLARE_WORKER_URL', 'https://your-domain.workers.dev')
        
        # Détecter si on est sur Deno Deploy
        if os.environ.get('DENO_DEPLOYMENT_ID'):
            return 'https://jeunact-bkcajngbx13k.elansarisadik.deno.net'
        
        # Par défaut, localhost pour le développement
        return 'http://localhost:5000'
    
    @staticmethod
    def is_cloudflare():
        """Détecte si l'application s'exécute sur Cloudflare"""
        return os.environ.get('CLOUDFLARE_WORKER') is not None