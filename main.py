from threading import Thread
from queue import Queue
from log_provider import log
import neopixel_main
from mqtt_client import mqtt_client

log.info("Threads loading")

message_queue = Queue()

mqtt = Thread(target=mqtt_client.loop_forever, args=(1,))
neopixel = Thread(target=neopixel_main.loop_forever, args=(message_queue,))

mqtt.start()
mqtt_client.user_data_set(message_queue)

neopixel.start()
