import time
import strip.effect_lib as e
from utils.config_parser import NUM_PIXEL
from utils.log_provider import log
from utils.data_types import NeopixelControl, ColorRgbw, EffectControl


def loop_forever(message_queue):
    log.info('Neopixel start')

    neopixel_control = NeopixelControl()
    effect_control = EffectControl()
    neo_buffer = fill_neo_buffer(neopixel_control)

    while True:

        if not message_queue.empty():
            neopixel_control = update_variables(
                message_queue, neopixel_control)

        log.debug('Neopixel: Show Type: %s Effect State: %s render on Index: %s',
                  neopixel_control.show_type, neopixel_control.effect_state, effect_control.effect_cycle_index)

        # set brightness
        if neopixel_control.brightness != effect_control.brightness_state:
            effect_control = effect_control._replace(
                brightness_state=neopixel_control.brightness)
            e.brightness(neopixel_control.brightness)

        if neopixel_control.effect_state != 'STOP':

            # handle solid color or off
            if neopixel_control.show_type == 'COLOR' or neopixel_control.main_switch == 'OFF':
                if neopixel_control.effect_state == 'START':
                    effect_control = get_random_callback(effect_control)
                    neo_buffer = fill_neo_buffer(neopixel_control)

                new_index, state = effect_control.render_callback(
                    neo_buffer, effect_control.effect_cycle_index, neopixel_control.effect_state)

                effect_control = effect_control._replace(
                    effect_cycle_index=new_index)
                neopixel_control = neopixel_control._replace(
                    effect_state=state)

            if neopixel_control.show_type == 'RAINBOW' and neopixel_control.main_switch == 'ON':
                if neopixel_control.effect_state == 'START':
                    effect_control = get_random_callback(effect_control)
                    neo_buffer, wheel_pos = e.rainbow_cycle(
                        neo_buffer, effect_control.wheel_pos)

                    effect_control = effect_control._replace(
                        wheel_pos=wheel_pos)

                new_index, state = effect_control.render_callback(
                    neo_buffer, effect_control.effect_cycle_index, neopixel_control.effect_state)

                effect_control = effect_control._replace(
                    effect_cycle_index=new_index)
                if state == 'STOP':
                    state = 'START'
                neopixel_control = neopixel_control._replace(
                    effect_state=state)

            time.sleep(neopixel_control.wait)

        else:
            time.sleep(3)


def update_variables(message_queue, neopixel_control):
    variables_copy = neopixel_control._asdict()
    for topic_name, value in message_queue.get().items():
        print(topic_name, value)
        variables_copy[topic_name] = value

    message_queue.task_done()
    return NeopixelControl(**variables_copy)


def fill_buffer_with_one_color(color_values):
    return [color_values for i in range(NUM_PIXEL)]


def fill_neo_buffer(neopixel_control):
    return (fill_buffer_with_one_color(ColorRgbw())
            if neopixel_control.main_switch == 'OFF'
            else fill_buffer_with_one_color(neopixel_control.dec_rgbw))


def get_random_callback(effect_control):
    return effect_control._replace(
        render_callback=e.get_random_render_callback())
