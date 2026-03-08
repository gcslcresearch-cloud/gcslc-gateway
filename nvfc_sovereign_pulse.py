"""
NVFC Sovereign Pulse — Streamlit app for National Velocity Falcon Cloud command.
Run: streamlit run nvfc_sovereign_pulse.py
"""
import streamlit as st
import streamlit.components.v1 as components

# Map: 13 states (Enugu, Kogi, Benue, Nasarawa, Gombe, Adamawa, Delta, Edo, Ondo, Bauchi, Anambra, Ebonyi, Abia),
# hovering falcon, Data Center hubs over Nasarawa & Kogi coking coal fields
map_svg = """
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 12px rgba(249,242,149,0.4));">
    <defs>
        <filter id="gold-glow">
            <feGaussianBlur stdDeviation="1" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <path id="falconOrbit" d="M320,380 Q350,340 380,300 Q410,310 420,320 Q440,280 450,250 Q490,265 520,280 Q545,250 560,220 Q520,280 280,450 Q300,430 320,420 Q290,410 260,400 Q400,350 480,300 Q400,360 340,400 Q360,380 380,360 Q370,400 360,420 Q340,400 320,380"/>
    </defs>
    <path d="M150,400 Q400,50 650,400" fill="none" stroke="#f9f295" stroke-width="1.5" opacity="0.9" filter="url(#gold-glow)">
        <animate attributeName="stroke-dasharray" values="0,1000;1000,0" dur="2.5s" repeatCount="indefinite"/>
    </path>
    <path d="M250,150 L380,80 L550,110 L680,250 L620,480 L420,550 L180,520 L120,320 Z" fill="rgba(249,242,149,0.06)" stroke="#f9f295" stroke-width="2.5" filter="url(#gold-glow)"/>
    <!-- 13 highlighted states -->
    <g id="states">
        <circle cx="320" cy="380" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="380" cy="300" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="420" cy="320" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="450" cy="250" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="520" cy="280" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="560" cy="220" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="280" cy="450" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="320" cy="420" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="260" cy="400" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="480" cy="300" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="340" cy="400" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="380" cy="360" r="4" fill="#f9f295" opacity="0.9"/>
        <circle cx="360" cy="420" r="4" fill="#f9f295" opacity="0.9"/>
    </g>
    <!-- Hovering Falcon: slowly circles 13 states -->
    <g fill="#f9f295" filter="url(#gold-glow)" transform="scale(2)">
        <path id="falcon" d="M0,-8 L6,4 L2,4 L4,8 L0,6 L-4,8 L-2,4 L-6,4 Z">
            <animateMotion dur="35s" repeatCount="indefinite" path="M320,380 Q350,340 380,300 Q410,310 420,320 Q440,280 450,250 Q490,265 520,280 Q545,250 560,220 Q520,280 280,450 Q300,430 320,420 Q290,410 260,400 Q400,350 480,300 Q400,360 340,400 Q360,380 380,360 Q370,400 360,420 Q340,400 320,380"/>
        </path>
    </g>
    <!-- Data Center hubs: Nasarawa, Kogi (coking coal fields) — glowing -->
    <g transform="translate(450,250)">
        <rect x="-18" y="-12" width="36" height="22" rx="3" fill="rgba(249,242,149,0.15)" stroke="#f9f295" stroke-width="1.5" filter="url(#gold-glow)"/>
        <text x="0" y="2" text-anchor="middle" fill="#f9f295" font-size="9" font-weight="bold">Data Center</text>
        <text x="0" y="12" text-anchor="middle" fill="#f9f295" font-size="7">Nasarawa</text>
    </g>
    <g transform="translate(380,300)">
        <rect x="-18" y="-12" width="36" height="22" rx="3" fill="rgba(249,242,149,0.15)" stroke="#f9f295" stroke-width="1.5" filter="url(#gold-glow)"/>
        <text x="0" y="2" text-anchor="middle" fill="#f9f295" font-size="9" font-weight="bold">Data Center</text>
        <text x="0" y="12" text-anchor="middle" fill="#f9f295" font-size="7">Kogi</text>
    </g>
    <circle cx="380" cy="220" r="5" fill="#f9f295">
        <animate attributeName="r" values="5;12;5" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="400" y="225" fill="#f9f295" font-family="monospace" font-size="12" filter="url(#gold-glow)">NVFC COMMAND HUB</text>
</svg>
"""

# Dashboard Configuration
st.set_page_config(
    page_title="NVFC Sovereign Pulse",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Sovereign Command Console: Deep Navy + 8R watermark + gold + signature
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    .stApp { background-color: #000033; position: relative; }
    
    /* Brainbox: faint pulsing watermark — 8R Stealth Paradigm Convergence */
    .stApp::after {
        content: '8R Stealth Paradigm Convergence';
        position: fixed;
        left: 0;
        top: 0;
        right: 0;
        bottom: 0;
        background: repeating-linear-gradient(
            -15deg,
            transparent 0px,
            transparent 120px,
            rgba(212,175,55,0.04) 120px,
            rgba(212,175,55,0.04) 121px
        );
        pointer-events: none;
        z-index: 0;
    }
    .stApp::before {
        content: '8R Stealth Paradigm Convergence  •  Sovereign  •  8R Stealth Paradigm Convergence';
        position: fixed;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%) rotate(-12deg);
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: 0.3em;
        color: rgba(212,175,55,0.06);
        white-space: nowrap;
        animation: watermark-pulse 4s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    @keyframes watermark-pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .stMarkdown p, .stMarkdown li, .stMarkdown span { color: #e8eef4 !important; }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: inherit; }
    [data-testid="stVerticalBlock"] > div { background: transparent; position: relative; z-index: 1; }
    
    .status-widget {
        width: 180px;
        border: 2px solid #d4af37;
        padding: 15px;
        background: rgba(0, 0, 51, 0.9);
        border-radius: 4px;
        box-shadow: 0 0 12px rgba(212, 175, 55, 0.2);
    }
    
    .humanoid-bubble {
        border: 1px solid #d4af37;
        background: rgba(0,0,51,0.95);
        border-radius: 8px;
        padding: 10px 12px;
        margin-top: 12px;
        font-size: 0.85rem;
        text-align: center;
        box-shadow: 0 0 10px rgba(212,175,55,0.2);
    }

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
    
    .signature-block { padding: 2rem 0 3rem; text-align: center; }
    .signature-block .shimmer-gold { opacity: 1; }
    
    .gallery-card {
        border: 1px solid rgba(212,175,55,0.5);
        background: rgba(0,0,51,0.8);
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
        font-size: 0.9rem;
    }
    .gallery-card .label { color: #f9f295; font-weight: 700; }
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
    <div style="margin-top: 20px; text-align: center;">
        <svg width="64" height="80" viewBox="0 0 64 80" xmlns="http://www.w3.org/2000/svg" style="margin: 0 auto;">
            <ellipse cx="32" cy="14" rx="10" ry="12" fill="none" stroke="#d4af37" stroke-width="1.5"/>
            <line x1="32" y1="26" x2="32" y2="44" stroke="#d4af37" stroke-width="1.5"/>
            <line x1="32" y1="44" x2="18" y2="68" stroke="#d4af37" stroke-width="1.5"/>
            <line x1="32" y1="44" x2="46" y2="68" stroke="#d4af37" stroke-width="1.5"/>
            <line x1="32" y1="34" x2="16" y2="38" stroke="#d4af37" stroke-width="1.5"/>
            <line x1="32" y1="34" x2="48" y2="38" stroke="#d4af37" stroke-width="1.5"/>
        </svg>
        <div class="humanoid-bubble shimmer-gold">I need energy to thrive.</div>
    </div>
    """, unsafe_allow_html=True)

with col_map:
    st.markdown(
        '<h2 class="shimmer-gold">NATIONAL VELOCITY FALCON CLOUD (NVFC)</h2>',
        unsafe_allow_html=True,
    )
    components.html(
        f'<div style="background:#000033; padding:0; margin:0;">{map_svg}</div>',
        height=500,
    )

# Industrial Gallery: NGECC cards
st.markdown('<p class="shimmer-gold" style="font-size: 1rem; margin: 1rem 0 0.5rem;">Industrial Gallery</p>', unsafe_allow_html=True)
gal1, gal2, gal3 = st.columns(3)
with gal1:
    st.markdown("""
    <div class="gallery-card">
        <div class="label">NGECC Urea Fertilizer</div>
        <div style="color: #b8c4ce; font-size: 0.8rem;">Sovereign feedstock</div>
    </div>
    """, unsafe_allow_html=True)
with gal2:
    st.markdown("""
    <div class="gallery-card">
        <div class="label">Activated Carbon</div>
        <div style="color: #b8c4ce; font-size: 0.8rem;">8R Stealth Paradigm</div>
    </div>
    """, unsafe_allow_html=True)
with gal3:
    st.markdown("""
    <div class="gallery-card">
        <div class="label">AI Hardware Feedstock</div>
        <div style="color: #b8c4ce; font-size: 0.8rem;">Germanium · high-value</div>
    </div>
    """, unsafe_allow_html=True)

# The Signature: shimmering gold, centered at base (Sovereign, Paradigm, Galadiman Ruwan Zazzau — spellings verified)
st.markdown("<br><br><hr style='border-color: rgba(212,175,55,0.4);'>", unsafe_allow_html=True)
st.markdown("""
<div class="signature-block" style="text-align: center; margin: 0 auto;">
    <h1 class="shimmer-gold" style="font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 0.5rem;">
        Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)
    </h1>
    <p class="shimmer-gold" style="letter-spacing: 5px; font-size: 0.9rem;">
        NVFC STRATEGIC COMMAND | GCSLC LTD/GTE
    </p>
</div>
""", unsafe_allow_html=True)
