from . import homology

def genus_upper_bound(manifold):
    M = homology.Mcomplex(manifold)
    return M.genus()
