import numpy as np
from collections import defaultdict

def dfs(graph, start, visited=None, trace=None):
    if visited is None:
        visited = []
    if trace is None:
        trace = [start]

    visited.append(start)
    out = []

    for nxt in graph[start]:
        if nxt not in visited:
            new_trace = trace + [nxt]
            out.append(tuple(new_trace))
            out.extend(dfs(graph, nxt, visited[:], new_trace))

    return out


def main(text: str) -> tuple[list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]]]:
    edges = [row.split(",") for row in text.split("\n")]

    g = defaultdict(list)
    for a, b in edges:
        g[a].append(b)

    verts = []
    for a, b in edges:
        if a not in verts:
            verts.append(a)
        if b not in verts:
            verts.append(b)

    idx = {v: i for i, v in enumerate(verts)}
    n = len(verts)

    r1 = np.zeros((n, n), bool)
    for a in g:
        ia = idx[a]
        for b in g[a]:
            r1[ia][idx[b]] = True

    r2 = r1.T.copy()

    r3 = np.zeros((n, n), bool)
    step = np.dot(r1, r1)

    longest = max(len(p) for p in dfs(g, edges[0][0]))
    for _ in range(longest - 2):
        r3[np.logical_or(r3, step)] = True
        step = np.dot(step, r1)

    r4 = r3.T.copy()

    r5 = np.zeros((n, n), bool)
    for a in g:
        arr = g[a]
        if len(arr) > 1:
            for i in range(len(arr)):
                ia = idx[arr[i]]
                for b in arr[i+1:]:
                    ib = idx[b]
                    r5[ia][ib] = True

    r5[np.logical_or(r5, r5.T)] = True

    return (
        r1.tolist(),
        r2.tolist(),
        r3.tolist(),
        r4.tolist(),
        r5.tolist()
    )


csv_string = "1,2\n1,3\n3,4\n3,5"
csv_string1 = "1,2\n1,3\n3,4\n3,5\n5,6\n6,7"
csv_string2 = "2,3\n2,1\n1,8\n1,5"
csv_string3 = "0,1\n0,2\n0,3\n0,4\n1,5\n1,6"

print(main(csv_string))
