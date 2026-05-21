import sys
import heapq

INF = 10**18

def reconstruct(parent, s, t):
    if s == t:
        return [s]
    if t not in parent:
        return None
    path = []
    cur = t
    while True:
        path.append(cur)
        if cur == s:
            break
        cur = parent.get(cur)
        if cur is None:
            return None
    path.reverse()
    return path

def greedy_best_first(names, h, W, s_name, t_name):
    n = len(names)
    idx = {names[i]: i for i in range(n)}
    s, t = idx[s_name], idx[t_name]

    # Priority: (h, g, name) as required
    pq = []
    heapq.heappush(pq, (h[s], 0, names[s], s))

    best_g = {s: 0}
    parent = {}          # parent[name_child] = name_parent
    expanded = set()     # nodes already expanded

    while pq:
        hu, gu, nu, u = heapq.heappop(pq)
        if u in expanded:
            continue
        # The (h,g,name) popped is the chosen node to expand
        expanded.add(u)

        if u == t:
            path = reconstruct(parent, s_name, t_name)
            return path, gu

        # expand neighbors (undirected graph via matrix)
        for v in range(n):
            w = W[u][v]
            if w <= 0:
                continue
            if v in expanded:
                continue
            ng = gu + w
            # keep the best known g for tie-breaking stability
            if (v not in best_g) or (ng < best_g[v]):
                best_g[v] = ng
                parent[names[v]] = names[u]
                heapq.heappush(pq, (h[v], ng, names[v], v))
            elif ng == best_g[v]:
                # If same g, prefer lexicographically smaller parent path implicitly by (h,g,name) PQ;
                # but we can also update parent if it improves deterministic behavior:
                # choose parent with smaller name to be consistent
                if parent.get(names[v]) is None or names[u] < parent[names[v]]:
                    parent[names[v]] = names[u]
                    heapq.heappush(pq, (h[v], ng, names[v], v))

    return None, None

def ucs(names, W, s_name, t_name):
    n = len(names)
    idx = {names[i]: i for i in range(n)}
    s, t = idx[s_name], idx[t_name]

    dist = [INF] * n
    dist[s] = 0
    parent = {}  # parent[name_child] = name_parent

    # Priority: (g, name) as required
    pq = []
    heapq.heappush(pq, (0, names[s], s))

    while pq:
        gu, nu, u = heapq.heappop(pq)
        if gu != dist[u]:
            continue
        if u == t:
            path = reconstruct(parent, s_name, t_name)
            return path, gu

        for v in range(n):
            w = W[u][v]
            if w <= 0:
                continue
            ng = gu + w
            if ng < dist[v]:
                dist[v] = ng
                parent[names[v]] = names[u]
                heapq.heappush(pq, (ng, names[v], v))
            elif ng == dist[v]:
                # tie: (g, name) => if same g, smaller name should be popped first;
                # update parent for deterministic path if parent name is larger
                if parent.get(names[v]) is None or names[u] < parent[names[v]]:
                    parent[names[v]] = names[u]
                    heapq.heappush(pq, (ng, names[v], v))

    return None, None

def main():
    data = sys.stdin.read().strip().splitlines()
    if not data:
        return
    it = iter(data)

    N = int(next(it).strip())
    names = next(it).strip().split()
    h_vals = list(map(int, next(it).strip().split()))
    if len(names) != N or len(h_vals) != N:
        raise ValueError("Input N không khớp số tên đỉnh hoặc số heuristic.")

    W = []
    for _ in range(N):
        row = list(map(int, next(it).strip().split()))
        if len(row) != N:
            raise ValueError("Ma trận W không đúng kích thước N x N.")
        W.append(row)

    s_name, t_name = next(it).strip().split()

    # GREEDY
    path_g, cost_g = greedy_best_first(names, h_vals, W, s_name, t_name)
    print("GREEDY")
    if path_g is None:
        print("NO PATH")
    else:
        print(f"{' '.join(path_g)} | cost={cost_g}")

    # UCS
    path_u, cost_u = ucs(names, W, s_name, t_name)
    print("UCS")
    if path_u is None:
        print("NO PATH")
    else:
        print(f"{' '.join(path_u)} | cost={cost_u}")

if __name__ == "__main__":
    main()

'''
11
S A B C D E F G H I K
125 123 82 118 115 72 40 0 70 40 30
0 55 42 48 0 72 0 0 0 0 0
55 0 0 0 45 0 0 0 0 0 0
42 0 0 40 0 0 40 0 0 0 0
48 0 40 0 0 0 68 0 0 0 0
0 45 0 0 0 45 0 0 0 0 0
72 0 0 0 45 0 0 82 0 0 0
0 0 40 68 0 0 0 55 0 0 0
0 0 0 0 0 82 55 0 0 47 38
0 0 0 0 0 0 0 0 0 50 0
0 0 0 0 0 0 0 47 50 0 0
0 0 0 0 0 0 0 38 0 0 0
S A

S->A | cost=55
UCS
S->A | cost=55
'''