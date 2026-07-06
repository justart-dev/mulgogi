"""피셀 경어드로 물고기 스프라이트를 정의한다."""

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


CARP = _build([
    [("  ▄▄██▄▄  ", "#ff9f43")],
    [(" ▄████●██▄ ", "#ff9f43")],
    [("█████████▌ ", "#ff9f43")],
    [(" ▀▀████▀▀  ", "#ff9f43")],
])

CRUCIAN = _build([
    [("  ▄▄██▄▄  ", "#feca57")],
    [(" ▄█", "#feca57"), ("█", "#ff9f43"), ("███", "#feca57"), ("█", "#ff9f43"), ("█▄ ", "#feca57")],
    [("█████████▌ ", "#feca57")],
    [(" ▀▀████▀▀  ", "#feca57")],
])

BLUEGILL = _build([
    [("  ▄▄██▄▄  ", "#2e86de")],
    [(" ▄█", "#2e86de"), ("●", "#1e1e1e"), ("█████▄ ", "#2e86de")],
    [("████", "#2e86de"), ("█", "#1e1e1e"), ("████▌ ", "#2e86de")],
    [(" ▀▀████▀▀  ", "#2e86de")],
])

TILAPIA = _build([
    [("  ▄▄▄██▄▄  ", "#8395a7")],
    [(" ▄███████▄ ", "#8395a7")],
    [("██████████▌", "#8395a7")],
    [(" ▀▀▀██▀▀▀  ", "#8395a7")],
])

TROUT = _build([
    [("  ▄▄██▄▄  ", "#10ac84")],
    [(" ▄█", "#10ac84"), ("■", "#006266"), ("███●██▄ ", "#10ac84")],
    [("█████", "#10ac84"), ("■", "#006266"), ("████▌ ", "#10ac84")],
    [(" ▀▀███", "#10ac84"), ("■", "#006266"), ("█▀▀  ", "#10ac84")],
])

PERCH = _build([
    [("  ▄▄██▄▄  ", "#1dd1a1")],
    [(" ▄█", "#1dd1a1"), ("█", "#10ac84"), ("███", "#1dd1a1"), ("█", "#10ac84"), ("██▄ ", "#1dd1a1")],
    [("█████████▌ ", "#1dd1a1")],
    [(" ▀▀█", "#1dd1a1"), ("█", "#10ac84"), ("██", "#1dd1a1"), ("█", "#10ac84"), ("▀▀  ", "#1dd1a1")],
])

CATFISH = _build([
    [("   ▄████▄   ", "#8d6e63")],
    [("  ▄█", "#8d6e63"), ("●", "#1e1e1e"), ("█████▄  ", "#8d6e63")],
    [(" ▀▀███████▌ ", "#8d6e63")],
    [("  ║  ▀▀▀  ║  ", "#6d4c41")],
])

BASS = _build([
    [("   ▄███▄   ", "#00d2d3")],
    [("  ▄█", "#00d2d3"), ("█", "#01a3a4"), ("██●██▄  ", "#00d2d3")],
    [(" ▀▀███████▌ ", "#00d2d3")],
    [("   ▀▀█▀▀   ", "#01a3a4")],
])

EEL = _build([
    [("           ", "#262626")],
    [(" ▄██████████▄ ", "#b8e994")],
    [("████████████▌", "#b8e994")],
    [("           ", "#262626")],
])

PIKE = _build([
    [("        ▄▄ ", "#badc58")],
    [(" ▄██████████▄", "#badc58")],
    [("█████████●█▌", "#badc58")],
    [(" ▀▀▀▀▀▀▀▀▀▀▀ ", "#badc58")],
])

STURGEON = _build([
    [("  ▄▄██▄▄  ", "#95afc0")],
    [(" ▄███●███▄ ", "#95afc0")],
    [("███", "#95afc0"), ("▲", "#535c68"), ("██████▌", "#95afc0")],
    [(" ▀▀▀▀▀▀▀▀  ", "#95afc0")],
])

SALMON = _build([
    [("  ▄▄██▄▄  ", "#ff6b6b")],
    [(" ▄█", "#ff6b6b"), ("●", "#1e1e1e"), ("█████▄ ", "#ff6b6b")],
    [("███", "#ff6b6b"), ("■", "#c0392b"), ("█████▌", "#ff6b6b")],
    [(" ▀▀███", "#ff6b6b"), ("■", "#c0392b"), ("▀▀  ", "#ff6b6b")],
])

GOLD_CARP = _build([
    [("  ▄▄██▄▄  ", "#f9ca24")],
    [(" ▄█", "#f9ca24"), ("★", "#fff200"), ("██●███▄ ", "#f9ca24")],
    [("★████████▌", "#f9ca24")],
    [(" ▀▀█", "#f9ca24"), ("★", "#fff200"), ("██▀▀  ", "#f9ca24")],
])

MACKEREL = _build([
    [("  ▄▄██▄▄  ", "#7ed6df")],
    [(" ▄█", "#7ed6df"), ("█", "#22a6b3"), ("███", "#7ed6df"), ("█", "#22a6b3"), ("██▄ ", "#7ed6df")],
    [("██", "#7ed6df"), ("█", "#22a6b3"), ("████", "#7ed6df"), ("█", "#22a6b3"), ("██▌", "#7ed6df")],
    [(" ▀▀████▀▀  ", "#7ed6df")],
])

TUNA = _build([
    [("   ▄████▄   ", "#30336b")],
    [("  ▄█", "#30336b"), ("●", "#f0f0f0"), ("█████▄  ", "#30336b")],
    [(" ▀▀███████▌ ", "#30336b")],
    [("   ▀▀█▀▀   ", "#130f40")],
])

OCTOPUS = _build([
    [("   ▄▄██▄▄   ", "#e056fd")],
    [("  ▄█", "#e056fd"), ("●", "#1e1e1e"), ("██", "#e056fd"), ("●", "#1e1e1e"), ("██▄  ", "#e056fd")],
    [("  ▀█████▀  ", "#e056fd")],
    [("  ║ ║ ║ ║  ", "#be2edd")],
])

SHARK = _build([
    [("      ▄▄  ", "#95a5a6")],
    [("  ▄█████████▄", "#95a5a6")],
    [(" ▀▀█████●███▌", "#95a5a6")],
    [("    ▀▀█▀▀  ", "#7f8c8d")],
])

MARLIN = _build([
    [("          ▄▄", "#22a6b3")],
    [(" ▄███████████▄", "#22a6b3")],
    [("██████████●█▌", "#22a6b3")],
    [("          ▀▀", "#22a6b3")],
])

WHALE = _build([
    [("   ▄▄████▄▄   ", "#3498db")],
    [("  ▄█", "#3498db"), ("●", "#f0f0f0"), ("██", "#3498db"), ("●", "#f0f0f0"), ("███▄  ", "#3498db")],
    [(" ▀▀█████████▌ ", "#3498db")],
    [("   ▀▀▀█▀▀▀   ", "#2980b9")],
])

FISH_SPRITES: dict[str, Text] = {
    "carp": CARP,
    "crucian": CRUCIAN,
    "bluegill": BLUEGILL,
    "tilapia": TILAPIA,
    "trout": TROUT,
    "perch": PERCH,
    "catfish": CATFISH,
    "bass": BASS,
    "eel": EEL,
    "pike": PIKE,
    "sturgeon": STURGEON,
    "salmon": SALMON,
    "gold_carp": GOLD_CARP,
    "mackerel": MACKEREL,
    "tuna": TUNA,
    "octopus": OCTOPUS,
    "shark": SHARK,
    "marlin": MARLIN,
    "whale": WHALE,
}


def fish_sprite(fish_id: str) -> Text:
    return FISH_SPRITES.get(fish_id, Text("?"))


def fish_icon(fish_id: str, caught: bool = True) -> Text:
    """Return a small 2-line icon for list views."""
    sprite = fish_sprite(fish_id)
    lines = str(sprite).splitlines()
    icon_lines = lines[:2]
    text = Text("\n").join(Text(line) for line in icon_lines)
    if not caught:
        text.stylize("dim #555555")
    return text


__all__ = ["fish_sprite", "fish_icon", "FISH_SPRITES"]
