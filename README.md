# mulgogi 🎣

A fishing game in your terminal.

```bash
pip install mulgogi
mulgogi
```

## Features

- 터미널에서 즐기는 낚시 루프: 캐스트 → 입질 → 릴
- 4개 낚시터, 10종의 물고기
- 레벨/경험치/골드 성장 시스템
- 도감, 업적, 통계
- 낚싯대/미끼 상점
- 시간대/날씨에 따라 달라지는 물고기 출현

## Controls

- `←` `→`: 낚싯대 각도 조절 (장식용)
- `Space`: 캐스트 / 입질 걸기 / 릴 멈추기
- `Esc` / `q`: 뒤로가기 / 종료

## Install

### pip

```bash
pip install mulgogi
mulgogi
```

### Homebrew (macOS/Linux)

```bash
brew tap justart-dev/mulgogi
brew install mulgogi
mulgogi
```

### Development

```bash
git clone https://github.com/justart-dev/mulgogi.git
cd mulgogi
python -m venv .venv
source .venv/bin/activate
pip install -e .
mulgogi
```

## License

MIT
