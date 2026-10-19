"""Draws all 35 original toy illustrations (vector, no photos).
Run: python3 scripts/mockup_illustrations_all.py out.json sheet_prefix
(out.json is embedded into site/index.html; sheet_*.html are contact sheets for review.)"""
import json, math, random, sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mockup_illustrations import shade, wrap, SH, ILLUS as BASE

def R(x,y,w,h,rx,fill,ex=""): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {ex}/>'
def E(cx,cy,rx,ry,fill,ex=""): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" {ex}/>'
def C(cx,cy,r,fill,ex=""): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {ex}/>'
def Pa(d,fill,ex=""): return f'<path d="{d}" fill="{fill}" {ex}/>'
def S(y=186,rx=60,ry=8): return SH.format(y=y,rx=rx,ry=ry)
def OUT(c,w=1.6): return f'stroke="{shade(c,.62)}" stroke-width="{w}" stroke-linejoin="round"'
def star(cx,cy,r,fill):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*.45
        pts.append(f"{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'

M={}

# 1 Action figure
def action():
    skin="#f0c29a"; s=[S(187,46)]
    s.append(Pa("M68 80 Q100 68 132 80 L146 156 Q100 172 54 156Z","#d6382f"))
    s.append(Pa("M80 84 Q100 76 120 84 L128 150 Q100 160 72 150Z","#b52a22"))
    s.append(R(78,126,21,48,7,"#1f6fd1")+R(101,126,21,48,7,"#1f6fd1"))
    s.append(R(74,164,27,19,8,"#d6382f")+R(99,164,27,19,8,"#d6382f"))
    s.append(Pa("M70 78 L130 78 L121 134 L79 134Z","#2a78d6",OUT("#2a78d6")))
    s.append(C(100,102,14,"#ffd34d")+star(100,102,10,"#d6382f"))
    s.append(R(77,126,46,9,4,"#ffd34d"))
    for x in (50,128):
        s.append(R(x,80,22,32,10,"#2a78d6")+R(x+2,104,18,28,9,skin)+C(x+11,134,10,skin))
    s.append(C(100,55,23,skin))
    s.append(Pa("M76 56 Q76 28 100 28 Q124 28 124 56 Q100 44 76 56Z","#d6382f"))
    s.append(R(79,50,42,13,6,"#d6382f")+E(90,56,5.5,3.2,"#fff")+E(110,56,5.5,3.2,"#fff")+C(90,56,1.8,"#1c1f26")+C(110,56,1.8,"#1c1f26"))
    s.append('<path d="M92 70 q8 6 16 0" stroke="#a55a3a" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    return wrap("".join(s))
M[1]=action()

# 2 Animal figures
def animals():
    s=[E(100,184,84,9,"#000","opacity=\".13\""),E(100,176,80,13,"#d8c8a6"),E(100,172,80,13,"#eadcbc")]
    # elephant
    g="#98a5b6"
    s.append(R(40,164,13,14,4,g)+R(66,164,13,14,4,g))
    s.append(E(58,150,28,22,g)+C(86,140,15,g)+E(75,141,13,15,"#8794a7")+Pa("M98 142 q9 6 3 22 q-3 6 -8 2 q4 -8 -2 -16Z",g)+Pa("M96 150 q8 3 10 11 l-5 2z","#fff")+C(90,136,2.2,"#2a2a2a"))
    # giraffe
    s.append(R(104,166,6,12,2,"#d49a22")+R(124,166,6,12,2,"#d49a22")+E(118,156,19,14,"#f2b632"))
    s.append(Pa("M118 150 L124 80 L136 80 L134 154Z","#f2b632"))
    s.append(E(138,76,13,9,"#f2b632",'transform="rotate(-12 138 76)"')+Pa("M132 68 l-2 -10 M140 66 l1 -10","none",'stroke="#8a5a1a" stroke-width="2"')+C(130,57,2.5,"#8a5a1a")+C(141,56,2.5,"#8a5a1a")+C(142,74,2,"#2a2a2a"))
    for cx,cy in ((112,154),(124,160),(128,110),(126,130),(130,92),(110,164)): s.append(C(cx,cy,3.6,"#a8661a"))
    # lion
    s.append(R(152,168,6,10,2,"#d08a24")+R(172,168,6,10,2,"#d08a24")+E(164,162,20,12,"#e9a23b"))
    s.append(C(176,148,17,"#a8601e")+C(176,148,11.5,"#f2c06a")+C(172,146,1.8,"#2a2a2a")+C(180,146,1.8,"#2a2a2a")+E(176,151,3,2.2,"#6a3a14"))
    s.append(Pa("M146 160 q-10 -2 -8 -14","none",'stroke="#d08a24" stroke-width="3" stroke-linecap="round"')+C(138,146,4,"#a8601e"))
    return wrap("".join(s))
M[2]=animals()

# 3 Barrel O' Slime
def slime():
    s=[S(187,50)]
    s.append(R(54,104,92,78,12,"#2a78d6",OUT("#2a78d6")))
    s.append(R(50,100,100,14,6,"#1f5fb0")+R(50,150,100,12,4,"#1f5fb0"))
    s.append(R(60,112,12,66,5,"#ffffff","opacity=\".22\""))
    s.append(Pa("M52 104 Q50 70 80 66 Q98 50 122 66 Q152 66 148 104 Q140 112 130 104 q-4 22 -12 6 q-4 -8 -8 4 q-6 18 -14 0 q-4 -10 -10 6 q-8 18 -16 0 q-3 -8 -8 -2 q-6 6 -10 -4Z","#61d836"))
    s.append(Pa("M70 82 Q84 70 100 76","none",'stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".5"'))
    s.append(C(112,78,6,"#8cf064")+C(86,90,4,"#8cf064"))
    s.append(Pa("M96 112 q-2 26 2 40","none",'stroke="#61d836" stroke-width="9" stroke-linecap="round"')+C(98,156,6.5,"#61d836"))
    return wrap("".join(s))
M[3]=slime()

# 4 Chutes & ladders
def chutes():
    s=[S(188,66)]
    s.append(R(30,26,140,140,12,"#f2c94c",OUT("#f2c94c",2)))
    cols=["#e8554e","#2a78d6","#29b36f","#f08a24"]
    for r in range(5):
        for c in range(5):
            s.append(R(38+c*25,34+r*25,23,23,4,cols[(r+c*2)%4]))
    # ladder
    s.append('<g transform="rotate(28 78 110)">'+R(66,72,6,70,2,"#8a5a2a")+R(86,72,6,70,2,"#8a5a2a")+"".join(R(66,78+i*14,26,5,2,"#b57b3a") for i in range(5))+'</g>')
    # slide
    s.append(Pa("M120 44 Q150 80 118 100 Q96 118 128 148","none",'stroke="#fff" stroke-width="13" stroke-linecap="round"')+Pa("M120 44 Q150 80 118 100 Q96 118 128 148","none",'stroke="#d6382f" stroke-width="9" stroke-linecap="round"'))
    for x,y,c in ((52,150,"#7b3fe4"),(150,58,"#ff5aa0")):
        s.append(E(x,y+9,8,3,"#000","opacity=\".25\"")+Pa(f"M{x-7} {y+8} Q{x} {y-14} {x+7} {y+8}Z",c)+C(x,y-9,5.5,c))
    return wrap("".join(s))
M[4]=chutes()

# 5 Dominoes
def pips(cx,cy,n,sz=3.3):
    pos={0:[],1:[(0,0)],2:[(-7,-7),(7,7)],3:[(-7,-7),(0,0),(7,7)],4:[(-7,-7),(7,-7),(-7,7),(7,7)],5:[(-7,-7),(7,-7),(0,0),(-7,7),(7,7)],6:[(-7,-8),(7,-8),(-7,0),(7,0),(-7,8),(7,8)]}
    return "".join(C(cx+dx,cy+dy,sz,"#fff") for dx,dy in pos[n])
def dominoes():
    s=[S(187,66)]
    def tile(cx,cy,ang,a,b):
        return (f'<g transform="rotate({ang} {cx} {cy})">'+R(cx-20,cy-38,40,76,7,"#1d2330",OUT("#1d2330"))+
                R(cx-17,cy-35,34,70,5,"#2a3142")+f'<line x1="{cx-16}" y1="{cy}" x2="{cx+16}" y2="{cy}" stroke="#e8c458" stroke-width="2"/>'+
                pips(cx,cy-19,a)+pips(cx,cy+19,b)+'</g>')
    s.append(tile(58,128,-24,6,5)); s.append(tile(142,126,22,3,2)); s.append(tile(100,110,2,6,6)); s.append(tile(100,130,0,4,1) if False else "")
    return wrap("".join(s))
M[5]=dominoes()

# 6 Colorbuds
def colorbuds():
    s=['<defs><linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7ab8"/><stop offset=".5" stop-color="#7a6bff"/><stop offset="1" stop-color="#2fd0c0"/></linearGradient></defs>',S(186,56)]
    s.append(R(50,100,100,66,30,"url(#cbg)",OUT("#7a6bff")))
    s.append(Pa("M52 128 H148","none",'stroke="#fff" stroke-width="2" opacity=".6"')+C(100,128,5,"#fff","opacity=\".9\""))
    for x,rot,c in ((64,-14,"#ff7ab8"),(136,14,"#2fd0c0")):
        s.append(f'<g transform="rotate({rot} {x} 60)">'+R(x-5,56,10,48,5,"#f4f4f6",OUT("#d0d3da",1.2))+C(x,48,19,c,OUT(c))+C(x,48,10,shade(c,1.12))+C(x-5,42,4,"#fff","opacity=\".6\"")+'</g>')
    return wrap("".join(s))
M[6]=colorbuds()

# 7 Dart gun (pistol)
def dartgun():
    s=[S(187,66)]
    s.append(R(100,92,36,64,10,"#f08a24",OUT("#f08a24")+' transform="rotate(14 118 124)"'))
    s.append(Pa("M36 70 H150 Q166 70 166 84 V108 Q166 118 156 118 H106 L98 100 H36Z","#ff9f2e",OUT("#ff9f2e")))
    s.append(R(14,76,62,24,8,"#ffd23a",OUT("#ffd23a"))+C(18,88,9,"#8a5a00")+C(18,88,5,"#2a1a00"))
    s.append(R(90,60,40,14,6,"#e87a14")+R(60,106,40,12,5,"#e87a14"))
    s.append(Pa("M104 122 q4 18 -2 28","none",'stroke="#8a4a08" stroke-width="6" stroke-linecap="round"'))
    for i,y in enumerate((150,162,174)):
        s.append(R(34+i*4,y-4,60,8,4,"#fff",OUT("#e6e6e6",1))+R(24+i*4,y-4,14,8,4,["#e8554e","#2a78d6","#29b36f"][i]))
    return wrap("".join(s))
M[7]=dartgun()

# 9 Dino egg
def dinoegg():
    s=[S(188,54)]
    s.append(Pa("M46 126 Q46 100 100 100 Q154 100 154 126 Q154 184 100 184 Q46 184 46 126Z","#7fcf6a",OUT("#7fcf6a")))
    for cx,cy,r in ((70,150,5),(120,166,5),(134,134,4.5),(90,128,4),(66,128,3.5),(110,148,4),(94,172,4)): s.append(C(cx,cy,r,"#3f9a4a","opacity=\".7\""))
    s.append(Pa("M46 126 L60 108 L74 124 L90 104 L104 122 L118 104 L132 122 L146 108 L154 126","#fff","opacity=\".0\""))
    # baby dino
    s.append(Pa("M72 112 Q70 60 100 56 Q132 54 130 112Z","#4fb35a",OUT("#4fb35a")))
    s.append(C(88,84,10,"#fff")+C(116,84,10,"#fff")+C(90,85,5,"#1c1f26")+C(114,85,5,"#1c1f26")+C(92,83,1.6,"#fff")+C(116,83,1.6,"#fff"))
    s.append(Pa("M92 102 q8 6 16 0","none",'stroke="#2a6a32" stroke-width="2.5" stroke-linecap="round"'))
    for cx in (80,100,120): s.append(Pa(f"M{cx-6} 66 L{cx} 52 L{cx+6} 66Z","#f2b632"))
    # shell crown
    s.append(Pa("M40 128 L56 108 L68 126 L82 108 L96 128 L110 108 L124 128 L138 108 L152 126 L160 128 Q160 150 150 150 H48 Q38 150 40 128Z","#7fcf6a",OUT("#7fcf6a")))
    for cx,cy,r in ((62,138,4),(108,140,4),(140,140,3.5)): s.append(C(cx,cy,r,"#3f9a4a","opacity=\".7\""))
    return wrap("".join(s))
M[9]=dinoegg()

# 10 Dinosaur figures (T-rex + stegosaurus)
def dinos():
    s=[S(188,80)]
    # stegosaurus (right, back)
    g="#f08a24"
    s.append(E(128,142,38,22,g,OUT(g)))
    for i,x in enumerate((104,118,132,146)): s.append(Pa(f"M{x-9} 126 L{x} {100-i%2*6} L{x+9} 126Z","#ffd23a",OUT("#ffd23a",1)))
    s.append(R(108,150,12,28,5,g)+R(140,150,12,28,5,g))
    s.append(Pa("M164 138 Q184 134 192 150 Q176 148 166 150Z",g)+E(88,142,16,12,g,OUT(g))+C(82,138,2.4,"#222"))
    # T-rex (left, front)
    t="#2fb7a8"
    s.append(Pa("M20 142 Q40 108 70 112 L82 138 Q60 148 40 168Z",t,OUT(t)))
    s.append(E(66,142,28,24,t,OUT(t)))
    s.append(R(54,150,14,32,6,shade(t,.92))+R(74,150,14,32,6,shade(t,.92)))
    s.append(R(52,176,22,8,4,shade(t,.7))+R(72,176,22,8,4,shade(t,.7)))
    s.append(Pa("M82 124 Q92 88 112 86 Q132 84 130 108 L104 110 Q104 126 90 136Z",t,OUT(t)))
    s.append(Pa("M104 108 H130 V114 H104Z","#fff")+C(108,94,3,"#fff")+C(109,94,1.6,"#1c1f26"))
    s.append(R(86,134,13,6,3,shade(t,.8)))
    return wrap("".join(s))
M[10]=dinos()

# 11 Etch A Sketch
def etch():
    s=[S(187,70)]
    s.append(R(28,34,144,126,12,"#e03a32",OUT("#e03a32",2)))
    s.append(R(44,50,112,80,6,"#c9ccd0",OUT("#8a8e94",2))+R(48,54,104,72,4,"#d7dadf"))
    s.append(Pa("M58 114 H80 V88 H104 V108 H124 V72 H142","none",'stroke="#33363c" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'))
    s.append(R(60,136,50,5,2,"#f2c94c","opacity=\".0\""))
    for x in (46,154): s.append(C(x,148,14,"#f5f5f5",OUT("#c5c7cc",2))+C(x,148,9,"#fff"))
    s.append(R(86,142,28,8,4,"#b82a24"))
    return wrap("".join(s))
M[11]=etch()

# 12 Foam disk launcher
def foamdisc():
    s=[S(188,66)]
    s.append(R(100,96,32,64,10,"#2a78d6",OUT("#2a78d6")+' transform="rotate(10 116 128)"'))
    s.append(R(30,66,128,42,16,"#3b8cf0",OUT("#3b8cf0")))
    s.append(R(20,76,30,22,8,"#1f5fb0")+R(130,60,34,18,7,"#ffd23a")+E(124,86,16,16,"#f08a24",OUT("#f08a24")))
    s.append(Pa("M98 108 q5 16 -2 28","none",'stroke="#16407a" stroke-width="6" stroke-linecap="round"'))
    for i,(x,y,c) in enumerate(((46,158,"#f08a24"),(88,164,"#e8554e"),(130,160,"#ffd23a"))):
        s.append(E(x,y,26,9,shade(c,.8))+E(x,y-5,26,9,c)+E(x,y-5,14,4.5,shade(c,1.15)))
    return wrap("".join(s))
M[12]=foamdisc()

# 13 Gamer headphones
def headset():
    s=[S(188,52)]
    s.append(Pa("M44 112 Q44 36 100 36 Q156 36 156 112","none",'stroke="#20242c" stroke-width="12" stroke-linecap="round"'))
    s.append(Pa("M44 112 Q44 44 100 44 Q156 44 156 112","none",'stroke="#3dff9a" stroke-width="2.5" opacity=".9"'))
    for x,r in ((40,-6),(160,6)):
        s.append(f'<g transform="rotate({r} {x} 130)">'+R(x-20,96,40,64,16,"#20242c",OUT("#20242c"))+R(x-12,106,24,44,10,"#2b303a")+C(x,128,9,"#3dff9a")+C(x,128,4,"#c8ffe4")+'</g>')
    s.append(Pa("M46 154 Q44 176 78 178","none",'stroke="#20242c" stroke-width="5" stroke-linecap="round"')+R(76,172,22,12,6,"#20242c")+C(94,178,3.5,"#3dff9a"))
    return wrap("".join(s))
M[13]=headset()

# 14 Glass marbles
def marbles():
    s=[S(186,66)]
    col=["#2a78d6","#e8554e","#29b36f","#f2b632","#7b3fe4","#ff5aa0","#2fd0c0"]
    pos=[(62,150,22),(104,156,22),(144,148,22),(84,114,22),(126,112,22),(104,74,22),(46,108,18)]
    pos=[(60,152,24),(106,160,24),(150,150,22),(82,112,24),(128,110,24),(104,66,24)]
    for (x,y,r),c in zip(pos,col):
        s.append(C(x,y,r,shade(c,.75),OUT(c,1))+C(x,y,r-3,c)+Pa(f"M{x-r+6} {y} Q{x} {y-r+6} {x+r-6} {y}","none",f'stroke="{shade(c,1.25)}" stroke-width="5" stroke-linecap="round" opacity=".7"')
                 +Pa(f"M{x-r+8} {y+4} Q{x} {y+r-4} {x+r-8} {y+4}","none",f'stroke="{shade(c,.65)}" stroke-width="3" opacity=".6"')+E(x-r*.35,y-r*.4,r*.28,r*.18,"#fff","opacity=\".85\" transform=\"rotate(-30 %s %s)\""%(x-r*.35,y-r*.4)))
    return wrap("".join(s))
M[14]=marbles()

# 15 Hot Wheels 5-pack
def car(x,y,c,sc=1):
    return (f'<g transform="translate({x} {y}) scale({sc})">'+Pa("M0 18 L4 8 Q10 0 24 0 H46 Q58 0 66 10 L78 12 Q84 14 84 20 V26 H0Z",c,OUT(c,1.2))+
            Pa("M16 10 Q22 4 30 4 H40 L40 12 H12Z","#bfe3ff")+Pa("M44 4 Q54 4 60 12 H44Z","#bfe3ff")+C(20,26,9,"#23262d")+C(20,26,4,"#c8ccd4")+C(64,26,9,"#23262d")+C(64,26,4,"#c8ccd4")+'</g>')
def hotwheels():
    s=[S(188,70)]
    s.append(R(22,40,156,132,12,"#f26a1b",OUT("#f26a1b",2))+R(30,48,140,116,8,"#ffb14a"))
    s.append(Pa("M22 130 Q70 100 178 120 V160 Q178 172 166 172 H34 Q22 172 22 160Z","#e85a10","opacity=\".35\""))
    cols=["#2a78d6","#e8554e","#29b36f","#f2c01b","#7b3fe4"]
    for i,(x,y) in enumerate(((36,62),(36,102),(36,142))): s.append(car(x,y,cols[i],.52 if False else .0) if False else "")
    pos=[(30,58),(100,58),(30,98),(100,98),(64,138)]
    for (x,y),c in zip(pos,cols): s.append(car(x,y,c,.82))
    return wrap("".join(s))
M[15]=hotwheels()

# 16 Jenga tower
def jenga():
    ex,ey,ez=(19,11),(-19,11),(0,-24)
    O=(100,104)
    def P(x,y,z): return (O[0]+x*ex[0]+y*ey[0]+z*ez[0], O[1]+x*ex[1]+y*ey[1]+z*ez[1])
    def pg(pts,fill,f): return '<polygon points="'+" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)+f'" fill="{shade(fill,f)}" stroke="{shade(fill,.55)}" stroke-width="0.8" stroke-linejoin="round"/>'
    s=[S(190,58)]
    h=0.55
    def block(x0,y0,z0,w,d,c):
        x0+=.03;y0+=.03;w-=.06;d-=.06
        t=[P(x0,y0,z0+h),P(x0+w,y0,z0+h),P(x0+w,y0+d,z0+h),P(x0,y0+d,z0+h)]
        l=[P(x0,y0+d,z0),P(x0+w,y0+d,z0),P(x0+w,y0+d,z0+h),P(x0,y0+d,z0+h)]
        r=[P(x0+w,y0,z0),P(x0+w,y0+d,z0),P(x0+w,y0+d,z0+h),P(x0+w,y0,z0+h)]
        return pg(l,c,.84)+pg(r,c,.68)+pg(t,c,1.0)
    tones=["#d9a35b","#c98f45","#e0b06a","#cf9a4f"]
    for layer in range(6):
        z=layer*h
        items=[]
        for k in range(3):
            if layer%2==0: items.append((0,k,3,1))
            else: items.append((k,0,1,3))
        items.sort(key=lambda t:t[0]+t[1])
        for n,(x0,y0,w,d) in enumerate(items):
            if layer==3 and n==1: continue
            s.append(block(x0,y0,z,w,d,tones[(layer*3+n)%4]))
    return wrap("".join(s))
M[16]=jenga()

# 17 Kids makeup kit
def makeup():
    s=[S(188,62)]
    s.append(R(34,34,132,64,10,"#f27aa6",OUT("#f27aa6")))
    s.append(R(42,42,116,48,6,"#ffd0e0")+C(100,66,13,"#fff","opacity=\".7\""))
    s.append(R(30,92,140,74,12,"#f9a1c0",OUT("#f27aa6")))
    cols=["#7b6bff","#ff7ab8","#2fd0c0","#ffd23a","#ff9a5a","#9ad84a"]
    for i,c in enumerate(cols):
        x=48+(i%3)*30; y=104+(i//3)*28
        s.append(R(x,y,24,22,5,"#fff")+R(x+2,y+2,20,18,4,c))
    s.append(R(142,100,10,32,3,"#c9285f")+R(142,92,10,10,3,"#f27aa6")+R(156,106,10,28,3,"#d63a82")+R(156,98,10,10,3,"#f27aa6"))
    s.append(Pa("M134 146 L168 120","none",'stroke="#e8c58a" stroke-width="4" stroke-linecap="round"')+E(171,117,5,8,"#ff7ab8",'transform="rotate(40 171 117)"'))
    return wrap("".join(s))
M[17]=makeup()

# 19 Magic sand
def sand():
    s=[S(188,62)]
    s.append(Pa("M36 118 Q36 76 100 74 Q164 76 164 118Z","#4fb8ff",OUT("#4fb8ff")))
    random.seed(4)
    for _ in range(46):
        x=random.randint(48,152); y=random.randint(86,116)
        if y<132: s.append(C(x,y,1.6,random.choice(["#fff","#bfe6ff","#2a78d6"]),'opacity=".7"'))
    s.append(Pa("M62 104 Q100 82 138 104","none",'stroke="#fff" stroke-width="3" opacity=".35" stroke-linecap="round"'))
    s.append(Pa("M30 112 H170 L158 172 Q156 182 144 182 H56 Q44 182 42 172Z","#ffffff",OUT("#c9ccd2",2)))
    s.append(Pa("M33 126 H167 L162 146 H38Z","#7b6bff")+R(30,106,140,12,6,"#7b6bff"))
    s.append(star(100,160,10,"#ffd23a"))
    return wrap("".join(s))
M[19]=sand()

# 20 Mini basketball hoop
def hoop():
    s=[S(188,56)]
    s.append(R(30,24,124,84,8,"#fff",OUT("#c9ccd2",3))+R(66,50,52,40,3,"none",'stroke="#e8554e" stroke-width="5"'))
    s.append(R(150,20,14,100,6,"#2a78d6")+R(120,40,34,10,4,"#2a78d6"))
    s.append(E(92,108,30,9,"none",'stroke="#f26a1b" stroke-width="5"'))
    for i in range(7):
        x=64+i*10; s.append(Pa(f"M{x} 110 L{92+(x-92)*.6:.0f} 148","none",'stroke="#8d97a8" stroke-width="2"'))
    s.append(Pa("M66 124 H118","none",'stroke="#fff" stroke-width="2"'))
    s.append(C(150,152,26,"#f08a24",OUT("#f08a24",1.4))+Pa("M124 152 H176 M150 126 V178","none",'stroke="#8a3a08" stroke-width="2"')+Pa("M132 136 Q150 152 168 136 M132 168 Q150 152 168 168","none",'stroke="#8a3a08" stroke-width="2"')+C(142,142,6,"#fff","opacity=\".25\""))
    return wrap("".join(s))
M[20]=hoop()

# 21 Mini ping pong
def pingpong():
    s=[S(188,66)]
    for x,y,rot,c in ((64,98,-22,"#e8554e"),(138,98,22,"#2a78d6")):
        s.append(f'<g transform="rotate({rot} {x} {y})">'+R(x-7,y+26,14,50,6,"#d9a35b",OUT("#d9a35b"))+C(x,y,40,c,OUT(c,1.6))+C(x,y,32,shade(c,1.1))+Pa(f"M{x-24} {y-14} Q{x} {y-30} {x+24} {y-14}","none",'stroke="#fff" stroke-width="4" opacity=".35" stroke-linecap="round"')+'</g>')
    s.append(C(100,166,12,"#fff",OUT("#d0d3da",1.4))+C(96,162,4,"#fff"))
    s.append(R(42,172,116,6,2,"#1c1f26","opacity=\".0\""))
    return wrap("".join(s))
M[21]=pingpong()

# 22 Monopoly board
def monopoly():
    s=[S(188,70)]
    s.append(R(26,26,148,148,8,"#f2efe3",OUT("#bdb9a8",2))+R(52,52,96,96,3,"#cfeadb"))
    cols=["#8a5a2a","#9ad4f2","#e86aa8","#f08a24","#e03a32","#f2d21b","#2fa84f","#2a5fd6"]
    # edges: 8 colored strips split on 4 sides (2 each)
    s.append(R(54,28,44,22,0,cols[0])+R(102,28,44,22,0,cols[1]))
    s.append(R(150,54,22,44,0,cols[2])+R(150,102,22,44,0,cols[3]))
    s.append(R(102,150,44,22,0,cols[4])+R(54,150,44,22,0,cols[5]))
    s.append(R(28,102,22,44,0,cols[6])+R(28,54,22,44,0,cols[7]))
    s.append(Pa("M58 118 L142 84","none",'stroke="#e03a32" stroke-width="16" stroke-linecap="round" opacity=".92"'))
    s.append(R(60,84,18,14,2,"#2fa84f")+Pa("M58 84 L69 74 L80 84Z","#e03a32"))
    # dice
    for x,y,rot,n in ((104,112,-14,5),(126,124,18,2)):
        s.append(f'<g transform="rotate({rot} {x} {y})">'+R(x-12,y-12,24,24,5,"#fff",OUT("#c9ccd2",1.2))+"".join(C(x+dx,y+dy,2.3,"#1c1f26") for dx,dy in ({5:[(-6,-6),(6,-6),(0,0),(-6,6),(6,6)],2:[(-5,-5),(5,5)]}[n]))+'</g>')
    # top hat token
    s.append(E(76,142,13,4.5,"#1c1f26")+R(68,122,16,20,3,"#1c1f26")+R(68,134,16,4,0,"#e03a32"))
    return wrap("".join(s))
M[22]=monopoly()

# 23 Mr Potato Head
def potato():
    s=[S(188,48)]
    s.append(E(76,178,22,9,"#f08a24",OUT("#f08a24"))+E(124,178,22,9,"#f08a24",OUT("#f08a24")))
    s.append(E(100,124,50,58,"#c98a52",OUT("#c98a52")))
    for cx,cy in ((70,150),(128,156),(80,178),(118,112),(90,94)): s.append(C(cx,cy,3,"#a8683a","opacity=\".7\""))
    s.append(E(48,118,9,14,"#f2a0b8",OUT("#f2a0b8",1))+E(152,118,9,14,"#f2a0b8",OUT("#f2a0b8",1)))
    s.append(E(84,100,12,13,"#fff",OUT("#bdbdbd",1))+E(116,100,12,13,"#fff",OUT("#bdbdbd",1))+C(86,102,6,"#2a78d6")+C(114,102,6,"#2a78d6")+C(87,103,3,"#1c1f26")+C(113,103,3,"#1c1f26"))
    s.append(E(100,122,11,9,"#f08a8a",OUT("#f08a8a",1)))
    s.append(Pa("M72 138 Q86 128 100 136 Q114 128 128 138 Q114 146 100 142 Q86 146 72 138Z","#2a1a10"))
    s.append(Pa("M84 150 Q100 162 116 150","none",'stroke="#c0392b" stroke-width="5" stroke-linecap="round"'))
    s.append(E(100,72,40,9,"#1c1f26")+Pa("M72 72 Q72 34 100 34 Q128 34 128 72Z","#1c1f26")+R(72,60,56,8,0,"#e8554e"))
    return wrap("".join(s))
M[23]=potato()

# 24 Nerf-style blaster (rifle)
def blaster():
    s=[S(188,70)]
    s.append(R(20,70,150,30,12,"#2a78d6",OUT("#2a78d6"))+R(8,74,34,22,8,"#f08a24",OUT("#f08a24"))+R(150,66,30,38,10,"#1f5fb0"))
    s.append(R(60,56,60,16,6,"#f08a24")+R(66,100,34,52,8,"#f08a24",OUT("#f08a24")))
    s.append(R(104,100,12,40,5,"#1f5fb0")+Pa("M120 102 q6 20 -2 34","none",'stroke="#16407a" stroke-width="6" stroke-linecap="round"'))
    s.append(R(78,96,22,10,3,"#ffd23a"))
    for i,y in enumerate((158,172)):
        s.append(R(40+i*14,y-5,70,10,5,"#ffd23a",OUT("#e0b01a",1))+R(30+i*14,y-5,16,10,5,"#e8554e")+R(48+i*14,y-5,52,10,0,"none",'stroke="#fff" stroke-width="0"'))
    return wrap("".join(s))
M[24]=blaster()

# 25 Play-Doh can
def dough_can(cx=100,cy=120,c="#f6c915",lid="#2a78d6",w=46,h=70,dough="#e8554e",show_dough=True):
    s=[]
    s.append(R(cx-w,cy-h/2+8,w*2,h,10,c,OUT(c,1.4)))
    s.append(E(cx,cy-h/2+8,w,w*0.34,shade(c,1.12)))
    s.append(R(cx-w+8,cy-h/2+20,10,h-26,4,"#fff","opacity=\".28\""))
    if show_dough: s.append(Pa(f"M{cx-w+8} {cy-h/2+8} Q{cx-w+4} {cy-h/2-22} {cx} {cy-h/2-24} Q{cx+w-4} {cy-h/2-22} {cx+w-8} {cy-h/2+8} Q{cx} {cy-h/2+22} {cx-w+8} {cy-h/2+8}Z",dough,OUT(dough,1.2)))
    s.append(R(cx-w-2,cy-h/2+30,w*2+4,16,3,lid))
    return "".join(s)
def playdoh_can():
    s=[S(188,52)]
    s.append(E(150,168,30,10,"#2a78d6")+E(150,162,30,10,"#4f9bf0"))
    s.append(dough_can(92,128,"#f6c915","#2a78d6",46,72,"#e8554e"))
    return wrap("".join(s))
M[25]=playdoh_can()

# 26 Play-Doh playset
def playset():
    s=[S(188,76)]
    s.append(R(22,138,156,30,8,"#ffd23a",OUT("#ffd23a"))+R(30,166,12,20,3,"#c9a010")+R(158,166,12,20,3,"#c9a010"))
    for x,c,d in ((48,"#2a78d6","#ffd23a"),(100,"#e8554e","#2fd0c0"),(152,"#29b36f","#ff7ab8")):
        s.append(dough_can(x,108,c,shade(c,.8),26,50,d))
    s.append(star(40,148,11,"#e8554e")+C(160,148,10,"#2a78d6")+Pa("M92 148 l8 -8 l8 8 l-8 8z","#29b36f"))
    return wrap("".join(s))
M[26]=playset()

# 27 Play-Doh toolkit
def toolkit():
    s=[S(188,70)]
    s.append(R(32,86,106,36,16,"#2fd0c0",OUT("#2fd0c0"))+R(138,98,32,12,6,"#d9a35b")+R(10,98,26,12,6,"#d9a35b"))
    s.append(R(48,94,70,8,4,"#fff","opacity=\".35\""))
    s.append(star(52,152,22,"#e8554e")+C(104,152,20,"#f6c915")+C(104,152,10,"#fff8d0")+R(132,136,30,30,8,"#7b6bff"))
    s.append(Pa("M40 146 L56 138 L58 150Z","none"))
    s.append(Pa("M20 44 Q46 28 74 44 Q100 22 128 44 Q148 36 170 50 Q176 70 150 74 Q100 82 50 74 Q16 70 20 44Z","#ff5aa0",OUT("#ff5aa0")))
    return wrap("".join(s))
M[27]=toolkit()

# 28 Playfoam
def playfoam():
    s=[S(188,62)]
    random.seed(7)
    cols=["#ff7ab8","#7be0b3","#7ab6ff","#ffd23a","#c9a3ff","#fff"]
    s.append(Pa("M40 96 Q100 60 160 96 L150 106 H50Z","none"))
    # foam mound
    for _ in range(120):
        x=random.randint(46,154); y=random.randint(40,112)
        if (x-100)**2/60**2+((y-110)**2)/72**2<1: s.append(C(x,y,random.choice([5,6,7]),random.choice(cols),'stroke="#e5e0f2" stroke-width=".8"'))
    s.append(Pa("M36 110 H164 L154 170 Q152 182 140 182 H60 Q48 182 46 170Z","#7b6bff",OUT("#7b6bff")))
    s.append(R(30,98,140,16,7,"#9a8cff")+R(52,128,96,34,8,"#fff","opacity=\".25\""))
    s.append(star(100,146,12,"#fff"))
    return wrap("".join(s))
M[28]=playfoam()

# 29 Plush pony
def pony():
    s=[S(188,66)]
    b="#c9a3ff"; d="#a982f0"; m="#ff7ab8"
    s.append(Pa("M158 100 Q186 100 182 150 Q176 128 156 120Z",m,OUT(m,1)))
    s.append(R(60,136,18,40,8,d)+R(82,140,18,38,8,b)+R(118,140,18,38,8,d)+R(138,136,18,40,8,b))
    for x in (60,82,118,138): s.append(R(x-1,170,20,10,5,"#7a5aa8"))
    s.append(E(106,124,56,34,b,OUT(b)))
    s.append(Pa("M62 120 Q46 80 62 52 Q84 36 100 54 Q104 90 92 120Z",b,OUT(b)))
    s.append(E(52,62,24,22,b,OUT(b))+Pa("M70 40 L76 24 L84 42Z",d)+Pa("M88 42 L96 28 L98 46Z",d))
    s.append(Pa("M82 40 Q112 40 112 80 Q100 70 92 96 Q80 72 70 90 Q66 56 82 40Z",m,OUT(m,1)))
    s.append(C(46,58,4.2,"#1c1f26")+C(47.5,56.5,1.3,"#fff")+E(38,76,4,2.5,"#8a5ac8")+Pa("M36 82 q6 4 12 0","none",'stroke="#7a4ac0" stroke-width="2" stroke-linecap="round"'))
    s.append(Pa("M104 120 l5 -8 l5 8 q-5 6 -10 0z","#ff7ab8"))
    return wrap("".join(s))
M[29]=pony()

# 31 Splash balls
def splashballs():
    s=[S(186,64)]
    cols=["#2a78d6","#e8554e","#29b36f","#f2b632","#7b3fe4"]
    pos=[(58,142,30),(116,150,32),(152,118,24),(78,92,30),(126,78,30)]
    for (x,y,r),c in zip(pos,cols):
        s.append(C(x,y,r,c,OUT(c,1.2))+C(x,y,r-5,shade(c,1.1)))
        for k in range(10):
            a=k*0.63; s.append(C(x+math.cos(a)*r*.55,y+math.sin(a)*r*.5,2.4,shade(c,.8),'opacity=".5"'))
        s.append(E(x-r*.35,y-r*.4,r*.3,r*.2,"#fff",f'opacity=".6" transform="rotate(-30 {x-r*.35} {y-r*.4})"'))
    return wrap("".join(s))
M[31]=splashballs()

# 32 Super soaker style
def soaker():
    s=[S(188,70)]
    s.append(R(40,50,92,52,22,"#7be0b3",OUT("#29b36f",2))+R(46,70,80,26,12,"#4fb8ff","opacity=\".75\"")+Pa("M52 80 Q70 70 88 80 T124 80","none",'stroke="#fff" stroke-width="2.5" opacity=".6"'))
    s.append(R(124,76,48,22,8,"#29b36f",OUT("#1f8a52"))+R(166,72,16,30,6,"#ffd23a")+R(24,84,26,20,8,"#1f8a52"))
    s.append(R(70,100,56,26,8,"#2a78d6",OUT("#2a78d6")))
    s.append(R(76,126,16,36,6,"#2a78d6")+R(104,112,10,26,5,"#16407a")+Pa("M120 108 q4 14 -2 24","none",'stroke="#ffd23a" stroke-width="5" stroke-linecap="round"'))
    s.append(R(60,142,44,18,9,"#ffd23a",OUT("#d9b020")))
    s.append(R(46,44,18,12,4,"#e8554e"))
    return wrap("".join(s))
M[32]=soaker()

# 35 Uno-style cards
def unocards():
    s=[S(188,66)]
    s.append(R(30,32,104,76,10,"#d6382f",OUT("#d6382f",2))+E(82,70,34,22,"#ffd23a",'transform="rotate(-18 82 70)"'))
    cards=[(-30,"#2a78d6","7"),(-10,"#29b36f","2"),(10,"#f2c01b","9"),(30,"#d6382f","5")]
    for ang,c,n in cards:
        s.append(f'<g transform="rotate({ang} 100 184)"><rect x="70" y="92" width="60" height="88" rx="8" fill="{c}" stroke="#fff" stroke-width="3"/>'+
                 f'<ellipse cx="100" cy="136" rx="21" ry="33" fill="#fff" transform="rotate(24 100 136)"/><text x="100" y="147" text-anchor="middle" style="font:900 32px sans-serif;fill:{c}">{n}</text>'+
                 f'<text x="79" y="108" style="font:900 12px sans-serif;fill:#fff">{n}</text></g>')
    return wrap("".join(s))
M[35]=unocards()

# ---------- Redrawn blasters (v2) ----------
def foam_dart(x,y,body="#fff",tip="#e8554e",ang=0,L=58):
    return (f'<g transform="rotate({ang} {x} {y})">'+R(x,y-4.5,L,9,4.5,body,OUT("#d9dce2",1))+R(x-8,y-5.5,16,11,5.5,tip)+R(x+L-14,y-4.5,14,9,4.5,shade(tip,.9),"opacity=\".0\"")+'</g>')

def pistol_parts(body,dark,tip,accent):
    s=[]
    # grip (behind body), leans back toward the shooter (right)
    s.append(Pa("M104 96 L142 96 L158 168 Q158 176 150 176 L128 176 Q120 176 118 168Z",dark,OUT(dark,2)))
    s.append("".join(Pa(f"M{118+i*3.2} {118+i*13} L{148+i*3.2} {118+i*13}","none",f'stroke="{shade(dark,.7)}" stroke-width="2.4" stroke-linecap="round"') for i in range(4)))
    # trigger guard + trigger
    s.append(Pa("M92 98 Q92 128 112 128 Q122 128 124 118","none",f'stroke="{dark}" stroke-width="6" stroke-linecap="round"'))
    s.append(Pa("M104 102 L110 102 L112 120 Q104 122 102 114Z",shade(dark,.65)))
    # body / slide
    s.append(R(30,62,130,40,16,body,OUT(body,2)))
    s.append(R(150,68,22,38,9,dark,OUT(dark,2)))
    s.append(R(46,54,86,12,5,accent))
    s.append(R(40,70,82,7,3.5,"#fff","opacity=\".28\""))
    s.append(R(60,82,48,6,3,shade(body,.8)))
    # muzzle tip
    s.append(R(10,68,40,28,10,tip,OUT(tip,2))+C(16,82,8.5,"#2a1a10")+C(16,82,4.5,"#000"))
    return "".join(s)

def dartgun2():
    s=[S(188,72), pistol_parts("#ff9f2e","#d9780f","#ffd23a","#e8554e")]
    s.append(foam_dart(26,150,"#ffffff","#2a78d6",-4,56)+foam_dart(36,168,"#ffffff","#29b36f",2,56))
    return wrap("".join(s))
M[7]=dartgun2()

def nerf2():
    s=[S(190,78)]
    # stock
    s.append(Pa("M150 78 L184 70 Q192 70 192 80 L190 116 Q190 124 182 122 L152 112Z","#1f5fb0",OUT("#1f5fb0",2)))
    # magazine with visible darts
    s.append(R(86,100,34,56,6,"#16407a",OUT("#16407a",1.5)))
    for i in range(4): s.append(R(92,106+i*12,22,9,4.5,"#ffd23a")+C(94,110.5+i*12,3.4,"#e8554e"))
    # grip
    s.append(Pa("M126 100 L152 100 L162 156 Q162 164 154 164 L138 164 Q130 164 128 156Z","#f08a24",OUT("#f08a24",2)))
    s.append(Pa("M118 100 Q118 128 134 128","none",'stroke="#f08a24" stroke-width="6" stroke-linecap="round"'))
    s.append(R(124,104,6,18,3,"#8a3a08"))
    # foregrip
    s.append(R(46,98,22,34,8,"#f08a24",OUT("#f08a24",1.8)))
    # body + barrel
    s.append(R(40,66,130,40,14,"#2a78d6",OUT("#2a78d6",2)))
    s.append(R(10,72,56,26,10,"#3b8cf0",OUT("#3b8cf0",2)))
    s.append(R(6,70,22,30,10,"#f08a24",OUT("#f08a24",2))+C(14,85,7.5,"#1a0e00"))
    s.append(R(70,70,70,9,4.5,"#fff","opacity=\".3\""))
    # scope/rail with red dot
    s.append(R(80,52,56,16,6,"#20242c")+C(108,60,5.5,"#ff3b30")+R(76,60,64,4,2,"#444b58"))
    s.append(R(150,72,16,10,4,"#ffd23a"))
    return wrap("".join(s))
M[24]=nerf2()

def disclauncher2():
    s=[S(190,70), pistol_parts("#3b8cf0","#1f5fb0","#f08a24","#ffd23a")]
    # transparent disc magazine on top with stacked discs
    s.append(R(76,14,50,46,8,"#cfe6ff",OUT("#7fb2ea",2))+R(80,18,42,38,6,"#e8f3ff","opacity=\".7\""))
    for i,c in enumerate(("#f08a24","#e8554e","#ffd23a","#f08a24")): s.append(E(101,50-i*9,18,5.5,shade(c,.85))+E(101,47-i*9,18,5.5,c))
    s.append(E(101,16,25,5,"#9fc8f5"))
    # loose discs
    for x,y,c in ((34,162,"#f08a24"),(70,174,"#e8554e")):
        s.append(E(x,y+4,22,8,shade(c,.8))+E(x,y,22,8,c)+E(x,y,11,4,shade(c,1.2)))
    return wrap("".join(s))
M[12]=disclauncher2()

def soaker2():
    s=[S(190,76)]
    # tank (translucent blue, with water + wave)
    s.append(R(56,28,92,58,26,"#bfe6ff",OUT("#6aaee8",2.5)))
    s.append(Pa("M62 62 Q80 54 98 62 T134 62 L142 74 Q142 82 130 82 H74 Q62 82 62 72Z","#4fb8ff"))
    s.append(R(70,36,12,32,6,"#fff","opacity=\".45\""))
    s.append(R(96,20,20,12,5,"#e8554e"))
    # barrel
    s.append(R(8,92,112,20,10,"#29b36f",OUT("#1f8a52",2))+R(2,88,28,28,9,"#ffd23a",OUT("#d9b020",2))+C(10,102,6,"#2a1a00"))
    s.append(R(30,96,70,5,2.5,"#fff","opacity=\".35\""))
    # body
    s.append(R(96,82,60,44,14,"#29b36f",OUT("#1f8a52",2))+R(104,90,44,8,4,"#fff","opacity=\".3\""))
    s.append(R(150,92,20,28,8,"#1f8a52"))
    # pump
    s.append(R(30,118,62,20,10,"#ffd23a",OUT("#d9b020",2))+"".join(R(38+i*9,121,4,14,2,"#c9a010") for i in range(6)))
    # grip + trigger guard
    s.append(Pa("M118 124 L146 124 L156 170 Q156 178 148 178 L132 178 Q124 178 122 170Z","#2a78d6",OUT("#2a78d6",2)))
    s.append(Pa("M106 124 Q106 148 124 148","none",'stroke="#2a78d6" stroke-width="6" stroke-linecap="round"')+R(112,128,6,18,3,"#16407a"))
    return wrap("".join(s))
M[32]=soaker2()

# ---------- Dinosaurs v2: T-rex (left, facing right) and stegosaurus (right, facing left), no overlap ----------
def dinos2():
    s=[S(190,86)]
    # ===== Stegosaurus (right) =====
    g="#f08a24"; gl="#ffd9a0"
    s.append(R(130,160,13,24,6,shade(g,.82))+R(176,160,13,24,6,shade(g,.82)))
    s.append(Pa("M184 136 Q198 140 200 164 Q188 156 176 154Z",g,OUT(g,1.5)))
    s.append(Pa("M196 150 l5 -9 l1 12Z","#fff3d0"))
    s.append(E(156,146,36,23,g,OUT(g,1.6)))
    s.append(E(154,156,22,10,gl,"opacity=\".75\""))
    for x,y,h in ((130,126,16),(142,118,20),(156,114,23),(170,118,20),(182,126,16)):
        s.append(Pa(f"M{x-8} {y+8} L{x} {y-h+8} L{x+8} {y+8}Z","#ffd23a",OUT("#ffd23a",1.2)))
    s.append(Pa("M126 138 Q116 150 118 164 L132 160Z",g,OUT(g,1.2)))
    s.append(E(112,158,14,9.5,g,OUT(g,1.4))+C(107,155,2.4,"#1c1f26")+Pa("M104 162 q5 3 9 0","none",'stroke="#8a3a08" stroke-width="1.8" stroke-linecap="round"'))
    s.append(R(144,162,13,22,6,g)+R(162,162,13,22,6,g))
    # ===== T-rex (left) =====
    s.append('<g transform="translate(4 186) scale(1.12) translate(-4 -186)">')
    t="#2fb7a8"; tl="#c4f0e8"
    s.append(R(54,164,14,20,6,shade(t,.78))+E(60,185,13,5,shade(t,.55)))
    s.append(Pa("M32 128 Q14 136 4 160 Q24 154 42 154Z",t,OUT(t,1.6)))
    s.append(E(52,138,24,22,t,OUT(t,1.6)))
    s.append(E(58,146,13,12,tl,"opacity=\".8\""))
    s.append(Pa("M62 124 Q64 94 82 90 L100 94 Q104 104 98 110 Q88 108 84 116 L76 136Z",t,OUT(t,1.4)))
    s.append(Pa("M84 108 Q94 112 102 106 L100 112 Q92 118 84 114Z",shade(t,.8)))
    s.append("".join(Pa(f"M{x} 107 l2.2 4.5 l2.2 -4.5Z","#fff") for x in (88,92.5,97)))
    s.append(C(88,98,3.6,"#fff")+C(89,98,1.9,"#1c1f26")+C(98,99,1.3,shade(t,.55)))
    s.append(Pa("M72 132 q9 3 11 12","none",f'stroke="{shade(t,.85)}" stroke-width="5" stroke-linecap="round"'))
    s.append(E(50,156,15,19,shade(t,.9),OUT(t,1.2))+R(43,164,13,20,6,t)+E(49,185,14,5,shade(t,.6)))
    s.append("</g>")
    return wrap("".join(s),"-2 36 212 164")
M[10]=dinos2()

ALL={**{k:v for k,v in BASE.items()},**M}
if __name__=="__main__":
    json.dump(ALL,open(sys.argv[1],"w"),separators=(",",":"))
    ids=sorted(ALL)
    # contact sheets: groups
    names={}
    import csv
    for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","public","data","products.csv"))): names[int(r["Product_ID"])]=r["Product_Name"]
    def sheet(group,path):
        h='<body style="margin:0;background:#fff;display:grid;grid-template-columns:repeat(4,250px);gap:12px;padding:12px;font:13px sans-serif">'+"".join(f'<div><div style="width:250px;height:250px;border:1px solid #eee">{ALL[k]}</div>{k} {names[k]}</div>' for k in group)+'</body>'
        open(path,"w").write(h)
    for i in range(0,len(ids),8): sheet(ids[i:i+8],sys.argv[2]+f"_{i//8}.html")
    print(len(ids),"illustrations")
