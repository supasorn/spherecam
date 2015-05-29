from motorcontrol import *
import os
import sys
import gflags
import re
import exifread
import math

FLAGS = gflags.FLAGS
gflags.DEFINE_string('output', 'cap5', 'Output folder')
gflags.DEFINE_string('iso', '200', 'ISO')
gflags.DEFINE_string('bracket', '1.58,-1.58', 'exposure bracketing')
gflags.DEFINE_bool('capture', False, 'start real capturing')
gflags.DEFINE_string('ud', '80,-80,20', 'Up Down direction')

def measure(ISO):
    print "Configuring camera setting..."
    et = os.popen("raspistill -n -t 3000 -o test.jpg -ISO " + ISO + " -set 2>&1").read().split("\n")
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
        lss = []
        lR = []
        lB = []
        liso = []
        probe = 4
        for i in range(probe):
            if i > 0:
                self.st.move(1, int(round(90 * 512.0 / 360)), 0.003)
            ss, R, B, iso = measure(FLAGS.iso)
            lss.append(ss)
            lR.append(R)
            lB.append(B)
            liso.append(iso)

            print ss, R, B, iso

        self.config = "-ISO " + str(sum(liso) / probe) + " -awb off -awbg " + str(sum(lR) / probe) + "," + str(sum(lB) / probe)
        self.ss = sum(lss) / probe
        self.bracket = [0.0] + [float(x.strip()) for x in FLAGS.bracket.split(",")]

    def setPanTilt(self, pan, panDiff):
        self.pan = pan
        self.panDiff = panDiff
        tilt = [int(x.strip()) for x in FLAGS.ud.split(",")]
        self.tiltLow = 90 + tilt[1] 
        self.tiltHigh = 90 + tilt[0]
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
                    config = self.config + " -ss " + str(self.ss * (2 ** self.bracket[k]))
                    print "Capture (%03d_%d) %d %d %s" % (count, k, j - 90, i, config)
                    if FLAGS.capture:
                        os.system('raspistill -o ' + FLAGS.output + "/" + ("%03d_%d" % (count, k)) + '.jpg -t 1 -n ' + config)
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
    p = Panner()
    p.setPanTilt(360, 36)
    p.capture()
    p.done()

if __name__ == '__main__':
    main(sys.argv)
    


