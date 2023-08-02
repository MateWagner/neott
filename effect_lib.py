import random
import neopixel_provider as neo
from data_types import ColorRgbw


def get_random_render_callback():
    i = random.randint(0, 1)
    if i == 0:
        return transition_left_to_right
    elif i == 1:
        return transition_right_to_left


def transition_left_to_right(neo_buffer, effect_cycle_index, effect_state):
    pixel_index = effect_cycle_index
    if effect_state == 'START':
        pixel_index = 0

    rgbw = neo_buffer[pixel_index]

    neo.pixels[pixel_index] = ((rgbw.red, rgbw.green, rgbw.blue, rgbw.white))
    neo.pixels.show()
    return pixel_index + 1, "STOP" if pixel_index == neo.pixels.n-1 else "RUN"


def transition_right_to_left(neo_buffer, effect_cycle_index, effect_state):
    pixel_index = effect_cycle_index
    if effect_state == 'START':
        pixel_index = neo.pixels.n-1

    rgbw = neo_buffer[pixel_index]

    neo.pixels[pixel_index] = ((rgbw.red, rgbw.green, rgbw.blue, rgbw.white))
    neo.pixels.show()
    return pixel_index - 1, "STOP" if pixel_index == 0 else "RUN"


def brightness(value):
    neo.pixels.brightness = value
    neo.pixels.show()


def rainbow_cycle(neo_buffer, wheel_pos):
    for pixel in range(neo.pixels.n):
        pixel_index = (pixel * 256 // neo.pixels.n) + wheel_pos
        color = wheel(pixel_index & 255)
        neo_buffer[pixel] = color

    return neo_buffer, ((wheel_pos+1) & 255)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        red = green = blue = 0
    elif pos < 85:
        red = int(pos * 3)
        green = int(255 - pos * 3)
        blue = 0
    elif pos < 170:
        pos -= 85
        red = int(255 - pos * 3)
        green = 0
        blue = int(pos * 3)
    else:
        pos -= 170
        red = 0
        green = int(pos * 3)
        blue = int(255 - pos * 3)
    return ColorRgbw(red, green, blue)
