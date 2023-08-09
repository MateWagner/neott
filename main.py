from threading import Thread, Lock
from queue import Queue
from utils.log_provider import log
from utils.data_types import NeopixelControl
import web.flask_main as web
import strip.neopixel_main as neopixel_main
from mqtt.mqtt_client import start_loop, mqttc

log.info("Threads loading")
lock = Lock()
state = NeopixelControl(lock)

mqtt = Thread(target=start_loop, args=(state,))
neopixel = Thread(target=neopixel_main.loop_forever, args=(state,))
flask = Thread(target=web.run_flask, args=(state,))

mqtt.start()
mqttc.user_data_set(state)
neopixel.start()
flask.start()
