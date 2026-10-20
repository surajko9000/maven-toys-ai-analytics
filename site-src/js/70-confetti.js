/* Soft confetti behind every page. */
/* ---------- soft confetti behind every page ---------- */
(function(){
  const C=["#ffd34d","#ff8fb1","#7be0b3","#9fc2ff","#ff9a5a","#b78cff"],K=["c-ci","c-sq","c-st"];
  let s=7;const r=()=>(s=(s*9301+49297)%233280)/233280;
  const bg=document.createElement("div");bg.className="cfbg";bg.setAttribute("aria-hidden","true");
  const COLS=8,ROWS=6;let i=0;
  for(let row=0;row<ROWS;row++)for(let col=0;col<COLS;col++,i++){const sz=11+Math.round(r()*10);
    const left=(col+.15+r()*.7)/COLS*96,top=14+(row+.15+r()*.7)/ROWS*82;
    bg.insertAdjacentHTML("beforeend",`<span class="${K[(i+row)%3]}" style="left:${left.toFixed(1)}%;top:${top.toFixed(1)}%;width:${sz}px;height:${sz}px;background:${C[(i*5+row)%6]};animation-delay:${(-r()*8).toFixed(1)}s"></span>`)}
  document.body.appendChild(bg);
})();

