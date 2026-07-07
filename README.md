# 🎣 mulgogi

**Fish in your shell** — a fishing game that runs entirely in your terminal.

`mulgogi` is a pixel-art fishing TUI built with Python + Textual.
Cast your line, time the bite, reel it in, and fill your collection — all from the comfort of your shell.

<p align="center">
  <img src="screenshots/main_menu.png" alt="mulgogi logo">
</p>

---

## Install

### pip (cross-platform)

```bash
pip install mulgogi
mulgogi
```

### Homebrew (macOS / Linux)

```bash
brew tap justart-dev/mulgogi
brew install justart-dev/mulgogi/mulgogi
mulgogi
```

### From source

```bash
git clone https://github.com/justart-dev/mulgogi.git
cd mulgogi
python3 -m mulgogi
```

---

## Controls

| Key | Action |
|---|---|
| `1` | Fish |
| `2` | Collection |
| `3` | Shop |
| `4` | Achievements |
| `5` | Stats |
| `6` | Aquarium |
| `7` | Settings |
| `q` | Quit |
| `←` / `→` | Adjust angle |
| `Space` | Cast / Bite / Stop reel |
| `Esc` | Back |

---

## Features

- **25 fish species** across ponds, rivers, lakes, and oceans — each with rarity tiers
- **Sprite styles** — switch between ASCII, block, and braille rendering in settings
- **Random events** — crabs, seagulls, rubber ducks, and more
- **Progression** — level up, unlock fishing spots, buy rods and bait
- **Collection & achievements** — catch them all and earn titles
- **Aquarium** — a serene tank where your collected fish souls swim
- **Weather** — date-based weather adds variety without losing immersion

---

## Tech Stack

- **Language:** Python 3.9+
- **TUI Framework:** [Textual](https://textual.textualize.io/)
- **Distribution:** PyPI (Trusted Publishing) + Homebrew tap

---

## License

MIT License