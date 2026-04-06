"""
Termii bulk SMS pulse — test node first, then scale from CSV.
"""

import requests

api_key = "TLAnLkwddGzmlfEwqXDAhklvmzytWsFfKuVevKqPMYTARQjDRUXVyJNFOfUDtw"

from_id = "Galadiman_R"

SMS = (
    "300k children back in school. The 8R Stealth Paradigm is live. "
    "Kaduna 2027 Convergence authorized. - Dr. Sa’ad Jaafaru"
)

target_nodes = [
    "2348099111515",
]

# TODO: Add the remaining 12,764 nodes from the CSV after this pulse succeeds.

TERMII_BULK_URL = "https://api.ng.termii.com/api/sms/send/bulk"

payload = {
    "api_key": api_key,
    "to": target_nodes,
    "from": from_id,
    "sms": SMS,
    "type": "plain",
    "channel": "generic",
}

response = requests.post(
    TERMII_BULK_URL,
    json=payload,
    headers={"Content-Type": "application/json"},
    timeout=60,
)

print(f"HTTP {response.status_code}")
print(response.text)
