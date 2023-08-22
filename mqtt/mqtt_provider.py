import paho.mqtt.client as mqtt
from utils.log_provider import log
import utils.config_parser as config_parser
from mqtt.mqtt_bridge import TOPIC_CALLBACK_MAP, initial_value_publisher
from utils.data_types import SystemState


def on_connect(_client, _user_data, _flags, rc):
    messages = {
        0: 'Connection successful',
        1: 'Connection refused - incorrect protocol version',
        2: 'Connection refused - invalid client identifier',
        3: 'Connection refused - server unavailable',
        4: 'Connection refused - bad username or password',
        5: 'Connection refused - not authorized',
    }
    log.info('Connection result code %s', messages.get(rc))


def on_message(client, _user_data, msg):
    log.debug('On topic: %s arrived: %s topic without callback!',
              msg.topic, msg.payload)

    # return the msg to the status topic with retain flag to keep connected clients sync
    client.publish(msg.topic + '/state', msg.payload, retain=True)


def on_publish(_client, _user_data, mid):
    log.debug('Publish mid: %s', mid)


def on_subscribe(_client, _user_data, mid, granted_qos):
    log.info('Subscribed: %s, granted qos: %s', mid, granted_qos)


def on_log(_client, _user_data, _level, buf):
    print(buf)


def subscribe_to_topic_loop(client):
    for topic in TOPIC_CALLBACK_MAP:
        client.subscribe(f'{config_parser.ROOT_TOPIC}{topic}')


def register_topic_callbacks(client):
    for topic_name, callback in TOPIC_CALLBACK_MAP.items():
        client.message_callback_add(
            config_parser.ROOT_TOPIC + topic_name, callback)


def start_loop(state: SystemState):
    # update the Broker with the default values to the state topic with retain flag, when the program start
    initial_value_publisher(mqtt_client, state)
    state.add_message_callback(send_update_to_broker)
    mqtt_client.user_data_set(state)
    mqtt_client.loop_forever(1)


def send_update_to_broker(topic, message) -> None:
    mqtt_client.publish(f'{config_parser.ROOT_TOPIC}{topic}/state',
                        message, retain=True)


def mqtt_client_init():
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    # Uncomment to enable debug messages
    # mqttc.on_log = on_log

    log.info('MQTT Client connecting...')

    client.connect(config_parser.HOST, config_parser.PORT,
                   config_parser.KEEP_ALIVE)

    # Subscribe loop
    subscribe_to_topic_loop(client)
    register_topic_callbacks(client)

    return client


mqtt_client = mqtt_client_init()
