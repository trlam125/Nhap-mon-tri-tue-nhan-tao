import sys
import heapq

INF = 10**18

def reconstruct_path(parent, s, t, labels):
    if s == t:
        return [labels[s]]
    if parent[t] == -1:
        return None
    path = []
    cur = t
    while cur != -1:
        path.append(labels[cur])
        if cur == s:
            break
        cur = parent[cur]
    if path[-1] != labels[s]:
        return None
    path.reverse()
    return path

def greedy_best_first(W, h, s, t, labels):
    n = len(labels)
    parent = [-1] * n
    g = [INF] * n
    visited = [False] * n
    discovered = [False] * n

    g[s] = 0
    pq = []
    heapq.heappush(pq, (h[s], s))
    discovered[s] = True

    while pq:
        _, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True

        if u == t:
            path = reconstruct_path(parent, s, t, labels)
            return g[u], path

        # Duyệt láng giềng theo thứ tự tăng dần chỉ số để ổn định
        for v in range(n):
            w = W[u][v]
            if w > 0 and not discovered[v]:
                discovered[v] = True
                parent[v] = u
                g[v] = g[u] + w
                heapq.heappush(pq, (h[v], v))

    return None, None

def ucs(W, s, t, labels):
    n = len(labels)
    parent = [-1] * n
    dist = [INF] * n
    visited = [False] * n

    dist[s] = 0
    pq = []
    heapq.heappush(pq, (0, s))

    while pq:
        g_u, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True

        if u == t:
            path = reconstruct_path(parent, s, t, labels)
            return g_u, path

        for v in range(n):
            w = W[u][v]
            if w > 0 and not visited[v]:
                ng = g_u + w
                # Relax: ưu tiên đường có g nhỏ hơn; nếu bằng nhau chọn parent nhỏ hơn để ổn định
                if ng < dist[v] or (ng == dist[v] and (parent[v] == -1 or u < parent[v])):
                    dist[v] = ng
                    parent[v] = u
                    heapq.heappush(pq, (ng, v))

    return None, None

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)

    n = int(next(it))
    labels = [next(it) for _ in range(n)]
    idx = {labels[i]: i for i in range(n)}

    W = [[int(next(it)) for _ in range(n)] for _ in range(n)]
    h = [int(next(it)) for _ in range(n)]

    S = next(it)
    T = next(it)
    s = idx[S]
    t = idx[T]

    # GREEDY
    gcost, gpath = greedy_best_first(W, h, s, t, labels)
    if gpath is None:
        print("GREEDY UNREACHABLE")
        print("-")
    else:
        print(f"GREEDY {gcost}")
        print(" ".join(gpath))

    # UCS
    ucost, upath = ucs(W, s, t, labels)
    if upath is None:
        print("UCS UNREACHABLE")
        print("-")
    else:
        print(f"UCS {ucost}")
        print(" ".join(upath))

if __name__ == "__main__":
    main()

'''
8
S A B C D E F G
0 2 3 0 0 0 0 0
0 0 0 0 3 0 0 0
0 0 0 3 1 0 0 0
0 0 0 0 0 2 0 0
0 0 0 1 0 0 3 0
0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0
6 4 4 3 4 1 1 0
S C

GREEDY 6
S B C
UCS 5
S B D C
'''