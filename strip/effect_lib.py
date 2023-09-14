
from utils import config, ColorRgbw, SystemState, get_rgbw, ShowType, BufferBuilder


class OneColor(BufferBuilder):
    def __init__(self, system_state) -> None:
        super().__init__(ShowType.COLOR)
        self._system_state: SystemState = system_state

    def drew_buffer(self) -> list[ColorRgbw]:
        color = get_rgbw(self._system_state.hex_rgb)
        return [color for i in range(config.NUM_PIXEL)]


class RainbowCycle(BufferBuilder):
    def __init__(self) -> None:
        super().__init__(ShowType.RAINBOW, True)
        self._wheel_position: int = 0

    def drew_buffer(self) -> list[ColorRgbw]:
        buffer: list[ColorRgbw] = []

        for pixel in range(config.NUM_PIXEL):
            pixel_index = (pixel * 256 // config.NUM_PIXEL) + \
                self._wheel_position
            color = self.__wheel((pixel_index & 255))
            buffer.append(color)
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


def drew_off() -> list[ColorRgbw]:
    return [ColorRgbw(0, 0, 0, 0) for i in range(config.NUM_PIXEL)]


def effect_factory(state: SystemState) -> list[BufferBuilder]:
    return [
        OneColor(state),
        RainbowCycle()
    ]
