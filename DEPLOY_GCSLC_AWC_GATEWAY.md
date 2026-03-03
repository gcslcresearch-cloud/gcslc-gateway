# GitHub–Vercel Push — GCSLC-AWC-Gateway

**AWC Nodal Repair: Port 8054 and Wayan's S24 Ultra Sync**  
**CAC: 176917792057 | Chairman Lock: Dr. Sa'ad Jaafaru**

Push the updated, **space-free** AWC portal (including **RealTimeEngine** 60s rerun and path fix) to a new GitHub repository named **GCSLC-AWC-Gateway**.

## 1. Create the new GitHub repository

- **Option A (GitHub CLI):** If you have `gh` installed:
  ```bash
  gh repo create GCSLC-AWC-Gateway --public --source=. --remote=awc-gateway --push
  ```
- **Option B (GitHub website):** Go to https://github.com/new, set repository name to **GCSLC-AWC-Gateway**, create it (no README), then run the commands below from your project root.

## 2. Add remote and push (from project root)

```bash
cd "/Users/user/Desktop/GCSLC_Sovereign_Gateway"
git remote add awc-gateway https://github.com/YOUR_USERNAME/GCSLC-AWC-Gateway.git
git add awc_portal_8054.py run_awc_portal_8054.sh DEPLOY_GCSLC_AWC_GATEWAY.md
# Include African_Gateway if it lives in this repo and the portal depends on it:
git add African_Gateway/ 2>/dev/null || true
git commit -m "AWC Nodal: 1,203 MW + 9.6×, RealTimeEngine 60s for S24 Ultra, path fix, CAC/Chairman Lock"
git push -u awc-gateway main
```

(Replace `YOUR_USERNAME` with your GitHub username; use `master` instead of `main` if that is your default branch.)

## 3. Vercel

Import the new repo **GCSLC-AWC-Gateway** in Vercel. Configure build for Streamlit (or Streamlit Cloud / Docker). Set environment variables so the S24 Ultra live data stream works (RealTimeEngine 60s refresh instead of static snapshot).

---

## Verification — clean terminal command to run on Port 8054

**Space-free path (recommended):**
```bash
cd "/Users/user/Desktop/GCSLC_Sovereign_Gateway" && source ".venv/bin/activate" && streamlit run "awc_portal_8054.py" --server.port 8054
```

**With launch script:**
```bash
./run_awc_portal_8054.sh
```

Then open **http://localhost:8054**.
