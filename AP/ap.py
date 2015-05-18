import os
import sys
import time


def cmd(st):
    print st
    os.system(st)

if len(sys.argv) != 2:
    print "1 for AP, 0 for Internet"
    exit(0)

# directory of this script
os.chdir(sys.path[0])
print "SphereCam Script"
#f = open("/home/pi/run.txt", "w")
time.sleep(5)

if sys.argv[1] == "1":
    cmd("cp interfaces /etc/network/interfaces")
    cmd("cp hostapd.conf /etc/hostapd/hostapd.conf")
    cmd("killall wpa_supplicant")
    cmd("service networking restart")
    cmd("service hostapd restart")
    cmd("ifconfig wlan0 10.5.5.1")
    cmd("service isc-dhcp-server restart")
    #f.write("done\n")
else:
    cmd("cp interfaces.backup /etc/network/interfaces")
    cmd("service hostapd stop")
    cmd("service isc-dhcp-server stop")
    cmd("service networking restart")
    cmd("ifup wlan0")

#f.close()

