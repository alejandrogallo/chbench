from chbench.parser.basis import *
from chbench.basis import *


def test_simple():
    lines = '''
    Li     0 
    S   9   1.00
       5988.0000000              0.0001330        
        898.9000000              0.0010250        
        205.9000000              0.0052720        
         59.2400000              0.0209290        
         19.8700000              0.0663400        
          7.4060000              0.1657750        
          2.9300000              0.3150380        
          1.1890000              0.3935230        
          0.4798000              0.1908700        
    S   9   1.00
       5988.0000000             -0.0000210        
        898.9000000             -0.0001610        
        205.9000000             -0.0008200        
         59.2400000             -0.0033260        
         19.8700000             -0.0105190        
          7.4060000             -0.0280970        
          2.9300000             -0.0559360        
          1.1890000             -0.0992370        
          0.4798000             -0.1121890        
    S   1   1.00
          0.0750900              1.0000000        
    S   1   1.00
          0.0283200              1.0000000        
    P   3   1.00
          3.2660000              0.0086300        0.123        
          0.6511000              0.0475380        0.0234        
          0.1696000              0.2097720        0.232         
    P   1   1.00
          0.0557800              1.0000000        
    P   1   1.00
          0.0205000              1.0000000        
    D   1   1.00
          0.1874000              1.0000000        
    D   1   1.00
          0.0801000              1.0000000        
    F   1   1.00
          0.1829000              1.0000000        
          '''.split('\n')

    bs = GaussianG94BaisSet(lines)
    assert(bs.element == 'Li')
    assert(len(bs.shells) == 10)

    # First shell
    assert(bs.shells[0].l == 0)
    assert(len(bs.shells[0].coefficients) == 9)
    assert(bs.shells[0].exponents[-1] == 0.4798)
    assert(bs.shells[0].coefficients[-1][0] == 0.19087)
    assert(bs.shells[1].l == 0)
    assert(bs.shells[2].l == 0)
    assert(bs.shells[3].l == 0)
    assert(bs.shells[4].l == 1)
    assert(bs.shells[7].l == 2)
    assert(bs.shells[9].l == 3)

    # First p shell
    p = bs.shells[4]
    assert(len(p.generate_l()) == 3)
    assert(len(p.functions) == 2 * 3)
    assert(isinstance(p.functions[0], ContractedGaussian))
    # They all have the same \vec l
    for function in p.functions:
        assert(len({(g.lx, g.ly, g.lz) for g in function.gaussians}) == 1)

    # First d shell
    d = bs.shells[7]
    assert(len(d.generate_l()) == 6)
    assert(len(d.functions) == 1 * 6)

    assert(len(bs.shells[9].generate_l()) == 10)


def test_get():
    bs = get('sto-3g', 'H')
    bs.translate([1, 1, 1])

    bs = get('cc-pvtz', 'H')

    try:
        bs = get('aacc-pvtz', 'H')
    except Exception:
        assert(True)
    else:
        assert(False)
