import MySQLdb

host = 'nmd.math.illinois.edu'     
root_password = '90957a5bce5140fefcd3'

knotdb_schema = """\
CREATE TABLE initial_knots (
 id integer primary key auto_increment,
 crossings integer,
 tetrahedra integer,
 tetrahedra_time integer, 
 volume float,
 volume_time float, 
 chern_simons float,
 chern_simons_time float,
 is_hyperbolic boolean, 
 alexander text,
 alexander_time float,
 alexander_genus_bound int, 
 alexander_monic boolean, 
 bridge_number int,
 bridge_number_time float,
 log_det float,
 hypertorsion_poly text,
 hypertorsion_poly_time float,
 hypertorsion_genus_bound int, 
 genus_upper_bound int,
 genus_upper_bound_time float
 )"""

def make_database():
    conn = MySQLdb.connect(host=host, user='root', passwd=root_password)
    cur = conn.cursor()
    cur.execute('DROP DATABASE random_knots')
    cur.execute('CREATE DATABASE random_knots')
    cur.execute('USE random_knots')
    cur.execute(knotdb_schema)
    for c in range(3, 1001):
        cur.execute('INSERT INTO initial_knots (crossings) VALUES (%s)', [c])
    for column in ['id', 'crossings', 'tetrahedra', 'volume']:
        cur.execute('ALTER TABLE initial_knots ADD INDEX (' + column +  ')')
