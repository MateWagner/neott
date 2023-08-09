import utils.config_parser as config_parser
import utils.log_provider as log
from utils.data_types import SystemState


def main_switch(client, state: SystemState, message):
    state.main_switch = message.payload.decode('utf-8').upper()
    acknowledge_message(client, message, state)


def solid_color(client, state: SystemState, message):
    state.hex_rgb = message.payload.decode('utf-8')
    acknowledge_message(client, message, state)


def show_type(client, state: SystemState, message):
    state.show_type = message.payload.decode('utf-8').upper()
    acknowledge_message(client, message, state)


def wait(client, state: SystemState, message):
    state.wait = float(message.payload)
    acknowledge_message(client, message, state)


def brightness(client, state: SystemState, message):
    state.brightness = float(message.payload)
    acknowledge_message(client, message, state)


TOPIC_CALLBACK_MAP = {
    'main_switch': main_switch,
    'solid_color': solid_color,
    'show_type': show_type,
    'wait': wait,
    'brightness': brightness
}


def acknowledge_message(client, message, state: SystemState):
    log.arrived_message(message)
    state.send_message_to_websocket(message)
    client.publish(message.topic + '/state', message.payload, retain=True)


# update the Broker with the default values to the state topic with retain flag, when the program start
def initial_value_publisher(mqtt_client, state):
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}main_switch/state',
                        str(state.main_switch), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}solid_color/state',
                        str(state.hex_rgb), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}show_type/state',
                        str(state.show_type), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}wait/state',
                        str(state.wait), retain=True)
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}brightness/state',
                        str(state.brightness), retain=True)
