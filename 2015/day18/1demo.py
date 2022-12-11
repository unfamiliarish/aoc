# from asciimatics import COLOUR_GREEN
from asciimatics.screen import Screen
from asciimatics.renderers.base import StaticRenderer
from asciimatics.scene import Scene
from asciimatics.effects import Print, Effect
from time import sleep


def demo(screen):
    s = r"abc"

    for i in range(5):
        screen.clear()
        screen.print_at(s, 10, 5 + i, Screen.COLOUR_, Screen.A_BOLD)
        screen.refresh()

    # screen.print_at(ss, 10, 5, Screen.COLOUR_GREEN)
    screen.refresh()
    sleep(10)


Screen.wrapper(demo)
