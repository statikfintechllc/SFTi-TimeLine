## Evidence repo generator

**Purpose**:
- Ingest timeline_base.csv (your Medium + Zenodo items)
- Auto-list and clone all GitHub repos for org/user statikfintechllc
- Extract first-commit timestamps for each repo
- Produce evidence/timeline.csv (combined, sorted by date)

**Requirements**:
- Linux or macOS with git, curl, jq, python3 (3.10+)
- A GitHub Personal Access Token (PAT) with public_repo or repo scope
- Enough disk space for cloning repos (shallow clones minimize space)

**Steps**:
1) Put your provided timeline_base.csv at repo root (I already generated a prefilled version).
2) export GITHUB_TOKEN="ghp_xxx"
3) ./scripts/list_and_clone_repos.sh statikfintechllc ./repos
4) ./scripts/first_commit_extractor.sh ./repos ./first_commits.csv
5) python3 scripts/build_evidence_timeline.py timeline_base.csv first_commits.csv evidence/timeline.csv

**Expected outputs**:
- first_commits.csv (repo,first_commit_iso,...)
- evidence/timeline.csv (combined timeline)

---

### How to run)

Run these commands in a terminal at repo root (assumes scripts are executable):

**First**:
```bash
export GITHUB_TOKEN="ghp_yourtokenhere"
```
**Then**:
```bash
./scripts/list_repos_api.sh statikfintechllc repos_metadata.csv
```
**Then**:
```bash
./scripts/first_commit_extractor.sh ./repos ./First_Commits.csv
```
**Finally**:
```bash
python3 scripts/build_evidence_timeline.py SFTi_TimeLine.csv First_Commits.csv evidence/timeline.csv
```
