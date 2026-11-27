"""Word-level transcript of a voiceover (local Whisper, free). Needs huggingface.co reachable on first run.
python transcribe.py voiceover.mp3 words.json [--model small.en]"""
import sys, json, argparse
from faster_whisper import WhisperModel
ap = argparse.ArgumentParser(); ap.add_argument("audio"); ap.add_argument("out"); ap.add_argument("--model", default="small.en"); a = ap.parse_args()
m = WhisperModel(a.model, device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(a.audio, word_timestamps=True, beam_size=1)
w = [[x.word.strip(), round(x.start, 2), round(x.end, 2)] for s in segs for x in s.words]
json.dump(w, open(a.out, "w")); print(len(w), "words; ends at", w[-1][2])
