
    def optimize_overcrossings(self):
        """
        Minimizes the number of crossings of a strand which crosses entirely
        above the diagram by finding the path crossing over the diagram with
        the least number of overcrossings.  It begins with the longest
        overcrossing, and continues with smaller ones until it successfully
        reduces the number of crossings.
        """
        from . import simplify
        return simplify.strand_pickup(self, self.overcrossings())

    def global_simplify(self,full_simplify=False):
        """
        Performs optimize_overcrossings on a diagram, flips, and performs the
        same process on the other side of the diagram, simplifying in between
        until the process stabilizes. The boolean full_simplify indicates 
        whether or not to perform a simplification that includes Reidemeister III
        type moves.
        
        >>> K = random_knot(100) #Generate a random knot diagram
        >>> K.simplify()
        False
        >>> K
        <Link: 1 comp; 55 cross>
        >>> K.global_simplify()
        >>> K
        <Link: 1 comp; 40 cross>
        """

        from . import simplify
        stabilized = len(self.crossings) == 0
        L = self
        while not stabilized:
            L, overcrossingsremoved = L.optimize_overcrossings()

            if full_simplify:
                L.simplify()
            else:
                L.basic_simplify()
                L._build_components()

            if len(L.crossings) == 0:
                break
            mirror = L.mirror()
            mirror, undercrossingsremoved = mirror.optimize_overcrossings()
            L = mirror.mirror()
            
            if full_simplify:
                L.simplify()
            else:
                L.basic_simplify()
                L._build_components()
            stabilized = ((overcrossingsremoved == 0) and (undercrossingsremoved == 0)) or (len(L.crossings) == 0)
        
        self.crossings = L.crossings
        self.labels = L.labels
        self.link_components = L.link_components
        self.name = L.name
 

    def overcrossings(self):
        """
        Returns a list of the sequences of overcrossings of the link,
        sorted in descending order of length
        """
        comp = self.link_components
        overcrosses = []
        for c in comp:
            origin = None
            for i in c:
                if i.is_under_crossing():
                    origin = i
                    break
            start = origin
            end = start.next()
            while True:
                length = 0
                alreadyseen = []
                while (end.is_over_crossing() or (end.crossing in alreadyseen)) and (end.crossing != start.crossing):
                    alreadyseen.append(end.crossing)
                    length += 1
                    end = end.next()
                if length >= 1:
                    overcrosses.append([start,length])
                start = end
                end = start.next()
                if start == origin:
                    break
        return sorted(overcrosses, key=lambda overcross: overcross[1], reverse=True)

    def backtrack(self, steps=10):
        """
        Performs a sequence of Reidemeister moves which increase or maintain the number of 
        crossings in a diagram.  The number of such moves is the parameter steps.

        >>> K = random_knot(100)   #randomly generated knot diagram
        >>> K
        <Link: 1 comp; 10 cross>
        >>> K.backtrack(steps = 15)
        >>> K
        <Link: 1 comp; 27 cross>

        """
        from . import simplify
        
        L = simplify.backtrack(self,num_steps = steps)
        self.crossings = L.crossings
        self.labels = L.labels
        self.link_components = L.link_components
        self.name = L.name
