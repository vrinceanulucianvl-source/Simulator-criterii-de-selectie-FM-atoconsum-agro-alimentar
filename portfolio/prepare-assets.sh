#!/usr/bin/env bash
# Download the three cinematic clips and re-encode them for scroll-scrubbing.
#
# Why this is necessary: a normal MP4 stores one keyframe every one to two
# seconds and reconstructs everything between them from differences. Playing
# forward that is fine. Seeking to an arbitrary time is not — the browser must
# find the previous keyframe and decode forward to reach the frame you asked
# for. Do that on every scroll frame and the scrub stutters or appears frozen.
#
# The fix is an all-intra encode: every frame becomes a keyframe, so any frame
# can be presented immediately. Files get larger, which is why they are served
# locally rather than over the network. +faststart moves the index to the front
# so the browser can seek before the file has finished downloading.
#
# Requires ffmpeg.  Usage:  bash prepare-assets.sh
set -euo pipefail

CDN="https://d8j0ntlcm91z4.cloudfront.net/user_3IGCVkXvjejfKQewPn4ej8wH0Op"
# The hero is not a raw generation: the delivered clip carried a hard cut a
# third of the way in, so it was trimmed and re-encoded, and the result lives
# in the upload bucket instead.
UP="https://d2ol7oe51mr4n9.cloudfront.net/user_3IGCVkXvjejfKQewPn4ej8wH0Op"
mkdir -p assets

fetch_and_encode() {
  local url="$1" out="$2" intra="$3"
  echo "→ $out"
  curl -fL --retry 3 -o "assets/.raw-$out" "$url"
  if [ "$intra" = "yes" ]; then
    # every frame a keyframe: instant seeking at any scroll position
    ffmpeg -y -loglevel error -i "assets/.raw-$out" \
      -c:v libx264 -preset slow -crf 20 -g 1 -keyint_min 1 -sc_threshold 0 \
      -pix_fmt yuv420p -an -movflags +faststart "assets/$out"
  else
    # ambient loops only play forward, so a normal encode is fine
    ffmpeg -y -loglevel error -i "assets/.raw-$out" \
      -c:v libx264 -preset slow -crf 22 \
      -pix_fmt yuv420p -an -movflags +faststart "assets/$out"
  fi
  rm -f "assets/.raw-$out"
}

fetch_and_encode "$UP/17fc177f-5ddd-488b-b0ba-072eb44cad37.mp4"                      01-boardroom.mp4  yes
fetch_and_encode "$CDN/hf_20260905_101239_161b5b35-5dc4-4154-b76e-b445b079ec0e.mp4" 02-strategist.mp4 no
fetch_and_encode "$CDN/hf_20260904_191420_26cce321-dd86-4623-9a6f-cf385221504b.mp4"  03-execution.mp4  no

echo
echo "Done. Now set USE_LOCAL_ASSETS = true in index.html."
ls -lh assets/*.mp4
