"""
Nigeria fractional viewport for parent-window eagle patrol — MUST stay aligned with app.py
_NG_FRAC_* / _NG_PAD_* / _NG_LAT_* / _NG_LON_* (Sovereign geofence).
"""

from __future__ import annotations

# Mirror app.py sovereign canvas (do not drift from app.py without updating both).
_NG_FRAC_X0 = 0.22
_NG_FRAC_X1 = 0.76
_NG_FRAC_Y0 = 0.24
_NG_FRAC_Y1 = 0.685
_NG_PAD_X = 0.068
_NG_PAD_Y = 0.058
_NG_LAT_MIN = 4.2
_NG_LAT_MAX = 13.95
_NG_LON_MIN = 2.65
_NG_LON_MAX = 14.68


def clamp_nigeria_fraction(pt: dict[str, float]) -> dict[str, float]:
    x = max(
        _NG_FRAC_X0 + _NG_PAD_X,
        min(_NG_FRAC_X1 - _NG_PAD_X, float(pt["x"])),
    )
    y = max(
        _NG_FRAC_Y0 + _NG_PAD_Y,
        min(_NG_FRAC_Y1 - _NG_PAD_Y, float(pt["y"])),
    )
    return {"x": round(x, 4), "y": round(y, 4)}


def latlon_to_nigeria_fraction(lat: float, lon: float) -> dict[str, float]:
    la = float(lat)
    lo = float(lon)
    x = (lo - _NG_LON_MIN) / (_NG_LON_MAX - _NG_LON_MIN)
    y = 1.0 - (la - _NG_LAT_MIN) / (_NG_LAT_MAX - _NG_LAT_MIN)
    return clamp_nigeria_fraction({"x": x, "y": y})
