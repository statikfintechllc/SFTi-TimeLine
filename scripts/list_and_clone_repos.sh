#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   export GITHUB_TOKEN="ghp_xxx"
#   ./scripts/list_repos_api.sh statikfintechllc ./repos_metadata.csv

ORG="$1"      # e.g., statikfintechllc
OUTFILE="${2:-./repos_metadata.csv}"
PER_PAGE=100

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "ERROR: set GITHUB_TOKEN env var (personal access token with repo/public_repo scopes)"
  exit 1
fi

echo "repo_name,created_at,pushed_at,updated_at,clone_url,html_url,description" > "$OUTFILE"

page=1
while :; do
  echo "Fetching page $page..."
  resp=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
       "https://api.github.com/users/$ORG/repos?per_page=$PER_PAGE&page=$page")

  count=$(echo "$resp" | jq 'length')
  if [[ "$count" -eq 0 || "$count" == "null" ]]; then
    break
  fi

  echo "$resp" | jq -r '.[] | [
    .name,
    .created_at,
    .pushed_at,
    .updated_at,
    .clone_url,
    .html_url,
    (.description // "")
  ] | @csv' >> "$OUTFILE"

  page=$((page+1))
done

echo "Done. Wrote $OUTFILE"
