from abc import ABC, abstractmethod
from utils import config, ColorRgbw, SystemState, get_rgbw, ShowType


class BufferBuilder(ABC):
    def __init__(self, name, is_consecutive: bool = False) -> None:
        self._name: ShowType = name,
        self._is_consecutive = is_consecutive

    @property
    def name(self):
        return self._name

    @property
    def is_consecutive(self):
        return self._is_consecutive

    @abstractmethod
    def build_buffer(self) -> list[ColorRgbw]:
        pass


class OneColor(BufferBuilder):
    def __init__(self, system_state) -> None:
        super().__init__(ShowType.COLOR)
        self._system_state: SystemState = system_state

    def build_buffer(self) -> list[ColorRgbw]:
        color = get_rgbw(self._system_state.hex_rgb)
        return [color for i in range(config.NUM_PIXEL)]


class RainbowCycle(BufferBuilder):
    def __init__(self) -> None:
        super().__init__(ShowType.RAINBOW, True)
        self._wheel_position: int

    def build_buffer(self) -> list[ColorRgbw]:
        buffer: list[ColorRgbw] = []

        for pixel in range(config.NUM_PIXEL):
            pixel_index = (pixel * 256 // config.NUM_PIXEL) + \
                self._wheel_position
            color = self.__wheel((pixel_index & 255))
            buffer[pixel] = color

        self._wheel_position = ((self._wheel_position+1) & 255)
        return buffer

    def __wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colors are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            red = green = blue = 0
        elif pos < 85:
            red = int(pos * 3)
            green = int(255 - pos * 3)
            blue = 0
        elif pos < 170:
            pos -= 85
            red = int(255 - pos * 3)
            green = 0
            blue = int(pos * 3)
        else:
            pos -= 170
            red = 0
            green = int(pos * 3)
            blue = int(255 - pos * 3)
        return ColorRgbw(red, green, blue)


def black_color() -> list[ColorRgbw]:
    return [ColorRgbw(0, 0, 0, 0) for i in range(config.NUM_PIXEL)]


def effect_factory(state: SystemState) -> list[BufferBuilder]:
    list(
        OneColor(state),
        RainbowCycle()
    )
