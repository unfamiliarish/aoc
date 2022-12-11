from asciimatics.screen import Screen
from asciimatics.renderers.base import StaticRenderer
from asciimatics.scene import Scene
from asciimatics.effects import Print, Effect

from dataclasses import dataclass
from enum import Enum

from time import sleep


class LightState(Enum):
    # brighter = turning on
    # darker = turning off
    OFF = -1
    DARKER = 0
    BRIGHTER = 1
    ON = 2


class ChristmasLights:
    def __init__(self) -> None:
        def build_light_grid() -> list:
            pass

        self.light_grid = build_light_grid()


def get_state_changes() -> None:
    pass


def update_new_states():
    pass


def get_new_state():
    def count_neighbors():
        pass

    pass


def get_char_and_color():
    pass


light_on = Screen.COLOUR_CYAN
turning_on = Screen.COLOUR_WHITE
turning_off = Screen.COLOUR_BLUE


def demo(screen):
    s = "abcc"
    for i in range(20):
        screen.clear()
        screen.print_at(s, 10, 5 + i, Screen.COLOUR_WHITE)
        screen.refresh()
        sleep(0.75)

    # screen.print_at(ss, 10, 5, Screen.COLOUR_GREEN)
    screen.refresh()
    sleep(10)


def count_neighbors(light_grid: list[list[int]], x: int, y: int) -> int:
    # counts neighbors of light at position (x,y)
    pass


def new_light_state(light_grid: list[list[int]]) -> list[list[int]]:
    # takes in light grid and returns new one with modified state
    pass


Screen.wrapper(demo)
