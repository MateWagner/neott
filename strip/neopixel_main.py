import time
from utils import log, SystemState, NeoLoopControl
from .render_lib import set_brightness, render_cycle_factory
from .effect_lib import effect_factory, TurnOff


def start(state: SystemState) -> None:
    log.info('Neopixel start')

    loop_control = NeoLoopControl(effect_factory(
        state), TurnOff(render_cycle_factory(), state))

    while True:
        loop_forever(state, loop_control)


def loop_forever(state: SystemState, control: NeoLoopControl) -> None:

    set_brightness(state.brightness)

    has_new_effect_in_use = not control.current_effect.is_name_match(
        state.show_type)

    # log.debug('Neopixel: Show Type: %s, Effect State: %s, Effect Class %s',
    #           state.show_type,  control.render_state, type(control.current_effect))

    if has_new_effect_in_use:
        control.set_new_effect(state.show_type)

    if state.is_on:
        control.current_effect.render()
    else:
        control.turn_off_effect.render()

    # sleep time on active render, between pixels
    time.sleep(state.wait)

    if control.is_render_finished:
        log.debug('Neopixel finished with task waiting to trigger')
        state.set_loop_is_stopped_event()
        state.wake_up_event.wait()
        state.clear_wakeup_event()
