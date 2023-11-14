from .effect_type import BufferBuilder
from .enums import ShowType


class NeoLoopControl:
    def __init__(self, effect_list, turn_off_effect):
        self._effect_list: list[BufferBuilder] = effect_list
        self._current_effect: BufferBuilder = effect_list[0]
        self._turn_off_effect: BufferBuilder = turn_off_effect

    @property
    def turn_off_effect(self) -> BufferBuilder:
        return self._turn_off_effect

    @property
    def current_effect(self) -> BufferBuilder:
        return self._current_effect

    @property
    def is_render_finished(self) -> bool:
        return self.current_effect.is_render_finished

    def set_new_effect(self, show_type: ShowType) -> None:
        self._current_effect = next(
            (effect for effect in self._effect_list if effect.is_name_match(show_type)), self._effect_list[0])
