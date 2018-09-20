import chbench.visualization.vispy as vp
import vispy
import ase.io
import os
from chbench.basis import *


benzenepath = os.path.join(
    os.path.dirname(__file__),
    'data', 'benzene.xyz'
)
atoms = ase.io.read(benzenepath)

canvas, view = vp.init()

spheres = [vp.Atom(a, edge_color='red') for a in atoms]

for s in spheres:
    view.add(s.sphere)

g = GaussianOrbital(2, 2, 2, 0, 0, 1, [0,0,0])
s = g.translate(atoms[1].position)
s = g.translate([0, 0, 2])
r = [-3, 3]
n = 100

iso = vp.OrbitalIsoSurface(
    s,
    r, r, r, n, n, n,
    level=0.02,
    shading='smooth',
)
view.add(iso.isosurface)

iso = vp.OrbitalIsoSurface(
    s,
    r, r, r, n, n, n,
    level=-0.002
)
view.add(iso.isosurface)


view.add(vp.xyzaxis())

if __name__ == "__main__":
    canvas.app.run()
