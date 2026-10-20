/* Dashboard tab: filters, KPIs, charts, table. */
/* ================= TAB 1: DASHBOARD ================= */
const dash={fopen:false,cats:new Set(CATS),pid:null,m0:0,m1:20,preset:"all",metric:"rev",trend:"values",show:"val",sort:{k:"gp",d:-1}};
const MET={rev:{n:"Revenue",f:fmt$},gp:{n:"Est. gross profit",f:fmt$},units:{n:"Units sold",f:fmtN},mg:{n:"Gross margin %",f:v=>pct(v)}};
const val=(b,m)=>m=="mg"?(b.rev?b.gp/b.rev:0):b[m];
const shr=(x,t)=>t?pct(x/t):"–";
const PRESETS=[["all","All time",0,20],["2022","2022",0,11],["2023","2023 so far",12,20],["l3","Last 3 months",18,20],["l6","Last 6 months",15,20]];
function setPreset(k){const p=PRESETS.find(x=>x[0]==k);dash.preset=k;dash.m0=p[2];dash.m1=p[3];renderDash()}
function setRange(which,v){v=+v;if(which=="m0"){dash.m0=v;if(dash.m1<v)dash.m1=v}else{dash.m1=v;if(dash.m0>v)dash.m0=v}
  dash.preset=(PRESETS.find(x=>x[2]==dash.m0&&x[3]==dash.m1)||[null])[0];renderDash()}
function fbar(key,open,sum,inner,reset){const re=key=="dash"?"renderDash":"renderToys";
  return `<div class="fbar"><button class="fhead" onclick="${key}.fopen=!${key}.fopen;${re}()" aria-expanded="${!!open}"><span class="fsum">${sum}</span>${reset?`<span class="freset" onclick="event.stopPropagation();${key}Reset()">Reset</span>`:""}<span class="fch">${open?"Hide ▴":"Filters ▾"}</span></button>${open?`<div class="fbody">${inner}<button class="btn fdone" onclick="${key}.fopen=false;${re}()">Done</button></div>`:""}</div>`}
const sc=(l,on)=>`<span class="sc ${on?"on":""}">${l}</span>`;
function dashReset(){Object.assign(dash,{cats:new Set(CATS),pid:null,m0:0,m1:20,preset:"all",metric:"rev",show:"val"});renderDash()}
function renderDash(){
  const cats=dash.cats.size<5?[...dash.cats]:null;const m=dash.metric;
  const A=agg({cats,pid:dash.pid,m0:dash.m0,m1:dash.m1});
  const len=dash.m1-dash.m0+1, hasPrev=dash.m0-len>=0;
  const B=hasPrev?agg({cats,pid:dash.pid,m0:dash.m0-len,m1:dash.m0-1}):null;
  const delta=(a,b)=>{if(!B||!b)return null;const d=a/b-1;return `<span class="${d>=0?"up":"down"}">${d>=0?"▲":"▼"} ${Math.abs(d*100).toFixed(1)}%</span> vs prior ${len} mo`};
  const mg=A.tot.rev?A.tot.gp/A.tot.rev:0, mgB=B&&B.tot.rev?B.tot.gp/B.tot.rev:null;
  const mgd=mgB==null?null:`<span class="${mg>=mgB?"up":"down"}">${mg>=mgB?"▲":"▼"} ${Math.abs((mg-mgB)*100).toFixed(1)} pts</span> vs prior ${len} mo`;
  const nprod=Object.keys(A.byProd).length;
  const T=m=="mg"?null:A.tot[m];
  const vt=b=>m=="mg"?pct(val(b,m)):dash.show=="pct"?shr(b[m],T):MET[m].f(b[m]);
  const tipFor=(name,b)=>`<b>${name}</b><br>Revenue ${fmt$(b.rev)} · ${shr(b.rev,A.tot.rev)} of selection<br>Est. profit ${fmt$(b.gp)} · ${shr(b.gp,A.tot.gp)}<br>Units ${fmtN(b.units)} · ${shr(b.units,A.tot.units)}<br>Margin ${pct(b.rev?b.gp/b.rev:0)}`;
  const catRows=CATS.filter(c=>A.byCat[c]).sort((a,b)=>val(A.byCat[b],m)-val(A.byCat[a],m)).map(c=>({label:c,v:val(A.byCat[c],m),vtext:vt(A.byCat[c]),color:CCOL[c],tip:tipFor(c,A.byCat[c])}));
  const top=Object.entries(A.byProd).sort((a,b)=>val(b[1],m)-val(a[1],m)).slice(0,10).map(([pid,b])=>({label:P[pid].name,v:val(b,m),vtext:vt(b),color:CCOL[P[pid].cat],tip:tipFor(`${P[pid].name} · ${P[pid].cat}`,b)}));
  const stores=Object.entries(A.byStore).sort((a,b)=>val(b[1],m)-val(a[1],m)).slice(0,8).map(([sid,b])=>({label:`${ST[sid].city} #${ST[sid].name.split(" ").pop()}`,v:val(b,m),vtext:vt(b),tip:tipFor(`${ST[sid].name} (${ST[sid].loc})`,b)}));
  const shareNote=m=="mg"?"Hover a bar for the revenue behind each margin":dash.show=="pct"?"Labels = % share of the current selection":"Hover a bar for share, profit and units";
  const ser=A.byMonth.slice(dash.m0,dash.m1+1).map(b=>val(b,m));
  const asPct=dash.trend=="pct"&&ser.length>1;
  let tvals=ser,tfmt=MET[m].f,tlabels=i=>mlabel(i+dash.m0);
  if(asPct){tvals=ser.slice(1).map((v,i)=>m=="mg"?(v-ser[i])*100:(ser[i]?(v/ser[i]-1)*100:0));
    tfmt=m=="mg"?(v=>(v>=0?"+":"")+v.toFixed(1)+" pts"):(v=>(v>=0?"+":"")+v.toFixed(0)+"%");tlabels=i=>mlabel(i+1+dash.m0)}
  const rows=Object.entries(A.byProd).map(([pid,b])=>({pid,name:P[pid].name,cat:P[pid].cat,units:b.units,rev:b.rev,gp:b.gp,mg:b.rev?b.gp/b.rev:0,shRev:A.tot.rev?b.rev/A.tot.rev:0,shGp:A.tot.gp?b.gp/A.tot.gp:0}));
  rows.sort((a,b)=>(a[dash.sort.k]>b[dash.sort.k]?1:-1)*dash.sort.d);
  const th=(k,l,r)=>`<th class="${r?"r":""}" onclick="dash.sort={k:'${k}',d:dash.sort.k=='${k}'?-dash.sort.d:-1};renderDash()">${l}${dash.sort.k==k?(dash.sort.d<0?" ↓":" ↑"):""}</th>`;
  const mopts=(sel)=>Array.from({length:21},(_,i)=>`<option value="${i}" ${i==sel?"selected":""}>${mlong(i)}</option>`).join("");
  const tl=(PRESETS.find(x=>x[0]==dash.preset)||[0,`${mlong(dash.m0)} – ${mlong(dash.m1)}`])[1];
  const dashSum=sc("📅 "+tl,dash.preset!="all")+sc("🏷️ "+(cats?cats.join(", "):"All categories"),!!cats)+sc("🧸 "+(dash.pid?P[dash.pid].name:"All toys"),!!dash.pid)+sc("📐 "+MET[m].n+(m!="mg"&&dash.show=="pct"?" · % share":""),m!="rev"||dash.show!="val");
  const dashDirty=dash.preset!="all"||!!cats||!!dash.pid||m!="rev"||dash.show!="val";
  document.getElementById("dashboard").innerHTML=`
  <h1><span class="h1t">${ILLUS[30]}</span>Sales Performance Dashboard</h1><p class="sub">Revenue, profit and units across 50 stores and 35 toys, Jan 2022 – Sep 2023. Click the filter bar to change the time window, category, toy or measure.</p>
  ${fbar("dash",dash.fopen,dashSum,`<div class="fgroup"><span class="lbl">📅 Time</span>
    ${PRESETS.map(([k,l])=>`<button class="chip ${dash.preset==k?"on":""}" onclick="setPreset('${k}')">${l}</button>`).join("")}
    <span style="color:var(--ink3)">or</span>
    <select onchange="setRange('m0',this.value)">${mopts(dash.m0)}</select> to <select onchange="setRange('m1',this.value)">${mopts(dash.m1)}</select></div>
  <div class="fgroup"><span class="lbl">🏷️ Category</span>
    ${CATS.map(c=>`<button class="chip ${dash.cats.size<5&&dash.cats.has(c)?"on":""}" onclick="toggleCat('${c}')"><i style="background:${CCOL[c]}"></i>${c}</button>`).join("")}
    <span class="lbl" style="margin-left:10px">🧸 Toy</span>
    <div class="combo" id="combo"><input type="text" id="prodin" placeholder="All toys (type to search)" autocomplete="off" value="${dash.pid?esc(P[dash.pid].name):""}" onfocus="comboOpen()" oninput="comboOpen(this.value)" onkeydown="comboKey(event)">
      ${dash.pid?`<span class="x" onclick="comboPick(0)" title="Clear">✕</span>`:""}<div class="list" id="combolist"></div></div></div>
  <div class="fgroup"><span class="lbl">📐 Chart measure</span><span class="seg">${Object.entries(MET).map(([k,v])=>`<button class="${m==k?"on":""}" onclick="dash.metric='${k}';renderDash()">${v.n}</button>`).join("")}</span></div>
  <div class="fgroup"><span class="lbl">🔢 Bar labels</span><span class="seg">${m=="mg"?`<button class="on" disabled>Margin %</button>`:`<button class="${dash.show=="val"?"on":""}" onclick="dash.show='val';renderDash()">Value</button><button class="${dash.show=="pct"?"on":""}" onclick="dash.show='pct';renderDash()">% of selection</button>`}</span></div>`,dashDirty)}
  <div class="kpis">
    <div class="kpi" style="background:#e3eefb"><div class="e">💰</div><div class="l">Revenue</div><div class="v">${fmt$(A.tot.rev)}</div><div class="d">${delta(A.tot.rev,B?.tot.rev)??"units × price"}</div></div>
    <div class="kpi" style="background:#def5ec"><div class="e">🪙</div><div class="l">Est. gross profit</div><div class="v">${fmt$(A.tot.gp)}</div><div class="d">${delta(A.tot.gp,B?.tot.gp)??"units × (price − cost)"}</div></div>
    <div class="kpi" style="background:#fcf0d2"><div class="e">📈</div><div class="l">Gross margin</div><div class="v">${A.tot.rev?pct(mg):"–"}</div><div class="d">${mgd??"profit ÷ revenue"}</div></div>
    <div class="kpi" style="background:#fbe6ee"><div class="e">📦</div><div class="l">Units sold</div><div class="v">${fmtN(A.tot.units)}</div><div class="d">${delta(A.tot.units,B?.tot.units)??"transaction units"}</div></div>
    <div class="kpi" style="background:#ece8fb"><div class="e">🏬</div><div class="l">Stores</div><div class="v">${Object.keys(A.byStore).length}</div><div class="d">with sales</div></div>
    <div class="kpi" style="background:#fdebe3"><div class="e">🧸</div><div class="l">Toys sold</div><div class="v">${nprod}</div><div class="d">of 35</div></div>
  </div>
  <div class="grid2">
    <div class="card"><div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px"><div><h3>${MET[m].n} by month${asPct?" (change vs prior month)":""}</h3><div class="note">Hover a dot for the value</div></div>
      <span class="seg"><button class="${asPct?"":"on"}" onclick="dash.trend='values';renderDash()">Values</button><button class="${asPct?"on":""}" onclick="dash.trend='pct';renderDash()">% change</button></span></div>${line(tvals,{fmt:tfmt,labels:tlabels})}</div>
    <div class="card"><h3>${MET[m].n} by category</h3><div class="note">Colors match the category buttons · ${shareNote}</div>${hbars(catRows,{fmt:MET[m].f,vw:80})}</div>
  </div>
  <div class="grid3">
    <div class="card"><h3>Top 10 toys by ${MET[m].n.toLowerCase()}</h3><div class="note">Bar color = category · ${shareNote}</div>${hbars(top,{fmt:MET[m].f,vw:80})}</div>
    <div class="card"><h3>Top 8 stores by ${MET[m].n.toLowerCase()}</h3><div class="note">Same time window and filters · ${shareNote}</div>${hbars(stores,{fmt:MET[m].f,vw:80})}</div>
  </div>
  <div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><div><h3>All toys in this view</h3><div class="note">Click a column to sort</div></div>
    <button class="btn" onclick="csvDownload('toys_filtered.csv',[['Toy','Category','Units','Revenue','% of revenue','Est gross profit','% of profit','Margin'],...dashRows.map(r=>[r.name,r.cat,r.units,r.rev.toFixed(2),(r.shRev*100).toFixed(1)+'%',r.gp.toFixed(2),(r.shGp*100).toFixed(1)+'%',(r.mg*100).toFixed(1)+'%'])])">⬇ Export CSV</button></div>
    ${rows.length?`<div style="max-height:340px;overflow:auto"><table class="tbl"><tr>${th("name","Toy")}${th("cat","Category")}${th("units","Units",1)}${th("rev","Revenue",1)}${th("shRev","% of rev.",1)}${th("gp","Est. profit",1)}${th("shGp","% of profit",1)}${th("mg","Margin",1)}</tr>
    ${rows.map(r=>`<tr><td>${EMOJI[r.pid]} ${r.name}</td><td>${r.cat}</td><td class="r">${fmtN(r.units)}</td><td class="r">${fmt$f(r.rev)}</td><td class="r">${pct(r.shRev)}</td><td class="r">${fmt$f(r.gp)}</td><td class="r">${pct(r.shGp)}</td><td class="r">${pct(r.mg)}</td></tr>`).join("")}</table></div>`:`<div class="note">No sales for this combination. Try widening the time window.</div>`}</div>
  <div class="defs"><b>Definitions.</b> Revenue = units × product price. Estimated gross profit = units × (price − cost). These are <i>reconstructed</i> from one current price per toy; the data has no price history, so they are not accounting figures. Deltas compare with the equal-length window just before the selected one (shown when the data goes back far enough). Percent labels show each item's share of the current selection (the filters above), so the bars shown may not add up to 100%. Gross margin % = estimated gross profit ÷ revenue. Source: sales.csv, products.csv, stores.csv.</div>`;
  window.dashRows=rows;
}
function toggleCat(c){ if(dash.cats.size==5){dash.cats=new Set([c])} else if(dash.cats.has(c)){dash.cats.delete(c);if(!dash.cats.size)dash.cats=new Set(CATS)} else dash.cats.add(c); renderDash()}
/* toy dropdown: alphabetical, ~5 rows visible, scrolls */
let comboHl=0;
function comboItems(q){q=(q||"").toLowerCase();return PSORT.filter(p=>p.name.toLowerCase().includes(q))}
function comboOpen(q){const inp=document.getElementById("prodin");const val=q===undefined?"":q;const items=comboItems(val);comboHl=0;
  const l=document.getElementById("combolist");
  l.innerHTML=(val?"":`<div class="opt ${comboHl==-1?"hl":""}" onmousedown="comboPick(0)"><b>All toys</b></div>`)+
    (items.length?items.map((p,i)=>`<div class="opt ${i==0&&val?"hl":""}" data-id="${p.id}" onmousedown="comboPick(${p.id})"><span>${EMOJI[p.id]}</span>${esc(p.name)}<small>${p.cat}</small></div>`).join(""):`<div class="opt" style="color:var(--ink3)">No toys match “${esc(val)}”</div>`);
  l.classList.add("on")}
function comboPick(id){dash.pid=id||null;renderDash()}
function comboKey(e){if(e.key=="Enter"){const first=document.querySelector("#combolist .opt[data-id]");if(first)comboPick(+first.dataset.id)}if(e.key=="Escape")document.getElementById("combolist").classList.remove("on")}
document.addEventListener("click",e=>{if(!e.target.closest(".combo"))document.getElementById("combolist")?.classList.remove("on")});

