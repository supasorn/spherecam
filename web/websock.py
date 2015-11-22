from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, disconnect
import time
from flask import send_file
import os
import subprocess


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ababa'
socketio = SocketIO(app)

root = '/home/pi/pano/'

@app.route('/')
def index():
    return render_template('index.html')


def generateOptions(name, opt, default):
    return [{"name": x, "id": name + "_" + x, "pick": x in default, "group": name + "Options"} for x in opt]

@app.route('/r/<angle>')
def r(angle):
    os.system("python /home/pi/pano/motor.py " + angle)
    return "OK"

@app.route('/pano')
def pano():
    isoOptions = generateOptions("iso", ["1", "2", "4", "6", "8", "A"], "2")
    bracketPosOptions = generateOptions("bracketPos", ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"], "2.0")
    bracketNegOptions = generateOptions("bracketNeg", ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"], "2.0")
    wbOptions = generateOptions("wb", ["auto", "sun", "cloud", "shade", "tungsten", "fluorescent", "incandescent", "flash", "horizon"], "auto")
    return render_template('pano.html', isoOptions = isoOptions, bracketPosOptions = bracketPosOptions, bracketNegOptions = bracketNegOptions, wbOptions = wbOptions)

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
    isoFlag = "--iso=" + str(int(message["iso"]) * 100) if message["iso"] != "A" else ""
    overwriteFlag = "--overwrite" if message["overwrite"] else ""
    outputFlag = "--output=" + message["dataset"] if len(message["dataset"]) > 0 else ""
    evsFlag = "--evs=" + message["evs"] if len(message["evs"]) > 0 else "--nobracket"
    wbFlag = "--wb=" + message["wb"]
    cmd = "python /home/pi/pano/main.py " + outputFlag + " " + evsFlag + " " + isoFlag + " " + wbFlag + " --nointeractive " + overwriteFlag
    #cmd = "ls"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, b''):
        emit('progress', {'v': line})
    p.stdout.close()
    p.wait() 

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

@app.route('/images/<path:f>')
def images(f):
    print f
    return send_file(root + 'captures/' + f)

def view(dataset, ran):
    st = '<meta name="viewport" content"width=device-width, initial-scale=1"/>'
    if not os.path.exists(root + '/captures/thumbnails/' + dataset):
        print "mkdir " + root + '/captures/thumbnails/' + dataset
        os.mkdir(root + '/captures/thumbnails/' + dataset);

    
    for i in ran:
        for j in range(10):
            f = '%03d_%d.jpg' % (i, j)
            if os.path.exists(root + "/captures/" + dataset + "/" + f):
                st += "<img width='400' src='/images/" + dataset + "/" + f + "'/><br/>"
            else:
                break
        st += "<br/><br/>"
    return st
@app.route('/view/<dataset>')
def view3(dataset):
    return view(dataset, range(1, 4))

@app.route('/viewall/<dataset>')
def viewall(dataset):
    return view(dataset, range(1, 13))

@app.route('/halt')
def halt():
    os.system("sudo halt")
    return ""

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
