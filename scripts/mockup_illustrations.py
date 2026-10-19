import json, math

def shade(hexc, f):
    hexc=hexc.lstrip("#"); r,g,b=[int(hexc[i:i+2],16) for i in (0,2,4)]
    r,g,b=[max(0,min(255,int(c*f))) for c in (r,g,b)]
    return f"#{r:02x}{g:02x}{b:02x}"

def wrap(inner, vb="0 0 200 200"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">{inner}</svg>'

SH='<ellipse cx="100" cy="{y}" rx="{rx}" ry="{ry}" fill="#000" opacity=".13"/>'

# ---------- Teddy bear ----------
def teddy():
    br,dk,lt="#c4864a","#b0733a","#ebcfa5"
    s=[SH.format(y=184,rx=56,ry=8)]
    # legs
    for x in (74,126):
        s.append(f'<ellipse cx="{x}" cy="168" rx="19" ry="15" fill="{dk}"/><ellipse cx="{x}" cy="172" rx="10" ry="7" fill="{lt}"/>')
    s.append(f'<ellipse cx="100" cy="138" rx="42" ry="40" fill="{br}"/><ellipse cx="100" cy="144" rx="25" ry="25" fill="{lt}"/>')
    # arms
    s.append(f'<ellipse cx="60" cy="130" rx="13" ry="23" fill="{dk}" transform="rotate(25 60 130)"/><ellipse cx="140" cy="130" rx="13" ry="23" fill="{dk}" transform="rotate(-25 140 130)"/>')
    s.append(f'<circle cx="70" cy="48" r="16" fill="{dk}"/><circle cx="70" cy="48" r="9" fill="{lt}"/><circle cx="130" cy="48" r="16" fill="{dk}"/><circle cx="130" cy="48" r="9" fill="{lt}"/>')
    s.append(f'<circle cx="100" cy="82" r="40" fill="{br}"/>')
    s.append(f'<ellipse cx="100" cy="97" rx="18" ry="14" fill="{lt}"/><ellipse cx="100" cy="90" rx="6.5" ry="4.8" fill="#3b2314"/>')
    s.append('<path d="M100 95 v5 M100 100 q-6 6 -11 2 M100 100 q6 6 11 2" stroke="#3b2314" stroke-width="2" fill="none" stroke-linecap="round"/>')
    s.append('<circle cx="86" cy="74" r="4.6" fill="#2a1a10"/><circle cx="114" cy="74" r="4.6" fill="#2a1a10"/><circle cx="87.5" cy="72.5" r="1.4" fill="#fff"/><circle cx="115.5" cy="72.5" r="1.4" fill="#fff"/>')
    # bow
    s.append('<path d="M100 119 L80 108 L80 130 Z" fill="#d6382f"/><path d="M100 119 L120 108 L120 130 Z" fill="#d6382f"/><path d="M100 119 L80 108 L80 114Z" fill="#e85a4f"/><path d="M100 119 L120 108 L120 114Z" fill="#e85a4f"/><circle cx="100" cy="119" r="6" fill="#b52a22"/>')
    return wrap("".join(s))

# ---------- Rubik's-style cube ----------
def cube():
    ex,ey,ez=(21,12.2),(-21,12.2),(0,-24)
    O=(100,108)
    def P(x,y,z): return (O[0]+x*ex[0]+y*ey[0]+z*ez[0], O[1]+x*ex[1]+y*ey[1]+z*ez[1])
    col={"W":"#f4f4f2","R":"#d93a30","B":"#1f6fd1","O":"#f08a24","G":"#22a755","Y":"#f3d21b"}
    top=["Y","G","W","R","Y","B","O","W","G"]
    left=["B","B","R","W","O","G","Y","B","R"]   # face y=3 (i across, k up)
    right=["R","Y","G","O","R","W","B","Y","O"]  # face x=3 (j across, k up)
    def poly(pts,fill,f):
        d=" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)
        return f'<polygon points="{d}" fill="{shade(fill,f)}" stroke="#16181c" stroke-width="1.6" stroke-linejoin="round"/>'
    s=[SH.format(y=190,rx=64,ry=8)]
    body=[P(0,0,3),P(3,0,3),P(3,3,3),P(3,3,0),P(0,3,0),P(0,3,3)]
    s.append(poly(body,"#16181c",1))
    for i in range(3):
        for j in range(3):
            c=top[j*3+i]; s.append(poly([P(i,j,3),P(i+1,j,3),P(i+1,j+1,3),P(i,j+1,3)],col[c],1.0))
    for i in range(3):
        for k in range(3):
            c=left[(2-k)*3+i]; s.append(poly([P(i,3,k),P(i+1,3,k),P(i+1,3,k+1),P(i,3,k+1)],col[c],0.86))
    for j in range(3):
        for k in range(3):
            c=right[(2-k)*3+j]; s.append(poly([P(3,j,k),P(3,j+1,k),P(3,j+1,k+1),P(3,j,k+1)],col[c],0.72))
    return wrap("".join(s))

# ---------- Brick stack ----------
def bricks():
    ex,ey,ez=(22,12.7),(-22,12.7),(0,-24)
    O=(78,100)
    def P(x,y,z): return (O[0]+x*ex[0]+y*ey[0]+z*ez[0], O[1]+x*ex[1]+y*ey[1]+z*ez[1])
    def pp(pts,fill,f,stroke=True):
        d=" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)
        return f'<polygon points="{d}" fill="{shade(fill,f)}" stroke="{shade(fill,.6)}" stroke-width="0.8" stroke-linejoin="round"/>'
    # (color,x0,y0,z0,w,d)
    B=[("#d93a30",0,0,0,4,2),("#1f6fd1",0,0,1,3,2),("#f3c01b",0,0,2,2,2)]
    s=[SH.format(y=186,rx=62,ry=8)]
    for idx,(c,x0,y0,z0,w,d) in enumerate(B):
        h=1
        top=[P(x0,y0,z0+h),P(x0+w,y0,z0+h),P(x0+w,y0+d,z0+h),P(x0,y0+d,z0+h)]
        left=[P(x0,y0+d,z0),P(x0+w,y0+d,z0),P(x0+w,y0+d,z0+h),P(x0,y0+d,z0+h)]
        right=[P(x0+w,y0,z0),P(x0+w,y0+d,z0),P(x0+w,y0+d,z0+h),P(x0+w,y0,z0+h)]
        s.append(pp(left,c,0.82)); s.append(pp(right,c,0.66)); s.append(pp(top,c,1.0))
        above=B[idx+1] if idx+1<len(B) else None
        cells=[(i,j) for i in range(x0,x0+w) for j in range(y0,y0+d)]
        cells.sort(key=lambda t:t[0]+t[1])
        for i,j in cells:
            if above and above[1]<=i<above[1]+above[4] and above[2]<=j<above[2]+above[5]: continue
            cx,cy=P(i+.5,j+.5,z0+h)
            s.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="10.5" ry="6.2" fill="{shade(c,.7)}"/>'
                     f'<rect x="{cx-10.5:.1f}" y="{cy-7:.1f}" width="21" height="7" fill="{shade(c,.8)}"/>'
                     f'<ellipse cx="{cx:.1f}" cy="{cy-7:.1f}" rx="10.5" ry="6.2" fill="{shade(c,1.08)}"/>')
    return wrap("".join(s))

# ---------- Deck of cards (fan) ----------
HEART="M0,5 C-12,-4 -10,-14 -4,-14 C-1,-14 0,-11 0,-9 C0,-11 1,-14 4,-14 C10,-14 12,-4 0,5Z"
SPADE="M0,-14 C-12,-4 -11,4 -5,4 C-3,4 -1.5,3 -1,2 C-1,6 -2,9 -5,10 L5,10 C2,9 1,6 1,2 C1.5,3 3,4 5,4 C11,4 12,-4 0,-14Z"
DIAM="M0,-14 L9,-2 L0,10 L-9,-2Z"
def fan():
    s=[SH.format(y=186,rx=64,ry=8)]
    cards=[(-32,"#d6382f",HEART),(-16,"#1c1f26",SPADE),(0,"#d6382f",DIAM),(16,"#1c1f26",SPADE),(32,"#d6382f",HEART)]
    for ang,c,path in cards:
        s.append(f'<g transform="rotate({ang} 100 176)"><rect x="68" y="78" width="64" height="94" rx="7" fill="#fff" stroke="#c9ccd2" stroke-width="1.5"/>'
                 f'<g transform="translate(79 93) scale(.55)"><path d="{path}" fill="{c}"/></g><g transform="translate(100 125) scale(1.5)"><path d="{path}" fill="{c}"/></g></g>')
    return wrap("".join(s))

# ---------- Toy robot ----------
def robot():
    d='<defs><linearGradient id="rbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1f5fa"/><stop offset="1" stop-color="#a9b6c8"/></linearGradient><linearGradient id="rbb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f9bf0"/><stop offset="1" stop-color="#1d5fc0"/></linearGradient></defs>'
    s=[d,SH.format(y=188,rx=52,ry=7)]
    st='stroke="#7c8aa0" stroke-width="2"'
    s.append(f'<rect x="72" y="156" width="18" height="26" rx="5" fill="url(#rbb)" {st}/><rect x="110" y="156" width="18" height="26" rx="5" fill="url(#rbb)" {st}/>')
    s.append(f'<rect x="66" y="176" width="30" height="10" rx="5" fill="#2b3544"/><rect x="104" y="176" width="30" height="10" rx="5" fill="#2b3544"/>')
    s.append(f'<rect x="28" y="96" width="18" height="48" rx="8" fill="url(#rbb)" {st}/><rect x="154" y="96" width="18" height="48" rx="8" fill="url(#rbb)" {st}/>')
    s.append('<circle cx="37" cy="148" r="9" fill="#d6dde8" stroke="#7c8aa0" stroke-width="2"/><circle cx="163" cy="148" r="9" fill="#d6dde8" stroke="#7c8aa0" stroke-width="2"/>')
    s.append(f'<rect x="50" y="92" width="100" height="70" rx="12" fill="url(#rbg)" {st}/>')
    s.append('<rect x="64" y="104" width="72" height="40" rx="8" fill="#243044"/><rect x="70" y="110" width="26" height="8" rx="3" fill="#3cd3ff"/><rect x="70" y="124" width="14" height="14" rx="3" fill="#ff5a4f"/><rect x="88" y="124" width="14" height="14" rx="3" fill="#ffd34d"/><circle cx="116" cy="131" r="7" fill="#3ddc97"/><rect x="104" y="110" width="26" height="8" rx="3" fill="#59657a"/>')
    s.append('<rect x="92" y="82" width="16" height="12" fill="#8793a5"/>')
    s.append(f'<rect x="64" y="34" width="72" height="52" rx="14" fill="url(#rbg)" {st}/>')
    s.append('<rect x="72" y="44" width="56" height="26" rx="10" fill="#243044"/><circle cx="87" cy="57" r="7" fill="#3cd3ff"/><circle cx="113" cy="57" r="7" fill="#3cd3ff"/><circle cx="89" cy="55" r="2.2" fill="#fff"/><circle cx="115" cy="55" r="2.2" fill="#fff"/>')
    s.append('<rect x="82" y="74" width="36" height="7" rx="3" fill="#59657a"/><path d="M89 74v7M96 74v7M104 74v7M111 74v7" stroke="#cfd6e2" stroke-width="1.5"/>')
    s.append('<line x1="100" y1="34" x2="100" y2="18" stroke="#7c8aa0" stroke-width="3"/><circle cx="100" cy="15" r="6" fill="#ff5a4f" stroke="#b83a31" stroke-width="1.5"/>')
    s.append('<rect x="56" y="52" width="8" height="18" rx="3" fill="#4f9bf0"/><rect x="136" y="52" width="8" height="18" rx="3" fill="#4f9bf0"/>')
    return wrap("".join(s))

ILLUS={8:fan(),18:bricks(),30:cube(),33:teddy(),34:robot()}
if __name__=="__main__":
    import sys
    json.dump(ILLUS,open(sys.argv[1],"w"),separators=(",",":"))
    # contact sheet for visual QA
    h='<body style="margin:0;background:#fff;display:grid;grid-template-columns:repeat(5,240px);gap:14px;padding:14px;font:12px sans-serif">'+"".join(f'<div><div style="width:240px;height:240px;background:#fff;border:1px solid #eee">{v}</div>{k}</div>' for k,v in ILLUS.items())+'</body>'
    open(sys.argv[2],"w").write(h)
