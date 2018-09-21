import numpy as np
import matplotlib.pyplot as plt
from chbench.basis import *
from chbench.visualization import *


p = PlaneWave([0, 1, 0])
p2 = PlaneWave([1, 1, 0])
p3 = PlaneWave([1, 4, 0])

g = 0*p + 0*p2 + p3 + 10 * GaussianOrbital(2, 2, 2, 0, 1, 0, [0,0,0])

nx = 100
ny = 100
lim = 4

#surface = plot_gaussian_with_surface_xy(
surface = plot_gaussian_xy(
    [-lim, lim], [-lim, lim], nx, ny, g, z=0, fill=False
)
plt.clabel(surface)


plt.show()

