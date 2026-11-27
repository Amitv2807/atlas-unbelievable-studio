const {chromium}=require('playwright');(async()=>{const T=require('path').resolve(process.argv[2]||'.');const ids=require(T+'/ids.json');const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+T+'/thumbs.html');await p.evaluate(()=>document.fonts.ready);await p.waitForFunction(()=>true);
for(const id of ids){const el=await p.$('#'+id);await el.scrollIntoViewIfNeeded();await el.screenshot({path:`${T}/thumb_${id}.png`});}
for(const id of ids){const w=await p.evaluate(id=>{const e=document.querySelector('#'+id+' .l2');return e.scrollWidth>e.clientWidth+2||e.getBoundingClientRect().width>1030;},id);if(w)console.log('overflow',id);}
await b.close();})();
