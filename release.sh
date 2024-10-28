#!/usr/bin/env bash

set -e
set -o pipefail

# Variables globales
CURRENT_DIR=$(pwd)
DORA_REPOSITORY=git@github.com:gip-inclusion/dora.git

# Couleurs ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color (reset)

# ===
# 1. PREPARE
# ===

# ---
# Check param(s)
# ---

# Vérification de l'argument release_type
if [ -z "$1" ]; then
  echo -e "${RED}⚠️  Vous devez spécifier le type de release (major, minor, patch).${NC}"
  exit 1
fi

RELEASE_TYPE=$1

# Vérification que release_type est valide
if [[ "$RELEASE_TYPE" != "major" && "$RELEASE_TYPE" != "minor" && "$RELEASE_TYPE" != "patch" ]]; then
  echo -e "${RED}⚠️  Type de release invalide : '$RELEASE_TYPE'. Utilisez uniquement 'major', 'minor' ou 'patch'.${NC}"
  exit 1
fi

# ---
# Check environment and rights
# ---

# Fonction pour vérifier l'existence d'une variable d'environnement
check_env_var_is_set() {
  local var_name=$1
  if [ -z "${!var_name}" ]; then
    echo -e "${RED}⚠️  La variable d'environnement $var_name doit être définie.${NC}"
    exit 1
  fi
}

# Vérification des variables d'environnement requises
check_env_var_is_set "SCALINGO_REGION"
check_env_var_is_set "SCALINGO_BACK_APP"
check_env_var_is_set "SCALINGO_FRONT_APP"

# Vérification que le CLI Scalingo est installé
if ! command -v scalingo &> /dev/null; then
  echo -e "${RED}⚠️  Le CLI Scalingo n'est pas installé. Veuillez l'installer avant d'exécuter ce script.${NC}"
  exit 1
fi

# Vérification de l'accès aux applications Scalingo
echo "${CYAN}🔍 Vérification des permissions Scalingo...${NC}"
APPS_LIST=$(scalingo apps --region "$SCALINGO_REGION")

check_app_access() {
  local app_name=$1
  if echo "$APPS_LIST" | grep -E "^\|[[:space:]]*$app_name[[:space:]]*\|[[:space:]]*collaborator[[:space:]]*\|" &> /dev/null; then
    echo -e "Accès confirmé pour l'application '$app_name'."
  else
    echo -e "${RED}⚠️  Vous n'avez pas accès en tant que collaborateur à l'application '$app_name' dans la région '$SCALINGO_REGION'. Veuillez vérifier vos permissions.${NC}"
    exit 1
  fi
}

check_app_access "$SCALINGO_BACK_APP"
check_app_access "$SCALINGO_FRONT_APP"

# ---
# Utils
# ---

# Fonction pour incrémenter la version
increment_version() {
  local version=$1
  local release_type=$2

  # Supprimer le 'v' au début et séparer en parties (major.minor.patch)
  version="${version#v}"
  IFS='.' read -r major minor patch <<< "$version"

  case $release_type in
    major)
      major=$((major + 1))
      minor=0
      patch=0
      ;;
    minor)
      minor=$((minor + 1))
      patch=0
      ;;
    patch)
      patch=$((patch + 1))
      ;;
    *)
      echo -e "${RED}⚠️  Type de release non valide. Utilisez major, minor ou patch.${NC}"
      exit 1
      ;;
  esac

  echo "v$major.$minor.$patch"
}

# Fonction pour gérer le processus de déploiement
deploy_repo() {
  local repo_url=$1
  local repo_name=$2
  
  echo -e "${CYAN}📦 Déploiement de l'application ${repo_name}${NC}"

  echo "Clonage du dépôt $repo_name..."
  git clone "$repo_url"
  cd "$repo_name"

  echo "Récupération des branches distantes pour $repo_name..."
  git fetch --all

  # Vérifier s'il y a des commits d'écart entre 'main' et le dépôt distant
  COMMITS_DIFF=$(git rev-list --count main..origin/main)

  if [ "$COMMITS_DIFF" -gt 0 ]; then
    echo "Il y a $COMMITS_DIFF commit(s) à déployer pour $repo_name."

    # Génération du tag basé sur le fichier 'version'
    if [ -f "$CURRENT_DIR/version" ]; then
      CURRENT_VERSION=$(cat "$CURRENT_DIR/version" | tr -d '[:space:]')
      VERSION=$(increment_version "$CURRENT_VERSION" "$RELEASE_TYPE")
      echo "$VERSION" > "$CURRENT_DIR/version"
      echo "📌 Nouvelle version : $VERSION (basée sur le type $RELEASE_TYPE)"
      
      # Ajouter et commiter la nouvelle version du fichier 'version'
      git add "$CURRENT_DIR/version"
      git commit -m "MEP $(date +'%d.%m.%Y') : Mise à jour de la version à $VERSION"
      git push origin main

      # Créer et pousser le nouveau tag
      git tag "$VERSION"
      git push origin "$VERSION"
    else
      echo -e "${RED}⚠️ Fichier version introuvable. Impossible de créer le tag.${NC}"
      exit 1
    fi
  else
    echo -e "${YELLOW}🙅 Pas de commits à déployer pour $repo_name. Aucun tag ou déploiement effectué.${NC}"
  fi

  # Déploiement de l'archive sur Scalingo
  if [ -n "$VERSION" ]; then
    echo "🚀 Déploiement de l'archive sur Scalingo pour les applications dora-back et dora-front"
    tag_archive_url="https://github.com/jbuget/dora/archive/refs/tags/$VERSION.tar.gz"
    echo "[dry-run] scalingo deploy --region $SCALINGO_REGION --app $SCALINGO_BACK_APP $tag_archive_url"
    echo "[dry-run] scalingo deploy --region $SCALINGO_REGION --app $SCALINGO_FRONT_APP $tag_archive_url"
    #scalingo deploy --region "$SCALINGO_REGION" --app "$SCALINGO_BACK_APP" "$tag_archive_url"
    #scalingo deploy --region "$SCALINGO_REGION" --app "$SCALINGO_FRONT_APP" "$tag_archive_url"
  else
    echo -e "${RED}⚠️ Version non définie. Déploiement Scalingo annulé.${NC}"
  fi

  # Revenir au répertoire temporaire
  cd ..
  echo ""
}

# ===
# 2. PERFORM
# ===

# Début
echo ""
echo -e "${YELLOW}🚀 Démarrage de la procédure de livraison${NC}"
echo ""

# Création d'un répertoire temporaire
TEMP_DIR=$(mktemp -d)
echo "✨ Création d'un répertoire temporaire pour le travail : $TEMP_DIR"
cd "$TEMP_DIR"
echo ""

# Déploiement
deploy_repo "$DORA_REPOSITORY" "dora"

# Nettoyage
echo "🧹 Nettoyage : retour au répertoire initial et suppression du répertoire temporaire."
cd "$CURRENT_DIR"
rm -rf "$TEMP_DIR"
echo ""

# Fin
echo -e "${GREEN}🎉 Fin de la procédure de livraison${NC}"
echo ""
trap - EXIT