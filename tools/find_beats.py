"""Find when each fact / chapter / keyword is spoken.
python find_beats.py words.json anchors.json beats.json
anchors.json: {"name": ["keyword-prefix", after_seconds, before_seconds], ...}
Also prints every "Number ..." start, which marks each fact."""
import sys, json
w = json.load(open(sys.argv[1])); A = json.load(open(sys.argv[2]))
T = [x[0].lower().strip('.,!?:;"\'') for x in w]
for i, x in enumerate(T):
    if x == "number" and i + 1 < len(T): print(f"{w[i][1]:8.2f}  number {' '.join(T[i+1:i+3])}")
def f(word, a, b=1e9):
    for i, x in enumerate(T):
        if a <= w[i][1] < b and x.startswith(word.lower()): return w[i][1]
R = {k: f(*v) for k, v in A.items()}; miss = [k for k, v in R.items() if v is None]
if miss: print("MISSING (set by hand):", miss)
json.dump(R, open(sys.argv[3], "w"), indent=0)
