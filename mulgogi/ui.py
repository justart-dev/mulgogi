"""TUI 화면 구성"""

import math
import random
import time
from datetime import datetime

from rich.console import RenderableType
from rich.text import Text

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

from .data import (
    ACHIEVEMENT_DATA,
    BAIT_BY_ID,
    BAIT_DATA,
    FISH_BY_ID,
    FISH_DATA,
    ROD_BY_ID,
    ROD_DATA,
    SPOT_BY_ID,
    SPOT_DATA,
    RARITY_NAMES,
    RARITY_STARS,
    RARITY_COLORS,
    Fish,
)
from .game import GameState, save_state
from .i18n import (
    LANGUAGE_NAMES,
    achievement_description,
    achievement_name,
    achievement_title,
    bait_description,
    bait_name,
    fish_name,
    normalize_language,
    rod_description,
    rod_name,
    spot_description,
    spot_name,
    t,
    time_label,
    title_label,
    weather_label,
)
from .particles import ParticleEmitter, ParticleOverlay
from .pixel_art import fish_sprite, VALID_STYLES


def lang(state: GameState) -> str:
    return normalize_language(state.language)


def current_time_of_day() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 8:
        return "dawn"
    if 8 <= hour < 17:
        return "day"
    if 17 <= hour < 20:
        return "dusk"
    return "night"


def current_weather() -> str:
    # 게임 속 날씨는 실제 날짜를 기준으로 결정 (같은 날은 같은 날씨)
    today = datetime.now().date()
    rng = random.Random(today.toordinal())
    return rng.choice(["sunny", "cloudy", "rainy"])


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def gradient_text(text: str, colors: list[str], bold: bool = True) -> Text:
    """Render text with a horizontal color gradient."""
    if not text:
        return Text("")
    rgb_colors = [_hex_to_rgb(c) for c in colors]
    result = Text()
    for i, char in enumerate(text):
        t = i / max(len(text) - 1, 1)
        # pick segment and local position
        segment = t * (len(rgb_colors) - 1)
        idx = int(segment)
        local_t = segment - idx
        c1 = rgb_colors[min(idx, len(rgb_colors) - 1)]
        c2 = rgb_colors[min(idx + 1, len(rgb_colors) - 1)]
        r = int(c1[0] + (c2[0] - c1[0]) * local_t)
        g = int(c1[1] + (c2[1] - c1[1]) * local_t)
        b = int(c1[2] + (c2[2] - c1[2]) * local_t)
        style = _rgb_to_hex(r, g, b)
        if bold:
            style = f"bold {style}"
        result.append_text(Text(char, style=style))
    return result


MULGOGI_ASCII = """███╗   ███╗██╗   ██╗██╗      ██████╗  ██████╗  ██████╗ ██╗
████╗ ████║██║   ██║██║     ██╔════╝ ██╔═══██╗██╔════╝ ██║
██╔████╔██║██║   ██║██║     ██║  ███╗██║   ██║██║  ███╗██║
██║╚██╔╝██║██║   ██║██║     ██║   ██║██║   ██║██║   ██║██║
██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╔╝╚██████╔╝██║
╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝
"""


class PlainStatic(Static):
    """Rich 마크업을 파싱하지 않는 Static. 사용자 데이터나 괄호가 포함된 텍스트에 안전."""

    def __init__(self, content: RenderableType = "", *, markup=False, **kwargs):
        super().__init__(content, markup=markup, **kwargs)

    def update(self, content: RenderableType = "", *, markup=False):
        # Always keep markup disabled regardless of caller; parent uses self._render_markup.
        return super().update(content)


class SplashWidget(Static):
    frame = reactive(0)

    def __init__(self, **kwargs):
        super().__init__("", **kwargs)
        self._timer = None
        self._running = False

    def on_mount(self):
        self._running = True
        self._timer = self.set_interval(0.15, self._tick)

    def _tick(self):
        if not self._running:
            return
        self.frame += 1
        waves = ["~", "-", "≈", "∿", "~"]
        lines = []
        for row in range(5):
            line = ""
            for col in range(40):
                idx = (self.frame + row * 3 + col) % len(waves)
                line += waves[idx]
            lines.append(line)
        self.update("\n".join(lines))

    def stop(self):
        self._running = False
        if self._timer:
            self._timer.stop()

    def start(self):
        self._running = True
        if self._timer:
            self._timer.stop()
        self._timer = self.set_interval(0.15, self._tick)


class AngleWidget(Static):
    angle = reactive(45)
    language = reactive("en")

    def render(self):
        length = 10
        x, y = 15, 5
        grid = [[" " for _ in range(40)] for _ in range(8)]
        rad = math.radians(self.angle)
        dx = math.cos(rad)
        dy = -math.sin(rad)
        for i in range(length):
            px = x + int(round(i * dx * 0.8))
            py = y + int(round(i * dy * 0.8))
            px = max(0, min(39, px))
            py = max(0, min(7, py))
            grid[py][px] = "/" if i < length - 1 else "@"
        grid[5][12] = "O"
        lines = ["".join(row) for row in grid]
        lines_joined = "\n".join(lines)
        return f"{lines_joined}\n\n{t(self.language, 'angle')}: {self.angle}°"


class ReelWidget(Static):
    position = reactive(0.0)
    target_range = reactive(0.2)
    language = reactive("en")

    def render(self):
        bar_width = 30
        pos = int(self.position * (bar_width - 1))
        pos = max(0, min(bar_width - 1, pos))
        center = bar_width // 2
        half = max(1, int(self.target_range * bar_width / 2))
        parts = []
        for i in range(bar_width):
            if i == pos:
                parts.append(Text("O", style="bold white"))
            elif center - half <= i <= center + half:
                parts.append(Text("=", style="green"))
            else:
                parts.append(Text("-", style="dim"))
        bar_text = Text.assemble(*parts)
        return Text.assemble(
            t(self.language, "reel_instruction_start"),
            Text("O", style="bold white"),
            t(self.language, "reel_instruction_middle"),
            Text(t(self.language, "green_zone"), style="green"),
            t(self.language, "reel_instruction_end"),
            bar_text,
            "]",
        )


class MainMenuScreen(Screen):
    BINDINGS = [
        ("1", "fish", "Fish"),
        ("2", "collection", "Collection"),
        ("3", "shop", "Shop"),
        ("4", "achievements", "Achievements"),
        ("5", "stats", "Stats"),
        ("6", "aquarium", "Aquarium"),
        ("7", "settings", "Settings"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        language = lang(self.app.game_state)
        with Vertical(classes="menu"):
            yield PlainStatic(MULGOGI_ASCII, classes="title")
            yield PlainStatic(gradient_text("Fish in your shell", ["#33d9b2", "#f1fa8c"]), classes="subtitle")
            yield PlainStatic("")
            yield Button(f"1. {t(language, 'fish_action')}", id="fish")
            yield Button(f"2. {t(language, 'collection')}", id="collection")
            yield Button(f"3. {t(language, 'shop')}", id="shop")
            yield Button(f"4. {t(language, 'achievements')}", id="achievements")
            yield Button(f"5. {t(language, 'stats')}", id="stats")
            yield Button(f"6. {t(language, 'aquarium')}", id="aquarium")
            yield Button(f"7. {t(language, 'settings')}", id="settings")
            yield Button(f"q. {t(language, 'quit')}", id="quit", variant="error")
            yield PlainStatic("")
            yield PlainStatic(t(language, "menu_help"), classes="help")
        yield Footer()

    def on_mount(self):
        self.query_one("#fish", Button).focus()

    def on_key(self, event):
        buttons = list(self.query(Button))
        if not buttons:
            return
        current = self.app.focused
        try:
            idx = buttons.index(current)
        except ValueError:
            idx = 0
        if event.key == "down":
            idx = (idx + 1) % len(buttons)
            buttons[idx].focus()
            event.stop()
        elif event.key == "up":
            idx = (idx - 1) % len(buttons)
            buttons[idx].focus()
            event.stop()

    def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id == "fish":
            self.app.push_screen(SpotSelectScreen(self.app.game_state))
        elif button_id == "collection":
            self.app.push_screen(CollectionScreen(self.app.game_state))
        elif button_id == "shop":
            self.app.push_screen(ShopScreen(self.app.game_state))
        elif button_id == "achievements":
            self.app.push_screen(AchievementsScreen(self.app.game_state))
        elif button_id == "stats":
            self.app.push_screen(StatsScreen(self.app.game_state))
        elif button_id == "aquarium":
            self.app.push_screen(AquariumScreen(self.app.game_state))
        elif button_id == "settings":
            self.app.push_screen(SettingsScreen(self.app.game_state))
        elif button_id == "quit":
            self.app.exit()

    def action_fish(self):
        self.app.push_screen(SpotSelectScreen(self.app.game_state))

    def action_collection(self):
        self.app.push_screen(CollectionScreen(self.app.game_state))

    def action_shop(self):
        self.app.push_screen(ShopScreen(self.app.game_state))

    def action_achievements(self):
        self.app.push_screen(AchievementsScreen(self.app.game_state))

    def action_stats(self):
        self.app.push_screen(StatsScreen(self.app.game_state))

    def action_aquarium(self):
        self.app.push_screen(AquariumScreen(self.app.game_state))

    def action_settings(self):
        self.app.push_screen(SettingsScreen(self.app.game_state))

    def action_quit(self):
        self.app.exit()


class FishingScreen(Screen):
    BINDINGS = [
        ("escape", "back", "Back"),
        ("q", "back", "Back"),
    ]

    def __init__(self, state: GameState, spot_id: str = "pond", **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.spot_id = spot_id
        self.phase = "menu"  # menu, waiting, biting, reeling, result
        self.angle = 45
        self.bite_timer = None
        self.reel_timer = None
        self.event_timer = None
        self.reel_pos = 0.0
        self.reel_dir = 1
        self.reel_speed = 0.06
        self.weather = current_weather()
        self.time_of_day = current_time_of_day()

    def compose(self) -> ComposeResult:
        language = lang(self.state)
        with Vertical(id="fishing-main"):
            yield PlainStatic(self._status_text(), id="status")
            yield PlainStatic(self._spot_text(), id="spot-info")
            angle = AngleWidget(id="angle")
            angle.language = language
            yield angle
            yield SplashWidget(id="splash")
            reel = ReelWidget(id="reel")
            reel.language = language
            yield reel
            yield PlainStatic("", id="result")
            yield Static(t(language, "fishing_help"), id="help")
            yield ParticleOverlay(id="particles")
        yield Footer()

    def on_mount(self):
        self.query_one("#splash", SplashWidget).display = False
        self.query_one("#reel", ReelWidget).display = False

    def _status_text(self) -> str:
        p = self.state.player
        rod = self.state.current_rod()
        bait = self.state.current_bait()
        language = lang(self.state)
        title_tag = f"({title_label(language, p.title)}) " if p.title else ""
        bait_text = bait_name(language, bait) if bait else "-"
        return (
            f"{title_tag}{t(language, 'level_short')}{p.level}  "
            f"{t(language, 'gold')}:{p.gold}  "
            f"{t(language, 'rod')}:{rod_name(language, rod)}  "
            f"{t(language, 'bait')}:{bait_text}"
        )

    def _spot_text(self) -> str:
        spot = SPOT_BY_ID[self.spot_id]
        language = lang(self.state)
        return (
            f"{t(language, 'spot')}: {spot_name(language, spot)} | "
            f"{t(language, 'time')}: {time_label(language, self.time_of_day)} | "
            f"{t(language, 'weather')}: {weather_label(language, self.weather)}"
        )

    def on_key(self, event):
        key = event.key
        if key in ("escape", "q"):
            self.action_back()
            return

        if self.phase == "menu":
            if key == "left":
                self.angle = max(10, self.angle - 5)
                self.query_one("#angle", AngleWidget).angle = self.angle
            elif key == "right":
                self.angle = min(80, self.angle + 5)
                self.query_one("#angle", AngleWidget).angle = self.angle
            elif key == "space":
                self.start_cast()
        elif self.phase == "biting":
            if key == "space":
                self.start_reel()
        elif self.phase == "reeling":
            if key == "space":
                self.stop_reel()
        elif self.phase == "result":
            if key == "space":
                self.reset()

    def start_cast(self):
        self.phase = "waiting"
        self.state.stats.total_casts += 1
        self.query_one("#status", Static).update(self._status_text())
        self.query_one("#help", Static).update(t(lang(self.state), "waiting"))
        self.query_one("#angle", AngleWidget).display = False
        splash = self.query_one("#splash", SplashWidget)
        splash.start()
        splash.display = True
        self.query_one("#result", PlainStatic).update("")
        self.pending_bite_delay = random.uniform(3.0, 10.0)
        event_delay = random.uniform(1.0, 2.0)
        self.event_timer = self.set_timer(event_delay, self._check_random_event)

    def _check_random_event(self):
        if self.phase != "waiting":
            return
        roll = random.random()
        events = [
            ("crab", 0.01),
            ("seagull", 0.01),
            ("worm_revolt", 0.01),
            ("fish_tease", 0.01),
            ("rubber_duck", 0.01),
        ]
        cumulative = 0.0
        for name, prob in events:
            cumulative += prob
            if roll < cumulative:
                self._trigger_event(name)
                return
        # 아무 이벤트도 없으면 정상 입질 타이머 시작
        self.bite_timer = self.set_timer(self.pending_bite_delay, self.trigger_bite)

    def _trigger_event(self, event_name: str):
        self._stop_all_timers()
        self.phase = "result"
        self.query_one("#splash", SplashWidget).stop()
        self.query_one("#splash", SplashWidget).display = False
        self.query_one("#help", Static).update(t(lang(self.state), "continue_back"))

        if event_name == "crab":
            self._event_bait_thief_crab()
        elif event_name == "seagull":
            self._event_seagull_steal()
        elif event_name == "worm_revolt":
            self._event_worm_revolt()
        elif event_name == "fish_tease":
            self._event_fish_tease()
        elif event_name == "rubber_duck":
            self._event_rubber_duck()

        save_state(self.state)

    def _event_bait_thief_crab(self):
        self.state.player.bait_id = "worm"
        self.query_one("#status", Static).update(self._status_text())
        self.query_one("#result", PlainStatic).update(
            Text(t(lang(self.state), "crab_event"), style="yellow")
        )

    def _event_seagull_steal(self):
        fish = self._pick_fish()
        language = lang(self.state)
        result_text = Text.assemble(
            (t(language, "seagull_event"), "red"),
            "\n\n",
            fish_sprite(fish.id, self.state.sprite_style),
            "\n\n",
            f"{t(language, 'escaped_fish')}: {fish_name(language, fish)} "
            f"({t(language, 'rarity')}: {RARITY_NAMES[fish.rarity]} {RARITY_STARS[fish.rarity]})",
        )
        self.query_one("#result", PlainStatic).update(result_text)

    def _event_worm_revolt(self):
        leveled_up = self.state.add_exp(3)
        language = lang(self.state)
        self.query_one("#status", Static).update(self._status_text())
        result_text = Text.assemble(
            (t(language, "worm_event_1"), "magenta"),
            "\n",
            t(language, "worm_event_2"),
            ("\n" + t(language, "exp_gain", amount=3), "green"),
            (t(language, "level_up"), "bold yellow") if leveled_up else ("", ""),
        )
        self.query_one("#result", PlainStatic).update(result_text)

    def _event_fish_tease(self):
        self.query_one("#result", PlainStatic).update(
            Text(t(lang(self.state), "tease_event"), style="red")
        )

    def _event_rubber_duck(self):
        duck_sprite = (
            "    _      _      _\n"
            "  >(.)__ <(.)__ =(.)__\n"
            "   (___/  (___/  (___/\n"
        )
        self.query_one("#result", PlainStatic).update(
            Text.assemble(
                (t(lang(self.state), "duck_event"), "yellow"),
                "\n\n",
                duck_sprite,
                "\n",
                t(lang(self.state), "duck_event_2"),
            )
        )

    def trigger_bite(self):
        if self.phase != "waiting":
            return
        self.phase = "biting"
        self.query_one("#help", Static).update(f"[bold][red]{t(lang(self.state), 'bite')}[/red][/bold]")
        self.bite_timer = self.set_timer(1.5, self.miss_bite)

    def miss_bite(self):
        if self.phase != "biting":
            return
        self.phase = "result"
        self.query_one("#splash", SplashWidget).stop()
        self.query_one("#splash", SplashWidget).display = False
        self.query_one("#help", Static).update(t(lang(self.state), "continue"))
        self.query_one("#result", PlainStatic).update(Text(t(lang(self.state), "missed_bite"), style="red"))
        save_state(self.state)

    def start_reel(self):
        self._stop_all_timers()
        self.phase = "reeling"
        rod = self.state.current_rod()
        success_range = 0.2 + rod.reel_bonus
        self.query_one("#help", Static).update(
            f"[bold][cyan]{t(lang(self.state), 'hook_set')}[/cyan][/bold]"
        )
        reel = self.query_one("#reel", ReelWidget)
        reel.target_range = success_range
        self.reel_pos = 0.0
        self.reel_dir = 1
        self.reel_speed = random.uniform(0.04, 0.10)
        self.reel_timer = self.set_interval(0.05, self.update_reel)

    def _stop_all_timers(self):
        if self.bite_timer:
            self.bite_timer.stop()
            self.bite_timer = None
        if self.event_timer:
            self.event_timer.stop()
            self.event_timer = None
        if self.reel_timer:
            self.reel_timer.stop()
            self.reel_timer = None

    def update_reel(self):
        self.reel_pos += self.reel_dir * self.reel_speed
        if self.reel_pos >= 1.0:
            self.reel_pos = 1.0
            self.reel_dir = -1
        elif self.reel_pos <= 0.0:
            self.reel_pos = 0.0
            self.reel_dir = 1
        widget = self.query_one("#reel", ReelWidget)
        widget.position = self.reel_pos
        widget.display = True

    def stop_reel(self):
        self._stop_all_timers()
        self.query_one("#reel", ReelWidget).display = False
        self.query_one("#splash", SplashWidget).stop()
        self.query_one("#splash", SplashWidget).display = False

        rod = self.state.current_rod()
        success_range = 0.2 + rod.reel_bonus
        center = 0.5
        if center - success_range / 2 <= self.reel_pos <= center + success_range / 2:
            self.catch_fish()
        else:
            self.lose_fish()

    def _pick_fish(self) -> Fish:
        spot = SPOT_BY_ID[self.spot_id]
        candidates = [FISH_BY_ID[fid] for fid in spot.fish_ids if fid in FISH_BY_ID]
        weights = []
        bait = self.state.current_bait()
        for fish in candidates:
            w = 1.0 / fish.rarity
            if fish.preferred_time == self.time_of_day or fish.preferred_time == "any":
                w *= 1.5
            if fish.preferred_weather == self.weather or fish.preferred_weather == "any":
                w *= 1.5
            if bait and bait.target_fish_id == fish.id:
                w *= 3.0
            w *= 1 + self.state.current_rod().cast_bonus + (bait.attract_bonus if bait else 0)
            weights.append(max(w, 0.01))
        return random.choices(candidates, weights=weights, k=1)[0]

    def catch_fish(self):
        self.phase = "result"
        fish = self._pick_fish()
        weight = round(random.uniform(fish.min_weight, fish.max_weight), 2)
        gold, exp, leveled_up, new_achievements = self.state.record_catch(
            fish, weight, self.time_of_day
        )
        self.state.unlock_spots()
        save_state(self.state)

        if new_achievements:
            language = lang(self.state)
            names = ", ".join(achievement_name(language, a) for a in new_achievements)
            titles = [a.title for a in new_achievements if a.title]
            title_text = (
                t(language, "title_result", titles=", ".join(title_label(language, title) for title in titles))
                if titles else ""
            )
        else:
            names = ""
            title_text = ""

        language = lang(self.state)
        self.query_one("#status", Static).update(self._status_text())
        self.query_one("#help", Static).update(t(language, "continue_back"))
        result_text = Text.assemble(
            (t(language, "caught", fish=fish_name(language, fish)), "green"),
            (t(language, "level_up"), "bold yellow") if leveled_up else ("", ""),
            (
                t(language, "achievement_unlocked", names=names, title_text=title_text),
                "bold magenta",
            ) if new_achievements else ("", ""),
            "\n\n",
            fish_sprite(fish.id, self.state.sprite_style),
            "\n\n",
            (
                f"{t(language, 'weight')}: {weight}kg |  "
                f"{t(language, 'rarity')}: {RARITY_NAMES[fish.rarity]} {RARITY_STARS[fish.rarity]}\n"
            ),
            t(language, "gold_exp_gain", gold=gold, exp=exp),
        )
        self.query_one("#result", PlainStatic).update(result_text)
        self.query_one("#particles", ParticleOverlay).burst()

    def lose_fish(self):
        self.phase = "result"
        self.query_one("#help", Static).update(t(lang(self.state), "continue_back"))
        self.query_one("#result", PlainStatic).update(Text(t(lang(self.state), "fish_escaped"), style="red"))
        save_state(self.state)

    def reset(self):
        self.phase = "menu"
        self.query_one("#angle", AngleWidget).display = True
        self.query_one("#splash", SplashWidget).display = False
        self.query_one("#reel", ReelWidget).display = False
        self.query_one("#particles", ParticleOverlay).clear()
        self.query_one("#help", Static).update(t(lang(self.state), "fishing_help_reset"))
        self.query_one("#result", PlainStatic).update("")

    def action_back(self):
        self._stop_all_timers()
        self.query_one("#splash", SplashWidget).stop()
        save_state(self.state)
        self.app.pop_screen()


class CollectionScreen(Screen):
    BINDINGS = [
        ("escape", "back", "Back"),
        ("q", "back", "Back"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        language = lang(self.state)
        with Vertical(classes="collection"):
            yield PlainStatic(t(language, "collection"), classes="title")
            yield PlainStatic(
                t(language, "collection_count", total=len(FISH_DATA), caught=len(self.state.collection)),
                id="count",
            )
            yield PlainStatic("")
            fish_lines = []
            for fish in FISH_DATA:
                rec = self.state.collection.get(fish.id)
                if rec:
                    line = Text.assemble(
                        ("✓", "green"),
                        f" {fish_name(language, fish)}  {RARITY_STARS[fish.rarity]}  "
                        f"{t(language, 'max_weight', weight=rec.max_weight)}  x{rec.count}",
                    )
                else:
                    line = Text.assemble(
                        ("? ? ?", "dim"),
                        f"  {RARITY_STARS[fish.rarity]}  ???",
                    )
                fish_lines.append(line)
            yield PlainStatic(Text("\n").join(fish_lines), id="fish-list")
            yield PlainStatic("")
            yield PlainStatic(t(language, "back_help"), id="help")
        yield Footer()

    def action_back(self):
        self.app.pop_screen()


class ShopScreen(Screen):
    BINDINGS = [
        ("escape", "back", "Back"),
        ("q", "back", "Back"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        language = lang(self.state)
        with Vertical(classes="shop"):
            yield PlainStatic(t(language, "shop"), classes="title")
            yield PlainStatic(t(language, "gold_owned", gold=self.state.player.gold), id="gold")
            yield PlainStatic("")
            yield PlainStatic(t(language, "rods"), classes="section")
            for rod in ROD_DATA:
                owned = rod.id == self.state.player.rod_id
                status = t(language, "owned") if owned else f"{rod.price} {t(language, 'gold')}"
                btn = Button(Text(f"{rod_name(language, rod)} - {status}"), id=f"rod-{rod.id}", disabled=owned)
                btn.description = rod_description(language, rod)
                yield btn
            yield PlainStatic("")
            yield PlainStatic(t(language, "bait_section"), classes="section")
            for bait in BAIT_DATA:
                owned = bait.id == self.state.player.bait_id
                status = t(language, "equipped") if owned else f"{bait.price} {t(language, 'gold')}"
                btn = Button(Text(f"{bait_name(language, bait)} - {status}"), id=f"bait-{bait.id}", disabled=owned)
                btn.description = bait_description(language, bait)
                yield btn
            yield PlainStatic("")
            yield PlainStatic("", id="desc")
            yield PlainStatic(t(language, "back_help"), id="help")
        yield Footer()

    def _find_button(self, widget):
        while widget and not isinstance(widget, Button):
            widget = widget.parent
        return widget

    def _update_desc(self, widget):
        btn = self._find_button(widget)
        desc = self.query_one("#desc", Static)
        if btn and hasattr(btn, "description"):
            desc.update(btn.description)
        else:
            desc.update("")

    def on_mouse_enter(self, event):
        self._update_desc(event.control)

    def on_mouse_leave(self, event):
        self._update_desc(event.control)

    def on_focus(self, event):
        self._update_desc(event.control)

    def on_blur(self, event):
        self._update_desc(event.control)

    def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id.startswith("rod-"):
            rod_id = button_id.replace("rod-", "")
            ok, msg = self.state.buy_rod(rod_id)
        elif button_id.startswith("bait-"):
            bait_id = button_id.replace("bait-", "")
            ok, msg = self.state.buy_bait(bait_id)
        else:
            return

        language = lang(self.state)
        self.query_one("#gold", Static).update(t(language, "gold_owned", gold=self.state.player.gold))
        self.query_one("#help", PlainStatic).update(msg)
        if ok:
            save_state(self.state)
            self._update_shop_buttons()

    def _update_shop_buttons(self):
        language = lang(self.state)
        for rod in ROD_DATA:
            owned = rod.id == self.state.player.rod_id
            status = t(language, "owned") if owned else f"{rod.price} {t(language, 'gold')}"
            btn = self.query_one(f"#rod-{rod.id}", Button)
            btn.label = Text(f"{rod_name(language, rod)} - {status}")
            btn.disabled = owned
        for bait in BAIT_DATA:
            owned = bait.id == self.state.player.bait_id
            status = t(language, "equipped") if owned else f"{bait.price} {t(language, 'gold')}"
            btn = self.query_one(f"#bait-{bait.id}", Button)
            btn.label = Text(f"{bait_name(language, bait)} - {status}")
            btn.disabled = owned

    def action_back(self):
        self.app.pop_screen()

    def on_mount(self):
        buttons = list(self.query(Button))
        for btn in buttons:
            if not btn.disabled:
                btn.focus()
                break

    def _enabled_buttons(self):
        return [btn for btn in self.query(Button) if not btn.disabled]

    def on_key(self, event):
        if event.key not in ("up", "down"):
            return
        buttons = self._enabled_buttons()
        if not buttons:
            return
        current = self.app.focused
        try:
            idx = buttons.index(current)
        except ValueError:
            idx = 0
        if event.key == "down":
            idx = (idx + 1) % len(buttons)
        elif event.key == "up":
            idx = (idx - 1) % len(buttons)
        buttons[idx].focus()
        event.stop()


class StatsScreen(Screen):
    BINDINGS = [
        ("escape", "back", "Back"),
        ("q", "back", "Back"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        language = lang(self.state)
        with Vertical(classes="stats"):
            yield PlainStatic(t(language, "stats"), classes="title")
            s = self.state.stats
            p = self.state.player
            active_title = title_label(language, p.title) if p.title else t(language, "none")
            text = (
                f"{t(language, 'title')}: {active_title}\n"
                f"{t(language, 'level')}: {p.level}\n"
                f"{t(language, 'exp')}: {p.exp} / {self.state.exp_to_next()}\n"
                f"{t(language, 'gold_owned', gold=p.gold)}\n"
                f"{t(language, 'total_casts')}: {s.total_casts}\n"
                f"{t(language, 'total_caught')}: {s.total_caught}\n"
                f"{t(language, 'total_weight')}: {s.total_weight:.2f}kg\n"
                f"{t(language, 'total_gold')}: {s.total_gold_earned}\n"
                f"{t(language, 'night_catches')}: {s.night_catches}\n"
                f"{t(language, 'epic_legendary', epic=s.epic_catches, legendary=s.legendary_catches)}\n"
                f"{t(language, 'started_at')}: {self.state.started_at}\n"
            )
            yield PlainStatic(text, id="stats-text")
            yield PlainStatic("")
            yield PlainStatic(t(language, "back_help"), id="help")
        yield Footer()

    def action_back(self):
        self.app.pop_screen()


class AchievementsScreen(Screen):
    BINDINGS = [
        ("escape", "back", "Back"),
        ("q", "back", "Back"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self._title_buttons: dict[str, str] = {}

    def compose(self) -> ComposeResult:
        language = lang(self.state)
        with Vertical(classes="achievements"):
            yield PlainStatic(t(language, "achievements"), classes="title")
            active = title_label(language, self.state.player.title) if self.state.player.title else t(language, "none")
            yield PlainStatic(f"{t(language, 'active_title')}: {active}", id="active-title")
            yield PlainStatic("")
            yield PlainStatic(t(language, "achievement_list"), classes="section")
            for ach in ACHIEVEMENT_DATA.values():
                unlocked = ach.id in self.state.achievements
                mark = Text("✓", style="green") if unlocked else Text("-", style="dim")
                translated_title = achievement_title(language, ach)
                title_part = f" / {t(language, 'title')}: {translated_title}" if translated_title else ""
                line = Text.assemble(
                    mark,
                    f" {achievement_name(language, ach)} - {achievement_description(language, ach)} "
                    f"({t(language, 'reward')}: {ach.reward_gold}G, {ach.reward_exp}XP){title_part}",
                )
                if not unlocked:
                    line.stylize("dim")
                yield PlainStatic(line)
            yield PlainStatic("")
            yield PlainStatic(t(language, "titles"), classes="section")
            unlocked_titles = [
                ach.title for ach in ACHIEVEMENT_DATA.values()
                if ach.title and ach.id in self.state.achievements
            ]
            if unlocked_titles:
                for idx, title in enumerate(unlocked_titles):
                    variant = "success" if title == self.state.player.title else "primary"
                    btn = Button(Text(title_label(language, title)), id=f"title-{idx}", variant=variant)
                    self._title_buttons[f"title-{idx}"] = title
                    yield btn
            else:
                yield PlainStatic(t(language, "no_titles"))
            yield PlainStatic("")
            yield PlainStatic(t(language, "back_help"), id="help")
        yield Footer()

    def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id and button_id.startswith("title-"):
            title = self._title_buttons.get(button_id)
            if title:
                self.state.player.title = title
                save_state(self.state)
                language = lang(self.state)
                self.query_one("#active-title", PlainStatic).update(
                    f"{t(language, 'active_title')}: {title_label(language, title)}"
                )
                for bid, t in self._title_buttons.items():
                    btn = self.query_one(f"#{bid}", Button)
                    btn.variant = "success" if t == title else "primary"

    def action_back(self):
        self.app.pop_screen()


class AquariumWidget(Static):
    frame = reactive(0)

    def __init__(self, state: GameState, **kwargs):
        super().__init__("", **kwargs)
        self.state = state
        self.tank_width = 62
        self.tank_height = 16
        self.max_fish = 8
        self.fish = self._populate()
        self._timer = None

    def _populate(self):
        fish_ids = list(self.state.collection.keys())
        if not fish_ids:
            return []
        random.shuffle(fish_ids)
        selected = fish_ids[: self.max_fish]
        result = []
        lanes = list(range(2, self.tank_height - 2))
        random.shuffle(lanes)
        for i, fid in enumerate(selected):
            if i >= len(lanes):
                break
            fish = FISH_BY_ID[fid]
            sprite = fish_sprite(fid, self.state.sprite_style)
            sprite_h = len(str(sprite).split("\n"))
            max_y = self.tank_height - 1 - sprite_h
            y = min(lanes[i], max_y)
            result.append(
                {
                    "fish": fish,
                    "x": random.randint(3, self.tank_width - 12),
                    "y": y,
                    "dir": random.choice([-1, 1]),
                    "speed": random.choice([1, 1, 2]),
                }
            )
        return result

    def on_mount(self):
        self._timer = self.set_interval(0.35, self._tick)

    def on_unmount(self):
        if self._timer:
            self._timer.stop()
            self._timer = None

    def _tick(self):
        self.frame += 1
        for f in self.fish:
            f["x"] += f["dir"] * f["speed"]
            fish_width = self._fish_width(f)
            if f["x"] <= 1:
                f["x"] = 1
                f["dir"] = 1
            elif f["x"] >= self.tank_width - fish_width - 1:
                f["x"] = self.tank_width - fish_width - 1
                f["dir"] = -1

    def _fish_width(self, f):
        sprite_lines = self._fish_sprite_lines(f)
        if not sprite_lines:
            return len(f["fish"].name) + 2
        return max(len(str(line)) for line in sprite_lines)

    def _fish_sprite_lines(self, f):
        """선택된 스프라이트 스타일로 물고기 스프라이트를 줄 단위로 반환."""
        fish = f["fish"]
        style = self.state.sprite_style
        sprite = fish_sprite(fish.id, style)
        lines = str(sprite).split("\n")
        return lines if lines else [fish.name]

    def render(self):
        if not self.fish:
            return Text(t(lang(self.state), "empty_aquarium"), style="dim")

        lines = []
        width = self.tank_width
        height = self.tank_height

        for y in range(height):
            if y == 0:
                line = Text("┌" + "─" * (width - 2) + "┐", style="cyan")
            elif y == height - 1:
                line = Text("└" + "─" * (width - 2) + "┘", style="cyan")
            else:
                # Collect sprite fragments for this row
                fish_on_row = []
                for f in self.fish:
                    sprite_lines = self._fish_sprite_lines(f)
                    fy = int(f["y"])
                    sprite_h = len(sprite_lines)
                    # Does this fish occupy the current row?
                    row_in_sprite = y - fy
                    if 0 <= row_in_sprite < sprite_h:
                        fish_on_row.append((f["x"], row_in_sprite, sprite_lines[row_in_sprite], f))
                fish_on_row.sort(key=lambda item: item[0])
                line_chars = [(" ", None)] * (width - 2)
                for fx, row_in_sprite, sprite_line, f in fish_on_row:
                    color = RARITY_COLORS.get(f["fish"].rarity, "white")
                    offset = fx - 1
                    for i, ch in enumerate(sprite_line):
                        pos = offset + i
                        if 0 <= pos < len(line_chars) and ch != " ":
                            line_chars[pos] = (ch, color)

                line = Text("│", style="cyan")
                for ch, style in line_chars:
                    line.append_text(Text(ch, style=style or ""))
                line.append_text(Text("│", style="cyan"))
            lines.append(line)

        return Text("\n").join(lines)


class AquariumScreen(Screen):
    BINDINGS = [
        ("escape", "back", "Back"),
        ("q", "back", "Back"),
        ("r", "refresh", "Refresh"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        language = lang(self.state)
        with Vertical(classes="aquarium"):
            yield PlainStatic(t(language, "aquarium_title"), classes="title")
            yield PlainStatic(t(language, "aquarium_subtitle"), classes="subtitle")
            yield PlainStatic("")
            yield AquariumWidget(self.state, id="tank")
            yield PlainStatic("")
            yield PlainStatic(t(language, "aquarium_help"), id="help")
        yield Footer()

    def action_refresh(self):
        widget = self.query_one("#tank", AquariumWidget)
        widget.fish = widget._populate()
        widget.refresh()

    def action_back(self):
        self.app.pop_screen()


class SettingsScreen(Screen):
    """설정 화면 - 물고기 스프라이트 스타일 선택 + 미리보기."""

    BINDINGS = [
        ("escape", "back", "Back"),
        ("q", "back", "Back"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self._sample_fish_id = "carp"
        from .data import FISH_BY_ID
        if self._sample_fish_id not in FISH_BY_ID:
            self._sample_fish_id = next(iter(FISH_BY_ID))

    def compose(self) -> ComposeResult:
        language = lang(self.state)
        with Vertical(classes="settings"):
            yield PlainStatic(t(language, "settings"), classes="title")
            yield PlainStatic("")
            yield PlainStatic(t(language, "language"), classes="section")
            yield PlainStatic(t(language, "language_desc"))
            yield PlainStatic("")
            for code in ("en", "ko"):
                label = LANGUAGE_NAMES[code]
                variant = "success" if code == language else "default"
                if code == language:
                    label = f"{label}  ✓ ({t(language, 'current')})"
                yield Button(Text(label), id=f"language-{code}", variant=variant)
            yield PlainStatic("")
            yield PlainStatic(t(language, "sprite_style"), classes="section")
            yield PlainStatic(t(language, "sprite_style_desc"))
            yield PlainStatic("")
            current = self.state.sprite_style
            for s in VALID_STYLES:
                label = f"{s}"
                if s == current:
                    variant = "success"
                    label = f"{s}  ✓ ({t(language, 'current')})"
                else:
                    variant = "default"
                btn = Button(Text(label), id=f"style-{s}", variant=variant)
                yield btn
            yield PlainStatic("")
            yield PlainStatic(t(language, "preview"), classes="section")
            yield PlainStatic(self._preview(self.state.sprite_style), id="preview")
            yield PlainStatic("")
            yield PlainStatic(t(language, "back_help"), id="help")
        yield Footer()

    def _preview(self, style: str) -> Text:
        return fish_sprite(self._sample_fish_id, style)

    def on_button_pressed(self, event):
        button_id = event.button.id or ""
        if button_id.startswith("style-"):
            style = button_id.replace("style-", "")
            if style in VALID_STYLES:
                self.state.sprite_style = style
                save_state(self.state)
                self._refresh_buttons()
                self.query_one("#preview", PlainStatic).update(self._preview(style))
        elif button_id.startswith("language-"):
            language = button_id.replace("language-", "")
            if language in LANGUAGE_NAMES:
                self.state.language = language
                save_state(self.state)
                self.refresh(recompose=True)

    def _refresh_buttons(self):
        language = lang(self.state)
        current = self.state.sprite_style
        for s in VALID_STYLES:
            btn = self.query_one(f"#style-{s}", Button)
            if s == current:
                btn.variant = "success"
                btn.label = Text(f"{s}  ✓ ({t(language, 'current')})")
            else:
                btn.variant = "default"
                btn.label = Text(f"{s}")

    def on_mount(self):
        buttons = list(self.query(Button))
        if buttons:
            buttons[0].focus()

    def _style_buttons(self):
        return list(self.query(Button))

    def on_key(self, event):
        if event.key not in ("up", "down"):
            return
        buttons = self._style_buttons()
        if not buttons:
            return
        current = self.app.focused
        try:
            idx = buttons.index(current)
        except ValueError:
            idx = 0
        if event.key == "down":
            idx = (idx + 1) % len(buttons)
        elif event.key == "up":
            idx = (idx - 1) % len(buttons)
        buttons[idx].focus()
        event.stop()

    def action_back(self):
        self.app.pop_screen()
        # 언어/스타일 변경이 부모 화면에 즉시 반영되도록 recompose
        self.app.screen.refresh(recompose=True)


class SpotSelectScreen(Screen):
    BINDINGS = [
        ("escape", "back", "Back"),
        ("q", "back", "Back"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        language = lang(self.state)
        with Vertical(classes="spots"):
            yield PlainStatic(t(language, "spot_select"), classes="title")
            yield PlainStatic(t(language, "spot_select_desc"))
            yield PlainStatic("")
            for spot in SPOT_DATA:
                unlocked = spot.id in self.state.player.unlocked_spots
                locked_text = t(language, "available") if unlocked else t(language, "unlock_level", level=spot.level_required)
                btn = Button(
                    Text(f"{spot_name(language, spot)} - {locked_text}"),
                    id=f"spot-{spot.id}",
                    disabled=not unlocked,
                )
                btn.description = spot_description(language, spot)
                yield btn
            yield PlainStatic("")
            yield PlainStatic("", id="desc")
            yield PlainStatic(t(language, "back_help"), id="help")
        yield Footer()

    def _find_button(self, widget):
        while widget and not isinstance(widget, Button):
            widget = widget.parent
        return widget

    def _update_desc(self, widget):
        btn = self._find_button(widget)
        desc = self.query_one("#desc", Static)
        if btn and hasattr(btn, "description"):
            desc.update(btn.description)
        else:
            desc.update("")

    def on_mouse_enter(self, event):
        self._update_desc(event.control)

    def on_mouse_leave(self, event):
        self._update_desc(event.control)

    def on_focus(self, event):
        self._update_desc(event.control)

    def on_blur(self, event):
        self._update_desc(event.control)

    def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id.startswith("spot-"):
            spot_id = button_id.replace("spot-", "")
            self.app.push_screen(FishingScreen(self.app.game_state, spot_id))

    def on_mount(self):
        buttons = list(self.query(Button))
        for btn in buttons:
            if not btn.disabled:
                btn.focus()
                break

    def _enabled_buttons(self):
        return [btn for btn in self.query(Button) if not btn.disabled]

    def on_key(self, event):
        if event.key not in ("up", "down"):
            return
        buttons = self._enabled_buttons()
        if not buttons:
            return
        current = self.app.focused
        try:
            idx = buttons.index(current)
        except ValueError:
            idx = 0
        if event.key == "down":
            idx = (idx + 1) % len(buttons)
        elif event.key == "up":
            idx = (idx - 1) % len(buttons)
        buttons[idx].focus()
        event.stop()

    def action_back(self):
        self.app.pop_screen()
