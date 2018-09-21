import numpy as np
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
    assert(newp.translate([1, 1, 1]).center[0] == 1)
    assert(newp.translate([1, 1, 1]).center[1] == 1)
    assert(newp.translate([1, 1, 1]).center[2] == 1)

    d = GaussianOrbital(0.01, 0.8, 0.0, 0, 2, 0, center)

    pd = d * 2 + p * 3
    assert(isinstance(pd, ContractedGaussian))
    assert(pd.functions[0])
    assert(pd.functions[0].beta == 2.0)
    assert(pd.functions[1].beta == 3.0)

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
    assert(g.functions)
    assert(g.coefficients is not None)
    assert(g(0, 0, 0) == 2.0)

    gg = p * 32 + g
    assert(isinstance(gg, ContractedGaussian))
    assert(gg.functions[0].lx == 1.0)
    assert(gg.functions[0].beta == 32.0)

    assert(2.0 == gg(0, 0, 0))
    doublegg  = gg * np.complex(0, 1)
    assert(np.complex(0, 2.0) == doublegg(0, 0, 0))

    dcontracted = ContractedGaussian(
        [1, 1],
        [gg, gg]
    )
    assert(dcontracted)
    assert(dcontracted(0,0,0) == 4.0)
