import spherogram as sp
import snappy as sn

K = sp.random_knot(500)
print('Starting knot: ')
print(K)
print('Volume: '+str(K.exterior().volume()))
K.global_simplify()
print('After global_simplify: ')
print(K)
print('Volume: '+str(K.exterior().volume()))
K.backtrack()
print('After backtrack: ')
print(K)
print('Volume: '+str(K.exterior().volume()))

K.global_simplify()
print('Simplifying again: ')
print(K)
print('Volume: '+str(K.exterior().volume()))


