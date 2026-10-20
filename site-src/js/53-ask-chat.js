/* Ask tab (4/4): chat window, thinking steps, follow-ups and answer rendering. */
const chat=[];let askBusy=false;let lastAsk=null;let askHelpOpen=false;
function renderAsk(){
  const groups={};for(const q of QS)(groups[q.group]??=[]).push(q);
  document.getElementById("ask").innerHTML=`<h1><span class="h1t">${ILLUS[34]}</span>Ask the Data: Questions in Plain English <span class="demobadge">🧪 Demo, not real AI</span></h1><p class="sub">Type a question in plain English. This page picks from 15 prepared questions and shows its work.</p>
  <details class="card demo" ${askHelpOpen?"open":""} ontoggle="askHelpOpen=this.open"><summary><span class="tag" style="background:#ffe9a0">💡 How it works</span> How does this demo work? How will this work in practice? Click to learn more</summary>
    <div class="mini"><div class="node" style="background:#e3eefb">🙋 You<small>ask in chat</small></div><div class="arrow">→</div><div class="node" style="background:#ece8fb">💬 Claude<small>or another AI chat tool</small></div><div class="arrow">→</div><div class="node" style="background:#fcf0d2">🗄️ Company data<small>AI writes and runs SQL</small></div><div class="arrow">→</div><div class="node" style="background:#def5ec">📊 Answer<small>in the chat: text, tables, charts</small></div></div>
    <p class="note" style="text-align:center;margin:6px 0 0;font-size:12.5px">In real life, you ask Claude (or a similar AI chat tool) connected to your company's data, and it answers right in the chat.</p>
    <div class="cmp">
      <div><h4>🚀 The real thing</h4><ul>
        <li>Open Claude (or ChatGPT, Gemini or similar), connected to your company's database.</li>
        <li>Ask anything in plain English. The AI writes the SQL, runs it, and answers in the chat, with a table or chart if you want.</li>
        <li>It handles new questions and follow-ups.</li>
        <li>Examples: Claude with an MCP connector (a plug-in for AI tools) to BigQuery, Snowflake or Postgres. Or built-in tools like Databricks Genie, Snowflake Cortex Analyst and Looker Conversational Analytics.</li></ul></div>
      <div><h4>🧪 This page is a demo, not the real thing</h4><ul>
        <li>By default there is no AI here. Your question is matched to 1 of 15 prepared questions.</li>
        <li><b>Optional:</b> turn on <b>Smarter matching</b> to use a small AI model in your browser. It only helps pick the question. The numbers still come from the CSVs.</li>
        <li>The answer is calculated from the CSV files in your browser.</li>
        <li>It remembers your last question, so "what about Electronics?" works.</li>
        <li>Anything else gets "I can't answer that."</li></ul></div>
      <div><h4>🤔 Why not real AI here?</h4><ul>
        <li>Real AI costs money for every question, plus a live database.</li>
        <li>It also needs safety rules.</li>
        <li>A free public page can't cover that.</li></ul></div>
    </div>
  </details>
  <div class="askwrap"><div>
    <div class="smartbar off" id="smartbar"></div>
    <div class="chat" id="chatlog">${chat.length?chat.map(m=>m.html).join(""):`<div class="msg a"><div class="who"><span class="bot">${ILLUS[34]}</span>Toy-Box Analyst</div>Hi! I'm a demo analyst, not real AI. Ask about toys, stores, categories, time or stock, and add a toy, category or time period, like <i>“best-selling toys in Games last quarter”</i>. I remember your last question, so you can follow up with <i>“what about Electronics?”</i><div class="sugg">${["Which toys generated the most profit last quarter?","How does 2023 compare with 2022?","Which category has the best gross margin?","Where do popular toys have zero stock?"].map(q=>`<button class="chip" onclick="ask(this.textContent)">${q}</button>`).join("")}</div></div>`}</div>
    <div class="askrow"><input type="text" id="askin" placeholder="Ask about toys, stores, categories, time or stock…" onkeydown="if(event.key=='Enter')ask()"><button class="btn pri" onclick="ask()">Ask</button></div>
  </div>
  <div class="card side"><h3>📚 Browse approved questions</h3>${Object.entries(groups).map(([g,qs])=>`<div class="grp"><div class="gt">${g}</div>${qs.map(q=>`<button onclick="ask(this.textContent,true)">${q.title}</button>`).join("")}</div>`).join("")}<div class="note">Tip: add a toy, category or time period to any question.</div></div></div>`;
  renderSmart();const l=document.getElementById("chatlog");if(chat.length)l.scrollTop=l.scrollHeight;
}
function ask(text,instant){
  if(askBusy&&!instant)return;
  const inp=document.getElementById("askin");const q=(text??inp?.value??"").trim();if(!q)return;
  chat.push({html:`<div class="msg u">${esc(q)}</div>`});while(chat.length>60)chat.shift();
  const done=async()=>{let pre=null;if(SMART.state=="on"&&!UNSUP.test(q)&&!/\bwhy\b/i.test(q)){try{pre=await decide(q)}catch(e){pre=null}}chat.pop();chat.push({html:answer(q,pre)});askBusy=false;renderAsk()};
  if(instant){chat.push({html:""});done();return}
  askBusy=true;const steps=["Reading your question…","Matching it to an approved calculation…","Computing from the CSVs…"];
  const tp=s=>`<div class="msg a typing"><span></span><span></span><span></span><i class="stp">${s}</i></div>`;
  chat.push({html:tp(steps[0])});renderAsk();
  steps.slice(1).forEach((s,k)=>setTimeout(()=>{if(askBusy){chat[chat.length-1].html=tp(s);renderAsk()}},(k+1)*380));
  setTimeout(done,steps.length*380);
}
const chips=(arr)=>`<div class="sugg">${arr.map(t=>`<button class="chip" onclick="ask(this.textContent)">${esc(t)}</button>`).join("")}</div>`;
function answer(q,pre){
  const slots=parseSlots(q);
  const FOLLOW=/^\s*(and|what about|how about|same|now|ok|okay|then|what if|also|instead|just)\b/i;
  const metric=METRICW.test(q);
  if(UNSUP.test(q)) return `<div class="msg a"><div class="who"><span class="bot">${ILLUS[34]}</span>Toy-Box Analyst</div><b>I can't answer that from this dataset.</b> It has sales, toys, stores and a stock snapshot, but no customer, survey, review, promotion or forecast data. Closest things I can answer:${chips(["Which toys generated the most profit?","How has revenue changed over time?","How does 2023 compare with 2022?"])}</div>`;
  if(/\bwhy\b/i.test(q)) return `<div class="msg a"><div class="who"><span class="bot">${ILLUS[34]}</span>Toy-Box Analyst</div><b>I can show you <i>what</i> changed, but not <i>why</i>.</b> The data has no information about causes like promotions or supply problems. I can show where the change happened:${chips(["How has revenue changed over time?","How does 2023 compare with 2022?","Which category has the best gross margin?"])}</div>`;
  if(AMBIG.test(q)&&!metric&&/\b(toy|toys|product|products)\b/i.test(q)) return `<div class="msg a"><div class="who"><span class="bot">${ILLUS[34]}</span>Toy-Box Analyst</div>“Best” can mean different things. Which do you mean?${chips(["What were the best-selling toys?","Which toys generated the most profit?","Which toys brought in the most revenue?"])}</div>`;
  let {best,score,near,via}=pre||match2(q);const thr=via=="embedding"?EMB_MIN:MATCH_MIN;
  const isFollow=!!lastAsk&&slots.chips.length>0&&(!best||score<thr||FOLLOW.test(q));
  if(isFollow){best=lastAsk.q;near=[best,...best.rel.map(id=>QI[id])]}
  const ctx=isFollow?{m0:0,m1:20,...lastAsk.slots,...slots}:{m0:0,m1:20,...slots};
  if(isFollow){const key=c=>c.split(":")[0];const mine=new Set(slots.chips.map(key));slots.chips=[...slots.chips,...lastAsk.chips.filter(c=>!mine.has(key(c)))]}
  if(!isFollow&&(!best||score<thr)) return `<div class="msg a"><div class="who"><span class="bot">${ILLUS[34]}</span>Toy-Box Analyst</div>I'm not sure I have an approved answer for that. Did you mean one of these?${chips(near.map(x=>x.title))}</div>`;
  if(best.needs=="pid"&&!ctx.pid) return `<div class="msg a"><div class="who"><span class="bot">${ILLUS[34]}</span>Toy-Box Analyst</div>Which toy do you mean?${chips(["Lego Bricks","Colorbuds","Rubik's Cube","Nerf Gun","Monopoly","Jenga"].map(n=>`Which stores sell the most ${n}?`))}</div>`;
  const r=best.run(ctx);
  if(r)lastAsk={q:best,slots:{...ctx},chips:[...slots.chips]};
  if(!r) return `<div class="msg a"><div class="who"><span class="bot">${ILLUS[34]}</span>Toy-Box Analyst</div>I understood this as <b>${best.title}</b>, but there are no sales for that combination${slots.chips.length?` (${slots.chips.join(", ")})`:""}. Try a wider time period.${chips(near.map(x=>x.title))}</div>`;
  let chart="";
  if(r.chart=="line") chart=line(r.series,{w:600,h:200,fmt:r.fmt,labels:i=>mlabel(i+r.offset)});
  else if(r.chart=="cards") chart=`<div class="bignum">${r.cards.map(c=>`<div><span style="font-size:12px;color:var(--ink2);font-weight:700">${c.l}</span><b class="${c.v>=0?"up":"down"}">${c.v>=0?"▲":"▼"} ${Math.abs(c.v).toFixed(1)}%</b></div>`).join("")}</div>`;
  else chart=hbars(r.rows,{w:600,fmt:r.fmt});
  const follow=[...best.rel.map(id=>QI[id].title)];
  const extra=[];if(!ctx.period&&best.needs!="pid"&&best.id!="yoy"&&best.id!="low_stock"&&best.id!="zero_stock")extra.push(best.title.replace(/\?$/,"")+" last quarter?");if(!ctx.cats&&best.needs!="pid"&&!["low_stock","zero_stock"].includes(best.id))extra.push(best.title.replace(/\?$/,"")+" in Games?");
  return `<div class="msg a"><div class="who"><span class="bot">${ILLUS[34]}</span>Toy-Box Analyst</div>
    <div style="font-size:12px;color:var(--ink2);margin-bottom:6px">${isFollow?"Following up on your last question. ":""}${via=="embedding"?"🧠 Matched by the in-browser model. ":""}I understood this as: <b>${best.title}</b>${slots.chips.length?`<br>${slots.chips.map(c=>`<span class="slot">${esc(c)}</span>`).join("")}`:""}</div>${esc(r.text)}
    <div style="margin:6px 0">${chart}</div>
    <div class="meta"><span class="ok">✓ Approved question</span> · computed live from the CSVs · Source: ${r.src}<br><b>How it's calculated:</b> ${r.def}
    <button class="btn" style="margin-left:8px" onclick='csvDownload("answer.csv",[${JSON.stringify(r.cols)},...${JSON.stringify(r.rows.map(x=>[x.label,x.v]))}])'>⬇ Download CSV</button></div>
    ${chips([...follow,...extra].slice(0,4))}</div>`;
}



