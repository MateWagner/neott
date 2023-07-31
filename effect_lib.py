import time
import random
import neopixel_provider as neo
import config_parser

# import variables as v
# from color import Color


def random_transition(red, green, blue, white, hold):
    i = random.randint(0, 1)
    if i == 0:
        transition_left_to_right(red, green, blue, white, hold)
    elif i == 1:
        transition_right_to_left(red, green, blue, white, hold)


def transition_left_to_right(red, green, blue, white, hold):
    for i in range(config_parser.NUM_PIXEL):
        neo.pixels[i] = ((red, green, blue, white))
        neo.pixels.show()
        time.sleep(hold)


def transition_right_to_left(red, green, blue, white, hold):
    for i in range(config_parser.NUM_PIXEL-1, -1, -1):
        neo.pixels[i] = ((red, green, blue, white))
        neo.pixels.show()
        time.sleep(hold)


def brightness(brightness):
    neo.pixels.brightness = brightness
    neo.pixels.show()


def rainbow_cycle(wheel, hold):
    for i in range(config_parser.NUM_PIXEL):
        pixel_index = (i * 256 // neo.num_pixels) + wheel
        neo.pixels[i] = wheel(pixel_index & 255)
    neo.pixels.show()
    time.sleep(hold)
    if wheel == 255:
        wheel = 0

    return (wheel+1)


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
    return (red, green, blue, 0)
