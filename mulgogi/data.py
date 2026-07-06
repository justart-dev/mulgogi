"""게임 데이터 정의"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Fish:
    id: str
    name: str
    ascii: str
    min_weight: float
    max_weight: float
    difficulty: int  # 1-5
    rarity: int  # 1 common, 2 uncommon, 3 rare, 4 epic, 5 legendary
    preferred_time: str  # dawn, day, dusk, night, any
    preferred_weather: str  # sunny, rainy, cloudy, any
    base_gold: int
    base_exp: int


@dataclass(frozen=True)
class Spot:
    id: str
    name: str
    level_required: int
    fish_ids: List[str]
    description: str


@dataclass(frozen=True)
class Rod:
    id: str
    name: str
    price: int
    reel_bonus: float  # 릴 성공 구간 확대
    cast_bonus: float  # 입질 확률 상승
    description: str


@dataclass(frozen=True)
class Bait:
    id: str
    name: str
    price: int
    attract_bonus: float  # 입질 확률 상승
    target_fish_id: Optional[str]  # 특정 어종 출현률 상승
    description: str


FISH_DATA: List[Fish] = [
    Fish("carp", "붕어", "  <\\\\><(_)>\n<))))><", 0.3, 1.5, 1, 1, "any", "any", 10, 5),
    Fish("crucian", "용붕어", "  <\"/\">\n <(o o)>\n  <\"/\">", 0.2, 0.8, 1, 1, "day", "sunny", 8, 4),
    Fish("trout", "송어", "  _  __\n>(___(_)>\n ~~~~~~~", 0.8, 2.5, 2, 2, "dawn", "cloudy", 25, 12),
    Fish("catfish", "메기", "  __\n (  \\\\___\n  \\_____)>", 1.5, 8.0, 3, 2, "night", "rainy", 40, 20),
    Fish("pike", "갑상어", "   /\\\n__/ o\\__\n  \\____/", 2.0, 6.0, 3, 3, "dusk", "any", 60, 30),
    Fish("bass", "뱀스", "   __\n  /  \\\n <` - |>\n  \\___/", 1.0, 4.0, 2, 2, "day", "sunny", 35, 15),
    Fish("eel", "민물장어", "  ~~~\n<~~~~~~~>\n  ~~~", 0.5, 3.0, 3, 3, "night", "rainy", 45, 22),
    Fish("salmon", "연어", "  _  __\n>(@@(_)>\n ~~~~~~~", 3.0, 12.0, 4, 4, "dawn", "cloudy", 120, 60),
    Fish("gold_carp", "황금잉어", "  \\*/\n*<(o o)>*\n  /| |\\\\", 2.0, 5.0, 4, 4, "day", "sunny", 150, 80),
    Fish("whale", "고래", "   __---__\n  /  O O  \\\n |    >    |\n  \\_______/", 50.0, 150.0, 5, 5, "night", "rainy", 2000, 1000),
]

SPOT_DATA: List[Spot] = [
    Spot("pond", "연못", 1, ["carp", "crucian", "trout"], "조용한 연못. 초보자에겐 딱 좋다."),
    Spot("river", "강가", 3, ["carp", "trout", "catfish", "pike"], "흔드는 물에서 낚시를 도전해보자."),
    Spot("lake", "호수", 5, ["bass", "pike", "eel", "salmon"], "넓은 호수에는 큰 물고기가 숨어있다."),
    Spot("sea", "바다", 8, ["bass", "eel", "salmon", "whale"], "끝을 알 수 없는 바다. 강한 납싯대가 필요하다."),
]

ROD_DATA: List[Rod] = [
    Rod("bamboo", "대나무 낚싯대", 0, 0.0, 0.0, "시작으로 주어지는 낚싯대."),
    Rod("carbon", "카보난 낚싯대", 500, 0.05, 0.05, "가벼운 더미 낚싯대."),
    Rod("titanium", "티타니엄 낚싯대", 2000, 0.12, 0.10, "전문가용 낚싯대. 바다의 괴물도 잡을 수 있다."),
]

BAIT_DATA: List[Bait] = [
    Bait("worm", "지렁이", 5, 0.0, None, "기본 미끼. 다 잘 먹는다."),
    Bait("cricket", "귀떠라미", 15, 0.05, None, "뱀스와 메기에 잘 물진다."),
    Bait("shrimp", "새우", 40, 0.08, "salmon", "연어를 끌어모으는 미끼."),
    Bait("golden_bait", "황금 미끼", 200, 0.15, "gold_carp", "희박한 물고기를 끌어모은다."),
]

FISH_BY_ID = {f.id: f for f in FISH_DATA}
SPOT_BY_ID = {s.id: s for s in SPOT_DATA}
ROD_BY_ID = {r.id: r for r in ROD_DATA}
BAIT_BY_ID = {b.id: b for b in BAIT_DATA}

RARITY_NAMES = {1: "Common", 2: "Uncommon", 3: "Rare", 4: "Epic", 5: "Legendary"}
RARITY_STARS = {1: "★", 2: "★★", 3: "★★★", 4: "★★★★", 5: "★★★★★"}
