import board
import neopixel
import config_parser

pixel_pin = getattr(board, config_parser.PIN)
num_pixels = config_parser.NUM_PIXEL
ORDER = getattr(neopixel, config_parser.ORDER)

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)
