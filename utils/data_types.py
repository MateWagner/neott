from collections import namedtuple
from threading import Event, Lock

ColorRgbw = namedtuple(
    'Color_rgbw', ['red', 'green', 'blue', 'white'], defaults=[0, 0, 0, 0])

default_color = ColorRgbw(255, 125, 255,)


class SystemState:
    def __init__(self, send_update_to_mqtt, send_update_to_websocket):
        self.lock: Lock = Lock()
        self.render_interrupt_event: Event = Event()
        self.wake_up_event: Event = Event()
        self.loop_sleep_event: Event = Event()
        self._main_switch = 'OFF'
        self._show_type = 'COLOR'
        self._wait = 0.1
        self._hex_rgb = "#ff80ff"
        self._brightness = 1.0
        self._send_update_to_mqtt = send_update_to_mqtt
        self._send_update_to_websocket = send_update_to_websocket

    @property
    def main_switch(self):
        return self._main_switch

    @main_switch.setter
    def main_switch(self, value: str):
        with self.lock:
            self._main_switch = value
            self._induce_render_cycle()

    @property
    def hex_rgb(self):
        return self._hex_rgb

    @hex_rgb.setter
    def hex_rgb(self, value: str):
        with self.lock:
            self._hex_rgb = value
            self._induce_render_cycle()

    @property
    def show_type(self):
        return self._show_type

    @show_type.setter
    def show_type(self, value: str):
        with self.lock:
            self._show_type = value
            self._induce_render_cycle()

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value: float):
        with self.lock:
            self._brightness = value
            self._induce_wake_up()

    @property
    def wait(self):
        return self._wait

    @wait.setter
    def wait(self, value: float):
        with self.lock:
            self._wait = value

    def send_message_to_websocket(self, message):
        with self.lock:
            self._send_update_to_websocket(message)

    def send_message_to_mqtt(self, topic, data):
        with self.lock:
            self._send_update_to_mqtt(topic, data)

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
        with self.lock:
            setattr(self, key, value)


class EffectControl:
    def __init__(self, render_callback, neo_buffer):
        self.effect_cycle_index = 0
        self.previous_main_switch_state = 0
        self.wheel_pos = 0
        self.render_callback = render_callback
        self.effect_state = "STOP"
        self.neo_buffer = neo_buffer
