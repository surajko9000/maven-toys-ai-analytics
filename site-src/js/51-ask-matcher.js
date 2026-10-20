/* Ask tab (2/4): phrasing-bank matcher (synonyms, typo repair) and the accuracy self-test. */
/* ---------- improved matcher: phrasing bank + IDF cosine + synonyms + typo repair ---------- */
const PARA=__PARA__;
const EVAL=__EVAL__;
const CANON={};
[["toy","toys","product","products","item","items"],["store","stores","shop","shops","location","locations","branch","branches"],
 ["sell","sells","selling","sold","sale","sales","seller","sellers"],["revenue","revenues","gross","grossing","dollars","money"],
 ["profit","profits","profitable","profitability","earn","earns","earned","earner","earners","earnings"],["margin","margins"],
 ["stock","inventory","stocked","shelf","shelves","shelved","hand"],["stockout","stockouts","unavailable","missing"],
 ["zero","empty","none"],["low","lowest","least","fewest","smallest","thin","thinnest","slim","worst","short","little","weakest","thinner"],
 ["top","best","biggest","highest","largest","greatest","strongest","hottest","peak","busiest"],
 ["month","months","monthly"],["year","years","yearly","annual","annually","yoy"],["compare","compared","comparison","versus","vs","against"],
 ["grow","growing","growth","rising","grew"],["trend","trending","history"],["category","categories","department","type"],
 ["unit","units"],["restock","reorder","restocking"],["low","nearly","almost","running"]].forEach(g=>g.slice(1).forEach(w=>CANON[w]=g[0]));
const NOISE=new Set(("last latest recent recently lately past this quarter q1 q2 q3 q4 2022 2023 games game art crafts sports outdoors electronics gadgets "+
  "january february march april may june july august september october november december all right now from do does did was were is are the a an of in on at by to for and with me my our we us you your show tell give list what which who how when where why many much each every ever per than that them these those it its be can will would should have has had get got into out as or one specific particular given any some made make makes making bring brings brought generate generated generates").split(" "));
NOISE.delete("out");NOISE.delete("month");
const ALIASRE=ALIAS.map(([a])=>new RegExp(`\\b${a}s?\\b`,"g"));
const DIMW=new Set(["toy","store","category","month","year"]);
const KEYW=new Set(["toy","store","category","month","year","stock","stockout","zero","margin","profit","revenue","unit","restock","popular","compare","trend","toyname","low","top"]);
const t2=s=>{const o=[];const yrs=new Set((s.match(/\b(2022|2023)\b/g)||[]));
  let s2=s.toLowerCase().replace(/['’]/g,"").replace(/[^a-z0-9 ]/g," ").replace(/\s+/g," ");for(const re of ALIASRE)s2=s2.replace(re," toyname ");
  for(let w of s2.split(/\s+/)){if(!w)continue;
    w=CANON[w]||CANON[w.replace(/s$/,"")]||w;if(NOISE.has(w))continue;if(!o.includes(w))o.push(w)}
  if(yrs.size>1)for(const w of["year","compare"])if(!o.includes(w))o.push(w);
  if(!o.some(w=>DIMW.has(w)||w=="stock"||w=="stockout"))o.push("toy");
  return o};
const BANK=[];const DF={};
for(const [id,list] of Object.entries(PARA))for(const p of list){const tk=t2(p);BANK.push({id,tk});for(const w of tk)DF[w]=(DF[w]||0)+1}
const VOCAB=Object.keys(DF),NB=BANK.length,idf=w=>Math.log(1+NB/(DF[w]||0.5))*(KEYW.has(w)?1.6:1);
function repair(w){if(DF[w])return w;if(w.length<5)return w;let b=null,bd=9;for(const v of VOCAB){if(v.length<5)continue;const d=lev(w,v);if(d<bd&&d<=(w.length>=8?2:1)){bd=d;b=v}}return b||w}
function match2(q){
  const qt=t2(q).map(repair);if(!qt.length)return {best:null,score:0,near:[],via:"none"};
  const qn=Math.sqrt(qt.reduce((s,w)=>s+idf(w)**2,0));const by={};
  for(const b of BANK){let dot=0;for(const w of qt)if(b.tk.includes(w))dot+=idf(w)**2;
    const bn=Math.sqrt(b.tk.reduce((s,w)=>s+idf(w)**2,0))||1;const sc=dot/(qn*bn);if(!(by[b.id]>=sc))by[b.id]=sc}
  const all=Object.entries(by).sort((a,b)=>b[1]-a[1]);
  return {best:QI[all[0][0]],score:all[0][1],margin:all[0][1]-(all[1]?all[1][1]:0),near:all.slice(0,3).map(x=>QI[x[0]]),via:"phrasing bank"}}
const MATCH_MIN=0.34;
/* route(): the intent decision the chat makes, reused by the self-test */
function route(q,m=match2){
  if(UNSUP.test(q)||/\bwhy\b/i.test(q))return null;
  const r=m(q);if(!r.best)return null;
  const s=m===match2?r.score:r.score;if(s<(m===match2?MATCH_MIN:0.4))return null;return r.best.id}
function runEval(){
  const cases=EVAL.cases;let o={old:0,neu:0,n:cases.length,inScope:0,oldIn:0,neuIn:0,fails:[]};
  for(const [q,exp] of cases){const e=exp=="none"?null:exp;const a=route(q,match),b=route(q,match2);
    if(a===e)o.old++;if(b===e)o.neu++;if(e){o.inScope++;if(a===e)o.oldIn++;if(b===e)o.neuIn++}
    if(b!==e)o.fails.push({q,exp:e,got:b,score:+(match2(q).score).toFixed(2)})}
  return o}


