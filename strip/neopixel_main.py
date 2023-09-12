import time
from functools import reduce
import random
import strip.effect_lib as effects
import strip.render_lib as render
from utils import log, ColorRgbw, SystemState, ShowType, CycleState


def loop_forever(state: SystemState) -> None:
    render_cycle_list: list[render.RenderCycle] = render.render_cycle_factory()
    effect_list: list[effects.BufferBuilder] = effects.effect_factory(state)

    effect_class: effects.BufferBuilder = get_effect(state, effect_list)
    render_state: CycleState = CycleState.STOP
    render_class: render.RenderCycle = render_cycle_list[random.randint(
        0, len(render_cycle_list)-1)]

    neo_buffer: list[ColorRgbw] = effects.black_color()

    log.info('Neopixel start')

    while True:

        if is_render_interrupted(state):
            render_state = CycleState.START

        log.debug('Neopixel: Show Type: %s Effect State: %s',
                  state.show_type,  render_state)

        # set brightness
        render.set_brightness(state.brightness)

        if render_state != CycleState.STOP:

            if render_state == CycleState.START:  # get build buffer when a new render cycle start
                effect_class = get_effect(state, effect_list)
                neo_buffer = get_buffer(state, effect_class)

                render_class = render_cycle_list[random.randint(
                    0, len(render_cycle_list)-1)]
                render_class.render_firs_pixel(
                    neo_buffer, effect_class.is_consecutive)
                render_state = render_class.get_render_state()
            else:
                render_class.render_next_pixel(
                    neo_buffer, effect_class.is_consecutive)
                render_state = render_class.get_render_state()

            # sleep time on active render between pixels
            time.sleep(state.wait)

        else:
            log.info('Neopixel finished with task waiting to trigger')
            with state.lock:
                state.loop_sleep_event.set()
            state.wake_up_event.wait()
            with state.lock:
                state.wake_up_event.clear()


def is_render_interrupted(state) -> bool:
    if state.render_interrupt_event.is_set():
        with state.lock:  # TODO integrate to SystemState
            state.render_interrupt_event.clear()
        return True
    return False


def get_buffer(state: SystemState, effect_class: effects.BufferBuilder) -> list[ColorRgbw]:
    if state.main_switch == 'OFF':  # handle off state
        return effects.black_color()

    return effect_class.build_buffer()


def get_effect(state: SystemState, effect_list: list[effects.BufferBuilder]) -> effects.BufferBuilder:
    return reduce(lambda result, element: find_effect_class(
        result, element, state.show_type), effect_list)


def find_effect_class(result, element: effects.BufferBuilder, show_type: ShowType):
    if element.name == show_type:
        result = element
        return result

    return result
