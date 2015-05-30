import os
from multiprocessing import Pool
import multiprocessing as mp
dataset = "outside"

def worker(x):
    st = "enfuse " 
    for k in range(3):
        st += dataset + "/%03d_%d.jpg " % (x, k)
    st += "-o " + dataset + "/%03d.jpg" % x
    os.system(st)

p = Pool(mp.cpu_count())
p.map(worker, range(1, 91))


