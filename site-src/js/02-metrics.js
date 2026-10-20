/* Shared metrics: agg() computes revenue, profit and units for every tab, so a number means the same thing everywhere. */
/* ---------- shared "metrics" layer: one set of definitions for every tab ---------- */
function agg({cats=null,pid=null,m0=0,m1=20}={}){
  const byMonth=Array.from({length:21},()=>({rev:0,gp:0,units:0}));
  const byProd={}, byStore={}, byCat={}, tot={rev:0,gp:0,units:0};
  for(const [sid,p,mi,u] of DATA.SMP){
    if(mi<m0||mi>m1) continue; if(pid&&p!=pid) continue; if(cats&&!cats.includes(P[p].cat)) continue;
    const r=rev(p,u),g=gp(p,u);
    const M=byMonth[mi];M.rev+=r;M.gp+=g;M.units+=u;
    const b=byProd[p]??={rev:0,gp:0,units:0};b.rev+=r;b.gp+=g;b.units+=u;
    const s=byStore[sid]??={rev:0,gp:0,units:0};s.rev+=r;s.gp+=g;s.units+=u;
    const c=byCat[P[p].cat]??={rev:0,gp:0,units:0};c.rev+=r;c.gp+=g;c.units+=u;
    tot.rev+=r;tot.gp+=g;tot.units+=u;}
  return {tot,byMonth,byProd,byStore,byCat};
}
const ALL = agg();

