from pathlib import Path

import numpy as np


def read():
    return np.array(
        [line.split(",") for line in Path("data/data9.txt").read_text().split("\n")]
    ).astype(int)


def sol1():
    x = read()
    sizes = np.prod(np.abs(x[None, :, :] - x[:, None, :]) + 1, axis=2)
    return sizes.max()


def compress(data, coord):
    i = 0
    data = data.copy()
    while i < data[:, coord].max():
        if not len(data[data[:, coord] == i]):
            data[data[:, coord] > i, coord] -= 1
        else:
            i += 1
    return data


def edge(a, b):
    xmin = min(a[0], b[0])
    xmax = max(a[0], b[0])
    ymin = min(a[1], b[1])
    ymax = min(a[1], b[1])
    return [[x, y] for x in range(xmin, xmax + 1) for y in range(ymin, ymax + 1)]


def sol2():
    data = read()
    sizes = np.prod(np.abs(data[None, :, :] - data[:, None, :]) + 1, axis=2)
    sorted_idx = np.argsort(sizes, axis=None)[::-1]
    sorted_idx = np.array(
        np.unravel_index(sorted_idx, shape=(len(data), len(data)))
    ).transpose()

    compressed = compress(compress(data, 0), 1)
    # compressed = data
    edges = np.concat([compressed, np.roll(compressed, shift=1, axis=0)], axis=1)
    vertical_edges = edges[edges[:, 0] == edges[:, 2]]
    vertical_edges_b = np.min(vertical_edges[:, [1, 3]], axis=1)
    vertical_edges_t = np.max(vertical_edges[:, [1, 3]], axis=1)
    horizontal_edges = edges[edges[:, 1] == edges[:, 3]]
    horizontal_edges_l = np.min(horizontal_edges[:, [0, 2]], axis=1)
    horizontal_edges_r = np.max(horizontal_edges[:, [0, 2]], axis=1)

    def is_inside(x, y):
        edges_to_right = vertical_edges[
            (vertical_edges[:, 0] >= x)
            & (vertical_edges_b <= y)
            & (vertical_edges_t > y)
        ]
        edges_to_left = vertical_edges[
            (vertical_edges[:, 0] <= x)
            & (vertical_edges_b <= y)
            & (vertical_edges_t > y)
        ]
        edges_below = horizontal_edges[
            (horizontal_edges[:, 1] >= y)
            & (horizontal_edges_l <= x)
            & (horizontal_edges_r > x)
        ]
        edges_above = horizontal_edges[
            (horizontal_edges[:, 1] <= y)
            & (horizontal_edges_l <= x)
            & (horizontal_edges_r > x)
        ]
        if (edges_to_right[:, 0] == x).any():
            return True
        if (edges_to_left[:, 0] == x).any():
            return True
        if (edges_below[:, 1] == y).any():
            return True
        if (edges_above[:, 1] == y).any():
            return True
        if len(edges_to_right) % 2 == 0:
            # print("edges_to_right", x, y)
            return False

        if len(edges_to_left) % 2 == 0:
            # print("edges_to_left")
            return False

        if len(edges_below) % 2 == 0:
            # print("edges_below")
            return False

        if len(edges_above) % 2 == 0:
            # print("edges_above")
            return False
        return True

    def rect_inside(p, q):
        left = min(p[0], q[0])
        right = max(p[0], q[0])
        bottom = max(p[1], q[1])
        top = min(p[1], q[1])
        for x in range(left, right + 1):
            for y in range(top, bottom + 1):
                if not is_inside(x, y):
                    return False
        return True

    for i, j in sorted_idx:
        if j <= i:
            continue
        print("check", data[i], data[j], sizes[i, j])
        if rect_inside(compressed[i], compressed[j]):
            break

    return sizes[i, j]
