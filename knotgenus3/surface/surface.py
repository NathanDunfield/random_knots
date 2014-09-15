from sage.all import vector, matrix, ZZ, cached_method, ChainComplex

class Triangle:
    """
    The vertices are numbered 0, 1, 2 in an anti-clockwise
    orientation.

    Edges of the triangle are specified by the vertex that they
    *don't* contain.
    """
    def __init__(self, edges=None, vertices=None):
        self.edges = edges if edges else EdgeList([None, None, None])
        self.vertices = vertices if vertices else [None, None, None]
        self.index = None

    def __repr__(self):
        return "<Tri: %s>" % self.index

    def oriented_sides(self):
        return [Side(self, e) for e in oriented_edges_of_triangle]
        
def opposite_vertex_from_edge( vertices ):
    other = [v for v in range(3) if not v in vertices]
    assert len(vertices) == 2 and len(other) == 1
    return other[0]

oriented_edges_of_triangle = [ (1,2), (2,0), (0, 1)]

class Edge:
    """
    An oriented edge 0 -> 1. 
    """
    def __init__(self, sides = None, vertices=None):
        self.sides, self.vertices= sides, vertices
        self.index = None

    def glued_to(self, side):
        for sides in ( [S for S in self.sides],  [-S for S in self. sides] ):
            if side in sides:
                sides.remove(side)
                return sides[0]

        raise IndexError, "Given side does not appear in this edge"

    def orientation_with_respect_to(self, side):
        """
        Returns +1 if the orientation of the given side matches the
        edges, -1 otherwise.
        """
        if side in self.sides:
            return 1
        elif -side in self.sides:
            return -1
        raise IndexError, "Given side does not appear in this edge"

    def __repr__(self):
        return "<Edge %s: %s : %s>" % (self.index, [v.index for v in self.vertices], self.sides)

    def reverse(self):
        self.vertices = (self.vertices[1], self.vertices[0])
        self.sides = tuple( [-s for s in self.sides] )
            
class EdgeList(list):
    """
    A list with one item for each edge in a Triangle.  The contents
    can be accessed either by a pair of vertices or by the opposite
    vertex.
    """
    def __getitem__(self, index):
        if not hasattr(index, "__iter__"):
            return list.__getitem__(self, index)
        else:
            return self[opposite_vertex_from_edge(index)]

class Vertex:
    def __init__(self, corners = None):
        self.corners = corners
        self.index = None
        self.incoming, self.outgoing = [], []

    def __repr__(self):
        return "<Vertex %s: %s %s : %s>" % (self.index, [e.index for e in self.incoming], [e.index for e in self.outgoing], self.corners)
        
class Side:
    """
    A neighborhood of an oriented edge in a triangle
    """
    def __init__(self, triangle = None, vertices = None):
        self.triangle, self.vertices = triangle, vertices
        self.index = None

    def __neg__(self):
        v, w = self.vertices
        S = Side(self.triangle, (w, v) )
        return S

    def __repr__(self):
        v, w = self.vertices
        return "<Side %s : %d -> %d>" % (self.triangle.index, v, w)

    def __cmp__(self, other):
        v, w = self.vertices
        V, W = other.vertices
        return cmp( (self.triangle, v, w) , (other.triangle, V, W) )

    def corners(self):
        v, w = self.vertices
        T = self.triangle
        return Corner(T, v), Corner(T, w)

    def edge(self):
        return self.triangle.edges[ self.vertices ]

    def opposite_vertex(self):
        return opposite_vertex_from_edge(self.vertices)

class Corner:
    """
    A neighborhood of a vertex V in a triangle T.  
    """
    def __init__(self, triangle=None, vertex=None):
        self.triangle, self.vertex = triangle, vertex

    def next_corner(self):
        v = self.vertex
        w = [2, 0, 1][v]
        E = self.triangle.edges[ (v, w) ]
        S = Side( self.triangle, (v, w) )
        OS = E.glued_to(S)
        return Corner(OS.triangle, OS.vertices[0])

    def edge_with_orientation(self):
        v = self.vertex
        w = [2, 0, 1][v]
        E = self.triangle.edges[ (v, w) ]
        S = Side(self.triangle, (v,w) )
        return E, E.orientation_with_respect_to(S)

    def __repr__(self):
        return "<Corner %s %d>" % (self.triangle.index, self.vertex)

    def __cmp__(self, other):
        return cmp( (self.triangle, self.vertex), (other.triangle, other.vertex) )

class Surface:
    """
    An oriented surface.
    """
    def __init__(self, triangles=None):
        self.triangles, self.edges, self.vertices = triangles, [], [] 

    def glue_triangles(self, T0, e0, T1, e1):
        """
        T0, T1 are triangles, and e0, e1 specify a gluing in one of two
        ways: as a list of vertices of the triangle, or as the vertex
        opposite the edge being glued.  In the latter case, the assumption
        is that the gluing preserves orientation.

        Returns the newly created edge.
        """

        if not hasattr(e0, "__iter__"):
            e0 = oriented_edges_of_triangle[e0]
            a,b = oriented_edges_of_triangle[e1]
            e1 = (b, a)
            
            S0, S1 = Side(T0, e0), Side(T1, e1)
            E = Edge( sides = (S0,S1) )
            
            T0.edges[opposite_vertex_from_edge(e0)] = E
            T1.edges[opposite_vertex_from_edge(e1)] = E

            self.edges.append(E)
            return E

    def build_vertices(self):
        """
        Build the 0 skeleton.
        """
        vertices = []
        corners = dict( [ [(T, v), Corner(T, v)] for T in self.triangles for v in range(3) ] ) 
        while corners:
            C0 = corners.itervalues().next()
            vertex = [C0]
            C = C0.next_corner()
            while C != C0:
                vertex.append(C)
                C = C.next_corner()

            V = Vertex(vertex)
            for C in vertex:
                corners.pop( (C.triangle, C.vertex) )
                C.triangle.vertices[C.vertex] = V

            vertices.append(V)

        self.vertices = vertices
        self._vertex_containing_corner = dict([( (C.triangle, C.vertex), V) for V in vertices for C in V.corners])

    def build(self):
        """
        Build the overall cell structure and label all the cells
        """
        self.build_vertices()

        for E in self.edges:
            S = E.sides[0]
            C0, C1 = S.corners()
            V0, V1 = self.vertex_containing_corner(C0), self.vertex_containing_corner(C1)
            E.vertices = (V0, V1)
            V0.outgoing.append(E), V1.incoming.append(E)

        self.index()
        
    def vertex_containing_corner(self, corner):
        return self._vertex_containing_corner[ (corner.triangle, corner.vertex) ]
        
    def index(self):
        for objects in [self.triangles, self.edges, self.vertices]:
            for i, x in enumerate(objects):
                x.index = i

    @cached_method
    def B1(self):
        """
        The matrix describing the boundary map C1 -> C0
        """

        V, E = len(self.vertices), len(self.edges)
        D = matrix(ZZ, V, E, sparse=True)
        for e in self.edges:
            v_init = e.vertices[0].index
            v_term = e.vertices[1].index
            D[v_term, e.index] += 1
            D[v_init, e.index] += -1

        return D

    @cached_method
    def B2(self):
        E, F = len(self.edges), len(self.triangles)
        D = matrix(ZZ, E, F, sparse=True)
        for T in self.triangles:
            for S in T.oriented_sides():
                E = S.edge()
                D[E.index, T.index] += E.orientation_with_respect_to(S)

        return D

    def euler(self):
        return  len(self.vertices) - len(self.edges) + len(self.triangles)

    def homology_chain_complex(self):
        return ChainComplex({2:self.B2(), 1:self.B1()}, degree=-1)

    @cached_method
    def gen_cocycles_for_H1(self):
        C = self.homology_chain_complex()
        C = C.dual()
        cohom = C.homology(generators=True)
        return matrix(cohom[1][1])
    
    def homology_test(self):
        C = self.homology_chain_complex()
        b = C.betti()
        assert b[0] - b[1] + b[2] == self.euler()


def first_pair_differing_in_first_component(L):
    for i in range(len(L)):
        a, b = L[i : i + 2]
        if a[0] != b[0]:
            return a, b

def segments_into_components(L):
    components = []
    while L:
        s0 = L[0]
        component = [s0]
        s = s0.next
        L.remove(s0)
        while s != s0:
            component.append(s)
            L.remove(s)
            s = s.next

        components.append(component)

    return components

def component_to_cycle(surface, component):
    w = len(surface.edges)*[0,]
    for s in component:
        w[s.edge.index] += s.orientation_agrees
    return OneCycle(surface, w)
        
        
class OneCycleSegment:
    def __init__(self, edge, orientation_agrees, family_index, next = None, previous = None):
        self.edge, self.orientation_agrees = edge, orientation_agrees
        self.next, self.previous = next, previous
        self.family_index = family_index

    def __repr__(self):
        return "<OCSeg: %d %d>" % (self.edge.index, self.family_index)

class OneCycle:
    def __init__(self, surface, weights):
        self.surface, self.weights = surface, weights
        print self.weights, type(self.weights)
        self.check_boundary_is_zero()

    def check_boundary_is_zero(self):
        w = vector(self.weights)
        B1 = self.surface.B1()
        assert B1 * w == 0

    def is_zero_in_homology(self):
        return self.surface.gen_cocycles_for_H1() * vector(self.weights) == 0
        
    def components(self):
        """
        Returns a list of the connected components of the multicurve
        corresponding to the 1-cycle, each given as a OneCycle.
        """
        S, W = self.surface, self.weights
        support = [i for i, w in enumerate(W) if w != 0]
        print "support", support
        segments = {}
        for i in support:
            E =S.edges[i]
            w = self.weights[i]
            o = 1 if w > 0 else -1
            segments[i] = [OneCycleSegment(E, o, a) for a in range(abs(w))]
        print "segments", segments

        for V in S.vertices:
            segs_at_vertex = []   # a cyclically ordered list of arcs of the multicurve
            for C in V.corners:
                E, o_edge = C.edge_with_orientation()   # o_edge = +1 means *outgoing*.
                i = E.index
                if i in support:
                    segs = segments[E.index]
                    o_strands = o_edge * segs[0].orientation_agrees
                    if o_strands > 0:
                        segs_at_vertex += [ (o_strands, s) for s in segs]
                    else:
                        segs_at_vertex += [ (o_strands, s) for s in reversed(segs)]

            assert sum([s[0] for s in segs_at_vertex]) == 0

            print "sav", segs_at_vertex
            while segs_at_vertex:
                s0, s1 = first_pair_differing_in_first_component( segs_at_vertex )
                print "s0, s1", s0, s1
                # want s0 to be incoming, s1 outgoing.  
                if s0[0] > 0:
                    s0, s1 = s1, s0
                s0[1].next, s1[1].prev = s1[1], s0[1]
                segs_at_vertex.remove(s0), segs_at_vertex.remove(s1)

        components = segments_into_components(  sum( segments.values(), [] ) )
        return [component_to_cycle(S, c) for c in components]


                

        
                
                                
                
            
        
        
        

    
        
            
            
            
        


                




        
    












