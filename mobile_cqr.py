import html
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
import pytz
import streamlit as st
import streamlit.components.v1 as components


PAGE_TITLE = "RHGI - DG Command Terminal"
FONT_LINK = "https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap"

DEEP_PRISM_NAVY = "#000033"
YELLOW_GOLD = "#D4AF37"
STARK_WHITE = "#ffffff"


def _format_countdown_wat(now: datetime, target_wat: datetime) -> str:
    """Months : Days : Hours : Minutes : Seconds (WAT) until February 2027 anchor."""
    if now >= target_wat:
        return "[0] : [0] : [00] : [00] : [00]"
    rd = relativedelta(target_wat, now)
    months = rd.years * 12 + rd.months
    days = rd.days
    h = rd.hours
    m = rd.minutes
    s = rd.seconds
    return f"[{months}] : [{days}] : [{h:02d}] : [{m:02d}] : [{s:02d}]"


def _make_mock_requests() -> list[dict]:
    return [
        {
            "id": "NW-LEAD",
            "role": "Regional Lead - NW",
            "requested_by": "Stealth Liaison Node",
            "grants_for_minutes": 30,
            "status": "PENDING",
        },
        {
            "id": "LOG-ANALYST",
            "role": "Logistics Analyst",
            "requested_by": "Corridor Desk",
            "grants_for_minutes": 30,
            "status": "PENDING",
        },
        {
            "id": "CANVASS-COORD",
            "role": "Canvasser Coordinator",
            "requested_by": "Ward Geometry Office",
            "grants_for_minutes": 30,
            "status": "PENDING",
        },
    ]


st.set_page_config(
    page_title=PAGE_TITLE,
    layout="centered",
    initial_sidebar_state="collapsed",
)


_TZ = pytz.timezone("Africa/Lagos")
# Election anchor for countdown header (matches the rest of the dashboard).
ELECTION_DATETIME_WAT = _TZ.localize(datetime(2027, 2, 25, 8, 0, 0))


if "mobile_cqr_requests" not in st.session_state:
    st.session_state.mobile_cqr_requests = _make_mock_requests()
if "mobile_cqr_audit" not in st.session_state:
    st.session_state.mobile_cqr_audit = []


_countdown = _format_countdown_wat(datetime.now(_TZ), ELECTION_DATETIME_WAT)

# Inject fonts + strict navy/gold/white styling and watermark.
st.markdown(
    f"""
    <link href="{FONT_LINK}" rel="stylesheet">
    <style>
      :root {{
        --navy: {DEEP_PRISM_NAVY};
        --gold: {YELLOW_GOLD};
        --white: {STARK_WHITE};
      }}
      html, body {{
        background: var(--navy) !important;
        color: var(--white) !important;
        font-family: 'Goldman', sans-serif !important;
      }}

      /* Streamlit chrome */
      [data-testid="stSidebar"] {{
        background: var(--navy) !important;
        color: var(--white) !important;
      }}
      [data-testid="stSidebar"] *, [data-testid="stApp"] * {{
        font-family: 'Goldman', sans-serif !important;
      }}

      /* Fixed background watermark (anti screen-capture feel) */
      .cqr-watermark {{
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0.15;
      }}
      .cqr-watermark span {{
        font-size: clamp(3rem, 10vw, 7rem);
        letter-spacing: 0.18em;
        color: var(--white);
        text-shadow: 0 0 18px rgba(212,175,55,0.25);
      }}

      /* Executive status bar */
      .cqr-topbar {{
        position: sticky;
        top: 0;
        z-index: 5;
        background: rgba(0,0,51,0.92);
        border: 1px solid rgba(212,175,55,0.35);
        border-radius: 14px;
        padding: 10px 14px;
        margin: 10px 0 16px 0;
      }}
      .cqr-toprow {{
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
      }}
      .cqr-topitem {{
        font-size: 0.98rem;
        color: var(--white);
        letter-spacing: 0.02em;
      }}
      .cqr-topitem b {{
        color: var(--gold);
        font-weight: 800;
      }}
      .cqr-countdown {{
        font-family: 'Goldman', sans-serif !important;
        font-size: 1.05rem;
        color: var(--white);
        text-align: center;
        margin-top: 6px;
      }}
      .cqr-countdown-label {{
        color: var(--white);
        font-weight: 700;
        margin-bottom: 4px;
      }}
      .cqr-countdown-units {{
        font-size: 0.82rem;
        color: var(--gold);
        opacity: 0.95;
        margin-bottom: 6px;
        letter-spacing: 0.02em;
      }}
      .cqr-countdown b {{
        color: var(--gold);
        font-weight: 900;
        font-family: 'Goldman', sans-serif !important;
        font-size: 1.12rem;
        letter-spacing: 0.06em;
      }}

      /* Identity + budget block (above executive bar) */
      .cqr-brand {{
        position: relative;
        z-index: 1;
        text-align: center;
        margin: 14px 0 6px 0;
        padding: 0 14px;
      }}
      .cqr-brand-title {{
        color: var(--gold);
        font-weight: 900;
        letter-spacing: 0.03em;
        font-size: clamp(1.05rem, 3.4vw, 1.35rem);
        margin: 0;
        text-shadow: 0 0 14px rgba(212,175,55,0.25);
      }}
      .cqr-creed-block {{
        color: var(--gold);
        font-weight: 700;
        margin: 8px 0 0 0;
        line-height: 1.45;
        font-size: 1.02rem;
      }}
      .cqr-mobile-metrics {{
        margin-top: 10px;
        display: flex;
        flex-direction: column;
        gap: 6px;
        align-items: center;
        justify-content: center;
      }}
      .cqr-mobile-metric {{
        color: var(--white);
        font-weight: 800;
        letter-spacing: 0.01em;
      }}
      .cqr-mobile-metric b {{
        color: var(--gold);
        font-weight: 900;
      }}

      /* Prism-framed cards for pending requests */
      .cqr-grid {{
        position: relative;
        z-index: 1;
        width: min(720px, 100%);
        margin: 0 auto;
        display: grid;
        gap: 14px;
      }}
      .cqr-card {{
        background: rgba(0,0,51,0.35);
        border: 1px solid rgba(212,175,55,0.45);
        border-radius: 16px;
        padding: 14px 14px;
        box-shadow: 0 0 18px rgba(212,175,55,0.12);
      }}
      .cqr-card h3 {{
        margin: 0 0 6px 0;
        font-size: 1.1rem;
        color: var(--gold);
        text-shadow: 0 0 12px rgba(212,175,55,0.2);
        font-family: 'Goldman', sans-serif !important;
      }}
      .cqr-meta {{
        color: var(--white);
        opacity: 0.95;
        font-size: 0.95rem;
        margin-bottom: 12px;
        line-height: 1.4;
      }}
      .cqr-extra {{
        color: var(--white);
        opacity: 0.98;
        font-size: 0.98rem;
        margin: 0 0 10px 0;
        text-align: left;
        font-weight: 700;
      }}

      /* Buttons: visual discipline (no unsafe tones) */
      .cqr-card button {{
        border-radius: 12px !important;
        font-family: 'Goldman', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important; /* +15% for one-tap mobile */
        padding: 0.75rem 0.95rem !important;
      }}
      /* Grant: Yellow Gold #D4AF37 — no Streamlit red / danger bleed */
      .cqr-card button[kind="primary"] {{
        background: #D4AF37 !important;
        background-image: none !important;
        color: #000033 !important;
        border: 2px solid #D4AF37 !important;
        box-shadow: none !important;
        animation: cqrGrantGoldPulse 1.85s ease-in-out infinite !important;
      }}
      .cqr-card button[kind="primary"]:hover {{
        background: #D4AF37 !important;
        background-image: none !important;
        color: #000033 !important;
        border-color: #D4AF37 !important;
      }}
      @keyframes cqrGrantGoldPulse {{
        0%, 100% {{ box-shadow: 0 0 10px rgba(212,175,55,0.45); transform: scale(1); }}
        50% {{ box-shadow: 0 0 26px rgba(212,175,55,0.9); transform: scale(1.03); }}
      }}

      /* Deny: Stark white outline, transparent fill */
      .cqr-card button[kind="secondary"] {{
        background: transparent !important;
        background-image: none !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        box-shadow: none !important;
      }}
      .cqr-card button[kind="secondary"]:hover {{
        background: transparent !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
      }}

      /* Remove any accidental danger tint (extra hardening) */
      .cqr-card button {{
        --btn-danger: rgba(0,0,0,0);
      }}

      /* CIEN-Verify Swat Widget — mirrors 14314/app.py (S24 Ultra primary) */
      .cqr-swat-primary {{
        position: relative;
        z-index: 1;
        width: 100%;
        max-width: min(520px, 100%);
        margin: 0 auto 18px auto;
      }}
      @keyframes rhgiSwatBorderPulse {{
        0%, 100% {{ box-shadow: 0 0 16px rgba(212,175,55,0.45), inset 0 0 22px rgba(212,175,55,0.08); }}
        50% {{ box-shadow: 0 0 38px rgba(212,175,55,0.95), inset 0 0 32px rgba(255,248,220,0.12); }}
      }}
      @keyframes rhgiSwatFillFlow {{
        0%, 100% {{ filter: brightness(1.02); transform: scaleY(1); }}
        50% {{ filter: brightness(1.18); transform: scaleY(1.02); }}
      }}
      @keyframes rhgiSwatShimmer {{
        0% {{ background-position: 0% 80%; }}
        100% {{ background-position: 0% 20%; }}
      }}
      .rhgi-swat-shell {{
        font-family: 'Goldman', sans-serif !important;
        border: 2px solid #D4AF37;
        border-radius: 22px;
        padding: 22px 20px 26px 20px;
        margin: 0;
        background: rgba(0,0,51,0.72);
        animation: rhgiSwatBorderPulse 2.6s ease-in-out infinite;
        position: relative;
        z-index: 2;
      }}
      .rhgi-swat-title {{
        color: #D4AF37 !important;
        font-weight: 800;
        font-size: clamp(0.95rem, 2.2vw, 1.12rem);
        text-align: center;
        letter-spacing: 0.06em;
        margin: 0 0 6px 0;
        text-shadow: 0 0 14px rgba(212,175,55,0.45);
      }}
      .rhgi-swat-sub {{
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.92rem;
        text-align: center;
        margin: 0 0 10px 0;
        opacity: 0.95;
      }}
      .rhgi-swat-target {{
        color: #D4AF37 !important;
        font-weight: 900;
        font-size: clamp(1.85rem, 5vw, 2.45rem);
        text-align: center;
        letter-spacing: 0.04em;
        text-shadow: 0 0 22px rgba(212,175,55,0.65), 0 0 44px rgba(212,175,55,0.25);
        margin: 0 0 14px 0;
        line-height: 1.1;
      }}
      .rhgi-swat-cylinder-wrap {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        margin: 8px 0 16px 0;
      }}
      .rhgi-swat-cylinder {{
        position: relative;
        width: 112px;
        height: 260px;
        border-radius: 56px;
        border: 2px solid rgba(212,175,55,0.75);
        background: linear-gradient(90deg,
          rgba(0,0,51,0.55) 0%,
          rgba(212,175,55,0.12) 45%,
          rgba(255,250,220,0.08) 50%,
          rgba(212,175,55,0.12) 55%,
          rgba(0,0,51,0.55) 100%);
        box-shadow:
          inset 0 0 36px rgba(255,255,255,0.12),
          inset 0 -20px 50px rgba(212,175,55,0.15),
          0 0 28px rgba(212,175,55,0.35);
        overflow: hidden;
      }}
      .rhgi-swat-fill {{
        position: absolute;
        left: 4px;
        right: 4px;
        bottom: 4px;
        height: 83.7%;
        border-radius: 0 0 48px 48px;
        background: linear-gradient(180deg,
          rgba(255,248,210,0.95) 0%,
          rgba(212,175,55,0.88) 35%,
          rgba(212,175,55,0.75) 70%,
          rgba(180,140,45,0.85) 100%);
        background-size: 100% 200%;
        animation: rhgiSwatFillFlow 2.4s ease-in-out infinite, rhgiSwatShimmer 3.2s linear infinite;
        box-shadow: inset 0 0 24px rgba(255,255,255,0.35), 0 0 22px rgba(212,175,55,0.55);
      }}
      .rhgi-swat-current {{
        color: #ffffff !important;
        font-weight: 800;
        font-size: 1.05rem;
        letter-spacing: 0.04em;
      }}
      .rhgi-swat-status {{
        color: #ffffff !important;
        font-size: clamp(0.78rem, 1.8vw, 0.9rem);
        font-weight: 600;
        line-height: 1.55;
        text-align: center;
        margin: 0 0 16px 0;
        padding: 10px 12px;
        border: 1px solid rgba(212,175,55,0.35);
        border-radius: 12px;
        background: rgba(0,0,51,0.5);
      }}
      .rhgi-swat-status .rhgi-swat-gold {{ color: #D4AF37 !important; font-weight: 800; }}
      .rhgi-swat-icons {{
        display: flex;
        justify-content: center;
        gap: 14px;
        flex-wrap: wrap;
        margin-top: 4px;
      }}
      .rhgi-swat-icon {{
        flex: 1 1 90px;
        max-width: 140px;
        text-align: center;
        color: #D4AF37 !important;
        font-weight: 800;
        font-size: 0.82rem;
        letter-spacing: 0.04em;
        padding: 10px 8px;
        border: 1px solid rgba(212,175,55,0.45);
        border-radius: 12px;
        background: rgba(0,0,51,0.45);
      }}
      .rhgi-swat-icon small {{
        display: block;
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.72rem;
        margin-top: 4px;
        opacity: 0.92;
      }}
    </style>
    <div class="cqr-watermark" aria-hidden="true"><span>GCSLC</span></div>
    <div class="cqr-brand">
      <h1 class="cqr-brand-title">{html.escape(PAGE_TITLE)}</h1>
      <div class="cqr-creed-block">Securing the 20.7M Mandate Anchor.</div>
      <div class="cqr-mobile-metrics">
        <div class="cqr-mobile-metric"><b>Global Logistics Fuel:</b> ₦108,961,000,000</div>
        <div class="cqr-mobile-metric"><b>Efficiency Gauge:</b> 1:15 Canvasser Ratio</div>
      </div>
    </div>
    <div class="cqr-topbar">
      <div class="cqr-toprow">
        <div class="cqr-topitem"><b>Mirror Integrity</b>: 100%</div>
        <div class="cqr-topitem"><b>Current Sessions</b>: 4</div>
      </div>
      <div class="cqr-countdown">
        <div class="cqr-countdown-label">Election Countdown → Feb 2027</div>
        <div class="cqr-countdown-units">[Months] : [Days] : [Hours] : [Minutes] : [Seconds]</div>
        <b>{html.escape(_countdown)}</b>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

_SWAT_TARGET = 21_750
_SWAT_CURRENT = 18_200
_SWAT_PCT = 83.7
st.markdown(
    f"""
    <div class="cqr-swat-primary">
      <div class="rhgi-swat-shell">
        <div class="rhgi-swat-title">LGA ACTIVATION METRIC (15/15 TARGET)</div>
        <div class="rhgi-swat-sub">LGA: KANO - NASARAWA</div>
        <div class="rhgi-swat-target">{_SWAT_TARGET:,}</div>
        <div class="rhgi-swat-cylinder-wrap">
          <div class="rhgi-swat-cylinder">
            <div class="rhgi-swat-fill"></div>
          </div>
          <div class="rhgi-swat-current">Current fill: {_SWAT_CURRENT:,}</div>
        </div>
        <div class="rhgi-swat-status">
          CURRENT STATE: <span class="rhgi-swat-gold">ACTIVATING</span> &gt;
          VELOCITY GAUGE: <span class="rhgi-swat-gold">{_SWAT_PCT}% [PULSING]</span> &gt;
          SWAT THRESHOLD: <span class="rhgi-swat-gold">{_SWAT_TARGET:,} [PENDING]</span>
        </div>
        <div class="rhgi-swat-icons">
          <div class="rhgi-swat-icon">CIEN-C<small>GeoCanvasser</small></div>
          <div class="rhgi-swat-icon">CIEN-I<small>Data Integrity</small></div>
          <div class="rhgi-swat-icon">CIEN-E<small>Logistics Fuel</small></div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='cqr-grid'>", unsafe_allow_html=True)

pending = [r for r in st.session_state.mobile_cqr_requests if r.get("status") == "PENDING"]

pending_count = len(pending)
_prev_pending = st.session_state.get("mobile_prev_pending_count", 0)
if pending_count > _prev_pending:
    # WebAudio chime — resume() helps Chrome/Samsung Internet (S24 Ultra) after autoplay policy.
    components.html(
        """
        <script>
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          const ctx = new AudioContext();
          function tone(freq, t0, t1, gainVal) {
            const o = ctx.createOscillator();
            const g = ctx.createGain();
            o.type = 'sine';
            o.frequency.setValueAtTime(freq, t0);
            g.gain.setValueAtTime(0.0001, t0);
            g.gain.exponentialRampToValueAtTime(gainVal, t0 + 0.01);
            g.gain.exponentialRampToValueAtTime(0.0001, t1);
            o.connect(g); g.connect(ctx.destination);
            o.start(t0); o.stop(t1);
          }
          function playChime() {
            const now = ctx.currentTime;
            tone(880, now, now+0.12, 0.22);
            tone(1174, now+0.14, now+0.26, 0.18);
            setTimeout(() => { try { ctx.close(); } catch(e){} }, 400);
          }
          if (ctx.state === 'suspended') {
            ctx.resume().then(playChime).catch(playChime);
          } else {
            playChime();
          }
        </script>
        """,
        height=0,
    )
st.session_state.mobile_prev_pending_count = pending_count

if not pending:
    st.markdown(
        "<div class='cqr-card'><h3>All Requests Cleared</h3><div class='cqr-meta'>No pending CQR actions remain.</div></div>",
        unsafe_allow_html=True,
    )
else:
    for req in pending:
        _id = req["id"]
        _role = req["role"]
        _by = req["requested_by"]
        _grant_for = int(req["grants_for_minutes"])

        st.markdown("<div class='cqr-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{html.escape(_role)}</h3>", unsafe_allow_html=True)
        st.markdown(
            "<div class='cqr-meta'>"
            f"Requested by: <span style='color: var(--white); font-weight:700;'>{html.escape(_by)}</span><br>"
            f"Status: <span style='color: var(--gold); font-weight:900;'>{html.escape(req['status'])}</span>"
            "</div>",
            unsafe_allow_html=True,
        )

        if _role == "Logistics Analyst":
            st.markdown(
                "<div class='cqr-extra'>Requesting NW Corridor Drill-down.</div>",
                unsafe_allow_html=True,
            )
        elif _role == "Canvasser Coordinator":
            st.markdown(
                "<div class='cqr-extra'>Requesting 15/15 Efficiency Gauge access.</div>",
                unsafe_allow_html=True,
            )

        # Buttons must be driven by `key=f'grant_{id}'` and `key=f'deny_{id}'`
        c1, c2 = st.columns(2)
        with c1:
            if st.button(
                f"Grant {_grant_for}m",
                key=f"grant_{_id}",
                use_container_width=True,
                help=f"Grant {_grant_for} minutes access for: {_role}",
                type="primary",
            ):
                st.session_state.mobile_cqr_requests = [
                    r for r in st.session_state.mobile_cqr_requests if r["id"] != _id
                ]
                st.session_state.mobile_cqr_audit.append(
                    {"id": _id, "action": "GRANTED", "at": datetime.now(_TZ).isoformat()}
                )
                st.rerun()
        with c2:
            if st.button(
                "Deny",
                key=f"deny_{_id}",
                use_container_width=True,
                help=f"Deny access request for: {_role}",
                type="secondary",
            ):
                st.session_state.mobile_cqr_requests = [
                    r for r in st.session_state.mobile_cqr_requests if r["id"] != _id
                ]
                st.session_state.mobile_cqr_audit.append(
                    {"id": _id, "action": "DENIED", "at": datetime.now(_TZ).isoformat()}
                )
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# Optional minimal audit trail (still mobile-friendly).
if st.session_state.mobile_cqr_audit:
    st.markdown("### Executive Audit")
    for row in st.session_state.mobile_cqr_audit[-5:]:
        st.caption(f"{row['action']} — {row['id']} @ {row['at']}")

