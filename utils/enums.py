from collections import namedtuple
from enum import Enum, auto

ColorRgbw = namedtuple(
    'Color_rgbw', ['red', 'green', 'blue', 'white'], defaults=[0, 0, 0, 0])

default_color = ColorRgbw(255, 125, 255,)


class ShowType(Enum):
    OFF = auto()
    COLOR = auto()
    RAINBOW = auto()


class CycleState(Enum):
    START = auto()
    RUN = auto()
    STOP = auto()


class MainSwitchState(Enum):
    ON = auto()
    OFF = auto()
