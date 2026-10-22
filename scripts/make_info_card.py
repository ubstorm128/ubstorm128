from pathlib import Path
import os

OUTPUT = Path(__file__).resolve().parent.parent / "info-card.svg"
STATIC = os.getenv("STATIC") == "1"

lines = [
    ("user", "ubstorm128"),
    ("role", "BCA Student | Developer"),
    ("focus", "Web Development"),
    ("interest", "Cybersecurity"),
    ("languages", "C, Java, Python, JavaScript"),
    ("stack", "React, Node.js, Express"),
    ("database", "MySQL, PostgreSQL, MongoDB"),
    ("status", "Building projects"),
]

width = 490
line_height = 29
height = 78 + len(lines) * line_height

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">',
    """
    <rect width="100%" height="100%" rx="12"
          fill="#0d1117" stroke="#30363d"/>
    <circle cx="20" cy="20" r="5" fill="#ff5f56"/>
    <circle cx="38" cy="20" r="5" fill="#ffbd2e"/>
    <circle cx="56" cy="20" r="5" fill="#27c93f"/>
    <text x="76" y="25" fill="#8b949e"
          font-family="monospace" font-size="12">
      ubstorm128@github ~
    </text>
    """,
]

for i, (key, value) in enumerate(lines):
    y = 65 + i * line_height
    delay = 0 if STATIC else i * 0.22

    parts.append(f"""
    <g font-family="monospace" font-size="13"
       opacity="1">
      <animate attributeName="opacity"
               values="0;1"
               begin="{delay:.2f}s"
               dur="0.35s"
               fill="freeze"/>
      <text x="20" y="{y}" fill="#39d353">
        {key}
      </text>
      <text x="115" y="{y}" fill="#c9d1d9">
        {value}
      </text>
    </g>
    """)

parts.append("</svg>")

OUTPUT.write_text("\n".join(parts), encoding="utf-8")
print(f"Created: {OUTPUT}")