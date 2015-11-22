import os
import re
import sys

#print os.popen("fdisk -l").read()
#st = re.findall("/dev/sdb6/", os.popen('fdisk -l').read())
st = os.popen('fdisk -l').read().replace("\n", "")
start = re.findall("/dev/sdb6[ ]*(\d*)", st)[0]
if (len(sys.argv) == 1): 
    print ("mount -oloop,offset=$((" + str(start) + "*512)) /dev/sdb/ /media/supasorn/")
    os.system("mount -oloop,offset=$((" + str(start) + "*512)) /dev/sdb/ /media/supasorn/")
else:
    os.system("umount /media/supasorn/")
#print st
