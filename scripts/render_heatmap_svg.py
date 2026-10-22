
from pathlib import Path
from datetime import date, timedelta
import json
import html

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

CELL = 11
GAP = 4
STEP = CELL + GAP
LEFT = 42
TOP = 52
WEEKS = 53
WIDTH = 860
HEIGHT = 230

def main():
    if not INPUT.exists():
        raise SystemExit("Missing data/contributions.json")

    data = json.loads(INPUT.read_text(encoding="utf-8"))
    days = {
        item["date"]: max(0, min(5, int(item["level"])))
        for item in data["days"]
    }

    today = max(date.fromisoformat(d) for d in days)
    start = today - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<style>',
        '@keyframes reveal {',
        'from { opacity:0; transform:translateY(-7px); }',
        'to { opacity:1; transform:translateY(0); }',
        '}',
        '.day { opacity:0; animation:reveal .35s ease-out forwards; }',
        '</style>',
        '<rect width="100%" height="100%" rx="8" fill="#0d1117"/>',
        '<text x="22" y="26" fill="#c9d1d9" '
        'font-size="15" font-family="monospace">'
        'GitHub Contribution Activity</text>',
    ]

    for week in range(WEEKS):
        for weekday in range(7):
            current = start + timedelta(days=week * 7 + weekday)
            if current > today:
                continue

            level = days.get(current.isoformat(), 0)
            x = LEFT + week * STEP
            y = TOP + weekday * STEP

            delay = week * 0.035 + weekday * 0.045

            parts.append(
                f'<rect class="day" x="{x}" y="{y}" '
                f'width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{PALETTE[level]}" '
                f'style="animation-delay:{delay:.3f}s">'
                f'<title>{current.isoformat()}</title>'
                f'</rect>'
            )

    for label, weekday in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        y = TOP + weekday * STEP + 9
        parts.append(
            f'<text x="7" y="{y}" fill="#8b949e" '
            f'font-size="10" font-family="monospace">'
            f'{label}</text>'
        )

    parts.append(
        '<text x="650" y="197" fill="#8b949e" '
        'font-size="11" font-family="monospace">Less</text>'
    )

    for i, color in enumerate(PALETTE):
        parts.append(
            f'<rect x="{686+i*17}" y="187" width="11" '
            f'height="11" rx="2" fill="{color}"/>'
        )

    parts.append(
        '<text x="794" y="197" fill="#8b949e" '
        'font-size="11" font-family="monospace">More</text>'
    )

    parts.append("</svg>")

    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
