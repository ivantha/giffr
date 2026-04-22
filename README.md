# giffr

Alfred workflow to search and copy GIFs & memes from the macOS launcher, powered by [Giphy](https://developers.giphy.com/).

- Copy URL, raw image bytes, or a Markdown embed — pick with a modifier key.
- Zero Python dependencies (uses only the macOS-bundled Python 3 standard library).

## Install

1. Download the latest `giffr.alfredworkflow` from the [Releases page](https://github.com/ivantha/giffr/releases).
2. Double-click the file — Alfred will import it.

## Setup

You need a free Giphy API key:

1. Create an app at the [Giphy developer dashboard](https://developers.giphy.com/dashboard).
2. Copy the generated **API Key**.
3. In Alfred, open **Workflows → giffr → Configure Workflow** (the `[x]` icon at the top right) and paste the key into the `GIPHY_API_KEY` field.

The default beta key is rate-limited to 42 requests/hour; request production access (also free) from the Giphy dashboard when you hit the limit.

Your key is stored locally in Alfred's workflow configuration and is marked `don't export`, so it's never committed to this repo or leaked if you share the workflow.

## Usage

| Keyword        | What it does                                              |
|----------------|-----------------------------------------------------------|
| `gif <query>`  | Search Giphy for GIFs matching the query.                 |
| `meme <query>` | Same search, with "meme" appended to bias toward memes.   |

On any result:

| Key          | Action                                                             |
|--------------|--------------------------------------------------------------------|
| `Enter`      | Copy raw GIF bytes (paste into Messages, Notes, etc.).             |
| `⌘ Enter`    | Copy the URL (auto-embeds in Slack, Discord).                      |
| `⌥ Enter`    | Copy as Markdown: `![](url)`.                                      |
| `Shift`      | Quick Look — large animated preview next to the results.           |

For the Quick Look panel to pop up automatically as you arrow through results (instead of only when you press Shift), turn on Alfred → Preferences → Features → Default Results → **"Show Quick Look previews automatically"**.

`Enter` detects GIF / PNG / JPEG via magic bytes; unknown formats are transparently converted to PNG via the built-in `sips` tool before copying.

## Development

Source lives in `src/`. Scripts are plain Python 3 and use only the standard library.

```
src/
├── search.py         # Giphy search → Alfred script filter JSON
├── copy_url.py       # copy URL action
├── copy_image.py     # download + copy image bytes (format-aware)
└── copy_markdown.py  # copy Markdown embed action
```

Alfred's workflow definition lives in `info.plist`. To build a shippable `.alfredworkflow`:

```sh
zip -r giffr.alfredworkflow info.plist icon.png src/ LICENSE README.md
```

Attach the resulting file to a GitHub Release.

## Roadmap

- Favorites / recent history.
- Sticker support (Giphy sticker endpoint).
- Reddit meme search as a dedicated `meme` backend.
- Raycast port.

## Attribution

Giphy requires a visible "Powered by GIPHY" attribution; it's included in every result's subtitle.

## License

MIT — see [LICENSE](LICENSE).
