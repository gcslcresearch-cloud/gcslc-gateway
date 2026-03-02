"""
Aliyu Riyadh Mirror — Secure Remote Dashboard for AWC & GEC Revitalization
D1 Refine | D2 Reset | D3 Research | D7 Re-engineer — BUA/NVIDIA Sovereign Strike prep.
GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION LTD/GTE — CAC: 176917792057.
© 2026 GCSLC. Proprietary. Secure access only.
"""
import os
import streamlit as st

st.set_page_config(
    page_title="Aliyu Riyadh Access — AWC & GEC | GCSLC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CAC and shimmer — unscrambled visual proof of sovereignty (never obfuscated)
CAC_CODE = "176917792057"
LEGAL_NAME = "GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION LTD/GTE"

# Sovereign aesthetic — Navy & Gold; CAC and shimmer remain unscrambled
st.markdown("""
<style>
.stApp { background-color: #002147 !important; min-height: 100vh; }
[data-testid="stAppViewContainer"] { background-color: #002147 !important; }
.main .block-container { background-color: #002147 !important; max-width: 100%; padding: 1rem 2rem; }
h1, h2, h3, p, span, label, .stMarkdown { color: #D4AF37 !important; }
.gcslc-legal-name-shimmer { background: linear-gradient(90deg, #002147, #D4AF37, #FFE55C, #D4AF37, #002147); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent !important; animation: gcslc-shimmer 4s linear infinite; }
@keyframes gcslc-shimmer { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
.gcslc-sovereign-footer { position: fixed; bottom: 0; left: 0; right: 0; z-index: 999; background: linear-gradient(180deg, rgba(0,26,51,0.97) 0%, #001a33 100%); border-top: 2px solid rgba(212,175,55,0.4); padding: 0.45rem 1rem; font-size: 0.75rem; color: #D4AF37; text-align: center; }
.gcslc-sovereign-footer .cac { letter-spacing: 0.1em; opacity: 0.95; }
.gcslc-sovereign-footer .chairman { font-weight: 700; margin-top: 0.2rem; }
.main .block-container { padding-bottom: 4rem !important; }
.mirror-card { background: rgba(212,175,55,0.12); border: 1px solid #D4AF37; border-radius: 12px; padding: 1rem 1.25rem; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# Header — CAC and shimmer: unscrambled visual proof
st.markdown(
    f'<div style="position: sticky; top: 0; z-index: 100; background: linear-gradient(180deg, #002147 0%, rgba(0,33,71,0.98) 100%); padding-bottom: 10px; margin-bottom: 12px; border-bottom: 1px solid rgba(212,175,55,0.25);">'
    f'<p class="gcslc-legal-name-shimmer" style="text-align: center; font-weight: 800; font-size: 0.95rem; margin: 0;">{LEGAL_NAME} | CAC: {CAC_CODE} | Chairman & Founder: Dr. Sa\'ad Jaafaru</p>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown("### Aliyu Riyadh Mirror — Secure Remote Dashboard")
st.caption("AWC & GEC revitalization. D1, D2, D3, D7 — BUA/NVIDIA Sovereign Strike prep. CAC & shimmer: unscrambled visual proof of sovereignty.")

# Secure access placeholder (D7 Re-engineer: secure gateway)
access_key = st.sidebar.text_input("Access key (secure)", type="password", key="riyadh_key")
if not access_key:
    st.info("Enter access key in sidebar to unlock dashboard links.")
else:
    st.success("Access granted. Dashboard links below.")

st.markdown("---")
st.write("#### AWC & GEC Portals — Revitalization")

# Base URL for links (user can set via env or default localhost)
BASE_URL = os.environ.get("GCSLC_GATEWAY_BASE", "http://localhost")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        f'<div class="mirror-card">'
        f'<p style="font-weight: 700; color: #FFD700;">African Wealth Cloud (AWC)</p>'
        f'<p style="color: #D4AF37; font-size: 0.9rem;">Continental view, Sovereign Glass, 8R Convergence.</p>'
        f'<a href="{BASE_URL}:8054" target="_blank" rel="noopener" style="color: #D4AF37; text-decoration: underline;">Open AWC — Port 8054</a>'
        f'</div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f'<div class="mirror-card">'
        f'<p style="font-weight: 700; color: #FFD700;">GEC — Sovereign Asset Dashboard</p>'
        f'<p style="color: #D4AF37; font-size: 0.9rem;">13-state corridor, 1,205 MW, WL Counter, BUA/NVIDIA.</p>'
        f'<a href="{BASE_URL}:8052" target="_blank" rel="noopener" style="color: #D4AF37; text-decoration: underline;">Open GEC — Port 8052</a>'
        f'</div>',
        unsafe_allow_html=True,
    )

col3, col4 = st.columns(2)
with col3:
    st.markdown(
        f'<div class="mirror-card">'
        f'<p style="font-weight: 700; color: #FFD700;">8R Strike Command — Sovereign AI Compute</p>'
        f'<p style="color: #D4AF37; font-size: 0.9rem;">Jensen Huang / NVIDIA portal, 1,205 MW pitch.</p>'
        f'<a href="{BASE_URL}:8053" target="_blank" rel="noopener" style="color: #D4AF37; text-decoration: underline;">Open Strike — Port 8053</a>'
        f'</div>',
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f'<div class="mirror-card">'
        f'<p style="font-weight: 700; color: #FFD700;">NWC/C&D — Port 8051</p>'
        f'<p style="color: #D4AF37; font-size: 0.9rem;">National Wealth Cloud, Coal & Diamond.</p>'
        f'<a href="{BASE_URL}:8051" target="_blank" rel="noopener" style="color: #D4AF37; text-decoration: underline;">Open NWC — Port 8051</a>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption("Aliyu Riyadh Mirror: secure remote dashboard for AWC and GEC revitalization. CAC Code and shimmering branding remain the unscrambled visual proof of GCSLC sovereignty.")

# Footer — CAC and shimmer: unscrambled visual proof
st.markdown(
    f'<div class="gcslc-sovereign-footer">'
    f'<span class="cac">CAC Name Availability Code: {CAC_CODE}</span>'
    f'<p class="chairman" style="font-weight: 700; margin-top: 0.2rem;">{LEGAL_NAME} | Chairman & Founder: Dr. Sa\'ad Jaafaru</p>'
    '<p style="font-size:0.7rem;opacity:0.9;margin-top:0.2rem;">CAC & shimmering branding — unscrambled visual proof of sovereignty.</p>'
    '</div>',
    unsafe_allow_html=True,
)
