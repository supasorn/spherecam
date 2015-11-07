import os
import sys

if len(sys.argv) < 2:
    exit(0)
if len(sys.argv) >= 2:
    dataset = sys.argv[1]

os.system("cd ~/sites/pan/utils/multires; rm -rf " + dataset + "; python generate.py ~/pano/captures/" + dataset + "/001\ Panorama.jpg -n /Applications/Hugin/HuginTools/nona -o " + dataset)


