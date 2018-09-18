import numpy as np
import matplotlib.pyplot as plt
from chbench.basis import *
from chbench.visualization import *


s = GaussianOrbital(0.02, 0.02, 0.02, 0, 0, 0, [-5, 0, 0])
s2 = s.translate([10, 0, 0])

shift = 20
antibonding = ContractedGaussian(
    [1, -1],
    [s.translate([0, shift, 0]), s.translate([10, shift, 0])]
)

bonding = ContractedGaussian(
    [1, 1],
    [s.translate([0, -shift, 0]), s.translate([10, -shift, 0])]
)


# p_x = GaussianOrbital(0.02, 0.02, 0.0, 1, 0, 0)
# p_y = GaussianOrbital(0.02, 0.02, 0.0, 0, 1, 0)

nx = 100
ny = 100

surface = plot_gaussian_xy([-20, 20], [-20, 20], nx, ny, s, z=2)
plt.clabel(surface)

surface = plot_gaussian_xy([-20, 20], [-20, 20], nx, ny, s2, z=2)
plt.clabel(surface)

surface = plot_gaussian_xy(
    [-20, 20], [-20 + shift, 20 + shift], nx, ny, antibonding, z=2
)
plt.clabel(surface)
surface = plot_gaussian_xy(
    [-20, 20], [-20 - shift, 20 - shift], nx, ny, bonding, z=2
)
plt.clabel(surface)

plt.show()
