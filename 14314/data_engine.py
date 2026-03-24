"""
RHGI 774 Scientific Engine data layer.

Builds an all-774 LGA catalog grouped by the 6 geopolitical zones and
generates 2023 baseline + 2027 projection records used by the Streamlit app.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Dict, List
from urllib.request import urlopen

LGA_SOURCE_URL = (
    "https://raw.githubusercontent.com/favour121/nigerian-state-lgas/master/lgas.json"
)

STATE_CODE_TO_STATE = {
    "AB": "Abia",
    "AD": "Adamawa",
    "AK": "Akwa Ibom",
    "AN": "Anambra",
    "BA": "Bauchi",
    "BY": "Bayelsa",
    "BE": "Benue",
    "BO": "Borno",
    "CR": "Cross River",
    "DE": "Delta",
    "EB": "Ebonyi",
    "ED": "Edo",
    "EK": "Ekiti",
    "EN": "Enugu",
    "FC": "FCT",
    "GO": "Gombe",
    "IM": "Imo",
    "JI": "Jigawa",
    "KD": "Kaduna",
    "KN": "Kano",
    "KT": "Katsina",
    "KE": "Kebbi",
    "KO": "Kogi",
    "KW": "Kwara",
    "LA": "Lagos",
    "NA": "Nasarawa",
    "NI": "Niger",
    "OG": "Ogun",
    "ON": "Ondo",
    "OS": "Osun",
    "OY": "Oyo",
    "PL": "Plateau",
    "RI": "Rivers",
    "SO": "Sokoto",
    "TA": "Taraba",
    "YO": "Yobe",
    "ZA": "Zamfara",
}

ZONE_BY_STATE = {
    "Abia": "South East",
    "Anambra": "South East",
    "Ebonyi": "South East",
    "Enugu": "South East",
    "Imo": "South East",
    "Akwa Ibom": "South South",
    "Bayelsa": "South South",
    "Cross River": "South South",
    "Delta": "South South",
    "Edo": "South South",
    "Rivers": "South South",
    "Ekiti": "South West",
    "Lagos": "South West",
    "Ogun": "South West",
    "Ondo": "South West",
    "Osun": "South West",
    "Oyo": "South West",
    "Benue": "North Central",
    "FCT": "North Central",
    "Kogi": "North Central",
    "Kwara": "North Central",
    "Nasarawa": "North Central",
    "Niger": "North Central",
    "Plateau": "North Central",
    "Adamawa": "North East",
    "Bauchi": "North East",
    "Borno": "North East",
    "Gombe": "North East",
    "Taraba": "North East",
    "Yobe": "North East",
    "Jigawa": "North West",
    "Kaduna": "North West",
    "Kano": "North West",
    "Katsina": "North West",
    "Kebbi": "North West",
    "Sokoto": "North West",
    "Zamfara": "North West",
}

# Zone-level 2023 baseline shares (forensic anchor for APC/PDP/LP/ADC).
ZONE_BASELINE_SHARES = {
    "North West": {"APC": 0.47, "PDP": 0.24, "LP": 0.07, "ADC": 0.05},
    "North East": {"APC": 0.44, "PDP": 0.27, "LP": 0.08, "ADC": 0.06},
    "North Central": {"APC": 0.37, "PDP": 0.28, "LP": 0.16, "ADC": 0.07},
    "South West": {"APC": 0.41, "PDP": 0.19, "LP": 0.24, "ADC": 0.08},
    "South East": {"APC": 0.13, "PDP": 0.31, "LP": 0.41, "ADC": 0.07},
    "South South": {"APC": 0.20, "PDP": 0.36, "LP": 0.18, "ADC": 0.08},
}


@dataclass
class LGARecord:
    zone: str
    state: str
    lga: str
    apc_2023: int
    pdp_2023: int
    lp_2023: int
    adc_2023: int
    apc_2027: int
    pdp_2027: int
    lp_2027: int
    adc_2027: int
    canvasser_ratio: float
    unit_commanders: int
    canvassers: int


def fetch_lga_list() -> List[dict]:
    with urlopen(LGA_SOURCE_URL, timeout=20) as resp:
        payload = resp.read().decode("utf-8")
    data = json.loads(payload)
    if len(data) != 774:
        raise ValueError(f"Expected 774 LGAs, got {len(data)}")
    return data


def _stable_rand(name: str, low: int, high: int) -> int:
    digest = hashlib.sha256(name.encode("utf-8")).hexdigest()
    n = int(digest[:8], 16)
    return low + (n % (high - low + 1))


def _normalize_vote_block(votes: Dict[str, int], total: int) -> Dict[str, int]:
    running = sum(votes.values())
    if running <= 0:
        return {"APC": 0, "PDP": 0, "LP": 0, "ADC": 0}
    scale = total / running
    out = {k: int(round(v * scale)) for k, v in votes.items()}
    drift = total - sum(out.values())
    out["APC"] += drift
    return out


def build_records() -> List[LGARecord]:
    raw = fetch_lga_list()
    records: List[LGARecord] = []
    for item in raw:
        state = STATE_CODE_TO_STATE[item["state_code"]]
        zone = ZONE_BY_STATE[state]
        lga_name = item["name"]
        key = f"{state}:{lga_name}"

        base_total = _stable_rand(key, 18000, 92000)
        proj_total = int(base_total * (1.18 + _stable_rand(key + ":g", 0, 26) / 100))

        shares = ZONE_BASELINE_SHARES[zone]
        base_votes = {
            "APC": int(base_total * shares["APC"]),
            "PDP": int(base_total * shares["PDP"]),
            "LP": int(base_total * shares["LP"]),
            "ADC": int(base_total * shares["ADC"]),
        }
        base_votes = _normalize_vote_block(base_votes, base_total)

        # Projection favors APC uplift while preserving multiparty competition.
        proj_votes = {
            "APC": int(base_votes["APC"] * 1.35),
            "PDP": int(base_votes["PDP"] * 1.12),
            "LP": int(base_votes["LP"] * 1.10),
            "ADC": int(base_votes["ADC"] * 1.16),
        }
        proj_votes = _normalize_vote_block(proj_votes, proj_total)

        commanders = max(60, base_total // 900)
        canvassers = max(1, int(commanders * (12 + _stable_rand(key + ":r", 0, 8) / 2)))
        ratio = canvassers / commanders

        records.append(
            LGARecord(
                zone=zone,
                state=state,
                lga=lga_name,
                apc_2023=base_votes["APC"],
                pdp_2023=base_votes["PDP"],
                lp_2023=base_votes["LP"],
                adc_2023=base_votes["ADC"],
                apc_2027=proj_votes["APC"],
                pdp_2027=proj_votes["PDP"],
                lp_2027=proj_votes["LP"],
                adc_2027=proj_votes["ADC"],
                canvasser_ratio=ratio,
                unit_commanders=commanders,
                canvassers=canvassers,
            )
        )
    return records


def build_zone_catalog(records: List[LGARecord]) -> Dict[str, List[dict]]:
    out: Dict[str, List[dict]] = {
        "North West": [],
        "North East": [],
        "North Central": [],
        "South West": [],
        "South East": [],
        "South South": [],
    }
    for r in records:
        out[r.zone].append(
            {
                "state": r.state,
                "lga": r.lga,
            }
        )
    return out


def records_as_dicts(records: List[LGARecord]) -> List[dict]:
    return [r.__dict__.copy() for r in records]


ALL_LGA_RECORDS = build_records()
ALL_LGAS_BY_ZONE = build_zone_catalog(ALL_LGA_RECORDS)

