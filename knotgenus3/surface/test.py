from surface import OneCycle, Triangle, Surface
from sage.all import vector, matrix

T0, T1, T2, T3 = [Triangle() for i in range(4)]
S = Surface([T0, T1, T2, T3])
# Make a rectangle:
S.glue_triangles(T0, 0, T1, 0)
S.glue_triangles(T2, 0, T3, 0)
S.glue_triangles(T1, 2, T2, 2)
# Glue the horizontal sides:
S.glue_triangles(T0, 1, T1, 1)
S.glue_triangles(T2, 1, T3, 1)
# Glue the vertical sides:
S.glue_triangles(T0, 2, T3, 2)
S.build()
S.vertices = S.vertices

def shift(L, i):
    return L[i:] + L[:i]

S.vertices[1].corners = shift(S.vertices[1].corners, 0)


hom_gens = S.homology_chain_complex().homology(generators=True)[1][1]

def test_cycle(w):
    T = matrix(hom_gens + S.B2().columns())
    return OneCycle(S, vector(w)*T)



def cycle_info(c):
    print c.weights, c.is_zero_in_homology(), cobasis*vector(c.weights)    

cobasis = S.gen_cocycles_for_H1()
#z = OneCycle(S, vector([-2, 0, 2, -1, 1, 0]))
z = test_cycle([1,0,0,2,0,0])
print len(z.components()), z.weights
