#!/usr/bin/env python3
"""
Script de démarrage pour l'application JeunAct
"""
import os
from app import app, db

if __name__ == '__main__':
    with app.app_context():
        # Créer les tables de la base de données si elles n'existent pas
        db.create_all()
        print("✅ Base de données initialisée")
    
    # Démarrer l'application
    print("🚀 Démarrage de l'application JeunAct...")
    print("📱 Accédez à http://localhost:5000")
    print("🔧 Administration: http://localhost:5000/admin")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
