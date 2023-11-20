from collections import namedtuple
from enum import Enum, auto

ColorRgbw = namedtuple(
    'Color_rgbw', ['red', 'green', 'blue', 'white'], defaults=[0, 0, 0, 0])

default_color = ColorRgbw(255, 125, 255,)


class ShowType(Enum):
    COLOR = "Color"
    RAINBOW_LOOP = "Rainbow Loop"
    COLOR_LOOP = "Color Loop"

    @classmethod
    def get_show_type_dict(cls):
        return {member.name: member.value for member in cls}


class RenderType(Enum):
    COLOR = auto()
    RAINBOW = auto()
    COLOR_LOOP = auto()


class CycleState(Enum):
    START = auto()
    RUN = auto()
    STOP = auto()


class MainSwitchState(Enum):
    ON = auto()
    OFF = auto()
