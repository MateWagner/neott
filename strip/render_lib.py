from abc import ABC, abstractmethod
import strip.neopixel_provider as neo
from utils import ColorRgbw, CycleState


class RenderCycle(ABC):
    def __init__(self, neo_pixel_instance) -> None:
        self._neo = neo_pixel_instance
        self._cycle_state: CycleState = CycleState.STOP

    @abstractmethod
    def render_firs_pixel(self, neo_buffer: list[ColorRgbw], is_consecutive: bool) -> None:
        pass

    @abstractmethod
    def render_next_pixel(self, neo_buffer: list[ColorRgbw], is_consecutive: bool) -> None:
        pass

    def render_at_index(self, color: ColorRgbw, index: int) -> None:
        self._neo.pixels[index] = (
            (color.red, color.green, color.blue, color.white))
        self._neo.pixels.show()

    def get_render_state(self) -> CycleState:
        return self._cycle_state


class FaderFrontToBack(RenderCycle):
    _index: int = 0

    def __init__(self) -> None:
        super().__init__(neo)

    def render_firs_pixel(self, neo_buffer: list[ColorRgbw], is_consecutive: bool) -> None:
        self._index = 0
        self._cycle_state = CycleState.RUN
        self.render_next_pixel(neo_buffer, is_consecutive)

    def render_next_pixel(self, neo_buffer: list[ColorRgbw], is_consecutive: bool) -> None:
        self.render_at_index(self._index, neo_buffer[self._index])

        self._index += 1

        if self._index == self._neo.pixels.n-1:
            self._cycle_state = CycleState.START if is_consecutive else CycleState.STOP


class FaderBackToFront(RenderCycle):
    _index: int = 0

    def __init__(self) -> None:
        super().__init__(neo)
        self._index = self._neo.pixels.n-1

    def render_firs_pixel(self, neo_buffer: list[ColorRgbw], is_consecutive: bool) -> None:
        self._index = self._neo.pixels.n-1
        self._cycle_state = CycleState.RUN
        self.render_next_pixel(neo_buffer, is_consecutive)

    def render_next_pixel(self, neo_buffer: list[ColorRgbw], is_consecutive: bool) -> None:
        self.render_at_index(self._index, neo_buffer[self._index])

        self._index += 1

        if self._index == 0:
            self._cycle_state = CycleState.START if is_consecutive else CycleState.STOP


def set_brightness(value):
    if (value != neo.pixels.brightness):
        neo.pixels.brightness = value
        neo.pixels.show()


def render_at_index(effect_control):
    rgbw = effect_control.neo_buffer[effect_control.effect_cycle_index]

    neo.pixels[effect_control.effect_cycle_index] = (
        (rgbw.red, rgbw.green, rgbw.blue, rgbw.white))
    neo.pixels.show()


def render_cycle_factory() -> list[RenderCycle]:
    return list(
        FaderBackToFront(),
        FaderFrontToBack()
    )
