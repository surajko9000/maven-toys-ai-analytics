/* Tooltip and plain-SVG chart helpers (bars and line). */
/* ---------- tooltip ---------- */
const tip=document.getElementById("tip");
document.addEventListener("mousemove",e=>{const t=e.target.closest("[data-tip]");
  if(t){tip.innerHTML=t.dataset.tip;tip.style.opacity=1;tip.style.left=Math.min(e.clientX+14,innerWidth-tip.offsetWidth-8)+"px";tip.style.top=(e.clientY+14)+"px"}else tip.style.opacity=0});

/* ---------- chart helpers (plain SVG) ---------- */
function hbars(rows,{w=520,color="var(--s1)",fmt=fmt$,label=r=>r.label,rowH=26,vw=70}={}){
  if(!rows.length) return `<div class="note">No data for this selection.</div>`;
  const max=Math.max(...rows.map(r=>r.v),1e-9),lw=150,h=rows.length*rowH+6;
  return `<svg viewBox="0 0 ${w} ${h}" width="100%">`+rows.map((r,i)=>{
    const y=i*rowH+3,bw=Math.max(2,(w-lw-vw)*Math.max(r.v,0)/max),L=label(r);
    return `<g data-tip="${esc(r.tip??L+": "+fmt(r.v))}"><text x="${lw-8}" y="${y+14}" text-anchor="end">${esc(L.length>24?L.slice(0,23)+"…":L)}</text>
    <rect x="${lw}" y="${y+3}" width="${bw}" height="${rowH-10}" rx="5" fill="${r.color??color}"/>
    <text x="${lw+bw+6}" y="${y+14}" style="fill:var(--ink)">${r.vtext??fmt(r.v)}</text></g>`}).join("")+`</svg>`;
}
function line(vals,{w=640,h=240,color="var(--s1)",fmt=fmt$,labels=mlabel}={}){
  const L=46,R=12,T=10,B=26,hi=(Math.max(...vals,0)*1.1)||1e-9,lo=Math.min(...vals,0)*1.1,n=Math.max(vals.length-1,1),x=i=>L+(w-L-R)*i/n,y=v=>T+(h-T-B)*(1-(v-lo)/(hi-lo));
  const ticks=[0,.25,.5,.75,1].map(t=>lo+t*(hi-lo));
  const path=vals.map((v,i)=>`${i?"L":"M"}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join("");
  const area=path+`L${x(vals.length-1)},${y(0)}L${x(0)},${y(0)}Z`;
  const step=Math.ceil(vals.length/7);
  return `<svg viewBox="0 0 ${w} ${h}" width="100%">`+
   ticks.map(t=>`<line x1="${L}" x2="${w-R}" y1="${y(t)}" y2="${y(t)}" stroke="var(--grid)"/><text x="${L-6}" y="${y(t)+4}" text-anchor="end">${fmt(t)}</text>`).join("")+
   `<line x1="${L}" x2="${w-R}" y1="${y(0)}" y2="${y(0)}" stroke="#d9cfb2" stroke-width="1.5"/><path d="${area}" fill="${color}" opacity=".10"/><path d="${path}" fill="none" stroke="${color}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>`+
   vals.map((v,i)=>`<g data-tip="<b>${labels(i)}</b><br>${fmt(v)}"><rect x="${x(i)-((w-L-R)/n)/2}" y="${T}" width="${(w-L-R)/n}" height="${h-T-B}" fill="transparent"/><circle cx="${x(i)}" cy="${y(v)}" r="3.5" fill="${color}" stroke="#fff" stroke-width="2"/></g>`).join("")+
   vals.map((v,i)=>i%step==0?`<text x="${x(i)}" y="${h-8}" text-anchor="middle">${labels(i)}</text>`:"").join("")+`</svg>`;
}
function csvDownload(name,rows){const csv=rows.map(r=>r.map(c=>`"${String(c).replace(/"/g,'""')}"`).join(",")).join("\n");
  const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv"}));a.download=name;a.click()}
function imgBlock(pid,cls){const i=IMG[pid];
  if(i) return `<img src="${i.src}" alt="${esc(P[pid].name)}" loading="lazy" onerror="this.parentNode.innerHTML=EMOJI[${pid}]">`;
  if(ILLUS[pid]) return `<span class="art">${ILLUS[pid]}</span>`;
  return EMOJI[pid]}
const TILE_OVERRIDE={}; /* white products get a soft tint so they stand out */
const STRONG={"Toys":"#e6effb","Art & Crafts":"#fdeee6","Games":"#e3f6ee","Sports & Outdoors":"#fcf5df","Electronics":"#fbebf2"};
const tileBg=pid=>TILE_OVERRIDE[pid]||STRONG[P[pid].cat];

