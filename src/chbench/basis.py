import numpy as np


class LinearSuperposition:

    def __init__(self, coefficients, functions):
        assert(len(functions) == len(coefficients)),\
            "The number of coefficients and functions must match"
        self.coefficients = coefficients
        self.functions = functions

    def __call__(self, *args):
        return sum(
            (g[0] * g[1])(*args)
            for g in zip(self.functions, self.coefficients)
        )

    def __mul__(self, beta):
        coefficients = beta * np.array(self.coefficients)
        g = self.copy()
        g.coefficients = coefficients
        return g

    def __rmul__(self, beta):
        """
        Multiplication by a scalar on the left
        """
        return self * beta

    def __radd__(self, other):
        return self + other

    def __add__(self, other):
        if isinstance(other, LinearSuperposition):
            functions = list(self.functions) + list(other.functions)
            coefficients = list(self.coefficients) + list(other.coefficients)
        else:
            raise NotImplementedError(
                'To sum {0} and {0} is not yet implemented'.format(
                    type(other), type(self)
                )
            )
        return LinearSuperposition(coefficients, functions)

    def copy(self):
        functions = [g.copy() for g in self.functions]
        return self.__class__(self.coefficients, functions)


class Orbital(LinearSuperposition):

    def __init__(self):
        LinearSuperposition.__init__(self, [1.0], [self])

    def __call__(self, x, y, z):
        raise NotImplementedError


class PlaneWave(Orbital):

    def __init__(self, k):
        assert len(k) == 3, 'Length of k has to be 3'
        Orbital.__init__(self)
        self.k = np.array(k)

    def copy(self):
        return PlaneWave(self.k)

    def __call__(self, x, y, z):
        return self.coefficients[0] * np.exp(
            np.complex(0, 1) * (self.k[0] * x + self.k[1] * y + self.k[2] * z)
        )


class GaussianOrbital(Orbital):

    def __init__(self, alphax, alphay, alphaz, lx, ly, lz, center):
        Orbital.__init__(self)
        assert(len(center) == 3)
        self.lx = lx
        self.ly = ly
        self.lz = lz
        self.alphax = alphax
        self.alphay = alphay
        self.alphaz = alphaz
        self.center = center

    def copy(self):
        g = GaussianOrbital(
            self.alphax, self.alphay, self.alphaz,
            self.lx, self.ly, self.lz, self.center
        )
        g.coefficients = self.coefficients
        return g

    def translate(self, newcenter):
        assert len(newcenter) == 3, 'Length of translation vec. has to be 3'
        g = self.copy()
        g.center = np.array(g.center) + np.array(newcenter)
        return g

    def __call__(self, X, Y, Z):
        return self.coefficients[0] * np.exp(
            - self.alphax * (X - self.center[0]) ** 2
            - self.alphay * (Y - self.center[1]) ** 2
            - self.alphaz * (Z - self.center[2]) ** 2
        ) * (X - self.center[0]) ** (self.lx
        ) * (Y - self.center[1]) ** (self.ly
        ) * (Z - self.center[2]) ** self.lz


class ContractedGaussian(LinearSuperposition):

    def __init__(self, coefficients, functions):
        LinearSuperposition.__init__(self, coefficients, functions)

    def translate(self, newcenter):
        assert len(newcenter) == 3, 'Length of translation vec. has to be 3'
        g = self.copy()
        g.functions = [g.translate(newcenter) for g in self.functions]
        return g
