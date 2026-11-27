#!/bin/bash
# Re-encode a rendered video with the final mix, under ~400 MB for 10 min, YouTube-friendly.
# encode_upload.sh RENDER.mp4 MIX.wav OUT.mp4
ffmpeg -v error -y -i "$1" -i "$2" -map 0:v -map 1:a -c:v libx264 -preset medium -b:v 4800k -maxrate 7000k -bufsize 14000k -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart "$3" && ls -la "$3"
