import paho.mqtt.client as mqtt
from log_provider import log
import config_parser
from utils.mqtt_bridge import TOPIC_CALLBACK_MAP, initial_value_publisher


def on_connect(client, userdata, flags, rc):
    # TODO 0: Connection successful 1: Connection refused - incorrect protocol version 2: Connection refused - invalid client identifier 3: Connection refused - server unavailable 4: Connection refused - bad username or password 5: Connection refused - not authorised 6-255: Currently unused.
    #  print("Connection returned result: "+connack_string(rc))
    log.info("Connection result code " + str(rc))


def on_message(client, userdata, msg):
    log.debug(
        f'On topic: {msg.topic} arrived: {msg.payload} topic without callback!'
    )

    # return the msg to the status topic with retain flag to keep the app update when a client connected
    client.publish(msg.topic + '/state', msg.payload, retain=True)


def on_publish(client, userdata, mid):
    log.debug(f'Publish mid: {mid}')


def on_subscribe(client, userdata, mid, granted_qos):
    log.info(f'Subscribed: {mid}, granted qos: {granted_qos}')


def on_log(client, userdata, level, buf):
    print(buf)


def subscribe_loop():
    for topic in TOPIC_CALLBACK_MAP:
        mqtt_client.subscribe(f'{config_parser.ROOT_TOPIC}{topic}')


def register_topic_callbacks(mqtt_client):
    for topic_name, callback in TOPIC_CALLBACK_MAP.items():
        mqtt_client.message_callback_add(
            config_parser.ROOT_TOPIC + topic_name, callback)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqtt_client.on_log = on_log

log.info('MQTT Client connecting...')

mqtt_client.connect(config_parser.HOST, config_parser.PORT,
                    config_parser.KEEP_ALIVE)

# Subscribe loop
subscribe_loop()

register_topic_callbacks(mqtt_client)

# update the Broker with the default values to the state topic with retain flag, when the program start
initial_value_publisher(mqtt_client)
