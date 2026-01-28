def main(data: str):
    edges = [line.split(",") for line in data.split("\n")]

    verts = set()
    for a, b in edges:
        verts.add(a)
        verts.add(b)

    verts = sorted(verts)
    size = len(verts)

    adj = [[0 for _ in range(size)] for _ in range(size)]

    pos = {v: i for i, v in enumerate(verts)}
    for a, b in edges:
        adj[pos[a]][pos[b]] = 1

    return adj


print(main("1,2\n1,3\n3,4\n3,5"))
