from flask import Flask, render_template
from flask_socketio import SocketIO, emit

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(flask_app, cors_allowed_origins="*",
                  logger=True, engineio_logger=True)


def run_flask():
    socket.run(flask_app, host='0.0.0.0', port=5000, debug=True,
               use_reloader=False)


@flask_app.get('/')
def hello():
    return render_template("index.html")


@socket.on('data')
def handle_message(data):
    print('received message: ' + data)


@socket.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})
