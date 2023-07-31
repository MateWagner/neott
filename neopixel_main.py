# pylint: disable=invalid-name
import time
import effect_lib as e

# main_switch = 0
# show = 'Color'
# effect_state = "STOP"
# wait = 0.1
# previous_state = 0
# red = 255
# green = 125
# blue = 255
# white = 0
# v_hex = '#ff80ff'
# pix_num = 0
# brightness = 1
# wheel = 0
# brightness_state = 1
# effect_state = False
# previous_state = 0
# brightness_state = 1


def update_variables(message_queue, variables):
    for topic_name, value in message_queue.get().items():
        variables[topic_name] = value

    message_queue.task_done()


def loop_forever(message_queue):
    variables = {
        "main_switch": 0,
        "show": 'Color',
        "effect_state": False,
        "wait": 0.1,
        "red": 255,
        "green": 125,
        "blue": 255,
        "white": 0,
        "v_hex": '#ff80ff',
        "pix_num": 0,
        "brightness": 1,
        "wheel": 0,
        "previous_state": 0,
        "brightness_state": 1
    }
    while True:
        if not message_queue.empty():
            update_variables(message_queue, variables)

        if variables.get('main_switch') == 0 and variables.get('previous_state') == 1:
            e.random_transition(0, 0, 0, 0, variables.get('wait'))
            variables['effect_state'] = False
            variables['previous_state'] = 0

        elif variables.get('main_switch') == 1:
            variables['previous_state'] = 1

            if variables.get('show') == "solid_color" and variables.get('effect_state') is True:
                e.random_transition(variables.get('red'), variables.get('green'), variables.get(
                    'blue'), variables.get('white'), variables.get('wait'))
                print('update')
                variables['effect_state'] = False

            if variables.get('show') == 'rainbow':
                variables['wheel'] = e.rainbow_cycle(
                    variables.get('wheel'), variables.get('wait'))
            # elif v.variables.get('show') == 'Test':
                # v.wheel = e.test(v.wheel)

        if variables.get('brightness') != variables.get('brightness_state'):
            e.brightness(variables.get('brightness'))
            variables['brightness_state'] = variables.get('brightness')

        # put the thread in sleep when no thing to do
        if variables['effect_state'] is False and variables.get('show') == 'Color' \
                or variables.get('main_switch') == 0:
            time.sleep(3)
