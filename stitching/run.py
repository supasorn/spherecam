import os
import glob
os.system("pto_gen -o project.pto *.jpg")
os.system("cpfind -o project.pto --multirow --celeste project.pto")
os.system("cpclean -o project.pto project.pto")
os.system("linefind -o project.pto project.pto")
os.system("autooptimiser -a -m -l -s -o project.pto project.pto")
os.system("pano_modify --canvas=AUTO --crop=AUTO -o project.pto project.pto")
os.system("nona -m TIFF_m -o project project.pto")
os.system("enblend -o project.tif " + " ".join(glob.glob("./*.tif")));
