import os
from multiprocessing import Pool
import multiprocessing as mp
import sys

dataset = "captures/wide5"

def worker(x):
    st = "enfuse " 
    k = 0
    print dataset + "/%03d_%d.jpg" % (x, k)
    print os.path.exists(dataset + "/%03d_%d.jpg" % (x, k))
    while os.path.exists(dataset + "/%03d_%d.jpg" % (x, k)):
        print "in"
        st += dataset + "/%03d_%d.jpg " % (x, k)
        k += 1
    st += "-o " + dataset + "/%03d.jpg" % x
    os.system(st)


if len(sys.argv) < 2:
    exit(0)
if len(sys.argv) >= 2:
    dataset = "captures/" + sys.argv[1]

p = Pool(mp.cpu_count())
p.map(worker, range(1, 13))


