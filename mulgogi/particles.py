"""Terminal confetti particle system inspired by confetty_rs."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List

from rich.text import Text

from textual.reactive import reactive
from textual.widgets import Static


CONFETTI_COLORS = [
    "#a864fd",
    "#29cdff",
    "#78ff44",
    "#ff718d",
    "#fdff6a",
]

CONFETTI_CHARS = ["█", "▓", "▒", "░", "▄", "▀"]

GRAVITY = 9.81


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    color: str
    char: str
    life: float = 1.0
    decay: float = field(default=0.0)

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += GRAVITY * dt * 5.0  # scale gravity for terminal cells
        self.life -= self.decay * dt


class ParticleEmitter:
    """Simple 2D confetti emitter."""

    def __init__(self) -> None:
        self.particles: List[Particle] = []

    def clear(self) -> None:
        self.particles.clear()

    def burst(
        self,
        count: int,
        origin_x: float,
        origin_y: float,
        spread: float = 120.0,
        upward: float = 80.0,
    ) -> None:
        for _ in range(count):
            vx = (random.random() - 0.5) * spread
            vy = -random.random() * upward
            color = random.choice(CONFETTI_COLORS)
            char = random.choice(CONFETTI_CHARS)
            p = Particle(
                x=origin_x + (random.random() - 0.5) * 4.0,
                y=origin_y,
                vx=vx,
                vy=vy,
                color=color,
                char=char,
                life=1.0,
                decay=random.uniform(0.3, 0.8),
            )
            self.particles.append(p)

    def update(self, width: int, height: int, dt: float = 0.05) -> None:
        for p in self.particles:
            p.update(dt)

        # remove off-screen or dead particles
        self.particles = [
            p
            for p in self.particles
            if p.life > 0
            and -2 <= int(p.x) <= width + 2
            and -2 <= int(p.y) <= height + 2
        ]

    def render(self, width: int, height: int) -> Text:
        if width <= 0 or height <= 0:
            return Text("")

        grid: List[List[Particle | None]] = [[None for _ in range(width)] for _ in range(height)]
        for p in self.particles:
            col = int(p.x)
            row = int(p.y)
            if 0 <= col < width and 0 <= row < height:
                grid[row][col] = p

        rows: List[Text] = []
        for row in grid:
            line = Text()
            for p in row:
                if p is not None:
                    line.append_text(Text(p.char, style=f"bold {p.color}"))
                else:
                    line.append_text(Text(" "))
            rows.append(line)
        return Text("\n").join(rows) if rows else Text("")


class ParticleOverlay(Static):
    """Full-screen particle overlay. Non-focusable so it does not block input."""

    can_focus = False
    active = reactive(False)

    def __init__(self, **kwargs):
        super().__init__("", **kwargs)
        self.emitter = ParticleEmitter()

    def on_mount(self):
        self._timer = self.set_interval(0.05, self._tick)

    def on_unmount(self):
        if self._timer:
            self._timer.stop()
            self._timer = None

    def _tick(self):
        if not self.active and not self.emitter.particles:
            return
        self.emitter.update(self.size.width, self.size.height, dt=0.05)
        if not self.emitter.particles:
            self.active = False
        self.refresh()

    def render(self):
        return self.emitter.render(self.size.width, self.size.height)

    def burst(self, count: int = 60):
        width = max(1, self.size.width)
        self.emitter.burst(count, width / 2, 0)
        self.active = True
        self.refresh()

    def clear(self):
        self.emitter.clear()
        self.active = False
        self.refresh()
