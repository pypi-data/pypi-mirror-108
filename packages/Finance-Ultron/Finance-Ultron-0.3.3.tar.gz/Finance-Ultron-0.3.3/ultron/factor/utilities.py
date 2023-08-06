import numpy as np
import numba as nb

@nb.njit(nogil=True, cache=True)
def agg_mean(groups, x):
    max_g = groups.max()
    length, width = x.shape
    res = np.zeros((max_g+1, width), dtype=np.float64)
    bin_count = np.zeros(max_g+1, dtype=np.int32)

    for i in range(length):
        for j in range(width):
            res[groups[i], j] += x[i, j]
        bin_count[groups[i]] += 1

    for i in range(max_g+1):
        curr = bin_count[i]
        for j in range(width):
            res[i, j] /= curr
    return res


def encode(obj: object) -> str:
    encoded = base64.encodebytes(pickle.dumps(obj))
    return encoded.decode('ascii')


def decode(str_repr: str):
    encoded = str_repr.encode('ascii')
    return pickle.loads(base64.decodebytes(encoded))

def list_eq(lhs: list, rhs: list):
    if not lhs and not rhs:
        return True

    if len(lhs) != len(rhs):
        return False

    for i, v1 in enumerate(lhs):
        if v1 != rhs[i]:
            return False
    return True