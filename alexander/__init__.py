from sage.all import magma as _magma
from sage.all import PolynomialRing, ZZ
import spherogram.dev.fastalex

_magma.AttachSpec(__path__[0] + '/alexander_magma/spec')
    
def snappy(manifold):
    return manifold.alexander_polynomial(try_hard_to_shorten_relators=False)

def magma(manifold):
    """
    We simplify the presentation first with Magma rather than SnapPy.
    This is much faster, and much faster than not simplifying the
    presentation at all.
    """
    G = _magma(manifold.fundamental_group(False, False, False))
    G = G.Simplify()
    print len(G.Generators())
    ans = G.AlexanderPolynomial().sage()
    return PolynomialRing(ZZ, 'a')(ans)

def dror(link):
    return spherogram.dev.fastalex.alexander(link)
    
