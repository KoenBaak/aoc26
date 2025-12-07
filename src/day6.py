from pathlib import Path

import numpy as np


def read():
    return Path("data/data6.txt").read_text().split("\n")


def read_problems():
    lines = read()
    nrs = np.array([[int(x) for x in line.split() if x] for line in lines[:-1]])
    ops = [x for x in lines[-1].split() if x]
    return nrs, ops


def read_problems_v2():
    lines = read()
    line_length = max(len(l) for l in lines)
    lines = [line.ljust(line_length) for line in lines]
    x = np.char.array([list(x) for x in lines]).transpose()
    ops = [o for o in x[:, -1] if o]
    nrs = np.array(x[:, :-1].replace(" ", "")).astype(object).sum(axis=1)
    nrs = np.concat([nrs, np.array([""])])
    return nrs, ops


def sol1():
    nrs, ops = read_problems()
    result = 0
    for i, x in enumerate(ops):
        op = np.sum if x == "+" else np.prod
        result += op(nrs[:, i])
    return result


def sol2():
    nrs, ops = read_problems_v2()
    result = 0
    for i, x in enumerate(ops):
        op = np.sum if x == "+" else np.prod
        problem_size = np.argmax(nrs == "")
        result += op(nrs[:problem_size].astype(int))
        nrs = nrs[problem_size + 1 :]
    return result
