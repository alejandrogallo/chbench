try:
    import vispy
except ImportError:
    print('You do not have vispy, you need to install it')
import ase.atom
import vispy.scene
import vispy.color
import vispy.scene.visuals
from vispy.visuals.transforms import STTransform
from ase.data import covalent_radii
import numpy as np


from vispy.scene.visuals import (
    Axis
)


def xyzaxis():
    # Create an XYZAxis visual
    axis = vispy.scene.visuals.XYZAxis()
    s = STTransform(translate=(0, 0), scale=(50, 50, 50, 1))
    affine = s.as_matrix()
    axis.transform = affine
    return axis


def init(**kwargs):
    canvas = vispy.scene.SceneCanvas(
        keys='interactive', show=True, **kwargs
    )
    # Set up a viewbox to display the cube with interactive arcball
    view = canvas.central_widget.add_view()
    view.bgcolor = '#ffffff'
    view.camera = 'turntable'
    view.padding = 0
    return canvas, view


class OrbitalVolume:

    def __init__(
            self, orbital, xrange, yrange, zrange, nx, ny, nz, **kwargs
            ):
        x = np.linspace(*xrange + [nx])
        y = np.linspace(*yrange + [ny])
        z = np.linspace(*zrange + [nz])
        X, Y, Z = np.meshgrid(x, y, z)
        f = orbital(X, Y, Z)
        self.volume = vispy.scene.visuals.Volume(
            f, **kwargs
        )
        xscale = (xrange[1] - xrange[0])  / nx
        yscale = (yrange[1] - yrange[0])  / ny
        zscale = (zrange[1] - zrange[0])  / nz
        self.volume.transform = STTransform(
            scale=[xscale, yscale, zscale],
            translate=[xrange[0], yrange[0], zrange[0]]
        )


class OrbitalIsoSurface:

    def __init__(
            self, orbital, xrange, yrange, zrange, nx, ny, nz, **kwargs
            ):
        x = np.linspace(*xrange + [nx])
        y = np.linspace(*yrange + [ny])
        z = np.linspace(*zrange + [nz])
        X, Y, Z = np.meshgrid(x, y, z)
        f = orbital(X, Y, Z)
        self.isosurface = vispy.scene.visuals.Isosurface(
            f, **kwargs
        )
        xscale = (xrange[1] - xrange[0])  / nx
        yscale = (yrange[1] - yrange[0])  / ny
        zscale = (zrange[1] - zrange[0])  / nz
        self.isosurface.transform = STTransform(
            scale=[xscale, yscale, zscale],
            translate=[xrange[0], yrange[0], zrange[0]]
        )



class Atom(vispy.scene.visuals.Sphere):

    def __init__(self, atom, **kwargs):
        import ase.data.colors
        assert(isinstance(atom, ase.atom.Atom))
        self.atom = atom

        if not kwargs.get('color'):
            kwargs['color'] = ase.data.colors.jmol_colors[int(self.atom.mass)]

        self.sphere = vispy.scene.visuals.Sphere(
            name=self.atom.symbol,
            radius=covalent_radii[self.atom.number],
            **kwargs
        )
        self.sphere.transform = STTransform(translate=self.atom.position)
