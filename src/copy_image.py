#!/usr/bin/env python3
"""Download an image at argv[1] and copy its raw bytes to the macOS clipboard.

Detects GIF / PNG / JPEG via magic bytes and uses the matching `«class …»`
clipboard type. Unknown formats are converted to PNG with the system `sips`
tool so pasting still works in apps that expect image bytes (Messages, Notes).
"""
import hashlib
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

FORMATS = [
    (b"GIF87a", "GIFf"),
    (b"GIF89a", "GIFf"),
    (b"\x89PNG\r\n\x1a\n", "PNGf"),
    (b"\xff\xd8\xff", "JPEG"),
]


def detect_class(path):
    with open(path, "rb") as f:
        head = f.read(8)
    for sig, klass in FORMATS:
        if head.startswith(sig):
            return klass
    return None


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    if not url:
        sys.stderr.write("no url given\n")
        sys.exit(1)

    name = hashlib.sha1(url.encode()).hexdigest()
    path = Path(tempfile.gettempdir()) / f"giffr-{name}"
    if not path.exists():
        urllib.request.urlretrieve(url, path)

    klass = detect_class(path)
    if klass is None:
        png_path = path.with_suffix(".png")
        subprocess.run(
            ["sips", "-s", "format", "png", str(path), "--out", str(png_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        path = png_path
        klass = "PNGf"

    script = f'set the clipboard to (read (POSIX file "{path}") as «class {klass}»)'
    subprocess.run(["osascript", "-e", script], check=True)
    print(url)


if __name__ == "__main__":
    main()
