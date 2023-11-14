import re
from .config_parser import ORDER
from .enums import ColorRgbw


def get_rgbw(hex_rgb: str) -> ColorRgbw:
    red = 0
    green = 0
    blue = 0
    white = 0

    if hex_rgb.upper() == '#FFFFFF' and 'W' in ORDER.upper():
        white = 255
    else:
        red = hex_to_rgb(hex_rgb)[0]
        green = hex_to_rgb(hex_rgb)[1]
        blue = hex_to_rgb(hex_rgb)[2]

    return ColorRgbw(red, green, blue, white)


def hex_to_rgb(hx, hsl=False):
    """Converts a HEX code into RGB or HSL.
    Args:
        hx (str): Takes both short as well as long HEX codes.
        hsl (bool): Converts the given HEX code into HSL value if True.
    Return:
        Tuple of length 3 consisting of either int or float values.
    Raise:
        ValueError: If given value is not a valid HEX code."""
    # Thank you to: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(int(hx[i]*2, 16) / div if div else
                         int(hx[i]*2, 16) for i in (1, 2, 3))
        return tuple(int(hx[i:i+2], 16) / div if div else
                     int(hx[i:i+2], 16) for i in (1, 3, 5))
    raise ValueError(f'"{hx}" is not a valid HEX code.')
