#!/bin/bash
# Render an Atlas canvas episode (or Short) straight to the YouTube upload file at 1440p / 24 Mbps.
# Works in chunks (capture -> encode -> delete frames) so raw 1440p frames (~1.1 MB each) never fill the disk.
#   render_upload.sh T0 T1 MIX.wav OUT.mp4 [CHUNK_SECONDS=120]
# Run it with the episode folder served on 127.0.0.1:8765 (python3 -m http.server 8765 inside engine/epN).
# Env: SIZE=1920x1080 (Shorts: 1080x1920)  SCALE=4/3 (-> 2560x1440)  WORKERS=4  BITRATE_K=24000  FPS=30
# Re-running the same command resumes: finished chunks are kept until the final file is verified.
set -e
T0=$1; T1=$2; MIX=$3; OUT=$4; CH=${5:-120}
HERE=$(cd "$(dirname "$0")" && pwd); WK=${WORKERS:-4}; BR=${BITRATE_K:-24000}; FPS=${FPS:-30}
[ -n "$OUT" ] || { echo "usage: render_upload.sh T0 T1 MIX.wav OUT.mp4 [CHUNK_SECONDS]"; exit 1; }
WORK="${OUT%.mp4}.chunks"; mkdir -p "$WORK"; : > "$WORK/list.txt"
calc(){ awk "BEGIN{print $1}"; }
k=0; s=$T0; total=0
while [ "$(calc "($s < $T1) ? 1 : 0")" = 1 ]; do
  e=$(calc "($s+$CH > $T1) ? $T1 : $s+$CH"); seg=$(printf "%s/seg_%03d.mp4" "$WORK" $k)
  f0=$(calc "int($s*$FPS+0.5)"); f1=$(calc "int($e*$FPS+0.5)"); n=$((f1-f0)); total=$((total+n))
  have=0; [ -f "$seg" ] && have=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 "$seg")
  if [ "$have" != "$n" ]; then
    node "$HERE/capture.js" "$s" "$e" "$WORK/frames" "$WK" "$FPS" | tail -1
    ffmpeg -v error -y -start_number "$f0" -framerate "$FPS" -i "$WORK/frames/frame_%06d.jpg" -frames:v "$n" -c:v libx264 -preset medium \
      -b:v ${BR}k -maxrate $((BR*9/8))k -bufsize $((BR*2))k -pix_fmt yuv420p -an "$seg"
    rm -rf "$WORK/frames"
  fi
  echo "file '$(basename "$seg")'" >> "$WORK/list.txt"; echo "[render] chunk $k  ${s}-${e} s  ok  $(date +%T)"; k=$((k+1)); s=$e
done
ffmpeg -v error -y -f concat -safe 0 -i "$WORK/list.txt" -ss "$T0" -t "$(calc "$T1-$T0")" -i "$MIX" -map 0:v -map 1:a -c:v copy \
  -c:a aac -b:a 320k -shortest -movflags +faststart "$OUT"
got=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 "$OUT")
[ "$got" = "$total" ] || { echo "[render] frame count $got != $total, chunks kept in $WORK"; exit 1; }
rm -rf "$WORK"; ls -la "$OUT"; ffprobe -v error -show_entries stream=width,height:format=duration,bit_rate -of default=nw=1 "$OUT"
echo "[render] DONE $(date +%T)"
