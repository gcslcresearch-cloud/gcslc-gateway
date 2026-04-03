# Hugging Face Spaces / Docker entrypoint — GCSLC CIEN Kaduna 2027 dashboard.
# HF’s Streamlit Docker template expects `streamlit_app.py` at the repo root.
# Local dev may still use: python3 -m streamlit run cien_kaduna_2027.py --server.port 9099
#
# PAYMENT_GATEWAY_KEY / TERMII_API_KEY: warm the secrets store before importing the app so
# Streamlit never surfaces a red error bar from ``st.secrets`` when no local secrets.toml exists.
# Missing keys are handled in cien_kaduna_2027 with ``load_if_toml_exists`` + ``.get`` (info banner only).

import streamlit as st

_lif = getattr(st.secrets, "load_if_toml_exists", None)
if callable(_lif):
    _lif()

from cien_kaduna_2027 import main

if __name__ == "__main__":
    main()
