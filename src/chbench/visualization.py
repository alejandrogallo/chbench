import numpy as np
import matplotlib.pyplot as plt


def plot_gaussian_xy(xrange, yrange, nx, ny, gaussian, z=0, **kwargs):
    x = np.linspace(*xrange + [nx])
    y = np.linspace(*yrange + [ny])
    X, Y = np.meshgrid(x, y)
    Z = gaussian(X, Y, X * 0 + z)
    return plt.contour(X, Y, Z, **kwargs)
