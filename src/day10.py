import functools
import operator
from pathlib import Path

import numpy as np
from scipy.optimize import milp
from scipy.optimize import LinearConstraint


def read():
    lines = Path("data/data10.txt").read_text().split("\n")
    lines = [line.split() for line in lines]
    targets = [line[0] for line in lines]
    joltages = [line[-1] for line in lines]
    buttons = [
        [
            list(map(int, word.removeprefix("(").removesuffix(")").split(",")))
            for word in line
            if word.startswith("(")
        ]
        for line in lines
    ]
    return targets, joltages, buttons


def button_to_int(button: list[int]):
    return sum(2**i for i in button)


def state(x: str):
    x = x.removeprefix("[").removesuffix("]")
    return sum([(c == "#") * 2**i for i, c in enumerate(x)])


def press_output(press, buttons):
    return functools.reduce(
        operator.xor, [((press >> i) & 1) * btn for i, btn in enumerate(buttons)]
    )


def sol1():
    all_targets, all_joltages, all_buttons = read()
    result = []
    for target, _, buttons in zip(all_targets, all_joltages, all_buttons):
        target = state(target)
        bs = [button_to_int(b) for b in buttons]
        for potential_solution in sorted(
            range(2 ** len(buttons)), key=lambda x: x.bit_count()
        ):
            out = press_output(potential_solution, bs)
            if out == target:
                result.append(potential_solution.bit_count())
                break
    return sum(result)


def buttons_to_matrix(n, buttons):
    result = np.zeros(shape=(len(buttons), n), dtype=int)
    for row, btn in enumerate(buttons):
        result[row, btn] = 1
    return result.T


def sol2():
    all_targets, all_joltages, all_buttons = read()
    result = []
    for _, target, buttons in zip(all_targets, all_joltages, all_buttons):
        target = np.array(target.removeprefix("{").removesuffix("}").split(",")).astype(
            int
        )
        A = buttons_to_matrix(len(target), buttons)
        result.append(
            milp(
                c=np.ones(len(buttons), dtype=int),
                integrality=1,
                constraints=[LinearConstraint(A=A, lb=target, ub=target)],
            ).x.sum()
        )
    return sum(result)