import MySQLdb, os, sys, re, time, random
import knot_sample
from sage.all import ZZ, PolynomialRing

host = 'nmd.math.illinois.edu'
user = '3mflds4ever'
user_password = '2a348baa47770ffe345'

class KnotDatabase:
    def __init__(self):
        self.connection = MySQLdb.connect(
                host=host, user=user, passwd=user_password)
        cursor = self.connection.cursor()
        cursor.execute('USE random_knots')
        cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA='random_knots' and TABLE_NAME='initial_knots'""")
        self.columns = [x[0] for x in cursor.fetchall()]
        self.cursor = cursor

    def execute_and_commit(self, command, arguments=None):
        self.cursor.execute(command, arguments)
        self.connection.commit()
        
    def update_entry(self, crossings, column, entry):
        command  = 'UPDATE initial_knots SET ' + column + '=%s where crossings=%s'
        self.execute_and_commit(command, [entry, crossings])

    def compute_entry(self, crossings, column, function, knot_or_exterior='exterior', **kwargs):
        start_time = time.time()
        X = getattr(knot_sample, knot_or_exterior)(crossings)
        ans = function(X, **kwargs)
        time_elapsed = time.time() - start_time
        self.update_entry(crossings, column, ans)
        timer_column = column + '_time'
        if timer_column in self.columns:
            self.update_entry(crossings, timer_column, time_elapsed)

    def store_polynomial(self, name, crossings, poly, time_elapsed):
        self.update_entry(crossings, name, repr(poly).replace(' ', ''))
        self.update_entry(crossings, name + '_time', time_elapsed)
        self.update_entry(crossings, name + '_genus_bound', poly.degree()/2)
        self.update_entry(crossings, name + '_monic', poly.is_monic())

    def compute_alexander(self, crossings):
        start_time = time.time()
        X = knot_sample.exterior(crossings)
        poly = X.alexander_polynomial(X, try_hard_to_shorten_relators=False)
        time_elapsed = time.time() - start_time
        self.store_polynomial('alexander', crossings, poly, time_elapsed)

    def compute_alexander_magma(self, crossings):
        import alexander
        start_time = time.time()
        X = knot_sample.exterior(crossings)
        poly = alexander.magma(X)
        time_elapsed = time.time() - start_time
        self.store_polynomial('alexander_magma', crossings, poly, time_elapsed)

    def compute_alexander_dror(self, crossings):
        import alexander
        start_time = time.time()
        X = knot_sample.knot(crossings)
        poly = alexander.dror(X)
        time_elapsed = time.time() - start_time
        self.store_polynomial('alexander_dror', crossings, poly, time_elapsed)

    def clear_column(self, col_name):
        self.execute_and_commit('UPDATE initial_knots SET ' + col_name + '=NULL')

    def clear_matching_columns(self, col_name_prefix):
        for column in self.columns:
            if column.startswith(col_name_prefix):
                self.clear_column(column)

    def get_entry(self, crossings, column):
        self.cursor.execute('SELECT ' + column + ' FROM initial_knots WHERE crossings=%d' %crossings)
        return self.cursor.fetchone()[0]
        

def eval_poly_column(dataframe, col_name):
    R = PolynomialRing(ZZ, 'a')
    def eval_poly(p):
        return None if p is None else R(p)
    dataframe[col_name] = map(eval_poly, dataframe[col_name])

def dataframe():
    import pandas
    KD = KnotDatabase()
    dataframe = pandas.read_sql("SELECT * FROM random_knots.initial_knots", KD.connection)
    for column in ['alexander', 'alexander_magma', 'alexander_dror']:
        eval_poly_column(dataframe, column)
    # remove any completely empty columns
    dataframe = dataframe.dropna(axis='columns', how='all')
    return dataframe
        
    
