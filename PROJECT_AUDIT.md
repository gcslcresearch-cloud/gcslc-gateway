# Full Project Audit — GCSLC Sovereign Gateway

**Chairman & Founder: Dr. Sa'ad Jaafaru** | CAC AV Code: 176917792057  
© GCSLC. Proprietary.

---

## 1. Resolve Path Errors ("File does not exist: 8R")

**Cause:** If the dashboard folder is named with spaces (e.g. `8R Stealth B_files`), running  
`streamlit run 8R Stealth B_files/nrrfc_dashboard.py`  
makes the shell split at spaces, so Streamlit receives only `8R` as the script name → "File does not exist: 8R".

**Fixes applied:**
- **Launch script:** `run_nrrfc_dashboard_8051.sh` is space-safe: all internal and terminal references use double-quoted variables (`"$ROOT"`, `"$DASHBOARD_SCRIPT"`). The script tries `"8R Stealth B_files/nrrfc_dashboard.py"` first, then falls back to `"B_Files/nrrfc_dashboard.py"`, so it works for either folder name without editing.
- **Internal paths:** Python uses `os.path.abspath(__file__)` and `dirname` in the dashboard; no change needed for space-safe resolution.
- **Docs:** All launch commands use double-quoted paths where the path may contain spaces. For a **clean push to GitHub**, ensure any script or CI uses quoted paths (e.g. `run "8R Stealth B_files/nrrfc_dashboard.py"` or `"B_Files/nrrfc_dashboard.py"`).

---

## 2. Recover Dashboard History (nrrfc_dashboard.py)

- **Git:** The repo has history for `B_Files/nrrfc_dashboard.py`. Commit `a95d521` (and earlier) had a version that was the **GEC_COAL_BASE_13** module (9.6× wealth multiplier, 1,205 MW, 13-state corridor). The **current** `B_Files/nrrfc_dashboard.py` is the **Streamlit UI** that:
  - Shows **$170.85B** total cycle and **9.6×** wealth multiplier (Germanium/Ammonia) as primary display.
  - Uses **1,205 MW** power logic (13-state AI-DC corridor; 1,203 MW appears in some legacy docs).
  - Has **CAC AV Code: 176917792057** and **Chairman: Dr. Sa'ad Jaafaru** in the header.
- **Local History / state.vscdb:** Cursor/VSCode “Open Timeline” (Local History) and `workspaceStorage/state.vscdb` live **outside this repo** (in your user profile). To restore an older editor version:
  1. In Cursor: right‑click `B_Files/nrrfc_dashboard.py` → **Open Timeline** (or Command Palette → “Local History: Find Entry to Restore”).
  2. Or inspect `~/Library/Application Support/Cursor/User/workspaceStorage/` (macOS) for the workspace and open `state.vscdb` (SQLite) if you need to recover state; the actual file content is usually in the workspace folder’s local history.
- **Current (GitHub/Vercel-linked) dashboard:** `B_Files/nrrfc_dashboard.py` includes **1,203 MW** power logic, **9.6×** wealth multiplier, **$50.1M** monthly revenue, **$170.85B** total cycle, and the **S24 Ultra navy-and-gold** optimized UI. D3 constants and 8R determinants are imported from project root via `sys.path.insert(0, _ROOT)`.

---

## 3. Sync external hooks (GitHub/Vercel ↔ local .env)

- **Re-align local with deployment:** So the live data stream remains accessible on your mobile device, keep **local .env** in sync with **GitHub/Vercel**:
  - **Vercel:** Project → Settings → Environment Variables — use the **exact same variable names** as in `.env.example` (e.g. `GCSLC_ABUJA_IPS`, `GCSLC_DASHBOARD_BASE_URL`).
  - **Local:** Copy `.env.example` to `.env` (or `.env.local`) and fill with the same values you use in Vercel (or leave commented for defaults).
  - **GitHub Actions / CI:** If you use secrets, map them to the same env var names so builds and the deployed app see identical config.
- **No secrets in repo:** This repo does not commit real `.env` values; only `.env.example` is tracked.

**`.env.example`** (in repo) documents expected variables:

```bash
# GCSLC Sovereign Gateway — Vercel / S24 Ultra live data (map in Vercel Dashboard)
# Do not commit real values; copy to .env and fill.

# Optional: comma-separated IPs allowed to see full 8R data (default: 127.0.0.1,::1)
# GCSLC_ABUJA_IPS=127.0.0.1,::1

# Optional: base URL of deployed dashboard (for S24 Ultra / mobile)
# GCSLC_DASHBOARD_BASE_URL=https://your-vercel-app.vercel.app

# Add any other keys your Vercel deployment or API expects
```

- **Vercel build:** If the dashboard is deployed as a Streamlit app, use a build command that runs Streamlit or a wrapper; ensure the **root directory** and **script path** in Vercel match the quoted path (e.g. `B_Files/nrrfc_dashboard.py` or `8R Stealth B_files/nrrfc_dashboard.py` with proper quoting in the build config).

---

## 4. Chairman Verification

- **CAC AV Code: 176917792057** and **Chairman: Dr. Sa'ad Jaafaru** are in:
  - **Header** of `B_Files/nrrfc_dashboard.py` (navy/gold bar).
  - **Footer** of the same file.
  - `B_Files/GEC_COAL_BASE_13.py` (PROPRIETARY_FOOTER, CAC_ANCHOR, CHAIRMAN_ANCHOR from `d8_logic`).
  - `d8_logic.py` (CAC_ANCHOR, CHAIRMAN_ANCHOR).
  - `PORTS.md` and this audit.

---

## 5. Final Launch Command (space-safe, Port 8051)

**Exact, space-safe terminal command** (run from project root):

```bash
cd "/Users/user/Desktop/GCSLC_Sovereign_Gateway" && source ".venv/bin/activate" && streamlit run "B_Files/nrrfc_dashboard.py" --server.port 8051
```

If your folder is named **8R Stealth B_files**, use the same command with that path in quotes. **Or use the launch script** (auto-detects folder; all refs quoted): `./run_nrrfc_dashboard_8051.sh`. Then open **http://localhost:8051**.

**Using the launch script (recommended):**  
Edit `run_nrrfc_dashboard_8051.sh` and set `DASHBOARD_SCRIPT` to the path above (with quotes in the script), then:
```bash
./run_nrrfc_dashboard_8051.sh
```

**With venv:**
```bash
cd /Users/user/Desktop/GCSLC_Sovereign_Gateway
source .venv/bin/activate
streamlit run "B_Files/nrrfc_dashboard.py" --server.port 8051
```

Then open **http://localhost:8051**. Using the **quoted** path avoids the “File does not exist: 8R” error.

---

## Summary

| Item | Status |
|------|--------|
| Path errors (spaces → 8R) | Fixed via quoted paths in script and docs |
| Dashboard history | Git has prior versions; Local History/state.vscdb in Cursor profile |
| 9.6× + 1,203 MW + navy/gold | In `nrrfc_dashboard.py` (GitHub/Vercel-linked); d8_logic at root |
| GitHub–Vercel env | .env.example added; map same keys in Vercel and locally |
| CAC + Chairman | In dashboard header and footer |
| Launch on 8051 | `streamlit run "B_Files/nrrfc_dashboard.py" --server.port 8051` (or script) |
