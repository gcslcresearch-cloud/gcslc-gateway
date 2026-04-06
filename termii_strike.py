"""
Termii SMS pulse — test node first, then scale from CSV.

Uses Bulk SMS with the first *active* sender ID from the account when available.
If there are no active alphanumeric sender IDs, falls back to the Number API
(Termii-assigned numeric sender — no `from` field).
"""

import sys

import requests

API_BASE = "https://api.ng.termii.com"

api_key = "TLAnLkwddGzmlfEwqXDAhklvmzytWsFfKuVevKqPMYTARQjDRUXVyJNFOfUDtw"

SMS = (
    "300k children back in school. The 8R Stealth Paradigm is live. "
    "Kaduna 2027 Convergence authorized. - Dr. Sa’ad Jaafaru"
)

target_nodes = [
    "2348099111515",
]

# TODO: Add the remaining 12,764 nodes from the CSV after this pulse succeeds.

TERMII_BULK_URL = f"{API_BASE}/api/sms/send/bulk"
TERMII_NUMBER_SEND_URL = f"{API_BASE}/api/sms/number/send"
SENDER_ID_URL = f"{API_BASE}/api/sender-id"


def fetch_sender_id_response():
    return requests.get(
        SENDER_ID_URL,
        params={"api_key": api_key},
        timeout=60,
    )


def active_sender_ids(payload: dict):
    content = payload.get("content") or []
    return [
        x["sender_id"]
        for x in content
        if (x.get("status") or "").lower() == "active" and x.get("sender_id")
    ]


def send_bulk(from_sender: str) -> None:
    body = {
        "api_key": api_key,
        "to": target_nodes,
        "from": from_sender,
        "sms": SMS,
        "type": "plain",
        "channel": "generic",
    }
    response = requests.post(
        TERMII_BULK_URL,
        json=body,
        headers={"Content-Type": "application/json"},
        timeout=120,
    )
    print(f"HTTP {response.status_code}")
    print(response.text)


def send_number_api() -> None:
    """Number API: no `from` / no alphanumeric sender — Termii routes via auto number."""
    for to in target_nodes:
        body = {
            "api_key": api_key,
            "to": to,
            "sms": SMS,
        }
        response = requests.post(
            TERMII_NUMBER_SEND_URL,
            json=body,
            headers={"Content-Type": "application/json"},
            timeout=120,
        )
        print(f"Number API  to={to!r}  HTTP {response.status_code}")
        print(response.text)


def main() -> None:
    r = fetch_sender_id_response()
    print(f"Sender ID fetch  HTTP {r.status_code}")
    if r.status_code != 200:
        print(r.text)
        print("Sender ID list not available — using Number API.", file=sys.stderr)
        send_number_api()
        return

    try:
        data = r.json()
    except ValueError:
        print(r.text)
        print("Invalid JSON from sender-id — using Number API.", file=sys.stderr)
        send_number_api()
        return

    actives = active_sender_ids(data)
    if actives:
        use = actives[0]
        print(f"Bulk SMS  from={use!r}  channel=generic")
        send_bulk(use)
    else:
        print(
            "No active sender IDs in account — using Number API (numeric / auto sender).",
            file=sys.stderr,
        )
        send_number_api()


if __name__ == "__main__":
    main()
