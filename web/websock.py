from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, disconnect
import time

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ababa'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    for i in range(3):
        emit('my response', {'data': message['data']})
        time.sleep(1)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Server Connected'})

@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    emit('my response', {'data': 'Disconnected!'})
    disconnect()

if __name__ == '__main__':
    socketio.run(app)
