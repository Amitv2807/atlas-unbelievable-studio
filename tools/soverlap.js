const {chromium}=require('playwright');(async()=>{const ids=process.argv[2].split(',');const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const id of ids){await p.goto(`http://127.0.0.1:8766/${id}/index.html`);await p.waitForFunction(()=>[...document.images].every(i=>i.complete));await p.evaluate(()=>document.fonts.ready);
const res=await p.evaluate(()=>{window.__noSat=true;const out=[];const ov=(a,b,m=4)=>a.x<b.x+b.w-m&&b.x<a.x+a.w-m&&a.y<b.y+b.h-m&&b.y<a.y+a.h-m;const inside=(a,b)=>a.x>=b.x-2&&a.y>=b.y-2&&a.x+a.w<=b.x+b.w+2&&a.y+a.h<=b.y+b.h+2;
 const html=id=>{const e=document.getElementById(id);if(+getComputedStyle(e).opacity<0.5||!e.textContent.trim())return null;const r=e.getBoundingClientRect();return {k:'html',t:id,x:r.x,y:r.y,w:r.width,h:r.height};};
 const capBox=()=>{const sp=[...document.querySelectorAll('#cap .w')];if(!sp.length||+document.getElementById('cap').style.opacity<0.5)return null;let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;for(const s of sp){const r=s.getBoundingClientRect();x0=Math.min(x0,r.x);y0=Math.min(y0,r.y);x1=Math.max(x1,r.right);y1=Math.max(y1,r.bottom);}return {k:'html',t:'captions',x:x0,y:y0,w:x1-x0,h:y1-y0};};
 for(let t=0;t<=window.__SHORT.dur;t+=0.2){window.__render(t);const B=window.__boxes.slice();const H=['sfact','hook','endc'].map(html).concat([capBox()]).filter(Boolean);const panels=B.filter(x=>x.k==='panel'),T=B.filter(x=>x.k!=='panel');
  for(const a of T){const inP=panels.some(pn=>inside(a,pn));if(a.x<8||a.y<8||a.x+a.w>1072||a.y+a.h>1912)out.push([+t.toFixed(1),'OFF-FRAME',a.t]);
   for(const h of H)if(ov(a,h))out.push([+t.toFixed(1),'UNDER '+h.t,a.t]);if(!inP)for(const pn of panels)if(ov(a,pn))out.push([+t.toFixed(1),'ON PANEL',a.t]);}
  for(const pn of panels)for(const h of H)if(ov(pn,h))out.push([+t.toFixed(1),'PANEL UNDER '+h.t,pn.t]);
  for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++)if(ov(T[i],T[j]))out.push([+t.toFixed(1),'TEXT/TEXT',T[i].t+' × '+T[j].t]);}
 return out;});
const g={};for(const [t,k,x] of res){const key=k+' | '+x;(g[key]=g[key]||[]).push(t);}
for(const [key,ts] of Object.entries(g)){let s=ts[0],e=ts[0];const rows=[];for(const t of ts.slice(1)){if(t-e>0.45){rows.push([s,e]);s=t;}e=t;}rows.push([s,e]);for(const [a,c] of rows)console.log(`${id} ${a.toFixed(1)}-${c.toFixed(1)}s  ${key}`);}}
await b.close();})();
