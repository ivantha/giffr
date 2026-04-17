#!/usr/bin/env python3
"""Alfred script filter: query Tenor v2 and emit results as JSON."""
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

TENOR_SEARCH = "https://tenor.googleapis.com/v2/search"
CACHE_DIR = Path.home() / "Library" / "Caches" / "com.ivantha.giffr"


def emit(items):
    print(json.dumps({"items": items}))


def error_item(title, subtitle):
    emit([{"title": title, "subtitle": subtitle, "valid": False, "icon": {"path": "icon.png"}}])


def cache_thumbnail(url):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    name = hashlib.sha1(url.encode()).hexdigest() + ".gif"
    path = CACHE_DIR / name
    if not path.exists():
        try:
            urllib.request.urlretrieve(url, path)
        except Exception:
            return None
    return str(path)


def main():
    api_key = os.environ.get("TENOR_API_KEY", "").strip()
    if not api_key:
        error_item(
            "Set your Tenor API key",
            "Open the workflow's Configure UI and paste a key into TENOR_API_KEY.",
        )
        return

    query = " ".join(sys.argv[1:]).strip()
    if os.environ.get("GIFFR_MODE") == "meme" and query:
        query = f"{query} meme"
    if not query:
        error_item("Type a search term", "e.g. 'gif cat', 'meme monday'")
        return

    params = {
        "q": query,
        "key": api_key,
        "client_key": "giffr",
        "limit": "20",
        "media_filter": "gif,tinygif",
        "contentfilter": "medium",
    }
    url = f"{TENOR_SEARCH}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=6) as resp:
            data = json.load(resp)
    except Exception as e:
        error_item("Tenor request failed", str(e))
        return

    items = []
    for result in data.get("results", []):
        media = result.get("media_formats", {})
        gif_url = media.get("gif", {}).get("url")
        if not gif_url:
            continue
        preview_url = media.get("tinygif", {}).get("url") or gif_url
        title = result.get("content_description") or result.get("title") or "GIF"
        markdown = f"![]({gif_url})"

        items.append({
            "uid": result.get("id", gif_url),
            "title": title,
            "subtitle": "Enter: copy URL   ⌘: copy image   ⌥: copy Markdown",
            "arg": gif_url,
            "icon": {"path": cache_thumbnail(preview_url) or "icon.png"},
            "mods": {
                "cmd": {"arg": gif_url, "subtitle": "Copy image bytes to clipboard"},
                "alt": {"arg": markdown, "subtitle": f"Copy Markdown: {markdown}"},
            },
        })

    if not items:
        error_item(f"No results for \"{query}\"", "Try a different query.")
        return

    emit(items)


if __name__ == "__main__":
    main()
