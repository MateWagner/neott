from flask import Flask
from flask_socketio import SocketIO, emit
from utils import SystemState


def run_flask(state: SystemState):
    flask_app = Flask(__name__, static_url_path='')
    flask_app.config['SECRET_KEY'] = 'secret!'
    socket = SocketIO(flask_app, cors_allowed_origins="*",
                      logger=True, engineio_logger=True)

    @flask_app.get('/')
    def index():
        return flask_app.send_static_file("index.html")

    @socket.on('main_switch')
    def incoming_main_switch(data):
        state.main_switch = data

    @socket.on('hex_rgb')
    def incoming_hex_rgb(data):
        state.hex_rgb = data
        emit('hex_rgb', data)

    @socket.on('brightness')
    def incoming_brightness(data):
        state.brightness = data

    @socket.on('wait')
    def incoming_wait(data):
        state.wait = data

    @socket.on('show_type')
    def incoming_show_type(data):
        state.show_type = data

    @socket.on('connect')
    def on_connect():
        emit('main_switch', state.main_switch.name)
        emit('hex_rgb', state.hex_rgb)
        emit('brightness', state.brightness)
        emit('wait', state.wait)
        emit('show_type', state.show_type.name)

    def send_update_to_websocket(topic, message):
        socket.emit(topic, message)

    state.add_message_callback(send_update_to_websocket)

    socket.run(flask_app, host='0.0.0.0', port=5000, debug=True,
               use_reloader=False,  allow_unsafe_werkzeug=True)
