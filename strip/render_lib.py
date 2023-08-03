import random
import strip.neopixel_provider as neo


def get_random_callback():
    i = random.randint(0, 1)
    if i == 0:
        return transition_left_to_right
    elif i == 1:
        return transition_right_to_left


def transition_left_to_right(neo_buffer, effect_cycle_index, effect_state, is_consecutive):
    pixel_index = effect_cycle_index
    effect_state_update = 'RUN'

    if effect_state == 'START':
        pixel_index = 0

    render_at_index(neo_buffer, pixel_index)

    if pixel_index == neo.pixels.n-1:
        effect_state_update = "START" if is_consecutive else "STOP"

    return pixel_index + 1, effect_state_update


def transition_right_to_left(neo_buffer, effect_cycle_index, effect_state, is_consecutive):
    pixel_index = effect_cycle_index
    effect_state_update = 'RUN'

    if effect_state == 'START':
        pixel_index = neo.pixels.n-1

    render_at_index(neo_buffer, pixel_index)
    if pixel_index == 0:
        effect_state_update = "START" if is_consecutive else "STOP"

    return pixel_index - 1, effect_state_update


def set_brightness(value):
    if (value != neo.pixels._brightness):
        neo.pixels.brightness = value
        neo.pixels.show()


def render_at_index(neo_buffer, pixel_index):
    rgbw = neo_buffer[pixel_index]

    neo.pixels[pixel_index] = ((rgbw.red, rgbw.green, rgbw.blue, rgbw.white))
    neo.pixels.show()
