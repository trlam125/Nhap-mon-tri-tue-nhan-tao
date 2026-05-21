from collections import deque
import sys

def safe(ml, cl, M, C):
    mr = M - ml
    cr = C - cl
    left = (ml == 0) or (ml >= cl)
    right = (mr == 0) or (mr >= cr)
    return left and right

def bfs(M, C, K):
    start = (M, C, 0)
    goal = (0, 0, 1)

    # sinh hành động, tránh đè biến M,C
    act = []
    for mm in range(K + 1):
        for cc in range(K + 1):
            if 1 <= mm + cc <= K and (mm == 0 or mm >= cc):
                act.append((mm, cc))

    q = deque([start])
    parent = {start: None}

    while q:
        ml, cl, b = q.popleft()

        if (ml, cl, b) == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path

        for mm, cc in act:
            if b == 0:
                if ml < mm or cl < cc:
                    continue
                nml, ncl, nb = ml - mm, cl - cc, 1
            else:
                mr, cr = M - ml, C - cl
                if mr < mm or cr < cc:
                    continue
                nml, ncl, nb = ml + mm, cl + cc, 0

            if not (0 <= nml <= M and 0 <= ncl <= C):
                continue
            if not safe(nml, ncl, M, C):
                continue

            nxt = (nml, ncl, nb)
            if nxt not in parent:
                parent[nxt] = (ml, cl, b)
                q.append(nxt)

    return None

def main():
    data = sys.stdin.read().strip().split()
    if len(data) < 3:
        return
    M = int(data[0])
    C = int(data[1])
    K = int(data[2])

    path = bfs(M, C, K)
    if path is None:
        print("NO SOLUTION")
    else:
        steps = len(path) - 1
        print(steps)
        for ml, cl, b in path:
            print(ml, cl, b)

if __name__ == "__main__":
    main()