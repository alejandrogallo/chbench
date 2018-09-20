import re


real_number = re.compile(r'(\+?-?\d+\.?\d*[Ee]?\+?-?\d*)')


def parse_vector(line, length, dtype):
    m = real_number.findall(line)
    if not m:
        raise SyntaxError(
            'Line "{0}" does not seem to be a vector'.format(line)
        )
    elif length is None:
        return [dtype(i) for i in m]
    elif len(m) != length:
        raise SyntaxError(
            'Line "{0}" is a longer vector than expected ({1})'.format(
                line, length
            )
        )
    else:
        return [dtype(m[i]) for i in range(length)]


