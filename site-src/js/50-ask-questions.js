/* Ask tab (1/4): slot parsing (toy, category, period), the 15 approved questions, and the original keyword matcher. */
/* ================= TAB 4: ASK ================= */
const FULL={m0:0,m1:20};
const ALIAS=(()=>{const first={};for(const p of DATA.P){const w=p.name.toLowerCase().replace(/[^a-z0-9 ]/g,"").split(" ")[0];first[w]=(first[w]||[]).concat(p.id)}
  const m=[];for(const p of DATA.P){m.push([p.name.toLowerCase().replace(/[^a-z0-9 ]/g,""),p.id]);const w=p.name.toLowerCase().replace(/[^a-z0-9 ]/g,"").split(" ")[0];if(w.length>=4&&first[w].length==1)m.push([w,p.id])}
  m.sort((a,b)=>b[0].length-a[0].length);return m})();
function parseSlots(q){
  const t=" "+q.toLowerCase().replace(/['’]/g,"").replace(/[^a-z0-9 ]/g," ").replace(/\s+/g," ")+" ";const slots={chips:[]};
  // toy
  for(const [a,id] of ALIAS){const re=new RegExp(`\\b${a}s?\\b`);if(re.test(t)){slots.pid=id;slots.chips.push("Toy: "+P[id].name);break}}
  // category
  const cm=[[/\b(games?)\b/,"Games"],[/\b(art|crafts?|arts)\b/,"Art & Crafts"],[/\b(sports?|outdoors?)\b/,"Sports & Outdoors"],[/\b(electronics?|gadgets?)\b/,"Electronics"],[/\b(in|for|within|of) (the )?toys\b|\btoys category\b|\btoy category\b/,"Toys"]];
  for(const [re,c] of cm) if(re.test(t)&&!(slots.pid&&P[slots.pid].cat!==c&&c!="Toys")){slots.cats=[c];slots.chips.push("Category: "+c);break}
  // period
  let m;
  if(/\blast quarter\b|\blatest quarter\b/.test(t)){slots.m0=18;slots.m1=20;slots.period="Q3 2023 (last full quarter in the data)"}
  else if(m=t.match(/\bq([1-4])\s*(?:20)?(22|23)?\b/)){const qn=+m[1];let yr=m[2]?+("20"+m[2]):(qn<=3?2023:2022);const s=(yr-2022)*12+(qn-1)*3;if(s+2<=20&&s>=0){slots.m0=s;slots.m1=s+2;slots.period=`Q${qn} ${yr}`+(m[2]?"":" (assumed)")}}
  else if(/\blast (3|three) months\b/.test(t)){slots.m0=18;slots.m1=20;slots.period="last 3 months of data (Jul–Sep 2023)"}
  else if(/\blast month\b/.test(t)){slots.m0=20;slots.m1=20;slots.period="Sep 2023 (last month in the data)"}
  else if((m=t.match(/\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?|(?:in|during|for) may)\s*(?:20)?(22|23)?\b/))){const w=m[1].replace(/^(in|during|for) /,"").slice(0,3);const mi=MN.map(x=>x.toLowerCase()).indexOf(w);let yr=m[2]?+("20"+m[2]):(mi<=8?2023:2022);const idx=(yr-2022)*12+mi;if(mi>=0&&idx>=0&&idx<=20){slots.m0=idx;slots.m1=idx;slots.period=mlong(idx)+(m[2]?"":" (assumed)")}}
  else if(m=t.match(/\b(2022|2023)\b/)){const y=+m[1];slots.m0=y==2022?0:12;slots.m1=y==2022?11:20;slots.period=y==2022?"2022":"2023 (Jan–Sep, the data ends in Sep)"}
  if(slots.period) slots.chips.push("Period: "+slots.period);
  return slots;
}
const scopeOf=(c)=>{const bits=[];if(c.pid)bits.push(P[c.pid].name);if(c.cats)bits.push(c.cats.join(", "));bits.push(c.period||"full period (Jan 2022 – Sep 2023)");return bits.join(", ")};
const topN=(obj,k,n=5,asc=false)=>Object.entries(obj).sort((a,b)=>asc?a[1][k]-b[1][k]:b[1][k]-a[1][k]).slice(0,n);
const nm=id=>P[id].name, sn=id=>ST[id].city+" #"+ST[id].name.split(" ").pop();
const QS=[
 {id:"top_profit",group:"🧸 Toys",title:"Which toys generated the most profit?",kw:"toys products profit most generated top earn profitable highest",rel:["top_units","cat_margin"],
  run:(c)=>{const A=agg(c),r=topN(A.byProd,"gp");if(!r.length)return null;return {text:`${nm(r[0][0])} generated the most estimated profit: ${fmt$f(r[0][1].gp)} (${scopeOf(c)}).`,rows:r.map(([id,b])=>({label:nm(id),v:b.gp})),fmt:fmt$f,cols:["Toy","Est. profit"],src:"sales.csv · products.csv",def:"Est. gross profit = units × (price − cost)."}}},
 {id:"top_units",group:"🧸 Toys",title:"What were the best-selling toys?",kw:"best selling toys products units sold popular top",rel:["top_rev","top_profit"],
  run:(c)=>{const A=agg(c),r=topN(A.byProd,"units");if(!r.length)return null;return {text:`${nm(r[0][0])} sold the most units (${fmtN(r[0][1].units)}) (${scopeOf(c)}). “Best-selling” here means units sold, not revenue.`,rows:r.map(([id,b])=>({label:nm(id),v:b.units})),fmt:fmtN,cols:["Toy","Units sold"],src:"sales.csv · products.csv",def:"Units sold = sum of transaction units."}}},
 {id:"top_rev",group:"🧸 Toys",title:"Which toys brought in the most revenue?",kw:"toys products revenue most brought money sales top highest",rel:["top_profit","low_margin"],
  run:(c)=>{const A=agg(c),r=topN(A.byProd,"rev");if(!r.length)return null;return {text:`${nm(r[0][0])} brought in the most revenue: ${fmt$f(r[0][1].rev)} (${scopeOf(c)}).`,rows:r.map(([id,b])=>({label:nm(id),v:b.rev})),fmt:fmt$f,cols:["Toy","Revenue"],src:"sales.csv · products.csv",def:"Revenue = units × price."}}},
 {id:"low_margin",group:"🧸 Toys",title:"Which toys have the lowest margin?",kw:"toys products lowest margin worst thin low profitability",rel:["top_rev","cat_margin"],
  run:(c)=>{const A=agg(c),r=Object.entries(A.byProd).map(([id,b])=>[id,b.gp/b.rev]).sort((a,b)=>a[1]-b[1]).slice(0,5);if(!r.length)return null;return {text:`${nm(r[0][0])} has the lowest gross margin at ${pct(r[0][1])} (${scopeOf(c)}).`,rows:r.map(([id,v])=>({label:nm(id),v:v*100})),fmt:v=>v.toFixed(1)+"%",cols:["Toy","Gross margin"],src:"sales.csv · products.csv",def:"Margin = estimated gross profit ÷ revenue."}}},
 {id:"store_rev",group:"🏬 Stores",title:"Which stores had the highest revenue?",kw:"stores store highest revenue best location sales most",rel:["store_profit","top_rev"],
  run:(c)=>{const A=agg(c),r=topN(A.byStore,"rev");if(!r.length)return null;return {text:`${sn(r[0][0])} had the highest revenue: ${fmt$f(r[0][1].rev)} (${scopeOf(c)}).`,rows:r.map(([id,b])=>({label:sn(id),v:b.rev})),fmt:fmt$f,cols:["Store","Revenue"],src:"sales.csv · products.csv · stores.csv",def:"Revenue = units × price."}}},
 {id:"store_profit",group:"🏬 Stores",title:"Which stores had the greatest estimated profit?",kw:"stores store greatest estimated profit most profitable",rel:["store_rev","top_profit"],
  run:(c)=>{const A=agg(c),r=topN(A.byStore,"gp");if(!r.length)return null;return {text:`${sn(r[0][0])} had the greatest estimated profit: ${fmt$f(r[0][1].gp)} (${scopeOf(c)}).`,rows:r.map(([id,b])=>({label:sn(id),v:b.gp})),fmt:fmt$f,cols:["Store","Est. profit"],src:"sales.csv · products.csv · stores.csv",def:"Est. gross profit = units × (price − cost)."}}},
 {id:"store_for_toy",group:"🏬 Stores",title:"Which stores sell the most of a particular toy?",kw:"stores store sell most particular toy specific lego nerf where sold",needs:"pid",rel:["store_rev","trend"],
  run:(c)=>{const A=agg(c),r=topN(A.byStore,"units");if(!r.length)return null;return {text:`${sn(r[0][0])} sold the most ${nm(c.pid)}: ${fmtN(r[0][1].units)} units (${scopeOf(c)}).`,rows:r.map(([id,b])=>({label:sn(id),v:b.units})),fmt:fmtN,cols:["Store","Units sold"],src:"sales.csv · stores.csv",def:"Units sold = sum of transaction units, for the selected toy."}}},
 {id:"cat_margin",group:"🏷️ Categories",title:"Which category has the best gross margin?",kw:"category categories margin best gross profitability highest",rel:["cat_rev","low_margin"],
  run:(c)=>{const A=agg(c),r=Object.entries(A.byCat).map(([k,b])=>[k,b.gp/b.rev]).sort((a,b)=>b[1]-a[1]);if(!r.length)return null;return {text:`${r[0][0]} has the best gross margin at ${pct(r[0][1])}${r.length>1?`, while ${r[r.length-1][0]} has the lowest at ${pct(r[r.length-1][1])}`:""} (${scopeOf(c)}).`,rows:r.map(([k,v])=>({label:k,v:v*100,color:CCOL[k]})),fmt:v=>v.toFixed(1)+"%",cols:["Category","Gross margin"],src:"sales.csv · products.csv",def:"Margin = estimated gross profit ÷ revenue."}}},
 {id:"cat_rev",group:"🏷️ Categories",title:"How does revenue compare across categories?",kw:"category categories revenue compare comparison breakdown split sales",rel:["cat_margin","trend"],
  run:(c)=>{const A=agg(c),r=topN(A.byCat,"rev",5);if(!r.length)return null;return {text:`${r[0][0]} is the biggest category by revenue: ${fmt$f(r[0][1].rev)}, ${pct(r[0][1].rev/A.tot.rev)} of the total (${scopeOf(c)}).`,rows:r.map(([k,b])=>({label:k,v:b.rev,color:CCOL[k]})),fmt:fmt$f,cols:["Category","Revenue"],src:"sales.csv · products.csv",def:"Revenue = units × price."}}},
 {id:"trend",group:"📅 Time",title:"How has revenue changed over time?",kw:"revenue changed change over time trend monthly month history growth",rel:["best_month","yoy"],
  run:(c)=>{const A=agg(c),v=A.byMonth.slice(c.m0,c.m1+1).map(b=>b.rev);if(!A.tot.rev)return null;return {text:`Monthly revenue ${scopeOf(c)}: total ${fmt$f(A.tot.rev)}${v.length>1?`, from ${fmt$f(v[0])} in ${mlong(c.m0)} to ${fmt$f(v[v.length-1])} in ${mlong(c.m1)}`:""}.`,chart:"line",series:v,offset:c.m0,rows:v.map((x,i)=>({label:mlong(i+c.m0),v:x})),fmt:fmt$f,cols:["Month","Revenue"],src:"sales.csv · products.csv",def:"Revenue = units × price, summed by month."}}},
 {id:"best_month",group:"📅 Time",title:"Which month had the highest revenue?",kw:"month highest revenue peak best busiest season",rel:["trend","yoy"],
  run:(c)=>{const A=agg(c),r=A.byMonth.map((b,i)=>({label:mlong(i),v:b.rev,i})).filter(x=>x.i>=c.m0&&x.i<=c.m1).sort((a,b)=>b.v-a.v).slice(0,5);if(!r.length||!r[0].v)return null;return {text:`${r[0].label} had the highest revenue: ${fmt$f(r[0].v)} (${scopeOf(c)}).`,rows:r,fmt:fmt$f,cols:["Month","Revenue"],src:"sales.csv · products.csv",def:"Revenue = units × price, summed by month."}}},
 {id:"yoy",group:"📅 Time",title:"How does 2023 compare with 2022?",kw:"2023 compare comparison 2022 year over year growth versus yoy grown growing",rel:["trend","cat_rev"],
  run:(c)=>{const a=agg({...c,m0:12,m1:20}).tot,b=agg({...c,m0:0,m1:8}).tot;if(!b.rev||!a.rev)return null;const d=(x,y)=>(x/y-1)*100;
    const o=[["Revenue",d(a.rev,b.rev)],["Units sold",d(a.units,b.units)],["Est. profit",d(a.gp,b.gp)]];
    return {text:`Comparing the same months (Jan–Sep): revenue is ${o[0][1]>=0?"up":"down"} ${Math.abs(o[0][1]).toFixed(1)}%, units ${o[1][1]>=0?"up":"down"} ${Math.abs(o[1][1]).toFixed(1)}%, and estimated profit ${o[2][1]>=0?"up":"down"} ${Math.abs(o[2][1]).toFixed(1)}% (${c.pid?nm(c.pid)+", ":""}${c.cats?c.cats.join(", ")+", ":""}2023 vs 2022).`,
      chart:"cards",cards:o.map(([l,v])=>({l,v})),rows:o.map(([l,v])=>({label:l,v:+v.toFixed(1)})),fmt:v=>v+"%",cols:["Measure","Change vs 2022"],src:"sales.csv · products.csv",def:"Jan–Sep 2023 vs Jan–Sep 2022, so the two periods are the same length. Time words in the question are ignored here."}}},
 {id:"low_stock",group:"📦 Stock",title:"Which toys have the least stock right now?",kw:"toys products least stock inventory low lowest running out left",rel:["zero_stock","restock"],
  run:(c)=>{const r=DATA.P.filter(p=>(!c.cats||c.cats.includes(p.cat))&&(!c.pid||c.pid==p.id)).map(p=>[p.id,INV[p.id].stock]).sort((a,b)=>a[1]-b[1]).slice(0,5);return {text:`${nm(r[0][0])} has the least stock on hand across all stores: ${fmtN(r[0][1])} units. This is a single snapshot, not a trend. Time filters don't apply to stock.`,rows:r.map(([id,v])=>({label:nm(id),v})),fmt:fmtN,cols:["Toy","Units in stock"],src:"inventory.csv · products.csv",def:"Stock on hand summed across stores from the supplied snapshot. Not a historical quantity."}}},
 {id:"zero_stock",group:"📦 Stock",title:"Which toys are out of stock in the most stores?",kw:"toys products out of stock zero empty stockout stockouts stores most",rel:["restock","low_stock"],
  run:(c)=>{const r=DATA.P.filter(p=>(!c.cats||c.cats.includes(p.cat))&&(!c.pid||c.pid==p.id)).map(p=>[p.id,INV[p.id].zero]).sort((a,b)=>b[1]-a[1]).slice(0,5);return {text:`${nm(r[0][0])} is at zero stock in ${r[0][1]} stores, the most of any toy. This is a single snapshot.`,rows:r.map(([id,v])=>({label:nm(id),v})),fmt:fmtN,cols:["Toy","Stores at zero stock"],src:"inventory.csv · products.csv",def:"Count of stores whose stock-on-hand is 0 in the snapshot."}}},
 {id:"restock",group:"📦 Stock",title:"Where do popular toys have zero stock?",kw:"popular toys products zero stock restock reorder demand empty out where stores",rel:["zero_stock","top_units"],
  run:(c)=>{const A=agg({...c}),sold={};for(const [sid,p,mi,u] of DATA.SMP){if(mi<c.m0||mi>c.m1)continue;if(c.pid&&p!=c.pid)continue;if(c.cats&&!c.cats.includes(P[p].cat))continue;sold[sid+"|"+p]=(sold[sid+"|"+p]||0)+u}
    const r=DATA.INVS.filter(x=>x[2]==0).map(([s,p])=>({label:`${nm(p)} @ ${ST[s].city} #${ST[s].name.split(" ").pop()}`,v:sold[s+"|"+p]||0})).sort((a,b)=>b.v-a.v).slice(0,5);if(!r.length||!r[0].v)return null;
    return {text:`The biggest gap: ${r[0].label} has zero stock now but sold ${fmtN(r[0].v)} units (${scopeOf(c)}). This ranks by past sales only; it is not an optimized restock plan.`,rows:r,fmt:fmtN,cols:["Toy @ store","Units sold in period"],src:"inventory.csv · sales.csv · products.csv · stores.csv",def:"Store-toy pairs with zero stock in the snapshot, ranked by units sold in the selected period."}}},
];
const QI=Object.fromEntries(QS.map(q=>[q.id,q]));
const AMBIG=/\b(best|favorite|favourite|greatest|top)\b/i, METRICW=/(selling|profit|revenue|units|margin|sold|sales|money|earn|stock|store|month|category|categories)/i;
const UNSUP=/(customer|satisf|review|rating|survey|return|refund|forecast|predict|next year|next month|employee|staff|competitor|weather|discount|promo|coupon)/i;
const STOP=new Set("the a an of in is are what which who how do we our to for and was were had has have with on at by me show tell most more than that this those these it its right now from as be can you i my your any all some".split(" "));
const toks=s=>s.toLowerCase().replace(/['’]/g,"").replace(/[^a-z0-9 ]/g," ").split(/\s+/).filter(w=>w&&!STOP.has(w));
function lev(a,b){const m=a.length,n=b.length,d=Array.from({length:m+1},(_,i)=>[i,...Array(n).fill(0)]);for(let j=0;j<=n;j++)d[0][j]=j;for(let i=1;i<=m;i++)for(let j=1;j<=n;j++)d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a[i-1]==b[j-1]?0:1));return d[m][n]}
const stem=w=>w.replace(/(ing|es|s)$/,"");
function match(q){const t=toks(q);let all=[];
  for(const Q of QS){const kws=[...new Set(toks(Q.kw+" "+Q.title))];let hit=0;
    for(const w of t){if(kws.includes(w)||kws.some(k=>stem(k)==stem(w))){hit++;continue}
      if(w.length>=5&&kws.some(k=>k.length>=5&&lev(w,k)<=(w.length>=8?2:1)))hit+=.8}
    all.push([Q,hit/Math.max(3,t.length)])}
  all.sort((a,b)=>b[1]-a[1]);return {best:all[0][0],score:all[0][1],near:all.slice(0,3).map(x=>x[0])}}

