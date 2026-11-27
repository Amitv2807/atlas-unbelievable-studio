"""Original, licence-free ambient music bed from Earshot synth pads (A-F-C-G), seamlessly looped.
python music_bed.py OUT.wav SECONDS"""
import sys, os, subprocess, tempfile
out, secs = sys.argv[1], float(sys.argv[2]); E = os.environ.get("EARSHOT", "earshot"); d = tempfile.mkdtemp()
def run(*a): subprocess.run(a, check=True, capture_output=True)
for n in ["A3", "F3", "C4", "G3"]:
    run(E, "make", "--sound", "pad/warm", "--pitch", n, "--dur", "10", "-o", f"{d}/w{n}.wav"); run(E, "make", "--sound", "pad/air", "--pitch", n, "--dur", "10", "-o", f"{d}/a{n}.wav")
    run("ffmpeg", "-v", "error", "-y", "-i", f"{d}/w{n}.wav", "-i", f"{d}/a{n}.wav", "-filter_complex",
        "[0]aresample=48000,aformat=channel_layouts=stereo[a];[1]aresample=48000,aformat=channel_layouts=stereo,volume=0.6[b];[a][b]amix=inputs=2:normalize=0,atrim=0:11.5,afade=t=in:d=1.5,afade=t=out:st=8.5:d=3", f"{d}/c{n}.wav")
run("ffmpeg", "-v", "error", "-y", *sum([["-i", f"{d}/c{n}.wav"] for n in ["A3", "F3", "C4", "G3"]], []), "-filter_complex",
    "[0][1]acrossfade=d=3:c1=tri:c2=tri[x];[x][2]acrossfade=d=3:c1=tri:c2=tri[y];[y][3]acrossfade=d=3:c1=tri:c2=tri", f"{d}/cycle.wav")
n = int(secs // 33) + 2; ins = sum([["-i", f"{d}/cycle.wav"] for _ in range(n)], []); f = []; prev = "[0]"
for i in range(1, n): f.append(f"{prev}[{i}]acrossfade=d=4:c1=qsin:c2=qsin" + (f"[x{i}]" if i < n - 1 else "")); prev = f"[x{i}]"
run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(f), "-ar", "48000", f"{d}/long.wav")
run("ffmpeg", "-v", "error", "-y", "-i", f"{d}/long.wav", "-af", f"lowpass=f=5000,atrim=0:{secs},afade=t=in:d=3,afade=t=out:st={secs-6}:d=6", "-ar", "48000", out)
print("bed:", out)
