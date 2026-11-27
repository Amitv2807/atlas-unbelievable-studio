"""Generate vertical Shorts projects from the Episode 1 composition.
python make_shorts.py PLAN.json EP_DIR OUT_DIR WORDS.json MIX.wav"""
import json, os, re, sys, subprocess, shutil
plan_p, ep, outd, words_p, mix = sys.argv[1:6]
SH = json.load(open(plan_p)); W = json.load(open(words_p))
src = open(os.path.join(ep, "index.html")).read()
EP_PLAN = json.load(open(os.path.join(ep, "assets/plan.json")))
FIX = {"barla": "Baarle", "barla,": "Baarle,", "lowe's": "Los", "angels.": "Angeles."}
HIRES = []
for f in sorted(os.listdir(os.path.join(ep, "assets/hires"))):
    if f.endswith(".json"):
        j = json.load(open(os.path.join(ep, "assets/hires", f))); HIRES.append({"n": f[:-5], "b": j["bbox"], "w": j["w"], "h": j["h"]})

def must(s, a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); return s.replace(a, b)

def template():
    s = src
    s = must(s, "html,body{margin:0;width:1920px;height:1080px;", "html,body{margin:0;width:1080px;height:1920px;")
    s = must(s, "#root{position:relative;width:1920px;height:1080px;", "#root{position:relative;width:1080px;height:1920px;")
    s = must(s, '<canvas id="cv" width="1920" height="1080"></canvas>', '<canvas id="cv" width="1080" height="1920"></canvas>' + "".join(
        f'<img id="hr_{h["n"]}" class="hr" src="assets/hires/{h["n"]}.jpg" alt="">' for h in HIRES))
    s = must(s, "const W=1920,H=1080,CX=960,CY=540,", "const W=1080,H=1920,CX=540,CY=820,")
    # wider framing in a narrow frame
    s = must(s, " return{lon,lat,R:Math.exp(lr)};}",
             " {const R0=Math.exp(lr);const k=R0<=700?1:R0>=2000?0.62:1-0.38*Math.log(R0/700)/Math.log(2000/700);return{lon,lat,R:R0*k};}}")
    # sharp regional textures
    i = s.index("const OW=960,OH=540,"); j = s.index("// ---------- camera ----------")
    s = s[:i] + r"""const REG=window.HIRES.map(h=>Object.assign({},h));
function loadRegs(){for(const r of REG){if(r.data)continue;const im=document.getElementById('hr_'+r.n);if(!im||!im.complete||!im.naturalWidth)continue;const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const x=c.getContext('2d');x.drawImage(im,0,0);r.data=x.getImageData(0,0,c.width,c.height).data;r.w=c.width;r.h=c.height;}}
const normLon=l=>((l+540)%360+360)%360-180;
function regAt(lon,lat){lon=normLon(lon);for(const r of REG)if(r.data&&lon>=r.b[0]&&lon<=r.b[2]&&lat>=r.b[1]&&lat<=r.b[3])return r;return null;}
const OFF={};function offFor(sc){if(!OFF[sc]){const c=document.createElement('canvas');c.width=Math.round(W*sc);c.height=Math.round(H*sc);const x=c.getContext('2d');OFF[sc]={c,x,img:x.createImageData(c.width,c.height)};}return OFF[sc];}
function drawSat(c,alpha){
 if(!TEX||alpha<=0||window.__noSat)return;loadRegs();const hr=c.R>2500&&regAt(c.lon,c.lat);const sc=hr?0.75:0.5,o=offFor(sc),OW=o.c.width,OH=o.c.height,d=o.img.data,R=c.R*sc,cx=CX*sc,cy=CY*sc;
 const p0=c.lat*D2R,sp=Math.sin(p0),cp=Math.cos(p0),l0=c.lon*D2R;
 for(let y=0;y<OH;y++){const py=(cy-y)/R;for(let x=0;x<OW;x++){const i=(y*OW+x)*4,px=(x-cx)/R,r2=px*px+py*py;
  if(r2>=1){d[i+3]=0;continue}const z=Math.sqrt(1-r2);
  const lat=Math.asin(clamp(z*sp+py*cp,-1,1)),lon=l0+Math.atan2(px,z*cp-py*sp),sh=0.45+0.55*Math.pow(z,0.6);
  const rg=hr?regAt(lon/D2R,lat/D2R):null;
  if(rg){const Dt=rg.data,RW=rg.w,RH=rg.h;let u=(normLon(lon/D2R)-rg.b[0])/(rg.b[2]-rg.b[0])*RW-0.5,v=(rg.b[3]-lat/D2R)/(rg.b[3]-rg.b[1])*RH-0.5;u=clamp(u,0,RW-1.001);v=clamp(v,0,RH-1.001);
   const u0=Math.floor(u),v0=Math.floor(v),fu=u-u0,fv=v-v0,a=(v0*RW+u0)*4,b=a+4,cc=a+RW*4,dd=cc+4;
   const ex=Math.min(u,RW-1-u)/RW,ey=Math.min(v,RH-1-v)/RH,wE=Math.min(1,Math.min(ex,ey)/0.08);
   let gu=((lon/(2*Math.PI)+0.5)%1+1)%1*TW-0.5,gv=clamp((0.5-lat/Math.PI)*TH-0.5,0,TH-1.001);const g0=Math.floor(gu),h0=Math.floor(gv),gfu=gu-g0,gfv=gv-h0,ga=(h0*TW+((g0+TW)%TW))*4,gb=(h0*TW+((g0+1)%TW))*4,gc=ga+TW*4,gd=gb+TW*4;
   for(let k=0;k<3;k++){const hv=((Dt[a+k]*(1-fu)+Dt[b+k]*fu)*(1-fv)+(Dt[cc+k]*(1-fu)+Dt[dd+k]*fu)*fv)*(0.75+0.25*sh)*1.05;
    const gvv=wE<1?((TEX[ga+k]*(1-gfu)+TEX[gb+k]*gfu)*(1-gfv)+(TEX[gc+k]*(1-gfu)+TEX[gd+k]*gfu)*gfv)*sh*1.12:0;d[i+k]=Math.min(255,hv*wE+gvv*(1-wE));}
   d[i+3]=255*alpha;continue;}
  let u=((lon/(2*Math.PI)+0.5)%1+1)%1*TW-0.5,v=(0.5-lat/Math.PI)*TH-0.5;if(v<0)v=0;if(v>TH-1.001)v=TH-1.001;
  const u0=Math.floor(u),v0=Math.floor(v),fu=u-u0,fv=v-v0,u1=(u0+1)%TW,uu=(u0+TW)%TW;
  const a=(v0*TW+uu)*4,b=(v0*TW+u1)*4,cc=((v0+1)*TW+uu)*4,dd=((v0+1)*TW+u1)*4;
  for(let k=0;k<3;k++){d[i+k]=Math.min(255,((TEX[a+k]*(1-fu)+TEX[b+k]*fu)*(1-fv)+(TEX[cc+k]*(1-fu)+TEX[dd+k]*fu)*fv)*sh*1.12);}
  d[i+3]=255*alpha;}}
 o.x.putImageData(o.img,0,0);ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';ctx.drawImage(o.c,0,0,W,H);}
""" + s[j:]
    s = must(s, "const satA=1-ramp(Math.log(c.R),Math.log(9000),Math.log(30000));",
             "loadRegs();const satA=regAt(c.lon,c.lat)?1-ramp(Math.log(c.R),Math.log(150000),Math.log(400000)):1-ramp(Math.log(c.R),Math.log(9000),Math.log(30000));")
    # panels -> slot below the map
    s = must(s, "function panel(x,y,w,h,a,title){if(a<=0)return;if(a>0.5)window.__boxes.push({k:'panel',t:title||'panel',x,y,w,h});",
             "let PT=null;function PB(x,y,w,h){const s=Math.min(980/w,440/h,1.25),tx=540-(x+w/2)*s,ty=1090-(y+h/2)*s;ctx.save();ctx.setTransform(s,0,0,s,tx,ty);PT={s,tx,ty};}function PE(){ctx.restore();PT=null;}\n"
             "const MB=b=>PT?{k:b.k,t:b.t,inP:b.inP,x:b.x*PT.s+PT.tx,y:b.y*PT.s+PT.ty,w:b.w*PT.s,h:b.h*PT.s}:b;\n"
             "function panel(x,y,w,h,a,title){if(a<=0)return;if(a>0.5)window.__boxes.push(MB({k:'panel',t:title||'panel',x,y,w,h}));")
    s = must(s, "if((o.a??1)>0.5)window.__boxes.push({k:'pill',t:txt,x:x0,y:y0,w:pw,h:ph,inP:!!o.inP});",
             "if((o.a??1)>0.5)window.__boxes.push(MB({k:'pill',t:txt,x:x0,y:y0,w:pw,h:ph,inP:!!o.inP}));")
    out = []; pos = 0
    for m in re.finditer(r"(?<!function )panel\((x,y,w,h|bx,by,bw,200),", s):
        st = m.start(); depth = 0; k = st
        while True:
            k -= 1; ch = s[k]
            if ch == "}": depth += 1
            elif ch == "{":
                if depth == 0: break
                depth -= 1
        bs = k; depth = 0; e = bs
        while True:
            e += 1; ch = s[e]
            if ch == "{": depth += 1
            elif ch == "}":
                if depth == 0: break
                depth -= 1
        out.append((st, e, m.group(1)))
    for st, e, args in sorted(out, reverse=True):
        rect = args if args != "bx,by,bw,200" else "bx,by,bw,200"
        s = s[:e] + "PE();" + s[e:]
        s = s[:st] + f"PB({rect});" + s[st:]
    s = must(s, "px=1560+(1-k)*500,py=470,pr=200", "px=790+(1-k)*400,py=520,pr=150")
    # fixed info pills and big numbers
    for a_, b_ in [("pill(560,860,", "pill(540,1370,"), ("pill(560,940,", "pill(540,1440,"), ("pill(1600,330,", "pill(540,1370,"),
                   ("pill(1600,420,", "pill(540,1440,"), ("pill(CX,960,", "pill(540,1370,")]:
        s = s.replace(a_, b_)
    s = re.sub(r"bigText\(CX,(930|960|900),", "bigText(CX,340,", s)
    # zones for shorts + disable episode overlays
    s = must(s, "ZONES.length=0;{let f0=0;", "ZONES.length=0;if(window.__SHORT){for(const z of window.__SHORT.zones)ZONES.push(z);}else{let f0=0;")
    s = must(s, " let fi=0;for(let i=1;i<=25;i++)if(t>=S[i])fi=i;", " if(!window.__SHORT){let fi=0;for(let i=1;i<=25;i++)if(t>=S[i])fi=i;")
    s = must(s, "document.getElementById('logo').style.opacity=.85*(1-ca)*(1-win(t,21.6,25.7,.5,.5));",
             "document.getElementById('logo').style.opacity=.85*(1-ca)*(1-win(t,21.6,25.7,.5,.5));}")
    # vertical-only label tweaks (narrower frame)
    for a_, b_ in [("window.__boxes.push({k:'big',t:txt,x:x-tw/2,y:y-size*0.6,w:tw,h:size*1.2});", "window.__boxes.push(MB({k:'big',t:txt,x:x-tw/2,y:y-size*0.6,w:tw,h:size*1.2}));"),
                   ("lab(BL,'SCHOOL · BLAINE, WA',230,64,", "lab(BL,'SCHOOL · BLAINE, WA',110,150,"),
                   ("lab([4.6,51.25],'BELGIUM',0,0,", "lab([4.45,51.42],'BELGIUM',0,0,"),
                   ("lab([4.7,51.62],'NETHERLANDS',-60,0,", "lab([5.4,51.74],'NETHERLANDS',0,0,"),
                   ("[[67,48],'KAZAKHSTAN'],[[76,41.9],'KYRGYZSTAN'],[[71.5,38.3],'TAJIKISTAN'],[[66,34],'AFGHANISTAN'],[[59,39],'TURKMENISTAN']",
                    "[[68,49],'KAZAKHSTAN'],[[78.5,42.6],'KYRGYZSTAN'],[[72.5,37.2],'TAJIKISTAN'],[[66,33.2],'AFGHANISTAN'],[[57.5,38.2],'TURKMENISTAN']"),
                   ("{bd:'#9aa5b1',size:24}));}}", "{bd:'#9aa5b1',size:20}));}}"), ("lab([62.5,42.6],'UZBEKISTAN',0,0,a*ua);", "lab([60.5,41.4],'UZBEKISTAN',0,0,a*ua);")]:
        s = must(s, a_, b_)
    return s

TPL = template()
CSS = """
#fact,#logo,#count,#chap,#title,#sub{display:none!important}
#sfact{position:absolute;left:40px;right:40px;top:96px;display:flex;align-items:center;gap:18px;opacity:0;background:linear-gradient(90deg,rgba(6,12,32,.92),rgba(6,12,32,.75));border:3px solid rgba(255,210,63,.7);border-radius:24px;padding:14px 22px 14px 14px;box-shadow:0 12px 40px #000a}
#sfact .n{font:62px Anton;color:#111;background:linear-gradient(#ffe066,#ff9500);border-radius:16px;padding:2px 18px}
#sfact .h{font:46px Anton;line-height:1.02}
#hook{position:absolute;left:0;right:0;top:330px;text-align:center;opacity:0;font:104px Anton;line-height:.98;color:#fff;-webkit-text-stroke:16px #000;paint-order:stroke fill;padding:0 40px}
#hook span{color:#ffd23f}
#cap{position:absolute;left:30px;right:30px;top:1478px;text-align:center;font:96px Anton;line-height:1.02;letter-spacing:.5px}
#cap .w{display:inline-block;margin:0 12px;-webkit-text-stroke:16px #000;paint-order:stroke fill;color:#fff}
#cap .w.on{color:#ffd23f}
#endc{position:absolute;left:0;right:0;top:1490px;text-align:center;opacity:0}
#endc div{display:inline-block;font:46px Archivo;background:#ff2d2d;border:5px solid #000;border-radius:18px;padding:12px 30px;box-shadow:0 10px 30px #000b}
"""
HTML_EXTRA = '<div id="sfact"><div class="n">#1</div><div class="h">FACT</div></div><div id="hook"></div><div id="cap"></div><div id="endc"><div>FULL 10-MIN VIDEO ON THE CHANNEL</div></div>'

def words_for(segs):
    caps = []; off = 0.0
    for a, b in segs:
        for wd, ws, we in W:
            if ws >= a - 0.02 and ws < b:
                t = FIX.get(wd.lower(), wd)
                caps.append([t, round(ws - a + off, 3), round(we - a + off, 3)])
        off += b - a
    groups = []; cur = []
    for c in caps:
        cur.append(c)
        if len(cur) == 3 or c[0][-1] in ".,?!":
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    return [{"s": g[0][1], "e": g[-1][2], "w": [[x[0].upper(), x[1]] for x in g]} for g in groups]

os.makedirs(outd, exist_ok=True)
for sh in SH:
    sid = f"s{sh['id']:02d}"; d = os.path.join(outd, sid); os.makedirs(d, exist_ok=True)
    if not os.path.exists(os.path.join(d, "assets")): os.symlink(os.path.join(ep, "assets"), os.path.join(d, "assets"))
    for f in ("hyperframes.json",): shutil.copy(os.path.join(ep, f), d)
    json.dump({"id": sid, "name": sid, "width": 1080, "height": 1920, "fps": 30}, open(os.path.join(d, "meta.json"), "w"))
    segs = sh["segs"]; dur = round(sum(b - a for a, b in segs), 2); caps = words_for(segs)
    cfg = {"segs": segs, "dur": dur, "facts": sh["facts"], "hook": sh["hook"], "caps": caps,
           "zones": [{"x": 30, "y": 80, "w": 1020, "h": 190}, {"x": 20, "y": 1470, "w": 1040, "h": 130}]}
    html = TPL.replace('data-composition-id="ep1" data-start="0" data-duration="638.2" data-width="1920" data-height="1080"',
                       f'data-composition-id="{sid}" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920"')
    html = html.replace("</style>", CSS + "</style>", 1)
    html = html.replace('<div id="sub">', HTML_EXTRA + '<div id="sub">', 1)
    html = html.replace("<script>\n(function(){", "<script>window.HIRES=" + json.dumps(HIRES) + ";window.__SHORT=" + json.dumps(cfg) + ";</script>\n<script>\n(function(){", 1)
    hook = sh["hook"].split(" "); mid = len(hook) // 2
    tail = r"""
const SC=window.__SHORT;const HD=HEAD;const mapT=ts=>{let o=0;for(const [a,b] of SC.segs){if(ts<o+(b-a)||(a===SC.segs[SC.segs.length-1][0]))return a+Math.min(ts-o,b-a);o+=b-a;}return SC.segs[SC.segs.length-1][1];};
const segIdx=ts=>{let o=0;for(let i=0;i<SC.segs.length;i++){const L=SC.segs[i][1]-SC.segs[i][0];if(ts<o+L)return i;o+=L;}return SC.segs.length-1;};
document.getElementById('hook').innerHTML=HOOKHTML;
window.__renderShort=function(ts){const t=mapT(ts);SC.zones.length=2;if(ts<2.9)SC.zones.push({x:20,y:300,w:1040,h:280});render(t);
 const i=segIdx(ts),f=SC.facts[i],sf=document.getElementById('sfact');if(sf.dataset.i!=i){sf.dataset.i=i;sf.querySelector('.n').textContent='#'+(i+1);sf.querySelector('.h').textContent=HD[f];}
 let o=0;for(let k=0;k<i;k++)o+=SC.segs[k][1]-SC.segs[k][0];const L=SC.segs[i][1]-SC.segs[i][0];
 sf.style.opacity=ramp(ts,o+.15,o+.5)*(1-ramp(ts,o+L-.25,o+L));
 document.getElementById('hook').style.opacity=1-ramp(ts,2.4,2.8);document.getElementById('hook').style.transform=`scale(${.9+.1*sine(ramp(ts,0,.5))})`;
 document.getElementById('endc').style.opacity=ramp(ts,SC.dur-3,SC.dur-2.6);
 let cur=null;for(const g of SC.caps)if(ts>=g.s-.05&&ts<g.e+.25)cur=g;const cap=document.getElementById('cap');const key=cur?String(cur.s):'';
 if(cap.dataset.k!==key){cap.dataset.k=key;cap.innerHTML=cur?cur.w.map(w=>`<span class="w" data-s="${w[1]}">${w[0]}</span>`).join(' '):'';}
 cap.style.opacity=1-ramp(ts,SC.dur-3,SC.dur-2.6);
 cap.querySelectorAll('.w').forEach(el=>{const s=+el.dataset.s,k=ramp(ts,s-.05,s+.08);el.classList.toggle('on',ts>=s-.05);el.style.transform=`scale(${k<1?.85+.15*k:1})`;});};
window.__render=t=>window.__renderShort(t);
""".replace("HOOKHTML", json.dumps(" ".join(hook[:mid]) + "<br><span>" + " ".join(hook[mid:]) + "</span>"))
    html = must(html, "const tl=gsap.timeline({paused:true});const st={t:0};\ntl.to(st,{t:638.2,duration:638.2,ease:'none',onUpdate:()=>render(st.t)},0);\nrender(0);",
                tail + f"const tl=gsap.timeline({{paused:true}});const st={{t:0}};\ntl.to(st,{{t:{dur},duration:{dur},ease:'none',onUpdate:()=>window.__renderShort(st.t)}},0);\nwindow.__renderShort(0);")
    html = html.replace("window.__timelines['ep1']=tl;", f"window.__timelines['{sid}']=tl;")
    html = html.replace('<audio id="aud" data-start="0" data-duration="638.2" data-track-index="5" src="assets/mix.mp3"',
                        f'<audio id="aud" data-start="0" data-duration="{dur}" data-track-index="5" src="audio.mp3"')
    open(os.path.join(d, "index.html"), "w").write(html)
    # audio: cut the finished episode mix at the same segments, short crossfades, YouTube loudness
    parts = []
    for k, (a, b) in enumerate(segs):
        p = os.path.join(d, f"part{k}.wav"); parts.append(p)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", mix, "-af", "afade=t=in:d=0.08,afade=t=out:st=%f:d=0.12" % (b - a - 0.12), p], check=True)
    inp = sum([["-i", p] for p in parts], []); n = len(parts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", "".join(f"[{k}]" for k in range(n)) + f"concat=n={n}:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.8:level=false,afade=t=out:st={dur-0.5}:d=0.5",
                    "-ar", "48000", "-c:a", "libmp3lame", "-b:a", "256k", os.path.join(d, "audio.mp3")], check=True)
    for p in parts: os.remove(p)
    print(sid, f"{dur:.1f}s", sh["hook"], "| caps:", len(caps))
