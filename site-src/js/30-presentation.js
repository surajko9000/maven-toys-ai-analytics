/* Presentation tab: slide viewer and downloads. */
/* ================= TAB 2: PRESENTATION ================= */
const catStats=CATS.map(c=>({c,...ALL.byCat[c],mg:ALL.byCat[c].gp/ALL.byCat[c].rev})).sort((a,b)=>b.rev-a.rev);
const byMg=[...catStats].sort((a,b)=>b.mg-a.mg), topProf=Object.entries(ALL.byProd).sort((a,b)=>b[1].gp-a[1].gp).slice(0,5);
const peak=ALL.byMonth.map((b,i)=>[i,b.rev]).sort((a,b)=>b[1]-a[1])[0];
const share=c=>catStats.find(x=>x.c==c).rev/ALL.tot.rev;
const Y22=agg({m0:0,m1:8}).tot, Y23=agg({m0:12,m1:20}).tot;
const chg=(a,b)=>(a/b-1)*100;
const DECK={pptx:"deck/Colorbuds_to_Playfoam.pptx",pdf:"deck/Colorbuds_to_Playfoam.pdf",
 titles:["Title slide: Colorbuds, our #1 profit toy, is in decline","Our top profit toy is fading, and a newer toy is already making up part of the gap","Colorbuds sales have fallen 68% since January 2022, across almost every store","Fading is normal for our toys: 9 of 10 recent launches are 40%+ below their peak","Playfoam is the early bright spot, but 13 empty stores are costing us about $5K a month","We recommend three moves: back newer, higher-margin toys, test a Colorbuds refresh, and review in 8 weeks"]};
let slide=0;
const deckImg=i=>`deck/preview/slide-${i+1}.jpg`;
function renderDeck(){
  const n=DECK.titles.length;
  document.getElementById("presentation").innerHTML=`<h1><span class="h1t">${ILLUS[6]}</span>From Colorbuds to Playfoam: The Business Review</h1>
  <p class="sub">The deck Claude drafted from the data. Click through it here, or download it to edit.</p>
  <div class="deckbar"><span class="dlabel">⬇ Download</span>
    <a class="btn pri" href="${DECK.pptx}" download>PowerPoint (.pptx)</a>
    <a class="btn" href="${DECK.pdf}" download>PDF</a>
    <button class="btn" onclick="deckFull()" title="Full screen">⛶ Full screen</button>
    <span class="hint"><b id="dcount"></b> &nbsp;·&nbsp; click the slide or use ← → keys</span></div>
  <div class="viewer">
    <button class="navb" id="dprev" onclick="go(-1)" aria-label="Previous slide">‹</button>
    <div class="stage" id="stage" onclick="go(1)"><img id="deckimg" alt="" draggable="false"></div>
    <button class="navb" id="dnext" onclick="go(1)" aria-label="Next slide">›</button>
  </div>
  <div class="thumbs">${Array.from({length:n},(_,i)=>`<button class="thumb" id="th${i}" onclick="goTo(${i})" aria-label="Go to slide ${i+1}"><img src="${deckImg(i)}" alt="" loading="lazy"><b>#${i+1}</b></button>`).join("")}</div>
  <p class="src">Snapshot of the data through Sep 30, 2023. Numbers are computed from the CSVs and checked against an independent calculation. Profit is estimated from current price and cost.</p>`;
  showSlide();
}
function showSlide(){
  const n=DECK.titles.length,img=document.getElementById("deckimg");if(!img)return;
  img.src=deckImg(slide);img.alt=`Slide ${slide+1} of ${n}: ${DECK.titles[slide]}`;
  document.getElementById("dcount").textContent=`Slide ${slide+1} of ${n}`;
  document.getElementById("dprev").disabled=slide==0;document.getElementById("dnext").disabled=slide==n-1;
  document.querySelectorAll(".thumb").forEach((b,i)=>b.classList.toggle("on",i==slide));
  for(const j of [slide-1,slide+1]) if(j>=0&&j<n){const p=new Image();p.src=deckImg(j)}
}
function goTo(i){slide=Math.min(DECK.titles.length-1,Math.max(0,i));showSlide()}
function go(d){goTo(slide+d)}
function deckFull(){const el=document.getElementById("stage");(el.requestFullscreen||el.webkitRequestFullscreen||(()=>{})).call(el)}
document.addEventListener("keydown",e=>{if(current=="presentation"&&!(e.target instanceof HTMLInputElement)){if(e.key=="ArrowRight")go(1);if(e.key=="ArrowLeft")go(-1);if(e.key=="Home")goTo(0);if(e.key=="End")goTo(DECK.titles.length-1)}});

