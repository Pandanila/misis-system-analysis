import numpy as np
from math import e, log2
from collections import defaultdict


def dfs(graph, start, seen=None, path=None):
    if seen is None:
        seen = []
    if path is None:
        path = [start]

    seen.append(start)
    all_paths = []

    for nxt in graph[start]:
        if nxt not in seen:
            new_path = path + [nxt]
            all_paths.append(tuple(new_path))
            all_paths.extend(dfs(graph, nxt, seen[:], new_path))

    return all_paths


def task1(text: str) -> tuple[list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]]]:
    pairs = [chunk.split(",") for chunk in text.split("\n")]

    graph = defaultdict(list)
    for a, b in pairs:
        graph[a].append(b)

    vertices = []
    for a, b in pairs:
        if a not in vertices:
            vertices.append(a)
        if b not in vertices:
            vertices.append(b)

    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)

    r1 = np.zeros((n, n), bool)
    for parent in graph:
        p_index = idx[parent]
        for child in graph[parent]:
            r1[p_index][idx[child]] = True

    r2 = r1.T

    r3 = np.zeros((n, n), bool)
    A = np.dot(r1, r1)

    max_path_len = max(len(p) for p in dfs(graph, pairs[0][0]))

    for _ in range(max_path_len - 2):
        r3[np.logical_or(r3, A)] = True
        A = np.dot(A, r1)

    r4 = r3.T

    r5 = np.zeros((n, n), bool)
    for boss in graph:
        subs = graph[boss]
        m = len(subs)
        if m > 1:
            for i in range(m):
                a_idx = idx[subs[i]]
                for sub2 in subs[i + 1 :]:
                    b_idx = idx[sub2]
                    r5[a_idx][b_idx] = True

    r5[np.logical_or(r5, r5.T)] = True

    return (
        r1.tolist(),
        r2.tolist(),
        r3.tolist(),
        r4.tolist(),
        r5.tolist(),
    )


def entropy(x: float) -> float:
    if x != 0:
        return -x * log2(x)
    return 0.0


def main(text: str) -> tuple[float, float]:
    rels = task1(text)
    k = 5
    n = len(rels[0])

    out_connections = np.zeros((n, k), int)
    for rel_idx, rel_matrix in enumerate(rels):
        for i in range(n):
            out_connections[i][rel_idx] = sum(rel_matrix[i])

    H_sum = 0.0
    for row in out_connections:
        row_sum = sum(row)
        for j in range(k):
            H_sum += entropy(float(row[j] / row_sum))

    C = -(1 / e) * log2(1 / e)
    H_ref = C * n * k

    h = H_sum / H_ref
    result = (round(H_sum, 1), round(h, 1))
    print(H_ref)
    return result


csv_string = "1,2\n1,3\n3,4\n3,5"
csv_string1 = "1,2\n2,3\n2,4\n4,5\n4,6"

print(main(csv_string1))
