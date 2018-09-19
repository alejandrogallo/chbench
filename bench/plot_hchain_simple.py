import numpy as np
import matplotlib.pyplot as plt
from chbench.basis import *
from chbench.visualization import *



nx = 100
ny = 100
k = 0
N = 20
a = 0.74
alpha = 1
xlims = [-2, N * a + 1]
ylims = [-2, 2]

ki = N /2
ki = 1
def modulator(x, ki):
    global a, N
    return np.exp(np.complex(0,1) * x * ki * 2 * np.pi / (a * N))

s = GaussianOrbital(alpha, alpha, alpha, 0, 0, 0, [0, 0, 0])

coefficients = [modulator(i * a, ki) for i in range(N)]
gaussians = [s.translate([i * a, 0, 0]) for i in range(N)]

b = ContractedGaussian(coefficients, gaussians)


surface = plot_gaussian_xy(
    xlims, ylims, nx, ny, lambda x,y,z: np.real(b(x,y,z)), z=0, fill=True,
)

for i, g in enumerate(gaussians):
    newg = g * coefficients[i]
    #gxlim = [g.center[0] - 1, g.center[0] + 1]
    plot_gaussian_xy(
        xlims, ylims, nx, ny, lambda x,y,z: np.real(newg(x,y,z)),
        z=0, fill=False, alpha=0.2, colors='k'
    )

plt.scatter([i * a for i in range(N)], [0] * N, color='k')
X = np.linspace(xlims[0], xlims[1], N * nx)
plt.plot(X, modulator(X, ki), 'r')
#plt.clabel(surface)



plt.show()
