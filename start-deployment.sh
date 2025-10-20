#!/bin/bash

# Script de démarrage rapide - QR Code Jeunact Cloudflare
# Exécute toutes les étapes de déploiement automatiquement

echo "🚀 QR Code Jeunact - Déploiement Cloudflare Workers 24/7"
echo "========================================================"
echo

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 requis mais non installé"
    exit 1
fi

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js requis mais non installé"
    echo "💡 Installez Node.js depuis https://nodejs.org"
    exit 1
fi

# Vérifier npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm requis mais non installé"
    exit 1
fi

echo "✅ Prérequis vérifiés"
echo

# Étape 1: Configuration Supabase
echo "📊 Étape 1: Configuration Supabase"
echo "----------------------------------"
python3 setup-supabase.py
if [ $? -ne 0 ]; then
    echo "❌ Erreur configuration Supabase"
    exit 1
fi
echo

# Étape 2: Migration des données
echo "🔄 Étape 2: Migration des données"
echo "---------------------------------"
python3 migrate-to-supabase.py
if [ $? -ne 0 ]; then
    echo "❌ Erreur migration des données"
    exit 1
fi
echo

# Étape 3: Déploiement Cloudflare
echo "☁️  Étape 3: Déploiement Cloudflare"
echo "-----------------------------------"
bash deploy-cloudflare.sh
if [ $? -ne 0 ]; then
    echo "❌ Erreur déploiement Cloudflare"
    exit 1
fi
echo

# Étape 4: Test de disponibilité
echo "🧪 Étape 4: Test de disponibilité"
echo "--------------------------------"
echo "Voulez-vous lancer un test de disponibilité ? (y/n)"
read -p "> " test_uptime

if [ "$test_uptime" = "y" ] || [ "$test_uptime" = "Y" ]; then
    echo "🚀 Lancement du test de disponibilité..."
    python3 test-uptime.py
fi

echo
echo "🎉 Déploiement terminé avec succès !"
echo "====================================="
echo
echo "📋 Résumé:"
echo "✅ Supabase configuré et migré"
echo "✅ Cloudflare Workers déployé"
echo "✅ Application disponible 24/7"
echo
echo "🔗 Liens utiles:"
echo "• Dashboard Cloudflare: https://dash.cloudflare.com"
echo "• Dashboard Supabase: https://supabase.com/dashboard"
echo "• Documentation: README-CLOUDFLARE.md"
echo
echo "🚀 Votre application QR Code Jeunact est maintenant disponible 24/7 !"
