# DevOps Coursework Diet 2 — Execution Runbook

**Before you start:** replace `YOURDOCKERHUB` with your real DockerHub username in:
`k8s/deployment.yaml`, `ansible/setup-production.yml`. In GitHub Actions the username
comes from a secret (set up in Phase 4) so the workflow files need no editing.

`app_ORIGINAL.py` / `app_FIXED.py` and the `_ORIGINAL`/`_FIXED` html files are helpers
for you — do NOT commit them. `app.py` currently holds the ORIGINAL (broken) code, which
is what goes on `main` first. The fix is applied on the `bugfix` branch (Phase 3).

📸 = capture a screenshot here for the report.

---

## Phase 0 — AWS setup (Preliminary Steps)
1. Launch **two EC2 instances**, both Ubuntu, t3.large, security group with port **5000** open (and 22 for SSH):
   - `Build Server`
   - `Production Server` — set storage to **12 GB**
2. On **both** servers: install Docker, configure Git + GitHub auth (labs 2 & 3).
3. On the **Production Server** only: install Ansible (`sudo apt update && sudo apt install -y ansible`).

---

## Phase 1 — Build the application (Task 1, 6 marks) — on Build Server
```bash
# Create the repo on GitHub named EXACTLY: currency-converter-app
# Then locally:
git clone https://github.com/<you>/currency-converter-app.git
cd currency-converter-app
# copy in all project files (app.py, Dockerfile, templates/, k8s/, tests/, .github/, requirements.txt)
git add .
git commit -m "Initial commit: currency converter starter app + Dockerfile"
git push origin main
```
📸 **GitHub repo showing files in main branch**

```bash
# Task 1c: build image manually and push to DockerHub
docker login
docker build -t YOURDOCKERHUB/currency-converter-app:latest .
docker push YOURDOCKERHUB/currency-converter-app:latest
```
📸 **Terminal after successful push** AND 📸 **DockerHub page showing the image**

---

## Phase 2 — Testing locally (Task 2 a-c, e — the "should fail" part)
```bash
pip install -r requirements.txt
# Run each test file — a and b should FAIL, c should PASS (this is expected)
python -m unittest tests.test_empty_input
python -m unittest tests.test_non_numeric
python -m unittest tests.test_conversion
```
📸 **Terminal showing test_empty_input and test_non_numeric FAILING** (proves the bugs exist)

---

## Phase 3 — Fix on bugfix branch (Task 2 d, e, f)
```bash
git checkout -b bugfix

# Apply the fixes (overwrite the broken files with the fixed versions)
cp app_FIXED.py app.py
cp templates/index_FIXED.html templates/index.html
rm app_FIXED.py app_ORIGINAL.py templates/index_FIXED.html templates/index_ORIGINAL.html

# Re-run all tests — ALL should now PASS
python -m unittest tests.test_empty_input
python -m unittest tests.test_non_numeric
python -m unittest tests.test_conversion
```
📸 **Terminal showing ALL tests PASSING**

```bash
git add .
git commit -m "bugfix: handle empty and non-numeric input, round results"
git push origin bugfix

# Merge bugfix into main
git checkout main
git merge bugfix
git push origin main

# Evidence of version control + merge
git log --graph --oneline --all
```
📸 **git log --graph output showing the branch + merge**
📸 **GitHub showing both main and bugfix branches**

> Note: if you delete the helper files only on bugfix, do the same cleanup on main after merge
> so the repo is tidy. Make sure `app.py` on main is the FIXED version after the merge.

---

## Phase 4 — GitHub secrets (needed before Actions runs)
In GitHub repo → Settings → Secrets and variables → Actions, add:
- `DOCKERHUB_USERNAME` = your DockerHub username
- `DOCKERHUB_TOKEN` = a DockerHub access token (DockerHub → Account Settings → Security → New Access Token)

---

## Phase 5 — Production server: Ansible + Kubernetes (Task 3, 12 marks) — on Production Server
```bash
cd currency-converter-app/ansible
# make sure dockerhub_user in setup-production.yml is set to YOUR username
ansible-playbook -i inventory.ini setup-production.yml
```
📸 **Terminal showing ALL Ansible stages passing (the PLAY RECAP with ok/changed, failed=0)**

```bash
# Verify the app is reachable
kubectl get pods
kubectl get services
curl $(minikube ip):30007
```

---

## Phase 6 — Self-hosted runner (needed for CD) — on Production Server
GitHub repo → Settings → Actions → Runners → New self-hosted runner (Linux).
Follow the shown commands to download, configure, and run it:
```bash
./run.sh   # leave this running in its own terminal
```
This runner is what CD.yml deploys through (`runs-on: self-hosted`).

---

## Phase 7 — Trigger the full CI/CD pipeline (Task 4, 30 + 5 marks)
Any push to `main` now triggers CI. When CI succeeds, CD runs on your self-hosted runner.
```bash
# make any small change on the Build Server, then:
git commit -am "trigger pipeline"
git push origin main
```
📸 **GitHub Actions: overall view showing all CI steps green, with your username + repo name visible**
- Download the full CI job log: Actions → the run → gear icon → Download log archive.
  📋 **Paste the FULL log text into the report.**

---

## Phase 8 — Video demonstration (record last, ≤10 min)
On the Production Server, in a SEPARATE terminal from the runner:
1. `curl $(minikube ip):30007` — show the app responds.
2. Browser → `http://<production-public-ip>:30007` (or the NodePort) — show it running.
3. On Build Server, edit `templates/index.html`: change `<h1>Currency Converter</h1>`
   to `<h1>Currency Converter V2</h1>`. Commit + push to main.
4. Watch the GitHub Actions run — narrate every step (checkout, install, 3 tests,
   build, container launch test, push, then CD rolling update).
5. Back on Production Server: `curl $(minikube ip):30007` again — show "V2" now appears.
6. Refresh the browser — show V2 live, service never went down.

Save as MP4: `StudentID__DevOps_CW.mp4` (S2260340__DevOps_CW.mp4).

---

## Report checklist (use DevOps_coursework_report_template)
- [ ] Introduction (20%): pipeline rationale + DevOps principles + challenges + reflection + explain why tests failed and how the fix works
- [ ] 📸 Docker evidence
- [ ] 📸 GitHub evidence (main + bugfix + merge)
- [ ] 📸 Ansible evidence (all stages pass)
- [ ] 📋 Full GitHub Actions log text + 📸 success screenshot with username/repo
- [ ] 📸 git log extract

## Three submission portals
- [ ] Report → Turnitin
- [ ] Video → GCU Learn
- [ ] Code → CodeGrade
