from collections.abc import Callable
from threading import Event, Lock
import re
from .log_provider import log
from .value_converter import get_rgbw
from .enums import ColorRgbw
from .enums import ShowType
from .enums import MainSwitchState


def auto_notify(method):
    def wrapper(self, *args, **kwargs):
        topic_name = method.__name__
        value = args[0]
        with self.lock:
            try:
                result = method(self, *args, **kwargs)
                self.notify_observers(topic_name, value)
            except ValueError as err:
                log.error(err)
                result = None

        return result
    return wrapper


class SystemState:
    def __init__(self, message_system):
        self.lock: Lock = Lock()
        self._render_interrupt_event: Event = Event()
        self.wake_up_event: Event = Event()
        self.loop_sleep_event: Event = Event()
        self._main_switch: MainSwitchState = MainSwitchState.OFF
        self._show_type: ShowType = ShowType.COLOR
        self._wait = 0.1
        self._hex_rgb = "#ff80ff"
        self._brightness = 1.0
        self._message_sender: MessagingSystem = message_system

    @property
    def is_on(self) -> bool:
        return self._main_switch == MainSwitchState.ON

    @property
    def main_switch(self):
        return self._main_switch

    @main_switch.setter
    @auto_notify
    def main_switch(self, value: str):
        try:
            self._main_switch = MainSwitchState[value]
            self._induce_render_cycle()
        except KeyError as exc:
            raise ValueError(
                f"Invalid main_switch: {value}. Valid values are {', '.join(e.name for e in MainSwitchState)}") from exc

    @property
    def get_rgb_value(self) -> ColorRgbw:
        return get_rgbw(self._hex_rgb)  # TODO inject dependency

    @property
    def hex_rgb(self):
        return self._hex_rgb

    @hex_rgb.setter
    @auto_notify
    def hex_rgb(self, value: str):
        pattern = r'^#([A-Fa-f0-9]{3}([A-Fa-f0-9]{1,2})?|[A-Fa-f0-9]{6}([A-Fa-f0-9]{2})?)$'

        if not re.match(pattern, value):
            raise ValueError(
                f"Invalid hex_color: {value}.Value must be valid GRB value in HEX code")

        self._hex_rgb = value.capitalize()
        self._induce_render_cycle()

    @property
    def show_type(self):
        return self._show_type

    @show_type.setter
    @auto_notify
    def show_type(self, value: str):
        try:
            self._show_type = ShowType[value]
            self._induce_render_cycle()
        except KeyError as exc:
            raise ValueError(
                f"Invalid show_type: {value}. Valid values are {', '.join(e.name for e in ShowType)}") from exc

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    @auto_notify
    def brightness(self, value: float):
        if 0 <= value <= 1:
            self._brightness = value
            self._induce_wake_up()
        else:
            raise ValueError(
                f"Invalid brightness: {value}.Value must be between 0 and 1")

    @property
    def wait(self):
        return self._wait

    @wait.setter
    @auto_notify
    def wait(self, value: float):
        if 0 <= value <= 1:
            self._wait = value
        else:
            raise ValueError(
                f"Invalid wait: {value}. Value must be between 0 and 1")

    def add_message_callback(self, callback: Callable[[str, str], None]) -> None:
        self._message_sender.add_message_callback(callback)

    def notify_observers(self, topic_name, value):
        self._message_sender.send_messages(topic_name, value)

    def is_render_interrupted(self) -> bool:
        if self._render_interrupt_event.is_set():
            with self.lock:
                self._render_interrupt_event.clear()
            return True
        return False

    def set_loop_is_stopped_event(self) -> None:
        with self.lock:
            self.loop_sleep_event.set()

    def clear_wakeup_event(self) -> None:
        with self.lock:
            self.wake_up_event.clear()

    def _induce_render_cycle(self):
        self._render_interrupt_event.set()
        self._induce_wake_up()

    def _induce_wake_up(self) -> None:
        if self.loop_sleep_event.is_set():
            self.loop_sleep_event.clear()
            self.wake_up_event.set()

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


class MessagingSystem:
    def __init__(self) -> None:
        self._callback_list: list[Callable[[str, str], None]] = list([])

    def add_message_callback(self, msg_callback: Callable[[str, str], None]) -> None:
        self._callback_list.append(msg_callback)

    def send_messages(self, topic: str, payload: str) -> None:
        for msg_callback in self._callback_list:
            msg_callback(topic, payload)
