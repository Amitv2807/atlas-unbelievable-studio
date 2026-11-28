#!/bin/bash
# Final YouTube encode at ~24 Mbps H.264. Owner rule (Nov 2026): always 22-25 Mbps; 2 Mbps blurred the maps and small text.
# encode_upload.sh RENDER.mp4|FRAMES_DIR MIX.wav OUT.mp4 [FPS=30]
# A frames directory holds frame_%06d.jpg (tools/capture.js output).
# Output is ~180 MB per minute, too big to send in chat (~400 MB limit): deliver it through Google Drive.
if [ -d "$1" ]; then IN=(-framerate "${4:-30}" -i "$1/frame_%06d.jpg"); else IN=(-i "$1"); fi
ffmpeg -v error -y "${IN[@]}" -i "$2" -map 0:v -map 1:a -c:v libx264 -preset slow -b:v 24000k -maxrate 27000k -bufsize 48000k \
  -pix_fmt yuv420p -c:a aac -b:a 320k -movflags +faststart "$3" && ls -la "$3"
