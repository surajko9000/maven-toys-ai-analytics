/* Ask tab (3/4): optional in-browser embedding model (opt-in, falls back to the keyword matcher). */
/* ---------- optional in-browser embedding model (opt-in, falls back to the keyword matcher) ---------- */
const SMART={state:"off",pct:0,embed:null,vecs:null,err:"",model:"Xenova/all-MiniLM-L6-v2",evalOut:""};
const EMB_MIN=0.5,KW_SURE=0.6,KW_MARGIN=0.15;       // starting guesses, to be tuned with the in-page accuracy test
const normQ=s=>{let o=" "+s.toLowerCase().replace(/['’]/g,"").replace(/[^a-z0-9 ]/g," ").replace(/\s+/g," ")+" ";for(const re of ALIASRE)o=o.replace(re," this toy ");return o.replace(/\s+/g," ").trim()};
function renderSmart(){
  const el=document.getElementById("smartbar");if(!el)return;
  const S=SMART;let h="";
  if(S.state=="off")h=`<span class="sbi">🧠</span><div class="sbt"><b>Smarter matching is off.</b> Turn it on to download a small AI model (about 25 MB, one time) into your browser. It only helps pick which prepared question you mean.</div><button class="btn pri" onclick="smartLoad()">Turn on</button>`;
  else if(S.state=="loading")h=`<span class="sbi">⏳</span><div class="sbt"><b>${S.pct<100?`Downloading the model… ${S.pct}%`:"Getting ready…"}</b><div class="pbar"><i style="width:${S.pct}%"></i></div></div>`;
  else if(S.state=="on")h=`<span class="sbi">🧠</span><div class="sbt"><b>Smarter matching is on.</b> A small AI model running in your browser helps pick the question. The numbers still come from the CSVs.${S.evalOut?`<div class="sbres">${S.evalOut}</div>`:""}</div><button class="btn" onclick="smartRunEval()">Test accuracy</button><button class="btn" onclick="SMART.state='off';renderSmart()">Turn off</button>`;
  else h=`<span class="sbi">⚠️</span><div class="sbt"><b>The model could not load.</b> The chat still works with the standard matcher. <span class="mut">(${esc(S.err)})</span></div><button class="btn" onclick="SMART.state='off';smartLoad()">Try again</button>`;
  el.className="smartbar "+S.state;el.innerHTML=h}
async function smartLoad(){
  if(SMART.state=="loading")return;
  if(SMART.vecs&&SMART.embed){SMART.state="on";renderSmart();return}
  SMART.state="loading";SMART.pct=0;SMART.err="";renderSmart();
  try{
    let embed;
    if(window.__embedFactory)embed=await window.__embedFactory();
    else{
      const tf=await import("https://cdn.jsdelivr.net/npm/@huggingface/transformers@3");
      const files={};
      const fe=await tf.pipeline("feature-extraction",SMART.model,{progress_callback:p=>{
        if(p.status=="progress"&&p.total){files[p.file]=[p.loaded,p.total];let a=0,b=0;for(const [l,tt] of Object.values(files)){a+=l;b+=tt}SMART.pct=Math.min(99,Math.round(a/b*100));renderSmart()}}});
      embed=async texts=>{const o=await fe(texts,{pooling:"mean",normalize:true});const d=o.data,n=texts.length,k=d.length/n;return Array.from({length:n},(_,i)=>Array.from(d.slice(i*k,(i+1)*k)))};
    }
    SMART.pct=100;renderSmart();
    const items=[];for(const [id,list] of Object.entries(PARA))for(const p of list)items.push([id,normQ(p)]);
    const vecs=[];for(let i=0;i<items.length;i+=24){const chunk=items.slice(i,i+24),vs=await embed(chunk.map(x=>x[1]));chunk.forEach((x,j)=>vecs.push({id:x[0],v:vs[j]}))}
    SMART.embed=embed;SMART.vecs=vecs;SMART.state="on";
  }catch(e){SMART.state="failed";SMART.err=String(e&&e.message||e).slice(0,140)}
  renderSmart()}
async function smartMatch(q){
  const [qv]=await SMART.embed([normQ(q)]);const by={};
  for(const b of SMART.vecs){let s=0;const v=b.v;for(let i=0;i<v.length;i++)s+=v[i]*qv[i];if(!(by[b.id]>=s))by[b.id]=s}
  const all=Object.entries(by).sort((a,b)=>b[1]-a[1]);
  return {best:QI[all[0][0]],score:all[0][1],margin:all[0][1]-(all[1]?all[1][1]:0),near:all.slice(0,3).map(x=>QI[x[0]]),via:"embedding"}}
async function decide(q){
  const kw=match2(q);kw.via="keywords";
  if(SMART.state!="on")return kw;
  if(kw.score>=KW_SURE&&kw.margin>=KW_MARGIN)return kw;
  return smartMatch(q)}
async function smartRunEval(){
  SMART.evalOut="Running…";renderSmart();
  let ok=0,inOk=0,inN=0,viaE=0;const fails=[];
  for(const [q,exp] of EVAL.cases){const e=exp=="none"?null:exp;let got=null;
    if(!(UNSUP.test(q)||/\bwhy\b/i.test(q))){const r=await decide(q);if(r.via=="embedding")viaE++;if(r.best&&r.score>=(r.via=="embedding"?EMB_MIN:MATCH_MIN))got=r.best.id}
    if(got===e)ok++;if(e){inN++;if(got===e)inOk++}else if(got)fails.push(q);if(got!==e&&e)fails.push(q+" → "+got)}
  const n=EVAL.cases.length;
  SMART.evalOut=`Test set: <b>${ok} of ${n} correct (${(100*ok/n).toFixed(1)}%)</b>. Of the in-scope questions, ${inOk} of ${inN} matched. The model decided ${viaE} questions; keywords handled the rest.`;
  window.__smartEval={ok,n,inOk,inN,viaE,fails};renderSmart()}

