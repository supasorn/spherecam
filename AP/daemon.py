import os
import RPi.GPIO as GPIO
import time
import socket
import fcntl
import struct
import sys

GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
def ip():
    ifname = "wlan0"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def checkState():
    f = open("/etc/network/interfaces").read()
    return "address" in f

if len(sys.argv) == 2:
    cmd = "python " + os.path.dirname(os.path.realpath(__file__)) + "/ap.py " + sys.argv[1]
    os.system(cmd)
    
while 1:
    if checkState(): # access point
        start = 0
        shouldRestart = ip() != "10.5.5.1"
        while ip() != "10.5.5.1":
            if time.time() - start > 3:
                os.system("ifconfig wlan0 10.5.5.1")
                start = time.time()
            GPIO.output(31, 1)
            time.sleep(0.5)
            GPIO.output(31, 0)
            time.sleep(0.5)
        if shouldRestart:
            os.system("service isc-dhcp-server restart")
    else:
        pass
    time.sleep(10)
    break 

    #print checkState()
    #print ip
