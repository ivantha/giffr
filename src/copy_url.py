#!/usr/bin/env python3
"""Copy the given URL (argv[1]) to the macOS clipboard via pbcopy."""
import subprocess
import sys


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    subprocess.run(["pbcopy"], input=text.encode(), check=True)
    print(text)


if __name__ == "__main__":
    main()
