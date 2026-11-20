import sys, io, base64, json
from PIL import Image, ImageSequence
src, out = sys.argv[1], sys.argv[2]
D = json.load(open(sys.argv[3])) if len(sys.argv)>3 else {}
im=Image.open(src); frames=[]; durs=[]
for f in ImageSequence.Iterator(im):
    fr=f.convert('RGBA').resize((69,66),Image.NEAREST); b=io.BytesIO(); fr.save(b,'PNG',optimize=True)
    frames.append(base64.b64encode(b.getvalue()).decode()); durs.append(f.info.get('duration',150))
tot=sum(durs)
W,H=1200,380
SANS="'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC',sans-serif"
MONO="ui-monospace,'SF Mono',Menlo,Consolas,monospace"
lines=[("Oh, a visitor. Welcome to A-510's","workshop. Come in, the kettle's on."),
       ("Mostly Python and TypeScript in here:","MCP servers, small tools, sharp edges."),
       None,
       ("Stay as long as you like. If something","is useful, leave a star on your way out.")]
n=D.get('activity',0); last=D.get('last_repo','')
if n: shift=(f"This shift: {n} contribution{'s' if n!=1 else ''} in two days.", (f"Last on the line: {last[:26]}." if last else "The lights go out; the work doesn't."))
else: shift=("Quiet shift so far. Nothing on the line yet.","I dusted the servers anyway.")
lines=[l or shift for l in lines]
SLOT=6.5; CYC=SLOT*len(lines)
o=[];A=o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="A-510 — small tools, sharp edges, and the parts that keep running. The whale maid says: {" ".join(a+b for a,b in lines)}">')
A(f'''<defs><clipPath id="f"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1026"/><stop offset="1" stop-color="#1a1430"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".18"/></pattern>
<linearGradient id="box" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141a38" stop-opacity=".96"/><stop offset="1" stop-color="#0a0d1e" stop-opacity=".98"/></linearGradient></defs>
<g clip-path="url(#f)"><rect width="{W}" height="{H}" fill="url(#bg)"/>''')
import random; R=random.Random(3)
for i in range(46):
    x=R.randrange(0,W,4); y=R.randrange(0,230,4)
    A(f'<rect x="{x}" y="{y}" width="4" height="4" fill="{R.choice(["#aab6e0","#ffe9a8","#7fd6e8"])}" opacity=".7"><animate attributeName="opacity" values=".7;.1;.7" dur="{R.uniform(2,6):.1f}s" begin="-{R.uniform(0,6):.1f}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
# distant skyline blocks
x=0
while x<W:
    w=R.randrange(40,110,4); h=R.randrange(30,96,4)
    A(f'<rect x="{x}" y="{248-h}" width="{w}" height="{h+140}" fill="#111634"/>')
    for k in range(int(w*h/700)):
        A(f'<rect x="{x+R.randrange(4,max(8,w-8),4)}" y="{248-h+R.randrange(4,max(8,h-4),4)}" width="4" height="4" fill="{R.choice(["#f0a04a","#e0382c","#ffe9a8"])}" opacity=".8"/>')
    x+=w+R.randrange(0,12,4)
A(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
# dialogue box
BX,BY,BW,BH=250,202,910,150
A(f'''<g shape-rendering="crispEdges"><rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" fill="url(#box)"/>
<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" fill="none" stroke="#e0382c" stroke-width="4"/><rect x="{BX+8}" y="{BY+8}" width="{BW-16}" height="{BH-16}" fill="none" stroke="#f0a04a" stroke-width="2" opacity=".55"/>
''' + ''.join(f'<rect x="{cx}" y="{cy}" width="12" height="12" fill="#f0a04a"/>' for cx,cy in ((BX-4,BY-4),(BX+BW-8,BY-4),(BX-4,BY+BH-8),(BX+BW-8,BY+BH-8))) + f'''
<path d="M{BX+86} {BY-38}h206l16 16v26h-222z" fill="#e0382c"/><path d="M{BX+86} {BY-38}h206l16 16" fill="none" stroke="#ffb0a0" stroke-width="2"/></g>
<text x="{BX+106}" y="{BY-9}" font-family="{MONO}" font-weight="700" font-size="19" letter-spacing="4" fill="#fff6ea">WHALE MAID</text>
<text x="{BX+262}" y="{BY-10}" font-family="{SANS}" font-size="13" fill="#ffd0c4">鲸娘</text>
<g><text x="{BX+90}" y="92" font-family="'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif" font-size="64" letter-spacing="-1" fill="#f6eede">A-510</text>
<text x="{BX+94}" y="126" font-family="'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif" font-style="italic" font-size="21" fill="#f0a04a">small tools, sharp edges, and the parts that keep running</text>
<rect x="{BX+62}" y="42" width="6" height="92" fill="#e0382c"/></g>
<g font-family="{MONO}" font-size="13" letter-spacing="2" fill="#6f7aa6"><text x="{BX+BW-250}" y="{BY-10}">AUTO</text><text x="{BX+BW-180}" y="{BY-10}" fill="#f0a04a">▶ SKIP</text><text x="{BX+BW-90}" y="{BY-10}">LOG</text></g>''')
TX=BX+140
for i,(a,b) in enumerate(lines):
    s0=i*SLOT/CYC; e=(i+1)*SLOT/CYC; ty=1.3/CYC
    for j,txt in enumerate((a,b)):
        st=s0+j*ty; en=st+ty; wd=BW-190
        pts=[(0,0),(st,0),(en,wd),(e-0.001,wd),(e,0),(1,0)]
        pts=[p for k,p in enumerate(pts) if k==0 or p[0]>pts[k-1][0]+1e-6 or k==len(pts)-1]
        if pts[1][0]<=1e-6: pts=pts[1:]; pts[0]=(0,0)
        A(f'<clipPath id="c{i}{j}"><rect x="{TX}" y="{BY+28+j*46}" height="46" width="0"><animate attributeName="width" values="{";".join(str(p[1]) for p in pts)}" keyTimes="{";".join(f"{p[0]:.4f}" for p in pts)}" dur="{CYC}s" repeatCount="indefinite"/></rect></clipPath>')
        A(f'<g clip-path="url(#c{i}{j})"><text x="{TX}" y="{BY+62+j*46}" font-family="{MONO}" font-size="27" fill="#f4f0ff">{txt.replace("&","&amp;")}</text></g>')
A(f'<path d="M{BX+BW-50} {BY+BH-40}h24l-12 14z" fill="#f0a04a"><animate attributeName="opacity" values="1;0" dur=".8s" calcMode="discrete" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 0;0 4" dur=".8s" calcMode="discrete" repeatCount="indefinite"/></path>')
# portrait
S=4.4; PX,PY=58,H-66*S+6
A(f'<g transform="translate({PX} {PY:.0f}) scale({S})" style="image-rendering:pixelated">')
acc=0
for i,(f,d) in enumerate(zip(frames,durs)):
    a0=acc/tot; a1=(acc+d)/tot; acc+=d
    if i==0: vals,kt='1;0;0',f'0;{a1:.4f};1'
    elif i==len(frames)-1: vals,kt='0;1;1',f'0;{a0:.4f};1'
    else: vals,kt='0;1;0;0',f'0;{a0:.4f};{a1:.4f};1'
    A(f'<image width="69" height="66" href="data:image/png;base64,{f}" opacity="{1 if i==0 else 0}" image-rendering="pixelated"><animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{tot/1000:.2f}s" calcMode="discrete" repeatCount="indefinite"/></image>')
A('</g></g></svg>')
svg='\n'.join(o); open(out,'w').write(svg)
# still preview: show line 2 fully
p=svg
for j in (0,1): p=p.replace('<clipPath id="c0%d"><rect x="%d" y="%d" height="46" width="0">'%(j,TX,BY+28+j*46),'<clipPath id="c0%d"><rect x="%d" y="%d" height="46" width="800">'%(j,TX,BY+28+j*46))
open(out.replace('.svg','_prev.svg'),'w').write(p)
