import random
from pytest_mock import MockerFixture
from pytest import MonkeyPatch
from utils import SystemState, MessagingSystem, NeoLoopControl, CycleState, MainSwitchState, ShowType
import strip.effect_lib as effect_lib
import strip.render_lib as render_lib
from strip.neopixel_main import loop_forever, get_effect, get_random_render_cycle

# sudo python -m pytest --cov=strip -v tests/


def test_interrupt_render_state_turn_to_run(monkeypatch: MonkeyPatch):
    msgs = MessagingSystem()
    state = SystemState(msgs)
    monkeypatch.setattr(state, 'is_render_interrupted', lambda: True)
    effect_list = effect_lib.effect_factory(state)
    render_list = render_lib.render_cycle_factory()
    control = NeoLoopControl(render_list, effect_list, effect_lib.drew_off())
    loop_forever(state, control)
    assert control.render_state is CycleState.RUN


def test_render_is_interrupted_neo_buffer_changes_on_on_state(monkeypatch: MonkeyPatch):
    msgs = MessagingSystem()
    state = SystemState(msgs)
    monkeypatch.setattr(state, 'is_render_interrupted', lambda: True)
    monkeypatch.setattr(state, '_main_switch', MainSwitchState.ON)
    effect_list = effect_lib.effect_factory(state)
    render_list = render_lib.render_cycle_factory()
    start_buffer = effect_lib.drew_off()
    control = NeoLoopControl(render_list, effect_list, start_buffer)
    loop_forever(state, control)

    assert start_buffer[0].red is not control.neo_buffer[0].red
    assert start_buffer[0].green is not control.neo_buffer[0].green
    assert start_buffer[0].blue is not control.neo_buffer[0].blue


def test_show_type_default_color(monkeypatch: MonkeyPatch):
    msgs = MessagingSystem()
    state = SystemState(msgs)
    monkeypatch.setattr(state, 'is_render_interrupted', lambda: True)
    monkeypatch.setattr(state, '_main_switch', MainSwitchState.ON)
    effect_list = effect_lib.effect_factory(state)
    render_list = render_lib.render_cycle_factory()
    start_buffer = effect_lib.drew_off()
    control = NeoLoopControl(render_list, effect_list, start_buffer)
    loop_forever(state, control)

    assert control.current_effect.name is ShowType.COLOR


def test_show_type_change_to_rainbow(monkeypatch: MonkeyPatch):
    msgs = MessagingSystem()
    state = SystemState(msgs)
    monkeypatch.setattr(state, 'is_render_interrupted', lambda: True)
    monkeypatch.setattr(state, '_main_switch', MainSwitchState.ON)
    monkeypatch.setattr(state, '_show_type', ShowType.RAINBOW)
    effect_list = effect_lib.effect_factory(state)
    render_list = render_lib.render_cycle_factory()
    start_buffer = effect_lib.drew_off()
    control = NeoLoopControl(render_list, effect_list, start_buffer)
    loop_forever(state, control)

    assert control.current_effect.name is ShowType.RAINBOW


def test_get_effect_from_list_with_show_type():
    msgs = MessagingSystem()
    state = SystemState(msgs)
    effect_list = effect_lib.effect_factory(state)
    assert get_effect(ShowType.RAINBOW, effect_list).name is ShowType.RAINBOW


def test_get_random_render_cycle(monkeypatch):
    render_list = render_lib.render_cycle_factory()
    expected = render_list[0]
    monkeypatch.setattr(random, 'choice', lambda _: expected)
    assert get_random_render_cycle(render_list) is expected


def test_when_cycle_stop_then_wait_to_wakeup(mocker: MockerFixture, monkeypatch: MonkeyPatch):
    msgs = MessagingSystem()
    state = SystemState(msgs)
    effect_list = effect_lib.effect_factory(state)
    render_list = render_lib.render_cycle_factory()
    control = NeoLoopControl(render_list, effect_list, effect_lib.drew_off())

    mocker.patch.object(state.wake_up_event, 'wait')
    # monkeypatch.setattr(state.wake_up_event, 'wait', lambda: False)

    loop_forever(state, control)
    assert control.render_state is CycleState.STOP
