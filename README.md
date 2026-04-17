# giffr

Alfred workflow to search and copy GIFs & memes from the macOS launcher.

- **GIFs** come from [Giphy](https://developers.giphy.com/).
- **Memes** come from [Imgur](https://apidocs.imgur.com/).
- Copy URL, raw image bytes, or a Markdown embed — pick with a modifier key.
- Zero Python dependencies (uses only the macOS-bundled Python 3 standard library).

## Install

1. Download the latest `giffr.alfredworkflow` from the [Releases page](https://github.com/ivantha/giffr/releases).
2. Double-click the file — Alfred will import it.

## Setup

You need two free credentials, one per provider:

### Giphy API key

1. Create an app at the [Giphy developer dashboard](https://developers.giphy.com/dashboard) (free, instant).
2. Copy the generated **API Key**.

The default beta key is rate-limited to 42 requests/hour; request production access (also free) when you hit the limit.

### Imgur Client ID

1. Register an app at [api.imgur.com/oauth2/addclient](https://api.imgur.com/oauth2/addclient) — pick **OAuth 2 authorization without a callback URL**.
2. Copy the generated **Client ID** (not the secret — giffr doesn't need it).

### Paste into Alfred

In Alfred, open **Workflows → giffr → Configure Workflow** (the `[x]` icon at the top right) and paste both values into the `GIPHY_API_KEY` and `IMGUR_CLIENT_ID` fields.

Both keys are stored locally in Alfred's workflow configuration and are marked `don't export`, so they're never committed to this repo or leaked if you share the workflow.

## Usage

| Keyword        | Backend | What it does                       |
|----------------|---------|------------------------------------|
| `gif <query>`  | Giphy   | Search for GIFs.                   |
| `meme <query>` | Imgur   | Search Imgur gallery for `<query> meme`. |

On any result:

| Key          | Action                                               |
|--------------|------------------------------------------------------|
| `Enter`      | Copy the URL (auto-embeds in Slack, Discord).        |
| `⌘ Enter`    | Copy raw image bytes (paste into Messages, Notes).   |
| `⌥ Enter`    | Copy as Markdown: `![](url)`.                        |

`⌘ Enter` handles GIF, PNG, and JPEG natively; anything else is transparently converted to PNG via the built-in `sips` tool before copying.

## Development

Source lives in `src/`. Scripts are plain Python 3 and use only the standard library.

```
src/
├── search.py         # Provider dispatch (Giphy/Imgur) → Alfred script filter JSON
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
- Tenor fallback provider.
- Raycast port.

## Attribution

Giphy requires a visible "Powered by GIPHY" attribution on results; it's included in every GIF result's subtitle. Imgur asks for a link back in published material.

## License

MIT — see [LICENSE](LICENSE).
