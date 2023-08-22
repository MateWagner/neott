import utils.config_parser as config_parser
import utils.log_provider as log
from utils.data_types import SystemState


def main_switch(_client, state: SystemState, message):
    state.main_switch = message.payload.decode('utf-8').upper()
    log.arrived_message(message)


def hex_rgb(_client, state: SystemState, message):
    state.hex_rgb = message.payload.decode('utf-8')
    log.arrived_message(message)


def show_type(_client, state: SystemState, message):
    state.show_type = message.payload.decode('utf-8').upper()
    log.arrived_message(message)


def wait(_client, state: SystemState, message):
    state.wait = float(message.payload)
    log.arrived_message(message)


def brightness(_client, state: SystemState, message):
    state.brightness = float(message.payload)
    log.arrived_message(message)


TOPIC_CALLBACK_MAP = {
    'main_switch': main_switch,
    'hex_rgb': hex_rgb,
    'show_type': show_type,
    'wait': wait,
    'brightness': brightness
}


# update the Broker with the default values to the state topic with retain flag, when the program start
def initial_value_publisher(mqtt_client, state):
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}main_switch/state',
                        str(state.main_switch), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}hex_rgb/state',
                        str(state.hex_rgb), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}show_type/state',
                        str(state.show_type), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}wait/state',
                        str(state.wait), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}brightness/state',
                        str(state.brightness), retain=True)
