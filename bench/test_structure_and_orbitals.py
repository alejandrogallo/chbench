import os
import ase.io
from chbench.basis import *
from chbench.visualization import *
from mayavi import mlab
import numpy as np

h2path = os.path.join(
    os.path.dirname(__file__),
    'data', 'h2.xyz'
)

atoms = ase.io.read(h2path)

alpha = 3
print(atoms[0])
print(atoms[1])
sl = GaussianOrbital(alpha, alpha, alpha, 0, 0, 0, atoms[0].position)
sr = GaussianOrbital(alpha, alpha, alpha, 0, 0, 0, atoms[1].position)

antibonding = ContractedGaussian(
    [1, -1],
    [sl, sr]
)
bonding = ContractedGaussian(
    [1, 1],
    [sl, sr]
)

r = [-1, 1]
npoints = 10


#contour3d(r, r, r, npoints, npoints, npoints, sl, opacity=0.2)
contour3d(r, r, r, npoints, npoints, npoints, antibonding, contours=3, opacity=0.2)
mlab.plot3d([-0.37, 0.37], [0, 0], [0,0], tube_radius=0.2)
plot_atoms_mayavi(atoms, resolution=10, scale_factor=10, opacity=0.4)

mlab.plot3d([1, 2], [0, 0], [0,0], tube_radius=0.2)

mlab.points3d(range(npoints), np.zeros(npoints), np.zeros(npoints), scale_factor=0.1)
mlab.points3d(np.zeros(npoints), range(npoints), np.zeros(npoints), scale_factor=0.1)
mlab.points3d(np.zeros(npoints), np.zeros(npoints), range(npoints), scale_factor=0.1)

mlab.outline()

mlab.show()
