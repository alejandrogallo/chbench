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

    def copy(self):
        functions = [g.copy() for g in self.functions]
        return ContractedGaussian(self.coefficients, functions)


class Orbital:

    def __init__(self):
        # This is a constant so that we can multiply by scalars
        self.beta = 1.0

    def __call__(self, x, y, z):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    def __mul__(self, beta):
        """
        Multiplication by a scalar on the right
        """
        new = self.copy()
        new.beta *= beta
        return new

    def __rmul__(self, beta):
        """
        Multiplication by a scalar on the left
        """
        new = self.copy()
        new.beta *= beta
        return new

    def __add__(self, other):
        if isinstance(other, LinearSuperposition):
            functions = [self.copy()] + other.functions
            coefficients = [1] + list(other.coefficients)
        elif isinstance(other, Orbital):
            functions = [self.copy(), other.copy()]
            coefficients = [1, 1]
        else:
            raise NotImplementedError('This operation is not implemented')
        return ContractedGaussian(coefficients, functions)


class PlaneWave(Orbital):

    def __init__(self, k):
        assert len(k) == 3, 'Length of k has to be 3'
        Orbital.__init__(self)
        self.k = np.array(k)

    def copy(self):
        return PlaneWave(self.k)

    def __call__(self, x, y, z):
        return self.beta * np.exp(
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
        self.beta = 1.0

    def copy(self):
        g = GaussianOrbital(
            self.alphax, self.alphay, self.alphaz,
            self.lx, self.ly, self.lz, self.center
        )
        g.beta = self.beta
        return g

    def translate(self, newcenter):
        assert len(newcenter) == 3, 'Length of translation vec. has to be 3'
        g = self.copy()
        g.center = np.array(g.center) + np.array(newcenter)
        return g

    def __call__(self, X, Y, Z):
        return self.beta * np.exp(
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
