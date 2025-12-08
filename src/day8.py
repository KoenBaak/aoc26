import functools
import operator
from pathlib import Path
import numpy as np


def read():
    return np.array(
        [line.split(",") for line in Path("data/data8.txt").read_text().split("\n")]
    ).astype(int)


def pairwise_distances(x):
    result = np.empty(shape=(x.shape[0], x.shape[0], x.shape[1]))
    for idx, left in enumerate(x):
        for jdx, right in enumerate(x):
            result[idx, jdx] = left - right
    return np.linalg.norm(result, axis=2)


def sol1():
    coords = read()
    d = pairwise_distances(coords)
    sorted_idx = np.argsort(d, axis=None)
    idx = np.array(np.unravel_index(sorted_idx, shape=d.shape)).transpose()[
        d.shape[0] :
    ]

    membership = {i: i for i in range(d.shape[0])}
    circuits = {i: {i} for i in range(d.shape[0])}

    def manage_circuits(i, j):
        keep = min(membership[i], membership[j])
        remove = max(membership[i], membership[j])
        for k in circuits[remove]:
            membership[k] = keep
        circuits[keep] |= circuits[remove]
        circuits[remove] = set()

    for _ in range(1000):
        i, j = idx[0]
        if not membership[i] == membership[j]:
            manage_circuits(i, j)
        idx = idx[2:]

    circuits = sorted(list(circuits.values()), key=lambda c: len(c), reverse=True)
    return functools.reduce(operator.mul, [len(c) for c in circuits[:3] if len(c) > 0])

def sol2():
    coords = read()
    d = pairwise_distances(coords)
    sorted_idx = np.argsort(d, axis=None)
    idx = np.array(np.unravel_index(sorted_idx, shape=d.shape)).transpose()[
        d.shape[0] :
    ]

    membership = {i: i for i in range(d.shape[0])}
    circuits = {i: {i} for i in range(d.shape[0])}

    def manage_circuits(i, j):
        keep = min(membership[i], membership[j])
        remove = max(membership[i], membership[j])
        for k in circuits[remove]:
            membership[k] = keep
        circuits[keep] |= circuits[remove]
        circuits.pop(remove)

    while len(circuits) > 1:
        i, j = idx[0]
        if not membership[i] == membership[j]:
            manage_circuits(i, j)
        idx = idx[2:]

    return coords[i, 0] * coords[j, 0]
