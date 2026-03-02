# GCSLC Sovereign Gateway — Active Ports

**Chairman & Founder: Dr. Sa'ad Jaafaru** — locked at top on all four ports.

| Port | App | Script | Launch |
|------|-----|--------|--------|
| **8051** | NRRFC Coal SSMV (NWC/C&D) | `nrrfc_coal_8051.py` | `./run_nrrfc_coal_8051.sh` |
| **8052** | Sovereign Asset Dashboard (Coal Corridor) | `coal_corridor_8052.py` | `./run_coal_corridor_8052.sh` |
| **8053** | 8R Strike Command (Wealth Cloud) | `strike_command_8053.py` | `./run_strike_command_8053.sh` |
| **8054** | AWC Portal (Continental View) | `awc_portal_8054.py` | `./run_awc_portal_8054.sh` |

## Path mapping (project sidebar)

- **Coal SSMV (8051):** `GCSLC_Sovereign_Gateway/nrrfc_coal_8051.py` — see also `Coal_SSMV/README.md`
- **Coal Corridor (8052):** `GCSLC_Sovereign_Gateway/coal_corridor_8052.py` — 12-state Coal and By-products corridor, $72B, 94%/22% reveal
- **8R Strike (8053):** `GCSLC_Sovereign_Gateway/strike_command_8053.py`
- **AWC Portal (8054):** `GCSLC_Sovereign_Gateway/awc_portal_8054.py`

## One-line launch (from project root)

```bash
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run nrrfc_coal_8051.py --server.port 8051
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run coal_corridor_8052.py --server.port 8052
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run strike_command_8053.py --server.port 8053
cd /path/to/GCSLC_Sovereign_Gateway && source .venv/bin/activate && streamlit run awc_portal_8054.py --server.port 8054
```

Or use the scripts: `./run_nrrfc_coal_8051.sh`, `./run_coal_corridor_8052.sh`, `./run_strike_command_8053.sh`, `./run_awc_portal_8054.sh`.
