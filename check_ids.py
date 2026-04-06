"""
Fetch and print all Sender IDs for this Termii account (Fetch Sender ID API).
"""

import json
import sys

import requests

from termii_strike import API_BASE, api_key

FETCH_URL = f"{API_BASE}/api/sender-id"


def main() -> None:
    r = requests.get(
        FETCH_URL,
        params={"api_key": api_key},
        timeout=60,
    )
    print(f"HTTP {r.status_code}")
    raw = r.text
    print(raw)

    try:
        data = r.json()
    except ValueError:
        print("Response was not JSON.", file=sys.stderr)
        sys.exit(1)

    content = data.get("content") or []
    if not content:
        print("\nNo sender IDs returned (empty list).")
        return

    approved = [x for x in content if (x.get("status") or "").lower() == "active"]
    other = [x for x in content if (x.get("status") or "").lower() != "active"]

    print("\n--- Approved (active) sender IDs ---")
    if not approved:
        print("(none)")
    else:
        for row in approved:
            sid = row.get("sender_id", "")
            print(f"  {sid!r}  country={row.get('country')!r}  createdAt={row.get('createdAt')!r}")

    print("\n--- Other (pending / blocked / etc.) ---")
    if not other:
        print("(none)")
    else:
        for row in other:
            sid = row.get("sender_id", "")
            st = row.get("status", "")
            print(f"  {sid!r}  status={st!r}  country={row.get('country')!r}")

    print("\n--- All sender_id values (raw list) ---")
    print(json.dumps([x.get("sender_id") for x in content], indent=2))


if __name__ == "__main__":
    main()
