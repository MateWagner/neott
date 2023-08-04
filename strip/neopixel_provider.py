import board
import neopixel
import utils.config_parser as config

pixel_pin = getattr(board, config.PIN)
num_pixels = config.NUM_PIXEL
ORDER = getattr(neopixel, config.ORDER)

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)
