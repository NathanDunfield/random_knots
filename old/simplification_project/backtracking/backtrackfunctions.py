from spherogram.links.simplify import DualGraphOfFaces, possible_type_III_moves, reidemeister_III
import spherogram.links.links as links
import random

def random_reverse_type_I(link,label):
    """
    Creates a twist between CrossingStrands cs1 and its opposite
    """
    cs1 = random.choice(link.crossing_strands())
    D = links.Crossing(label)
    link.crossings.append(D)

    cs2 = cs1.opposite()
    D[2] = D[3]
    cs1ec, cs1cep = cs1.crossing, cs1.entry_point
    D[0] = cs1ec[cs1cep]
    cs2ec, cs2cep = cs2.crossing, cs2.entry_point
    D[1] = cs2ec[cs2cep]



def random_reverse_type_II(link, label1, label2):
    G = DualGraphOfFaces(link)
    while True:
        face = random.choice(list(G.vertices))
        if len(face)>1:
            break
    c, d = random.sample(face,2)
    new1, new2 = links.Crossing(label1), links.Crossing(label2)    
    c_cross, c_ep = c.crossing, c.entry_point
    cop_cross, cop_ep = c.opposite().crossing, c.opposite().entry_point
    d_cross, d_ep = d.crossing, d.entry_point
    dop_cross, dop_ep = d.opposite().crossing, d.opposite().entry_point
    new1[2], new1[3] = new2[0], new2[3]
    new1[0], new1[1] = dop_cross[dop_ep], c_cross[c_ep]
    new2[1], new2[2] = cop_cross[cop_ep], d_cross[d_ep]

    link.crossings.append(new1)
    link.crossings.append(new2)

def random_reverse_move(link,t,n):

    if t == 1:
        print( 'Type I' )
        random_reverse_type_I(link,'new'+str(n))
    elif t == 2:
        print( 'Type II' )
        random_reverse_type_II(link,'new'+str(n),'new'+str(n+1))
    else:
        print( 'Type III' )
        #link._build_components()
        poss_moves = possible_type_III_moves(link)
        if len(poss_moves) != 0:
            reidemeister_III(link, random.choice(poss_moves))
            link._build_components()

def backtrack(link, num_steps = 10):
    n = 0
    for i in range(num_steps):
        t = random.randint(1,3)
        n += t%3

        random_reverse_move(link,t,n)
        
        clear_orientations(link)

        L = links.Link(link.crossings)
        link = L
    clear_orientations(link)
    relabel_crossings(link)
    return link.crossings


def clear_orientations(link):
    link.link_components = None
    for i in link.crossings:
        i.sign = 0
        i.directions.clear()

def relabel_crossings(link):
    for i,cr in enumerate(link.crossings):
        cr.label = str(i)


