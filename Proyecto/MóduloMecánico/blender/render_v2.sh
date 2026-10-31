#!/bin/bash
# render_v2.sh: render animacion_v2.py to a PNG sequence with a stall watchdog, then build MP4 + GIF.
# Run on the Mac inside tmux:  tmux new -d -s pi-video "bash ~/PI_CAD/sin_push/blender/render_v2.sh"
# Log: render_v2.log; the last line is RENDER_V2_OK or RENDER_V2_ERROR: <why>.
set -u
cd "$HOME/PI_CAD/sin_push" || exit 1
exec >> render_v2.log 2>&1

BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
FFMPEG=/opt/homebrew/bin/ffmpeg
FRAMES="$HOME/PI_CAD/sin_push/frames_v2"
OUT="$HOME/PI_CAD/sin_push/out"
TOTAL=600
STALL_S=120        # no new frame for 2 min -> stop that Blender (by its PID) and relaunch
MAX_RELAUNCH=3     # a relaunch resumes after the last finished frame

ts() { date "+%Y-%m-%d %H:%M:%S"; }
fail() { echo "$(ts) RENDER_V2_ERROR: $*"; exit 1; }
count() { find "$FRAMES" -name "f_*.png" -size +0 2>/dev/null | wc -l | tr -d " "; }
mkdir -p "$FRAMES" "$OUT"
echo "$(ts) start; frames already rendered: $(count)/$TOTAL"

attempt=0
while [ "$(count)" -lt "$TOTAL" ]; do
  [ "$attempt" -gt "$MAX_RELAUNCH" ] && break
  # drop empty / truncated frames (no IEND chunk) so Blender re-renders exactly those
  for f in "$FRAMES"/f_*.png; do
    [ -e "$f" ] || continue
    if [ ! -s "$f" ] || [ "$(tail -c 8 "$f" | xxd -p)" != "49454e44ae426082" ]; then
      echo "$(ts) removing broken frame $f"; rm -f "$f"
    fi
  done
  echo "$(ts) blender attempt $attempt (restarts used: $attempt/$MAX_RELAUNCH), at $(count)/$TOTAL"
  "$BLENDER" -b -P blender/animacion_v2.py -- --in stl/ensamble_piezas --png "$FRAMES" > "blender_v2_$attempt.log" 2>&1 &
  bpid=$!
  last=$(count); t_last=$(date +%s)
  while kill -0 "$bpid" 2>/dev/null; do
    sleep 15
    n=$(count)
    if [ "$n" != "$last" ]; then last=$n; t_last=$(date +%s); fi
    if [ $(( $(date +%s) - t_last )) -gt "$STALL_S" ]; then
      echo "$(ts) stalled at $n/$TOTAL for >${STALL_S}s: kill $bpid"
      kill "$bpid"; sleep 5; kill -9 "$bpid" 2>/dev/null
      break
    fi
  done
  wait "$bpid" 2>/dev/null
  echo "$(ts) blender attempt $attempt ended; frames $(count)/$TOTAL"
  grep -E "Traceback|Error:" "blender_v2_$attempt.log" | head -5
  attempt=$((attempt + 1))
done

n=$(count)
[ "$n" -eq "$TOTAL" ] || fail "only $n/$TOTAL frames after $attempt attempts (see blender_v2_*.log)"
"$FFMPEG" -y -hide_banner -loglevel error -framerate 30 -i "$FRAMES/f_%04d.png" \
  -c:v libx264 -pix_fmt yuv420p -crf 17 -preset slow -profile:v high -movflags +faststart \
  "$OUT/LG_mec_animacion_v2.mp4" || fail "ffmpeg mp4"
# GIF: the whole 20 s at 2.5x = 8 s, 15 fps, 720 px wide, own palette
"$FFMPEG" -y -hide_banner -loglevel error -i "$OUT/LG_mec_animacion_v2.mp4" \
  -vf "setpts=PTS/2.5,fps=15,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" \
  -loop 0 "$OUT/LG_mec_animacion_v2.gif" || fail "ffmpeg gif"
echo "$(ts) mp4 $(stat -f %z "$OUT/LG_mec_animacion_v2.mp4") bytes, gif $(stat -f %z "$OUT/LG_mec_animacion_v2.gif") bytes"
echo "$(ts) RENDER_V2_OK"
