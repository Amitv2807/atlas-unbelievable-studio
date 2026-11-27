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
 ("x", 389.2, 395.6, "", "MONGOLIA'S OPEN STEPPE", "for 2,000 years, horsemen rode south toward China", {"file": "PIA10613.jpg"}),
 ("Great_Wall|Mutianyu", 395.9, 404.4, "", "THE GREAT WALL", "an expensive answer to a geographic weakness", {}),
 ("iss070e091714", 419.2, 427.6, "", "THE HIMALAYAS", "from the International Space Station", {}),
 ("x", 446.6, 452.9, "1963", "THE TIBETAN PLATEAU", "the water tower of Asia · photographed from Mercury-Atlas 9", {"file": "s63-06440.jpg"}),
 ("x", 571.0, 578.2, "", "XINJIANG", "deserts of the far northwest · Lop Nur from orbit", {"file": "GSFC_20171208_Archive_e001892.jpg"}),
 ("Nemesis", 659.7, 663.0, "1841", "FIRST OPIUM WAR", "the Royal Navy's Nemesis destroys Chinese war junks", {}),
 ("x", 682.8, 686.5, "", "THE STRAIT OF MALACCA", "Sumatra and Singapore from the Space Shuttle", {"file": "s43-151-238.jpg"}),
 ("Singapore_Strait|anchorage", 719.7, 724.6, "", "THE MALACCA DILEMMA", "", {}),
 ("x", 772.1, 775.6, "", "PAKISTAN'S COAST NEAR GWADAR", "", {"file": "GSFC_20171208_Archive_e000108.jpg"}),
 ("x", 776.0, 782.9, "", "THE KARAKORAM", "the overland route into Xinjiang crosses these mountains", {"file": "iss069e060266.jpg"}),
 ("Pasir_Panjang|container", 795.9, 804.6, "", "PORT OF SINGAPORE", "41 million+ containers in 2024", {}),
 ("Liaoning", 871.2, 876.4, "", "CHINA'S NAVY", "from coastal force to the world's largest by ship count", {}),
 ("x", 906.0, 911.8, "", "THE TAIWAN STRAIT AT NIGHT", "from the International Space Station", {"file": "iss072e435710.jpg"}),
 ("Taiwan_Strait|transit", 946.8, 951.0, "", "THE US NAVY", "more than twice China's tonnage", {}),
 ("Murmansk", 1033.4, 1039.0, "", "MURMANSK", "ice-free, but it opens onto the Arctic", {}),
 ("x", 1052.9, 1056.4, "", "THE BOSPHORUS, ISTANBUL", "controlled by Turkey", {"file": "iss072e574770.jpg"}),
 ("x", 1080.0, 1086.2, "", "VLADIVOSTOK", "Golden Horn Bay ices over in winter", {"file": "PIA16290.jpg"}),
 ("icebreaker|50_Let|Pobedy", 1086.4, 1089.4, "", "ICEBREAKERS", "keep the Pacific port open", {}),
 ("Tsushima|Port_Arthur", 1106.0, 1111.8, "1905", "RUSSIA LOSES PORT ARTHUR TO JAPAN", "", {}),
 ("GSFC_20171208", 1123.6, 1132.2, "", "ARCTIC SEA ICE IS SHRINKING", "ice-free summers expected before 2050", {"kb": [0.6, 0.5, 1.25, 0.8, 0.6, 1.35]}),
 ("x", 1157.3, 1164.0, "", "ANCHORAGE, ALASKA", "home of Joint Base Elmendorf-Richardson and its F-22s", {"file": "PIA02675.jpg"}),
 ("x", 1174.0, 1184.0, "", "PUGET SOUND, WASHINGTON", "Naval Base Kitsap: Ohio-class ballistic missile submarines", {"file": "iss074e0723716.jpg"}),
 ("x", 1201.8, 1208.0, "", "LONGYEARBYEN, SVALBARD", "Norway · demilitarised by the 1920 treaty", {"file": "PIA10626.jpg"}),
 ("iss029e012564", 1283.1, 1289.5, "", "THE UNITED STATES", "two oceans, two neighbours", {}),
 ("x", 410.6, 415.0, "1969", "THE USSURI FRONTIER", "Soviet and Chinese troops clashed here · seen from Skylab", {"file": "sl4-140-4110.jpg"}),
 ("x", 430.9, 435.6, "", "THE HIMALAYAN FRONTIER", "war in 1962, deadly clashes in Galwan in 2020", {"file": "iss063e032032.jpg"}),
 ("Annamite|jungle", 490.4, 494.0, "", "JUNGLE", "", {}),
 ("Vinson|Da_Nang", 541.0, 545.4, "2018", "US CARRIER AT DA NANG", "the first since the Vietnam War", {}),
 ("054A|frigate", 958.2, 964.5, "", "FRIGATES & PATROL SHIPS", "built for nearby waters", {}),
 ("Cold_Response", 1229.0, 1235.4, "", "EXERCISE COLD RESPONSE", "NATO in the far north", {}),
 ("x", 1294.0, 1298.0, "", "THE RIO GRANDE VALLEY", "seen from Gemini 11, 1966", {"file": "s66-54558.jpg"}),
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
    c = CR.get(f, {}); auth = c.get("author", "").strip().split("\n")[0]
    auth = re.sub(r"^This [Pp]hoto was taken by\s*", "", auth); auth = re.sub(r"^\S+\.(jpe?g|png|tiff?):\s*", "", auth, flags=re.I)
    auth = re.sub(r"\s*derivative work.*", "", auth, flags=re.I); auth = "NASA/METI ASTER" if auth.startswith("NASA/GSFC/METI") else ("NASA " + auth if auth in ("JSC", "GSFC") else auth); auth = re.sub(r"\s+", " ", auth).strip(" .")[:60]
    cr = f"{auth} · {c.get('license','')}" if c else ""
    M.append({"id": mid, "t0": t0, "t1": t1, "tag": tag, "cap": cap, "sub": sub, "cr": cr, **{k2: v for k2, v in o.items() if k2 not in ("pick", "file")}})
LOCK = float(os.environ.get("LOCK", 0)); LF = os.environ.get("LOCKFILE")
if LOCK and LF:  # keep beats before LOCK exactly as already rendered; only add new ones after it
    old = json.loads(open(LF).read().split("=", 1)[1].rstrip().rstrip(";"))
    M = [m for m in old if m["t0"] < LOCK] + [m for m in M if m["t0"] >= LOCK]
    used = {m["id"]: used.get(m["id"], "") for m in M}
open(os.path.join(OUT, "media.js"), "w").write("window.MEDIA=" + json.dumps(M, ensure_ascii=False) + ";\n")
imgs = " ".join(f'<img id="m_{m}" class="hr" src="assets/media/{m}.jpg" alt="">' for m in used)
p = "engine/ep2/index.html"; s = open(p).read()
s = re.sub(r'\n?<!--media-->.*?<!--/media-->', "", s, flags=re.S)
s = s.replace('<div id="logo">', f'<!--media-->{imgs}<!--/media-->\n <div id="logo">', 1)
open(p, "w").write(s)
pj = os.path.join(OUT, "plan.json"); P = json.load(open(pj)); z = [t for t in P["SFX"].get("zoom", []) if t not in P.get("_mz", [])]
mz = [round(m["t0"] - 0.25, 2) for m in M]; P["SFX"]["zoom"] = sorted(z + mz); P["_mz"] = mz; json.dump(P, open(pj, "w"))
cred = sorted({f"{c['title']} — {c['author']} — {c['license']} — {c['source']}" for c in CR.values() if re.sub(r"\W+", "", os.path.splitext(c["file"])[0])[:40] in used})
open(os.path.join(E, "media-credits.txt"), "w").write("\n".join(cred) + "\n")
print(len(M), "beats,", len(used), "images; missing:", missing)
