#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Pixel-art pipeline:
#   1. rsvg-convert renders the SVG at the logical pixel grid (PIXEL_SIZE).
#      Combined with shape-rendering="crispEdges" in the SVG, this yields
#      one solid color per cell, no anti-aliasing.
#   2. magick upscales to TARGET with nearest-neighbor (-filter point),
#      preserving the chunky cell edges instead of smoothing them.
PIXEL_SIZE=32
TARGET=1024

tmp=$(mktemp -t giffr_icon_XXXXXX).png
trap 'rm -f "$tmp"' EXIT

rsvg-convert -w "$PIXEL_SIZE" -h "$PIXEL_SIZE" icon.svg -o "$tmp"
magick "$tmp" -filter point -resize "${TARGET}x${TARGET}" ../icon.png

for size in 512 256 128 64 32; do
  magick "$tmp" -filter point -resize "${size}x${size}" "preview_${size}.png"
done

echo "Wrote ../icon.png (${TARGET}px, pixel-art from ${PIXEL_SIZE}x${PIXEL_SIZE}) + preview_{512,256,128,64,32}.png"
