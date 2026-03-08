"""
NVFC Sovereign Pulse — Streamlit app for National Velocity Falcon Cloud command.
Run: streamlit run nvfc_sovereign_pulse.py
"""
import os
import streamlit as st

# Page Configuration for NVFC Command
st.set_page_config(page_title="NVFC Sovereign Pulse", layout="wide")

# Custom CSS for the Shimmering Signature & Headers
st.markdown("""
<style>
.shimmer-gold {
    background: linear-gradient(90deg, #d4af37, #f9f295, #ffffff, #f9f295, #d4af37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite linear;
    font-weight: bold;
}
@keyframes shimmer { to { background-position: 200% center; } }
.st-status { color: #00ff88; }
.st-reserve { color: rgba(212, 175, 55, 0.95); }
</style>
""", unsafe_allow_html=True)

# Layout: Slim States Widget (Left) and High-Velocity Map (Right)
col1, col2 = st.columns([1, 4])

with col1:
    st.markdown('<h3 class="shimmer-gold">STATUS ARCHIVE</h3>', unsafe_allow_html=True)
    st.markdown('<div class="st-status">● ACTIVE</div>', unsafe_allow_html=True)
    st.markdown('<div class="st-status">● ACTIVE</div>', unsafe_allow_html=True)
    st.markdown('<span class="shimmer-gold">● RESERVE</span>', unsafe_allow_html=True)
    for _ in range(10):
        st.markdown('<div class="st-reserve">● RESERVE</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h2 class="shimmer-gold">NATIONAL VELOCITY FALCON CLOUD</h2>', unsafe_allow_html=True)
    # High-velocity map: use falcon_map.svg or a PNG in project root; fallback placeholder
    map_paths = ["falcon_map.svg", "falcon_map.png", "path_to_your_falcon_map.svg"]
    map_path = None
    for p in map_paths:
        if os.path.isfile(p):
            map_path = p
            break
    if map_path:
        st.image(map_path, use_container_width=True)
    else:
        # Placeholder: inline Nigeria outline SVG via HTML
        st.markdown("""
        <div style="background: rgba(0,0,0,0.2); border: 1px solid rgba(212,175,55,0.3); border-radius: 8px; padding: 20px; min-height: 280px; display: flex; align-items: center; justify-content: center;">
            <svg viewBox="0 0 200 240" width="180" style="opacity: 0.6;" xmlns="http://www.w3.org/2000/svg">
                <path fill="none" stroke="#d4af37" stroke-width="1.5" d="M100 20 L160 50 L180 100 L165 160 L120 220 L80 200 L40 150 L35 90 L60 40 Z"/>
            </svg>
        </div>
        <p style="color: #888; font-size: 0.85rem;">Add <code>falcon_map.svg</code> or <code>falcon_map.png</code> to this folder to show the Falcon map.</p>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<h1 style="text-align: center;" class="shimmer-gold">Dr. Sa\'ad Jaafaru (Galadiman Ruwan Zazzau)</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="text-align: center; font-size: 0.75rem; letter-spacing: 4px; opacity: 0.9;" class="shimmer-gold">NATIONAL VELOCITY FALCON CLOUD (NVFC) COMMAND</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="text-align: center; margin-top: 1rem;"><span style="background: #006747; color: white; padding: 6px 16px; border-radius: 4px;">CAC Name Reservation Approved: Nigerian Green Energy and Chemicals Corporation</span></p>',
    unsafe_allow_html=True,
)
