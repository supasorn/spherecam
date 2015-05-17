import os
import sys


def cmd(st):
    print st
    os.system(st)

if len(sys.argv) != 2:
    print "1 for AP, 0 for Internet"
    exit(0)

# directory of this script
os.chdir(sys.path[0])

if sys.argv[1] == "1":
    cmd("cp interfaces /etc/network/interfaces")
    cmd("service networking restart")
    cmd("service hostapd restart")
    cmd("service isc-dhcp-server restart")
else:
    cmd("cp interfaces.backup /etc/network/interfaces")
    cmd("service hostapd stop")
    cmd("service isc-dhcp-server stop")
    cmd("service networking restart")

