from threading import Thread
from utils import log, SystemState, MessagingSystem
import web
import strip
import mqtt

log.info("Threads loading")

state = SystemState(MessagingSystem())

mqtt_thread = Thread(target=mqtt.start_loop, args=(state,))
neopixel = Thread(target=strip.loop_forever, args=(state,))
flask = Thread(target=web.run_flask, args=(state,))

mqtt_thread.start()
neopixel.start()
flask.start()
