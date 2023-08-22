from utils import config, ColorRgbw


def fill_with_one_color(color_values):
    return [color_values for i in range(config.NUM_PIXEL)]


def rainbow_cycle(effect_control):
    for pixel in range(config.NUM_PIXEL):
        pixel_index = (pixel * 256 // config.NUM_PIXEL) + \
            effect_control.wheel_pos
        color = wheel(pixel_index & 255)
        effect_control.neo_buffer[pixel] = color

    effect_control.wheel_pos = ((effect_control.wheel_pos+1) & 255)


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
