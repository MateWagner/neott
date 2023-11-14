from abc import ABC, abstractmethod
from .enums import ColorRgbw
from .enums import CycleState


class RenderCycle(ABC):
    def __init__(self, neo_pixel_instance) -> None:
        self._neo = neo_pixel_instance
        self._cycle_state: CycleState = CycleState.STOP

    @property
    def is_render_finished(self) -> bool:
        return self._cycle_state == CycleState.STOP

    @property
    def is_render_start(self) -> bool:
        return self._cycle_state == CycleState.START

    @abstractmethod
    def initialise(self) -> None:
        pass

    @abstractmethod
    def render(self, neo_buffer: list[ColorRgbw], is_consecutive: bool = False) -> None:
        pass

    @abstractmethod
    def _set_cycle_state(self, is_consecutive: bool) -> None:
        pass

    def _render_at_index(self, index: int,  color: ColorRgbw) -> None:
        self._neo.pixels[index] = (
            (color.red, color.green, color.blue, color.white))
        self._neo.pixels.show()

    def get_render_state(self) -> CycleState:
        return self._cycle_state
