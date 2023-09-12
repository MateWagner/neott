from collections import namedtuple
from collections.abc import Callable
from enum import Enum
from threading import Event, Lock

ColorRgbw = namedtuple(
    'Color_rgbw', ['red', 'green', 'blue', 'white'], defaults=[0, 0, 0, 0])

default_color = ColorRgbw(255, 125, 255,)


class ShowType(Enum):
    COLOR = 1
    RAINBOW = 2


class CycleState(Enum):
    START = 1
    RUN = 2
    STOP = 3


def auto_notify(method):
    def wrapper(self, *args, **kwargs):
        topic_name = method.__name__
        value = args[0]
        with self.lock:
            result = method(self, *args, **kwargs)
            self.notify_observers(topic_name, value)
        return result
    return wrapper


class SystemState:
    def __init__(self, message_system):
        self.lock: Lock = Lock()
        self.render_interrupt_event: Event = Event()
        self.wake_up_event: Event = Event()
        self.loop_sleep_event: Event = Event()
        self._main_switch = 'OFF'
        self._show_type: ShowType = ShowType.COLOR
        self._wait = 0.1
        self._hex_rgb = "#ff80ff"
        self._brightness = 1.0
        self._message_sender: MessagingSystem = message_system

    @property
    def main_switch(self):
        return self._main_switch

    @main_switch.setter
    @auto_notify
    def main_switch(self, value: str):
        self._main_switch = value
        self._induce_render_cycle()

    @property
    def hex_rgb(self):
        return self._hex_rgb

    @hex_rgb.setter
    @auto_notify
    def hex_rgb(self, value: str):
        self._hex_rgb = value.capitalize()
        self._induce_render_cycle()

    @property
    def show_type(self):
        return self._show_type

    @show_type.setter
    @auto_notify
    def show_type(self, value: str):
        self._show_type = ShowType[value]
        self._induce_render_cycle()

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    @auto_notify
    def brightness(self, value: float):
        self._brightness = value
        self._induce_wake_up()

    @property
    def wait(self):
        return self._wait

    @wait.setter
    @auto_notify
    def wait(self, value: float):
        self._wait = value

    def add_message_callback(self, callback: Callable[[str, str], None]) -> None:
        self._message_sender.add_message_callback(callback)

    def notify_observers(self, topic_name, value):
        self._message_sender.send_messages(topic_name, value)

    def _induce_render_cycle(self):
        self.render_interrupt_event.set()
        self._induce_wake_up()

    def _induce_wake_up(self):
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


class NeoLoopControl:
    def __init__(self, render_index, neo_buffer):
        self.effect_cycle_index = 0
        self.previous_main_switch_state = 0
        self.wheel_pos = 0
        self.render_index = render_index
        self.effect_state = "STOP"
        self.neo_buffer = neo_buffer
