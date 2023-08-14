from flask import Flask
from flask_socketio import SocketIO, emit
from utils.data_types import SystemState

flask_app = Flask(__name__, static_url_path='')
flask_app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(flask_app, cors_allowed_origins="*",
                  logger=True, engineio_logger=True)


def run_flask(state: SystemState):

    @flask_app.get('/')
    def index():
        return flask_app.send_static_file("index.html")

    @socket.on('main_switch')
    def incoming_main_switch(data):
        state.main_switch = data
        state.send_message_to_mqtt('main_switch', data)

    @socket.on('hex_rgb')
    def incoming_hex_rgb(data):
        state.hex_rgb = data
        state.send_message_to_mqtt('hex_rgb', data)
        emit('hex_rgb', data)

    @socket.on('brightness')
    def incoming_brightness(data):
        state.brightness = data
        state.send_message_to_mqtt('brightness', data)

    @socket.on('wait')
    def incoming_wait(data):
        state.wait = data
        state.send_message_to_mqtt('wait', data)

    @socket.on('show_type')
    def incoming_show_type(data):
        state.show_type = data
        state.send_message_to_mqtt('show_type', data)

    @socket.on('connect')
    def on_connect():
        emit('main_switch', state.main_switch)
        emit('hex_rgb', state.hex_rgb)
        emit('brightness', state.brightness)
        emit('wait', state.wait)
        emit('show_type', state.show_type)

    socket.run(flask_app, host='0.0.0.0', port=5000, debug=True,
               use_reloader=False)


def send_update_to_websocket(message):
    topic = message.topic.split('/')[-1]
    socket.emit(topic, message.payload.decode('utf-8'))
