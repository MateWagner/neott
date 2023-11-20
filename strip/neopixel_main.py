import time
from utils import log, SystemState, NamedShow, BaseShowType
from .render_lib import set_brightness, render_cycle_factory
from .show_lib import named_show_factory, TurnOff


def start(state: SystemState) -> None:
    log.info('Neopixel start')
    named_show_list = named_show_factory(state)
    off_show = TurnOff(render_cycle_factory(), state)
    while True:
        loop_forever(state, named_show_list, off_show)


def loop_forever(state: SystemState, named_show_list, turn_off) -> None:
    current_show: BaseShowType

    set_brightness(state.brightness)

    if state.is_on:
        current_show = get_current_show(
            named_show_list, state.show_type)
    else:
        current_show = turn_off

    current_show.render()

    # sleep time on active render, between pixels
    time.sleep(state.wait)

    if current_show.is_show_finished:
        log.debug('Neopixel finished with task waiting to trigger')
        state.set_loop_is_stopped_event()
        state.wake_up_event.wait()
        state.clear_wakeup_event()


def get_current_show(named_show_list, show_type) -> NamedShow:
    return next(
        (effect for effect in named_show_list if effect.is_name_match(show_type)), named_show_list[0])
