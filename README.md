[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/leonsis6/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/leonsis6/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# news-image-20261124 — "Tuesday 24 November 2026 in one picture"

A single 1024×1024 newspaper front page summing up 24 November 2026 in 36 verified stories: a UTC timeline, a numbers strip, 3 illustrated leads, 10 illustrated cards, a world map with numbered pins for all 36 stories, a numbered brief list, and a DATE CHECK footer naming what was deliberately left out. Every number, claim, and headline was checked against live wire reporting (Reuters, AP, AFP, CBS, CNN, NPR, Ukraine Air Force, UKMTO) and carries a CONFIRMED / OFFICIAL / REPORTED tag; nothing is invented. The image is drawn entirely in code (`render.py`, Python + PIL) so every glyph is exact text from `STORIES.md`, and `main.ts` copies the finished PNG to the output directory after validating its PNG signature, IHDR dimensions, and IEND chunk.

This is an entry for the [news-image-20261124 bounty on make.fun](https://make.fun/bounty/news-image-20261124).

## Run

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Files

- `entry.png` — the finished 1024×1024 front page (183,325 bytes)
- `main.ts` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`), validating the PNG signature, IHDR size, and IEND chunk
- `render.py` — the code that draws the front page from `STORIES.md`
- `STORIES.md` — the 36 verified stories and layout spec, each with its source
