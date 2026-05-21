import sys
import heapq

INF = 10**18

def astar(names, h, W, start_name, goal_name):
    n = len(names)
    idx = {names[i]: i for i in range(n)}
    s = idx[start_name]
    t = idx[goal_name]

    # adjacency list từ ma trận (đồ thị có hướng)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            w = W[i][j]
            if w > 0:
                adj[i].append((j, w))

    # gScore và parent để truy vết đường đi
    g = [INF] * n
    parent = [-1] * n
    g[s] = 0

    # heap theo tie-breaking: (f, g, name, node)
    heap = []
    heapq.heappush(heap, (g[s] + h[s], g[s], names[s], s))

    best_goal = INF  # để an toàn nếu heuristic không nhất quán

    while heap:
        f_u, g_u, name_u, u = heapq.heappop(heap)

        # bỏ entry cũ
        if g_u != g[u]:
            continue

        # nếu đã có nghiệm goal tốt hơn và f hiện tại >= best_goal thì dừng
        if best_goal != INF and f_u >= best_goal:
            break

        if u == t:
            best_goal = g_u
            # không return ngay để chắc chắn tối ưu (trường hợp heuristic không consistent)

        # Relax các cạnh
        for v, w in adj[u]:
            ng = g_u + w
            if ng < g[v]:
                g[v] = ng
                parent[v] = u
                heapq.heappush(heap, (ng + h[v], ng, names[v], v))
            # nếu ng == g[v] thì đề không yêu cầu tie-break chọn parent, nên giữ như cũ

    if g[t] == INF:
        return None

    # truy vết path
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