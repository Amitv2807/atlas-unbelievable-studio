"""Archive photo beats for Episode 2 -> engine/ep2/assets/media.js (+ resized copies in assets/media/) and whoosh SFX in plan.json.
Run from the repo root after plan.py:  .venv/bin/python -I episodes/ep2-geography-trap/media.py
Each beat: (pattern in episodes/.../media/, start, end, tag, caption, subline, options). Times are VO seconds (see vo/words.json)."""
import json, glob, os, re, subprocess
E = "episodes/ep2-geography-trap"; OUT = "engine/ep2/assets"; MD = os.path.join(E, "media")
CR = {c["file"]: c for c in json.load(open(os.path.join(MD, "credits.json")))}
BEATS = [
 ("Putin_and_Xi_Jinping_concluded", 13.6, 21.0, "", "XI JINPING & VLADIMIR PUTIN", "40+ meetings", {}),
 ("taiga", 101.8, 106.2, "", "SIBERIA: VAST, COLD, EMPTY", "", {}),
 ("Kremlin|Red_Square", 113.5, 120.6, "", "MOSCOW", "Moscow + St Petersburg: over 1/4 of Russia's output", {}),
 ("Lissner|Poles|Kremlin_1612|1612", 163.6, 169.6, "1610", "POLAND-LITHUANIA TAKES MOSCOW", "", {}),
 ("Poltava", 169.8, 172.3, "1708", "SWEDEN MARCHES IN", "", {}),
 ("Napoleon", 172.5, 176.7, "1812", "NAPOLEON REACHES MOSCOW", "", {}),
 ("Bundesarchiv", 176.9, 180.2, "1941", "GERMANY INVADES", "", {}),
 ("Berlin_Wall|Berliner_Mauer", 205.3, 210.3, "1989-91", "THE SOVIET BLOC COLLAPSES", "", {}),
 ("Kremlin|Red_Square", 302.3, 310.8, "", "THE KREMLIN", "reading history through the map", {"pick": 1}),
 ("Ugra", 315.7, 319.9, "1480", "END OF MONGOL RULE", "", {}),
 ("Peter", 325.3, 328.2, "1703", "PETER THE GREAT", "fights his way to the Baltic", {}),
 ("Catherine|Ekaterina|Catharine", 328.5, 331.1, "1772-95", "CATHERINE THE GREAT", "helps carve up Poland", {}),
 ("tank|Ukraine", 342.4, 351.2, "", "THE PRICE OF THE WAR", "Western estimates: well past 1 million casualties, killed and wounded", {}),
 ("horse|Mongolia", 389.2, 395.6, "", "THE OPEN STEPPE", "for 2,000 years, horsemen rode south", {}),
 ("Great_Wall|Mutianyu", 395.9, 404.4, "", "THE GREAT WALL", "an expensive answer to a geographic weakness", {}),
 ("Himalaya|iss0|ISS0", 419.2, 427.6, "", "THE HIMALAYAS", "from the International Space Station", {}),
 ("Three_Gorges", 453.3, 457.2, "", "THE YANGTZE", "Three Gorges Dam", {}),
 ("Kashgar", 571.0, 578.2, "", "KASHGAR, XINJIANG", "gateway to Central Asia", {}),
 ("Nemesis", 659.7, 663.0, "1841", "FIRST OPIUM WAR", "the Royal Navy's Nemesis destroys Chinese war junks", {}),
 ("tanker|Malacca", 682.8, 686.5, "", "THE STRAIT OF MALACCA", "about 4/5 of China's oil imports pass here", {}),
 ("Singapore_Strait|anchorage", 719.7, 724.6, "", "THE MALACCA DILEMMA", "", {}),
 ("Gwadar", 772.1, 775.6, "", "GWADAR, PAKISTAN", "", {}),
 ("Karakoram", 776.0, 782.9, "", "KARAKORAM HIGHWAY", "the overland route into Xinjiang", {}),
 ("Pasir_Panjang|container", 795.9, 804.6, "", "PORT OF SINGAPORE", "41 million+ containers in 2024", {}),
 ("Liaoning", 871.2, 876.4, "", "CHINA'S NAVY", "from coastal force to the world's largest by ship count", {}),
 ("TSMC", 909.3, 915.4, "", "TAIWAN'S CHIP INDUSTRY", "", {}),
 ("Taiwan_Strait|transit", 946.8, 951.0, "", "THE US NAVY", "more than twice China's tonnage", {}),
 ("Murmansk", 1033.4, 1039.0, "", "MURMANSK", "ice-free, but it opens onto the Arctic", {}),
 ("Bosphorus|Istanbul", 1052.9, 1056.4, "", "THE BOSPHORUS, ISTANBUL", "controlled by Turkey", {}),
 ("Vladivostok|Golden_Horn", 1080.0, 1086.2, "", "VLADIVOSTOK", "Golden Horn Bay ices over in winter", {}),
 ("icebreaker|50_Let|Pobedy", 1086.4, 1089.4, "", "ICEBREAKERS", "keep the Pacific port open", {}),
 ("Tsushima|Port_Arthur", 1106.0, 1111.8, "1905", "RUSSIA LOSES PORT ARTHUR TO JAPAN", "", {}),
 ("sea_ice|Arctic", 1123.6, 1132.2, "", "ARCTIC SEA ICE IS SHRINKING", "", {}),
 ("F-22|Elmendorf|Raptor", 1157.3, 1164.0, "", "JOINT BASE ELMENDORF-RICHARDSON", "F-22 fighters, Alaska", {}),
 ("Kitsap|submarine", 1174.0, 1184.0, "", "NAVAL BASE KITSAP", "home of Ohio-class ballistic missile submarines", {}),
 ("Longyearbyen|Svalbard", 1201.8, 1208.0, "", "SVALBARD (NORWAY)", "", {}),
 ("night|Night", 1283.1, 1289.5, "", "THE UNITED STATES", "two oceans, two neighbours", {}),
]
files = sorted(f for f in os.listdir(MD) if not f.endswith((".json", ".txt", ".mp4", ".webm")) and os.path.getsize(os.path.join(MD, f)) > 20000)
used, M, missing = {}, [], []
for pat, t0, t1, tag, cap, sub, o in BEATS:
    rx = re.compile(pat, re.I); cands = [f for f in files if rx.search(f)]
    if o.get("file"): cands = [o["file"]]
    k = o.get("pick", 0); f = cands[k] if len(cands) > k else (cands[0] if cands else None)
    if not f: missing.append(cap); continue
    mid = re.sub(r"\W+", "", os.path.splitext(f)[0])[:40]
    if mid not in used:
        dst = os.path.join(OUT, "media", mid + ".jpg")
        if not os.path.exists(dst):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(MD, f), "-vf", "scale='min(2400,iw)':-2", "-q:v", "3", dst], check=True)
        used[mid] = f
    c = CR.get(f, {}); auth = re.sub(r"\s+", " ", c.get("author", ""))[:60]
    cr = f"{auth} · {c.get('license','')}" if c else ""
    M.append({"id": mid, "t0": t0, "t1": t1, "tag": tag, "cap": cap, "sub": sub, "cr": cr, **{k2: v for k2, v in o.items() if k2 not in ("pick", "file")}})
open(os.path.join(OUT, "media.js"), "w").write("window.MEDIA=" + json.dumps(M, ensure_ascii=False) + ";\n")
imgs = " ".join(f'<img id="m_{m}" class="hr" src="assets/media/{m}.jpg" alt="">' for m in used)
p = "engine/ep2/index.html"; s = open(p).read()
s = re.sub(r'\n?<!--media-->.*?<!--/media-->', "", s, flags=re.S)
s = s.replace('<div id="logo">', f'<!--media-->{imgs}<!--/media-->\n <div id="logo">', 1)
open(p, "w").write(s)
pj = os.path.join(OUT, "plan.json"); P = json.load(open(pj)); z = [t for t in P["SFX"].get("zoom", []) if t not in P.get("_mz", [])]
mz = [round(m["t0"] - 0.25, 2) for m in M]; P["SFX"]["zoom"] = sorted(z + mz); P["_mz"] = mz; json.dump(P, open(pj, "w"))
cred = sorted({f"{c['title']} — {c['author']} — {c['license']} — {c['source']}" for f in used.values() for c in [CR.get(f)] if c})
open(os.path.join(E, "media-credits.txt"), "w").write("\n".join(cred) + "\n")
print(len(M), "beats,", len(used), "images; missing:", missing)
