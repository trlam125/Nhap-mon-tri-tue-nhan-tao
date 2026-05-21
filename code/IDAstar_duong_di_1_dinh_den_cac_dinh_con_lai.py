from collections import deque
import sys

BETA = 2

def ida(name, h, W, str_name, goal_name):
    n = len(name)
    idx = {name[i]: i for i in range(n)}
    s = idx[str_name]
    t = idx[goal_name]
    
    a = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            w = W[i][j]
            if w > 0: a[i].append((j, w))
    def ord(u, g_u):
        cand = []
        for v, w in a[u]:
            gv = g_u + w
            fv = gv + h[v]
            cand.append((fv, gv, name[v], v, w))
        cand.sort(key = lambda x : (x[0], x[1], x[2]))
        return cand
    threshold = h[s]
    best_path = None
    best_cost = None
    while True:
        in_path = set([s])
        path = [s]
        found_cost = float("inf")
        found_path = None
        had_cutoff = False
        
        def dfs(u, g_u):
            nonlocal found_cost, found_path, had_cutoff
            f_u = g_u + h[u]
            if f_u > threshold:
                had_cutoff = True
                return
            if g_u >= found_cost: return
            if u == t:
                if g_u < found_cost:
                    found_cost = g_u
                    found_path = path[:]
                return
            for fv, gv, vname, v, w in ord(u, g_u):
                if v in in_path: continue
                if gv >= found_cost: continue
                if fv > threshold:
                    had_cutoff = True
                    continue
                in_path.add(v)
                path.append(v)
                dfs(v, gv)
                path.pop()
                in_path.remove(v)
        dfs(s, 0)
        if found_path is not None:
            best_path = found_path
            best_cost = found_cost
            break
        if not had_cutoff: return None
        threshold += BETA
    return best_path, best_cost, name
    
def main():
    data = sys.stdin.read().strip().split()
    if not data: return
    it = iter(data)
    n = int(next(it))
    name = [next(it) for _ in range(n)]
    h = [int(next(it)) for _ in range(n)]
    w = []
    for _ in range(n):
        row = [int(next(it)) for _ in range(n)]
        w.append(row)
    str_name = next(it)
    goal_name = next(it)
    print("ASTAR")
    res = ida(name, h, w, str_name, goal_name)
    if res is None: print("NO PATH")
    else:
        path_idx, cost, name = res
        path_name = [name[i] for i in path_idx]
        print("->".join(path_name), f"| cost={cost}")
        
main()


'''
8
S A B C D E F G
6 4 4 3 4 1 1 0
0 2 3 0 0 0 0 0
0 0 0 0 3 0 0 0
0 0 0 3 1 0 0 0
0 0 0 0 0 2 0 0
0 0 0 1 0 0 3 0
0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0
S A

ASTAR
S->A | cost=2
'''