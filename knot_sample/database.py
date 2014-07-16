import sqlite3, bz2

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



