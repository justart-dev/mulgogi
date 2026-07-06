"""게임 상태 관리"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

from .data import (
    BAIT_BY_ID,
    FISH_BY_ID,
    ROD_BY_ID,
    ROD_DATA,
    Fish,
    Rod,
    Bait,
)


SAVE_DIR = Path.home() / ".local" / "share" / "mulgogi"
SAVE_FILE = SAVE_DIR / "save.json"


@dataclass
class FishRecord:
    count: int = 0
    max_weight: float = 0.0
    first_caught_at: str = ""


@dataclass
class Player:
    level: int = 1
    exp: int = 0
    gold: int = 100
    rod_id: str = "bamboo"
    bait_id: str = "worm"
    unlocked_spots: List[str] = field(default_factory=lambda: ["pond"])


@dataclass
class Stats:
    total_casts: int = 0
    total_caught: int = 0
    total_weight: float = 0.0
    total_gold_earned: int = 0
    play_time_seconds: int = 0


@dataclass
class GameState:
    player: Player = field(default_factory=Player)
    collection: Dict[str, FishRecord] = field(default_factory=dict)
    achievements: Set[str] = field(default_factory=set)
    stats: Stats = field(default_factory=Stats)
    started_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))

    def current_rod(self) -> Rod:
        return ROD_BY_ID.get(self.player.rod_id, ROD_DATA[0])

    def current_bait(self) -> Bait | None:
        return BAIT_BY_ID.get(self.player.bait_id, None)

    def add_exp(self, amount: int) -> bool:
        """경험치를 추가하고 레벨업 여부를 반환"""
        self.player.exp += amount
        leveled_up = False
        while self.player.exp >= self.exp_to_next():
            self.player.exp -= self.exp_to_next()
            self.player.level += 1
            leveled_up = True
        return leveled_up

    def exp_to_next(self) -> int:
        return self.player.level * 100

    def record_catch(self, fish: Fish, weight: float):
        fish_id = fish.id
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        if fish_id not in self.collection:
            self.collection[fish_id] = FishRecord(first_caught_at=now)
        rec = self.collection[fish_id]
        rec.count += 1
        rec.max_weight = max(rec.max_weight, weight)

        self.stats.total_caught += 1
        self.stats.total_weight += weight

        gold = int(fish.base_gold * weight)
        exp = int(fish.base_exp * weight)

        rod = self.current_rod()
        bait = self.current_bait()
        gold = int(gold * (1 + rod.cast_bonus + (bait.attract_bonus if bait else 0)))

        self.player.gold += gold
        self.stats.total_gold_earned += gold
        leveled_up = self.add_exp(exp)

        self._check_achievements()
        return gold, exp, leveled_up

    def _check_achievements(self):
        if self.stats.total_caught >= 1:
            self.achievements.add("first_fish")
        if self.stats.total_caught >= 10:
            self.achievements.add("ten_fish")
        if self.stats.total_caught >= 100:
            self.achievements.add("hundred_fish")
        if self.stats.total_weight >= 10:
            self.achievements.add("heavy_haul")
        if self.stats.total_weight >= 100:
            self.achievements.add("ton_of_fish")
        if self.player.gold >= 1000:
            self.achievements.add("rich")
        if len(self.collection) >= 5:
            self.achievements.add("collector")
        if len(self.collection) >= len(FISH_BY_ID):
            self.achievements.add("master_collector")
        if "whale" in self.collection:
            self.achievements.add("whale_hunter")

    def unlock_spots(self):
        for spot_id in ["river", "lake", "sea"]:
            if spot_id not in self.player.unlocked_spots:
                from .data import SPOT_BY_ID
                spot = SPOT_BY_ID[spot_id]
                if self.player.level >= spot.level_required:
                    self.player.unlocked_spots.append(spot_id)

    def buy_rod(self, rod_id: str) -> tuple[bool, str]:
        if rod_id == self.player.rod_id:
            return False, "이미 소유한 낚싯대입니다."
        rod = ROD_BY_ID.get(rod_id)
        if not rod:
            return False, "존재하지 않는 낚싯대입니다."
        if self.player.gold < rod.price:
            return False, f"골드가 부족합니다. (필요: {rod.price})"
        self.player.gold -= rod.price
        self.player.rod_id = rod_id
        return True, f"{rod.name}을(를) 구매했습니다."

    def buy_bait(self, bait_id: str) -> tuple[bool, str]:
        bait = BAIT_BY_ID.get(bait_id)
        if not bait:
            return False, "존재하지 않는 미끼입니다."
        if self.player.gold < bait.price:
            return False, f"골드가 부족합니다. (필요: {bait.price})"
        self.player.gold -= bait.price
        self.player.bait_id = bait_id
        return True, f"{bait.name}를 구매했습니다."

    def to_dict(self) -> dict:
        return {
            "player": asdict(self.player),
            "collection": {k: asdict(v) for k, v in self.collection.items()},
            "achievements": sorted(list(self.achievements)),
            "stats": asdict(self.stats),
            "started_at": self.started_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        player = Player(**data.get("player", {}))
        collection = {
            k: FishRecord(**v) for k, v in data.get("collection", {}).items()
        }
        achievements = set(data.get("achievements", []))
        stats = Stats(**data.get("stats", {}))
        started_at = data.get("started_at", time.strftime("%Y-%m-%d %H:%M:%S"))
        return cls(player, collection, achievements, stats, started_at)


def load_state() -> GameState:
    if SAVE_FILE.exists():
        try:
            with SAVE_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return GameState.from_dict(data)
        except Exception:
            pass
    return GameState()


def save_state(state: GameState):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    with SAVE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, ensure_ascii=False, indent=2)
