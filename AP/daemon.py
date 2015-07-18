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

def dhcpRunning():
    stat = os.popen("service isc-dhcp-server status")
    return "not" not in stat.read()

def checkState():
    f = open("/etc/network/interfaces").read()
    return "address" in f

def blink(sec):
    for i in range(sec):
        GPIO.output(31, 1)
        time.sleep(0.5)
        GPIO.output(31, 0)
        time.sleep(0.5)


if len(sys.argv) == 2:
    blink(5)
    cmd = "python " + os.path.dirname(os.path.realpath(__file__)) + "/ap.py " + sys.argv[1]
    os.system(cmd)
    
while 1:
    blink(1)
    os.system("killall wpa_supplicant")
    blink(2)
    os.system("service networking restart")
    blink(3)
    os.system("service hostapd restart")
    blink(4)
    os.system("ifconfig wlan0 10.5.5.1")
    blink(5)
    os.system("service isc-dhcp-server restart")
    time.sleep(60)

while 1:
    if checkState(): # access point
        #while ip() != "10.5.5.1":
        while not dhcpRunning():
            blink(3)
            os.system("ifconfig wlan0 10.5.5.1")
            time.sleep(3)
            blink(5)
            os.system("service isc-dhcp-server restart")
            blink(3)
    else:
        pass
    time.sleep(10)
    #blink(5)
    #break 

    #print checkState()
    #print ip
