# SFTi-TimeLine

## Purpose
Reproducible, timestamp-verified chronology for all StatikFinTech, LLC outputs — Medium, Zenodo, and GitHub — combined into one auditable dataset.

## Requirements
- Linux/macOS with `git`, `curl`, `jq`, `python3 (3.10+)`
- GitHub Personal Access Token with `public_repo` or `repo` scope

## Steps

1. Prepare base:
   - Ensure `SFTi_TimeLine.csv` (Medium + Zenodo or whatever you choose) is in repo root.
   - Export your GitHub token:  
```bash
   export GITHUB_TOKEN="ghp_xxx"
```
2. Fetch live GitHub metadata:
```bash
   ./scripts/list_and_clone_repos.sh statikfintechllc repos_metadata.csv
```
3. (Optional) Extract first-commit provenance:
```bash
   ./scripts/first_commit_extractor.sh ./repos ./First_Commits.csv
```
4. Build unified evidence timeline:
```bash
   python3 scripts/build_evidence_timeline.py SFTi_TimeLine.csv repos_metadata.csv evidence/timeline.csv
```
   - Or, using commit provenance:  
```bash
   python3 scripts/build_evidence_timeline.py SFTi_TimeLine.csv First_Commits.csv evidence/timeline.csv
```
## Outputs
- `repos_metadata.csv` — live GitHub repo metadata  
- `First_Commits.csv` — oldest verifiable commit timestamps  
- `evidence/timeline.csv` — full merged, date-sorted, machine-verifiable record

## Notes
- Works for both user and org accounts.
- Safe to rerun (auto-overwrite cleanly).
- Folders auto-created.
- ISO-8601 dates ensure chronological sort.
