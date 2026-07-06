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

    CSS_PATH = "mulgogi.tcss"

    def __init__(self):
        super().__init__()
        self.game_state = load_state()

    def on_mount(self):
        self.push_screen(MainMenuScreen())


def main():
    parser = argparse.ArgumentParser(prog="mulgogi", description="A fishing game in your terminal")
    parser.add_argument("--version", action="version", version="%(prog)s 0.4.0")
    parser.parse_args()
    app = MulgogiApp()
    app.run()


if __name__ == "__main__":
    main()
