from __future__ import division
from motorcontrol import *
import os
import sys
import gflags
import re
import exifread
import math
from time import gmtime, strftime

FLAGS = gflags.FLAGS
gflags.DEFINE_string('output', '', 'Output folder')
gflags.DEFINE_string('iso', '200', 'ISO')
#gflags.DEFINE_string('evs', '1.58,-2', 'exposure bracketing')
gflags.DEFINE_string('evs', '2,-2', 'exposure bracketing')
#gflags.DEFINE_string('evs', '3.5,1.58', 'exposure bracketing')
gflags.DEFINE_bool('bracket', True, 'Use bracketing')
gflags.DEFINE_bool('capture', True, 'start real capturing')
#gflags.DEFINE_string('ud', '80,-60,20', 'Up Down direction')
gflags.DEFINE_string('ud', '70,-40,50', 'Up Down direction')

def measure(ISO):
    print "Configuring camera setting..."
    et = os.popen("raspistill -n -t 2000 -o test.jpg -ISO " + ISO + " -set 2>&1").read().split("\n")
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
        self.sv.setAngle(90)
        self.probe()

    def probe(self):
        lss = [[] for x in range(3)]
        lR = []
        lB = []
        prob = 4
        for i in range(prob):
            if i > 0:
                self.st.move(-1, int(round((360 / prob) * 512.0 / 360)), 0.002)
            #for i, ud in enumerate([60, 0, -60]):
            for i, ud in enumerate([0]):
                self.sv.setAngle(90 - ud)
                ss, R, B, iso = measure(FLAGS.iso)
                lss[i].append(ss)
                if ud == 0:
                    lR.append(R)
                    lB.append(B)

                print ss, R, B, iso

        self.config = "-ISO " + FLAGS.iso + " -awb off -awbg " + str(sum(lR) / len(lR)) + "," + str(sum(lB) / len(lB))
        self.ss = sum(lss[0]) / len(lss[0])

        #self.ss = sum(lss[1]) / len(lss[1])
        #print min(lss[0]), max(lss[2])
        #print min(lss[0]) / self.ss
        #bright = math.log(min(lss[0]) / self.ss, 2)
        #dark = math.log(max(lss[2]) / self.ss, 2)
        #print bright, dark

        self.bracket = [0.0]
        if FLAGS.bracket:
            self.bracket += [float(x.strip()) for x in FLAGS.evs.split(",")]

    def setPanTilt(self, pan, panDiff):
        self.pan = pan
        self.panDiff = panDiff
        tilt = [int(x.strip()) for x in FLAGS.ud.split(",")]
        self.tiltLow = 90 - tilt[0] 
        self.tiltHigh = 90 - tilt[1]
        self.tiltDiff = tilt[2]

    def capture(self):
        sw = 0
        count = 1
        for i in range(0, self.pan, self.panDiff):
            r = range(self.tiltHigh, self.tiltLow-1, -self.tiltDiff)
            if sw == 0:
                r = r[::-1]
            sw ^= 1
            for j in r:
                self.sv.setAngle(j)
                for k in range(len(self.bracket)):
                    config = self.config + " -ss " + str(self.ss * (2 ** self.bracket[k])) + " --exif angleLR=" + str(i) + " --exif angleUD=" + str(j) + " -vf -hf"
                    print "Capture (%03d_%d) %d %d %s" % (count, k, j - 90, i, config)
                    if FLAGS.capture:
                        os.system('raspistill -o ' + FLAGS.output + "/" + ("%03d_%d" % (count, k)) + '.jpg -t 1 -n ' + config)
                    else:
                        time.sleep(0.5)
                count += 1
            if i + self.panDiff < self.pan:
                self.st.move(1, int(round(self.panDiff * 512.0 / 360)), 0.002)

    def done(self):
        self.st.done()
        self.sv.done()

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    if len(FLAGS.output) == 0:
        FLAGS.output = strftime("%Y_%m_%d_%H:%M:%S", gmtime())

    if FLAGS.capture:
        if not os.path.exists(FLAGS.output):
            os.mkdir(FLAGS.output)
        else:
            choice = raw_input("Capture already exists. Replace [y/n]?").lower()
            if choice not in ['y']:
                exit(0)
        
    p = Panner()
    #p.setPanTilt(360, 36)
    #p.setPanTilt(360, 72)
    p.setPanTilt(360, 90)
    p.capture()
    p.done()

if __name__ == '__main__':
    main(sys.argv)
    


