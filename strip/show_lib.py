
from utils import config, ColorRgbw, SystemState, \
    ShowType, NamedShow, NamedShowRandomRender, ShowRandomRender, log
from .render_lib import render_cycle_factory
from .util.strip_helpers import wheel


class TurnOff(ShowRandomRender):
    def __init__(self, render_cycle_list, system_state) -> None:
        super().__init__(system_state, render_cycle_list)

    def _drew_buffer(self) -> None:
        log.debug('Show: %s, drew new buffer', self.__class__)
        self._neo_buffer = [ColorRgbw() for i in range(config.NUM_PIXEL)]


class OneColor(NamedShowRandomRender):
    def __init__(self, render_cycle_list, system_state) -> None:
        super().__init__(ShowType.COLOR, system_state, render_cycle_list)

    def _drew_buffer(self) -> None:
        log.debug('Show: %s, drew new buffer', self.__class__)
        color = self._system_state.get_rgb_value
        self._neo_buffer = [color for i in range(config.NUM_PIXEL)]


class RainbowLoop(NamedShowRandomRender):
    def __init__(self, render_cycle_list, system_state) -> None:
        super().__init__(ShowType.RAINBOW_LOOP, system_state, render_cycle_list, True)
        self._wheel_position: int = 0

    def _drew_buffer(self) -> None:
        log.debug('Show: %s, drew new buffer', self.__class__)
        buffer: list[ColorRgbw] = []

        for pixel in range(config.NUM_PIXEL):
            pixel_index = (pixel * 256 // config.NUM_PIXEL) + \
                self._wheel_position
            color = wheel((pixel_index & 255))
            buffer.append(color)
        self._wheel_position = (self._wheel_position+1) & 255

        self._neo_buffer = buffer


class ColorLoop(NamedShowRandomRender):
    def __init__(self, render_cycle_list, system_state) -> None:
        super().__init__(ShowType.COLOR_LOOP, system_state, render_cycle_list, True)
        self._wheel_position: int = 0

    def _drew_buffer(self) -> None:
        log.debug('Show: %s, drew new buffer', self.__class__)
        color = wheel((self._wheel_position & 255))
        self._neo_buffer = [color for i in range(config.NUM_PIXEL)]
        self._wheel_position = (self._wheel_position+1) & 255


def named_show_factory(state: SystemState) -> list[NamedShow]:
    render_list = render_cycle_factory()
    return [
        OneColor(render_list, state),
        RainbowLoop(render_list, state),
        ColorLoop(render_list, state)
    ]
