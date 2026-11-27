"""Analyse every track in music/ and write music/library.json.
.venv/bin/python -I tools/analyze_music.py [music_dir]
Per track: duration, tempo + beat times, energy curve (1 s), brightness, major/minor, percussiveness, sections,
and a score for each mood (mysterious, epic, fun, dark). A mood prefix in the filename ("dark - …") overrides the guess."""
import sys, os, json, glob, numpy as np, librosa
D = sys.argv[1] if len(sys.argv) > 1 else "music"; LIB = os.path.join(D, "library.json")
lib = json.load(open(LIB)) if os.path.exists(LIB) else {}
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]); MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
KEYS = "C C# D D# E F F# G G# A A# B".split()
def keymode(chroma):
    c = chroma.mean(axis=1); best = (-9, "", "")
    for i in range(12):
        for prof, mode in ((MAJ, "major"), (MIN, "minor")):
            r = np.corrcoef(c, np.roll(prof, i))[0, 1]
            if r > best[0]: best = (r, KEYS[i], mode)
    return best[1], best[2], round(float(best[0]), 2)
def z(x, lo, hi): return float(np.clip((x - lo) / (hi - lo), 0, 1))
import subprocess, re, shutil
Q = {"mysterious": "mysterious curious documentary background music", "epic": "epic cinematic orchestral music with big drums",
     "fun": "happy upbeat playful fun music", "dark": "dark ominous tense suspenseful music"}
def listen_scores(path):
    """Earshot's listening model (CLAP): forced choice between the four mood descriptions. Needs earshot[listen] + torch."""
    exe = os.path.join(os.path.dirname(sys.executable), "earshot")
    if not os.path.exists(exe): return None
    r = subprocess.run([exe, "match", path, Q["mysterious"], "--alts", Q["epic"], Q["fun"], Q["dark"], "--json"], capture_output=True, text=True,
                       env={**os.environ, "HF_HUB_DISABLE_XET": "1"})
    try: summ = json.loads(r.stdout[r.stdout.find("{"):])["summary"]
    except Exception: return None
    m = re.search(r"Forced choice vs your alternatives:(.*)", summ); v = re.findall(r"(\d+)%", m.group(1) if m else "")
    return dict(zip(["mysterious", "epic", "fun", "dark"], [int(x) / 100 for x in v])) if len(v) == 4 else None
for path in sorted(glob.glob(os.path.join(D, "*.mp3")) + glob.glob(os.path.join(D, "*.wav"))):
    name = os.path.basename(path)
    if name in lib and lib[name].get("v") == 3: continue
    y, sr = librosa.load(path, sr=22050, mono=True); dur = len(y) / sr
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr); tempo = float(np.atleast_1d(tempo)[0]); bt = librosa.frames_to_time(beats, sr=sr)
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]; t = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=512)
    per_s = [float(rms[(t >= s) & (t < s + 1)].mean()) if np.any((t >= s) & (t < s + 1)) else 0.0 for s in range(int(np.ceil(dur)))]
    e = np.array(per_s); en = (e / (e.max() + 1e-9)).round(3)
    cent = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    yh, yp = librosa.effects.hpss(y); perc = float(np.sum(yp ** 2) / (np.sum(y ** 2) + 1e-9))
    key, mode, kconf = keymode(librosa.feature.chroma_cqt(y=yh, sr=sr))
    onset_rate = len(librosa.onset.onset_detect(y=y, sr=sr)) / dur
    dyn = float(np.percentile(en, 95) - np.percentile(en, 20))
    S = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13); bounds = librosa.segment.agglomerative(S, k=min(8, max(3, int(dur // 25))))
    sections = [round(float(x), 2) for x in librosa.frames_to_time(bounds, sr=sr)]
    bright = z(cent, 1200, 3200); fast = z(tempo, 70, 140); minor = 1.0 if mode == "minor" else 0.0
    sc = {"mysterious": round(0.35 * minor + 0.25 * (1 - bright) + 0.2 * (1 - z(perc, .15, .5)) + 0.2 * (1 - abs(fast - .45) * 2), 2),
          "epic": round(0.4 * z(dyn, .2, .7) + 0.25 * z(float(e.max() / (e.mean() + 1e-9)), 1.3, 3) + 0.2 * (1 - abs(fast - .5) * 2) + 0.15 * z(perc, .2, .5), 2),
          "fun": round(0.35 * (1 - minor) + 0.3 * bright + 0.2 * fast + 0.15 * z(perc, .2, .5), 2),
          "dark": round(0.4 * minor + 0.35 * (1 - bright) + 0.25 * (1 - fast), 2)}
    listen = listen_scores(path)
    if listen: sc = {k: round(0.75 * listen[k] + 0.25 * sc[k], 2) for k in sc}
    tag = name.split(" - ")[0].strip().lower().lstrip("★ ")
    mood = tag if tag in sc else max(sc, key=sc.get)
    lib[name] = {"v": 3, "file": name, "duration": round(dur, 1), "bpm": round(tempo, 1), "beats": [round(float(b), 3) for b in bt],
                 "energy": en.tolist(), "brightness_hz": round(cent), "key": f"{key} {mode}", "key_conf": kconf, "percussive": round(perc, 2),
                 "onsets_per_s": round(onset_rate, 2), "dynamics": round(dyn, 2), "sections": sections, "scores": sc, "mood": mood,
                 "mood_source": "filename" if tag in sc else ("listening+analysis" if listen else "analysis"), "listen": listen, "source": "YouTube Audio Library (owner-supplied)", "uses": []}
    print(f"{name[:40]:40s} {dur:6.1f}s {tempo:6.1f}bpm {key:>2} {mode:5s} bright {cent:5.0f}Hz perc {perc:.2f} dyn {dyn:.2f} -> {mood:10s} {sc}")
json.dump(lib, open(LIB, "w"), indent=1); print("library:", LIB, len(lib), "tracks")
