import os
import ase.io
from chbench.visualization import *
from mayavi import mlab


benzenepath = os.path.join(
    os.path.dirname(__file__),
    'data', 'benzene.xyz'
)
atoms = ase.io.read(benzenepath)

plot_atoms_mayavi(atoms, resolution=10)
mlab.show()
