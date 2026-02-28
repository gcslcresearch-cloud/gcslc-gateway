"""
National Wealth Cloud for Nigeria: Coal & Diamond (NWC/C&D)
37-Node Geopolitical Grid — 36 States + FCT with Local Government Areas (LGAs).
© GCSLC. Proprietary.
"""

from typing import Dict, List, Union

# Region → (state, LGA count) per user spec. FCT has named area councils.
_REGION_STATE_LGAS = {
    "North West": [("Kaduna", 23), ("Kano", 44), ("Katsina", 34), ("Jigawa", 27), ("Sokoto", 23), ("Kebbi", 21), ("Zamfara", 14)],   # 186
    "North East": [("Borno", 27), ("Yobe", 17), ("Bauchi", 20), ("Gombe", 11), ("Adamawa", 21), ("Taraba", 16)],  # 112
    "North Central": [("Kogi", 21), ("Niger", 25), ("Kwara", 16), ("Benue", 23), ("Plateau", 17), ("Nasarawa", 13)],  # 121
    "South South": [("Rivers", 23), ("Cross River", 18), ("Delta", 25), ("Edo", 18), ("Akwa Ibom", 31), ("Bayelsa", 8)],  # 123
    "South East": [("Anambra", 21), ("Enugu", 17), ("Imo", 27), ("Abia", 17), ("Ebonyi", 13)],  # 95
    "South West": [("Lagos", 20), ("Oyo", 33), ("Osun", 30), ("Ondo", 18), ("Ogun", 20), ("Ekiti", 16)],  # 137
    "FCT": None,  # special: 6 area councils by name
}

FCT_LGA_NAMES = ["Abuja Municipal", "Bwari", "Kuje", "Gwagwalada", "Abaji", "Kwali"]

# Build state → region
STATE_REGION: Dict[str, str] = {}
for region, pairs in _REGION_STATE_LGAS.items():
    if pairs:
        for state, _ in pairs:
            STATE_REGION[state] = region
STATE_REGION["FCT"] = "FCT"

# Build state → LGA count or list of LGA names (for FCT)
STATE_LGA_COUNT: Dict[str, int] = {}
STATE_LGA_NAMES: Dict[str, Union[int, List[str]]] = {}
for region, pairs in _REGION_STATE_LGAS.items():
    if pairs:
        for state, count in pairs:
            STATE_LGA_COUNT[state] = count
            STATE_LGA_NAMES[state] = [f"{state} LGA {i+1}" for i in range(count)]
STATE_LGA_COUNT["FCT"] = len(FCT_LGA_NAMES)
STATE_LGA_NAMES["FCT"] = FCT_LGA_NAMES


def get_region(state: str) -> str:
    """Return geopolitical region for a state or FCT."""
    return STATE_REGION.get(state, "")


def get_lgas(state: str) -> List[str]:
    """Return list of LGA names (or placeholder labels) for drill-down."""
    return STATE_LGA_NAMES.get(state, [])
