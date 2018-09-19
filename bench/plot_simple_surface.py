import numpy as np
import matplotlib.pyplot as plt
from chbench.basis import *
from chbench.visualization import *


s = GaussianOrbital(0.02, 0.02, 0.02, 0, 0, 0, [-5, 0, 0])
s2 = s.translate([10, 0, 0])

shift = 0
antibonding = ContractedGaussian(
    [1, -1],
    [s.translate([0, shift, 0]), s.translate([10, shift, 0])]
)

bonding = ContractedGaussian(
    [1, 1],
    [s.translate([0, -shift, 0]), s.translate([10, -shift, 0])]
)


nx = 100
ny = 100

surface = plot_gaussian_with_surface_xy(
    [-20, 20], [-20, 20], nx, ny, antibonding, z=2
)
plt.show()
