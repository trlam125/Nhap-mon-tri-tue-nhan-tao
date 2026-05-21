import sys
import heapq

INF = 10**18

def astar(names, h, W, start_name, goal_name):
    n = len(names)
    idx = {names[i]: i for i in range(n)}
    s = idx[start_name]
    t = idx[goal_name]

    # Build adjacency list (vô hướng => ma trận đối xứng, cứ đọc W[i][j] > 0)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            w = W[i][j]
            if w > 0:
                adj[i].append((j, w))

    g = [INF] * n
    parent = [-1] * n
    g[s] = 0

    # tie-breaking trong OPEN: (f, g, name, node)
    heap = []
    heapq.heappush(heap, (h[s], 0, names[s], s))

    best_goal = INF  # để an toàn nếu heuristic không consistent

    while heap:
        f_u, g_u, name_u, u = heapq.heappop(heap)

        # bỏ bản ghi cũ
        if g_u != g[u]:
            continue

        # nếu đã có nghiệm goal tốt hơn và f hiện tại >= best_goal => dừng
        if best_goal != INF and f_u >= best_goal:
            break

        if u == t:
            best_goal = g_u
            # không return ngay để an toàn (trường hợp h không consistent)

        for v, w in adj[u]:
            ng = g_u + w
            if ng < g[v]:
                g[v] = ng
                parent[v] = u
                heapq.heappush(heap, (ng + h[v], ng, names[v], v))

    if g[t] == INF:
        return None

    # Reconstruct path
    path = []
    cur = t
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path, g[t]

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)

    N = int(next(it))
    names = [next(it) for _ in range(N)]
    h = [int(next(it)) for _ in range(N)]

    W = []
    for _ in range(N):
        row = [int(next(it)) for _ in range(N)]
        W.append(row)

    start_name = next(it)
    goal_name = next(it)

    print("ASTAR")
    res = astar(names, h, W, start_name, goal_name)
    if res is None:
        print("NO PATH")
    else:
        path_idx, cost = res
        path_names = [names[i] for i in path_idx]
        print("->".join(path_names), f"| cost={cost}")

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

ASTAR
S->A | cost=55
'''