import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from utils.data_types import SystemState

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(flask_app, cors_allowed_origins="*",
                  logger=True, engineio_logger=True)
STATE = None


def run_flask(system_state: SystemState):
    STATE = system_state
    with STATE.lock:
        STATE.websocket_out_callback = send_msg
    socket.run(flask_app, host='0.0.0.0', port=5000, debug=True,
               use_reloader=False)


@flask_app.get('/')
def index():
    return render_template("index.html")


@socket.on('return-data')
def handle_message(data):

    print('parse json', json.loads(data))
    print('received message: ' + data)


@socket.on('connect')
def test_connect(auth):
    # TODO send current status
    emit('my response', {'data': 'Connected'})


def send_msg(message):
    topic = message.topic.split('/')[-1]
    socket.emit(topic, message.payload.decode('utf-8'))
