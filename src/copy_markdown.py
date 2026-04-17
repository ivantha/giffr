#!/usr/bin/env python3
"""Copy a Markdown image embed (argv[1] is already the Markdown string) to the clipboard."""
import subprocess
import sys


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    subprocess.run(["pbcopy"], input=text.encode(), check=True)
    print(text)


if __name__ == "__main__":
    main()
