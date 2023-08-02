import re
import utils.config_parser as config_parser
from utils.log_provider import arrived_message
from utils.data_types import ColorRgbw, NeopixelControl


def main_switch(client, message_queue, message):
    message_queue.put(
        {
            'main_switch': message.payload.decode('utf-8'),
            'effect_state': 'START',
        }
    )
    acknowledge_massage(client, message)


def solid_color(client, message_queue, message):
    string_payload = message.payload.decode('utf-8')
    red = 0
    green = 0
    blue = 0
    white = 0

    if string_payload == '#FFFFFF' and 'W' in config_parser.ORDER.upper():
        white = 255
    else:
        red = hex_to_rgb(string_payload)[0]
        green = hex_to_rgb(string_payload)[1]
        blue = hex_to_rgb(string_payload)[2]

    message_queue.put(
        {
            'dec_rgbw': ColorRgbw(red, green, blue, white),
            'effect_state': 'START',
        }
    )
    acknowledge_massage(client, message)


def show_type(client, message_queue, message):
    message_queue.put(
        {
            'show_type': message.payload.decode('utf-8'),
            'effect_state': 'START'
        }
    )
    acknowledge_massage(client, message)


def wait(client, message_queue, message):
    message_queue.put({'wait': float(message.payload)})
    acknowledge_massage(client, message)


def brightness(client, message_queue, message):
    message_queue.put({'brightness': float(message.payload)})
    acknowledge_massage(client, message)


TOPIC_CALLBACK_MAP = {
    'main_switch': main_switch,
    'solid_color': solid_color,
    'show_type': show_type,
    'wait': wait,
    'brightness': brightness
}


def hex_to_rgb(hx, hsl=False):
    """Converts a HEX code into RGB or HSL.
    Args:
        hx (str): Takes both short as well as long HEX codes.
        hsl (bool): Converts the given HEX code into HSL value if True.
    Return:
        Tuple of length 3 consisting of either int or float values.
    Raise:
        ValueError: If given value is not a valid HEX code."""
    # Thank you to: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(int(hx[i]*2, 16) / div if div else
                         int(hx[i]*2, 16) for i in (1, 2, 3))
        return tuple(int(hx[i:i+2], 16) / div if div else
                     int(hx[i:i+2], 16) for i in (1, 3, 5))
    raise ValueError(f'"{hx}" is not a valid HEX code.')


def acknowledge_massage(client, message):
    arrived_message(message)
    client.publish(message.topic + '/state', message.payload, retain=True)


# update the Broker with the default values to the state topic with retain flag, when the program start
def initial_value_publisher(mqtt_client):
    initial_values = NeopixelControl()
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}main_switch/state',
                        str(initial_values.main_switch), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}solid_color/state',
                        str(initial_values.hex_rgb), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}show_type/state',
                        str(initial_values.show_type), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}wait/state',
                        str(initial_values.wait), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}brightness/state',
                        str(initial_values.brightness), retain=True)
