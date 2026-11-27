#!/bin/bash
# One-time setup for a fresh session. Run from the repo root:  bash setup/setup.sh
set -e
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null || { echo "ffmpeg missing (apt-get install -y ffmpeg)"; exit 1; }
# 1) HyperFrames renderer (pinned) + Playwright helpers
[ -f package.json ] || echo '{"name":"atlas-unbelievable-studio","private":true}' > package.json
npm i -D hyperframes@0.7.109 gsap@3.14.2 --onnxruntime-node-install-cuda=skip --no-audit --no-fund
# 2) Python tools: yt-dlp, Earshot (sound effects), Whisper (transcripts), imaging
command -v uv >/dev/null || pip install -q uv
uv venv -q -p 3.11 .venv
VIRTUAL_ENV=.venv uv pip install -q "yt-dlp[default]" numpy pillow faster-whisper "earshot @ git+https://github.com/Leonxlnx/earshot" librosa
# Earshot listening model (music mood): CPU PyTorch + transformers (needs download.pytorch.org)
VIRTUAL_ENV=.venv uv pip install -q torch --index-url https://download.pytorch.org/whl/cpu && VIRTUAL_ENV=.venv uv pip install -q "transformers>=4.40" || echo "listening model skipped (PyTorch host blocked?)"
# 3) Quality checker (motionmaxxing look.py) and optional skills
mkdir -p ext && cd ext
[ -d motionmaxxing ] || git clone -q --depth 1 https://github.com/Tejashmakwana/motionmaxxing.git
cd ..
echo "Setup done. Python: .venv/bin/python   Earshot: .venv/bin/earshot   Render: npx hyperframes render"
