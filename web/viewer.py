from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, disconnect
from flask import send_file
import time
import os

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ababa'
socketio = SocketIO(app)

#root = '/home/pi/pano/'
root = '/Users/supasorn/spherecam/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images/<path:f>')
def images(f):
    print f
    return send_file(root + 'captures/' + f)

@app.route('/view/<dataset>')
def view(dataset):
    st = '<meta name="viewport" content"width=device-width, initial-scale=1"/>'
    if not os.path.exists(root + '/captures/thumbnails/' + dataset):
        print "mkdir " + root + '/captures/thumbnails/' + dataset
        os.mkdir(root + '/captures/thumbnails/' + dataset);

    
    for i in range(1, 4):
        for j in range(3):
            f = '%03d_%d.jpg' % (i, j)
            if not os.path.exists(root + '/captures/thumbnails/' + dataset + '/' + f):
                os.system("convert " + root + '/captures/' + dataset + '/' + f + " -resize 15\% " + root + "/captures/thumbnails/" + dataset + "/" + f)
            if os.path.exists(root + "/captures/thumbnails/" + dataset + "/" + f):
                #st += "<img src='/images/thumbnails/" + dataset + "/" + f + "'/><br/>"
                st += "<img width='100' src='/images/" + dataset + "/" + f + "'/><br/>"
        st += "<br/><br/>"
    return st


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
