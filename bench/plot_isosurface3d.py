import numpy as np
import matplotlib.pyplot as plt
from chbench.basis import *
from chbench.visualization import *
from mayavi import mlab


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
nz = 100

surface = contour3d(
    [-20, 20], [-20, 20], [-20, 20], nx, ny, nz, antibonding, z=2
)
mlab.show()
