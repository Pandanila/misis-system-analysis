import numpy as np


def parse(text: str) -> dict:
    mapping = {}
    group_id = 0
    i = 0
    length = len(text)

    while i < length:
        ch = text[i]
        if ch == "[":
            j = text.find("]", i)
            if j == -1:
                raise ValueError("Нет закрывающей скобки ']'")
            inner = text[i + 1:j]
            tokens = [t.strip() for t in inner.split(",") if t.strip()]
            for t in tokens:
                mapping[t] = group_id
            group_id += 1
            i = j + 1
        elif ch == "," or ch.isspace():
            i += 1
        else:
            start = i
            while i < length and text[i] not in ",[":
                i += 1
            token = text[start:i].strip()
            if token:
                mapping[token] = group_id
                group_id += 1

    return mapping


def build_matrix(idx_map: dict, elems: list[str]) -> np.ndarray:
    n = len(elems)
    mat = np.zeros((n, n), bool)

    for i in range(n):
        gi = idx_map[elems[i]]
        for j in range(n):
            gj = idx_map[elems[j]]
            if gi <= gj:
                mat[i, j] = True

    return mat


def main(s1: str, s2: str) -> str:
    elems = [item.strip(",[]") for item in s1.split(",")]

    idx_A = parse(s1)
    idx_B = parse(s2)

    A = build_matrix(idx_A, elems)
    B = build_matrix(idx_B, elems)

    AT = A.T
    BT = B.T

    AB = A * B
    ABT = AT * BT

    combined = AB + ABT

    zeros = list(zip(*np.where(~combined)))
    unique_pairs = {tuple(sorted(p)) for p in zeros}
    result = [(elems[i], elems[j]) for i, j in unique_pairs]

    return result


str1 = "1,[2,3],4,[5,6,7],8,9,10"
str2 = "[1,2],[3,4,5],6,7,9,[8,10]"
str3 = "x1,[x2,x3],x4,[x5,x6,x7],x8,x9,x10"
str4 = "x3,[x1,x4],x2,x6,[x5,x7,x8],[x9,x10]"

print(main(str1, str2))
