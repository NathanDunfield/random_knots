import spherogram, snappy, os, sqlite3, bz2

def small_triangulation(manifold, tries=100):
    M = manifold.without_hyperbolic_structure()
    ans = M.copy()
    for i in range(tries):
        M.randomize()
        if M.num_tetrahedra() < ans.num_tetrahedra():
            ans = M
    return ans

def small_triangulation_of_exterior(link, outer_tries=10, inner_tries=100):
    ans = None
    for i in range(outer_tries):
        M = small_triangulation(link.exterior())
        if ans is None or M.num_tetrahedra() < ans.num_tetrahedra():
            ans = M
    return ans.with_hyperbolic_structure()


class KnotDatabase:
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def _column_entry_for_knot(self, column, crossings):
        self.cursor.execute('SELECT %s FROM knots WHERE crossings=%d' % (column, int(crossings)))
        ans = self.cursor.fetchone()
        if ans is None:
            raise ValueError('No knot with %d crossings in database' % crossings)
        return ans[0]


    def knot(self, crossings):
        PD = self._column_entry_for_knot('PD', crossings)
        return spherogram.Link(eval(PD))

    def exterior(self, crossings):
        """
        Return a simplified triangulation of the exterior of the database knot
        with n crossings. 
        """
        tri_blob = self._column_entry_for_knot('triangulation', crossings)
        if tri_blob == None:
            raise ValueError('Triangulation for %d crossings is not known' % crossings)
        return snappy.Manifold(bz2.decompress(tri_blob))

    def available(self):
        return [a[0] for a in self.cursor.execute('SELECT crossings FROM knots').fetchall()]

module_path = os.path.dirname(__file__)
knot_db = KnotDatabase(module_path + '/knots.sqlite')
knot = knot_db.knot
exterior = knot_db.exterior
