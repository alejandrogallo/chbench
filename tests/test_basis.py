from chbench.basis import *


def test_simple_gaussian():
    center = [0, 0, 0]
    p = GaussianOrbital(0.2, 0.2, 0.2, 1, 0, 0, center)

    assert(p.beta == 1.0)
    assert(p.alphax == 0.2)
    assert(p.lx == 1)
    assert(abs(p(1, 0, 1) - 0.670320046035639) < 1e-5)

    newp = p * 2
    assert(p.beta == 1.0)
    assert(newp.beta == 2.0)
    assert(abs(p(1, 0, 1) - 0.670320046035639) < 1e-5)
    assert(abs(newp(1, 0, 1) - 2 * 0.670320046035639) < 1e-5)

    d = GaussianOrbital(0.01, 0.8, 0.0, 0, 2, 0, center)

    pd = d * 2 + p * 3
    assert(isinstance(pd, ContractedGaussian))
    assert(pd.gaussians[0])
    assert(pd.gaussians[0].beta == 2.0)
    assert(pd.gaussians[1].beta == 3.0)

    newd = d.copy()
    newd.beta = 32
    assert(d.beta == 1.0)

    try:
        newd + 2
    except NotImplementedError:
        assert(True)
    else:
        assert(False)


def test_simple_cgaussian():
    center = [0, 0, 0]
    s = GaussianOrbital(0.01, 0.8, 0.0, 0, 0, 0, center)
    p = GaussianOrbital(0.2, 0.2, 0.2, 1, 0, 0, center)

    g = ContractedGaussian([2, 3], [s, p])
    assert(g.gaussians)
    assert(g.coefficients)
    assert(g(0, 0, 0) == 2.0)

    gg = p * 32 + g
    assert(isinstance(gg, ContractedGaussian))
    assert(gg.gaussians[0].lx == 1.0)
    assert(gg.gaussians[0].beta == 32.0)
