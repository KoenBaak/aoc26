from pathlib import Path

import numpy as np


def read():
    lines = Path("data/data12.txt").read_text().split("\n")
    blocks = []
    current = []
    for line in lines:
        if not line:
            blocks.append(current)
            current = []
        else:
            current.append(line)

    target = current
    shapes = {}
    for shape_block in blocks:
        shapes[int(shape_block[0].removesuffix(":"))] = np.array(
            (
                np.char.array(list(map(list, shape_block[1:])))
                .replace(".", "0")
                .replace("#", "1")
            )
        ).astype(int)

    return shapes, target

def shape_as_str(shape):
    return "\n".join("".join(str(x) for x in row) for row in shape)

def unique_variants(shape):
    seen = set()
    result = []
    for k in range(4):
        for flip0 in (True, False):
            for flip1 in (True, False):
                s = np.rot90(shape, k=k)
                if flip0:
                    s = np.flip(s,axis=0)
                if flip1:
                    s = np.flip(s, axis=1)
                s_str = shape_as_str(s)
                if s_str not in seen:
                    result.append(s)
                    seen.add(s_str)
    return result



def sol1():
    shapes, targets = read()
    surely_impossible = 0
    surely_possible = 0
    for line in targets:
        area_shape, rest = line.split(": ", 1)
        x, y = tuple(map(int, area_shape.split("x")))
        target = dict(enumerate(map(int, rest.split(" "))))
        if x * y >= sum(shapes[idx].size * amount for idx, amount in target.items()):
            surely_possible += 1
        if x * y < sum(shapes[idx].sum() * amount for idx, amount in target.items()):
            surely_impossible += 1
    # hehe yeah this is funny
    return surely_possible, surely_impossible, len(targets)