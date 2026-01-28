import numpy as np


def parse(text: str) -> dict:
    s = text.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1].strip()

    mapping = {}
    group = 0
    i = 0
    length = len(s)

    while i < length:
        ch = s[i]
        if ch == "[":
            j = s.find("]", i)
            if j == -1:
                raise ValueError("Нет закрывающей скобки ']'")
            inner = s[i + 1:j]
            tokens = [t.strip() for t in inner.split(",") if t.strip()]
            for tok in tokens:
                mapping[tok] = group
            group += 1
            i = j + 1
        elif ch == "," or ch.isspace():
            i += 1
        else:
            start = i
            while i < length and s[i] not in ",[":
                i += 1
            tok = s[start:i].strip()
            if tok:
                mapping[tok] = group
                group += 1

    return mapping


def matrix(idx_map: dict, items: list[str]) -> np.ndarray:
    n = len(items)
    mat = np.zeros((n, n), bool)

    for i in range(n):
        gi = idx_map[items[i]]
        for j in range(n):
            gj = idx_map[items[j]]
            if gi <= gj:
                mat[i, j] = True

    return mat


def main(str1: str, str2: str):
    elems = [part.strip(",[]") for part in str1.split(",")]

    idx_A = parse(str1)
    idx_B = parse(str2)

    A = matrix(idx_A, elems)
    B = matrix(idx_B, elems)

    AT = A.T
    BT = B.T

    AB = A * B
    ABT = AT * BT
    disj = AB + ABT

    coords = list(zip(*np.where(~disj)))
    pair_indices = {tuple(sorted(p)) for p in coords}
    contradictions = [(elems[i], elems[j]) for i, j in pair_indices]

    C = AB.copy()
    for a, b in contradictions:
        i = elems.index(a)
        j = elems.index(b)
        C[i, j] = True
        C[j, i] = True

    E = C * C.T

    n = len(elems)
    E_star = E.copy()
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if not E_star[i, j]:
                    E_star[i, j] = E_star[i, k] and E_star[k, j]

    visited = [False] * n
    clusters = []
    for i in range(n):
        if not visited[i]:
            block = []
            for j in range(n):
                if E_star[i, j]:
                    block.append(elems[j])
                    visited[j] = True
            clusters.append(block)

    def cluster_less(c1, c2):
        for a in c1:
            ia = elems.index(a)
            for b in c2:
                ib = elems.index(b)
                if not C[ia, ib]:
                    return False
        return True

    changed = True
    while changed:
        changed = False
        for i in range(len(clusters) - 1):
            if cluster_less(clusters[i + 1], clusters[i]):
                clusters[i], clusters[i + 1] = clusters[i + 1], clusters[i]
                changed = True

    result = []
    for cl in clusters:
        if len(cl) == 1:
            result.append(cl[0])
        else:
            result.append(cl)

    return result


str1 = "[1,[2,3],4,[5,6,7],8,9,10]"
str2 = "[[1,2],[3,4,5],6,7,9,[8,10]]"
print(main(str1, str2))

str3 = "[x1,[x2,x3],x4,[x5,x6,x7],x8,x9,x10]"
str4 = "[x3,[x1,x4],x2,x6,[x5,x7,x8],[x9,x10]]"
# print(main(str3, str4))

str5 = "[T,[K,M],D,Z]"
str6 = "[[T,K],M,Z,D]"
# print(main(str5, str6))
