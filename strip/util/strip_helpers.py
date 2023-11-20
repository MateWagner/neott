from utils import ColorRgbw


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
