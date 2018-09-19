import numpy as np
import matplotlib.pyplot as plt


def plot_gaussian_xy(xrange, yrange, nx, ny, gaussian, z=0, **kwargs):
    x = np.linspace(*xrange + [nx])
    y = np.linspace(*yrange + [ny])
    X, Y = np.meshgrid(x, y)
    Z = gaussian(X, Y, X * 0 + z)
    return plt.contour(X, Y, Z, **kwargs)


def plot_gaussian_with_surface_xy(xrange, yrange, nx, ny, gaussian, z=0, **kwargs):
    from mpl_toolkits.mplot3d import axes3d
    x = np.linspace(*xrange + [nx])
    y = np.linspace(*yrange + [ny])
    X, Y = np.meshgrid(x, y)
    Z = gaussian(X, Y, X * 0 + z)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, alpha=0.5, rstride=1, cstride=1, cmap='autumn_r')
    ax.contour(X, Y, Z, offset=-1)
    return fig


def contour3d(xrange, yrange, zrange, nx, ny, nz, gaussian, **kwargs):
    from mayavi import mlab
    x = np.linspace(*xrange + [nx])
    y = np.linspace(*yrange + [ny])
    z = np.linspace(*zrange + [nz])
    X, Y, Z = np.meshgrid(x, y, z)
    f = gaussian(X, Y, Z)
    # TODO: implement contour3d with XYZ
    #s = mlab.contour3d(X, Y, Z, f, contours=3, transparent=True)
    return mlab.contour3d(f, contours=5, transparent=True)


def plot_atoms_mayavi(atoms, **kwargs):
    # docs.enthought.com/mayavi/mayavi/auto/
    # mlab_helper_functions.html#mayavi.mlab.points3d
    from mayavi import mlab
    from ase.data import covalent_radii
    x = [a.position[0] for a in atoms]
    y = [a.position[1] for a in atoms]
    z = [a.position[2] for a in atoms]
    r = [covalent_radii[a.number] for a in atoms]
    pts = mlab.points3d(x, y, z, **kwargs)
    pts.mlab_source.dataset.point_data.scalars = r
    return pts
