import itertools
from collections import defaultdict
from pathlib import Path

import numpy as np


def read():
    lines = Path("data/data7.txt").read_text().split("\n")
    return np.array(list(map(list, lines)))


def sol1():
    m = read()
    beam = m[0] == "S"
    n_splits = 0
    for i in range(1, m.shape[0]):
        row = m[i]
        continued_beam = (row != "^") & beam
        split_beam = (row == "^") & beam
        n_splits += np.sum(split_beam)
        right_split = np.roll(split_beam, shift=1)
        right_split[0] = "."
        left_split = np.roll(split_beam, shift=-1)
        right_split[-1] = "."
        beam = continued_beam | left_split | right_split
    return n_splits


def sol2():
    m = read()
    old_positions = {np.argmax(m[0] == "S").item(): 1}
    new_positions = defaultdict(int)
    n_timelines = 1
    for row in m[1:]:
        for idx, count in old_positions.items():
            if row[idx] != "^":
                new_positions[idx] += count
            else:
                n_timelines += count
                new_positions[idx - 1] += count
                new_positions[idx + 1] += count
        old_positions = new_positions
        new_positions = defaultdict(int)

    return n_timelines
