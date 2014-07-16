from snappy.snap import alexander_polynomial
from sage.all import magma as _magma, PolynomialRing, ZZ

_magma.AttachSpec(__path__[0] + '/alexander_magma/spec')
    
def snappy(manifold):
        return alexander_polynomial(manifold, try_hard_to_shorten_relators=False)

def magma(manifold):
    G = _magma(manifold.fundamental_group(False, False, False))
    S = G.Simplify()
    ans = S.AlexanderPolynomial().sage()
    return PolynomialRing(ZZ, 'a')(ans)
    
    
