const {chromium}=require('playwright');(async()=>{const [ids,times,out]=[process.argv[2].split(','),process.argv[3].split(',').map(Number),process.argv[4]];
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
for(const id of ids){await p.goto(`http://127.0.0.1:8766/${id}/index.html`);await p.waitForFunction(()=>[...document.images].every(i=>i.complete));await p.evaluate(()=>document.fonts.ready);
 const dur=await p.evaluate(()=>window.__SHORT.dur);
 for(const f of times){const t=f<0?dur+f:f;await p.evaluate(t=>window.__render(t),t);await p.screenshot({path:`${out}/${id}_${String(f).replace('-','m')}.jpg`,type:'jpeg',quality:70});}}
console.log('errors:',errs.slice(0,5));await b.close();})();
