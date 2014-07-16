import os, sqlite3
import spherogram, snappy

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

    def knot(self, n):
        self.cursor.execute('SELECT PD FROM knots WHERE crossings=?', (int(n),))
        ans = self.cursor.fetchone()
        if ans is None:
            raise ValueError('No knot with %d crossings in database' % n)
        else:
            return spherogram.Link(eval(ans[0]))

    def exterior(self, n):
        """
        Return a simplified triangulation of the exterior of the database knot
        with n crossings.  Everytime a triangulation is generated, it is saved
        to disk so that future calls will always yield the same triangulation.
        """
        K = self.knot(n)
        triangulation_file = __path__[0] + '/exteriors/%d.tri' % n
        if os.path.exists(triangulation_file):
            M = snappy.Manifold(triangulation_file)
        else:
            M = small_triangulation_of_exterior(K)
            M.save(triangulation_file)
        return M

    def available(self):
        return [a[0] for a in self.cursor.execute('SELECT crossings FROM knots').fetchall()]


knot_db = KnotDatabase(__path__[0] + '/knots.sqlite')
knot = knot_db.knot
exterior = knot_db.exterior
