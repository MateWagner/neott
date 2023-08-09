from collections import namedtuple


ColorRgbw = namedtuple(
    'Color_rgbw', ['red', 'green', 'blue', 'white'], defaults=[0, 0, 0, 0])

default_color = ColorRgbw(255, 125, 255,)

NeopixelControls = namedtuple('Variables', [
    'main_switch',
    'show_type',
    'effect_state',
    'wait',
    'dec_rgbw',
    'hex_rgb',
    'brightness',],
    defaults=[
        'OFF',
        'COLOR',
        'STOP',
        0.1,
        default_color,
        '#ff80ff',
        1
])


EffectControls = namedtuple('RunVariables', [
    'effect_cycle_index',
    'previous_main_switch_state',
    'wheel_pos',
    'render_callback',],
    defaults=[
        0,
        0,
        0,
        None,
])


class NeopixelControl:
    def __init__(self, lock):
        self.lock = lock
        self.main_switch = 'OFF'
        self.show_type = 'COLOR'
        self.wait = 0.1
        self.hex_rgb = "#ff80ff"
        self.brightness = 1
        self.mqtt_message_callback = None
        self.websocket_message_callback = None


class EffectControl:
    def __init__(self, render_callback):
        self.effect_cycle_index = 0
        self.previous_main_switch_state = 0
        self.wheel_pos = 0
        self.render_callback = render_callback
        self.effect_state = "STOP"
