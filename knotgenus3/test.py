import sys
sys.path.append('..')
sys.setrecursionlimit(10000)
import homology
import knot_sample

def example(crossings):
    M = knot_sample.exterior(crossings)
    return homology.Mcomplex(M)

def test(crossings):
    M = example(crossings)
    return M.genus()
