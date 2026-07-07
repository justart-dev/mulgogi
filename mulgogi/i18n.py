"""Display translations for mulgogi."""

from __future__ import annotations

from typing import Any


DEFAULT_LANGUAGE = "en"
LANGUAGES = ("en", "ko")
LANGUAGE_NAMES = {"en": "English", "ko": "Korean"}


def normalize_language(language: str | None) -> str:
    return language if language in LANGUAGES else DEFAULT_LANGUAGE


UI_TEXT = {
    "en": {
        "back": "Back",
        "quit": "Quit",
        "fish": "Fish",
        "fish_action": "Go fishing",
        "collection": "Collection",
        "shop": "Shop",
        "achievements": "Achievements",
        "stats": "Stats",
        "aquarium": "Aquarium",
        "settings": "Settings",
        "menu_help": "Use arrow keys or numbers/Enter/click to choose  |  q: Quit",
        "angle": "Angle",
        "reel_instruction_start": "Press Space to stop ",
        "reel_instruction_middle": " in the ",
        "reel_instruction_end": "\n[",
        "green_zone": "green zone",
        "fishing_help": "← →: Angle  |  Space: Cast/Bite/Reel  |  Esc: Back",
        "fishing_help_reset": "← →: Adjust angle  |  Space: Cast/Bite/Reel  |  Esc: Back",
        "level_short": "Lv.",
        "gold": "Gold",
        "rod": "Rod",
        "bait": "Bait",
        "spot": "Spot",
        "time": "Time",
        "weather": "Weather",
        "waiting": "Waiting for a fish to bite...",
        "continue_back": "Space: Continue  |  Esc: Back",
        "continue": "Press Space to continue",
        "crab_event": "A crab stole your bait! You put on a basic worm instead.",
        "seagull_event": "You had just caught a fish, but a seagull snatched it!",
        "escaped_fish": "Escaped fish",
        "rarity": "Rarity",
        "worm_event_1": "The worms staged a bucket revolt and escaped!",
        "worm_event_2": "Instead, nearby fish gather after catching the scent.",
        "exp_gain": "EXP +{amount}",
        "level_up": " ★ Level up!",
        "tease_event": "A fish nibbled off the bait and fled! You were played...",
        "duck_event": "You caught a yellow rubber duck!",
        "duck_event_2": "Someone threw away a toy. Cast again.",
        "bite": "!! Bite !! Press Space to set the hook!",
        "missed_bite": "You missed the bite... only the bait is gone.",
        "hook_set": "Hook set! Press Space to stop O in the green zone.",
        "caught": "Caught {fish}!",
        "achievement_unlocked": "\n★ Achievement unlocked: {names}{title_text}",
        "title_result": "\nTitle: {titles}",
        "weight": "Weight",
        "gold_exp_gain": "Gold +{gold}  EXP +{exp}\n",
        "fish_escaped": "The fish got away... try again.",
        "collection_count": "Caught {caught} of {total} species",
        "max_weight": "max {weight}kg",
        "back_help": "Esc or q: Back",
        "owned": "(Owned)",
        "equipped": "(Equipped)",
        "current": "current",
        "rods": "Rods",
        "bait_section": "Bait",
        "gold_owned": "Gold: {gold}",
        "active_title": "Active title",
        "none": "None",
        "level": "Level",
        "exp": "EXP",
        "total_casts": "Total casts",
        "total_caught": "Total fish caught",
        "total_weight": "Total weight caught",
        "total_gold": "Total gold earned",
        "night_catches": "Night catches",
        "epic_legendary": "Epic catches: {epic}  Legendary catches: {legendary}",
        "started_at": "Started at",
        "achievement_list": "Achievement list",
        "title": "Title",
        "reward": "Reward",
        "titles": "Titles",
        "no_titles": "No unlocked titles yet.",
        "empty_aquarium": "No souls live here yet. Wait for new meetings at the fishing spots.",
        "aquarium_title": "Aquarium of Fish Souls",
        "aquarium_subtitle": "Memories etched in your collection swim through the water.",
        "aquarium_help": "r: Refresh souls  |  Esc or q: Back",
        "refresh": "Refresh",
        "sprite_style": "Fish sprite style",
        "sprite_style_desc": "Choose the fish art style shown in catch results and seagull events.",
        "preview": "Preview",
        "language": "Language",
        "language_desc": "Choose the language used by menus, data, events, and results.",
        "spot_select": "Choose Fishing Spot",
        "spot_select_desc": "Choose where you want to fish.",
        "available": "Available",
        "unlock_level": "Unlocks at Lv.{level}",
        "already_have_rod": "You already own this rod.",
        "missing_rod": "That rod does not exist.",
        "not_enough_gold": "Not enough gold. (Need: {price})",
        "bought_rod": "Bought {name}.",
        "missing_bait": "That bait does not exist.",
        "bought_bait": "Bought {name}.",
    },
    "ko": {
        "back": "뒤로",
        "quit": "종료",
        "fish": "낚시",
        "fish_action": "낚시하기",
        "collection": "도감",
        "shop": "상점",
        "achievements": "업적",
        "stats": "통계",
        "aquarium": "어항",
        "settings": "설정",
        "menu_help": "방향키 또는 숫자/엔터/클릭으로 선택  |  q: 종료",
        "angle": "각도",
        "reel_instruction_start": "Space로 ",
        "reel_instruction_middle": "를 ",
        "reel_instruction_end": "에 맞출 때 멈춰라\n[",
        "green_zone": "초록색 구간",
        "fishing_help": "← →: 각도  |  Space: 캐스트/입질/릴  |  Esc: 뒤로",
        "fishing_help_reset": "← →: 각도 조절  |  Space: 캐스트/입질/릴  |  Esc: 뒤로",
        "level_short": "Lv.",
        "gold": "골드",
        "rod": "낚싯대",
        "bait": "미끼",
        "spot": "낚시터",
        "time": "시간",
        "weather": "날씨",
        "waiting": "물고기가 물기를 기다리는 중...",
        "continue_back": "Space: 계속  |  Esc: 뒤로",
        "continue": "Space를 눌러 계속",
        "crab_event": "게가 미끼를 훔쳐갔다! 대신 기본 지렁이를 달았다.",
        "seagull_event": "물고기를 방금 잡았는데 갈매기가 낚아채갔다!",
        "escaped_fish": "도망간 물고기",
        "rarity": "희귀도",
        "worm_event_1": "지렁이가 통에서 반란을 일으켜 도망쳤다!",
        "worm_event_2": "대신 물고기 냄새를 맡고 주변에 물고기들이 몰려든다.",
        "exp_gain": "경험치 +{amount}",
        "level_up": " ★ 레벨업!",
        "tease_event": "물고기가 미끼만 뜯어먹고 도망갔다! 농락당했다...",
        "duck_event": "노란 고무 오리를 낚았다!",
        "duck_event_2": "누가 버린 장난감이다. 다시 던져보자.",
        "bite": "!! 입질 !!  Space를 눌러 릴을 걸어라!",
        "missed_bite": "입질을 놓쳤다... 미끼만 날아갔다.",
        "hook_set": "챔질! Space로 O를 초록색 구간에 멈춰라.",
        "caught": "{fish}을(를) 잡았다!",
        "achievement_unlocked": "\n★ 업적 달성: {names}{title_text}",
        "title_result": "\n칭호: {titles}",
        "weight": "무게",
        "gold_exp_gain": "골드 +{gold}  경험치 +{exp}\n",
        "fish_escaped": "물고기가 도망갔다... 다시 도전해보자.",
        "collection_count": "총 {total}종 중 {caught}종 잡음",
        "max_weight": "최대 {weight}kg",
        "back_help": "Esc 또는 q: 뒤로",
        "owned": "(소유 중)",
        "equipped": "(장비 중)",
        "current": "현재",
        "rods": "낚싯대",
        "bait_section": "미끼",
        "gold_owned": "보유 골드: {gold}",
        "active_title": "장착 칭호",
        "none": "없음",
        "level": "레벨",
        "exp": "경험치",
        "total_casts": "총 캐스트 횟수",
        "total_caught": "총 잡은 마리수",
        "total_weight": "총 잡은 무게",
        "total_gold": "총 번 골드",
        "night_catches": "밤 낚시 횟수",
        "epic_legendary": "Epic 잡은 횟수: {epic}  Legendary 잡은 횟수: {legendary}",
        "started_at": "시작일",
        "achievement_list": "업적 목록",
        "title": "칭호",
        "reward": "보상",
        "titles": "칭호",
        "no_titles": "아직 해금된 칭호가 없습니다.",
        "empty_aquarium": "아직 이 곳에 머물 영혼이 없다. 낚시터에서 만남을 기다리자.",
        "aquarium_title": "물고기들의 영혼이 담긴 어항",
        "aquarium_subtitle": "도감에 새겨진 기억들이 물속을 뛰어다닌다.",
        "aquarium_help": "r: 영혼 새로 불러내기  |  Esc 또는 q: 뒤로",
        "refresh": "새로고침",
        "sprite_style": "물고기 스프라이트 스타일",
        "sprite_style_desc": "낚시 결과와 갈매기 이벤트에서 표시할 물고기 그림 스타일을 고르세요.",
        "preview": "미리보기",
        "language": "언어",
        "language_desc": "메뉴, 데이터, 이벤트, 결과에 사용할 언어를 고르세요.",
        "spot_select": "낚시터 선택",
        "spot_select_desc": "원하는 낚시터를 선택하세요.",
        "available": "가능",
        "unlock_level": "Lv.{level} 해금",
        "already_have_rod": "이미 소유한 낚싯대입니다.",
        "missing_rod": "존재하지 않는 낚싯대입니다.",
        "not_enough_gold": "골드가 부족합니다. (필요: {price})",
        "bought_rod": "{name}을(를) 구매했습니다.",
        "missing_bait": "존재하지 않는 미끼입니다.",
        "bought_bait": "{name}를 구매했습니다.",
    },
}

TIME_OF_DAY = {
    "en": {"dawn": "dawn", "day": "day", "dusk": "dusk", "night": "night"},
    "ko": {"dawn": "새벽", "day": "낮", "dusk": "해질녘", "night": "밤"},
}

WEATHER = {
    "en": {"sunny": "sunny", "cloudy": "cloudy", "rainy": "rainy"},
    "ko": {"sunny": "맑음", "cloudy": "흐림", "rainy": "비"},
}

FISH_NAMES = {
    "en": {
        "carp": "Carp",
        "crucian": "Crucian carp",
        "bluegill": "Bluegill",
        "tilapia": "Tilapia",
        "trout": "Trout",
        "perch": "Perch",
        "catfish": "Catfish",
        "bass": "Bass",
        "eel": "Freshwater eel",
        "pike": "Pike",
        "sturgeon": "Sturgeon",
        "salmon": "Salmon",
        "gold_carp": "Golden carp",
        "mackerel": "Mackerel",
        "tuna": "Tuna",
        "octopus": "Octopus",
        "shark": "Shark",
        "marlin": "Marlin",
        "whale": "Whale",
        "koi": "Koi",
        "zander": "Zander",
        "piranha": "Piranha",
        "red_snapper": "Red snapper",
        "swordfish": "Swordfish",
        "jellyfish": "Jellyfish",
    }
}

SPOT_TRANSLATIONS = {
    "en": {
        "pond": ("Pond", "A quiet pond. Perfect for beginners."),
        "river": ("Riverbank", "Try fishing in restless, flowing water."),
        "lake": ("Lake", "Large fish hide in the wide lake."),
        "sea": ("Sea", "An endless sea. You will need a strong rod."),
    }
}

ROD_TRANSLATIONS = {
    "en": {
        "bamboo": ("Bamboo rod", "The rod you start with."),
        "carbon": ("Carbon rod", "A light dummy rod."),
        "titanium": ("Titanium rod", "A professional rod. It can handle sea monsters."),
    }
}

BAIT_TRANSLATIONS = {
    "en": {
        "worm": ("Worm", "Basic bait. Everything likes it."),
        "cricket": ("Cricket", "Bass and catfish bite well on it."),
        "shrimp": ("Shrimp", "Bait that attracts salmon."),
        "squid_bait": ("Squid bait", "Draws in large sea species."),
        "golden_bait": ("Golden bait", "Attracts rare fish."),
    }
}

ACHIEVEMENT_TRANSLATIONS = {
    "en": {
        "first_fish": ("First Catch", "Catch one fish", "Fishing Novice"),
        "ten_fish": ("Skilled Angler", "Catch 10 fish", "Pond Ruler"),
        "hundred_fish": ("Fishing Fanatic", "Catch 100 fish", "Fishing Addict"),
        "heavy_haul": ("Heavy Haul", "Catch 10kg total weight", "Strong Angler"),
        "ton_of_fish": ("One-Ton Record", "Catch 100kg total weight", "Big Catch Angler"),
        "rich": ("Born Rich", "Hold 1000 gold", "Rich Angler"),
        "collector": ("Collector", "Catch at least 5 species", "Collection Keeper"),
        "master_collector": ("Perfect Collector", "Catch every species", "Fish Scholar"),
        "whale_hunter": ("Whale Hunter", "Catch a whale", "Ruler of the Sea"),
        "night_owl": ("Night Angler", "Catch 10 fish at night", "Night Tracker"),
        "legendary_catch": ("Legendary Fish", "Catch a Legendary fish", "Legendary Angler"),
    }
}


def t(language: str, key: str, **kwargs: Any) -> str:
    language = normalize_language(language)
    text = UI_TEXT[language].get(key, UI_TEXT[DEFAULT_LANGUAGE].get(key, key))
    return text.format(**kwargs) if kwargs else text


def time_label(language: str, value: str) -> str:
    language = normalize_language(language)
    return TIME_OF_DAY[language].get(value, value)


def weather_label(language: str, value: str) -> str:
    language = normalize_language(language)
    return WEATHER[language].get(value, value)


def fish_name(language: str, fish: Any) -> str:
    if normalize_language(language) == "en":
        return FISH_NAMES["en"].get(fish.id, fish.name)
    return fish.name


def spot_name(language: str, spot: Any) -> str:
    if normalize_language(language) == "en":
        return SPOT_TRANSLATIONS["en"].get(spot.id, (spot.name, spot.description))[0]
    return spot.name


def spot_description(language: str, spot: Any) -> str:
    if normalize_language(language) == "en":
        return SPOT_TRANSLATIONS["en"].get(spot.id, (spot.name, spot.description))[1]
    return spot.description


def rod_name(language: str, rod: Any) -> str:
    if normalize_language(language) == "en":
        return ROD_TRANSLATIONS["en"].get(rod.id, (rod.name, rod.description))[0]
    return rod.name


def rod_description(language: str, rod: Any) -> str:
    if normalize_language(language) == "en":
        return ROD_TRANSLATIONS["en"].get(rod.id, (rod.name, rod.description))[1]
    return rod.description


def bait_name(language: str, bait: Any) -> str:
    if normalize_language(language) == "en":
        return BAIT_TRANSLATIONS["en"].get(bait.id, (bait.name, bait.description))[0]
    return bait.name


def bait_description(language: str, bait: Any) -> str:
    if normalize_language(language) == "en":
        return BAIT_TRANSLATIONS["en"].get(bait.id, (bait.name, bait.description))[1]
    return bait.description


def achievement_name(language: str, achievement: Any) -> str:
    if normalize_language(language) == "en":
        return ACHIEVEMENT_TRANSLATIONS["en"].get(
            achievement.id,
            (achievement.name, achievement.description, achievement.title),
        )[0]
    return achievement.name


def achievement_description(language: str, achievement: Any) -> str:
    if normalize_language(language) == "en":
        return ACHIEVEMENT_TRANSLATIONS["en"].get(
            achievement.id,
            (achievement.name, achievement.description, achievement.title),
        )[1]
    return achievement.description


def achievement_title(language: str, achievement: Any) -> str | None:
    if achievement.title is None:
        return None
    if normalize_language(language) == "en":
        return ACHIEVEMENT_TRANSLATIONS["en"].get(
            achievement.id,
            (achievement.name, achievement.description, achievement.title),
        )[2]
    return achievement.title


def title_label(language: str, stored_title: str) -> str:
    if not stored_title:
        return ""
    if normalize_language(language) == "ko":
        return stored_title
    for translations in ACHIEVEMENT_TRANSLATIONS["en"].values():
        english_title = translations[2]
        if english_title == stored_title:
            return english_title
    return {
        "낚시 입문자": "Fishing Novice",
        "연못 지배자": "Pond Ruler",
        "낚시 중독자": "Fishing Addict",
        "힘센 낚시꾼": "Strong Angler",
        "대물 낚시꾼": "Big Catch Angler",
        "부자 낚시꾼": "Rich Angler",
        "도감 수집가": "Collection Keeper",
        "물고기 박사": "Fish Scholar",
        "바다의 제왕": "Ruler of the Sea",
        "밤의 추적자": "Night Tracker",
        "전설 낚시꾼": "Legendary Angler",
    }.get(stored_title, stored_title)
