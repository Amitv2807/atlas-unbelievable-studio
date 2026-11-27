const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('http://127.0.0.1:8765/index.html');await p.evaluate(()=>document.fonts.ready);
for(const t of process.argv[2].split(',').map(Number)){const r=await p.evaluate(t=>{window.__noSat=true;window.__render(t);return window.__boxes.map(x=>`${x.t.slice(0,28).padEnd(28)} x${Math.round(x.x)} y${Math.round(x.y)} w${Math.round(x.w)} h${Math.round(x.h)}`)},t);console.log('t='+t+'\n  '+r.join('\n  '));}
await b.close();})();
