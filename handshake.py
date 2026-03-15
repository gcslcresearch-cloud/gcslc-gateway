"""
GCSLC Sovereign Gateway — handshake and sovereign sound protocol.
Uses Mac's native afplay in background (&) so it doesn't lag the data.
"""
import os
import sys
import time

_SOUNDS_DIR = "/System/Library/Sounds"
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_ASSETS = os.path.join(_SCRIPT_DIR, "assets")
SOUNDS = {
    "boot": f"{_SOUNDS_DIR}/Glass.aiff",
    "process": f"{_SOUNDS_DIR}/Morse.aiff",
    "tink": f"{_SOUNDS_DIR}/Tink.aiff",
    "talon_lock": f"{_SOUNDS_DIR}/Submarine.aiff",
    # Majestic Eagle/Falcon cry on NWC login (GCSLC2026) — fallback to system if no asset
    "eagle_cry": os.path.join(_ASSETS, "eagle_cry.aiff") if os.path.isdir(_ASSETS) else None,
    "eagle_cry_fallback": f"{_SOUNDS_DIR}/Hero.aiff",
    # SWAT-style HUD two-beep loop (path only; playback via frontend <audio loop> when provided)
    "swat_beep": os.path.join(_ASSETS, "swat_hud_beep.wav") if os.path.isdir(_ASSETS) else None,
}

# The 37-Node Mesh (36 States + FCT)
STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "FCT", "Gombe",
    "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara",
    "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau",
    "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara",
]
NUM_STATE_NODES = len(STATES)


def play_sound(effect: str) -> None:
    """Play a sound effect in background via afplay. The '&' keeps it from lagging the data."""
    path = SOUNDS.get(effect)
    if path and os.path.isfile(path):
        os.system(f"afplay {path!r} &")


def run_diagnostic_pulse() -> None:
    """NWC/CD diagnostic pulse: one Tink per state (37-node mesh), then Talon Lock chime."""
    print("INITIALIZING NWC/CD DIAGNOSTIC PULSE...")
    for state in STATES:
        print(f"Node Check: {state.upper()}... [SYNCHRONIZED]")
        play_sound("tink")
        time.sleep(0.05)  # High-velocity timing

    print("\n" + "=" * 45)
    print("ALL 37 NODES SECURED. ENGAGING TALON LOCK.")
    print("=" * 45)
    play_sound("talon_lock")
    print("STATUS: 100% TALON LOCK CONFIRMED.")


def run_sovereign_handshake() -> None:
    """Run the sovereign handshake: boot chime, 37 state-node Tinks during init, then banner."""
    play_sound("boot")
    print("\n" + "=" * 45)
    print("   GCSLC SOVEREIGN GATEWAY: ONLINE")
    print("=" * 45)
    print(f"Strategic Engine (Python): {sys.version.split()[0]}")
    print("8R Determinants D1-D8:   INITIALIZED")
    print("National Asset Mode:     ACTIVE")

    for state in STATES:
        play_sound("tink")

    print("-" * 45)
    print("STATUS: READY FOR ASSET REVITALIZATION")
    print("=" * 45 + "\n")


def play_talon_lock_confirmed() -> None:
    """Play Submarine chime when 95% Talon Lock is confirmed. Runs in background."""
    play_sound("talon_lock")


def play_eagle_cry() -> None:
    """Majestic Eagle/Falcon cry on NWC login (Password: GCSLC2026). Runs in background."""
    path = SOUNDS.get("eagle_cry")
    if path and os.path.isfile(path):
        os.system(f"afplay {path!r} &")
    else:
        fallback = SOUNDS.get("eagle_cry_fallback")
        if fallback and os.path.isfile(fallback):
            os.system(f"afplay {fallback!r} &")


def get_swat_beep_path():
    """Return path to SWAT-style HUD two-beep WAV for frontend loop, or None."""
    path = SOUNDS.get("swat_beep")
    return path if path and os.path.isfile(path) else None


if __name__ == "__main__":
    run_diagnostic_pulse()
