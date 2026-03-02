# GCSLC Sovereign Gateway — Active Ports

**Chairman & Founder: Dr. Sa'ad Jaafaru** — locked at top on all four ports.

| Port | App | Script | Launch |
|------|-----|--------|--------|
| **8051** | NRRFC Coal SSMV (NWC/C&D) | `nrrfc_coal_8051.py` | `./run_nrrfc_coal_8051.sh` |
| **8052** | Sovereign Asset Dashboard (Coal Corridor) | `coal_corridor_8052.py` | `./run_coal_corridor_8052.sh` |
| **8053** | 8R Strike Command (Wealth Cloud) | `strike_command_8053.py` | `./run_strike_command_8053.sh` |
| **8054** | AWC Portal (Continental View) | `awc_portal_8054.py` | `./run_awc_portal_8054.sh` |
| **8055** | Aliyu Riyadh Mirror (Secure Remote Dashboard) | `aliyu_riyadh_access.py` | `./run_aliyu_riyadh_8055.sh` |

## Path mapping (project sidebar)

- **Coal SSMV (8051):** `GCSLC_Sovereign_Gateway/nrrfc_coal_8051.py` — see also `Coal_SSMV/README.md`
- **Coal Corridor (8052):** `GCSLC_Sovereign_Gateway/coal_corridor_8052.py` — 13-state Coal and By-products corridor, 639.3 Mt, 1,205 MW (WPC 2026 Roadmap Ready), $72B, 94%/22% reveal
- **8R Strike (8053):** `GCSLC_Sovereign_Gateway/strike_command_8053.py`
- **AWC Portal (8054):** `GCSLC_Sovereign_Gateway/awc_portal_8054.py`
- **Aliyu Riyadh Mirror (8055):** `GCSLC_Sovereign_Gateway/aliyu_riyadh_access.py` — secure remote dashboard for AWC & GEC revitalization; D1/D2/D3/D7 BUA/NVIDIA Sovereign Strike prep.

## One-line launch (from project root)

```bash
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run nrrfc_coal_8051.py --server.port 8051
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run coal_corridor_8052.py --server.port 8052
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run strike_command_8053.py --server.port 8053
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run awc_portal_8054.py --server.port 8054
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run aliyu_riyadh_access.py --server.port 8055
```

Or use the scripts: `./run_nrrfc_coal_8051.sh`, `./run_coal_corridor_8052.sh`, `./run_strike_command_8053.sh`, `./run_awc_portal_8054.sh`, `./run_aliyu_riyadh_8055.sh`.

## WordPress deployment (Full Width)

- **Custom HTML IFrame blocks:** See `wordpress_iframe_blocks.html`. One block per port (8051–8054), each with $1.5 Trillion Wealth Cloud and $72B Opportunity Gap overlays. Replace `YOUR_BASE_URL` with your gateway base URL before pasting into a WordPress Full Width section.
