import chbench.algebra


class Group(chbench.algebra.Monoid):

    def __init__(self, elements, operation, e, inverse_operation):
        chbench.algebra.Monoid.__init__(self, elements, operation, e)
        assert(callable(inverse_operation)), (
            'The inverse operation must be a callable object'
        )
        self.inverse_operation = inverse_operation

    def inverse(self, element):
        e = self.inverse_operation(element)
        assert(e in self), (
            'The inverse of the element does not seem to be in the group'
        )
        return e

    def copy(self):
        return Group(
            self.elements, self.operation, self.e, self.inverse_operation
        )


class ZMod(Group):
    def __init__(self, n):
        Group.__init__(
            self, range(1, n), lambda x, y: x * y % n, 1, self._inverse)
        self.n = n

    def _inverse(self, element):
        return [self(element, x) for x in self.elements].index(self.e) + 1
