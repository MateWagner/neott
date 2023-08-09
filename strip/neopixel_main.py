import time
import strip.effect_lib as effects
import strip.render_lib as render
from utils.log_provider import log
from utils.data_types import NeopixelControls, ColorRgbw, EffectControl
from utils.value_converter import get_rgbw


def loop_forever(state):
    log.info('Neopixel start')

    effect_control = EffectControl(
        render.get_random_callback(), fill_neo_buffer(state))

    while True:

        process_event_and_start_effect(state, effect_control)

        log.debug('Neopixel: Show Type: %s Effect State: %s render on Index: %s',
                  state.show_type,  effect_control.effect_state, effect_control.effect_cycle_index)

        # set brightness
        render.set_brightness(state.brightness)

        if effect_control.effect_state != 'STOP':

            if state.show_type == 'COLOR' or state.main_switch == 'OFF':
                handle_solid_color_and_off(state, effect_control)

            # if neopixel_control.show_type == 'RAINBOW' and neopixel_control.main_switch == 'ON':
            #     neopixel_control, effect_control, neo_buffer = handle_rainbow_cycle(
            #         neopixel_control, effect_control, neo_buffer)

            # sleep time on active render between pixels
            time.sleep(state.wait)

        else:
            #  TODO TEST state.trigger_event.wait()  process_event_and_start_effect(state, effect_control) should stop the loop and put in sleep while the signal is arriving
            time.sleep(3)


def process_event_and_start_effect(state, effect_control):
    if state.trigger_event.is_set():
        with state.lock:
            state.trigger_event.clear()
        effect_control.effect_state = 'START'


# def handle_rainbow_cycle(neopixel_control, effect_control, neo_buffer):
#     buffer_copy = copy.deepcopy(neo_buffer)
#     if neopixel_control.effect_state == 'START':
#         effect_control = get_random_callback(effect_control)
#         buffer_copy, wheel_pos = effects.rainbow_cycle(
#             buffer_copy, effect_control.wheel_pos)
#         effect_control = effect_control._replace(
#             wheel_pos=wheel_pos)

#     neopixel_control, effect_control = render_next_pixel(
#         neopixel_control, effect_control, buffer_copy, True)

#     return neopixel_control, effect_control, buffer_copy


def handle_solid_color_and_off(state, effect_control):
    if effect_control.effect_state == 'START':
        effect_control.render_callback = render.get_random_callback()
        effect_control.neo_buffer = fill_neo_buffer(state)

    render_next_pixel(effect_control, False)


def render_next_pixel(effect_control, is_consecutive):
    effect_control.render_callback(effect_control, is_consecutive)


def update_variables(message_queue, neopixel_control):
    variables_copy = neopixel_control._asdict()
    for topic_name, value in message_queue.get().items():
        log.info('Update arrived on: %s topic, value: %s', topic_name, value)
        variables_copy[topic_name] = value

    message_queue.task_done()
    return NeopixelControls(**variables_copy)


def fill_neo_buffer(state):
    return (effects.fill_with_one_color(ColorRgbw())
            if state.main_switch == 'OFF'
            else effects.fill_with_one_color(get_rgbw(state.hex_rgb)))
