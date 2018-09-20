import chbench.visualization.vispy as vp
import vispy
import ase.io
import ase.atom
import os
from chbench.basis import *
import chbench.parser.basis


nx = 100
ny = nx
k = 0
N = 10
a = 0.74
alpha = 1
xlims = [-2, N * a + 1]
ylims = [-2, 2]

atoms = np.array([
    ase.atom.Atom(position=[i * a, 0, 0], symbol='H') for i in range(N)
])

canvas, view = vp.init()

spheres = [vp.Atom(a, edge_color='red') for a in atoms]

for s in spheres:
    view.add(s.sphere)

ki = N /2
ki = 0
def modulator(x, ki):
    global a, N
    return np.exp(np.complex(0,1) * x * ki * 2 * np.pi / (a * N))

#bs = chbench.parser.basis.get('cc-pvdz', 'H')
bs = chbench.parser.basis.get('sto-3g', 'H')
s = bs.shells[0].functions[0]
s = GaussianOrbital(alpha, alpha, alpha, 0, 0, 1, [0, 0, 0])


print('Building new coeffs')
coefficients = [modulator(i * a, ki) for i in range(N)]
print('Building new gaussians')
gaussians = [s.translate(h.position) for h in atoms]

print('Building new cgaussians')
b = ContractedGaussian(coefficients, gaussians)



iso = 0.3
for level in [-iso, iso]:
    surface = vp.OrbitalIsoSurface(
        lambda x,y,z: np.real(b(x,y,z)),
        xlims, ylims, ylims, nx, nx, nx,
        level=level,
        color=(0.5, 0.0, 1, 0.3),
        shading='smooth',
    )
    #view.add(surface.isosurface)

for g in gaussians:
    surface = vp.OrbitalIsoSurface(
        lambda x,y,z: np.real(g(x,y,z)),
        xlims, ylims, ylims, nx, nx, nx,
        level=level,
        color=(0.5, 0.5, 1, 0.1),
    )
    view.add(surface.isosurface)



view.add(vp.xyzaxis())

if __name__ == "__main__":
    canvas.app.run()
