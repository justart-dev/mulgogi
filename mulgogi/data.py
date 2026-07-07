"""게임 데이터 정의"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


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


@dataclass(frozen=True)
class Achievement:
    id: str
    name: str
    description: str
    reward_gold: int
    reward_exp: int
    title: Optional[str] = None


FISH_DATA: List[Fish] = [
    Fish("carp", "붕어", "  <\\\\><(_)>\n<))))><", 0.3, 1.5, 1, 1, "any", "any", 10, 5),
    Fish("crucian", "용붕어", "  <\\\"/\\\">\n <(o o)>\n  <\\\"/\\\">", 0.2, 0.8, 1, 1, "day", "sunny", 8, 4),
    Fish("bluegill", "블루길", "  .-=-.\n /(o o)\\\n  \\ - /\n   `-'", 0.1, 0.5, 1, 1, "day", "sunny", 6, 3),
    Fish("tilapia", "틸라피아", "   __\n  /  \\\n <`  '>\n  \\__/", 0.4, 1.2, 1, 1, "any", "any", 9, 4),
    Fish("trout", "송어", "  _  __\n>(___(_)>\n ~~~~~~~", 0.8, 2.5, 2, 2, "dawn", "cloudy", 25, 12),
    Fish("perch", "농어", "   /\\\n  /  \\\n <_  _>\n   \\/", 0.5, 2.0, 2, 2, "dusk", "any", 22, 10),
    Fish("catfish", "메기", "  __\n (  \\\\___\n  \\_____)>", 1.5, 8.0, 3, 2, "night", "rainy", 40, 20),
    Fish("bass", "배스", "   __\n  /  \\\n <` - |>\n  \\___/", 1.0, 4.0, 2, 2, "day", "sunny", 35, 15),
    Fish("eel", "민물장어", "  ~~~\n<~~~~~~~>\n  ~~~", 0.5, 3.0, 3, 3, "night", "rainy", 45, 22),
    Fish("pike", "갑상어", "   /\\\n__/ o\\__\n  \\____/", 2.0, 6.0, 3, 3, "dusk", "any", 60, 30),
    Fish("sturgeon", "철갑상어", "  ___\n <_(_)>\n  ~~~", 5.0, 20.0, 4, 4, "night", "any", 180, 90),
    Fish("salmon", "연어", "  _  __\n>(@@(_)>\n ~~~~~~~", 3.0, 12.0, 4, 4, "dawn", "cloudy", 120, 60),
    Fish("gold_carp", "황금잉어", "  \\*/\n*<(o o)>*\n  /| |\\\\", 2.0, 5.0, 4, 4, "day", "sunny", 150, 80),
    Fish("mackerel", "고등어", "  .---.\n<( - )>\n  `---'", 0.6, 2.5, 2, 2, "day", "any", 28, 14),
    Fish("tuna", "참치", "   ___\n  /   \\\n |  o  |\n  \\___/", 8.0, 30.0, 4, 4, "day", "any", 250, 120),
    Fish("octopus", "문어", "   .---.\n  / o o \\\n |   <   |\n  \\  -  /\n   `---'", 1.0, 5.0, 3, 3, "night", "rainy", 70, 35),
    Fish("shark", "상어", "      /\\\n     /  \\\n    /    \\\n   /______\\\n  (  o  o  )\n   \\  ==  /\n    \\____/", 20.0, 80.0, 5, 4, "night", "any", 600, 300),
    Fish("marlin", "청새치", "     /|\n    / |\n   /  |\n  /   |\n<(    |\n  \\   |\n   \\__|", 15.0, 60.0, 5, 5, "dawn", "any", 1500, 750),
    Fish("whale", "고래", "   __---__\n  /  O O  \\\n |    >    |\n  \\_______/", 50.0, 150.0, 5, 5, "night", "rainy", 2000, 1000),
    Fish("koi", "비단잉어", "  \\\\*/\n*<(o o)>*\n  /| |\\\\", 1.0, 4.0, 3, 3, "day", "sunny", 80, 40),
    Fish("zander", "샌더어", "   /\\\\\n__/ o\\__\n  \\____/", 2.0, 6.0, 3, 3, "night", "any", 90, 45),
    Fish("piranha", "피라냐", "   /\\\\\n__/ \\//\\__\n  \\____/", 0.5, 1.5, 2, 2, "day", "sunny", 30, 15),
    Fish("red_snapper", "붉은돖", "  .---.\n<( o )>\n  `---'", 1.0, 4.0, 2, 2, "day", "any", 40, 20),
    Fish("swordfish", "황새치", "     /|\n    / |\n   /  |\n  /   |\n<(    |\n  \\   |\n   \\__|", 10.0, 40.0, 4, 4, "dawn", "any", 500, 250),
    Fish("jellyfish", "해파리", "   .---.\n  / o o \\\n |   <   |\n  \\  -  /\n   `---'", 0.5, 2.0, 1, 1, "night", "rainy", 15, 8),
]

SPOT_DATA: List[Spot] = [
    Spot("pond", "연못", 1, ["carp", "crucian", "bluegill", "tilapia", "trout", "koi"], "조용한 연못. 초보자에겐 딱 좋다."),
    Spot("river", "강가", 3, ["carp", "trout", "catfish", "pike", "bluegill", "tilapia", "perch", "sturgeon", "zander", "piranha", "koi"], "흔드는 물에서 낚시를 도전해보자."),
    Spot("lake", "호수", 5, ["bass", "pike", "eel", "salmon", "perch", "sturgeon", "zander"], "넓은 호수에는 큰 물고기가 숨어있다."),
    Spot("sea", "바다", 8, ["bass", "eel", "salmon", "whale", "mackerel", "tuna", "octopus", "shark", "marlin", "perch", "red_snapper", "swordfish", "jellyfish"], "끝을 알 수 없는 바다. 강한 낚싯대가 필요하다."),
]

ROD_DATA: List[Rod] = [
    Rod("bamboo", "대나무 낚싯대", 0, 0.0, 0.0, "시작으로 주어지는 낚싯대."),
    Rod("carbon", "카보난 낚싯대", 500, 0.05, 0.05, "가벼운 더미 낚싯대."),
    Rod("titanium", "티타니엄 낚싯대", 2000, 0.12, 0.10, "전문가용 낚싯대. 바다의 괴물도 잡을 수 있다."),
]

BAIT_DATA: List[Bait] = [
    Bait("worm", "지렁이", 5, 0.0, None, "기본 미끼. 다 잘 먹는다."),
    Bait("cricket", "귀뚜라미", 15, 0.05, None, "배스와 메기에 잘 물진다."),
    Bait("shrimp", "새우", 40, 0.08, "salmon", "연어를 끌어모으는 미끼."),
    Bait("squid_bait", "오징어 미끼", 80, 0.10, "tuna", "바다 대형 어종을 끌어모은다."),
    Bait("golden_bait", "황금 미끼", 200, 0.15, "gold_carp", "희박한 물고기를 끌어모은다."),
]

ACHIEVEMENT_DATA: Dict[str, Achievement] = {
    "first_fish": Achievement("first_fish", "첫 수확", "물고기 한 마리 잡기", 50, 20, "낚시 입문자"),
    "ten_fish": Achievement("ten_fish", "숙련자", "물고기 10마리 잡기", 100, 50, "연못 지배자"),
    "hundred_fish": Achievement("hundred_fish", "낚시광", "물고기 100마리 잡기", 500, 200, "낚시 중독자"),
    "heavy_haul": Achievement("heavy_haul", "무거운 한 마리", "총 낚은 무게 10kg 돌파", 100, 30, "힘센 낚시꾼"),
    "ton_of_fish": Achievement("ton_of_fish", "1톤의 기록", "총 낚은 무게 100kg 돌파", 300, 100, "대물 낚시꾼"),
    "rich": Achievement("rich", "금수저", "보유 골드 1000 돌파", 0, 0, "부자 낚시꾼"),
    "collector": Achievement("collector", "수집가", "5종 이상 잡기", 200, 80, "도감 수집가"),
    "master_collector": Achievement("master_collector", "완벽한 수집가", "모든 어종 잡기", 1000, 500, "물고기 박사"),
    "whale_hunter": Achievement("whale_hunter", "고래 사냥꾼", "고래 잡기", 2000, 1000, "바다의 제왕"),
    "night_owl": Achievement("night_owl", "밤낚시꾼", "밤에 10마리 잡기", 150, 60, "밤의 추적자"),
    "legendary_catch": Achievement("legendary_catch", "전설의 물고기", "Legendary 등급 물고기 잡기", 500, 200, "전설 낚시꾼"),
}

FISH_BY_ID = {f.id: f for f in FISH_DATA}
SPOT_BY_ID = {s.id: s for s in SPOT_DATA}
ROD_BY_ID = {r.id: r for r in ROD_DATA}
BAIT_BY_ID = {b.id: b for b in BAIT_DATA}

RARITY_NAMES = {1: "Common", 2: "Uncommon", 3: "Rare", 4: "Epic", 5: "Legendary"}
RARITY_STARS = {1: "★", 2: "★★", 3: "★★★", 4: "★★★★", 5: "★★★★★"}
RARITY_COLORS = {1: "#95a5a6", 2: "#2ecc71", 3: "#3498db", 4: "#9b59b6", 5: "#f1c40f"}
