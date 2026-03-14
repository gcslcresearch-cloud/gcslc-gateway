"""
Sovereign Mirror — Digital Doorstep for GCSLC
Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE.
Cinematic entry for global titans (Silicon Valley, Wall Street, Sovereign Wealth Funds).
Password: 8R-DECODE-2026 → Sovereign Bridge → K-GEC Terminal (localhost:8054).
© 2026 GCSLC. Chairman & Founder: Dr. Sa'ad Jaafaru.
"""

import streamlit as st

# --- Page config (must be first Streamlit call) ---
st.set_page_config(
    page_title="Sovereign Mirror — GCSLC",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Session state ---
if "mirror_decoded" not in st.session_state:
    st.session_state.mirror_decoded = False

# --- Design tokens ---
NAVY = "#000033"
GOLD = "#D4AF37"
K_GEC_URL = "http://localhost:8054"
PASSWORD_UNLOCK = "8R-DECODE-2026"
FULL_NAME = "Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE"
SIGNATURE = "Dr. Jaafaru Sa'ad — Chairman & Founder"
TICKER_TEXT = "COAL [NGECC]: $170.8B INDEX  |  SILICON FEEDSTOCK: 639.3M MT  |  GERMANIUM PULSE: ACTIVE  |  ABUJA-ZARIA-KANO CORRIDOR"

# --- Global CSS: Institutional Navy, Sovereign Gold, Goldman font, Prism, Pulse, Ticker, Signature, Bridge ---
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');

:root {
    --institutional-navy: #000033;
    --sovereign-gold: #D4AF37;
    --gold-light: rgba(212, 175, 55, 0.95);
    --gold-subtle: rgba(212, 175, 55, 0.6);
}

/* Base: deep navy, gold accents */
.stApp, [data-testid="stAppViewContainer"], .main .block-container {
    background: var(--institutional-navy) !important;
    color: var(--sovereign-gold) !important;
}
.main .block-container { padding: 1rem 2rem 6rem; max-width: 100%; }

/* All headers: Goldman */
h1, h2, h3, .gcslc-header, .pulse-box h3, .ticker-text {
    font-family: 'Goldman', sans-serif !important;
    color: var(--sovereign-gold) !important;
}

/* Shimmering Prism: liquid gold and white light across full name */
.prism-name {
    font-family: 'Goldman', sans-serif !important;
    font-size: clamp(1.25rem, 3vw, 2rem) !important;
    font-weight: 700;
    text-align: center;
    letter-spacing: 0.02em;
    line-height: 1.4;
    background: linear-gradient(
        110deg,
        #D4AF37 0%,
        #F9F295 15%,
        #FFFFFF 35%,
        #F9F295 55%,
        #D4AF37 75%,
        #B8960C 100%
    );
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: prism-shimmer 4s ease-in-out infinite;
}
@keyframes prism-shimmer {
    0%, 100% { background-position: 0% center; }
    50% { background-position: 100% center; }
}

/* 8R Prosperity Pulse: three diagonal boxes with breathing zoom */
.pulse-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin: 2rem 0;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}
.pulse-box {
    background: rgba(0, 0, 51, 0.6);
    border: 2px solid var(--sovereign-gold);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    animation: pulse-breathe 3.5s ease-in-out infinite;
    transform-origin: center;
}
.pulse-box h3 {
    font-size: clamp(0.9rem, 1.5vw, 1.1rem);
    margin: 0 0 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.pulse-box .value {
    font-family: 'Goldman', sans-serif;
    font-size: clamp(1.1rem, 2vw, 1.4rem);
    font-weight: 700;
    color: var(--sovereign-gold);
}
@keyframes pulse-breathe-1 {
    0%, 100% { transform: rotate(-1.5deg) scale(1); }
    50% { transform: rotate(-1.5deg) scale(1.04); }
}
@keyframes pulse-breathe-2 {
    0%, 100% { transform: rotate(1deg) scale(1); }
    50% { transform: rotate(1deg) scale(1.04); }
}
@keyframes pulse-breathe-3 {
    0%, 100% { transform: rotate(-1deg) scale(1); }
    50% { transform: rotate(-1deg) scale(1.04); }
}
.pulse-box:nth-child(1) { animation: pulse-breathe-1 3.5s ease-in-out 0s infinite; }
.pulse-box:nth-child(2) { animation: pulse-breathe-2 3.5s ease-in-out 0.2s infinite; }
.pulse-box:nth-child(3) { animation: pulse-breathe-3 3.5s ease-in-out 0.4s infinite; }

/* Live Ticker: smooth infinite scroll */
.ticker-wrap {
    position: fixed;
    bottom: 3rem;
    left: 0;
    right: 0;
    height: 2.5rem;
    background: rgba(0, 0, 51, 0.95);
    border-top: 2px solid var(--sovereign-gold);
    overflow: hidden;
    z-index: 900;
    display: flex;
    align-items: center;
}
.ticker-inner {
    display: flex;
    animation: ticker-scroll 35s linear infinite;
    white-space: nowrap;
}
.ticker-text {
    font-family: 'Goldman', sans-serif;
    font-size: 0.9rem;
    color: var(--sovereign-gold);
    letter-spacing: 0.15em;
    padding: 0 3rem;
}
@keyframes ticker-scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

/* Signature watermark */
.signature-watermark {
    position: fixed;
    bottom: 0.5rem;
    right: 1rem;
    font-family: 'Goldman', sans-serif;
    font-size: 0.7rem;
    color: var(--gold-subtle);
    letter-spacing: 0.08em;
    z-index: 901;
    opacity: 0.85;
}

/* Sovereign Bridge overlay (after password) */
.bridge-overlay {
    position: fixed;
    inset: 0;
    background: var(--institutional-navy);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    animation: bridge-fade-in 0.5s ease-out;
}
.bridge-scan {
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, transparent, var(--sovereign-gold), transparent);
    animation: bridge-scan 2s ease-in-out 1;
    box-shadow: 0 0 20px var(--sovereign-gold);
}
.bridge-title {
    font-family: 'Goldman', sans-serif;
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    color: var(--sovereign-gold);
    margin: 2rem 0;
    letter-spacing: 0.2em;
    animation: bridge-glow 1.5s ease-in-out 2;
}
@keyframes bridge-fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
}
@keyframes bridge-scan {
    0% { transform: translateY(-100vh); }
    100% { transform: translateY(100vh); }
}
@keyframes bridge-glow {
    0%, 100% { opacity: 1; text-shadow: 0 0 20px var(--gold-subtle); }
    50% { opacity: 0.9; text-shadow: 0 0 40px var(--sovereign-gold); }
}

/* Password input styling */
div[data-testid="stVerticalBlock"] > div:has(input) label {
    font-family: 'Goldman', sans-serif !important;
    color: var(--sovereign-gold) !important;
}
.stTextInput input { border: 2px solid var(--sovereign-gold) !important; border-radius: 8px !important; }
.stButton > button {
    font-family: 'Goldman', sans-serif !important;
    background: transparent !important;
    color: var(--sovereign-gold) !important;
    border: 2px solid var(--sovereign-gold) !important;
    border-radius: 8px !important;
}
.stButton > button:hover {
    background: rgba(212, 175, 55, 0.15) !important;
    border-color: var(--sovereign-gold) !important;
    color: var(--sovereign-gold) !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .pulse-grid { grid-template-columns: 1fr; gap: 1rem; }
    .pulse-box:nth-child(1), .pulse-box:nth-child(2), .pulse-box:nth-child(3) { transform: none; }
    .main .block-container { padding: 0.75rem 1rem 5rem; }
    .ticker-wrap { bottom: 2.5rem; height: 2rem; }
    .ticker-text { font-size: 0.75rem; }
    .signature-watermark { font-size: 0.6rem; right: 0.5rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Post-decode: Sovereign Bridge + K-GEC entry ---
if st.session_state.mirror_decoded:
    st.markdown(
        """
        <div class="bridge-overlay" id="gcslc-bridge">
            <div class="bridge-scan"></div>
            <p class="bridge-title">SOVEREIGN BRIDGE</p>
            <p style="font-family: Goldman, sans-serif; color: rgba(212,175,55,0.8); font-size: 0.95rem;">Decode verified. Proceed to K-GEC Terminal.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### Sovereign Bridge — Access granted")
    st.markdown("The Digital Doorstep has verified your decode. Enter the K-GEC Terminal to continue.")
    st.link_button("Enter K-GEC Terminal →", url=K_GEC_URL, type="primary")
    st.caption(f"Or open in browser: {K_GEC_URL}")
    st.markdown(
        f'<div class="ticker-wrap"><div class="ticker-inner"><span class="ticker-text">{TICKER_TEXT}</span><span class="ticker-text">{TICKER_TEXT}</span></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="signature-watermark">{SIGNATURE}</div>', unsafe_allow_html=True)
    st.stop()

# --- Main Mirror: Digital Doorstep ---
st.markdown('<p class="gcslc-header" style="text-align:center; font-size:0.9rem; letter-spacing:0.2em; margin-bottom:0.5rem;">DIGITAL DOORSTEP</p>', unsafe_allow_html=True)
st.markdown(f'<p class="prism-name">{FULL_NAME}</p>', unsafe_allow_html=True)
st.markdown("---")

# 8R Prosperity Pulse: three diagonal boxes
st.markdown(
    """
    <div class="pulse-grid">
        <div class="pulse-box">
            <h3>Asset Anchor</h3>
            <p class="value">$170.85B</p>
            <p style="font-size:0.8rem; color: rgba(212,175,55,0.8);">Valuation anchor</p>
        </div>
        <div class="pulse-box">
            <h3>Sovereign Value</h3>
            <p class="value">8R Stealth</p>
            <p style="font-size:0.8rem; color: rgba(212,175,55,0.8);">Paradigm lock</p>
        </div>
        <div class="pulse-box">
            <h3>Abundance</h3>
            <p class="value">639.3M MT</p>
            <p style="font-size:0.8rem; color: rgba(212,175,55,0.8);">Coal-to-compute</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown("#### Access the K-GEC Terminal")
pwd = st.text_input("Decode phrase", type="password", placeholder="Enter decode phrase", key="mirror_pwd", label_visibility="collapsed")
col1, col2, _ = st.columns([1, 1, 2])
with col1:
    submit = st.button("Decode")
with col2:
    pass
if submit and pwd.strip() == PASSWORD_UNLOCK:
    st.session_state.mirror_decoded = True
    st.rerun()
elif submit and pwd:
    st.caption("Incorrect decode phrase.")

# Live Ticker (duplicated content for seamless loop)
st.markdown(
    f'<div class="ticker-wrap"><div class="ticker-inner"><span class="ticker-text">{TICKER_TEXT}</span><span class="ticker-text">{TICKER_TEXT}</span></div></div>',
    unsafe_allow_html=True,
)
st.markdown(f'<div class="signature-watermark">{SIGNATURE}</div>', unsafe_allow_html=True)
