import random
import strip.neopixel_provider as neo


def get_random_callback():
    i = random.randint(0, 1)
    if i == 0:
        return transition_left_to_right
    elif i == 1:
        return transition_right_to_left


def transition_left_to_right(effect_control, is_consecutive):
    effect_state_update = 'RUN'

    if effect_control.effect_state == 'START':
        effect_control.effect_cycle_index = 0

    render_at_index(effect_control)

    if effect_control.effect_cycle_index == neo.pixels.n-1:
        effect_state_update = "START" if is_consecutive else "STOP"

    effect_control.effect_state = effect_state_update
    effect_control.effect_cycle_index += 1


def transition_right_to_left(effect_control, is_consecutive):
    effect_state_update = 'RUN'

    if effect_control.effect_state == 'START':
        effect_control.effect_cycle_index = neo.pixels.n-1

    render_at_index(effect_control)

    if effect_control.effect_cycle_index == 0:
        effect_state_update = "START" if is_consecutive else "STOP"

    effect_control.effect_state = effect_state_update
    effect_control.effect_cycle_index -= 1


def set_brightness(value):
    if (value != neo.pixels.brightness):
        neo.pixels.brightness = value
        neo.pixels.show()


def render_at_index(effect_control):
    rgbw = effect_control.neo_buffer[effect_control.effect_cycle_index]

    neo.pixels[effect_control.effect_cycle_index] = (
        (rgbw.red, rgbw.green, rgbw.blue, rgbw.white))
    neo.pixels.show()
