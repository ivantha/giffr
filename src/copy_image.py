#!/usr/bin/env python3
"""Download the GIF at argv[1] and copy its raw bytes to the macOS clipboard as a GIF.

Uses `osascript` with the `«class GIFf»` clipboard type so apps like Messages and
Notes receive the image rather than a plain URL.
"""
import hashlib
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    if not url:
        sys.stderr.write("no url given\n")
        sys.exit(1)

    name = hashlib.sha1(url.encode()).hexdigest() + ".gif"
    path = Path(tempfile.gettempdir()) / f"giffr-{name}"
    if not path.exists():
        urllib.request.urlretrieve(url, path)

    script = (
        f'set the clipboard to (read (POSIX file "{path}") as «class GIFf»)'
    )
    subprocess.run(["osascript", "-e", script], check=True)
    print(url)


if __name__ == "__main__":
    main()
