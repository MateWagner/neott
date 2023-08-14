import time
import strip.effect_lib as effects
import strip.render_lib as render
from utils.log_provider import log
from utils.data_types import ColorRgbw, EffectControl, SystemState
from utils.value_converter import get_rgbw


def loop_forever(state: SystemState):
    log.info('Neopixel start')

    effect_control = EffectControl(
        render.get_random_callback(), fill_neo_buffer(state))

    while True:

        render_interrupt_event_and_start(state, effect_control)

        log.debug('Neopixel: Show Type: %s Effect State: %s render on Index: %s',
                  state.show_type,  effect_control.effect_state, effect_control.effect_cycle_index)

        # set brightness
        render.set_brightness(state.brightness)

        if effect_control.effect_state != 'STOP':

            if state.show_type == 'COLOR' or state.main_switch == 'OFF':
                handle_solid_color_and_off(state, effect_control)

            if state.show_type == 'RAINBOW' and state.main_switch == 'ON':
                handle_rainbow_cycle(effect_control)

            # sleep time on active render between pixels
            time.sleep(state.wait)

        else:
            log.info('Neopixel finished with task waiting to trigger')
            with state.lock:
                state.loop_sleep_event.set()
            state.wake_up_event.wait()
            with state.lock:
                state.wake_up_event.clear()


def render_interrupt_event_and_start(state, effect_control):
    if state.render_interrupt_event.is_set():
        with state.lock:
            state.render_interrupt_event.clear()
        effect_control.effect_state = 'START'


def handle_rainbow_cycle(effect_control):
    if effect_control.effect_state == 'START':
        effect_control.render_callback = render.get_random_callback()
        effects.rainbow_cycle(effect_control)

    render_next_pixel(effect_control, True)


def handle_solid_color_and_off(state, effect_control):
    if effect_control.effect_state == 'START':
        effect_control.render_callback = render.get_random_callback()
        effect_control.neo_buffer = fill_neo_buffer(state)

    render_next_pixel(effect_control, False)


def render_next_pixel(effect_control, is_consecutive):
    effect_control.render_callback(effect_control, is_consecutive)


def fill_neo_buffer(state):
    return (effects.fill_with_one_color(ColorRgbw())
            if state.main_switch == 'OFF'
            else effects.fill_with_one_color(get_rgbw(state.hex_rgb)))
