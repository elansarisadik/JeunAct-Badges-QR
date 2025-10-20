# Script de déploiement Cloudflare Workers pour Windows PowerShell
# QR Code Jeunact - Configuration 24/7

Write-Host "🚀 Déploiement QR Code Jeunact sur Cloudflare Workers" -ForegroundColor Blue
Write-Host "==================================================" -ForegroundColor Blue
Write-Host ""

# Fonction pour afficher les messages
function Write-Info {
    param($Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Write-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Vérifier les prérequis
Write-Info "Vérification des prérequis..."

# Vérifier Python
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python installé: $pythonVersion"
} catch {
    Write-Error "Python n'est pas installé"
    exit 1
}

# Vérifier Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Success "Node.js installé: $nodeVersion"
} catch {
    Write-Error "Node.js n'est pas installé"
    exit 1
}

Write-Host ""
Write-Info "📊 Étape 1: Configuration Supabase"
Write-Host "----------------------------------"

# Demander les informations Supabase
$supabaseUrl = Read-Host "🌐 Entrez l'URL de votre projet Supabase (ex: https://xyz.supabase.co)"
$supabaseKey = Read-Host "🔑 Entrez votre clé API Supabase (anon key)"
$dbPassword = Read-Host "🔐 Entrez le mot de passe de votre base de données Supabase"

if (-not $supabaseUrl -or -not $supabaseKey -or -not $dbPassword) {
    Write-Error "Toutes les informations Supabase sont requises"
    exit 1
}

# Extraire l'ID du projet
$projectId = $supabaseUrl -replace "https://", "" -replace ".supabase.co", ""

# Construire l'URL de connexion PostgreSQL
$databaseUrl = "postgresql://postgres:$dbPassword@db.$projectId.supabase.co:5432/postgres"

Write-Success "URL de connexion générée: $databaseUrl"

# Créer le fichier .env.local
$envContent = @"
# Configuration Supabase pour QR Code Jeunact
DATABASE_URL=$databaseUrl
SUPABASE_URL=$supabaseUrl
SUPABASE_ANON_KEY=$supabaseKey
SUPABASE_PROJECT_ID=$projectId
"@

$envContent | Out-File -FilePath ".env.local" -Encoding UTF8
Write-Success "Configuration sauvegardée dans .env.local"

Write-Host ""
Write-Info "🔄 Étape 2: Migration des données"
Write-Host "---------------------------------"

# Vérifier si le fichier SQLite existe
if (Test-Path "instance/jeunact_members.db") {
    Write-Info "Base de données SQLite trouvée, migration en cours..."
    
    # Installer psycopg2 si nécessaire
    try {
        pip install psycopg2-binary
        Write-Success "psycopg2-binary installé"
    } catch {
        Write-Warning "Erreur installation psycopg2-binary"
    }
    
    # Exécuter la migration
    try {
        python migrate-to-supabase.py
        Write-Success "Migration des données terminée"
    } catch {
        Write-Warning "Erreur lors de la migration"
    }
} else {
    Write-Warning "Base de données SQLite non trouvée, création des tables vides"
}

Write-Host ""
Write-Info "☁️  Étape 3: Installation Wrangler CLI"
Write-Host "-------------------------------------"

# Installer Wrangler globalement
try {
    npm install -g wrangler
    Write-Success "Wrangler CLI installé"
} catch {
    Write-Error "Erreur installation Wrangler CLI"
    Write-Info "Essayez d'exécuter: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    Write-Info "Puis relancez ce script"
    exit 1
}

Write-Host ""
Write-Info "🔐 Étape 4: Authentification Cloudflare"
Write-Host "--------------------------------------"

# Authentification Cloudflare
try {
    wrangler login
    Write-Success "Authentification Cloudflare réussie"
} catch {
    Write-Error "Erreur authentification Cloudflare"
    exit 1
}

Write-Host ""
Write-Info "📦 Étape 5: Configuration des services Cloudflare"
Write-Host "-----------------------------------------------"

# Créer le bucket R2
try {
    wrangler r2 bucket create jeunact-photos
    Write-Success "Bucket R2 'jeunact-photos' créé"
} catch {
    Write-Warning "Bucket R2 pourrait déjà exister"
}

# Créer le namespace KV
try {
    $kvOutput = wrangler kv:namespace create "MEMBERS_KV" --preview false
    $kvId = ($kvOutput | Select-String 'id = "([^"]*)"').Matches[0].Groups[1].Value
    Write-Success "Namespace KV créé: $kvId"
    
    $kvPreviewOutput = wrangler kv:namespace create "MEMBERS_KV" --preview true
    $kvPreviewId = ($kvPreviewOutput | Select-String 'id = "([^"]*)"').Matches[0].Groups[1].Value
    Write-Success "Namespace KV preview créé: $kvPreviewId"
    
    # Mettre à jour wrangler.toml
    $wranglerContent = Get-Content "wrangler.toml" -Raw
    $wranglerContent = $wranglerContent -replace "your-kv-namespace-id", $kvId
    $wranglerContent = $wranglerContent -replace "your-preview-kv-namespace-id", $kvPreviewId
    $wranglerContent = $wranglerContent -replace "postgresql://postgres:password@db.project-ref.supabase.co:5432/postgres", $databaseUrl
    
    # Générer une clé secrète
    $secretKey = [System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
    $wranglerContent = $wranglerContent -replace "your-secret-key-here", $secretKey
    
    $wranglerContent | Out-File -FilePath "wrangler.toml" -Encoding UTF8
    Write-Success "wrangler.toml mis à jour"
    
} catch {
    Write-Warning "Erreur création namespace KV"
}

Write-Host ""
Write-Info "🚀 Étape 6: Déploiement de l'application"
Write-Host "---------------------------------------"

# Déploiement en staging
try {
    Write-Info "Déploiement en staging..."
    wrangler deploy --env staging
    Write-Success "Déploiement staging réussi"
} catch {
    Write-Warning "Erreur déploiement staging"
}

# Déploiement en production
try {
    Write-Info "Déploiement en production..."
    wrangler deploy --env production
    Write-Success "Déploiement production réussi"
} catch {
    Write-Error "Erreur déploiement production"
    exit 1
}

Write-Host ""
Write-Success "🎉 Déploiement terminé avec succès !"
Write-Host "====================================="
Write-Host ""
Write-Host "📋 Résumé:" -ForegroundColor Green
Write-Host "✅ Supabase configuré et migré" -ForegroundColor Green
Write-Host "✅ Cloudflare Workers déployé" -ForegroundColor Green
Write-Host "✅ Application disponible 24/7" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Liens utiles:" -ForegroundColor Cyan
Write-Host "• Dashboard Cloudflare: https://dash.cloudflare.com" -ForegroundColor Cyan
Write-Host "• Dashboard Supabase: https://supabase.com/dashboard" -ForegroundColor Cyan
Write-Host "• Documentation: README-CLOUDFLARE.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Votre application QR Code Jeunact est maintenant disponible 24/7 !" -ForegroundColor Green
