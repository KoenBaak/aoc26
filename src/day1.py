from pathlib import Path
import numpy as np


def read_rotations() -> np.ndarray:
    lines = Path("data/data1.txt").read_text().split("\n")
    x = np.char.array(lines).replace("R", "").replace("L", "-")
    return np.array(x).astype(np.int64)


def left_at_zero(x: np.ndarray) -> int:
    return ((50 + x.cumsum()) % 100 == 0).sum()


def intermediate_zeros(x: np.ndarray) -> int:
    pos = np.concat([[50], (50 + x.cumsum())]) % 100
    prev_pos = np.roll(pos, 1)
    pos, prev_pos = pos[1:], prev_pos[1:]
    result = np.sum(np.abs(x) // 100)
    result += np.sum((x > 0) & (pos < prev_pos) & (pos != 0) & (prev_pos != 0))
    result += np.sum((x < 0) & (pos > prev_pos) & (pos != 0) & (prev_pos != 0))
    return result


def sol1():
    return left_at_zero(read_rotations())


def sol2():
    x = read_rotations()
    return left_at_zero(x) + intermediate_zeros(x)
