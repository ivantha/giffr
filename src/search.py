#!/usr/bin/env python3
"""Alfred script filter: search Giphy (for `gif`) or Imgur (for `meme`)."""
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

GIPHY_SEARCH = "https://api.giphy.com/v1/gifs/search"
IMGUR_SEARCH = "https://api.imgur.com/3/gallery/search/viral/all/0"
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
    # Preserve extension so Alfred renders the right thing.
    ext = Path(urllib.parse.urlparse(url).path).suffix or ".img"
    path = CACHE_DIR / f"{name}{ext}"
    if not path.exists():
        try:
            urllib.request.urlretrieve(url, path)
        except Exception:
            return None
    return str(path)


def fetch_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=6) as resp:
        return json.load(resp)


def search_giphy(query, api_key):
    params = {
        "api_key": api_key,
        "q": query,
        "limit": "20",
        "rating": "pg-13",
        "bundle": "messaging_non_clips",
    }
    data = fetch_json(f"{GIPHY_SEARCH}?{urllib.parse.urlencode(params)}")
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


def _imgur_thumb(link):
    """Insert Imgur's 'm' (medium 320×320) size suffix before the extension."""
    if not link:
        return None
    head, dot, tail = link.rpartition(".")
    if not dot or "/" in tail:
        return link
    return f"{head}m.{tail}"


def search_imgur(query, client_id):
    url = f"{IMGUR_SEARCH}?{urllib.parse.urlencode({'q': query})}"
    data = fetch_json(url, headers={"Authorization": f"Client-ID {client_id}"})
    items = []
    for result in data.get("data", []):
        if result.get("is_album"):
            cover_id = result.get("cover")
            ext = (result.get("cover_ext") or "").lstrip(".") or "jpg"
            if not cover_id:
                continue
            link = f"https://i.imgur.com/{cover_id}.{ext}"
        else:
            link = result.get("link")
            if not link:
                continue
        preview = _imgur_thumb(link)
        title = result.get("title") or "Meme"
        markdown = f"![]({link})"
        items.append({
            "uid": result.get("id", link),
            "title": title,
            "subtitle": "Enter: copy URL   ⌘: copy image   ⌥: copy Markdown   (via Imgur)",
            "arg": link,
            "icon": {"path": cache_thumbnail(preview) or "icon.png"},
            "mods": {
                "cmd": {"arg": link, "subtitle": "Copy image bytes to clipboard"},
                "alt": {"arg": markdown, "subtitle": f"Copy Markdown: {markdown}"},
            },
        })
    return items


def main():
    provider = os.environ.get("GIFFR_PROVIDER", "giphy").lower()
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        hint = "e.g. 'gif cat'" if provider == "giphy" else "e.g. 'meme monday'"
        error_item("Type a search term", hint)
        return

    try:
        if provider == "giphy":
            key = os.environ.get("GIPHY_API_KEY", "").strip()
            if not key:
                error_item(
                    "Set your Giphy API key",
                    "Open Configure Workflow and paste a key into GIPHY_API_KEY.",
                )
                return
            items = search_giphy(query, key)
        elif provider == "imgur":
            cid = os.environ.get("IMGUR_CLIENT_ID", "").strip()
            if not cid:
                error_item(
                    "Set your Imgur Client ID",
                    "Open Configure Workflow and paste it into IMGUR_CLIENT_ID.",
                )
                return
            items = search_imgur(f"{query} meme", cid)
        else:
            error_item(f"Unknown provider: {provider}", "Expected 'giphy' or 'imgur'.")
            return
    except Exception as e:
        error_item(f"{provider.title()} request failed", str(e))
        return

    if not items:
        error_item(f"No results for \"{query}\"", "Try a different query.")
        return

    emit(items)


if __name__ == "__main__":
    main()
