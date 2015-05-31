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

@app.route('/shot')
def shot():
    return render_template('shot.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    for i in range(3):
        emit('my response', {'data': message['data']})
        time.sleep(1)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Server Connected'})


def captureWB(wb):
    print "capturing %s" % wb
    folder = "static/capturewb"
    if not os.path.exists(folder):
        os.mkdir(folder)

    #os.system("cp /home/supasorn/pano/outside/021_0.jpg " + folder + "/" + wb)
    os.system("raspistill -t 2000 -vf -hf -w 320 -h 240 -awb " + wb + " -o " + folder + "/" + wb + ".jpg")

    return "/" + folder + "/" + wb + ".jpg"

@socketio.on('capturewb', namespace="/test")
def capturewb():
    wbs = ['auto', 'sun', 'cloud', 'shade', 'tungsten', 'fluorescent', 'incandescent', 'flash', 'horizon']
    for wb in wbs:
        url = captureWB(wb)
        emit('capturewb', {'wb': wb, 'url': url})
        emit('log', {'data': wb})
        time.sleep(0.1)

@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    emit('my response', {'data': 'Disconnected!'})
    disconnect()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
