from motorcontrol import *
import os
import sys
import gflags
import re
import exifread

FLAGS = gflags.FLAGS
gflags.DEFINE_string('output', 'cap4', 'Output folder')
gflags.DEFINE_string('iso', 'auto', 'ISO')
gflags.DEFINE_bool('capture', False, 'start real capturing')

def measure(ISO):
    print "Configuring camera setting..."
    et = os.popen("raspistill -n -t 5000 -o test.jpg -ISO " + ISO + " -set 2>&1").read().split("\n")
    lastline = et[-2]
    exp = re.findall("now (\d*)", et[-3])[0]
    #print exp
    R, B = re.findall("R=(.*?),.*B=(.*)", lastline)[0]
    R = R.split("/")
    R = float(R[0])/float(R[1])
    B = B.split("/")
    B = float(B[0])/float(B[1])
    #print R, G

    f = open("test.jpg", "rb")
    tags = exifread.process_file(f, details=False)
    iso = int("%s" % tags["EXIF ISOSpeedRatings"])
    return (int(exp), R, B, iso) 

class Panner:
    def __init__(self):
        self.pan = 0
        self.st = Stepper()
        self.sv = Servo()
        self.config = ""

    def setConfig(self, config):
        exp, R, B, iso = config
        self.config = "-ISO " + str(iso) + " -awb off -awbg " + str(R) + "," + str(B) + " -ss " + str(exp)

    def setPanTilt(self, pan, panDiff, tiltLow, tiltHigh, tiltDiff):
        self.pan = pan
        self.panDiff = panDiff
        self.tiltLow = 90 + tiltLow
        self.tiltHigh = 90 + tiltHigh
        self.tiltDiff = tiltDiff

    def capture(self):
        sw = 0
        count = 1
        for i in range(0, self.pan, self.panDiff):
            if sw  == 0:
                r = range(self.tiltLow, self.tiltHigh+1, self.tiltDiff)
            else:
                r = range(self.tiltHigh, self.tiltLow-1, -self.tiltDiff)
            sw ^= 1
            for j in r:
                self.sv.setAngle(j)
                print "Capture (%d) %d %d %s" % (count, j, i, self.config)
                if FLAGS.capture:
                    os.system('raspistill -o ' + FLAGS.output + "/" + ("%03d" % count) + '.jpg -t 1 -n ' + self.config)
                else:
                    time.sleep(0.5)
                count += 1
            self.st.move(1, int(round(self.panDiff * 512.0 / 360)), 0.008)

    def done(self):
        self.st.done()
        self.sv.done()

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    if not os.path.exists(FLAGS.output):
        os.mkdir(FLAGS.output)
    config = measure(FLAGS.iso)
    p = Panner()
    p.setConfig(config)
    p.setPanTilt(360, 36, -80, 80, 20)
    p.capture()
    p.done()

if __name__ == '__main__':
    main(sys.argv)
    


