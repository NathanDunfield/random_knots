from snappy import *
from spherogram import *
from sage.all import *

def braid_closure_via_tangles(braid):
    n = max(-min(braid),max(braid))+1
    l = len(braid)
    B = IdentityBraid(n)
    for i in range(l):
        v = braid[i]
        nextpiece = IdentityBraid(abs(v)-1)|RationalTangle(sign(v))|IdentityBraid(n-abs(v)-1)
        B = B*nextpiece
    return B.braid_closure()

def braid_closure_via_crossings(braid):
    l = len(braid)
    crossings = [Crossing(i) for i in range(l)]
    for i in range(l):
        foundleftstrand = False
        foundrightstrand = False
        j = (i+1)%l

        while ((not foundleftstrand) or (not foundrightstrand)):
            if (not foundleftstrand) and (abs(braid[j]) == abs(braid[i])-1):
                crossings[i][3] = crossings[j][1]
                print('attaching ' + str(i) + '3 to ' + str(j) +'1')
                foundleftstrand = True
            if (not foundrightstrand) and (abs(braid[j]) == abs(braid[i])+1):
                crossings[i][0] = crossings[j][2]
                print('attaching ' + str(i) + '0 to ' + str(j) +'2')
                foundrightstrand = True
            if abs(braid[j]) == abs(braid[i]):
                if (not foundleftstrand):
                    crossings[i][3] = crossings[j][2]
                    print('attaching ' + str(i) + '3 to ' + str(j) +'2')
                    foundleftstrand = True
                if (not foundrightstrand):
                    crossings[i][0] = crossings[j][1]
                    print('attaching ' + str(i) + '0 to ' + str(j) +'1')
                    foundrightstrand = True
            j = (j+1)%l
            
    for i in range(l):
        if braid[i]>0:
            crossings[i].rotate_by_90()
    return Link(crossings)
