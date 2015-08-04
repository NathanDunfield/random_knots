        
def strand_pickup(link,overcrossingstrand):
    """
    Simplifies link by optimizing the path of the longest sequence of overcrossings.
    Returns a new link and the number of crossings removed.
    """
    for overcross in overcrossingstrand:
        startcep = overcross[0]
        length = overcross[1]
        G = links.Link.dual_graph(link)

        #finding all crosses traversed by the overcrossing, accounting for possible self-intersection
        endpoint = startcep.next()
        crossingset = set([endpoint.crossing])
        for i in range(1,length):
            endpoint = endpoint.next()
            crossingset.add(endpoint.crossing)
        endpoint = endpoint.next()

        #creating list of edges of the dual graph corresponding to segments of the strand overcross
        crossgraph = nx.Graph()
        edgescrossed = []
        s = startcep


        for i in range(length+1):
            edge = (s.rotate(2),s.next())
            listOfEdges = list(G.edges)
            for j in range(len(listOfEdges)):
                edgereverse = (edge[1],edge[0])
                if(listOfEdges[j].interface == edge or listOfEdges[j].interface == edgereverse ):
                    edge = listOfEdges[j]
                    break

            edgescrossed.append(edge)
            s = s.next()



        #create a networkx graph with these edges, and find the connected components
        for i in range(len(edgescrossed)):
            crossgraph.add_edge(edgescrossed[i][0],edgescrossed[i][1])


        components = nx.connected_components(crossgraph)


        #collapse the connected components in original dual graph
        Gx = G.to_networkx()
        for i in range(len(components)):
            merge_vertices(Gx,components[i])
        Gx_nodes = Gx.nodes()

        #find shortest path between start and end points
        source = None
        dest = None

        for i in range(len(Gx)):
            for j in range(len((Gx_nodes[i]))):

                if Gx_nodes[i][j] == edgescrossed[0][0]:

                    source = Gx_nodes[i]

                if Gx_nodes[i][j] == edgescrossed[-1][0]:

                    dest = Gx_nodes[i]
        path = nx.shortest_path(Gx,source,dest)

        crossingsremoved = length - (len(path) - 1)

        if crossingsremoved == 0:
            continue

        #force all elements of path to be represented as tuples (to account for single elements)
        for i in range(len(path)):
            if(not type(path[i]) == tuple):
                path[i] = path[i],

        #creating a new list of crossings from which to rebuild the link, remove old overcross
        newcrossings = list(link.crossings)
        for i in newcrossings:   #remove old orientations
            i.sign = 0
            i.directions.clear()
        toremove = startcep.next()
        for i in range(len(crossingset)):
            loose1 = toremove.rotate(1).opposite()
            loose2 = toremove.rotate(3).opposite()

            lc1, lc1ep = loose1.crossing, loose1.entry_point
            lc2, lc2ep = loose2.crossing, loose2.entry_point

            while lc1 not in newcrossings:
                lc1, lc1ep = lc1.rotate(2).opposite().crossing, lc1.rotate(2).opposite().entry_point
            while lc2 not in newcrossings:
                lc2, lc2ep = lc2.rotate(2).opposite().crossing, lc2.rotate(2).opposite().entry_point
            lc1[lc1ep] = lc2[lc2ep]
            newcrossings.remove(toremove.crossing)
            toremove = toremove.next()


        looseend = startcep.rotate(2)

        #find new sequence of overcrossings to create
        for i in range(len(path)-1):
            nextedge = None
            label = 'new%d' % i
            crossingtoadd = links.Crossing(label)
            first = None
            for j in range(len(path[i])):
                found = False
                idict = G.incidence_dict[path[i][j]]
                for l in range(len(idict)):
                    if(idict[l][0] != path[i][j]):
                        totest = idict[l][0]
                    else:
                        totest = idict[l][1]

                    if(totest in path[i+1]):
                        found = True
                        nextedge = idict[l]
                        first = path[i][j]


            for i in first:
                if i == nextedge.interface[0] or i == nextedge.interface[1]:
                    lec, lecep = looseend.crossing, looseend.entry_point
                    crossingtoadd[1] = lec[lecep]
                    ic,icep = i.crossing,i.entry_point
                    ico,icoep = i.opposite().crossing, i.opposite().entry_point
                    while ic not in newcrossings:
                        temp = ic.crossing_strands()[icep]
                        ic,icep = temp.rotate(2).opposite().crossing,temp.rotate(2).opposite().entry_point
                    while ico not in newcrossings:
                        temp = ico.crossing_strands()[icoep]
                        ico,icoep = temp.rotate(2).opposite().crossing,temp.rotate(2).opposite().entry_point

                    crossingtoadd[2] = ic[icep]
                    crossingtoadd[0] = ico[icoep]



            looseend = crossingtoadd.crossing_strands()[3]
            newcrossings.append(crossingtoadd)

        lec, lecep = looseend.crossing, looseend.entry_point
        ec, ecep = endpoint.crossing, endpoint.entry_point
        ec[ecep] = lec[lecep]
        return links.Link(newcrossings), crossingsremoved

    return link, 0

def merge_vertices(graph,vertices):
    """
    Merges list of vertices of networkx graph and throws together all edges of all the merged vertices
    """

    v = tuple(vertices)
    graph.add_node(v)
    for i in range(len(v)):
	edgelist = graph.edges(v[i])
	for j in range(len(edgelist)):
	    graph.add_edge(v,edgelist[j][0])
	    graph.add_edge(v,edgelist[j][1])
	graph.remove_node(v[i])

    return


def random_reverse_type_I(link,label):
    """
    Randomly adds a loop in a strand, adding one crossing with given label
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
    
    D.rotate(random.randint(0,1)) #choose whether over or under crossing

def random_reverse_type_II(link, label1, label2):
    """
    Randomly crosses two strands, adding two crossings, with labels label1 and label2
    """

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
    """
    Performs a crossing increasing move of type t, where t is 1, 2, or 3
    n is for labeling the new crossings
    """
    if t == 1:
        random_reverse_type_I(link,'new'+str(n))
    elif t == 2:
        random_reverse_type_II(link,'new'+str(n),'new'+str(n+1))
    else:
        poss_moves = possible_type_III_moves(link)
        if len(poss_moves) != 0:
            reidemeister_III(link, random.choice(poss_moves))


def backtrack(link, num_steps = 10):
    """
    Randomly perform a series of Reidemeister moves which increase or preserve the
    number of crossings of a link diagram, with the number of such moves num_steps
    Use the method backtrack in the Link class.
    """
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
    return links.Link(link.crossings)
    

def clear_orientations(link):
    """
    Resets the orientations on the crossings of a link to default values
    """
    link.link_components = None
    for i in link.crossings:
        i.sign = 0
        i.directions.clear()

def relabel_crossings(link):
    """
    Relabel the crossings as integers
    """
    for i,cr in enumerate(link.crossings):
        cr.label = str(i)

    
