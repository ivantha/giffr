#!/usr/bin/env python3
"""Download an image at argv[1] and copy it to the macOS clipboard in two
representations at once: `public.file-url` (so Snapchat / Discord / Slack
treat it like a dragged file and preserve animation) and raw image bytes
under the matching UTI (so Messages / Notes / Mail paste it inline).

Format is detected from magic bytes. Unknown formats fall through the
built-in `sips` tool and are copied as PNG.
"""
import hashlib
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

FORMATS = [
    (b"GIF87a", "com.compuserve.gif"),
    (b"GIF89a", "com.compuserve.gif"),
    (b"\x89PNG\r\n\x1a\n", "public.png"),
    (b"\xff\xd8\xff", "public.jpeg"),
]

# JXA script: writes one NSPasteboardItem carrying two UTIs —
# public.file-url and the image-bytes UTI — so each paste target
# picks whichever flavor it knows how to read.
JXA = r"""
function run(argv) {
    ObjC.import('AppKit');
    const [path, uti] = argv;
    const pb = $.NSPasteboard.generalPasteboard;
    pb.clearContents;
    const item = $.NSPasteboardItem.alloc.init;
    const fileURL = $.NSURL.fileURLWithPath(path);
    item.setStringForType(fileURL.absoluteString.js, 'public.file-url');
    const data = $.NSData.dataWithContentsOfFile(path);
    item.setDataForType(data, uti);
    // $([item]) forces a JS array -> NSArray; a bare [item] bridges to NSDictionary and throws.
    pb.writeObjects($([item]));
}
"""


def detect_uti(path):
    with open(path, "rb") as f:
        head = f.read(8)
    for sig, uti in FORMATS:
        if head.startswith(sig):
            return uti
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

    uti = detect_uti(path)
    if uti is None:
        png_path = path.with_suffix(".png")
        subprocess.run(
            ["sips", "-s", "format", "png", str(path), "--out", str(png_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        path = png_path
        uti = "public.png"

    subprocess.run(
        ["osascript", "-l", "JavaScript", "-e", JXA, str(path), uti],
        check=True,
    )
    print(url)


if __name__ == "__main__":
    main()
