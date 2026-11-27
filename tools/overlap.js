const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('http://127.0.0.1:8765/index.html');await p.waitForFunction(()=>document.getElementById('tex').complete);await p.evaluate(()=>document.fonts.ready);
if(process.argv[2])await p.evaluate(r=>{const [a,b]=r.split(',').map(Number);window.__T0=a;window.__T1=b;},process.argv[2]);
const res=await p.evaluate(()=>{window.__noSat=true;const out=[];const ov=(a,b,m=4)=>a.x<b.x+b.w-m&&b.x<a.x+a.w-m&&a.y<b.y+b.h-m&&b.y<a.y+a.h-m;const inside=(a,b)=>a.x>=b.x-2&&a.y>=b.y-2&&a.x+a.w<=b.x+b.w+2&&a.y+a.h<=b.y+b.h+2;
 const html=id=>{const e=document.getElementById(id);if(!e||+getComputedStyle(e).opacity<0.5)return null;const r=(id==='fact'||id==='logo'||id==='count')?e.getBoundingClientRect():null;return r?{k:'html',t:id,x:r.x,y:r.y,w:r.width,h:r.height}:null;};
 const DUR=window.__DUR||638.2,T0=window.__T0||0,T1=window.__T1||DUR;for(let t=T0;t<=T1;t+=0.2){window.__render(t);const full=['chap','title','sub'].some(id=>{const e=document.getElementById(id);return e&&+e.style.opacity>0.3});if(full)continue;
  const B=window.__boxes.slice();const H=['fact','logo','count'].map(html).filter(Boolean);const panels=B.filter(x=>x.k==='panel'),T=B.filter(x=>x.k!=='panel');
  for(const a of T){const inP=panels.some(pn=>inside(a,pn));
   if(a.x<8||a.y<8||a.x+a.w>1912||a.y+a.h>1072)out.push([+t.toFixed(1),'OFF-FRAME',a.t]);
   for(const h of H)if(ov(a,h))out.push([+t.toFixed(1),'UNDER '+h.t,a.t]);
   if(!inP)for(const pn of panels)if(ov(a,pn))out.push([+t.toFixed(1),'ON PANEL '+pn.t,a.t]);}
  for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++)if(ov(T[i],T[j]))out.push([+t.toFixed(1),'TEXT/TEXT',T[i].t+'  ×  '+T[j].t]);}
 return out;});
// group into ranges
const g={};for(const [t,k,x] of res){const key=k+' | '+x;(g[key]=g[key]||[]).push(t);}
const rows=[];for(const [key,ts] of Object.entries(g)){let s=ts[0],e=ts[0];for(const t of ts.slice(1)){if(t-e>0.45){rows.push([s,e,key]);s=t;}e=t;}rows.push([s,e,key]);}
rows.sort((a,b)=>a[0]-b[0]);const fmt=t=>`${Math.floor(t/60)}:${(t%60).toFixed(1).padStart(4,'0')}`;
for(const [s,e,k] of rows)console.log(`${fmt(s)}-${fmt(e)}  (${(e-s+0.2).toFixed(1)}s)  ${k}`);console.log('TOTAL ranges:',rows.length);await b.close();})();
