import sys
from collections import deque

def build_path(parent, s, t):
    # Truy vết từ t về s bằng parent (lưu chỉ số)
    path = []
    cur = t
    while cur != -1:
        path.append(cur)
        if cur == s:
            break
        cur = parent[cur]
    if path[-1] != s:
        return None
    path.reverse()
    return path

def main():
    data = sys.stdin.read().strip().splitlines()
    if not data:
        return

    it = iter(data)
    n = int(next(it).strip())
    labels = next(it).strip().split()
    idx = {labels[i]: i for i in range(n)}

    a = []
    for _ in range(n):
        row = list(map(int, next(it).strip().split()))
        a.append(row)

    s_label, t_label = next(it).strip().split()
    s = idx[s_label]
    t = idx[t_label]

    # BFS
    dist = [-1] * n
    parent = [-1] * n
    q = deque()

    dist[s] = 0
    q.append(s)

    while q:
        u = q.popleft()
        if u == t:
            break
        for v in range(n):
            if a[u][v] == 1 and dist[v] == -1:
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)

    if dist[t] == -1:
        print("UNREACHABLE")
        return

    path_idx = build_path(parent, s, t)
    path_labels = [labels[i] for i in path_idx]

    print(dist[t])
    print(" ".join(path_labels))

if __name__ == "__main__":
    main()


'''
9
S A B C D E F H G
0 1 1 1 0 1 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 1 0 0
0 0 1 0 0 0 1 1 0
0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0
S D

2
S A D
'''