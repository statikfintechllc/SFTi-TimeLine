#!/usr/bin/env python3
"""
Combine timeline_base.csv with repo first commit CSV into evidence/timeline.csv
Usage:
  python3 scripts/build_evidence_timeline.py timeline_base.csv repos/first_commits.csv evidence/timeline.csv
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

if len(sys.argv) != 4:
    print("Usage: build_evidence_timeline.py timeline_base.csv first_commits.csv out.csv")
    sys.exit(1)

SFTi_TimeLine_csv = sys.argv[1]
First_Commits_csv = sys.argv[2]
out_csv = sys.argv[3]

# load base
entries = []
with open(base_csv, newline='', encoding='utf-8') as f:
    rdr = csv.DictReader(f)
    for r in rdr:
        entries.append(r)

# load repos
repo_map = {}
with open(first_commits_csv, newline='', encoding='utf-8') as f:
    rdr = csv.DictReader(f)
    for r in rdr:
        repo_map[r['repo']] = r

# produce combined rows
combined = []
for r in entries:
    combined.append({
        'source_type': r.get('type',''),
        'title': r.get('title',''),
        'url': r.get('url',''),
        'doi': r.get('doi',''),
        'published_at': r.get('created_at',''),
        'repo_first_commit_iso': '',
        'repo_first_commit_hash': '',
        'repo_first_commit_author': '',
        'notes': r.get('notes','')
    })

# augment with any repos found
for repo, info in repo_map.items():
    combined.append({
        'source_type': 'repo',
        'title': repo,
        'url': '',
        'doi': '',
        'published_at': info.get('first_commit_iso',''),
        'repo_first_commit_iso': info.get('first_commit_iso',''),
        'repo_first_commit_hash': info.get('first_commit_hash',''),
        'repo_first_commit_author': info.get('first_commit_author',''),
        'notes': 'auto-collected'
    })

# sort by published_at where possible
def parse_iso(s):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return datetime.max

combined_sorted = sorted(combined, key=lambda x: parse_iso(x['published_at'] or '9999-12-31T00:00:00'))

# write out
Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
with open(out_csv, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['source_type','title','url','doi','published_at','repo_first_commit_iso','repo_first_commit_hash','repo_first_commit_author','notes']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for row in combined_sorted:
        w.writerow(row)

print("Wrote", out_csv)
