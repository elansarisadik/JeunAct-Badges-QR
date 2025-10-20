#!/usr/bin/env python3
"""
Test de disponibilité 24/7 pour QR Code Jeunact
Monitoring et alertes automatiques
"""

import requests
import time
import json
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class UptimeMonitor:
    def __init__(self, app_url, check_interval=300):  # 5 minutes par défaut
        self.app_url = app_url
        self.check_interval = check_interval
        self.uptime_log = []
        self.downtime_log = []
        self.start_time = datetime.now()
        
    def check_app_health(self):
        """Vérifier la santé de l'application"""
        try:
            # Test de la page principale
            response = requests.get(f"{self.app_url}/", timeout=10)
            if response.status_code == 200:
                return True, "Page principale accessible"
            
            # Test de l'API admin
            response = requests.get(f"{self.app_url}/admin", timeout=10)
            if response.status_code == 200:
                return True, "Page admin accessible"
            
            return False, f"Erreur HTTP: {response.status_code}"
            
        except requests.exceptions.Timeout:
            return False, "Timeout de connexion"
        except requests.exceptions.ConnectionError:
            return False, "Erreur de connexion"
        except Exception as e:
            return False, f"Erreur inattendue: {str(e)}"
    
    def log_status(self, is_up, message):
        """Enregistrer le statut"""
        timestamp = datetime.now()
        log_entry = {
            'timestamp': timestamp.isoformat(),
            'status': 'UP' if is_up else 'DOWN',
            'message': message
        }
        
        if is_up:
            self.uptime_log.append(log_entry)
        else:
            self.downtime_log.append(log_entry)
            self.send_alert(log_entry)
    
    def send_alert(self, log_entry):
        """Envoyer une alerte en cas de panne"""
        print(f"🚨 ALERTE: Application DOWN à {log_entry['timestamp']}")
        print(f"   Raison: {log_entry['message']}")
        
        # Ici vous pouvez ajouter des notifications:
        # - Email
        # - Slack
        # - Discord
        # - SMS
        
    def calculate_uptime_percentage(self):
        """Calculer le pourcentage de disponibilité"""
        total_checks = len(self.uptime_log) + len(self.downtime_log)
        if total_checks == 0:
            return 100.0
        
        uptime_checks = len(self.uptime_log)
        return (uptime_checks / total_checks) * 100
    
    def generate_report(self):
        """Générer un rapport de disponibilité"""
        uptime_percentage = self.calculate_uptime_percentage()
        total_checks = len(self.uptime_log) + len(self.downtime_log)
        runtime = datetime.now() - self.start_time
        
        print("\n" + "="*60)
        print("📊 RAPPORT DE DISPONIBILITÉ 24/7")
        print("="*60)
        print(f"🌐 URL: {self.app_url}")
        print(f"⏱️  Durée du monitoring: {runtime}")
        print(f"🔍 Nombre total de vérifications: {total_checks}")
        print(f"✅ Disponibilité: {uptime_percentage:.2f}%")
        print(f"📈 Temps de fonctionnement: {len(self.uptime_log)} vérifications")
        print(f"📉 Temps d'arrêt: {len(self.downtime_log)} vérifications")
        
        if self.downtime_log:
            print("\n🚨 INCIDENTS DÉTECTÉS:")
            for incident in self.downtime_log[-5:]:  # 5 derniers incidents
                print(f"   • {incident['timestamp']}: {incident['message']}")
        
        # Sauvegarder le rapport
        report = {
            'app_url': self.app_url,
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'uptime_percentage': uptime_percentage,
            'total_checks': total_checks,
            'uptime_checks': len(self.uptime_log),
            'downtime_checks': len(self.downtime_log),
            'incidents': self.downtime_log
        }
        
        with open('uptime-report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Rapport sauvegardé dans uptime-report.json")
        
        return uptime_percentage
    
    def run_continuous_monitoring(self, duration_hours=24):
        """Lancer le monitoring continu"""
        print(f"🚀 Démarrage du monitoring 24/7")
        print(f"🌐 URL: {self.app_url}")
        print(f"⏰ Intervalle: {self.check_interval} secondes")
        print(f"🕐 Durée: {duration_hours} heures")
        print(f"📅 Début: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "="*60)
        
        end_time = self.start_time + timedelta(hours=duration_hours)
        
        try:
            while datetime.now() < end_time:
                is_up, message = self.check_app_health()
                self.log_status(is_up, message)
                
                # Afficher le statut
                status_icon = "✅" if is_up else "❌"
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"{status_icon} [{timestamp}] {message}")
                
                # Attendre avant la prochaine vérification
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n⏹️  Monitoring arrêté par l'utilisateur")
        
        # Générer le rapport final
        uptime_percentage = self.generate_report()
        
        if uptime_percentage >= 99.9:
            print("\n🎉 EXCELLENT! Disponibilité >= 99.9%")
        elif uptime_percentage >= 99.0:
            print("\n✅ BON! Disponibilité >= 99.0%")
        elif uptime_percentage >= 95.0:
            print("\n⚠️  ACCEPTABLE! Disponibilité >= 95.0%")
        else:
            print("\n❌ PROBLÈME! Disponibilité < 95.0%")

def main():
    print("🚀 Test de disponibilité 24/7 - QR Code Jeunact")
    print("=" * 60)
    
    # Demander l'URL de l'application
    app_url = input("🌐 Entrez l'URL de votre application Cloudflare Workers: ").strip()
    
    if not app_url:
        print("❌ URL requise")
        sys.exit(1)
    
    # Demander l'intervalle de vérification
    try:
        interval = int(input("⏰ Intervalle de vérification en secondes (défaut: 300): ") or "300")
    except ValueError:
        interval = 300
    
    # Demander la durée du test
    try:
        duration = int(input("🕐 Durée du test en heures (défaut: 24): ") or "24")
    except ValueError:
        duration = 24
    
    # Créer et lancer le monitor
    monitor = UptimeMonitor(app_url, interval)
    monitor.run_continuous_monitoring(duration)

if __name__ == "__main__":
    main()
