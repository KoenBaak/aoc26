from pathlib import Path

import numpy as np


def read_map():
    return Path("data/data4.txt").read_text().split("\n")


def read_map_arr():
    return np.array([[x == "@" for x in line] for line in read_map()]).astype(int)


def enlarge(x):
    result = np.zeros(shape=(x.shape[0] + 2, x.shape[1] + 2))
    result[1:-1, 1:-1] = x
    return result


def can_be_removed(m):
    x = np.zeros_like(m)
    for xshift in (-1, 0, 1):
        for yshift in (-1, 0, 1):
            if xshift == 0 and yshift == 0:
                continue
            n = np.roll(m, shift=yshift, axis=0)
            n = np.roll(n, shift=xshift, axis=1)
            x += n
    return m.astype(bool) & (x < 4)


def sol1():
    m = enlarge(read_map_arr())
    return np.sum(can_be_removed(m))


def sol2():
    m = enlarge(read_map_arr())
    can_removed = can_be_removed(m)
    total = np.sum(can_removed)
    while np.any(can_removed):
        m = m - can_removed.astype(int)
        can_removed = can_be_removed(m)
        total += np.sum(can_removed)
    return total
