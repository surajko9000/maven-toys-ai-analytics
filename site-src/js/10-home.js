/* Home tab. */
/* ================= TAB 0: START HERE ================= */
function goToy(btn,id){
  if(matchMedia("(prefers-reduced-motion: reduce)").matches){show("toys");openToy(id);return}
  btn.classList.add("pop");document.querySelector("main").classList.add("leaving");
  setTimeout(()=>{document.querySelector("main").classList.remove("leaving");show("toys");openToy(id)},230)}
function renderStart(){
  const cards=[["dashboard","1","Dashboard","img/home-dashboard.jpg","Charts and tables that people can filter themselves, without asking an analyst.","Open the dashboard","#2a78d6",""],
               ["presentation","2","Presentation","deck/preview/slide-1.jpg","A short deck that tells the story and ends with a recommendation. Download it as PowerPoint or PDF.","Open the presentation","#e08a00",""],
               ["ask","3","Ask questions","img/home-ask.jpg","Type a one-off question and get an answer with a chart. A demo of ad hoc requests.","Try Ask","#1baf7a",""],
               ["toys","✨","Toy Finder","img/home-toys.jpg","A custom data app: browse all 35 toys like a store catalog. I asked for a picture of every toy, and Claude drew all 35 as original illustrations. Normally this takes a developer, a designer and weeks of work.","Open the Toy Finder","#d6336c","Bonus · only possible with Claude"]]
    .map(([k,n,h,img,d,b,c,tag])=>`<div class="hcard" onclick="show('${k}')"><img src="${img}" alt="Preview of the ${h} tab" loading="lazy"><div class="hb">${tag?`<span class="hunlock">${tag}</span>`:`<span class="hn" style="background:${c}">${n}</span>`}<h3>${h}</h3><p>${d}</p><span class="btn pri" style="background:${c};border-color:${c}">${b} →</span></div></div>`).join("");
  const SH=[[6,"Colorbuds",-6],[18,"Lego Bricks",5],[29,"Plush Pony",-4],[28,"Playfoam",6],[9,"Dino Egg",-5],[33,"Teddy Bear",4],[34,"Toy Robot",-6],[30,"Rubik's Cube",5],[16,"Jenga",-4],[11,"Etch A Sketch",6],[14,"Glass Marbles",-5],[31,"Splash Balls",4]];
  const shelf=SH.map(([id,n,r],i)=>`<button style="--i:${i};rotate:${r}deg" title="${n}" aria-label="Meet ${n}" onclick="goToy(this,${id})">${ILLUS[id]}</button>`).join("");
  document.getElementById("start").innerHTML=`
  <div class="hherowrap">
    <div class="hhero">
      <span class="eyebrow">A Claude Code experiment</span>
      <h1>Maven Toys Analytics Hub</h1>
    </div>
  </div>
  <div class="shelf">${shelf}</div><div class="shelfboard"></div>
  <p class="shelfhint">Tap a toy to meet it :)</p>
  <div class="card hctx">
    <p>This site is a <b>demonstration</b> of what Claude Code can build for a data analyst.</p>
    <p>Data analysts are usually asked for <b>three</b> things:</p>
    <div class="hchips"><span>📊 Dashboards</span><span>🎤 Presentations</span><span>💬 Ad hoc data requests</span></div>
    <p><b>I built all three data artifacts entirely with Claude.</b></p>
    <p>They are based on free sample data from a fictional toy company in Mexico, <b>Maven Toys</b>. The analysis covers sales, profit, margin and stock. The results are below.</p>
  </div>
  <div class="hcards">${cards}</div>

  <div class="hfacts">
    <div><span class="hfi">🗂️</span><div><b>The data</b><br>Free sample data from Maven Analytics: 50 stores, 35 toys, Jan 2022 to Sep 2023.</div></div>
    <div><span class="hfi">🤖</span><div><b>Made by Claude, checked by a human</b><br>Claude wrote all the code, charts, slides, drawings and text. I wrote the requests and checked the numbers.</div></div>
  </div>
  <div class="hfoot">Built by <a class="lnk" href="https://github.com/surajko9000" target="_blank" rel="noopener" style="margin-left:0">@surajko9000</a> to see how far Claude Code can go on everyday analyst work
    · <a class="lnk" href="https://github.com/surajko9000/maven-toys-ai-analytics" target="_blank" rel="noopener">View the code on GitHub ↗</a></div>`;
}

