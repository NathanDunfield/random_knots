import sys
sys.path.append('..')
sys.setrecursionlimit(10000)
import homology
import knot_sample

def example(crossings):
    M = knot_sample.exterior(crossings)
    return homology.Mcomplex(M)

for i in range(100):
    M = example(5)
    print M.genus()
