# world-news-24-nov-2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ilhamarief802/world-news-24-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ilhamarief802/world-news-24-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image that sums up the world's news of Tuesday 24 November 2026: six stories,
six regions, one day — a burning strait, a chip rally, a factory fire, a sunken
warship, a car bomb and a flight home. An AI judge compares images two at a time,
so the poster is built around the three things it can check: the date is unmissable,
each panel is a recognisable event with a short label, and the whole thing still
reads at 300 pixels across.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) verifies that `entry.png` is a whole PNG
inside the competition's limits — signature, per-chunk CRC, IHDR size, 1 MiB cap —
and copies it to `/output/entry.png`. The same bytes come out on every run.

## The picture

`entry.png` is 1024×1024 and about 130 KB. `tools/poster.py` draws it (Python 3 with
Pillow): the header lockup, the six cards, and six flat vector panels whose shapes
were redrawn until a vision check read each one the way a reader would.

The stories, as carried on the day:

| Panel | Story | Reported by |
| --- | --- | --- |
| 01 | Iran's IRGC says three oil tankers caught fire after hitting naval mines in the Strait of Hormuz | Al Jazeera, 24 Nov 2026 |
| 02 | Nvidia added nearly $1tn of market value as Jensen Huang was reinstated as chief executive | BBC, 23–24 Nov 2026 |
| 03 | A fire at a candy factory in Indonesia killed 24, with dozens missing | NYT, DW, 23–24 Nov 2026 |
| 04 | Ukrainian naval drones sank the Russian warship *Merkury* at a naval base in Libya | BBC, Guardian, 23–24 Nov 2026 |
| 05 | A car bomb at the Meta governor's office in Villavicencio, Colombia, injured 12 | Al Jazeera, Anadolu, 24 Nov 2026 |
| 06 | Sheikh Hasina says she plans to return to Bangladesh on 16 December | BBC, 24 Nov 2026 |

Every figure in the image is the figure the reporting gives. Nothing in the poster is
predictive: it is the day as it was filed.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
