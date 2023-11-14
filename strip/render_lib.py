import strip.neopixel_provider as neo
from utils import ColorRgbw, CycleState, RenderCycle


class FaderFrontToBack(RenderCycle):
    def __init__(self) -> None:
        super().__init__(neo)
        self._index: int = 0

    def render_firs_pixel(self, neo_buffer: list[ColorRgbw]) -> None:
        self._index = 0
        self._cycle_state = CycleState.RUN
        self.render_next_pixel(neo_buffer)

    def render_next_pixel(self, neo_buffer: list[ColorRgbw], is_consecutive: bool = False) -> None:
        self._render_at_index(self._index, neo_buffer[self._index])

        self._index += 1
        self._set_cycle_state(is_consecutive)

    def _set_cycle_state(self, is_consecutive: bool) -> None:
        if self._index is self._neo.pixels.n:
            self._cycle_state = CycleState.START if is_consecutive else CycleState.STOP


class FaderBackToFront(RenderCycle):
    def __init__(self) -> None:
        super().__init__(neo)
        self._index = self._neo.pixels.n-1

    def render_firs_pixel(self, neo_buffer: list[ColorRgbw]) -> None:
        self._index = self._neo.pixels.n-1
        self._cycle_state = CycleState.RUN
        self.render_next_pixel(neo_buffer)

    def render_next_pixel(self, neo_buffer: list[ColorRgbw], is_consecutive: bool = False) -> None:
        self._render_at_index(self._index, neo_buffer[self._index])

        self._index -= 1
        self._set_cycle_state(is_consecutive)

    def _set_cycle_state(self, is_consecutive: bool) -> None:
        if self._index == -1:
            self._cycle_state = CycleState.START if is_consecutive else CycleState.STOP


def set_brightness(value):
    if value is not neo.pixels.brightness:
        neo.pixels.brightness = value
        neo.pixels.show()


def render_cycle_factory() -> list[RenderCycle]:
    return [
        FaderBackToFront(),
        FaderFrontToBack()
    ]
