"""
So far, there are 152 cases where both SnapPy and Magma have computed
the alexander polynomial and gotten the same answer.

There are 22 cases where SnapPy gets the impossible answer of 0, for example
those with 178, 179, 185, 186 crossings.
"""


import pandas as pd
import knot_db

df = knot_db.dataframe()
bad_snappy = df[df.alexander==0]
da = df.dropna(subset = ['alexander', 'alexander_magma'])
