from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, disconnect
import time
import os

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


def captureWB(wb):
    folder = "static/capturewb"
    if not os.path.exists(folder):
        os.mkdir(folder)

    os.system("cp /home/supasorn/pano/outside/021_0.jpg " + folder + "/" + wb)
    return "/" + folder + "/" + wb

@socketio.on('capturewb', namespace="/test")
def capturewb():
    wbs = ['sunny', 'shade']
    for wb in wbs:
        url = captureWB(wb)
        emit('capturewb', {'wb': wb, 'url': url})

@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    emit('my response', {'data': 'Disconnected!'})
    disconnect()

if __name__ == '__main__':
    socketio.run(app)
