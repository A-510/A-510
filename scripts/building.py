import sys, math, random, json
from PIL import Image, ImageDraw, ImageSequence
SRC=sys.argv[1]; OUT=sys.argv[2]
D=json.load(open(sys.argv[3])) if len(sys.argv)>3 else {'pushes':99}
PUSH=D.get('activity',D.get('pushes',0))
PRIORITY=['typing','building','thinking','thumbs-up','happy','music','swim']
AWAKE=set(PRIORITY[:min(7,math.ceil(PUSH/8))]) if PUSH else set()
RW,RH,ROOF,GND=100,76,16,6
W,H=RW*4,ROOF+RH*2+GND
T=80; TICK=100
order=[['typing','thinking','music','sleeping'],['building','swim','happy','thumbs-up']]
def load(name):
    im=Image.open(f'{SRC}/{name}.gif'); fr=[];du=[]
    for f in ImageSequence.Iterator(im):
        fr.append(f.convert('RGBA').resize((69,66),Image.NEAREST)); du.append(f.info.get('duration',150))
    tot=sum(du); loops=max(1,(T*TICK)//tot); seq=[]
    for k in range(T):
        t=k*TICK
        if t>=loops*tot: seq.append(0); continue
        t%=tot; acc=0
        for i,d in enumerate(du):
            acc+=d
            if t<acc: seq.append(i); break
    return fr,seq
SPR={n:load(n) for row in order for n in row}
def hsh(*a): return random.Random(hash(a)).random()
K='#080a14'
def base(d,x,y,wall,floor,fl2):
    d.rectangle([x,y,x+RW-1,y+RH-1],fill=wall)
    d.rectangle([x,y+RH-6,x+RW-1,y+RH-1],fill=floor); d.line([x,y+RH-6,x+RW-1,y+RH-6],fill=fl2)
    for i in range(x+6,x+RW,12): d.line([i,y+RH-5,i,y+RH-1],fill=fl2)
    d.rectangle([x+46,y+1,x+53,y+2],fill='#3a4466'); d.rectangle([x+48,y+3,x+51,y+3],fill='#ffe9a8')
def frame_border(d,x,y):
    d.rectangle([x,y,x+RW-1,y+RH-1],outline=K)
def r_typing(d,x,y,t):
    base(d,x,y,'#141b33','#232a44','#2f3858')
    for (mx,my) in ((3,14),(3,30)):
        d.rectangle([x+mx,y+my,x+mx+13,y+my+10],fill='#2a3350'); d.rectangle([x+mx+1,y+my+1,x+mx+12,y+my+9],fill='#06140f')
        for r in range(4):
            ln=int(3+hsh('c',mx,my,r,(t+r*3)//6)*8)
            d.line([x+mx+2,y+my+2+r*2,x+mx+1+ln,y+my+2+r*2],fill='#3fe08a' if r!=(t//5)%4 else '#b8ffd8')
    d.rectangle([x+86,y+24,x+96,y+69],fill='#0d1222'); d.rectangle([x+86,y+24,x+96,y+69],outline='#2a3350')
    for i in range(10):
        on=hsh('l',i,t//(2+i%3))>.45
        d.point([x+88+(i%2)*4,y+27+i*4],fill=('#3fe08a' if i%3 else '#ff5a4a') if on else '#1a2238')
        d.line([x+88,y+29+i*4,x+94,y+29+i*4],fill='#1a2238')
    d.line([x+60,y+72,x+86,y+72],fill='#0d1222')
def r_thinking(d,x,y,t):
    base(d,x,y,'#1d1830','#2b2440','#3a3154')
    d.rectangle([x+3,y+8,x+24,y+24],fill='#5a4a34'); d.rectangle([x+4,y+9,x+23,y+23],fill='#16302a')
    for bx,by in((6,11),(15,11),(10,18)): d.rectangle([x+bx,y+by,x+bx+5,y+by+3],outline='#dfe9e0')
    d.line([x+12,y+13,x+14,y+13],fill='#dfe9e0'); d.line([x+13,y+15,x+13,y+17],fill='#dfe9e0')
    n=(t//10)%4
    for i,c in enumerate(['#f0a04a','#ff8f9c','#7fd6e8']):
        if i<=n: d.rectangle([x+84+i*5,y+8+(i%2)*4,x+87+i*5,y+11+(i%2)*4],fill=c)
    d.rectangle([x+85,y+36,x+97,y+69],fill='#3a2a22'); 
    for s in range(3):
        yy=y+38+s*11; d.line([x+86,yy+8,x+96,yy+8],fill='#5a4030')
        for b in range(5): d.line([x+86+b*2,yy+1+int(hsh('b',s,b)*3),x+86+b*2,yy+7],fill=['#e0382c','#f0a04a','#7fd6e8','#8f68b4','#3fb07c'][(s+b)%5])
    d.rectangle([x+4,y+62,x+9,y+69],fill='#8a4a2a'); 
    for px_,py_ in((6,58),(4,60),(8,59),(6,55),(3,57),(9,56)): d.rectangle([x+px_,y+py_,x+px_+1,y+py_+2],fill='#3fb07c')
def r_music(d,x,y,t):
    base(d,x,y,'#261530','#34203f','#452b52')
    for i in range(0,RW-4,6):
        on=(i//6+t//4)%3; d.point([x+3+i,y+5+(1 if (i//6)%2 else 0)],fill=['#ff5a4a','#f0a04a','#7fd6e8'][on])
    d.rectangle([x+3,y+40,x+14,y+69],fill='#0d0a14'); d.rectangle([x+3,y+40,x+14,y+69],outline='#4a3458')
    b=1 if (t//2)%2 else 0
    d.ellipse([x+5-b,y+43-b,x+12+b,y+50+b],fill='#3a2848',outline='#8f68b4'); d.ellipse([x+5,y+56,x+12,y+65],fill='#3a2848',outline='#8f68b4'); d.point([x+8,y+60],fill='#e0382c')
    for i in range(6):
        hgt=int(3+10*abs(math.sin(t*.45+i*1.3))*(.5+.5*hsh('e',i)))
        d.rectangle([x+82+i*2+i//1*0,y+34-hgt,x+82+i*2,y+34],fill='#f0a04a' if hgt<9 else '#e0382c')
    d.rectangle([x+82,y+40,x+96,y+58],fill='#7a1a14'); d.ellipse([x+86,y+45,x+92,y+51],fill='#f0a04a'); d.rectangle([x+88,y+47,x+90,y+49],fill='#7a1a14')
    d.rectangle([x+4,y+14,x+16,y+30],fill='#1a2a4a'); d.line([x+6,y+26,x+10,y+18],fill='#7fd6e8'); d.line([x+10,y+18,x+14,y+26],fill='#7fd6e8')
def r_sleeping(d,x,y,t):
    base(d,x,y,'#0e1226','#171c34','#222946')
    d.rectangle([x+46,y+3,x+53,y+3],fill='#3a4466')
    d.rectangle([x+78,y+9,x+96,y+29],fill='#3a4466'); d.rectangle([x+79,y+10,x+95,y+28],fill='#050816')
    d.ellipse([x+86,y+13,x+93,y+20],fill='#ffe9a8'); d.ellipse([x+84,y+12,x+90,y+19],fill='#050816')
    for i,(sx,sy) in enumerate(((81,13),(83,22),(92,25),(88,24),(81,26))):
        if hsh('s',i,t//(5+i))>.3: d.point([x+sx,y+sy],fill='#dfe9ff')
    d.line([x+87,y+10,x+87,y+28],fill='#3a4466'); d.line([x+79,y+19,x+95,y+19],fill='#3a4466')
    d.rectangle([x+76,y+8,x+77,y+32],fill='#7a1a14'); d.rectangle([x+97,y+8,x+98,y+32],fill='#7a1a14')
    d.ellipse([x+5,y+12,x+15,y+22],fill='#dfe9ff',outline='#3a4466'); d.line([x+10,y+17,x+10,y+14],fill=K); d.line([x+10,y+17,x+10+(1 if (t//20)%2 else 2),y+18],fill='#e0382c')
    g=(t//8)%2
    d.rectangle([x+5,y+60,x+9,y+69],fill='#3a2a22'); d.rectangle([x+3,y+54,x+11,y+60],fill='#f0a04a' if g else '#d98a3a'); d.rectangle([x+1,y+66,x+13,y+69],fill='#f0a04a',outline=None) if False else None
    d.rectangle([x+20,y+71,x+80,y+73],fill='#3a2848')
def r_building(d,x,y,t):
    base(d,x,y,'#1b2030','#2a2f40','#3a4055')
    for i in range(-8,RW,8):
        d.polygon([(x+max(1,i),y+7),(x+max(1,i+4),y+7),(x+max(1,i+8),y+10),(x+max(1,i+4),y+10)],fill='#f0c040')
    d.rectangle([x+1,y+6,x+RW-2,y+6],fill=K); d.rectangle([x+1,y+11,x+RW-2,y+11],fill=K)
    for i in range(-8,RW,8):
        if i+8>RW-2: break
    d.rectangle([x+1,y+7,x+2,y+10],fill='#f0c040')
    sw=int(round(2*math.sin(t*.2)))
    d.line([x+12,y+12,x+12+sw,y+30],fill='#8b95a3'); d.rectangle([x+10+sw,y+30,x+14+sw,y+31],fill='#8b95a3'); d.rectangle([x+8+sw,y+32,x+16+sw,y+40],fill='#b0763a',outline='#5a3a1c'); d.line([x+8+sw,y+36,x+16+sw,y+36],fill='#e9dcc0')
    d.rectangle([x+1,y+64,x+RW-2,y+69],fill='#10131c'); 
    for i in range(0,RW,6): d.point([x+1+(i+t)%(RW-2),y+66],fill='#56607a'); d.point([x+1+(i+t+3)%(RW-2),y+68],fill='#56607a')
    for o_ in (0,50):
        cx=x+((t*1+o_)%110)-8
        if x+1<=cx<=x+RW-10: d.rectangle([cx,y+56,cx+8,y+63],fill='#b0763a',outline='#5a3a1c'); d.line([cx+4,y+56,cx+4,y+63],fill='#e9dcc0')
    d.rectangle([x+84,y+18,x+96,y+32],fill='#0d1222',outline='#3a4055'); d.rectangle([x+86,y+20,x+94,y+22],fill='#3fe08a' if (t//6)%2 else '#1a4a30'); d.rectangle([x+86,y+25,x+89,y+29],fill='#e0382c'); d.rectangle([x+91,y+25,x+94,y+29],fill='#f0a04a')
def r_swim(d,x,y,t):
    base(d,x,y,'#12303a','#1a4250','#24586a')
    for i in range(0,RW,8): d.line([x+i,y+1,x+i,y+RH-7],fill='#183c48')
    for j in range(4,RH-7,8): d.line([x+1,y+j,x+RW-2,y+j],fill='#183c48')
    d.rectangle([x+46,y+1,x+53,y+2],fill='#3a4466'); d.rectangle([x+48,y+3,x+51,y+3],fill='#ffe9a8')
    d.ellipse([x+4,y+10,x+18,y+24],fill='#06121c',outline='#8b95a3'); d.line([x+11,y+10,x+11,y+24],fill='#8b95a3'); d.line([x+4,y+17,x+18,y+17],fill='#8b95a3')
    for i in range(5):
        yy=y+50-((t+i*13)%44); xx=x+82+i*3+int(2*math.sin((t+i*9)*.3))
        d.point([xx,yy],fill='#bfe9f5'); d.point([xx+1,yy-1],fill='#8fc4d4')
    d.rectangle([x+84,y+16,x+96,y+18],fill='#8b95a3'); 
    for i,c in enumerate(['#ff8f9c','#f3ead8']): d.rectangle([x+85+i*6,y+19,x+89+i*6,y+30],fill=c)
def r_happy(d,x,y,t):
    base(d,x,y,'#15223a','#22304c','#30405e')
    d.rectangle([x+4,y+9,x+20,y+25],fill='#1f8a4c',outline='#0d4a28')
    d.line([x+7,y+17,x+11,y+21],fill='#fff',width=2); d.line([x+11,y+21,x+17,y+12],fill='#fff',width=2)
    d.rectangle([x+83,y+7,x+95,y+30],fill='#b02a22'); d.polygon([(x+83,y+30),(x+89,y+26),(x+95,y+30)],fill='#15223a')
    d.ellipse([x+86,y+12,x+92,y+18],outline='#f0c040'); d.point([x+89,y+15],fill='#f0c040')
    for (bx,by,bw,bh) in ((82,58,10,11),(90,62,8,7),(84,50,9,8)):
        d.rectangle([x+bx,y+by,x+bx+bw,y+by+bh],fill='#b0763a',outline='#5a3a1c'); d.line([x+bx+bw//2,y+by,x+bx+bw//2,y+by+bh],fill='#e9dcc0')
    d.rectangle([x+3,y+52,x+12,y+69],fill='#0d1222',outline='#30405e'); 
    for i in range(3): d.point([x+5+i*3,y+55],fill='#3fe08a' if (t//3+i)%3 else '#1a4a30')
    for i in range(8):
        yy=y+8+((t*2+int(hsh('k',i)*60))%58); xx=x+24+int(hsh('kx',i)*56)
        d.point([xx,yy],fill=['#f0a04a','#ff8f9c','#7fd6e8','#3fe08a'][i%4])
def r_thumbs(d,x,y,t):
    base(d,x,y,'#221a14','#33271c','#463626')
    d.rectangle([x+3,y+8,x+22,y+34],fill='#e9dcc0',outline='#5a4030'); d.rectangle([x+10,y+6,x+15,y+9],fill='#8b95a3')
    n=(t//12)%6
    for i in range(5):
        yy=y+12+i*4; d.line([x+10,yy,x+19,yy],fill='#9a8a70')
        d.rectangle([x+5,yy-1,x+7,yy+1],outline='#5a4030')
        if i<n: d.point([x+6,yy],fill='#1f8a4c'); d.point([x+7,yy-1],fill='#1f8a4c')
    d.rectangle([x+86,y+10,x+92,y+30],fill='#0d0a08',outline='#463626')
    d.ellipse([x+87,y+12,x+91,y+16],fill='#4a1410'); d.ellipse([x+87,y+18,x+91,y+22],fill='#4a3410'); d.ellipse([x+87,y+24,x+91,y+28],fill='#3fe08a' if (t//5)%4 else '#1a4a30')
    d.rectangle([x+82,y+40,x+96,y+69],fill='#14100c',outline='#5a4030'); d.rectangle([x+84,y+36,x+94,y+39],fill='#1f8a4c'); d.point([x+94,y+56],fill='#f0c040')
    d.rectangle([x+3,y+60,x+12,y+69],fill='#b0763a',outline='#5a3a1c'); d.line([x+3,y+64,x+12,y+64],fill='#e9dcc0')
ROOMS={'typing':r_typing,'thinking':r_thinking,'music':r_music,'sleeping':r_sleeping,'building':r_building,'swim':r_swim,'happy':r_happy,'thumbs-up':r_thumbs}
FONT={'D':["110","101","101","101","110"],'A':["111","101","111","101","101"],'Y':["101","101","111","010","010"],'P':["111","101","111","100","100"],'U':["101","101","101","101","111"],'E':["111","100","110","100","111"],'0':["111","101","101","101","111"],'1':["010","110","010","010","111"],'2':["111","001","111","100","111"],'3':["111","001","111","001","111"],'4':["101","101","111","001","001"],'5':["111","100","111","001","111"],'6':["111","100","111","101","111"],'7':["111","001","010","010","010"],'8':["111","101","111","101","111"],'9':["111","101","111","001","111"],'N':["101","111","111","111","101"],'I':["111","010","010","010","111"],'G':["111","100","101","101","111"],'H':["101","101","111","101","101"],'T':["111","010","010","010","010"],'S':["111","100","111","001","111"],'F':["111","100","110","100","100"],' ':["0","0","0","0","0"]}
STARS=[(random.Random(i).randrange(W),random.Random(i*7).randrange(0,9)) for i in range(40)]
frames=[]
for t in range(T):
    im=Image.new('RGBA',(W,H),'#070b18'); d=ImageDraw.Draw(im)
    for i,(sx,sy) in enumerate(STARS):
        if hsh('st',i,t//(6+i%5))>.25: d.point([sx,sy],fill='#aab6e0' if i%3 else '#ffe9a8')
    d.rectangle([0,ROOF-4,W-1,ROOF-1],fill='#0c0f1c'); d.line([0,ROOF-4,W-1,ROOF-4],fill='#2a3350')
    for ax in (30,70,330,372): d.line([ax,ROOF-4,ax,ROOF-12],fill='#2a3350'); d.line([ax-3,ROOF-10,ax+3,ROOF-10],fill='#2a3350'); d.line([ax-2,ROOF-8,ax+2,ROOF-8],fill='#2a3350')
    if (t//5)%2: d.point([30,ROOF-13],fill='#ff3b2e'); d.point([372,ROOF-13],fill='#ff3b2e')
    txt='NIGHT SHIFT'; tx=W//2-len(txt)*2; flick = t in (37,38,41)
    for ci,ch in enumerate(txt):
        dim = flick or (ch=='F' and (t%40) in (10,11,12,15))
        for ry,row in enumerate(FONT[ch]):
            for rx,v in enumerate(row):
                if v=='1': d.point([tx+ci*4+rx,ROOF-11+ry],fill='#6a1a14' if dim else '#ff4a3a')
    d.line([tx-2,ROOF-5,tx+len(txt)*4,ROOF-5],fill='#2a3350')
    t2='2 DAYS  '+str(min(PUSH,9999)); t2x=W-8-len(t2)*4
    for ci,ch in enumerate(t2):
        for ry,row in enumerate(FONT[ch]):
            for rx,v in enumerate(row):
                if v=='1': d.point([t2x+ci*4+rx,ROOF-11+ry],fill='#f0a04a' if ci>6 else '#56607a')
    d.rectangle([0,H-GND,W-1,H-1],fill='#0c0f1c'); d.line([0,H-GND,W-1,H-GND],fill='#2a3350')
    for r in range(2):
        for c in range(4):
            n=order[r][c]; x=c*RW; y=ROOF+r*RH
            ROOMS[n](d,x,y,t)
            # lamp cone
            cone=Image.new('RGBA',(W,H),(0,0,0,0)); cd=ImageDraw.Draw(cone)
            cd.polygon([(x+48,y+4),(x+51,y+4),(x+84,y+RH-7),(x+15,y+RH-7)],fill=(255,233,168,16 if (n in AWAKE) else 0))
            im.alpha_composite(cone); d=ImageDraw.Draw(im)
            asleep = n!='sleeping' and n not in AWAKE
            fr,seq=SPR['sleeping' if asleep else n]; sp=fr[seq[t]]; sx,sy=x+15,y+RH-6-66
            if n=='swim' and not asleep:
                px=sp.load(); wl=60; first=True
                for yy in range(40,66):
                    cols=[c for c in range(69) if px[c,yy][3]>0]
                    if not cols: continue
                    pl,pr=px[cols[0],yy],px[cols[-1],yy]
                    if not (pl[2]>170 and pl[2]>pl[0]+40): continue
                    if first: wl=yy; first=False
                    for xx in range(x+1,sx+cols[0]): im.putpixel((xx,sy+yy),pl)
                    for xx in range(sx+cols[-1]+1,x+RW-1): im.putpixel((xx,sy+yy),pr)
                for yy in range(sy+66,y+RH-1):
                    for xx in range(x+1,x+RW-1): im.putpixel((xx,yy),(58,140,214,255))
                # duck
                b=(t//6)%2
                d.rectangle([x+88,sy+wl-3+b,x+92,sy+wl-1+b],fill='#ffd84a'); d.rectangle([x+91,sy+wl-5+b,x+93,sy+wl-3+b],fill='#ffd84a'); d.point([x+94,sy+wl-4+b],fill='#ff8a2a'); d.point([x+92,sy+wl-5+b],fill=K)
            im.alpha_composite(sp,(sx,sy))
            if asleep:
                dark=Image.new('RGBA',(RW,RH),(4,6,16,150)); im.alpha_composite(dark,(x,y))
            d=ImageDraw.Draw(im)
            frame_border(d,x,y)
    frames.append(im.convert('RGB'))
S=3
big=[f.resize((W*S,H*S),Image.NEAREST) for f in frames]
mont=Image.new('RGB',(W*4,H*5))
for i in range(20): mont.paste(frames[i*4],((i%4)*W,(i//4)*H))
pal=mont.quantize(colors=255,method=Image.MEDIANCUT,dither=Image.NONE)
q=[f.quantize(palette=pal,dither=Image.NONE) for f in big]
q[0].save(OUT+'.gif',save_all=True,append_images=q[1:],duration=TICK,loop=0,optimize=True)
if len(sys.argv)>4: big[12].save(sys.argv[4])
