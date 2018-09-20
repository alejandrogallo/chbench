from chbench.basis import GaussianOrbital, ContractedGaussian
from chbench.parser.utils import *
from chbench.parser.regex import *
import re
import os


gaussian_header = re.compile(r"^([a-zA-Z]+) (\d+)$")
angular_header = re.compile(r"^([A-Z]+) (\d) (\d+\.\d+)$")
gaussian_separator = re.compile(r"^\*\*\*+$")


class ShellG94:

    def __init__(self, lines):
        assert(isinstance(lines, list)), 'Lines must be a python list'
        self.lines = lines
        self.exponents = []
        self.coefficients = []
        self.l = None
        self.lsymbol = None
        self.functions = []
        self.parse()

    def translate(self, newcenter):
        self.functions = [f.translate(newcenter) for f in self.functions]

    @staticmethod
    def get_l_from_symbol(symbol):
        symbols = 'SPDFG'
        return symbols.index(symbol)

    def generate_l(self):
        return list({
            (lx, ly, lz)
            for lx in range(0, self.l+1)
            for ly in range(0, self.l+1)
            for lz in range(0, self.l+1)
            if lx + ly + lz == self.l
        })

    def parse(self):
        lines = clean_lines(self.lines)

        m = angular_header.match(lines.pop(0))
        self.lsymbol = m.group(1)
        self.l = ShellG94.get_l_from_symbol(self.lsymbol)
        nbasis_functions = int(m.group(2))
        for line in lines:
            m = parse_vector(line, None, float)
            self.exponents.append(m[0])
            self.coefficients.append(m[1:])

        for l in self.generate_l():
            for i in range(len(self.coefficients[0])):
                coefficients = [c[i] for c in self.coefficients]
                gaussians = [
                    GaussianOrbital(
                        a, a, a,
                        l[0], l[1], l[2], [0, 0, 0]
                    )
                    for a in self.exponents
                ]

                self.functions.append(
                    ContractedGaussian(coefficients, gaussians)
                )


class GaussianG94BaisSet:

    def __init__(self, lines):
        assert(isinstance(lines, list)), 'Lines must be a python list'
        assert(lines), 'Lines must not be empty'
        self.lines = lines
        self.element = None
        self.shells = []

        self.parse()

    def translate(self, newcenter):
        assert len(newcenter) == 3, 'Length of translation vec. has to be 3'
        self.shells = [s.translate(newcenter) for s in self.shells]

    def parse(self):
        self.lines = clean_lines(self.lines)
        lines = self.lines
        parsing = True

        m = gaussian_header.match(lines.pop(0))
        self.element = m.group(1)

        while lines:
            shell_lines = [lines.pop(0)]
            m = angular_header.match(shell_lines[0])
            angular = m.group(1)
            nbasis_functions = int(m.group(2))
            shell_lines += [lines.pop(0) for i in range(nbasis_functions)]
            self.shells.append(
                ShellG94(shell_lines)
            )


class BasisSetFileSearcher:

    def __init__(self, filepath, element):
        self.lines = []
        self.parse(filepath, element)

    def parse(self, filepath, element):
        lines = []
        record = False
        with open(filepath) as f:
            for line in f:
                try:
                    cline = clean_lines([line])[0]
                except IndexError:
                    continue
                m = gaussian_header.match(cline)
                if m and m.group(1) == element:
                    record = True

                m = gaussian_separator.match(cline)
                if m and record:
                    self.lines = lines
                    return


                if record:
                    lines.append(cline)

        raise Exception(
            'No info for element {0} found in {1}'.format(
                element, filepath
            )
        )



def get(basis_set, element):
    basis_data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data', 'basis'
    )
    assert(os.path.exists(basis_data_path))
    filepath = os.path.join(basis_data_path, basis_set + '.g94')
    lines = BasisSetFileSearcher(filepath, element).lines
    return GaussianG94BaisSet(lines)
