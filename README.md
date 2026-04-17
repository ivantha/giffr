# giffr

Alfred workflow to search and copy GIFs & memes, powered by [Tenor](https://tenor.com/gifapi).

- Fast keyword-driven search from Alfred.
- Copy GIF URL, raw image bytes, or a Markdown embed — pick with a modifier key.
- Zero Python dependencies (uses only the macOS-bundled Python 3 standard library).

## Install

1. Download the latest `giffr.alfredworkflow` from the [Releases page](https://github.com/ivantha/giffr/releases).
2. Double-click the file — Alfred will import it.

## Setup

You need a free Tenor API key:

1. Go to [Google Cloud Console → Tenor API](https://developers.google.com/tenor/guides/quickstart) and create an API key.
2. In Alfred, open **Workflows → giffr → Configure Workflow** (the `[x]` icon at the top right).
3. Paste the key into the `TENOR_API_KEY` field and save.

Your key is stored locally in Alfred's workflow configuration and is never committed to this repo.

## Usage

| Keyword        | What it does                                |
|----------------|---------------------------------------------|
| `gif <query>`  | Search Tenor for GIFs matching the query.   |
| `meme <query>` | Same search, biased toward meme-style GIFs. |

On any result:

| Key          | Action                                               |
|--------------|------------------------------------------------------|
| `Enter`      | Copy the GIF URL (auto-embeds in Slack, Discord).    |
| `⌘ Enter`    | Copy GIF image bytes (paste into Messages, Notes).   |
| `⌥ Enter`    | Copy as Markdown: `![](url)`.                        |

## Development

Source lives in `src/`. Scripts are plain Python 3 and use only the standard library.

```
src/
├── search.py         # Tenor search → Alfred script filter JSON
├── copy_url.py       # copy URL action
├── copy_image.py     # download + copy image bytes action
└── copy_markdown.py  # copy Markdown embed action
```

Alfred's workflow definition lives in `info.plist`. To build a shippable `.alfredworkflow`:

```sh
zip -r giffr.alfredworkflow info.plist icon.png src/ LICENSE README.md
```

Attach the resulting file to a GitHub Release.

## Roadmap

- Favorites / recent history.
- Sticker support (Tenor sticker endpoint).
- Giphy fallback provider.
- Raycast port.

## License

MIT — see [LICENSE](LICENSE).
