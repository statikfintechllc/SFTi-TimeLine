#!/usr/bin/env python3
"""
Combine timeline_base.csv (Medium + Zenodo) with repo metadata or first-commit CSV
to produce evidence/timeline.csv

Usage:
  python3 scripts/build_evidence_timeline.py SFTi_TimeLine.csv repos_metadata.csv evidence/timeline.csv
  OR
  python3 scripts/build_evidence_timeline.py SFTi_TimeLine.csv First_Commits.csv evidence/timeline.csv
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

if len(sys.argv) != 4:
    print("Usage: build_evidence_timeline.py base.csv commits.csv out.csv")
    sys.exit(1)

base_csv = sys.argv[1]
commits_csv = sys.argv[2]
out_csv = sys.argv[3]

# load base
entries = []
with open(base_csv, newline="", encoding="utf-8") as f:
    rdr = csv.DictReader(f)
    for r in rdr:
        entries.append(r)

# load repos
repo_map = {}
with open(commits_csv, newline="", encoding="utf-8") as f:
    rdr = csv.DictReader(f)
    for r in rdr:
        key = r.get("repo") or r.get("repo_name")
        if key:
            repo_map[key] = r

# combine
combined = []
for r in entries:
    combined.append(
        {
            "source_type": r.get("type", ""),
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "doi": r.get("doi", ""),
            "published_at": r.get("created_at", ""),
            "repo_first_commit_iso": "",
            "repo_first_commit_hash": "",
            "repo_first_commit_author": "",
            "notes": r.get("notes", ""),
        }
    )

for repo, info in repo_map.items():
    combined.append(
        {
            "source_type": "repo",
            "title": repo,
            "url": info.get("html_url", ""),
            "doi": "",
            "published_at": info.get("first_commit_iso", info.get("created_at", "")),
            "repo_first_commit_iso": info.get("first_commit_iso", ""),
            "repo_first_commit_hash": info.get("first_commit_hash", ""),
            "repo_first_commit_author": info.get("first_commit_author", ""),
            "notes": info.get("description", "auto-collected"),
        }
    )


def parse_iso(s):
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        # Return timezone-naive datetime for consistent sorting
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return dt
    except Exception:
        return datetime.max


combined_sorted = sorted(
    combined, key=lambda x: parse_iso(x["published_at"] or "9999-12-31T00:00:00")
)

Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "source_type",
        "title",
        "url",
        "doi",
        "published_at",
        "repo_first_commit_iso",
        "repo_first_commit_hash",
        "repo_first_commit_author",
        "notes",
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(combined_sorted)

print(f"Wrote {out_csv}")
