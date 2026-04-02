# Hugging Face Spaces / Docker entrypoint — GCSLC CIEN Kaduna 2027 dashboard.
# HF’s Streamlit Docker template expects `streamlit_app.py` at the repo root.
# Local dev may still use: python3 -m streamlit run cien_kaduna_2027.py --server.port 9099

from cien_kaduna_2027 import main

if __name__ == "__main__":
    main()
