
from pathlib import Path
import json
import re
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "contributions.json"
USERNAME = "ubstorm128"


def main():
    url = f"https://github.com/users/{USERNAME}/contributions"
    response = requests.get(
        url,
        headers={"User-Agent": "GitHub-Profile-Heatmap"},
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    days = []

    for cell in soup.select("td[data-date][data-level]"):
        date = cell.get("data-date")
        level = int(cell.get("data-level", "0"))

        if date:
            days.append({
                "date": date,
                "level": level,
            })

    if not days:
        raise RuntimeError(
            "No contribution days found. GitHub may have changed "
            "its HTML structure or the request was blocked."
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps({
            "username": USERNAME,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "days": days,
        }, indent=2),
        encoding="utf-8",
    )

    print(f"Saved {len(days)} contribution days to {OUTPUT}")


if __name__ == "__main__":
    main()
