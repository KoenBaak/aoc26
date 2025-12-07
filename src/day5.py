from pathlib import Path

import numpy as np


def read():
    return Path("data/data5.txt").read_text().split("\n")


def read_db():
    lines = read()
    ranges = []
    ids = []
    sep_seen = False
    for line in lines:
        if not line:
            sep_seen = True
            continue
        if not sep_seen:
            ranges.append(tuple(map(int, line.split("-"))))
        else:
            ids.append(int(line))
    return ranges, ids


def sol1():
    ranges, ids = read_db()
    ranges = np.array(ranges)
    lower = ranges[:, 0]
    upper = ranges[:, 1]
    result = 0
    for i in ids:
        if ((i >= lower) & (i <= upper)).any():
            result += 1
    return result


def disjoint_ranges(space, new_range):
    for l, u in space:
        if l <= new_range[0] <= new_range[1] <= u:
            return space
        elif l <= new_range[0] <= u:
            changed = (l, new_range[1])
            return disjoint_ranges({x for x in space if x != (l, u)}, changed)
        elif l <= new_range[1] <= u:
            changed = (new_range[0], u)
            return disjoint_ranges({x for x in space if x != (l, u)}, changed)
        elif new_range[0] <= l <= u <= new_range[1]:
            return {x for x in space if x != (l, u)} | {new_range}
    return space | {new_range}


def sol2():
    ranges, _ = read_db()
    space = set()
    for r in ranges:
        space = disjoint_ranges(space, r)
    ranges = np.array(list(space))
    lower = ranges[:, 0]
    upper = ranges[:, 1]
    return (upper - lower + 1).sum()
