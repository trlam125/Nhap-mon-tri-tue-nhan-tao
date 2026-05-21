import sys
from collections import deque

def bfs_path(pages, edges, start, goal):
    # Build adjacency list, giữ thứ tự xuất hiện input
    adj = {p: [] for p in pages}
    for u, v in edges:
        if u in adj:   # theo đề thì u,v đều hợp lệ
            adj[u].append(v)

    if start == goal:
        return [start]

    q = deque([start])
    parent = {start: None}  # để truy vết đường đi

    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if v not in parent:
                parent[v] = u
                if v == goal:
                    # reconstruct
                    path = []
                    cur = goal
                    while cur is not None:
                        path.append(cur)
                        cur = parent[cur]
                    path.reverse()
                    return path
                q.append(v)

    return None

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)

    N = int(next(it))
    M = int(next(it))

    pages = [next(it) for _ in range(N)]

    edges = []
    for _ in range(M):
        u = next(it); v = next(it)
        edges.append((u, v))

    start = next(it)
    goal = next(it)

    path = bfs_path(pages, edges, start, goal)
    if path is None:
        print("NO PATH")
    else:
        k = len(path) - 1
        print(k)
        for p in path:
            print(p)

if __name__ == "__main__":
    main()
