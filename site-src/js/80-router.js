/* Tab navigation and URL hash routing (also test hooks such as #ask-eval). */
/* ---------- router ---------- */
const TABS=[["start","🏠","Home","var(--s7)"],["dashboard","📊","Dashboard","var(--s1)"],["toys","🧸","Toy Finder","var(--s5)"],["presentation","🎤","Presentation","#d68700"],["ask","💬","Ask","var(--s3)"]];
let current="start";
function show(t){current=t;history.replaceState(null,"","#"+t);
  document.querySelectorAll(".tab").forEach(e=>e.classList.toggle("on",e.id==t));
  document.getElementById("nav").innerHTML=TABS.map(([k,e,l,c])=>`<button class="${k==t?"on":""}" style="${k==t?`background:${c}`:""}" onclick="show('${k}')">${e} ${l}</button>`).join("");
  ({start:renderStart,dashboard:renderDash,presentation:renderDeck,toys:renderToys,ask:renderAsk})[t]();
  closeToy();scrollTo(0,0)}
(function(){const h=location.hash.slice(1);
  if(h=="dash-open"){dash.fopen=true;show("dashboard");return}
  if(h=="dash-filt"){setPreset("l3");dash.cats=new Set(["Games"]);show("dashboard");return}
  if(h=="toys-open"){toys.fopen=true;show("toys");return}
  if(h=="toys-l3"){toyPreset("l3");show("toys");return}
  if(h.startsWith("toy:")){show("toys");openToy(+h.slice(4))}
  else if(h.startsWith("dash:")){dash.cats=new Set([h.slice(5)]);show("dashboard")}
  else if(h.startsWith("pid:")){dash.pid=+h.slice(4);show("dashboard")}
  else if(h=="dash-mg"){dash.metric="mg";dash.trend="pct";show("dashboard")}
  else if(h=="dash-pct"){dash.trend="pct";dash.show="pct";show("dashboard")}
  else if(h.startsWith("deck:")){slide=+h.slice(5);show("presentation")}
  else if(h=="ask-demo"){show("ask");["which toys made the most profit last quarter","best selling toys in games in 2022","which stores sell the most lego","how satisfied are our customers?","which toy is the best?","wich category has the best margn"].forEach(q=>ask(q,true))}
  else if(h=="ask-home"){show("ask");ask("which toys made the most profit",true)}
  else if(h=="ask-smart-fake"){window.__embedFactory=async()=>{const D=96,hv=s=>{let x=2166136261;for(const c of s)x=Math.imul(x^c.charCodeAt(0),16777619);return Math.abs(x)};
      return async texts=>texts.map(s=>{const v=new Array(D).fill(0);for(const w of t2(s))v[hv(w)%D]+=1;for(let i=0;i<s.length-2;i++)v[hv(s.slice(i,i+3))%D]+=.3;const n=Math.hypot(...v)||1;return v.map(x=>x/n)})};show("ask");smartLoad()}
  else if(h=="ask-help"){askHelpOpen=true;show("ask")}
  else if(h=="ask-ex"){show("ask")}
  else if(h=="ask-eval"){show("ask");const o=runEval();document.getElementById("ask").insertAdjacentHTML("afterbegin",`<pre id="evalout">${JSON.stringify(o)}</pre>`)}
  else if(h=="ask-follow"){show("ask");["which toys made the most profit","what about electronics?","and in 2022?","best selling toys","which stores sell the most lego"].forEach(q=>ask(q,true))}
  else show(TABS.some(t=>t[0]==h)?h:"start")})();
