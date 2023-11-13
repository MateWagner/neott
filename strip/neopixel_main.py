import time
import random
from utils import log, ColorRgbw, SystemState, ShowType, CycleState, \
    MainSwitchState, NeoLoopControl, RenderCycle, BufferBuilder
from .render_lib import render_cycle_factory, set_brightness
from .effect_lib import drew_off, effect_factory


def start(state: SystemState) -> None:
    log.info('Neopixel start')
    loop_control = NeoLoopControl(render_cycle_factory(),
                                  effect_factory(state), drew_off())

    while True:
        loop_forever(state, loop_control)


def loop_forever(state: SystemState, control: NeoLoopControl) -> None:
    if state.is_render_interrupted():
        control.render_state = CycleState.START

    set_brightness(state.brightness)

    is_render_cycle_start = control.render_state is CycleState.START
    has_new_effect_in_use = state.show_type is not control.current_effect.name

    log.debug('Neopixel: Show Type: %s, Effect State: %s, Effect Class %s',
              state.show_type,  control.render_state, type(control.current_effect))

    if has_new_effect_in_use:
        control.current_effect = get_effect(
            state.show_type, control.effect_list)

    if is_render_cycle_start:
        control.neo_buffer = drew_new_buffer(
            state.main_switch, control.current_effect)

        control.current_renderer = get_random_render_cycle(
            control.render_cycle_list)
        control.current_renderer.render_firs_pixel(control.neo_buffer)

    else:
        render_next_pixel(state.main_switch,
                          control.current_renderer,
                          control.neo_buffer,
                          control.is_effect_consecutive()
                          )

    control.render_state = control.current_renderer.get_render_state()

    # sleep time on active render, between pixels
    time.sleep(state.wait)

    is_render_cycle_stopped = control.render_state is CycleState.STOP
    if is_render_cycle_stopped:
        log.debug('Neopixel finished with task waiting to trigger')
        state.set_loop_is_stopped_event()
        state.wake_up_event.wait()
        state.clear_wakeup_event()


def render_next_pixel(main_switch: MainSwitchState, render: RenderCycle,
                      neo_buffer: list[ColorRgbw], is_consecutive: bool) -> None:
    if main_switch is MainSwitchState.OFF:
        render.render_next_pixel(neo_buffer)
    else:
        render.render_next_pixel(neo_buffer, is_consecutive)


def drew_new_buffer(main_switch: MainSwitchState, current_effect: BufferBuilder) -> list[ColorRgbw]:
    if main_switch is MainSwitchState.OFF:
        return drew_off()
    return current_effect.drew_buffer()


def get_random_render_cycle(render_cycle_list: list[RenderCycle]) -> RenderCycle:
    return random.choice(render_cycle_list)


def get_effect(show_type: ShowType, effect_list: list[BufferBuilder]) -> BufferBuilder:
    return next((effect for effect in effect_list if effect.name == show_type), effect_list[0])
