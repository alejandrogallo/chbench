from chbench.algebra.group import *


def test_simple():
    g = ZMod(7)
    assert(g(1, 1) == 1)
    assert(g(1, g.e) == 1)
    assert(g.inverse(1) == 1)
    assert(g.inverse(2) == 4)
    assert(g.inverse(3) == 5)
    assert(g.inverse(4) == 2)
    assert(g.inverse(5) == 3)
    assert(g.inverse(6) == 6)
    two_g = 2 * g
    assert(len(two_g.elements) == 6)
    assert(g.pow(2, 0) == g.e)
    assert(g.pow(2, 1) == 2)
    assert(g.pow(2, 2) == 4)
    assert(g.pow(2, 3) == g.e)
