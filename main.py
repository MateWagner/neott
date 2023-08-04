from threading import Thread
from queue import Queue
from utils.log_provider import log
import strip.neopixel_main as neopixel_main
from mqtt.mqtt_client import mqttc

log.info("Threads loading")

message_queue = Queue()

mqtt = Thread(target=mqttc.loop_forever, args=(1,))
neopixel = Thread(target=neopixel_main.loop_forever, args=(message_queue,))

mqtt.start()
mqttc.user_data_set(message_queue)

neopixel.start()
