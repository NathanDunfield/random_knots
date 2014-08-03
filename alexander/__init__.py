from snappy.snap import alexander_polynomial
from sage.all import magma as _magma
from sage.all import PolynomialRing, ZZ

_magma.AttachSpec(__path__[0] + '/alexander_magma/spec')
    
def snappy(manifold):
    return alexander_polynomial(manifold, try_hard_to_shorten_relators=False)

def magma(manifold):
    """
    We simplify the presentation first with Magma rather than SnapPy.
    This is much faster, and much faster than not simplifying the
    presentation at all.
    """
    G = _magma(manifold.fundamental_group(False, False, False))
    G = G.Simplify()    
    ans = G.AlexanderPolynomial().sage()
    return PolynomialRing(ZZ, 'a')(ans)
    
    
