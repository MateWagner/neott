import random
from abc import ABC, abstractmethod
from .enums import ColorRgbw
from .enums import ShowType
from .data_types import SystemState
from .render_type import RenderCycle


class BufferBuilder(ABC):
    def __init__(self, name, system_state, is_consecutive: bool = False) -> None:
        self._name: ShowType = name
        self._system_state: SystemState = system_state
        self._is_consecutive: bool = is_consecutive
        self._neo_buffer: list[ColorRgbw]
        self._render_cycle: RenderCycle

    def is_name_match(self, show_type: ShowType) -> bool:
        return self._name == show_type

    @property
    def is_consecutive(self):
        return self._is_consecutive

    @property
    def is_render_finished(self) -> bool:
        return self._render_cycle.is_render_finished

    @property
    def _is_render_start(self) -> bool:
        return self._render_cycle.is_render_start

    @abstractmethod
    def _drew_buffer(self) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass


class BufferBuilderRandom(BufferBuilder):
    def __init__(self, name, system_state, render_cycle_list, is_consecutive: bool = False) -> None:
        super().__init__(name, system_state, is_consecutive)
        self._list_of_render_cycle: list[RenderCycle] = render_cycle_list
        self._set_new_random_render_cycle()

    def _set_new_random_render_cycle(self) -> None:
        self._render_cycle = random.choice(self._list_of_render_cycle)

    def render(self) -> None:
        if self._system_state.is_render_interrupted() or self._is_render_start:
            self._drew_buffer()
            self._set_new_random_render_cycle()
            self._render_cycle.initialise()

        if self.is_render_finished:
            return

        self._render_cycle.render(
            self._neo_buffer, self._is_consecutive)
