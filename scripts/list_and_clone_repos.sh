#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   export GITHUB_TOKEN="ghp_xxx"
#   ./scripts/list_and_clone_repos.sh statikfintechllc ./repos

ORG="$1"       # e.g., statikfintechllc
OUTDIR="${2:-./repos}"
PER_PAGE=100

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "ERROR: set GITHUB_TOKEN env var (personal access token with repo/public_repo scopes)"
  exit 1
fi

mkdir -p "$OUTDIR"

page=1
while :; do
  echo "Listing page $page..."
  resp=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
       "https://api.github.com/orgs/$ORG/repos?per_page=$PER_PAGE&page=$page")

  count=$(echo "$resp" | jq 'length')
  if [[ "$count" -eq 0 ]]; then
    break
  fi

  echo "$resp" | jq -r '.[].clone_url' | while read -r clone_url; do
    repo_name=$(basename -s .git "$clone_url")
    target="$OUTDIR/$repo_name"
    if [[ -d "$target/.git" ]]; then
      echo "Already cloned: $repo_name"
      continue
    fi
    echo "Cloning $repo_name ..."
    git clone --depth 1 "$clone_url" "$target" || echo "clone failed for $repo_name"
  done

  page=$((page+1))
done

echo "Done. Cloned repos are in $OUTDIR"
