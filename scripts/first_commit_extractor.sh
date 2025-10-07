#!/usr/bin/env bash
set -euo pipefail

BASEDIR="${1:-./repos}"
OUTFILE="${2:-First_Commits.csv}"

echo "repo,first_commit_iso,first_commit_hash,first_commit_author" > "$OUTFILE"

for d in "$BASEDIR"/*; do
  if [[ -d "$d/.git" ]]; then
    repo=$(basename "$d")
    echo "Processing $repo ..."
    pushd "$d" >/dev/null

    git fetch --unshallow --tags --quiet || true

    commit_info=$(git rev-list --max-parents=0 HEAD | head -n 1)
    if [[ -z "$commit_info" ]]; then
      commit_info=$(git rev-list --reverse --all | head -n 1)
    fi

    if [[ -n "$commit_info" ]]; then
      hash="$commit_info"
      iso=$(git show -s --format=%cI "$hash")
      author=$(git show -s --format='%an' "$hash")
      echo "$repo,$iso,$hash,\"$author\"" >> ../"$OUTFILE"
    else
      echo "$repo,UNKNOWN,UNKNOWN,UNKNOWN" >> ../"$OUTFILE"
    fi

    popd >/dev/null
  fi
done

echo "Wrote $OUTFILE"
