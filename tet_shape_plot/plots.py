import nplot
import knot_sample
import numpy as np
import matplotlib.pyplot as plt
import mpltools
import pandas as pd

mpltools.style.use('grayscale')

def compute_data(N):
    shapes = []
    for c in range(1001)[-N:]:
        M = knot_sample.exterior(c)
        shapes += M.tetrahedra_shapes('rect', fixed_alignment=False)
    real = np.array([s.real() for s in shapes])
    imag = np.array([s.imag() for s in shapes])
    return real, imag

def make_hexbin_plot():
    df = pd.read_pickle('shapes.pickle')
    F = nplot.Figure()
    hexs = F.axis.hexbin(df.real, df.imag, gridsize = 30, cmap=plt.cm.gray_r)
    F.figure.colorbar(hexs)
    F.axis.set_aspect('equal')
    F.axis.set_ylim(ymin=0.0)
    F.draw()
    return F

