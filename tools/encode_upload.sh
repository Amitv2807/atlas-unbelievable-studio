#!/bin/bash
# Final YouTube encode at ~9 Mbps H.264. Owner rule (Nov 2026): always 8-10 Mbps; 2 Mbps blurred the maps and small text.
# encode_upload.sh RENDER.mp4|FRAMES_DIR MIX.wav OUT.mp4 [FPS=30]
# A frames directory holds frame_%06d.jpg (tools/capture.js output).
# Output is ~70 MB per minute, too big to send in chat (~400 MB limit): deliver it through Google Drive.
if [ -d "$1" ]; then IN=(-framerate "${4:-30}" -i "$1/frame_%06d.jpg"); else IN=(-i "$1"); fi
ffmpeg -v error -y "${IN[@]}" -i "$2" -map 0:v -map 1:a -c:v libx264 -preset slow -b:v 9000k -maxrate 12000k -bufsize 18000k \
  -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$3" && ls -la "$3"
