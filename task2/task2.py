from math import e, log2
import numpy as np
from collections import defaultdict

def dfs(graph, edge, seen=None, path=None):
    if seen is None: seen = []
    if path is None: path = [edge]
    
    seen.append(edge)
    
    paths = []
    for e in graph[edge]:
        if e not in seen:
            t_path = path + [e]
            paths.append(tuple(t_path))
            paths.extend(dfs(graph, e, seen[:], t_path))
    
    return paths

def task1(s: str) -> tuple[list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]]]:
    pairs = [item.split(',') for item in s.split('\n')]
    
    # матрица смежности
    graph_dict = defaultdict(list)
    for (f, s) in pairs:
        graph_dict[f].append(s)
        
    vertexes = []     
    for item in pairs:
        if item[0] not in vertexes:
            vertexes.append(item[0])
        if item[1] not in vertexes:
            vertexes.append(item[1])
            
    index = {v: i for i, v in enumerate(vertexes)}
    
    n = len(vertexes)
    
    # матрица r1 - непосредственное управление
    r1 = np.zeros((n,n),bool) 
    
    for key in graph_dict:
        f_idx = index[key]
        for item in graph_dict[key]:
            r1[f_idx][index[item]] = 1
    
    # матрица r2 - непосредственное подчинение
    r2 = r1.T

    # матрица r3 - опосредованное управление
    r3 = np.zeros((n,n),bool)
    A = np.dot(r1,r1)
    
    max_path_len = max(len(p) for p in dfs(graph_dict, pairs[0][0]))

    for i in range(max_path_len - 2):
        r3[np.logical_or(r3,A)] = 1
        A = np.dot(A,r1)
    
    # матрица r4 - опосредованное подчинение
    r4 = r3.T

    # матрица r5 - соподчинение на одном уровне
    r5 = np.zeros((n,n),bool)
    
    for edge in graph_dict:
        edges = graph_dict[edge] 
        len_edges = len(edges)
        if len_edges > 1:
            for i in range(len_edges):
                f_idx = index[edges[i]]
                for s_edge in edges[i+1:]:
                    s_idx = index[s_edge]
                    r5[f_idx][s_idx] = 1           
        
    r5[np.logical_or(r5,r5.T)] = 1 
    ans = (r1.tolist(), r2.tolist(), r3.tolist(), r4.tolist(), r5.tolist())

    return ans

def entropy(num: float) -> float:
    if num != 0:
        H = -num*log2(num)
        return H
    return 0.0

def main(s: str) -> tuple[float, float]:
    v = task1(s)
    k = 5
    n = len(v[0])  
      
    ans = []
    out_connections = np.zeros((n,k), int)

    for idx, item in enumerate(v):
        for i in range(n):
            out_connections[i][idx] = sum(item[i])
        
    H_sum = sum(entropy(float(row[i]/sum(row))) for i in range(k) for row in out_connections) 
        
    C = -1/e*log2(1/e)
    H_ref = C * n * k
    
    h = H_sum / H_ref

    ans = (round(H_sum,1), round(h,1))
    print(H_ref)
    return ans
    
csv_string = "1,2\n1,3\n3,4\n3,5"
csv_string1 = "1,2\n2,3\n2,4\n4,5\n4,6"
print(main(csv_string1))
