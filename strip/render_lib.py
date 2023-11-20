import strip.neopixel_provider as neo_instance
from utils import ColorRgbw, CycleState, RenderCycle, log


class FaderFrontToBack(RenderCycle):
    def __init__(self, neo) -> None:
        super().__init__(neo)
        self._index: int = 0

    def _initialise(self) -> None:
        self._index = 0
        self._cycle_state = CycleState.RUN

    def render(self, neo_buffer: list[ColorRgbw], is_consecutive: bool = False) -> None:
        if self.is_render_start:
            self._initialise()
        log.debug('Render cycle name: %s, index: %s',
                  self.__class__, self._index)
        self._render_at_index(self._index, neo_buffer[self._index])

        self._index += 1
        self._set_cycle_state(is_consecutive)

    def _set_cycle_state(self, is_consecutive: bool) -> None:
        if self._index is self._neo.pixels.n:
            self._cycle_state = CycleState.START if is_consecutive else CycleState.STOP


class FaderBackToFront(RenderCycle):
    def __init__(self, neo) -> None:
        super().__init__(neo)
        self._index = self._neo.pixels.n-1

    def _initialise(self) -> None:
        self._index = self._neo.pixels.n-1
        self._cycle_state = CycleState.RUN

    def render(self, neo_buffer: list[ColorRgbw], is_consecutive: bool = False) -> None:
        if self.is_render_start:
            self._initialise()
        log.debug('Render cycle name: %s, index: %s',
                  self.__class__, self._index)
        self._render_at_index(self._index, neo_buffer[self._index])

        self._index -= 1
        self._set_cycle_state(is_consecutive)

    def _set_cycle_state(self, is_consecutive: bool) -> None:
        if self._index == -1:
            self._cycle_state = CycleState.START if is_consecutive else CycleState.STOP


def set_brightness(value):
    if value is not neo_instance.pixels.brightness:
        neo_instance.pixels.brightness = value
        neo_instance.pixels.show()


def render_cycle_factory() -> list[RenderCycle]:
    return [
        FaderBackToFront(neo_instance),
        FaderFrontToBack(neo_instance)
    ]
