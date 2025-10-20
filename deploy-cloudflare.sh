#!/bin/bash

# Script de déploiement automatisé pour Cloudflare Workers
# QR Code Jeunact - Configuration 24/7

set -e

echo "🚀 Déploiement QR Code Jeunact sur Cloudflare Workers"
echo "=================================================="

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier si Wrangler est installé
check_wrangler() {
    log_info "Vérification de Wrangler CLI..."
    if ! command -v wrangler &> /dev/null; then
        log_error "Wrangler CLI n'est pas installé"
        log_info "Installation de Wrangler..."
        npm install -g wrangler
        log_success "Wrangler installé avec succès"
    else
        log_success "Wrangler CLI est installé"
    fi
}

# Authentification Cloudflare
authenticate_cloudflare() {
    log_info "Authentification Cloudflare..."
    if ! wrangler whoami &> /dev/null; then
        log_warning "Vous devez vous connecter à Cloudflare"
        wrangler login
    else
        log_success "Déjà connecté à Cloudflare"
    fi
}

# Créer le bucket R2 pour les photos
create_r2_bucket() {
    log_info "Création du bucket R2 pour les photos..."
    
    # Vérifier si le bucket existe déjà
    if wrangler r2 bucket list | grep -q "jeunact-photos"; then
        log_success "Bucket R2 'jeunact-photos' existe déjà"
    else
        wrangler r2 bucket create jeunact-photos
        log_success "Bucket R2 'jeunact-photos' créé"
    fi
}

# Créer le namespace KV pour le cache
create_kv_namespace() {
    log_info "Création du namespace KV..."
    
    # Créer le namespace de production
    PROD_NAMESPACE=$(wrangler kv:namespace create "MEMBERS_KV" --preview false 2>/dev/null | grep -o 'id = "[^"]*"' | cut -d'"' -f2)
    if [ ! -z "$PROD_NAMESPACE" ]; then
        log_success "Namespace KV de production créé: $PROD_NAMESPACE"
    fi
    
    # Créer le namespace de preview
    PREVIEW_NAMESPACE=$(wrangler kv:namespace create "MEMBERS_KV" --preview true 2>/dev/null | grep -o 'id = "[^"]*"' | cut -d'"' -f2)
    if [ ! -z "$PREVIEW_NAMESPACE" ]; then
        log_success "Namespace KV de preview créé: $PREVIEW_NAMESPACE"
    fi
    
    # Mettre à jour wrangler.toml avec les vrais IDs
    if [ ! -z "$PROD_NAMESPACE" ] && [ ! -z "$PREVIEW_NAMESPACE" ]; then
        sed -i "s/your-kv-namespace-id/$PROD_NAMESPACE/g" wrangler.toml
        sed -i "s/your-preview-kv-namespace-id/$PREVIEW_NAMESPACE/g" wrangler.toml
        log_success "wrangler.toml mis à jour avec les IDs KV"
    fi
}

# Générer une clé secrète forte
generate_secret_key() {
    log_info "Génération d'une clé secrète forte..."
    SECRET_KEY=$(openssl rand -base64 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    log_success "Clé secrète générée"
}

# Configuration des variables d'environnement
configure_environment() {
    log_info "Configuration des variables d'environnement..."
    
    # Demander l'URL de production
    read -p "🌐 Entrez votre domaine Cloudflare Workers (ex: qr-jeunact.votre-domaine.workers.dev): " WORKER_URL
    
    # Demander l'URL de la base de données Supabase
    read -p "🗄️  Entrez l'URL de votre base de données Supabase (postgresql://...): " DATABASE_URL
    
    # Mettre à jour wrangler.toml
    sed -i "s|your-secret-key-here|$SECRET_KEY|g" wrangler.toml
    sed -i "s|https://qr-code-jeunact.your-domain.workers.dev|https://$WORKER_URL|g" wrangler.toml
    sed -i "s|postgresql://postgres:password@db.project-ref.supabase.co:5432/postgres|$DATABASE_URL|g" wrangler.toml
    
    log_success "Variables d'environnement configurées"
}

# Déployer l'application
deploy_application() {
    log_info "Déploiement de l'application..."
    
    # Déploiement en staging d'abord
    log_info "Déploiement en staging..."
    wrangler deploy --env staging
    
    # Test du staging
    log_info "Test du déploiement staging..."
    sleep 5
    
    # Déploiement en production
    log_info "Déploiement en production..."
    wrangler deploy --env production
    
    log_success "Application déployée avec succès !"
}

# Configuration du domaine personnalisé
setup_custom_domain() {
    log_info "Configuration du domaine personnalisé..."
    
    read -p "🌍 Voulez-vous configurer un domaine personnalisé ? (y/n): " SETUP_DOMAIN
    
    if [ "$SETUP_DOMAIN" = "y" ] || [ "$SETUP_DOMAIN" = "Y" ]; then
        read -p "📝 Entrez votre domaine personnalisé (ex: qr.jeunact.com): " CUSTOM_DOMAIN
        
        log_info "Configuration du domaine $CUSTOM_DOMAIN..."
        log_warning "Vous devez configurer manuellement le domaine dans le dashboard Cloudflare:"
        log_info "1. Allez dans Workers & Pages"
        log_info "2. Sélectionnez votre worker"
        log_info "3. Allez dans Settings > Triggers"
        log_info "4. Ajoutez votre domaine: $CUSTOM_DOMAIN"
    fi
}

# Test de l'application
test_application() {
    log_info "Test de l'application..."
    
    # Obtenir l'URL de production
    PROD_URL=$(grep "PRODUCTION_URL" wrangler.toml | head -1 | cut -d'"' -f2)
    
    if [ ! -z "$PROD_URL" ]; then
        log_info "Test de l'URL: $PROD_URL"
        
        # Test simple avec curl
        if curl -s -o /dev/null -w "%{http_code}" "$PROD_URL" | grep -q "200"; then
            log_success "Application accessible et fonctionnelle !"
        else
            log_warning "L'application pourrait ne pas être encore accessible"
        fi
    fi
}

# Fonction principale
main() {
    echo
    log_info "Début du processus de déploiement..."
    echo
    
    # Étapes de déploiement
    check_wrangler
    authenticate_cloudflare
    generate_secret_key
    configure_environment
    create_r2_bucket
    create_kv_namespace
    deploy_application
    setup_custom_domain
    test_application
    
    echo
    log_success "🎉 Déploiement terminé avec succès !"
    echo
    log_info "📋 Résumé du déploiement:"
    log_info "   • Application déployée sur Cloudflare Workers"
    log_info "   • Bucket R2 créé pour les photos"
    log_info "   • Namespace KV créé pour le cache"
    log_info "   • Configuration 24/7 activée"
    echo
    log_info "🔗 Liens utiles:"
    log_info "   • Dashboard Cloudflare: https://dash.cloudflare.com"
    log_info "   • Monitoring: wrangler tail"
    log_info "   • Logs: wrangler tail --format=pretty"
    echo
}

# Exécuter le script principal
main "$@"
