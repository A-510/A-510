"""Operator-file style stats card, drawn from data.json."""
import sys, io, json, math, base64
from PIL import Image
src, out, D = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
im = Image.open(src); im.seek(min(8, im.n_frames - 1))
b = io.BytesIO(); im.convert("RGBA").resize((69, 66), Image.NEAREST).save(b, "PNG"); PORT = base64.b64encode(b.getvalue()).decode()
W, H = 1200, 320
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"
LC = {"Python": "#3572A5", "TypeScript": "#3178c6", "Rust": "#dea584", "JavaScript": "#f1e05a", "Go": "#00ADD8", "Shell": "#89e051", "C": "#8b95a3", "C++": "#f34b7d", "HTML": "#e34c26", "Dart": "#00B4AB", "Gleam": "#ffaff3", "Lua": "#5a67d8", "PowerShell": "#5391fe"}
o = []; A = o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Operator file for {D["user"]}: {D["stars"]} stars, {D["followers"]} followers, {D["repos"]} public repositories, {D.get("activity", 0)} contributions in the last two days.">')
A(f'''<defs><clipPath id="f"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1026"/><stop offset="1" stop-color="#1a1430"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".18"/></pattern></defs>
<g clip-path="url(#f)"><rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#scan)"/>
<g shape-rendering="crispEdges"><rect x="24" y="24" width="{W-48}" height="{H-48}" fill="none" stroke="#e0382c" stroke-width="4"/><rect x="32" y="32" width="{W-64}" height="{H-64}" fill="none" stroke="#f0a04a" stroke-width="2" opacity=".5"/>''')
for cx, cy in ((20, 20), (W - 32, 20), (20, H - 32), (W - 32, H - 32)): A(f'<rect x="{cx}" y="{cy}" width="12" height="12" fill="#f0a04a"/>')
A(f'<path d="M24 24h250l18 18v22H24z" fill="#e0382c"/></g>')
A(f'<text x="44" y="53" font-family="{MONO}" font-weight="700" font-size="17" letter-spacing="4" fill="#fff6ea">OPERATOR FILE</text>')
A(f'<text x="60" y="140" font-family="{SERIF}" font-size="58" letter-spacing="-1" fill="#f6eede">{D["user"]}</text>')
A(f'<text x="62" y="172" font-family="{SERIF}" font-style="italic" font-size="19" fill="#f0a04a">night-shift cat · tools for agents</text>')
star = "M0-11l3 7 8 1-6 5 2 8-7-4-7 4 2-8-6-5 8-1z"
for i in range(6): A(f'<path d="{star}" transform="translate({72 + i * 30} 208)" fill="#f0a04a"/>')
A(f'<text x="60" y="262" font-family="{MONO}" font-size="12.5" letter-spacing="2.4" fill="#6f7aa6">CLASS  SUPPORTER / FACTORY</text>')
A(f'<text x="60" y="282" font-family="{MONO}" font-size="12.5" letter-spacing="2.4" fill="#6f7aa6">TRAIT  DOES NOT CLOCK OUT</text>')
# stat bars
X0 = 470
rows = [("STARS", D["stars"], 20000), ("FOLLOWERS", D["followers"], 2000), ("REPOS", D["repos"], 1000), ("LAST 2 DAYS", D.get("activity", 0), 300)]
for i, (lab, v, mx) in enumerate(rows):
    y = 84 + i * 36; seg = min(12, max(1 if v else 0, round(12 * math.log10(v + 1) / math.log10(mx + 1))))
    A(f'<text x="{X0}" y="{y}" font-family="{MONO}" font-size="14" letter-spacing="2.2" fill="#8b90b8">{lab}</text>')
    A('<g shape-rendering="crispEdges">' + "".join(f'<rect x="{X0 + 168 + k * 20}" y="{y - 13}" width="16" height="14" fill="{("#e0382c" if k < 8 else "#f0a04a") if k < seg else "#232a4a"}"/>' for k in range(12)) + "</g>")
    A(f'<text x="{X0 + 422}" y="{y}" font-family="{MONO}" font-weight="700" font-size="17" fill="#f6eede">{v:,}</text>')
# languages
langs = D.get("langs") or []
if langs:
    y = 236; x = X0; BWID = 430
    A(f'<text x="{X0}" y="{y - 12}" font-family="{MONO}" font-size="12.5" letter-spacing="2.4" fill="#6f7aa6">LOADOUT</text><g shape-rendering="crispEdges">')
    tot = sum(s for _, s in langs)
    for n, s in langs:
        w = max(4, round(BWID * s / tot)); A(f'<rect x="{x}" y="{y}" width="{w - 3}" height="14" fill="{LC.get(n, "#8b90b8")}"/>'); x += w
    A("</g>"); x = X0
    for n, s in langs[:4]:
        A(f'<rect x="{x}" y="{y + 28}" width="10" height="10" fill="{LC.get(n, "#8b90b8")}"/><text x="{x + 16}" y="{y + 38}" font-family="{MONO}" font-size="13" fill="#c9cde6">{n} {round(100 * s / tot)}%</text>')
        x += 34 + len(f"{n} {round(100 * s / tot)}%") * 8.2
A(f'<image x="{W - 300}" y="{H - 30 - 66 * 3.6:.0f}" width="{69 * 3.6:.0f}" height="{66 * 3.6:.0f}" href="data:image/png;base64,{PORT}" style="image-rendering:pixelated" image-rendering="pixelated"/>')
A("</g></svg>")
open(out, "w").write("\n".join(o))
