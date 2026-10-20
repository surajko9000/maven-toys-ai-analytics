/* Data and constants: the compact dataset, toy drawings, lookups, number formatting. */
const DATA = __DATA__;
const MN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const mlabel = i => `${MN[i%12]} ${String(2022+Math.floor(i/12)).slice(2)}`;
const mlong = i => `${MN[i%12]} ${2022+Math.floor(i/12)}`;
const CATS = ["Toys","Art & Crafts","Games","Sports & Outdoors","Electronics"];
const CCOL = {"Toys":"var(--s1)","Art & Crafts":"var(--s2)","Games":"var(--s3)","Sports & Outdoors":"var(--s4)","Electronics":"var(--s5)"};
const CTINT = {"Toys":"#e3eefb","Art & Crafts":"#fdebe3","Games":"#def5ec","Sports & Outdoors":"#fcf0d2","Electronics":"#fbe6ee"};
const EMOJI = {1:"🦸",2:"🦁",3:"🧪",4:"🪜",5:"🎲",6:"🎧",7:"🎯",8:"🃏",9:"🥚",10:"🦖",11:"✏️",12:"🥏",13:"🎧",14:"🔮",15:"🏎️",16:"🧱",17:"💄",18:"🧱",19:"⏳",20:"🏀",21:"🏓",22:"🎩",23:"🥔",24:"🔫",25:"🎨",26:"🎨",27:"🛠️",28:"☁️",29:"🐴",30:"🧩",31:"💦",32:"💧",33:"🧸",34:"🤖",35:"🃏"};
/* Real photos go here once image sources are reachable. Shape: {pid:{src,credit,license,url}}. Anything missing falls back to the emoji tile. */
const IMG = {};
/* Original illustrations drawn for this project (not photos). Shape: {pid: svgString}. */
const ILLUS = __ILLUS__;
const P = Object.fromEntries(DATA.P.map(p=>[p.id,p]));
const ST = Object.fromEntries(DATA.ST.map(s=>[s.id,s]));
const PSORT = [...DATA.P].sort((a,b)=>a.name.localeCompare(b.name));
const INV = {}; for(const p of DATA.P) INV[p.id]={stock:0,stocked:0,zero:0,zeroStores:[]};
for(const [sid,pid,q] of DATA.INVS){const r=INV[pid];r.stock+=q;r.stocked++;if(q==0){r.zero++;r.zeroStores.push(sid)}}
const fmt$ = v => Math.abs(v)>=1e6?`$${(v/1e6).toFixed(2)}M`:Math.abs(v)>=1e3?`$${(v/1e3).toFixed(0)}K`:`$${v.toFixed(0)}`;
const fmt$f = v => "$"+Math.round(v).toLocaleString();
const fmtN = v => Math.round(v).toLocaleString();
const pct = v => (v*100).toFixed(1)+"%";
const rev = (pid,u)=>u*P[pid].price, gp=(pid,u)=>u*(P[pid].price-P[pid].cost);
const esc = s => String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

