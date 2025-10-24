import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///jeunact_members.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # URL de base pour les QR codes et redirections
    @staticmethod
    def get_base_url():
        """Retourne l'URL de base selon l'environnement"""
        # Si une URL de production est définie, l'utiliser
        if os.environ.get('PRODUCTION_URL'):
            return os.environ.get('PRODUCTION_URL')
        
        # URL Vercel par défaut (sera remplacée par l'URL réelle)
        return 'https://jeunact-badges-qr.vercel.app'