// Capture frames of a canvas episode for a time range with N parallel browsers (episode served on :8765).
// node capture.js T0 T1 OUT_DIR [WORKERS=4] [FPS=30]   -> OUT_DIR/frame_%06d.jpg numbered from frame 0 of the episode
// Frames that already exist are skipped, so a stopped capture can resume.
const {chromium}=require('playwright');const fs=require('fs');
const [T0,T1,OUT,WK='4',FPS='30']=process.argv.slice(2);const fps=+FPS,f0=Math.round(+T0*fps),f1=Math.round(+T1*fps),nw=+WK;fs.mkdirSync(OUT,{recursive:true});
const name=f=>`${OUT}/frame_${String(f).padStart(6,'0')}.jpg`;
(async()=>{let done=0;const t0=Date.now();
 await Promise.all([...Array(nw).keys()].map(async w=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});p.on('pageerror',e=>console.log('pageerror',e.message));
  await p.goto('http://127.0.0.1:8765/index.html');await p.waitForFunction(()=>[...document.images].every(i=>i.complete));await p.evaluate(()=>document.fonts.ready);
  await p.evaluate(()=>window.__render(0));
  for(let f=f0+w;f<f1;f+=nw){if(fs.existsSync(name(f)))continue;await p.evaluate(t=>window.__render(t),f/fps);await p.screenshot({path:name(f),type:'jpeg',quality:88});
   if(++done%600===0){const s=(Date.now()-t0)/1000;console.log(`${done}/${f1-f0} frames, ${(done/s).toFixed(1)} fps`);}}
  await b.close();}));console.log('CAPTURE DONE',f0,f1);})();
