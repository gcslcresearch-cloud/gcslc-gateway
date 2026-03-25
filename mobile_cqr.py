import html
from datetime import datetime, timedelta

import pytz
import streamlit as st


PAGE_TITLE = "Renewed Hope Grassroots Initiatives (RHGI) - 15/15 Sovereign Mirror"
FONT_LINK = "https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap"

DEEP_PRISM_NAVY = "#000033"
YELLOW_GOLD = "#D4AF37"
STARK_WHITE = "#ffffff"


def _format_countdown_wat(now: datetime, target_wat: datetime) -> str:
    """Days:Hrs:Min:Sec (all in WAT)."""
    if now >= target_wat:
        return "0:00:00:00"
    delta = target_wat - now
    days = delta.days
    seconds = delta.seconds
    hrs = seconds // 3600
    seconds = seconds % 3600
    mins = seconds // 60
    secs = seconds % 60
    return f"{days}:{hrs:02d}:{mins:02d}:{secs:02d}"


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
        font-size: 1.05rem;
        color: var(--white);
        text-align: center;
        margin-top: 6px;
      }}
      .cqr-countdown b {{
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
      }}
      .cqr-meta {{
        color: var(--white);
        opacity: 0.95;
        font-size: 0.95rem;
        margin-bottom: 12px;
        line-height: 1.4;
      }}

      /* Buttons: visual discipline (no unsafe tones) */
      .cqr-card button {{
        border-radius: 12px !important;
        font-family: 'Goldman', sans-serif !important;
        font-weight: 800 !important;
      }}
      /* Grant: Gold border + White text */
      .cqr-card button[kind="primary"] {{
        background: transparent !important;
        color: var(--white) !important;
        border: 1px solid rgba(212,175,55,0.75) !important;
        box-shadow: none !important;
      }}

      /* Deny: White border + White text */
      .cqr-card button[kind="secondary"] {{
        background: transparent !important;
        color: var(--white) !important;
        border: 1px solid rgba(255,255,255,0.8) !important;
        box-shadow: none !important;
      }}

      /* Remove any accidental danger tint (extra hardening) */
      .cqr-card button {{
        --btn-danger: rgba(0,0,0,0);
      }}
    </style>
    <div class="cqr-watermark" aria-hidden="true"><span>GCSLC</span></div>
    <div class="cqr-topbar">
      <div class="cqr-toprow">
        <div class="cqr-topitem"><b>Mirror Integrity</b>: 100%</div>
        <div class="cqr-topitem"><b>Current Sessions</b>: 4</div>
      </div>
      <div class="cqr-countdown">
        Election Countdown: <b>{html.escape(_countdown)}</b>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown("<div class='cqr-grid'>", unsafe_allow_html=True)

pending = [r for r in st.session_state.mobile_cqr_requests if r.get("status") == "PENDING"]

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

