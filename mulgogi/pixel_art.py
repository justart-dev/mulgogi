"""물고기 스프라이트 정의.

세 가지 스타일을 제공한다:
- block: 반블록 문자를 활용한 픽셀 아트
- ascii: 텍스트 기반 ASCII 아트
- braille: 점자 패턴 (ASCII 아트를 2배 업스케일 후 변환)
"""

from rich.text import Text


def _build(lines: list[list[tuple[str, str]]]) -> Text:
    """Each inner list is a line composed of (string, color) segments."""
    result = Text()
    for i, segments in enumerate(lines):
        for chars, color in segments:
            result.append_text(Text(chars, style=f"{color}"))
        if i < len(lines) - 1:
            result.append_text(Text("\n"))
    return result


# ---------------------------------------------------------------------------
# Block sprites
# ---------------------------------------------------------------------------

CARP_BLOCK = _build([
    [("  ▄▄██▄▄  ", "#ff9f43")],
    [(" ▄████●██▄ ", "#ff9f43")],
    [("█████████▌ ", "#ff9f43")],
    [(" ▀▀████▀▀  ", "#ff9f43")],
])

CRUCIAN_BLOCK = _build([
    [("  ▄▄██▄▄  ", "#feca57")],
    [(" ▄█", "#feca57"), ("█", "#ff9f43"), ("███", "#feca57"), ("█", "#ff9f43"), ("█▄ ", "#feca57")],
    [("█████████▌ ", "#feca57")],
    [(" ▀▀████▀▀  ", "#feca57")],
])

BLUEGILL_BLOCK = _build([
    [("  .-=-.\n /(o o)\\\n  \\ - /\n   `-'", "#2e86de")],
])

TILAPIA_BLOCK = _build([
    [("   __\n  /  \\\n <`  '>\n  \\__/", "#8395a7")],
])

TROUT_BLOCK = _build([
    [("  _  __\n>(___(_)>\n ~~~~~~~", "#10ac84")],
])

PERCH_BLOCK = _build([
    [("   /\\\n  /  \\\n <_  _>\n   \\/", "#1dd1a1")],
])

CATFISH_BLOCK = _build([
    [("  __\n (  \\\\___\n  \\_____)>", "#8d6e63")],
])

BASS_BLOCK = _build([
    [("   __\n  /  \\\n <` - |>\n  \\___/", "#00d2d3")],
])

EEL_BLOCK = _build([
    [("  ~~~\n<~~~~~~~>\n  ~~~", "#b8e994")],
])

PIKE_BLOCK = _build([
    [("   /\\\n__/ o\\__\n  \\____/", "#badc58")],
])

STURGEON_BLOCK = _build([
    [("  ___\n <_(_)>\n  ~~~", "#95afc0")],
])

SALMON_BLOCK = _build([
    [("  _  __\n>(@@(_)>\n ~~~~~~~", "#ff6b6b")],
])

GOLD_CARP_BLOCK = _build([
    [("  \\*/\n*<(o o)>*\n  /| |\\\\", "#f9ca24")],
])

MACKEREL_BLOCK = _build([
    [("  .---.\n<( - )>\n  `---'", "#7ed6df")],
])

TUNA_BLOCK = _build([
    [("   ___\n  /   \\\n |  o  |\n  \\___/", "#30336b")],
])

OCTOPUS_BLOCK = _build([
    [("   .---.\n  / o o \\\n |   <   |\n  \\  -  /\n   `---'", "#e056fd")],
])

SHARK_BLOCK = _build([
    [("      /\\\n     /  \\\n    /    \\\n   /______\\\n  (  o  o  )\n   \\  ==  /\n    \\____/", "#95a5a6")],
])

MARLIN_BLOCK = _build([
    [("     /|\n    / |\n   /  |\n  /   |\n<(    |\n  \\   |\n   \\__|", "#22a6b3")],
])

WHALE_BLOCK = _build([
    [("   __---__\n  /  O O  \\\n |    >    |\n  \\_______/", "#3498db")],
])

KOI_BLOCK = _build([
    [("  \\\\*/\n*<(o o)>*\n  /| |\\\\", "#ff9f43")],
])

ZANDER_BLOCK = _build([
    [("   /\\\\\n__/ o\\__\n  \\____/", "#2ed573")],
])

PIRANHA_BLOCK = _build([
    [("   /\\\\\n__/ \\//\\__\n  \\____/", "#ff4757")],
])

RED_SNAPPER_BLOCK = _build([
    [("  .---.\n<( o )>\n  `---'", "#ff6b6b")],
])

SWORDFISH_BLOCK = _build([
    [("     /|\n    / |\n   /  |\n  /   |\n<(    |\n  \\   |\n   \\__|", "#70a1ff")],
])

JELLYFISH_BLOCK = _build([
    [("   .---.\n  / o o \\\n |   <   |\n  \\  -  /\n   `---'", "#ff9ff3")],
])


# ---------------------------------------------------------------------------
# ASCII sprites
# ---------------------------------------------------------------------------

CARP_ASCII = _build([
    [("          ______        ", "#ff9f43")],
    [("         /      \\       ", "#ff9f43")],
    [("        /        \\      ", "#ff9f43")],
    [("   >---(   ●    ●  )--->", "#ff9f43")],
    [("        \\    __    /     ", "#ff9f43")],
    [("         \\__/  \\__/      ", "#ff9f43")],
    [("           |    |        ", "#ff9f43")],
])

CRUCIAN_ASCII = _build([
    [("         /\\      /\\      ", "#feca57")],
    [("        /  \\    /  \\     ", "#feca57")],
    [("       /    \\  /    \\    ", "#feca57")],
    [("      < ( o      o ) >   ", "#feca57")],
    [("       \\    \\  /    /    ", "#feca57")],
    [("        \\    \\/    /     ", "#feca57")],
    [("         \\________/      ", "#feca57")],
])

BLUEGILL_ASCII = _build([
    [("         .--------.      ", "#2e86de")],
    [("        /    o     \\     ", "#2e86de")],
    [("       |      >      |   ", "#2e86de")],
    [("       |             |   ", "#2e86de")],
    [("        \\    ---    /    ", "#2e86de")],
    [("         '--------'      ", "#2e86de")],
])

TILAPIA_ASCII = _build([
    [("           ______        ", "#8395a7")],
    [("          /      \\       ", "#8395a7")],
    [("         /        \\      ", "#8395a7")],
    [("        |          |     ", "#8395a7")],
    [("       <(__________)>    ", "#8395a7")],
    [("          \\____/         ", "#8395a7")],
])

TROUT_ASCII = _build([
    [("            ___          ", "#10ac84")],
    [("           /   \\_____    ", "#10ac84")],
    [("      ____/  ●      ● \\  ", "#10ac84")],
    [("     /    \\      ●     > ", "#10ac84")],
    [("    /   ●   \\_________/  ", "#10ac84")],
    [("   /_________\\           ", "#10ac84")],
])

PERCH_ASCII = _build([
    [("            /\\           ", "#1dd1a1")],
    [("           /  \\          ", "#1dd1a1")],
    [("          / /\\ \\         ", "#1dd1a1")],
    [("         / /  \\ \\        ", "#1dd1a1")],
    [("        <_/    \\_>       ", "#1dd1a1")],
    [("          \\    /         ", "#1dd1a1")],
    [("           \\__/          ", "#1dd1a1")],
])

CATFISH_ASCII = _build([
    [("           ________      ", "#8d6e63")],
    [("          /        \\     ", "#8d6e63")],
    [("         |   ●    ● |    ", "#8d6e63")],
    [("         |    __    |    ", "#8d6e63")],
    [("        <____|  |____>   ", "#8d6e63")],
    [("            |  |         ", "#6d4c41")],
    [("            |  |         ", "#6d4c41")],
])

BASS_ASCII = _build([
    [("            ___          ", "#00d2d3")],
    [("           /   \\____     ", "#00d2d3")],
    [("          /  -      \\    ", "#00d2d3")],
    [("         /     -      >  ", "#00d2d3")],
    [("        /______-____/    ", "#00d2d3")],
])

EEL_ASCII = _build([
    [("   ~~~~~~~~~~~~~~~~~~~~~~~~", "#b8e994")],
    [("  <~~~~~~~~~~~~~~~~~~~~~~~~>", "#b8e994")],
    [("   ~~~~~~~~~~~~~~~~~~~~~~~~", "#b8e994")],
])

PIKE_ASCII = _build([
    [("            /\\           ", "#badc58")],
    [("        ___/  \\          ", "#badc58")],
    [("       /        \\        ", "#badc58")],
    [("      /          >       ", "#badc58")],
    [("     /__________/        ", "#badc58")],
])

STURGEON_ASCII = _build([
    [("            ________     ", "#95afc0")],
    [("           /        \\    ", "#95afc0")],
    [("          | /\\    /\\ |   ", "#95afc0")],
    [("          |/  \\  /  \\|   ", "#95afc0")],
    [("         <_|_|__|__|_|_>  ", "#95afc0")],
])

SALMON_ASCII = _build([
    [("            ___          ", "#ff6b6b")],
    [("           /   \\_____    ", "#ff6b6b")],
    [("      ____/  @      @ \\  ", "#ff6b6b")],
    [("     /    \\      @     > ", "#ff6b6b")],
    [("    /   @   \\_________/  ", "#ff6b6b")],
    [("   /_________\\           ", "#ff6b6b")],
])

GOLD_CARP_ASCII = _build([
    [("          ______         ", "#f9ca24")],
    [("         /      \\        ", "#f9ca24")],
    [("        /        \\       ", "#f9ca24")],
    [("   >---(   ★    ★  )--->", "#f9ca24")],
    [("        \\    ★    /     ", "#f9ca24")],
    [("         \\__/  \\__/      ", "#f9ca24")],
])

MACKEREL_ASCII = _build([
    [("         .----------.    ", "#7ed6df")],
    [("        /  =    =    \\   ", "#7ed6df")],
    [("       <    =    =    >  ", "#7ed6df")],
    [("        \\  =    =    /   ", "#7ed6df")],
    [("         '----------'    ", "#7ed6df")],
])

TUNA_ASCII = _build([
    [("           ________      ", "#30336b")],
    [("          /        \\     ", "#30336b")],
    [("         |    ●     |    ", "#30336b")],
    [("         |          |    ", "#30336b")],
    [("        <(__________)>   ", "#30336b")],
])

OCTOPUS_ASCII = _build([
    [("            .------.     ", "#e056fd")],
    [("           /  ●  ●  \\    ", "#e056fd")],
    [("          |     <     |  ", "#e056fd")],
    [("           \\   ===   /   ", "#e056fd")],
    [("            | | | | |    ", "#be2edd")],
    [("           /  | | |  \\   ", "#be2edd")],
])

SHARK_ASCII = _build([
    [("              /\\         ", "#95a5a6")],
    [("         ____/  \\____    ", "#95a5a6")],
    [("        /            \\   ", "#95a5a6")],
    [("       /   ●        ●  > ", "#95a5a6")],
    [("      /_____||________/  ", "#7f8c8d")],
    [("           |||           ", "#7f8c8d")],
    [("          |||            ", "#7f8c8d")],
])

MARLIN_ASCII = _build([
    [("         /|              ", "#22a6b3")],
    [("        / |    /\\        ", "#22a6b3")],
    [("       /  |___/  \\___    ", "#22a6b3")],
    [("      /   |          _>  ", "#22a6b3")],
    [("     /    |         /    ", "#22a6b3")],
    [("    <_____|_________/    ", "#22a6b3")],
])

WHALE_ASCII = _build([
    [("        _____ _____      ", "#3498db")],
    [("       /     V     \\     ", "#3498db")],
    [("      |  ●       ●  |    ", "#3498db")],
    [("      |      >      |    ", "#3498db")],
    [("       \\___________/     ", "#3498db")],
    [("        \\_________/      ", "#2980b9")],
])

KOI_ASCII = _build([
    [("          ______         ", "#ff9f43")],
    [("         /      \\        ", "#ff9f43")],
    [("        /        \\       ", "#ff9f43")],
    [("   >---(   ●    ●  )--->", "#ff9f43")],
    [("        \\  \\__/  /       ", "#f0f0f0")],
    [("         \\_/    \\_/      ", "#f0f0f0")],
])

ZANDER_ASCII = _build([
    [("            ___          ", "#2ed573")],
    [("           /   \\_____    ", "#2ed573")],
    [("      ____/  ◇      ◇ \\  ", "#2ed573")],
    [("     /    \\      ◇     > ", "#2ed573")],
    [("    /   ◇   \\_________/  ", "#2ed573")],
    [("   /_________\\           ", "#2ed573")],
])

PIRANHA_ASCII = _build([
    [("            ___          ", "#ff4757")],
    [("           /   \\_____    ", "#ff4757")],
    [("      ____/  ▼▼▼     \\  ", "#ff4757")],
    [("     /    \\    ▼▼▼    > ", "#ff4757")],
    [("    / ▼▼▼   \\_________/  ", "#ff4757")],
    [("   /_________\\           ", "#ff4757")],
])

RED_SNAPPER_ASCII = _build([
    [("         .--------.      ", "#ff6b6b")],
    [("        /    o     \\     ", "#ff6b6b")],
    [("       |      >      |   ", "#ff6b6b")],
    [("       |             |   ", "#ff6b6b")],
    [("        \\    ---    /    ", "#ff6b6b")],
    [("         '--------'      ", "#ff6b6b")],
])

SWORDFISH_ASCII = _build([
    [("            |            ", "#70a1ff")],
    [("           /|\\           ", "#70a1ff")],
    [("          / | \\          ", "#70a1ff")],
    [("         /  |  \\_____    ", "#70a1ff")],
    [("        /   |        >   ", "#70a1ff")],
    [("       <____|________/   ", "#70a1ff")],
])

JELLYFISH_ASCII = _build([
    [("            .------.     ", "#ff9ff3")],
    [("           (  ●  ●  )    ", "#ff9ff3")],
    [("            '------'     ", "#f368e0")],
    [("            | |||| |     ", "#f368e0")],
    [("            | |||| |     ", "#f368e0")],
])


# ---------------------------------------------------------------------------
# Braille sprites (generated from ASCII sprites)
# ---------------------------------------------------------------------------

def _ascii_to_braille(text_sprite: Text) -> Text:
    """Convert an ASCII text sprite to a Braille pattern sprite.

    Each ASCII character is upscaled 2x in both directions, then grouped
    into 2x4 Braille cells.
    """
    import re

    lines = str(text_sprite).split("\n")
    if not lines:
        return Text("")

    # Upscale 2x (pad lines to equal width first)
    upscaled: list[str] = []
    max_w = max((len(line) for line in lines), default=0)
    for line in lines:
        padded = line.ljust(max_w)
        expanded = "".join(ch * 2 for ch in padded)
        upscaled.append(expanded)
        upscaled.append(expanded)

    h = len(upscaled)
    w = len(upscaled[0]) if h else 0

    # Braille dot mapping for a 2(wide) x 4(tall) cell:
    # (dx, dy) -> bit index
    dots = [
        (0, 0, 0),
        (0, 1, 1),
        (0, 2, 2),
        (1, 0, 3),
        (1, 1, 4),
        (1, 2, 5),
        (0, 3, 6),
        (1, 3, 7),
    ]

    # Determine a single base color from the source text markup.
    base_color = "#ffffff"
    markup = text_sprite.markup
    match = re.search(r"#([0-9a-fA-F]{6})", markup)
    if match:
        base_color = f"#{match.group(1)}"

    braille_lines: list[list[tuple[str, str]]] = []
    for y in range(0, h, 4):
        row: list[tuple[str, str]] = []
        for x in range(0, w, 2):
            offset = 0
            for dx, dy, bit in dots:
                px = x + dx
                py = y + dy
                if 0 <= px < w and 0 <= py < h and upscaled[py][px] != " ":
                    offset |= 1 << bit
            row.append((chr(0x2800 + offset), base_color))
        braille_lines.append(row)
    return _build(braille_lines)


CARP_BRAILLE = _ascii_to_braille(CARP_ASCII)
CRUCIAN_BRAILLE = _ascii_to_braille(CRUCIAN_ASCII)
BLUEGILL_BRAILLE = _ascii_to_braille(BLUEGILL_ASCII)
TILAPIA_BRAILLE = _ascii_to_braille(TILAPIA_ASCII)
TROUT_BRAILLE = _ascii_to_braille(TROUT_ASCII)
PERCH_BRAILLE = _ascii_to_braille(PERCH_ASCII)
CATFISH_BRAILLE = _ascii_to_braille(CATFISH_ASCII)
BASS_BRAILLE = _ascii_to_braille(BASS_ASCII)
EEL_BRAILLE = _ascii_to_braille(EEL_ASCII)
PIKE_BRAILLE = _ascii_to_braille(PIKE_ASCII)
STURGEON_BRAILLE = _ascii_to_braille(STURGEON_ASCII)
SALMON_BRAILLE = _ascii_to_braille(SALMON_ASCII)
GOLD_CARP_BRAILLE = _ascii_to_braille(GOLD_CARP_ASCII)
MACKEREL_BRAILLE = _ascii_to_braille(MACKEREL_ASCII)
TUNA_BRAILLE = _ascii_to_braille(TUNA_ASCII)
OCTOPUS_BRAILLE = _ascii_to_braille(OCTOPUS_ASCII)
SHARK_BRAILLE = _ascii_to_braille(SHARK_ASCII)
MARLIN_BRAILLE = _ascii_to_braille(MARLIN_ASCII)
WHALE_BRAILLE = _ascii_to_braille(WHALE_ASCII)
KOI_BRAILLE = _ascii_to_braille(KOI_ASCII)
ZANDER_BRAILLE = _ascii_to_braille(ZANDER_ASCII)
PIRANHA_BRAILLE = _ascii_to_braille(PIRANHA_ASCII)
RED_SNAPPER_BRAILLE = _ascii_to_braille(RED_SNAPPER_ASCII)
SWORDFISH_BRAILLE = _ascii_to_braille(SWORDFISH_ASCII)
JELLYFISH_BRAILLE = _ascii_to_braille(JELLYFISH_ASCII)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

STYLE_MAP: dict[str, dict[str, Text]] = {
    "carp": {
        "block": CARP_BLOCK,
        "ascii": CARP_ASCII,
        "braille": CARP_BRAILLE,
    },
    "crucian": {
        "block": CRUCIAN_BLOCK,
        "ascii": CRUCIAN_ASCII,
        "braille": CRUCIAN_BRAILLE,
    },
    "bluegill": {
        "block": BLUEGILL_BLOCK,
        "ascii": BLUEGILL_ASCII,
        "braille": BLUEGILL_BRAILLE,
    },
    "tilapia": {
        "block": TILAPIA_BLOCK,
        "ascii": TILAPIA_ASCII,
        "braille": TILAPIA_BRAILLE,
    },
    "trout": {
        "block": TROUT_BLOCK,
        "ascii": TROUT_ASCII,
        "braille": TROUT_BRAILLE,
    },
    "perch": {
        "block": PERCH_BLOCK,
        "ascii": PERCH_ASCII,
        "braille": PERCH_BRAILLE,
    },
    "catfish": {
        "block": CATFISH_BLOCK,
        "ascii": CATFISH_ASCII,
        "braille": CATFISH_BRAILLE,
    },
    "bass": {
        "block": BASS_BLOCK,
        "ascii": BASS_ASCII,
        "braille": BASS_BRAILLE,
    },
    "eel": {
        "block": EEL_BLOCK,
        "ascii": EEL_ASCII,
        "braille": EEL_BRAILLE,
    },
    "pike": {
        "block": PIKE_BLOCK,
        "ascii": PIKE_ASCII,
        "braille": PIKE_BRAILLE,
    },
    "sturgeon": {
        "block": STURGEON_BLOCK,
        "ascii": STURGEON_ASCII,
        "braille": STURGEON_BRAILLE,
    },
    "salmon": {
        "block": SALMON_BLOCK,
        "ascii": SALMON_ASCII,
        "braille": SALMON_BRAILLE,
    },
    "gold_carp": {
        "block": GOLD_CARP_BLOCK,
        "ascii": GOLD_CARP_ASCII,
        "braille": GOLD_CARP_BRAILLE,
    },
    "mackerel": {
        "block": MACKEREL_BLOCK,
        "ascii": MACKEREL_ASCII,
        "braille": MACKEREL_BRAILLE,
    },
    "tuna": {
        "block": TUNA_BLOCK,
        "ascii": TUNA_ASCII,
        "braille": TUNA_BRAILLE,
    },
    "octopus": {
        "block": OCTOPUS_BLOCK,
        "ascii": OCTOPUS_ASCII,
        "braille": OCTOPUS_BRAILLE,
    },
    "shark": {
        "block": SHARK_BLOCK,
        "ascii": SHARK_ASCII,
        "braille": SHARK_BRAILLE,
    },
    "marlin": {
        "block": MARLIN_BLOCK,
        "ascii": MARLIN_ASCII,
        "braille": MARLIN_BRAILLE,
    },
    "whale": {
        "block": WHALE_BLOCK,
        "ascii": WHALE_ASCII,
        "braille": WHALE_BRAILLE,
    },
    "koi": {
        "block": KOI_BLOCK,
        "ascii": KOI_ASCII,
        "braille": KOI_BRAILLE,
    },
    "zander": {
        "block": ZANDER_BLOCK,
        "ascii": ZANDER_ASCII,
        "braille": ZANDER_BRAILLE,
    },
    "piranha": {
        "block": PIRANHA_BLOCK,
        "ascii": PIRANHA_ASCII,
        "braille": PIRANHA_BRAILLE,
    },
    "red_snapper": {
        "block": RED_SNAPPER_BLOCK,
        "ascii": RED_SNAPPER_ASCII,
        "braille": RED_SNAPPER_BRAILLE,
    },
    "swordfish": {
        "block": SWORDFISH_BLOCK,
        "ascii": SWORDFISH_ASCII,
        "braille": SWORDFISH_BRAILLE,
    },
    "jellyfish": {
        "block": JELLYFISH_BLOCK,
        "ascii": JELLYFISH_ASCII,
        "braille": JELLYFISH_BRAILLE,
    },
}

VALID_STYLES = ["ascii", "block", "braille"]


def fish_sprite(fish_id: str, style: str = "ascii") -> Text:
    """Return the sprite for a fish in the requested style."""
    style = style if style in VALID_STYLES else "ascii"
    fish_styles = STYLE_MAP.get(fish_id, {})
    return fish_styles.get(style, Text("?"))


def fish_icon(fish_id: str, style: str = "ascii", caught: bool = True) -> Text:
    """Return a small 2-line icon for list views."""
    sprite = fish_sprite(fish_id, style)
    lines = sprite.split("\n")[:2]
    text = Text("\n").join(lines)
    if not caught:
        text.stylize("dim #555555")
    return text


__all__ = ["fish_sprite", "fish_icon", "STYLE_MAP", "VALID_STYLES"]
