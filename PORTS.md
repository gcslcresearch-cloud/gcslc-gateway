# GCSLC Sovereign Gateway — Active Ports

**Chairman & Founder: Dr. Sa'ad Jaafaru** — locked at top on all four ports.

| Port | App | Script | Launch |
|------|-----|--------|--------|
| **8051** | NRRFC Coal SSMV (9.6× Multiplier) | `GCSLC_DASHBOARDS/1_NRRFC_9.6x_Multiplier.py` | `./run_nrrfc_coal_8051.sh` |
| **8051** | NRRFC Dashboard (8R B_Files; 9.6×, 1,205 MW) | `B_Files/nrrfc_dashboard.py` | `./run_nrrfc_dashboard_8051.sh` |
| **8052** | Sovereign Asset Dashboard (AWC Portal) | `coal_corridor_8052.py` | `./run_coal_corridor_8052.sh` or `./GCSLC_DASHBOARDS/2_AWC_Portal_Launcher.sh` |
| **8053** | 8R Strike (AWC Coal/Diamond) | `GCSLC_DASHBOARDS/3_AWC_Coal_Diamond.py` | `./run_strike_command_8053.sh` |
| **8054** | AWC Portal — Sovereign Cloud, Eagle, AI-Compute (Continental View) | `awc_portal_8054.py` | `./run_awc_portal_8054.sh` |

## Path mapping (project sidebar)

- **Coal SSMV (8051):** `GCSLC_Sovereign_Gateway/GCSLC_DASHBOARDS/1_NRRFC_9.6x_Multiplier.py` — see also `Coal_SSMV/README.md`
- **NRRFC Dashboard (8051):** `GCSLC_Sovereign_Gateway/B_Files/nrrfc_dashboard.py` — 9.6×, $170.85B, 1,205 MW, 13 states; space-safe launch: `./run_nrrfc_dashboard_8051.sh` or `streamlit run "B_Files/nrrfc_dashboard.py" --server.port 8051`
- **Coal Corridor (8052):** `GCSLC_Sovereign_Gateway/coal_corridor_8052.py` — 13-state Coal and By-products corridor, 639.3 Mt, 1,205 MW (WPC 2026 Roadmap Ready), $72B, 94%/22% reveal
- **8R Strike (8053):** `GCSLC_Sovereign_Gateway/GCSLC_DASHBOARDS/3_AWC_Coal_Diamond.py`
- **AWC Portal (8054):** `GCSLC_Sovereign_Gateway/awc_portal_8054.py` — Sovereign Cloud interface, RealTimeEngine 60s ($50.1M, 1,203 MW, 9.6×), Apex Eagle. The Eagle flies on 8054.

## One-line launch (from project root)

**Space-safe:** Use double quotes around any path that contains spaces (e.g. `8R Stealth B_files`) to avoid "File does not exist: 8R".

```bash
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run GCSLC_DASHBOARDS/1_NRRFC_9.6x_Multiplier.py --server.port 8051
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run "B_Files/nrrfc_dashboard.py" --server.port 8051
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run coal_corridor_8052.py --server.port 8052
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run GCSLC_DASHBOARDS/3_AWC_Coal_Diamond.py --server.port 8053
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run awc_portal_8054.py --server.port 8054
```

Or use the scripts: `./run_nrrfc_coal_8051.sh`, `./run_nrrfc_dashboard_8051.sh`, `./run_coal_corridor_8052.sh`, `./run_strike_command_8053.sh`, `./run_awc_portal_8054.sh`. **Launch 8051+8052+8053 at once:** `./GCSLC_DASHBOARDS/LAUNCH_ALL.sh`. See **PROJECT_AUDIT.md** for full audit and space-safe commands.

## WordPress deployment (Full Width)

- **Custom HTML IFrame blocks:** See `wordpress_iframe_blocks.html`. One block per port (8051–8054), each with $1.5 Trillion Wealth Cloud and $72B Opportunity Gap overlays. Replace `YOUR_BASE_URL` with your gateway base URL before pasting into a WordPress Full Width section.
