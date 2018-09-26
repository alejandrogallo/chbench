class Set(set):
    pass


class SemiGroup:

    def __init__(self, elements, operation):
        self.elements = Set(elements)
        assert(callable(operation)), 'The operation must be a callable object'
        self.operation = operation

    def __call__(self, x, y):
        assert(x in self), 'First argument must be an element'
        assert(y in self), 'Second argument must be an element'
        r = self.operation(x, y)
        assert(r in self), (
            'The result does not pertain to the algebraic structure'
        )
        return r

    def __contains__(self, element):
        return element in self.elements

    def __rmul__(self, element):
        assert(element in self)
        g = self.copy()
        new_elements = [g(element, e) for e in self.elements]
        g.set_elements(new_elements)
        return g

    def set_elements(self, elements):
        self.selements = Set(elements)

    def copy(self):
        return SemiGroup(self.elements, self.operation)

    def pow(self, element, exponent):
        e = element
        for i in range(exponent - 1):
            e = self(element, e)
        assert(e in self)
        return e


class Monoid(SemiGroup):

    def __init__(self, elements, operation, e):
        SemiGroup.__init__(self, elements, operation)
        self.e = e

    def copy(self):
        return Monoid(self.elements, self.operation, self.e)

    def pow(self, element, exponent):
        if exponent == 0:
            return self.e
        else:
            return super(Monoid, self).pow(element, exponent)
