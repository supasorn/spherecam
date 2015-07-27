from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, disconnect
import time
import os
import subprocess


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ababa'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


def generateOptions(name, opt, default):
    return [{"name": x, "id": name + "_" + x, "pick": x in default, "group": name + "Options"} for x in opt]

@app.route('/pano')
def pano():

    isoOptions = generateOptions("iso", ["1", "2", "4", "6", "8", "A"], "2")
    bracketPosOptions = generateOptions("bracketPos", ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"], "2.0")
    bracketNegOptions = generateOptions("bracketNeg", ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"], "2.0")
    return render_template('pano.html', isoOptions = isoOptions, bracketPosOptions = bracketPosOptions, bracketNegOptions = bracketNegOptions)

@app.route('/shot')
def shot():

    sizeOptions = generateOptions("size", ["Small", "Medium", "Large", "Full"], "Full")
    timeOptions = generateOptions("time", ["0", "0.5", "1", "2", "5"], "2")
    isoOptions = generateOptions("iso", ["1", "2", "3", "4", "5", "6", "7", "8", "A"], "A")
    return render_template('shot.html', sizeOptions = sizeOptions, timeOptions = timeOptions, isoOptions = isoOptions)

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
    os.system("raspistill -st -t 2000 -vf -hf -w 320 -h 240 -awb " + wb + " -o " + folder + "/" + wb + ".jpg")

    return "/" + folder + "/" + wb + ".jpg"

@socketio.on('capture', namespace="/test")
def capture(message):
    cmd = "python ../main.py --output=" + message["dataset"] + " --evs=" + message["evs"]
    #p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
    #for line in iter(p.stdout.readline, b''):
        #emit('progress', {'v': line})
    #p.stdout.close()
    #p.wait() 
    emit('progress', {'v': cmd})

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
