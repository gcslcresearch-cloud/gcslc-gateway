"""
NVFC Sovereign Pulse — Streamlit app for National Velocity Falcon Cloud command.
Run: streamlit run nvfc_sovereign_pulse.py
"""
import streamlit as st
import streamlit.components.v1 as components

map_svg = """
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 10px rgba(212,175,55,0.3));">
    <path d="M150,400 Q400,50 650,400" fill="none" stroke="#f9f295" stroke-width="0.8" opacity="0.4">
        <animate attributeName="stroke-dasharray" values="0,1000;1000,0" dur="2.5s" repeatCount="indefinite" />
    </path>
    
    <path d="M250,150 L380,80 L550,110 L680,250 L620,480 L420,550 L180,520 L120,320 Z" 
          fill="rgba(212, 175, 55, 0.05)" 
          stroke="#d4af37" 
          stroke-width="2" />
          
    <circle cx="380" cy="220" r="5" fill="#f9f295">
        <animate attributeName="r" values="5;12;5" dur="2s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite" />
    </circle>
    <text x="400" y="225" fill="#f9f295" font-family="monospace" font-size="12">NVFC COMMAND HUB</text>
</svg>
"""

# Dashboard Configuration
st.set_page_config(
    page_title="NVFC Sovereign Pulse",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS: Deep Navy background + layered text/map + slim Status widget + shimmer gold
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    /* Deep Navy Blue app background */
    .stApp {
        background-color: #0a0a2e;
    }
    
    /* Layer all Streamlit text and blocks cleanly over navy */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #e8eef4 !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: inherit;
    }
    [data-testid="stVerticalBlock"] > div {
        background: transparent;
    }
    
    /* Slim Status Archive widget (180px) with gold border */
    .status-widget {
        border: 1px solid #d4af37;
        padding: 15px;
        background: rgba(10, 10, 46, 0.95);
        border-radius: 4px;
        width: 180px;
    }

    /* Shimmer gold for header, status, and signature — high-contrast on navy */
    .shimmer-gold {
        background: linear-gradient(90deg, #d4af37, #f9f295, #d4af37);
        background-size: 200% auto;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer_flow 2.5s linear infinite;
        font-weight: bold;
    }
    @keyframes shimmer_flow { to { background-position: 200% center; } }
    
    /* Footer signature: ensure high-contrast on navy */
    .signature-block .shimmer-gold { opacity: 1; }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown(
    '<h1 class="shimmer-gold" style="text-align: center;">GCSLC STRATEGIC COMMAND</h1>',
    unsafe_allow_html=True,
)

# Layout Architecture
col_side, col_map = st.columns([1, 4])

with col_side:
    st.markdown("""
    <div class="status-widget">
        <p class="shimmer-gold" style="font-size: 0.8rem; letter-spacing: 2px;">STATUS ARCHIVE</p>
        <p style="color: #00ff88; margin: 5px 0;">● ACTIVE</p>
        <p style="color: #00ff88; margin: 5px 0;">● ACTIVE</p>
        <p class="shimmer-gold" style="margin: 5px 0;">● RESERVE</p>
    </div>
    """, unsafe_allow_html=True)

with col_map:
    st.markdown(
        '<h2 class="shimmer-gold">NATIONAL VELOCITY FALCON CLOUD (NVFC)</h2>',
        unsafe_allow_html=True,
    )
    components.html(
        f'<div style="background:#0a0a2e; padding:0; margin:0;">{map_svg}</div>',
        height=500,
    )

# Footer: Shimmering gold signature — high-contrast on navy
st.markdown("<br><br><hr style='border-color: rgba(212,175,55,0.3);'>", unsafe_allow_html=True)
st.markdown("""
<div class="signature-block" style="text-align: center;">
    <h1 class="shimmer-gold" style="font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 0;">
        Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)
    </h1>
    <p class="shimmer-gold" style="letter-spacing: 5px; font-size: 0.9rem;">
        NVFC STRATEGIC COMMAND | GCSLC LTD/GTE
    </p>
</div>
""", unsafe_allow_html=True)
