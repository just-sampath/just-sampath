"""Generate the GitHub profile README images (light + dark). Usage: python scripts/generate_assets.py assets"""
import os
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "light": dict(paper="#fbf7f0", dots="#e6dfd2", ink="#24292f", muted="#5f646b",
                  accent="#c2410c", accent_soft="#f3d3bd", box="#fffdf9", border="#d9d1c3"),
    "dark": dict(paper="#14181f", dots="#262d37", ink="#e7e2d9", muted="#9aa3ad",
                 accent="#fb923c", accent_soft="#4a2f1d", box="#1b2029", border="#2f3743"),
}
SANS = "ui-sans-serif, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"


def defs(t, w, h):
    return f"""
  <defs>
    <pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="{t['dots']}"/>
    </pattern>
    <filter id="rough" filterUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">
      <feTurbulence type="fractalNoise" baseFrequency="0.025" numOctaves="2" seed="7"/>
      <feDisplacementMap in="SourceGraphic" scale="1.4"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M1 1 L9 5 L1 9" fill="none" stroke="{t['ink']}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <marker id="arrow-accent" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M1 1 L9 5 L1 9" fill="none" stroke="{t['accent']}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="{t['paper']}" stroke="{t['border']}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#dots)"/>"""


def style(t):
    return f"""
  <style>
    text {{ font-family: {SANS}; }}
    .flow {{ stroke: {t['accent']}; stroke-width: 2.4; stroke-linecap: round; stroke-dasharray: 2 16;
             animation: flow 1.4s linear infinite; }}
    @keyframes flow {{ to {{ stroke-dashoffset: -36; }} }}
    @media (prefers-reduced-motion: reduce) {{ .flow {{ animation: none; opacity: 0; }} }}
  </style>"""


def box(t, x, y, w, h, label, note):
    cx = x + w / 2
    return f"""
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t['box']}" stroke="{t['ink']}" stroke-width="1.6" filter="url(#rough)"/>
    <text x="{cx}" y="{y + h / 2 + 6}" text-anchor="middle" font-size="17" font-weight="600" fill="{t['ink']}">{escape(label)}</text>
    <text x="{cx}" y="{y - 12}" text-anchor="middle" font-size="12.5" fill="{t['muted']}">{escape(note)}</text>"""


def arrow(t, x1, x2, y):
    return f"""
    <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{t['ink']}" stroke-width="1.6" marker-end="url(#arrow)" filter="url(#rough)"/>
    <line class="flow" x1="{x1 + 4}" y1="{y}" x2="{x2 - 10}" y2="{y}"/>"""


def tap(t, x, y1, y2):
    """Dotted line from a step down to the observability lane."""
    return f"""
    <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2 - 4}" stroke="{t['muted']}" stroke-width="1.4" stroke-dasharray="2 5" stroke-linecap="round"/>
    <circle cx="{x}" cy="{y2}" r="3.5" fill="{t['muted']}"/>"""


def header(name, t):
    w, h = 900, 440
    by, bh = 206, 48           # box row
    cy = by + bh / 2
    lane_y, lane_h = 350, 50   # observability lane
    goal = "making AI systems reliable &amp; cost-effective at scale"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"
     aria-label="Sampath: full stack and applied AI engineer, backend and system design at heart. Now: making AI systems reliable and cost-effective at scale.">
  {style(t)}{defs(t, w, h)}
  <text x="48" y="78" font-size="40" font-weight="700" fill="{t['ink']}" letter-spacing="-0.5">Sampath</text>
  <text x="50" y="108" font-size="16" fill="{t['muted']}">full stack &amp; applied AI engineer · backend &amp; system design at heart</text>

  <rect x="48" y="128" width="54" height="24" rx="12" fill="{t['accent']}"/>
  <text x="75" y="144.5" text-anchor="middle" font-size="11.5" font-weight="700" fill="{t['paper']}" letter-spacing="1">NOW</text>
  <text x="114" y="145" font-size="16" fill="{t['ink']}">{goal}</text>

  <g>
    <circle cx="58" cy="{cy}" r="5" fill="{t['accent']}"/>
    <text x="70" y="{cy + 5}" font-size="15" fill="{t['ink']}">request</text>
    {arrow(t, 136, 186, cy)}
    {box(t, 190, by, 150, bh, "boundary", "budget: time + cost")}
    {arrow(t, 342, 392, cy)}
    {box(t, 396, by, 130, bh, "model", "suggests")}
    {arrow(t, 528, 578, cy)}
    {box(t, 582, by, 130, bh, "check", "code decides")}
    {arrow(t, 714, 770, cy)}
    <circle cx="796" cy="{cy}" r="22" fill="{t['accent_soft']}" stroke="{t['accent']}" stroke-width="2" filter="url(#rough)"/>
    <path d="M785 {cy} l7 7 l13 -14" fill="none" stroke="{t['accent']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="796" y="{by - 12}" text-anchor="middle" font-size="12.5" fill="{t['muted']}">reliable</text>

    <path d="M647 {by + bh} V{by + bh + 40} H461 V{by + bh + 8}" fill="none" stroke="{t['accent']}" stroke-width="1.8"
          stroke-dasharray="6 6" marker-end="url(#arrow-accent)" filter="url(#rough)"/>
    <text x="554" y="{by + bh + 62}" text-anchor="middle" font-size="13" font-weight="600" fill="{t['accent']}">retry ≤ n, then fail loudly</text>

    {tap(t, 265, by + bh, lane_y)}
    {tap(t, 420, by + bh, lane_y)}
    {tap(t, 690, by + bh, lane_y)}
    {tap(t, 796, cy + 22, lane_y)}
    <rect x="190" y="{lane_y}" width="660" height="{lane_h}" rx="{lane_h / 2}" fill="{t['box']}" stroke="{t['ink']}"
          stroke-width="1.6" filter="url(#rough)"/>
    <g transform="translate(214 {lane_y + lane_h / 2})" fill="none" stroke="{t['accent']}" stroke-width="2"
       stroke-linecap="round" stroke-linejoin="round">
      <path d="M0 0 H6 L10 -9 L16 9 L21 -4 L24 0 H30"/>
    </g>
    <text x="256" y="{lane_y + lane_h / 2 + 6}" font-size="17" font-weight="600" fill="{t['ink']}">observe</text>
    <text x="336" y="{lane_y + lane_h / 2 + 5}" font-size="13.5" fill="{t['muted']}">traces · latency · cost · answer quality, on every step</text>
  </g>
</svg>
"""
    open(os.path.join(OUT, f"{name}-{'dark' if t is THEMES['dark'] else 'light'}.svg"), "w", encoding="utf-8").write(svg)


CARDS = [
    ("adaptive-deterministic-rag", "RAG where code, not the model, makes the decisions",
     "hybrid search · faithfulness checks · 98% test coverage", "Python", "#3572A5"),
    ("paydown", "Floating-rate home-loan tracker with what-if scenarios",
     "encrypted private data · leak check in CI · live demo", "TypeScript", "#3178c6"),
    ("leetcode-guider", "An AI coach that won't just hand you the answer",
     "Chrome extension · works with 5 LLM providers", "JavaScript", "#f1e05a"),
    ("get-GO-ing", "Learning Go, the Go way",
     "interfaces · goroutines · a chi + Postgres API", "Go", "#00ADD8"),
]


def card(repo, line1, line2, lang, lang_color, t, theme):
    w, h = 440, 150
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"
     aria-label="{escape(repo)}: {escape(line1)}">
  {style(t)}{defs(t, w, h)}
  <g filter="url(#rough)">
    <circle cx="32" cy="36" r="6" fill="none" stroke="{t['accent']}" stroke-width="2"/>
    <line x1="38" y1="36" x2="50" y2="36" stroke="{t['accent']}" stroke-width="2"/>
    <circle cx="56" cy="36" r="6" fill="{t['accent']}"/>
  </g>
  <text x="74" y="42" font-size="17" font-weight="700" fill="{t['ink']}">{escape(repo)}</text>
  <text x="26" y="80" font-size="14" fill="{t['ink']}">{escape(line1)}</text>
  <text x="26" y="102" font-size="12.5" fill="{t['muted']}">{escape(line2)}</text>
  <circle cx="32" cy="127" r="5" fill="{lang_color}"/>
  <text x="44" y="131.5" font-size="12.5" fill="{t['muted']}">{escape(lang)}</text>
  <text x="{w - 24}" y="131.5" text-anchor="end" font-size="12.5" font-weight="600" fill="{t['accent']}">view repo →</text>
</svg>
"""
    open(os.path.join(OUT, f"card-{repo}-{theme}.svg"), "w", encoding="utf-8").write(svg)


TOOLBOX = [
    ("build", ["Python", "TypeScript", "Node.js", "FastAPI", "Express"]),
    ("store", ["MongoDB", "PostgreSQL", "Redis", "Qdrant", "Pinecone"]),
    ("run", ["AWS", "Azure Functions", "Docker", "BullMQ"]),
    ("think", ["Claude", "OpenAI", "LangGraph", "LlamaIndex"]),
    ("learning", ["Go"]),
]


def toolbox(t, theme):
    w = 900
    row_h, top = 46, 34
    h = top + row_h * len(TOOLBOX) + 14
    rows = []
    for i, (group, items) in enumerate(TOOLBOX):
        y = top + i * row_h
        rows.append(f'<text x="40" y="{y + 21}" font-size="13" font-weight="700" fill="{t["accent"]}">{group}</text>')
        x = 140
        for item in items:
            cw = round(len(item) * 7.9 + 30)
            rows.append(
                f'<rect x="{x}" y="{y}" width="{cw}" height="30" rx="15" fill="{t["box"]}" stroke="{t["ink"]}" '
                f'stroke-width="1.3" filter="url(#rough)"/>'
                f'<text x="{x + cw / 2}" y="{y + 20}" text-anchor="middle" font-size="13.5" fill="{t["ink"]}">{escape(item)}</text>')
            x += cw + 10
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"
     aria-label="Toolbox: {escape('; '.join(g + ': ' + ', '.join(i) for g, i in TOOLBOX))}">
  {style(t)}{defs(t, w, h)}
  {''.join(rows)}
</svg>
"""
    open(os.path.join(OUT, f"toolbox-{theme}.svg"), "w", encoding="utf-8").write(svg)


for theme, t in THEMES.items():
    header("header", t)
    for c in CARDS:
        card(*c, t, theme)
    toolbox(t, theme)

print("\n".join(sorted(os.listdir(OUT))))
