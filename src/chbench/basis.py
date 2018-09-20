import numpy as np


class GaussianOrbital:

    def __init__(self, alphax, alphay, alphaz, lx, ly, lz, center):
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

    def __mul__(self, beta):
        new_g = self.copy()
        new_g.beta *= beta
        return new_g

    def __add__(self, other):
        if isinstance(other, ContractedGaussian):
            gaussians = [self.copy()] + other.gaussians
            coefficients = [1] + list(other.coefficients)
        elif isinstance(other, GaussianOrbital):
            gaussians = [self.copy(), other.copy()]
            coefficients = [1, 1]
        else:
            raise NotImplementedError('This operation is not implemented')
        return ContractedGaussian(coefficients, gaussians)

    def __call__(self, X, Y, Z):
        return self.beta * np.exp(
            - self.alphax * (X - self.center[0]) ** 2
            - self.alphay * (Y - self.center[1]) ** 2
            - self.alphaz * (Z - self.center[2]) ** 2
        ) * (X - self.center[0]) ** (self.lx
        ) * (Y - self.center[1]) ** (self.ly
        ) * (Z - self.center[2]) ** self.lz


class ContractedGaussian:

    def __init__(self, coefficients, gaussians):
        assert(len(gaussians) == len(coefficients))
        self.coefficients = np.array(coefficients)
        self.gaussians = gaussians

    def __call__(self, X, Y, Z):
        return sum(
            (g[0] * g[1])(X,Y,Z)
            for g in zip(self.gaussians, self.coefficients)
        )

    def __mul__(self, beta):
        coefficients = beta * np.array(self.coefficients)
        g = self.copy()
        g.coefficients = coefficients
        return g

    def copy(self):
        gaussians = [g.copy() for g in self.gaussians]
        cs = self.coefficients
        return ContractedGaussian(cs, gaussians)

    def translate(self, newcenter):
        assert len(newcenter) == 3, 'Length of translation vec. has to be 3'
        self.gaussians = [g.translate(newcenter) for g in self.gaussians]
