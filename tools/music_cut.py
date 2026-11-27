"""Build a music bed from library tracks, one track per section, with crossfades and per-track loudness matching.
python music_cut.py SPEC.json OUT.wav DURATION
SPEC.json: [{"file": "music/Track.mp3", "start": 0, "end": 187.0, "offset": 0}, ...]  (times in the episode, offset into the track)
Tracks shorter than their section loop; every section fades in/out over XF seconds so sections crossfade."""
import sys, json, subprocess
spec, out, dur = json.load(open(sys.argv[1])), sys.argv[2], float(sys.argv[3]); XF = 2.5
ins, f, lab = [], [], []
for k, s in enumerate(spec):
    a = max(0.0, s["start"] - XF / 2); b = min(dur, s["end"] + XF / 2); L = b - a
    ins += ["-stream_loop", "-1", "-ss", str(s.get("offset", 0)), "-i", s["file"]]
    fo = 4.0 if s["end"] >= dur - 0.01 else XF
    f.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{L:.3f},asetpts=PTS-STARTPTS,loudnorm=I=-20:TP=-3:LRA=11,aresample=48000,"
             f"afade=t=in:st=0:d={XF if a > 0 else 0.5},afade=t=out:st={L - fo:.3f}:d={fo},adelay={int(a * 1000)}|{int(a * 1000)}[m{k}]")
    lab.append(f"[m{k}]")
f.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=longest,atrim=0:{dur}[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(f), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le", out], check=True)
print("bed:", out, len(spec), "sections")
