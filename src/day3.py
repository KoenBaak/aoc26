from pathlib import Path

import numpy as np


def read_banks():
    return Path("data/data3.txt").read_text().split("\n")


def sol1():
    banks = np.array([list(line) for line in read_banks()]).astype(int)
    first = np.max(banks[:, :-1], axis=1)
    first_idx = np.argmax(banks[:, :-1], axis=1)
    second = np.max(
        banks
        * (
            np.tile(np.arange(banks.shape[1]), reps=(banks.shape[0], 1))
            > first_idx.reshape(-1, 1)
        ),
        axis=1,
    )
    return np.sum(first * 10 + second)


def find_next_digit(banks, remaining):
    stop = -remaining if remaining > 0 else None
    next_digit = np.max(banks[:, :stop], axis=1)
    idx = np.argmax(banks[:, :stop], axis=1)
    bank_remainder = banks * (
        np.tile(np.arange(banks.shape[1]), reps=(banks.shape[0], 1))
        > idx.reshape(-1, 1)
    )
    return next_digit, bank_remainder


def sol2():
    banks = np.array([list(line) for line in read_banks()]).astype(int)
    found = []
    for x in range(11, -1, -1):
        digit, banks = find_next_digit(banks, x)
        found.append(digit * 10**x)
    return np.sum(np.array(found))
