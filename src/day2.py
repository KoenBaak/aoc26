from pathlib import Path
import typing as t


def read_ranges() -> t.Generator[list[str], None, None]:
    return (
        r.split("-")
        for line in Path("data/data2.txt").read_text().split("\n")
        for r in line.split(",")
    )


def all_numbers(ranges):
    for l, r in ranges:
        for x in range(int(l), int(r) + 1):
            yield x


def is_invalid(x: int):
    x = str(x)
    return x[: len(x) // 2] == x[len(x) // 2 :]


def divisors(x: int):
    for d in range(1, x):
        if x % d == 0:
            yield d


def is_invalid_v2(x: int):
    x = str(x)
    for d in divisors(len(x)):
        parts = set(x[d * i : d * (i + 1)] for i in range(len(x) // d))
        if len(parts) == 1:
            return True
    return False


def sol1():
    return sum(filter(lambda x: is_invalid(x), all_numbers(read_ranges())))


def sol2():
    return sum(filter(lambda x: is_invalid_v2(x), all_numbers(read_ranges())))
