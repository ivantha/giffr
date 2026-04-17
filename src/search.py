#!/usr/bin/env python3
"""Alfred script filter: search Giphy and emit results as JSON.

The `meme` keyword sets GIFFR_MODE=meme, which appends "meme" to the query.
"""
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

GIPHY_SEARCH = "https://api.giphy.com/v1/gifs/search"
CACHE_DIR = Path.home() / "Library" / "Caches" / "com.ivantha.giffr"


def emit(items):
    print(json.dumps({"items": items}))


def error_item(title, subtitle):
    emit([{"title": title, "subtitle": subtitle, "valid": False, "icon": {"path": "icon.png"}}])


def cache_thumbnail(url):
    if not url:
        return None
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    name = hashlib.sha1(url.encode()).hexdigest()
    ext = Path(urllib.parse.urlparse(url).path).suffix or ".img"
    path = CACHE_DIR / f"{name}{ext}"
    if not path.exists():
        try:
            urllib.request.urlretrieve(url, path)
        except Exception:
            return None
    return str(path)


def search_giphy(query, api_key):
    params = {
        "api_key": api_key,
        "q": query,
        "limit": "20",
        "rating": "pg-13",
        "bundle": "messaging_non_clips",
    }
    url = f"{GIPHY_SEARCH}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=6) as resp:
        data = json.load(resp)

    items = []
    for result in data.get("data", []):
        images = result.get("images", {})
        gif_url = images.get("original", {}).get("url")
        if not gif_url:
            continue
        preview = images.get("fixed_height_small", {}).get("url") or gif_url
        title = result.get("title") or "GIF"
        markdown = f"![]({gif_url})"
        items.append({
            "uid": result.get("id", gif_url),
            "title": title,
            "subtitle": "Enter: copy URL   ⌘: copy image   ⌥: copy Markdown   (Powered by GIPHY)",
            "arg": gif_url,
            "icon": {"path": cache_thumbnail(preview) or "icon.png"},
            "mods": {
                "cmd": {"arg": gif_url, "subtitle": "Copy image bytes to clipboard"},
                "alt": {"arg": markdown, "subtitle": f"Copy Markdown: {markdown}"},
            },
        })
    return items


def main():
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        error_item("Type a search term", "e.g. 'gif cat', 'meme monday'")
        return

    if os.environ.get("GIFFR_MODE") == "meme":
        query = f"{query} meme"

    key = os.environ.get("GIPHY_API_KEY", "").strip()
    if not key:
        error_item(
            "Set your Giphy API key",
            "Open Configure Workflow and paste a key into GIPHY_API_KEY.",
        )
        return

    try:
        items = search_giphy(query, key)
    except Exception as e:
        error_item("Giphy request failed", str(e))
        return

    if not items:
        error_item(f"No results for \"{query}\"", "Try a different query.")
        return

    emit(items)


if __name__ == "__main__":
    main()
