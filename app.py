"""
NVFC Sovereign Pulse — Streamlit app with Status sidebar and High-Velocity Nigeria map.
Run: streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="NVFC Sovereign Pulse",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Shimmer gold + Playfair + Status widget CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    .shimmer-gold {
        background: linear-gradient(90deg, #d4af37, #f9f295, #ffffff, #f9f295, #d4af37);
        background-size: 200% auto;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer_flow 3s linear infinite;
        font-weight: bold;
    }
    @keyframes shimmer_flow { to { background-position: 200% center; } }

    [data-testid="stSidebar"] {
        min-width: 180px !important;
        max-width: 180px !important;
    }
    [data-testid="stSidebar"] .stMarkdown { font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# Slim Status sidebar (180px)
with st.sidebar:
    st.markdown('<p class="shimmer-gold" style="font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 12px;">STATUS</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #00ff88; margin: 6px 0;">● ACTIVE</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #00ff88; margin: 6px 0;">● ACTIVE</p>', unsafe_allow_html=True)
    st.markdown('<p class="shimmer-gold" style="margin: 6px 0;">● RESERVE</p>', unsafe_allow_html=True)
    for _ in range(6):
        st.markdown('<p class="shimmer-gold" style="margin: 6px 0;">● RESERVE</p>', unsafe_allow_html=True)

# Main: NVFC branding + High-Velocity Map of Nigeria
st.markdown('<h1 class="shimmer-gold" style="text-align: center;">GCSLC · NVFC STRATEGIC COMMAND</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="shimmer-gold" style="font-size: 1.25rem;">NATIONAL VELOCITY FALCON CLOUD — High-Velocity Map</h2>', unsafe_allow_html=True)

# High-Velocity Map of Nigeria (inline SVG)
st.markdown("""
<div style="
    background: rgba(10, 10, 10, 0.6);
    border: 1px solid rgba(212, 175, 55, 0.4);
    border-radius: 12px;
    padding: 24px;
    min-height: 360px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 16px 0;
">
    <svg viewBox="0 0 200 240" width="100%" max-width="320px" style="opacity: 0.85;" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="ng_gold" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#d4af37"/>
                <stop offset="50%" stop-color="#f9f295"/>
                <stop offset="100%" stop-color="#d4af37"/>
            </linearGradient>
        </defs>
        <path fill="none" stroke="url(#ng_gold)" stroke-width="2" d="M100 20 L160 50 L180 100 L165 160 L120 220 L80 200 L40 150 L35 90 L60 40 Z"/>
    </svg>
</div>
<p style="text-align: center; color: #888; font-size: 0.8rem;">Nigeria — Sovereign Grid · NVFC</p>
""", unsafe_allow_html=True)

# Footer: Shimmering gold signature (Playfair Display)
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center;">
    <h1 class="shimmer-gold" style="font-family: 'Playfair Display', serif; font-size: 2.2rem; margin-bottom: 0;">
        Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)
    </h1>
    <p class="shimmer-gold" style="letter-spacing: 4px; font-size: 0.85rem; opacity: 0.9;">NVFC STRATEGIC COMMAND | GCSLC LTD/GTE</p>
</div>
""", unsafe_allow_html=True)
