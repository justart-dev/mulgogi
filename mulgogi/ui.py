"""TUI 화면 구성"""

import random
import time
from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static

from .data import (
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
    Fish,
)
from .game import GameState, save_state


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
    # 게임 속 날씨는 런덤으로 결정 (세션 당 구절마다 초기화)
    return random.choice(["sunny", "cloudy", "rainy"])


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
        for i in range(length):
            px = x + int(round(i * 0.7))
            py = y - int(round(i * 0.7))
            if 0 <= px < 40 and 0 <= py < 8:
                grid[py][px] = "/" if i < length - 1 else "@"
        grid[5][12] = "O"
        lines = ["".join(row) for row in grid]
        lines_joined = "\n".join(lines)
        return f"{lines_joined}\n\n각도: {self.angle}° (장식용)"


class ReelWidget(Static):
    position = reactive(0.0)
    target_range = reactive(0.2)

    def render(self):
        bar_width = 30
        pos = int(self.position * (bar_width - 1))
        pos = max(0, min(bar_width - 1, pos))
        center = bar_width // 2
        half = max(1, int(self.target_range * bar_width / 2))
        bar = []
        for i in range(bar_width):
            if i == pos:
                bar.append("[bold white]O[/]")
            elif center - half <= i <= center + half:
                bar.append("[green]=[/]")
            else:
                bar.append("[dim]-[/]")
        return (
            "Space로 O를 [green]초록색 구간[/]에 맞출 때 멈춰라\n"
            f"[{''.join(bar)}]"
        )


class MainMenuScreen(Screen):
    BINDINGS = [
        ("1", "fish", "낚시"),
        ("2", "collection", "도감"),
        ("3", "shop", "상점"),
        ("4", "stats", "통계"),
        ("q", "quit", "종료"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="menu"):
            yield Static("mulgogi 🎣", classes="title")
            yield Static("터미널에서 즐기는 낚시 게임", classes="subtitle")
            yield Static("")
            yield Button("1. 낚시하기", id="fish", variant="primary")
            yield Button("2. 도감", id="collection")
            yield Button("3. 상점", id="shop")
            yield Button("4. 통계", id="stats")
            yield Button("q. 종료", id="quit", variant="error")
        yield Footer()

    def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id == "fish":
            self.app.push_screen(SpotSelectScreen(self.app.game_state))
        elif button_id == "collection":
            self.app.push_screen(CollectionScreen(self.app.game_state))
        elif button_id == "shop":
            self.app.push_screen(ShopScreen(self.app.game_state))
        elif button_id == "stats":
            self.app.push_screen(StatsScreen(self.app.game_state))
        elif button_id == "quit":
            self.app.exit()

    def action_fish(self):
        self.app.push_screen(SpotSelectScreen(self.app.game_state))

    def action_collection(self):
        self.app.push_screen(CollectionScreen(self.app.game_state))

    def action_shop(self):
        self.app.push_screen(ShopScreen(self.app.game_state))

    def action_stats(self):
        self.app.push_screen(StatsScreen(self.app.game_state))

    def action_quit(self):
        self.app.exit()


class FishingScreen(Screen):
    BINDINGS = [
        ("escape", "back", "뒤로"),
        ("q", "back", "뒤로"),
    ]

    CSS = """
    FishingScreen { align: center middle; }
    #fishing-main { width: 80; height: auto; border: solid green; padding: 1 2; }
    """

    def __init__(self, state: GameState, spot_id: str = "pond", **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.spot_id = spot_id
        self.phase = "menu"  # menu, waiting, biting, reeling, result
        self.angle = 45
        self.bite_timer = None
        self.reel_timer = None
        self.reel_pos = 0.0
        self.reel_dir = 1
        self.reel_speed = 0.06
        self.last_result = None
        self.weather = current_weather()
        self.time_of_day = current_time_of_day()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="fishing-main"):
            yield Static(self._status_text(), id="status")
            yield Static(self._spot_text(), id="spot-info")
            yield AngleWidget(id="angle")
            yield SplashWidget(id="splash")
            yield ReelWidget(id="reel")
            yield Static("", id="result")
            yield Static("← →: 각도  |  Space: 캐스트/입질/릴  |  Esc: 뒤로", id="help")
        yield Footer()

    def on_mount(self):
        self.query_one("#splash", SplashWidget).display = False
        self.query_one("#reel", ReelWidget).display = False

    def _status_text(self) -> str:
        p = self.state.player
        rod = self.state.current_rod()
        bait = self.state.current_bait()
        return f"Lv.{p.level}  골드:{p.gold}  낚싯대:{rod.name}  미끼:{bait.name if bait else '-'}"

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
        self.query_one("#help", Static).update("물고기가 물기를 기다리는 중...  Space: 입질 시도")
        self.query_one("#angle", AngleWidget).display = False
        self.query_one("#splash", SplashWidget).display = True
        self.query_one("#result", Static).update("")
        delay = random.uniform(1.5, 4.0)
        self.bite_timer = self.set_timer(delay, self.trigger_bite)

    def trigger_bite(self):
        if self.phase != "waiting":
            return
        self.phase = "biting"
        self.query_one("#help", Static).update("[bold red]!! 입질 !!  Space를 눌러 릴을 걸어라![/]")
        self.bite_timer = self.set_timer(1.5, self.miss_bite)

    def miss_bite(self):
        if self.phase != "biting":
            return
        self.phase = "result"
        self.query_one("#splash", SplashWidget).stop()
        self.query_one("#splash", SplashWidget).display = False
        self.query_one("#help", Static).update("Space를 눌러 계속")
        self.query_one("#result", Static).update("[red]입질을 놓츰... 미끼만 날아갔다.[/]")
        save_state(self.state)

    def start_reel(self):
        self._stop_all_timers()
        self.phase = "reeling"
        rod = self.state.current_rod()
        success_range = 0.2 + rod.reel_bonus
        self.query_one("#help", Static).update(
            "[bold cyan]챔질! Space로 O를 초록색 구간에 멈춰라.[/]"
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

    def action_back(self):
        self._stop_all_timers()
        self.query_one("#splash", SplashWidget).stop()
        save_state(self.state)
        self.app.pop_screen()

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
        gold, exp, leveled_up = self.state.record_catch(fish, weight)
        self.state.unlock_spots()
        save_state(self.state)

        level_text = " [bold yellow]★ 레벨업![/]" if leveled_up else ""
        self.query_one("#status", Static).update(self._status_text())
        self.query_one("#help", Static).update("Space를 눌러 계속")
        self.query_one("#result", Static).update(
            f"[green]{fish.name}을(를) 잡았다![/]{level_text}\n\n"
            f"{fish.ascii}\n\n"
            f"무게: {weight}kg  |  희귀도: {RARITY_NAMES[fish.rarity]} {RARITY_STARS[fish.rarity]}\\n"
            f"골드 +{gold}  경험치 +{exp}\n"
        )

    def lose_fish(self):
        self.phase = "result"
        self.query_one("#help", Static).update("Space를 눌러 계속")
        self.query_one("#result", Static).update("[red]물고기가 도망갔다... 다시 도전해보자.[/]")
        save_state(self.state)

    def reset(self):
        self.phase = "menu"
        self.query_one("#angle", AngleWidget).display = True
        self.query_one("#splash", SplashWidget).display = False
        self.query_one("#reel", ReelWidget).display = False
        self.query_one("#help", Static).update("← →: 각도  |  Space: 캐스트/입질/릴  |  Esc: 뒤로")
        self.query_one("#result", Static).update("")

    def action_back(self):
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
        yield Header(show_clock=True)
        with Vertical(classes="collection"):
            yield Static("도감 📜", classes="title")
            yield Static(f"총 {len(FISH_DATA)}종 중 {len(self.state.collection)}종 잡음", id="count")
            yield Static("")
            fish_lines = []
            for fish in FISH_DATA:
                rec = self.state.collection.get(fish.id)
                if rec:
                    line = f"[green]✓[/] {fish.name}  {RARITY_STARS[fish.rarity]}  최대 {rec.max_weight}kg  x{rec.count}"
                else:
                    line = f"[dim]? ? ?  {RARITY_STARS[fish.rarity]}  ???[/]"
                fish_lines.append(line)
            yield Static("\n".join(fish_lines), id="fish-list")
            yield Static("")
            yield Static("Esc 또는 q: 뒤로", id="help")
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
        yield Header(show_clock=True)
        with Vertical(classes="shop"):
            yield Static("상점 🛒", classes="title")
            yield Static(f"보유 골드: {self.state.player.gold}", id="gold")
            yield Static("")
            yield Static("[낚싯대]", classes="section")
            for rod in ROD_DATA:
                owned = rod.id == self.state.player.rod_id
                status = "[소유 중]" if owned else f"{rod.price} 골드"
                btn = Button(f"{rod.name} - {status}", id=f"rod-{rod.id}", disabled=owned)
                btn.description = rod.description
                yield btn
            yield Static("")
            yield Static("[미끼]", classes="section")
            for bait in BAIT_DATA:
                owned = bait.id == self.state.player.bait_id
                status = "[장비 중]" if owned else f"{bait.price} 골드"
                btn = Button(f"{bait.name} - {status}", id=f"bait-{bait.id}", disabled=owned)
                btn.description = bait.description
                yield btn
            yield Static("")
            yield Static("", id="desc")
            yield Static("Esc 또는 q: 뒤로", id="help")
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
        self.query_one("#help", Static).update(msg)
        if ok:
            save_state(self.state)
            self._update_shop_buttons()

    def _update_shop_buttons(self):
        for rod in ROD_DATA:
            owned = rod.id == self.state.player.rod_id
            status = "[소유 중]" if owned else f"{rod.price} 골드"
            btn = self.query_one(f"#rod-{rod.id}", Button)
            btn.label = f"{rod.name} - {status}"
            btn.disabled = owned
        for bait in BAIT_DATA:
            owned = bait.id == self.state.player.bait_id
            status = "[장비 중]" if owned else f"{bait.price} 골드"
            btn = self.query_one(f"#bait-{bait.id}", Button)
            btn.label = f"{bait.name} - {status}"
            btn.disabled = owned

    def action_back(self):
        self.app.pop_screen()


class StatsScreen(Screen):
    BINDINGS = [
        ("escape", "back", "뒤로"),
        ("q", "back", "뒤로"),
    ]

    def __init__(self, state: GameState, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="stats"):
            yield Static("통계 📊", classes="title")
            s = self.state.stats
            p = self.state.player
            text = (
                f"레벨: {p.level}\n"
                f"경험치: {p.exp} / {self.state.exp_to_next()}\n"
                f"보유 골드: {p.gold}\n"
                f"총 캐스트 횟수: {s.total_casts}\n"
                f"총 잡은 마리수: {s.total_caught}\n"
                f"총 잡은 무게: {s.total_weight:.2f}kg\n"
                f"총 번 골드: {s.total_gold_earned}\n"
                f"시작일: {self.state.started_at}\n"
            )
            yield Static(text, id="stats-text")
            yield Static("")
            yield Static("[업적]", classes="section")
            if self.state.achievements:
                ach_text = "\n".join(sorted(self.state.achievements))
            else:
                ach_text = "아직 달성한 업적이 없습니다."
            yield Static(ach_text, id="achievements")
            yield Static("")
            yield Static("Esc 또는 q: 뒤로", id="help")
        yield Footer()

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
        yield Header(show_clock=True)
        with Vertical(classes="spots"):
            yield Static("낚시터 선택 🌊", classes="title")
            yield Static("원하는 낚시터를 선택하세요.")
            yield Static("")
            for spot in SPOT_DATA:
                unlocked = spot.id in self.state.player.unlocked_spots
                locked_text = "가능" if unlocked else f"Lv.{spot.level_required} 해금"
                btn = Button(
                    f"{spot.name} - {locked_text}",
                    id=f"spot-{spot.id}",
                    disabled=not unlocked,
                )
                btn.description = spot.description
                yield btn
            yield Static("")
            yield Static("", id="desc")
            yield Static("Esc 또는 q: 뒤로", id="help")
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

    def action_back(self):
        self.app.pop_screen()
