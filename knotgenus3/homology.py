import snappy
import snappy.snap.t3mlite as t3m
from snappy.snap.t3mlite.simplex import *
from sage.all import matrix, cached_method, ZZ, ChainComplex
from . import optimize

def euler_to_genus(euler):
    """
    Given:

    * M = complement of a null-homologous knot in a QHS
    * euler = euler of some surface S which is nontrivial in H_2(M, bdry M)

    returns an *upper* bound on the genus of the knot.

    The reason we can't just solve (1 - 2g = euler) is that S may have nugatory
    boundary components which bound discs in the torus (bdry M). 
    """
    if euler % 2 == 0:
        euler += 1  # At least one nugagory component of (bdry S).
    return (1 - euler)/2

#----------- Boundary maps in homology for an Mcomplex ------------------

def boundary_three(manifold):
    F, T = len(manifold.Faces), len(manifold.Tetrahedra) 
    ans = matrix.zero(F, T, sparse=True)
    for F in manifold.Faces:
        t0, t1 = [C.Tetrahedron.Index for C in F.Corners]
        ans[F.Index, t0] +=  1
        ans[F.Index, t1] += -1
    return ans
        
def boundary_two(manifold):
    VerticesOfFace = { F0 : (V1, V2, V3), F1 : (V0, V3, V2), F2 : (V0, V1, V3), F3 :
                       (V0, V2, V1) }

    E, F = len(manifold.Edges), len(manifold.Faces)
    ans = matrix.zero(E, F, sparse=True)
    for F in manifold.Faces:
        C  = F.Corners[0]
        tet = C.Tetrahedron
        vertices =  VerticesOfFace[C.Subsimplex]
        for i in range(3):
            a, b = vertices[i], vertices[(i + 1)%3]
            e = tet.Class[a | b]
            ans[e.index(), F.Index] += e.orientation_with_respect_to(tet, a, b)
    return ans 
    
def boundary_one(manifold):
    V, E = len(manifold.Vertices), len(manifold.Edges)
    D = matrix.zero(V, E, sparse=True)
    for e in manifold.Edges:
        v_init, v_term = [v.Index for v in e.Vertices]
        D[v_term, e.Index] += 1
        D[v_init, e.Index] += -1
    return matrix(D)

def boundary_maps(manifold):
    """
    The boundary maps in the homology chain complex of the 
    underlying cell-complex of a Mcomplex.

    >>> M = Mcomplex('o9_12345')
    >>> len(M.boundary_maps()) == 3
    True
    """
    B1, B2, B3 = boundary_one(manifold), boundary_two(manifold), boundary_three(manifold)
    assert B1*B2 == 0 and B2*B3 == 0 
    return B1, B2, B3



#---------- Adding methods to Mcomplex ---------------------

class Mcomplex(t3m.Mcomplex):
    def __init__(self, tetrahedron_list=None):
        if isinstance(tetrahedron_list, (snappy.Manifold, snappy.ManifoldHP)):
            self.shapes = map(complex, tetrahedron_list.tetrahedra_shapes('rect'))
        t3m.Mcomplex.__init__(self, tetrahedron_list)

    @cached_method
    def boundary_maps(self):
        return boundary_maps(self)

    def B1(self):
        return self.boundary_maps()[0]

    def B2(self):
        return self.boundary_maps()[1]

    def B3(self):
        return self.boundary_maps()[2]

    @cached_method
    def generator_of_H2(self):
        # Use Sage, which invokes CHomP when installed, otherwise PARI.
        B1, B2, B3 = self.boundary_maps()
        C = ChainComplex({3:B3, 2:B2, 1:B1}, degree=-1)
        H2, gens = C.homology(generators=True)[2]
        if not H2.is_cyclic() or H2.is_finite() or len(gens) != 1:
            raise ValueError("Homology group is not Z")
        return gens[0]

    @cached_method
    def optimal_generator_of_H2(self):
        """
        Returns a cycle of minimal l^1 norm representing the
        generator of H_2.

        >>> M = Mcomplex('K14n2134')
        >>> M.optimal_generator_of_H2().norm(1)
        14
        """
        gen = self.generator_of_H2()
        return optimize.optimal_chain(gen, self.B3())

    def genus(self,  two_cycle=None):
        if two_cycle is None:
            two_cycle = self.optimal_generator_of_H2()
        norm =  two_cycle.norm(1)
        assert norm % 2 == 0 
        euler = -norm/2
        return euler_to_genus(euler)
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()

