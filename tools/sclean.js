const {chromium}=require('playwright');(async()=>{const plan=JSON.parse(process.argv[2]),out=process.argv[3];
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const [id,t] of plan){await p.goto(`http://127.0.0.1:8766/${id}/index.html`);await p.waitForFunction(()=>[...document.images].every(i=>i.complete));await p.evaluate(()=>document.fonts.ready);
 await p.evaluate(t=>{window.__render(t);for(const id of ['sfact','cap','hook','endc'])document.getElementById(id).style.visibility='hidden';},t);
 await p.screenshot({path:`${out}/bg_${id}.png`});}
await b.close();})();
