from pathlib import Path


def read():
    lines = Path("data/data11.txt").read_text().split("\n")
    lines = [line.split() for line in lines]
    return {line[0].removesuffix(":"): line[1:] for line in lines}


def sol1():
    graph = read()
    paths = [("you",)]
    completed = []
    while paths:
        continued_paths = []
        for path in paths:
            tail = path[-1]
            for v in graph[tail]:
                continued = path + (v,)
                if v == "out":
                    completed.append(continued)
                else:
                    continued_paths.append(continued)
        paths = continued_paths
    return len(completed)


def sol2():
    graph = read()

    reach_memo = {}
    paths_memo = {}

    def reach(v):
        if v in reach_memo:
            return reach_memo[v]
        if v not in graph:
            return set()
        result = set(graph[v])
        for n in result:
            result = result | reach(n)
        reach_memo[v] = result
        return result

    def get_paths(s, e):
        if (s, e) in paths_memo:
            return paths_memo[(s, e)]

        if e not in reach(s):
            return []

        if e in graph[s]:
            return [(s, e)]

        result = []
        for v in graph[s]:
            paths = [(s,) + path for path in get_paths(v, e)]
            result.extend(paths)

        paths_memo[(s, e)] = result
        return result


    # svr_to_dac = len(get_paths("svr", "dac"))
    svr_to_fft = len(get_paths("svr", "fft"))
    # dac_to_fft = len(get_paths("dac", "fft"))
    fft_to_dac = len(get_paths("fft", "dac"))
    # fft_to_out = len(get_paths("fft", "out"))
    dac_to_out = len(get_paths("dac", "out"))

    # no paths from dac to fft so should be this
    return svr_to_fft * fft_to_dac * dac_to_out
