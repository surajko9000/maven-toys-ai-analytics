/* Toy Finder tab: catalog, filters, toy detail panel. */
/* ================= TAB 3: TOY FINDER ================= */
const toys={fopen:false,q:"",cat:"All",sort:"gp",dir:-1,m0:0,m1:20,preset:"all"};
function toysReset(){Object.assign(toys,{q:"",cat:"All",sort:"gp",dir:-1,m0:0,m1:20,preset:"all"});renderToys()}
function toyPreset(k){const p=PRESETS.find(x=>x[0]==k);toys.preset=k;toys.m0=p[2];toys.m1=p[3];renderToys()}
function toyRange(w,v){v=+v;if(w=="m0"){toys.m0=v;if(toys.m1<v)toys.m1=v}else{toys.m1=v;if(toys.m0>v)toys.m0=v}toys.preset=(PRESETS.find(x=>x[2]==toys.m0&&x[3]==toys.m1)||[null])[0];renderToys()}
const SORTS={gp:"Profit",rev:"Revenue",units:"Units sold",price:"Price",name:"Name"};
const dirWord=(k,d)=>k=="name"?(d>0?"A → Z":"Z → A"):(d<0?"Highest first":"Lowest first");
function setSort(k){if(toys.sort==k)toys.dir*=-1;else{toys.sort=k;toys.dir=k=="name"?1:-1}renderToys()}
function renderToys(){
  const val=p=>toys.sort=="name"?p.p.name:toys.sort=="price"?p.p.price:p[toys.sort];
  const R=agg({m0:toys.m0,m1:toys.m1}),Z={rev:0,gp:0,units:0};
  const mopts=sel=>Array.from({length:21},(_,i)=>`<option value="${i}" ${i==sel?"selected":""}>${mlong(i)}</option>`).join("");
  const ttl=(PRESETS.find(x=>x[0]==toys.preset)||[0,`${mlong(toys.m0)} – ${mlong(toys.m1)}`])[1];
  const tSum=sc("📅 "+ttl,toys.preset!="all")+sc("🏷️ "+toys.cat,toys.cat!="All")+sc("↕️ "+SORTS[toys.sort]+" · "+dirWord(toys.sort,toys.dir),toys.sort!="gp"||toys.dir!=-1)+(toys.q?sc("🔎 “"+esc(toys.q)+"”",true):"");
  const tDirty=toys.preset!="all"||toys.cat!="All"||toys.sort!="gp"||toys.dir!=-1||!!toys.q;
  const list=DATA.P.filter(p=>(toys.cat=="All"||p.cat==toys.cat)&&p.name.toLowerCase().includes(toys.q.toLowerCase()))
    .map(p=>({p,...(R.byProd[p.id]||Z)})).sort((a,b)=>{const x=val(a),y=val(b);return (typeof x=="string"?x.localeCompare(y):x-y)*toys.dir});
  document.getElementById("toys").innerHTML=`<h1><span class="h1t">${ILLUS[33]}</span>Toy Catalog: How Every Toy Performs</h1><p class="sub">Browse the catalog and tap any toy to see how it performs. <span class="tag">Toy art is original illustration, not product photos.</span></p>
  ${fbar("toys",toys.fopen,tSum,`<div class="fgroup"><span class="lbl">📅 Time</span>
    ${PRESETS.map(([k,l])=>`<button class="chip ${toys.preset==k?"on":""}" onclick="toyPreset('${k}')">${l}</button>`).join("")}
    <span style="color:var(--ink3)">or</span>
    <select onchange="toyRange('m0',this.value)">${mopts(toys.m0)}</select> to <select onchange="toyRange('m1',this.value)">${mopts(toys.m1)}</select></div>
  <div class="fgroup"><span class="lbl">🔎 Find</span><input type="search" id="toyq" placeholder="Search toys…" value="${esc(toys.q)}" oninput="toys.q=this.value;renderToys();const i=document.getElementById('toyq');i.focus();i.setSelectionRange(99,99)">
   <span class="lbl" style="margin-left:8px">🏷️ Category</span>${["All",...CATS].map(c=>`<button class="chip ${toys.cat==c?"on":""}" onclick="toys.cat='${c}';renderToys()">${c}</button>`).join("")}</div>
  <div class="fgroup"><span class="lbl">↕️ Sort by</span><span class="seg">${Object.entries(SORTS).map(([k,l])=>`<button class="${toys.sort==k?"on":""}" onclick="toys.sort='${k}';toys.dir=${k=="name"?1:-1};renderToys()">${l}</button>`).join("")}</span>
   <button class="dir" onclick="toys.dir*=-1;renderToys()" title="Flip the order">⇅ ${dirWord(toys.sort,toys.dir)}</button></div>`,tDirty)}
  <p class="cap">${mlong(toys.m0)} – ${mlong(toys.m1)}: <b>${list.length}</b> toy${list.length==1?"":"s"}, sorted by <b>${SORTS[toys.sort].toLowerCase()}</b>, <b>${dirWord(toys.sort,toys.dir).toLowerCase()}</b>.</p>
  ${list.length?`<div class="cards">${list.map(({p,rev,gp,units},i)=>`<div class="toy ${units?"":"off"}" style="--cc:${CCOL[p.cat]}" onclick="openToy(${p.id})"><div class="img" style="background:${tileBg(p.id)}"><span class="rank ${i<3?"r"+(i+1):""}">#${i+1}</span>${INV[p.id].zero>=8?`<span class="oos">Out in ${INV[p.id].zero} stores</span>`:""}${imgBlock(p.id)}</div>
   <div class="b"><div class="n">${p.name}</div><div class="c"><i></i>${p.cat} · $${p.price.toFixed(2)}</div>
   ${units?`<div class="m"><span>Units<b>${fmtN(units)}</b></span><span>Profit<b>${fmt$(gp)}</b></span></div>`:`<div class="na">No sales in this window</div>`}</div></div>`).join("")}</div>`:`<div class="card">No toys match “${esc(toys.q)}”. Try a different search or category.</div>`}`;
}
function openToy(id){
  const p=P[id],R=agg({m0:toys.m0,m1:toys.m1}),b=R.byProd[id]||{rev:0,gp:0,units:0},iv=INV[id],ms=ALL_BY_PROD_MONTH(id);
  const A=agg({pid:id,m0:toys.m0,m1:toys.m1});
  const stores=Object.entries(A.byStore).map(([sid,s])=>({label:ST[sid].city+" #"+ST[sid].name.split(" ").pop(),v:s.rev})).sort((a,b)=>b.v-a.v).slice(0,6);
  const rankP=DATA.P.map(q=>[q.id,(R.byProd[q.id]||{gp:0}).gp]).sort((a,b)=>b[1]-a[1]).findIndex(([k])=>k==id)+1;
  const im=IMG[id];
  document.getElementById("panel").innerHTML=`<div style="display:flex;justify-content:space-between"><span class="tag">${p.cat}</span><button class="btn" onclick="closeToy()">✕ Close</button></div>
  <div class="hero-img" style="background:${tileBg(id)};margin-top:10px;border:2px solid var(--line)">${imgBlock(id)}</div>${im?`<div class="credit">Photo: ${esc(im.credit)} · ${esc(im.license)}</div>`:(ILLUS[id]?`<div class="credit">Original illustration, not a product photo.</div>`:`<div class="credit">Placeholder icon, not a product photo.</div>`)}
  <h2 style="margin:0;font-size:26px">${p.name}</h2>
  <div class="sub" style="margin:2px 0 0">Price $${p.price.toFixed(2)} · Cost $${p.cost.toFixed(2)} · Unit margin ${pct((p.price-p.cost)/p.price)}</div>
  <div class="stats"><div class="stat"><div class="l">Units sold</div><div class="v">${fmtN(b.units)}</div></div><div class="stat"><div class="l">Revenue</div><div class="v">${fmt$(b.rev)}</div></div><div class="stat"><div class="l">Est. profit</div><div class="v">${fmt$(b.gp)}</div></div></div>
  <div class="cap">🏆 Ranks <b>#${rankP}</b> of 35 by estimated profit, ${mlong(toys.m0)} – ${mlong(toys.m1)}.</div>
  <div class="card" style="margin:12px 0"><h3>Monthly revenue</h3>${line(ms,{w:500,h:170})}</div>
  <div class="card" style="margin:12px 0"><h3>Top stores</h3><div class="note">By revenue, ${mlong(toys.m0)} – ${mlong(toys.m1)}</div>${hbars(stores,{w:500})}</div>
  <div class="card" style="margin:12px 0"><h3>📦 Stock on hand (current snapshot)</h3><div class="note">One undated snapshot, not a history</div>
  ${iv.stocked?`<b style="font-size:22px">${fmtN(iv.stock)}</b> units across ${iv.stocked} of 50 stores<br><b>${iv.zero}</b> store${iv.zero==1?"":"s"} at zero stock${iv.zero?`: ${iv.zeroStores.slice(0,6).map(s=>ST[s].city).join(", ")}${iv.zero>6?`, +${iv.zero-6} more`:""}`:""}`:"No inventory rows for this toy."}</div>
  <div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn pri" onclick="closeToy();show('ask');ask('Which stores sell the most ${p.name}?',true)">💬 Ask about this toy</button>
  <a class="btn" style="text-decoration:none" target="_blank" rel="noopener" href="https://www.google.com/search?q=${encodeURIComponent(p.name+" toy")}">🔎 Search the web for it ↗</a></div>
  <div class="credit" style="margin-top:8px">The web link is a plain search, not an official product page.</div>`;
  document.getElementById("drawer").classList.add("on");
}
function ALL_BY_PROD_MONTH(id){return agg({pid:id}).byMonth.map(b=>b.rev)}
function closeToy(){document.getElementById("drawer").classList.remove("on")}
document.getElementById("drawer").addEventListener("click",e=>{if(e.target.id=="drawer")closeToy()});

