import sqlite3, bz2, zipfile, os

knot_schema = """
CREATE TABLE knots (
 id integer primary key,
 crossings integer,
 PD text)
"""

def make_database():
    conn = sqlite3.connect('knots.sqlite')
    cur = conn.cursor()
    cur.execute(knot_schema)
    cur.execute('CREATE INDEX cross_index ON knots (crossings)')
    for line in bz2.BZ2File('./knot_database.bz2'):
        cross, PD = line.strip().split('\t')
        PD = PD.replace(' ', '')
        cur.execute('INSERT INTO knots (crossings, PD) VALUES (?, ?)', (int(cross), PD))
    conn.commit()
    conn.close()

def add_tri_column():
    conn = sqlite3.connect('knots.sqlite')
    cur = conn.cursor()
    cur.execute('ALTER TABLE knots ADD triangulation blob')
    conn.commit()
    conn.close()

def add_triangulations():
    conn = sqlite3.connect('knots.sqlite')
    cur = conn.cursor()
    exteriors = zipfile.ZipFile('exteriors.zip')
    for filename in exteriors.namelist():
        if filename[-1] != '/':
            cross = int(os.path.basename(filename).split('.')[0])
            tri_blob = sqlite3.Binary(exteriors.open(filename).read())
            cur.execute('UPDATE knots SET triangulation=(?) where crossings=(?)', (tri_blob, cross))
    conn.commit()
    conn.close()
    
