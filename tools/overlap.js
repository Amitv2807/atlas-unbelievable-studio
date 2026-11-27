const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('http://127.0.0.1:8765/index.html');await p.waitForFunction(()=>document.getElementById('tex').complete);await p.evaluate(()=>document.fonts.ready);
if(process.argv[2])await p.evaluate(r=>{const [a,b]=r.split(',').map(Number);window.__T0=a;window.__T1=b;},process.argv[2]);
const res=await p.evaluate(()=>{window.__noSat=true;const out=[];const ov=(a,b,m=4)=>a.x<b.x+b.w-m&&b.x<a.x+a.w-m&&a.y<b.y+b.h-m&&b.y<a.y+a.h-m;const inside=(a,b)=>a.x>=b.x-2&&a.y>=b.y-2&&a.x+a.w<=b.x+b.w+2&&a.y+a.h<=b.y+b.h+2;
 const html=id=>{const e=document.getElementById(id);if(!e||+getComputedStyle(e).opacity<0.5)return null;const r=(id==='fact'||id==='logo'||id==='count')?e.getBoundingClientRect():null;return r?{k:'html',t:id,x:r.x,y:r.y,w:r.width,h:r.height}:null;};
 const DUR=window.__DUR||638.2,T0=window.__T0||0,T1=window.__T1||DUR;for(let t=T0;t<=T1;t+=0.2){window.__render(t);const full=['chap','title','sub'].some(id=>{const e=document.getElementById(id);return e&&+e.style.opacity>0.3});if(full)continue;
  const B=window.__boxes.slice(),LN=window.__lines||[];const segHit=(p,q,b)=>{const m=6,x0=b.x+m,y0=b.y+m,x1=b.x+b.w-m,y1=b.y+b.h-m;if(x1<=x0||y1<=y0)return false;let t0=0,t1=1;const dx=q[0]-p[0],dy=q[1]-p[1];for(const [pp,qq] of [[-dx,p[0]-x0],[dx,x1-p[0]],[-dy,p[1]-y0],[dy,y1-p[1]]]){if(pp===0){if(qq<0)return false;}else{const r=qq/pp;if(pp<0){if(r>t1)return false;if(r>t0)t0=r;}else{if(r<t0)return false;if(r<t1)t1=r;}}}return true;};const H=['fact','logo','count'].map(html).filter(Boolean);const panels=B.filter(x=>x.k==='panel'),IC=B.filter(x=>x.k==='icon'),T=B.filter(x=>x.k!=='panel'&&x.k!=='icon');
  for(const a of T){for(const L of LN){let hit=false;for(let i=0;i<L.length-1&&!hit;i++)hit=segHit(L[i],L[i+1],a);if(hit){out.push([+t.toFixed(1),'LINE THROUGH',a.t]);break;}}for(const ic of IC)if(ov(a,ic,2)){out.push([+t.toFixed(1),'ICON ON',a.t+'  ×  '+ic.t]);break;}}
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
