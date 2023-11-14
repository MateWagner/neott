
from utils import config, ColorRgbw, SystemState, \
    ShowType, BufferBuilder, BufferBuilderRandom
from .render_lib import render_cycle_factory


class TurnOff(BufferBuilderRandom):
    def __init__(self, render_cycle_list, system_state) -> None:
        super().__init__(ShowType.COLOR, system_state, render_cycle_list)

    def _drew_buffer(self) -> None:
        self._neo_buffer = [ColorRgbw(0, 0, 0, 0)
                            for i in range(config.NUM_PIXEL)]


class OneColor(BufferBuilderRandom):
    def __init__(self, render_cycle_list, system_state) -> None:
        super().__init__(ShowType.COLOR, system_state, render_cycle_list)

    def _drew_buffer(self) -> None:
        color = self._system_state.get_rgb_value
        self._neo_buffer = [color for i in range(config.NUM_PIXEL)]


class RainbowCycle(BufferBuilderRandom):
    def __init__(self, render_cycle_list, system_state) -> None:
        super().__init__(ShowType.RAINBOW, system_state, render_cycle_list, True)
        self._wheel_position: int = 0

    def _drew_buffer(self) -> None:
        buffer: list[ColorRgbw] = []

        for pixel in range(config.NUM_PIXEL):
            pixel_index = (pixel * 256 // config.NUM_PIXEL) + \
                self._wheel_position
            color = self._wheel((pixel_index & 255))
            buffer.append(color)
        self._wheel_position = ((self._wheel_position+1) & 255)

        self._neo_buffer = buffer

    def _wheel(self, pos):
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
        OneColor(render_cycle_factory(), state),
        RainbowCycle(render_cycle_factory(), state)
    ]
