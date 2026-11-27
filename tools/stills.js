const {chromium}=require('playwright');(async()=>{const times=process.argv[2].split(',').map(Number),out=process.argv[3];
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://127.0.0.1:8765/index.html');await p.waitForFunction(()=>document.getElementById('tex').complete);await p.evaluate(()=>document.fonts.ready);
for(const t of times){await p.evaluate(t=>window.__render(t),t);await p.screenshot({path:`${out}/s_${String(t).padStart(6,'0')}.jpg`,type:'jpeg',quality:70});}
console.log('errors:',errs.slice(0,5));await b.close();})();
