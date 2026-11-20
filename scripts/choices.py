"""Static visual-novel choice buttons."""
import sys
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"
for name, label in (("work", "See what we build"), ("shift", "Tour the night shift"), ("whale", "Meet the whale maid")):
    W, H = 384, 64
    open(f"{sys.argv[1]}/choice-{name}.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
<g shape-rendering="crispEdges"><rect x="4" y="4" width="{W-8}" height="{H-8}" fill="#0f1430"/><rect x="4" y="4" width="{W-8}" height="{H-8}" fill="none" stroke="#e0382c" stroke-width="3"/><rect x="0" y="0" width="10" height="10" fill="#f0a04a"/><rect x="{W-10}" y="{H-10}" width="10" height="10" fill="#f0a04a"/></g>
<path d="M30 22l14 10-14 10z" fill="#f0a04a"><animate attributeName="opacity" values="1;.3" dur=".9s" calcMode="discrete" repeatCount="indefinite"/></path>
<text x="60" y="39" font-family="{MONO}" font-size="19" fill="#f4f0ff">{label}</text></svg>''')
