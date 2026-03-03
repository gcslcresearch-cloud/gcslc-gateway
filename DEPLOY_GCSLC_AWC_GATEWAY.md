# GitHub–Vercel Push — GCSLC-AWC-Gateway

**AWC Nodal Release: Sovereign Gateway Audit (D2, D6, D7)**  
**CAC: 176917792057 | Chairman Lock: Dr. Sa'ad Jaafaru**

Push the updated, **space-free** AWC portal (including **RealTimeEngine** with `st.empty()` and 60s rerun, path fix, and D6 .env mapping) to a new GitHub repository named **GCSLC-AWC-Gateway**.

## Sovereign Gateway Audit Summary

| Determinant | Status | Notes |
|-------------|--------|--------|
| **Path** | ✅ Resolved | Project not in folder with spaces; `awc_portal_8054.py` at project root. "File does not exist: 8R" resolved. |
| **D2 Operational Anchor** | ✅ Confirmed | `RealTimeEngine` in `awc_portal_8054.py`: `st.empty()` containers + 60s rerun loop; mobile browser refreshes $50.1M revenue container (no stale snapshot). Interval configurable via `GCSLC_AWC_REALTIME_INTERVAL_SEC` in `.env`. |
| **D6 Compliance Integration** | ✅ Mapped | Legal/technical compliance in `.env`: SSL/TLS (HTTPS on Vercel for 8054), `GCSLC_ABUJA_IPS`, `GCSLC_AWC_REALTIME_INTERVAL_SEC`, optional `GCSLC_API_KEY`. See `.env.example`. |
| **D7 Sovereign Verification** | ✅ Confirmed | Header and sidebar include **CAC: 176917792057** and **Chairman Lock: Dr. Sa'ad Jaafaru** (signature of Dr. Sa'ad Jaafaru). |

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
git add awc_portal_8054.py run_awc_portal_8054.sh DEPLOY_GCSLC_AWC_GATEWAY.md .env.example
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
