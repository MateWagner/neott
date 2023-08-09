from threading import Thread, Lock, Event
from utils.log_provider import log
from utils.data_types import SystemState
import web.flask_main as web
import strip.neopixel_main as neopixel_main
from mqtt.mqtt_client import start_loop

log.info("Threads loading")
state = SystemState(Lock(), Event(), Event(), Event())

mqtt = Thread(target=start_loop, args=(state,))
neopixel = Thread(target=neopixel_main.loop_forever, args=(state,))
flask = Thread(target=web.run_flask, args=(state,))

mqtt.start()
neopixel.start()
flask.start()
