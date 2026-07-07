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
from .particles import ParticleEmitter, ParticleOverlay
from .pixel_art import fish_sprite


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


class AngleWidget(Static):
    angle = reactive(45)

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
        return f"{lines_joined}\n\n각도: {self.angle}°"


class ReelWidget(Static):
    position = reactive(0.0)
    target_range = reactive(0.2)

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
            "Space로 ",
            Text("O", style="bold white"),
            "를 ",
            Text("초록색 구간", style="green"),
            "에 맞출 때 멈춰라\n[",
            bar_text,
            "]",
        )


class MainMenuScreen(Screen):
    BINDINGS = [
        ("1", "fish", "낚시"),
        ("2", "collection", "도감"),
        ("3", "shop", "상점"),
        ("4", "achievements", "업적"),
        ("5", "stats", "통계"),
        ("6", "aquarium", "어항"),
        ("q", "quit", "종료"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(classes="menu"):
            yield PlainStatic(MULGOGI_ASCII, classes="title")
            yield PlainStatic(gradient_text("Fish in your shell", ["#33d9b2", "#f1fa8c"]), classes="subtitle")
            yield PlainStatic("")
            yield Button("1. 낚시하기", id="fish")
            yield Button("2. 도감", id="collection")
            yield Button("3. 상점", id="shop")
            yield Button("4. 업적", id="achievements")
            yield Button("5. 통계", id="stats")
            yield Button("6. 어항", id="aquarium")
            yield Button("q. 종료", id="quit", variant="error")
            yield PlainStatic("")
            yield PlainStatic("방향키 또는 숫자/엔터/클릭으로 선택  |  q: 종료", classes="help")
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

    def action_quit(self):
        self.app.exit()


class FishingScreen(Screen):
    BINDINGS = [
        ("escape", "back", "뒤로"),
        ("q", "back", "뒤로"),
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
        with Vertical(id="fishing-main"):
            yield PlainStatic(self._status_text(), id="status")
            yield PlainStatic(self._spot_text(), id="spot-info")
            yield AngleWidget(id="angle")
            yield SplashWidget(id="splash")
            yield ReelWidget(id="reel")
            yield PlainStatic("", id="result")
            yield Static("← →: 각도  |  Space: 캐스트/입질/릴  |  Esc: 뒤로", id="help")
            yield ParticleOverlay(id="particles")
        yield Footer()

    def on_mount(self):
        self.query_one("#splash", SplashWidget).display = False
        self.query_one("#reel", ReelWidget).display = False

    def _status_text(self) -> str:
        p = self.state.player
        rod = self.state.current_rod()
        bait = self.state.current_bait()
        title_tag = f"({p.title}) " if p.title else ""
        return f"{title_tag}Lv.{p.level}  골드:{p.gold}  낚싯대:{rod.name}  미끼:{bait.name if bait else '-'}"

    def _spot_text(self) -> str:
        spot = SPOT_BY_ID[self.spot_id]
        return f"낚시터: {spot.name} | 시간: {self.time_of_day} | 날씨: {self.weather}"

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
        self.query_one("#help", Static).update("물고기가 물기를 기다리는 중...")
        self.query_one("#angle", AngleWidget).display = False
        self.query_one("#splash", SplashWidget).display = True
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
        self.query_one("#help", Static).update("Space: 계속  |  Esc: 뒤로")

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
            Text("게가 미끼를 훔쳐갔다! 대신 기본 지렁이를 달았다.", style="yellow")
        )

    def _event_seagull_steal(self):
        fish = self._pick_fish()
        result_text = Text.assemble(
            ("물고기를 방금 잡았는데 갈매기가 낚아채갔다!", "red"),
            "\n\n",
            fish_sprite(fish.id),
            "\n\n",
            f"도망간 물고기: {fish.name} (희귀도: {RARITY_NAMES[fish.rarity]} {RARITY_STARS[fish.rarity]})",
        )
        self.query_one("#result", PlainStatic).update(result_text)

    def _event_worm_revolt(self):
        leveled_up = self.state.add_exp(3)
        self.query_one("#status", Static).update(self._status_text())
        result_text = Text.assemble(
            ("지렁이가 통에서 반란을 일으켜 도망쳤다!", "magenta"),
            "\n",
            "대신 물고기 냄새를 맡고 주변에 물고기들이 몰려든다.",
            ("\n경험치 +3", "green"),
            (" ★ 레벨업!", "bold yellow") if leveled_up else ("", ""),
        )
        self.query_one("#result", PlainStatic).update(result_text)

    def _event_fish_tease(self):
        self.query_one("#result", PlainStatic).update(
            Text("물고기가 미끼만 뜯어먹고 도망갔다! 농락당했다...", style="red")
        )

    def _event_rubber_duck(self):
        duck_sprite = (
            "    _      _      _\n"
            "  >(.)__ <(.)__ =(.)__\n"
            "   (___/  (___/  (___/\n"
        )
        self.query_one("#result", PlainStatic).update(
            Text.assemble(
                ("노란 고무 오리를 낚았다!", "yellow"),
                "\n\n",
                duck_sprite,
                "\n",
                "누가 버린 장난감이다. 다시 던져보자.",
            )
        )

    def trigger_bite(self):
        if self.phase != "waiting":
            return
        self.phase = "biting"
        self.query_one("#help", Static).update("[bold][red]!! 입질 !!  Space를 눌러 릴을 걸어라![/red][/bold]")
        self.bite_timer = self.set_timer(1.5, self.miss_bite)

    def miss_bite(self):
        if self.phase != "biting":
            return
        self.phase = "result"
        self.query_one("#splash", SplashWidget).stop()
        self.query_one("#splash", SplashWidget).display = False
        self.query_one("#help", Static).update("Space를 눌러 계속")
        self.query_one("#result", PlainStatic).update(Text("입질을 놓쳤다... 미끼만 날아갔다.", style="red"))
        save_state(self.state)

    def start_reel(self):
        self._stop_all_timers()
        self.phase = "reeling"
        rod = self.state.current_rod()
        success_range = 0.2 + rod.reel_bonus
        self.query_one("#help", Static).update(
            "[bold][cyan]챔질! Space로 O를 초록색 구간에 멈춰라.[/cyan][/bold]"
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
            names = ", ".join(a.name for a in new_achievements)
            titles = [a.title for a in new_achievements if a.title]
            title_text = f"\n칭호: {', '.join(titles)}" if titles else ""
        else:
            names = ""
            title_text = ""

        self.query_one("#status", Static).update(self._status_text())
        self.query_one("#help", Static).update("Space: 계속  |  Esc: 뒤로")
        result_text = Text.assemble(
            (f"{fish.name}을(를) 잡았다!", "green"),
            (" ★ 레벨업!", "bold yellow") if leveled_up else ("", ""),
            (f"\n★ 업적 달성: {names}{title_text}", "bold magenta") if new_achievements else ("", ""),
            "\n\n",
            fish_sprite(fish.id),
            "\n\n",
            f"무게: {weight}kg  |  희귀도: {RARITY_NAMES[fish.rarity]} {RARITY_STARS[fish.rarity]}\n",
            f"골드 +{gold}  경험치 +{exp}\n",
        )
        self.query_one("#result", PlainStatic).update(result_text)
        self.query_one("#particles", ParticleOverlay).burst()

    def lose_fish(self):
        self.phase = "result"
        self.query_one("#help", Static).update("Space: 계속  |  Esc: 뒤로")
        self.query_one("#result", PlainStatic).update(Text("물고기가 도망갔다... 다시 도전해보자.", style="red"))
        save_state(self.state)

    def reset(self):
        self.phase = "menu"
        self.query_one("#angle", AngleWidget).display = True
        self.query_one("#splash", SplashWidget).display = False
        self.query_one("#reel", ReelWidget).display = False
        self.query_one("#particles", ParticleOverlay).clear()
        self.query_one("#help", Static).update("← →: 각도 조절  |  Space: 캐스트/입질/릴  |  Esc: 뒤로")
        self.query_one("#result", PlainStatic).update("")

    def action_back(self):
        self._stop_all_timers()
        self.query_one("#splash", SplashWidget).stop()
        save_state(self.state)
        self.app.pop_screen()


class CollectionScreen(Screen):
    BINDINGS = [
        ("escape", "back", "뒤로"),
        ("q", "back", "뒤로"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        with Vertical(classes="collection"):
            yield PlainStatic("도감", classes="title")
            yield PlainStatic(f"총 {len(FISH_DATA)}종 중 {len(self.state.collection)}종 잡음", id="count")
            yield PlainStatic("")
            fish_lines = []
            for fish in FISH_DATA:
                rec = self.state.collection.get(fish.id)
                if rec:
                    line = Text.assemble(
                        ("✓", "green"),
                        f" {fish.name}  {RARITY_STARS[fish.rarity]}  최대 {rec.max_weight}kg  x{rec.count}",
                    )
                else:
                    line = Text.assemble(
                        ("? ? ?", "dim"),
                        f"  {RARITY_STARS[fish.rarity]}  ???",
                    )
                fish_lines.append(line)
            yield PlainStatic(Text("\n").join(fish_lines), id="fish-list")
            yield PlainStatic("")
            yield PlainStatic("Esc 또는 q: 뒤로", id="help")
        yield Footer()

    def action_back(self):
        self.app.pop_screen()


class ShopScreen(Screen):
    BINDINGS = [
        ("escape", "back", "뒤로"),
        ("q", "back", "뒤로"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        with Vertical(classes="shop"):
            yield PlainStatic("상점", classes="title")
            yield PlainStatic(f"보유 골드: {self.state.player.gold}", id="gold")
            yield PlainStatic("")
            yield PlainStatic("낚싯대", classes="section")
            for rod in ROD_DATA:
                owned = rod.id == self.state.player.rod_id
                status = "(소유 중)" if owned else f"{rod.price} 골드"
                btn = Button(Text(f"{rod.name} - {status}"), id=f"rod-{rod.id}", disabled=owned)
                btn.description = rod.description
                yield btn
            yield PlainStatic("")
            yield PlainStatic("미끼", classes="section")
            for bait in BAIT_DATA:
                owned = bait.id == self.state.player.bait_id
                status = "(장비 중)" if owned else f"{bait.price} 골드"
                btn = Button(Text(f"{bait.name} - {status}"), id=f"bait-{bait.id}", disabled=owned)
                btn.description = bait.description
                yield btn
            yield PlainStatic("")
            yield PlainStatic("", id="desc")
            yield PlainStatic("Esc 또는 q: 뒤로", id="help")
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

        self.query_one("#gold", Static).update(f"보유 골드: {self.state.player.gold}")
        self.query_one("#help", PlainStatic).update(msg)
        if ok:
            save_state(self.state)
            self._update_shop_buttons()

    def _update_shop_buttons(self):
        for rod in ROD_DATA:
            owned = rod.id == self.state.player.rod_id
            status = "(소유 중)" if owned else f"{rod.price} 골드"
            btn = self.query_one(f"#rod-{rod.id}", Button)
            btn.label = Text(f"{rod.name} - {status}")
            btn.disabled = owned
        for bait in BAIT_DATA:
            owned = bait.id == self.state.player.bait_id
            status = "(장비 중)" if owned else f"{bait.price} 골드"
            btn = self.query_one(f"#bait-{bait.id}", Button)
            btn.label = Text(f"{bait.name} - {status}")
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
        ("escape", "back", "뒤로"),
        ("q", "back", "뒤로"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        with Vertical(classes="stats"):
            yield PlainStatic("통계", classes="title")
            s = self.state.stats
            p = self.state.player
            active_title = p.title or "없음"
            text = (
                f"칭호: {active_title}\n"
                f"레벨: {p.level}\n"
                f"경험치: {p.exp} / {self.state.exp_to_next()}\n"
                f"보유 골드: {p.gold}\n"
                f"총 캐스트 횟수: {s.total_casts}\n"
                f"총 잡은 마리수: {s.total_caught}\n"
                f"총 잡은 무게: {s.total_weight:.2f}kg\n"
                f"총 번 골드: {s.total_gold_earned}\n"
                f"밤 낚시 횟수: {s.night_catches}\n"
                f"Epic 잡은 횟수: {s.epic_catches}  Legendary 잡은 횟수: {s.legendary_catches}\n"
                f"시작일: {self.state.started_at}\n"
            )
            yield PlainStatic(text, id="stats-text")
            yield PlainStatic("")
            yield PlainStatic("Esc 또는 q: 뒤로", id="help")
        yield Footer()

    def action_back(self):
        self.app.pop_screen()


class AchievementsScreen(Screen):
    BINDINGS = [
        ("escape", "back", "뒤로"),
        ("q", "back", "뒤로"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self._title_buttons: dict[str, str] = {}

    def compose(self) -> ComposeResult:
        with Vertical(classes="achievements"):
            yield PlainStatic("업적", classes="title")
            active = self.state.player.title or "없음"
            yield PlainStatic(f"장착 칭호: {active}", id="active-title")
            yield PlainStatic("")
            yield PlainStatic("업적 목록", classes="section")
            for ach in ACHIEVEMENT_DATA.values():
                unlocked = ach.id in self.state.achievements
                mark = Text("✓", style="green") if unlocked else Text("-", style="dim")
                title_part = f" / 칭호: {ach.title}" if ach.title else ""
                line = Text.assemble(
                    mark,
                    f" {ach.name} - {ach.description} (보상: {ach.reward_gold}G, {ach.reward_exp}XP){title_part}",
                )
                if not unlocked:
                    line.stylize("dim")
                yield PlainStatic(line)
            yield PlainStatic("")
            yield PlainStatic("칭호", classes="section")
            unlocked_titles = [
                ach.title for ach in ACHIEVEMENT_DATA.values()
                if ach.title and ach.id in self.state.achievements
            ]
            if unlocked_titles:
                for idx, title in enumerate(unlocked_titles):
                    variant = "success" if title == self.state.player.title else "primary"
                    btn = Button(Text(title), id=f"title-{idx}", variant=variant)
                    self._title_buttons[f"title-{idx}"] = title
                    yield btn
            else:
                yield PlainStatic("아직 해금된 칭호가 없습니다.")
            yield PlainStatic("")
            yield PlainStatic("Esc 또는 q: 뒤로", id="help")
        yield Footer()

    def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id and button_id.startswith("title-"):
            title = self._title_buttons.get(button_id)
            if title:
                self.state.player.title = title
                save_state(self.state)
                self.query_one("#active-title", PlainStatic).update(f"장착 칭호: {title}")
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
            result.append(
                {
                    "fish": fish,
                    "x": random.randint(3, self.tank_width - 12),
                    "y": lanes[i],
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
        return len(f["fish"].name) + 2

    def _fish_chars(self, f):
        fish = f["fish"]
        head = ">" if f["dir"] > 0 else "<"
        tail = "<" if f["dir"] > 0 else ">"
        color = RARITY_COLORS.get(fish.rarity, "white")
        chars = []
        chars.append((tail, color))
        for ch in fish.name:
            chars.append((ch, color))
        chars.append((head, color))
        return chars

    def render(self):
        if not self.fish:
            return Text("아직 이 곳에 머물 영혼이 없다. 낚시터에서 만남을 기다리자.", style="dim")

        lines = []
        width = self.tank_width
        height = self.tank_height

        for y in range(height):
            if y == 0:
                line = Text("┌" + "─" * (width - 2) + "┐", style="cyan")
            elif y == height - 1:
                line = Text("└" + "─" * (width - 2) + "┘", style="cyan")
            else:
                fish_on_row = [f for f in self.fish if int(f["y"]) == y]
                fish_on_row.sort(key=lambda f: f["x"])
                line_chars = [(" ", None)] * (width - 2)
                for f in fish_on_row:
                    fx = int(f["x"])
                    for i, (ch, style) in enumerate(self._fish_chars(f)):
                        pos = fx + i - 1
                        if 0 <= pos < len(line_chars):
                            line_chars[pos] = (ch, style)

                line = Text("│", style="cyan")
                for ch, style in line_chars:
                    line.append_text(Text(ch, style=style or ""))
                line.append_text(Text("│", style="cyan"))
            lines.append(line)

        return Text("\n").join(lines)


class AquariumScreen(Screen):
    BINDINGS = [
        ("escape", "back", "뒤로"),
        ("q", "back", "뒤로"),
        ("r", "refresh", "새로고침"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        with Vertical(classes="aquarium"):
            yield PlainStatic("물고기들의 영혼이 담긴 어항", classes="title")
            yield PlainStatic("도감에 새겨진 기억들이 물속을 뛰어다닌다.", classes="subtitle")
            yield PlainStatic("")
            yield AquariumWidget(self.state, id="tank")
            yield PlainStatic("")
            yield PlainStatic("r: 영혼 새로 불러내기  |  Esc 또는 q: 뒤로", id="help")
        yield Footer()

    def action_refresh(self):
        widget = self.query_one("#tank", AquariumWidget)
        widget.fish = widget._populate()
        widget.refresh()

    def action_back(self):
        self.app.pop_screen()


class SpotSelectScreen(Screen):
    BINDINGS = [
        ("escape", "back", "뒤로"),
        ("q", "back", "뒤로"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        with Vertical(classes="spots"):
            yield PlainStatic("낚시터 선택", classes="title")
            yield PlainStatic("원하는 낚시터를 선택하세요.")
            yield PlainStatic("")
            for spot in SPOT_DATA:
                unlocked = spot.id in self.state.player.unlocked_spots
                locked_text = "가능" if unlocked else f"Lv.{spot.level_required} 해금"
                btn = Button(
                    Text(f"{spot.name} - {locked_text}"),
                    id=f"spot-{spot.id}",
                    disabled=not unlocked,
                )
                btn.description = spot.description
                yield btn
            yield PlainStatic("")
            yield PlainStatic("", id="desc")
            yield PlainStatic("Esc 또는 q: 뒤로", id="help")
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
