from utils import config, SystemState, arrived_message


def main_switch(_client, state: SystemState, message):
    state.main_switch = message.payload.decode('utf-8').upper()
    arrived_message(message)


def hex_rgb(_client, state: SystemState, message):
    state.hex_rgb = message.payload.decode('utf-8')
    arrived_message(message)


def show_type(_client, state: SystemState, message):
    state.show_type = message.payload.decode('utf-8').upper()
    arrived_message(message)


def wait(_client, state: SystemState, message):
    state.wait = float(message.payload)
    arrived_message(message)


def brightness(_client, state: SystemState, message):
    state.brightness = float(message.payload)
    arrived_message(message)


TOPIC_CALLBACK_MAP = {
    'main_switch': main_switch,
    'hex_rgb': hex_rgb,
    'show_type': show_type,
    'wait': wait,
    'brightness': brightness
}


# update the Broker with the default values to the state topic with retain flag, when the program start
def initial_value_publisher(mqtt_client, state):
    mqtt_client.publish(f'{config.ROOT_TOPIC}main_switch/state',
                        str(state.main_switch.name), retain=True)
    mqtt_client.publish(f'{config.ROOT_TOPIC}hex_rgb/state',
                        str(state.hex_rgb), retain=True)
    mqtt_client.publish(f'{config.ROOT_TOPIC}show_type/state',
                        str(state.show_type.name), retain=True)
    mqtt_client.publish(f'{config.ROOT_TOPIC}wait/state',
                        str(state.wait), retain=True)
    mqtt_client.publish(f'{config.ROOT_TOPIC}brightness/state',
                        str(state.brightness), retain=True)
