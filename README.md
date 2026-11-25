# Sum up 25 November's world news in one image

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/akitaBugBounty/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/akitaBugBounty/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

Bounty: https://make.fun/bounty/news-image-20261125

## What the image shows

The image is a newspaper front page, masthead "THE WORLD IN ONE IMAGE",
dated "WEDNESDAY 25 NOVEMBER 2026". It sums up the day's world news
story by story, so the picture alone tells the news:

- **Lead panel — Strait of Hormuz.** An oil tanker sails the strait
  between two coastlines, with spiked naval mines in the water and an
  explosion at the tanker's bow. Headline: "MINES HIT TANKERS IN
  STRAIT OF HORMUZ". Iran's Revolutionary Guard Navy said three oil
  tankers were hit by naval mines on 25 November.
- **Panel 2 — COP31 collapse.** A city skyline under a cracked globe
  and a wilting leaf. Headline: "COP31 COLLAPSES WITHOUT A DEAL".
  Oil and gas producers blocked fossil-fuel phaseout language at the
  Antalya talks on 25 November.
- **Panel 3 — Cyber breach.** A cracked shield on a dark background
  with circuit lines and binary digits. Headline: "CIA AND ODNI HIT
  BY CYBER BREACH". Unclassified systems were compromised, reported
  25 November.
- **Panel 4 — Iowa blast evacuation.** An explosion flash and smoke
  over an evacuation road with a yellow EVAC sign. Headline: "IOWA
  BLAST EVACUATION". The US Army was to detonate lead azide and
  residents were urged to evacuate, 25 November.
- **Bottom ticker.** "HUAWEI GUILTY ON 10 COUNTS" (US trade-secrets
  trial verdict, 24 November), "GIULIANI GETS MEDAL OF FREEDOM",
  "RUSSIAN MISSILES BREACH POLISH AIRSPACE", "HOUTHI DRONE HITS
  RIYADH TOWER, 11 HURT", "WHO FLEES EBOLA HOSPITAL IN CONGO",
  "THANKSGIVING RUSH", and "GAZA: POLLUTION RISK IN 99%".
- **Footer — drone at sea.** A small globe, a cargo ship, and a drone
  overhead. Headline: "UKRAINE: DRONE HITS CARGO SHIP AT SEA"
  (Gulf of Finland / off Libya).

## How it is built

`draw_image.py` draws the whole 1024x1024 picture with Python's
standard library only: hand-written pixel primitives, a hand-authored
5x7 bitmap font, and a hand-written PNG encoder (zlib + struct).
`main.py` copies the rendered `entry.png` to `/output/entry.png`
byte-for-byte and prints its sha256. No network, no randomness.

## Reproducing it

Run `python3 draw_image.py` to regenerate `entry.png` from scratch,
then `python3 main.py` to copy it to `/output/entry.png`. Both runs
produce identical bytes: the drawing is fully deterministic, with no
timestamps, randomness, or network access anywhere in the program.
