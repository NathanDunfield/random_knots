"""
Some simple example surfaces.
"""
import random
from surface import Triangle, Surface

def sphere():
    T0, T1 = Triangle(), Triangle()
    S = Surface( [T0, T1] )
    S.glue_triangles(T0, 0, T1, 0)
    S.glue_triangles(T0, 1, T1, 2)
    S.glue_triangles(T0, 2, T1, 1)    
    S.build()
    return S


def torus1():
    T0, T1 = Triangle(), Triangle()
    S = Surface( [T0, T1] )
    for e in range(3):
        S.glue_triangles(T0, e, T1, e)
    S.build()
    return S

def torus2():
    T = [Triangle() for i in range(4)]
    S = Surface(T)

    # Make a hexagon

    for i in range(3):
        S.glue_triangles(T[i], 0, T[i+1], 1)

    # Glue the sides

    S.glue_triangles(T[0], 2, T[3], 2)
    S.glue_triangles(T[0], 1, T[2], 2)
    S.glue_triangles(T[1], 2, T[3], 0)
    S.build()
    return S

def random_surface(N):
    triangles = [Triangle() for i in range(2*N)]
    sides = [ (T, v) for T in triangles for v in range(3)]
    S = Surface(triangles)
    while sides:
        S0, S1 = random.sample(sides, 2)
        S.glue_triangles(S0[0], S0[1], S1[0], S1[1])
        sides.remove(S0), sides.remove(S1)
    S.build()
    return S
