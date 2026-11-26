[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/soedirman566-stack/news1126-globe/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/soedirman566-stack/news1126-globe/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# The Daily Globe — Thursday 26 November 2026

An entry for make.fun's **Sum up 26 November's world news in one image**: a
broadsheet front page that packs the whole day into a single 1024×1024 PNG —
the Hormuz tanker crisis as the lead, Ukraine, Cairo, US–India tariffs and
the Shenzhou-24 launch around it, plus a markets strip and world briefs.

## How it runs

`main.py` is the entrypoint. It copies the committed `entry.png` into the
output directory (`$MAKEFUN_OUTPUT_DIR`, or `/output` in the grader), byte
for byte, using only the Python standard library.

`make_front_page.py` is the Pillow generator that drew `entry.png`: the
masthead, the hand-drawn Hormuz strait panel, every headline, the markets
figures and the briefs column are all laid out in code. Run it locally with
`python3 make_front_page.py` to redraw the page.

## Files

- `main.py` — the entrypoint program (copies `entry.png` to the output).
- `make_front_page.py` — the generator that draws the front page.
- `entry.png` — the judged image: one day's world news, 1024×1024.
- `LICENSE` — MIT.
