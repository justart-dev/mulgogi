import argparse

from textual.app import App

from .game import load_state
from .ui import (
    CollectionScreen,
    FishingScreen,
    MainMenuScreen,
    ShopScreen,
    SpotSelectScreen,
    StatsScreen,
)


class MulgogiApp(App):
    """mulgogi 메인 앱"""

    CSS = """
    Screen { align: center middle; }
    .menu { width: 60; height: auto; border: solid green; padding: 1 2; }
    .collection { width: 80; height: auto; border: solid blue; padding: 1 2; }
    .shop { width: 70; height: auto; border: solid yellow; padding: 1 2; }
    .stats { width: 60; height: auto; border: solid magenta; padding: 1 2; }
    .spots { width: 70; height: auto; border: solid cyan; padding: 1 2; }
    .title { text-align: center; text-style: bold; }
    .subtitle { text-align: center; }
    .section { text-style: bold; }
    Static { text-align: center; }
    Button { width: 100%; }
    """

    def __init__(self):
        super().__init__()
        self.game_state = load_state()

    def on_mount(self):
        self.push_screen(MainMenuScreen())


def main():
    parser = argparse.ArgumentParser(prog="mulgogi", description="A fishing game in your terminal")
    parser.add_argument("--version", action="version", version="%(prog)s 0.3.0")
    parser.parse_args()
    app = MulgogiApp()
    app.run()


if __name__ == "__main__":
    main()
