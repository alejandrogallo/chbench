import numpy as np
import matplotlib.pyplot as plt
from chbench.basis import *
from chbench.visualization import *
import chbench.parser.basis



nx = 400
ny = nx
k = 0
N = 10
a = 0.74
alpha = 1
xlims = [-2, N * a + 1]
ylims = [-2, 2]

hydrogens = np.array([[i * a, 0, 0] for i in range(N)])
#hydrogens = np.array([[np.sin(i * a), np.cos(i * a), 0] for i in range(N)])

ki = N /2
ki = 1
def modulator(x, ki):
    global a, N
    return np.exp(np.complex(0,1) * x * ki * 2 * np.pi / (a * N))

bs = chbench.parser.basis.get('cc-pvdz', 'H')
bs = chbench.parser.basis.get('sto-3g', 'H')
s = GaussianOrbital(alpha, alpha, alpha, 0, 0, 0, [0, 0, 0])
s = bs.shells[0].functions[0]


print('Building new coeffs')
coefficients = [modulator(i * a, ki) for i in range(N)]
print('Building new gaussians')
gaussians = [s.translate(h) for h in hydrogens]

print('Building new cgaussians')
b = ContractedGaussian(coefficients, gaussians)

print('Building new surface')
surface = plot_gaussian_xy(
    xlims, ylims, nx, ny, lambda x,y,z: np.real(b(x,y,z)), z=0, fill=True,
)

for i, g in enumerate(gaussians):
    newg = g * coefficients[i]
    gxlims = [i * a -1 , i * a +1] #[g.center[0] - 1, g.center[0] + 1]
    plot_gaussian_xy(
        xlims, ylims, nx, ny, lambda x,y,z: np.real(newg(x,y,z)),
        z=0, fill=False, alpha=0.1, colors='k'
    )

plt.scatter(hydrogens[:,0], hydrogens[:,1], color='k')

# X = np.linspace(xlims[0], xlims[1], N * nx)
# plt.plot(X, modulator(X, ki), 'r')

plt.title(r'$k = \frac{{2\pi {k}}}{{aN}}$'.format(k=ki))

plt.show()
