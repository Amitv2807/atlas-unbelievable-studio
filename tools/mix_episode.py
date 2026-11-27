"""Final mix: voice + ducked music bed + timed SFX from plan.json, normalised to -14 LUFS for YouTube.
python mix_episode.py voiceover.mp3 bed.wav plan.json sfx_dir OUT.wav DURATION [BED_GAIN=0.55]
BED_GAIN scales a bed normalised to about -19 LUFS; 0.55 keeps music ~10 dB under the voice (0.22 buried it)."""
import sys, json, subprocess
vo, bed, plan, K, out, dur = sys.argv[1:7]; G = float(sys.argv[7]) if len(sys.argv) > 7 else 0.55; X = json.load(open(plan))["SFX"]; K = K.rstrip("/") + "/"
M = {"whoosh": ("whoosh-flyover.wav", 0.45), "zoom": ("whoosh-short.wav", 0.5), "tick": ("tick-counter.wav", 0.6), "title": ("title-hit.wav", 0.5), "boom": ("impact-reveal.wav", 0.7), "pop": ("pop-marker.wav", 0.8)}
ins = ["-i", vo, "-i", bed]
f = ["[0:a]aresample=48000,aformat=channel_layouts=stereo,apad,asplit=2[v][vsc]", f"[1:a]aresample=48000,volume={G},apad[bed]", f"[bed][vsc]sidechaincompress=threshold=0.05:ratio=3:attack=30:release=600,atrim=0:{dur}[m]"]
lab = []; k = 2
for name, times in X.items():
    src, vol = M[name]
    for t in times:
        ins += ["-i", K + src]; ms = int(t * 1000); f.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[s{k}]"); lab.append(f"[s{k}]"); k += 1
f.append("[v][m]" + "".join(lab) + f"amix=inputs={2+len(lab)}:normalize=0:duration=first,atrim=0:{dur}[mix]")
f.append("[mix]loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.6:level=false:attack=1:release=50,volume=0.3dB[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(f), "-map", "[out]", "-t", dur, "-ar", "48000", "-c:a", "pcm_s16le", out], check=True)
print("mix:", out, "with", k - 2, "sfx")
