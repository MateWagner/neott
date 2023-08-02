from collections import namedtuple


ColorRgbw = namedtuple(
    'Color_rgbw', ['red', 'green', 'blue', 'white'], defaults=[0, 0, 0, 0])

default_color = ColorRgbw(255, 80, 255,)

NeopixelControl = namedtuple('Variables', [
    'main_switch',
    'show_type',
    'effect_state',
    'wait',
    'dec_rgbw',
    'brightness',],
    defaults=[
        'OFF',
        'COLOR',
        'STOP',
        0.1,
        default_color,
        1
])


EffectControl = namedtuple('RunVariables', [
    'effect_cycle_index',
    'brightness_state',
    'previous_main_switch_state',
    'wheel_pos',
    'render_callback',],
    defaults=[
        0,
        1.0,
        0,
        0,
        None,
])
