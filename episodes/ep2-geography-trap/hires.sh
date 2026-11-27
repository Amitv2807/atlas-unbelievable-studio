#!/bin/bash
# Sharp NASA GIBS textures for the zoomed scenes of Episode 2 (bbox much larger than each camera view).
# Usage: bash episodes/ep2-geography-trap/hires.sh   (writes engine/ep2/assets/hires/*.jpg + .json)
cd "$(dirname "$0")/../.." || exit 1
O=engine/ep2/assets/hires; mkdir -p $O
m(){ n=$1; shift; [ -f $O/$n.json ] || .venv/bin/python -I tools/gibs_mosaic.py "$@" $O/$n.jpg --max-width 4096 2>&1 | tail -1; }
L(){ # pick levels so the texture is ~4096 px wide: level = ceil(log2(4096*0.5625/span))
python3 -c "import math,sys;s=float(sys.argv[1]);l=max(1,math.ceil(math.log2(2304/s)));print(min(l,7),min(l,11))" $1; }
reg(){ n=$1; x0=$2; y0=$3; x1=$4; y1=$5; read a b < <(L $(python3 -c "print($x1-($x0))")); m $n $x0 $y0 $x1 $y1 --level $a --relief-level $b & }
reg europe   -12 36 72 72
reg tibet     62 14 112 46
reg china     70 15 140 55
reg seasia    88 -12 125 22
reg sgstrait 102.6 0.4 105.2 2.4
reg chain    110 5 150 45
reg pakistan  50 15 90 45
reg straits   20 30 40 46
reg redsea    30 8 52 32
reg gibraltar -12 32 2 40
reg vlad     122 34 148 52
reg bering  -180 55 -150 72
reg arcticno  -40 55 60 82
wait; ls -la $O
