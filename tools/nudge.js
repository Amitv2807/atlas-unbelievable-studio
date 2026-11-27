// Suggest offsets for labels flagged by overlap.js: node nudge.js "LABEL|T0|T1" ...   (episode served on :8765)
// Prints SHIFT entries: the smallest move that keeps the label clear of lines, icons, panels, other text and the frame across T0..T1.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('http://127.0.0.1:8765/index.html');await p.waitForFunction(()=>document.getElementById('tex').complete);await p.evaluate(()=>document.fonts.ready);
for(const arg of process.argv.slice(2)){const [lab,t0,t1]=arg.split('|');
 const r=await p.evaluate(([lab,t0,t1])=>{window.__noSat=true;const S=window.__SHIFT();const base=S[lab]?S[lab].slice():[0,0];
  const ov=(a,b,m=4)=>a.x<b.x+b.w-m&&b.x<a.x+a.w-m&&a.y<b.y+b.h-m&&b.y<a.y+a.h-m;
  const seg=(p,q,b)=>{const m=4,x0=b.x+m,y0=b.y+m,x1=b.x+b.w-m,y1=b.y+b.h-m;let a0=0,a1=1;const dx=q[0]-p[0],dy=q[1]-p[1];for(const [pp,qq] of [[-dx,p[0]-x0],[dx,x1-p[0]],[-dy,p[1]-y0],[dy,y1-p[1]]]){if(pp===0){if(qq<0)return false;}else{const rr=qq/pp;if(pp<0){if(rr>a1)return false;if(rr>a0)a0=rr;}else{if(rr<a0)return false;if(rr<a1)a1=rr;}}}return true;};
  const snaps=[];for(let t=+t0;t<=+t1+1e-6;t+=0.4){window.__render(t);const B=window.__boxes.slice(),me=B.find(x=>x.t===lab&&x.k!=='panel');if(!me)continue;
   const html=['fact','logo','count'].map(id=>{const e=document.getElementById(id);if(!e||+getComputedStyle(e).opacity<0.5)return null;const q=e.getBoundingClientRect();return {x:q.x,y:q.y,w:q.width,h:q.height};}).filter(Boolean);
   snaps.push({me:{...me},others:B.filter(x=>x!==me&&!(x.k==='txt'&&x.inP&&B.some(pn=>pn.k==='panel'&&ov(x,pn)&&false))),lines:window.__lines.slice(),html});}
  if(!snaps.length)return {lab,err:'not seen'};
  const cand=[];for(let r=0;r<=360;r+=20)for(let k=0;k<16;k++){const an=k*Math.PI/8;const d=[Math.round(r*Math.cos(an)),Math.round(r*Math.sin(an))];if(r===0&&k)continue;cand.push(d);}
  for(const [dx,dy] of cand){let ok=true;for(const s of snaps){const b={...s.me,x:s.me.x+dx,y:s.me.y+dy};
    if(b.x<16||b.y<16||b.x+b.w>1904||b.y+b.h>1064){ok=false;break;}
    if(s.html.some(h=>ov(b,h))){ok=false;break;}
    if(s.others.some(o=>o.k!=='txt'||!o.inP?ov(b,o,-6):ov(b,o))){ok=false;break;}
    if(s.lines.some(L=>{for(let i=0;i<L.length-1;i++)if(seg(L[i],L[i+1],b))return true;return false;})){ok=false;break;}}
   if(ok)return {lab,shift:[base[0]+dx,base[1]+dy],move:[dx,dy]};}
  return {lab,err:'no clear spot within 360px'};},[lab,t0,t1]);
 console.log(JSON.stringify(r));}
await b.close();})();
