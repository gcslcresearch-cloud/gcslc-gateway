"""
NVFC Sovereign Pulse — D7 Re-engineer (zero st.image / components.html).
Run: streamlit run nvfc_sovereign_pulse.py
"""
import streamlit as st
import sys

# Zero-error guard (spelling: Sovereign, Galadiman Ruwan Zazzau)
SOVEREIGN = "Sovereign"
PARADIGM = "Paradigm"
SIGNATURE_TITLE = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)"
DETERMINANTS = ("Refinement", "Reset", "Research", "Restructure", "Resuscitate", "Revitalize", "Re-engineer", "Retain")
AUDIO_ENABLED = False

# 13 coal states (official names)
COAL_STATES = ("Enugu", "Kogi", "Benue", "Nasarawa", "Gombe", "Adamawa", "Delta", "Edo", "Ondo", "Bauchi", "Anambra", "Ebonyi", "Abia")

# Dashboard Configuration
st.set_page_config(
    page_title=f"NVFC {SOVEREIGN} Pulse",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# First rendered: Sovereign Comparison Widget (UAE vs. Nigeria) via st.sidebar.info
st.sidebar.markdown("**8R Stealth Paradigm Convergence**")
st.sidebar.markdown("---")
st.sidebar.info("""
**🌍 GLOBAL STRATEGIC CONTEXT**

**UAE (G42/Microsoft):** $15.2B Investment in AI Cloud.

**NIGERIA (NGECC):** 2 Billion MT Coal Ground-Base.

*Strategic Gap:* The NVFC provides the energy feedstock (D1–D8) that global clouds need to thrive.
""")


def _inject_css():
    """Minimal CSS: navy background, no external fonts or images."""
    st.markdown("""
<style>
.stApp { background-color: #000033; }
.stMarkdown p, .stMarkdown li, .stMarkdown span { color: #e8eef4 !important; }
.gallery-card { border: 1px solid rgba(212,175,55,0.5); background: rgba(0,0,51,0.8); border-radius: 8px; padding: 12px 16px; }
.gallery-card .label { color: #f9f295; font-weight: 700; }
</style>
""", unsafe_allow_html=True)


def _coal_states_markdown():
    """13 Coal States + Falcon as simple st.markdown with emoji (no SVG, no components.html)."""
    states_line = " · ".join(f"📍 {s}" for s in COAL_STATES)
    return f"""
🦅 **Falcon** — NVFC over 13 coal states

**13 Coal States:**  
{states_line}

🏛️ Data Centers: Nasarawa · Kogi
"""


def main():
    """Run dashboard with try-except per section so one failing visual does not crash the session."""
    try:
        _inject_css()
    except Exception as e:
        print(f"[NVFC] CSS inject failed: {e}", file=sys.stderr)
        st.markdown("<style>.stApp { background-color: #000033; }</style>", unsafe_allow_html=True)

    try:
        brainbox_text = " · ".join(f"D{i+1} {d}" for i, d in enumerate(DETERMINANTS))
        st.caption(f"*{brainbox_text}*")
    except Exception as e:
        print(f"[NVFC] Brainbox failed: {e}", file=sys.stderr)

    if AUDIO_ENABLED:
        try:
            st.markdown("""<audio id="pulseHumMain" loop preload="auto" style="position:absolute;width:0;height:0;opacity:0;"><source src="40hz_pulse_hum.mp3" type="audio/mpeg"></audio>""", unsafe_allow_html=True)
        except Exception:
            pass

    try:
        st.markdown('<h1 class="shimmer-gold" style="text-align: center;">GCSLC STRATEGIC COMMAND</h1>', unsafe_allow_html=True)
    except Exception as e:
        print(f"[NVFC] Header failed: {e}", file=sys.stderr)
        st.title("GCSLC STRATEGIC COMMAND")

    col_side, col_map = st.columns([1, 4])

    try:
        with col_side:
            st.markdown("**8R BRAINBOX DETERMINANTS**")
            for i, d in enumerate(DETERMINANTS):
                st.markdown(f"• D{i+1} {d}")
            st.markdown("---")
            st.markdown("**STATUS ARCHIVE**")
            st.markdown("● ACTIVE")
            st.markdown("● RESERVE")
            st.markdown("---")
            st.markdown("👤 **Humanoid**")
            st.markdown("*I need energy to thrive.*")
    except Exception as e:
        print(f"[NVFC] Sidebar column failed: {e}", file=sys.stderr)
        with col_side:
            st.caption("8R BRAINBOX DETERMINANTS")
            for i, d in enumerate(DETERMINANTS):
                st.caption(f"D{i+1} {d}")

    try:
        with col_map:
            st.markdown("### 🦅 NATIONAL VELOCITY FALCON CLOUD (NVFC)")
            st.markdown(_coal_states_markdown())
    except Exception as e:
        print(f"[NVFC] Map section failed: {e}", file=sys.stderr)
        with col_map:
            st.markdown("### NATIONAL VELOCITY FALCON CLOUD (NVFC)")
            st.markdown("📍 13 Coal States · 🦅 Falcon")

    try:
        st.markdown('<p class="shimmer-gold" style="font-size:1rem; margin:1rem 0 0.5rem;">Industrial Gallery</p>', unsafe_allow_html=True)
        gal1, gal2, gal3 = st.columns(3)
        with gal1:
            st.markdown(f'<div class="gallery-card"><div class="label">NGECC Urea Fertilizer</div><div style="color:#b8c4ce; font-size:0.8rem;">{SOVEREIGN} feedstock</div></div>', unsafe_allow_html=True)
        with gal2:
            st.markdown(f'<div class="gallery-card"><div class="label">Activated Carbon</div><div style="color:#b8c4ce; font-size:0.8rem;">8R Stealth {PARADIGM}</div></div>', unsafe_allow_html=True)
        with gal3:
            st.markdown('<div class="gallery-card"><div class="label">AI Hardware Feedstock</div><div style="color:#b8c4ce; font-size:0.8rem;">Germanium · high-value</div></div>', unsafe_allow_html=True)
    except Exception as e:
        print(f"[NVFC] Gallery failed: {e}", file=sys.stderr)

    try:
        st.markdown("---")
        # Hard-coded signature: standard st.header (no custom HTML/CSS)
        st.header(SIGNATURE_TITLE)
        st.caption("NVFC STRATEGIC COMMAND | GCSLC LTD/GTE")
    except Exception as e:
        print(f"[NVFC] Signature failed: {e}", file=sys.stderr)
        st.caption(SIGNATURE_TITLE)


main()
