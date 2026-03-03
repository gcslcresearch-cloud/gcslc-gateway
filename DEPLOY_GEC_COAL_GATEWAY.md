# GitHub–Vercel Push — GEC-Coal-Gateway

**AWC Nodal Repair: GEC-COAL-BASE-13 Nodal Release (D2 and D7)**  
**CAC: 176917792057 | Chairman Lock: Dr. Sa'ad Jaafaru**

Push the updated, **space-free** dashboard (including **WebSocket logic** — RealTimeEngine with st.empty() and 60s rerun) to a new GitHub repository named **GEC-Coal-Gateway**.

## 1. Create the new GitHub repository

- **Option A (GitHub CLI):** If you have `gh` installed:
  ```bash
  gh repo create GEC-Coal-Gateway --public --source=. --remote=gcgl --push
  ```
- **Option B (GitHub website):** Go to https://github.com/new, set repository name to **GEC-Coal-Gateway**, create it (no README), then run the commands below from your project root.

## 2. Add remote and push (from project root)

```bash
cd "/Users/user/Desktop/GCSLC_Sovereign_Gateway"
git remote add gcgl https://github.com/YOUR_USERNAME/GEC-Coal-Gateway.git
git add B_Files/nrrfc_dashboard.py run_nrrfc_dashboard_8051.sh B_Files/GEC_COAL_BASE_13.py d8_logic.py DEPLOY_GEC_COAL_GATEWAY.md
git commit -m "AWC Nodal Repair: GEC-COAL-BASE-13 D2/D7, RealTimeEngine 60s WebSocket, path fix, CAC/Chairman Lock"
git push -u gcgl main
```

(Replace `YOUR_USERNAME` with your GitHub username; use `master` instead of `main` if that is your default branch.)

## 3. Vercel

Import the new repo **GEC-Coal-Gateway** in Vercel. Configure build for Streamlit (or Streamlit Cloud / Docker). Set environment variables to match `.env.example` so the S24 Ultra live data stream works (live WebSocket instead of static snapshot).

---

## Verification — clean terminal command to run on Port 8051

**Space-free path (recommended):**
```bash
cd "/Users/user/Desktop/GCSLC_Sovereign_Gateway" && source ".venv/bin/activate" && streamlit run "B_Files/nrrfc_dashboard.py" --server.port 8051
```

**With launch script (space-free path):**
```bash
./run_nrrfc_dashboard_8051.sh
```

Then open **http://localhost:8051**.
