from collections import deque
import sys

def neighbors(state, cap):
    """Sinh các trạng thái kề từ state = (a,b,c) theo 3 loại thao tác."""
    a, b, c = state
    A, B, C = cap
    x = [a, b, c]
    caps = [A, B, C]

    res = []

    # 1) Fill i: đổ đầy can i
    for i in range(3):
        if x[i] < caps[i]:
            nx = x[:]
            nx[i] = caps[i]
            res.append(tuple(nx))

    # 2) Empty i: đổ hết can i
    for i in range(3):
        if x[i] > 0:
            nx = x[:]
            nx[i] = 0
            res.append(tuple(nx))

    # 3) Pour i -> j
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            if x[i] == 0 or x[j] == caps[j]:
                continue
            t = min(x[i], caps[j] - x[j])
            nx = x[:]
            nx[i] -= t
            nx[j] += t
            res.append(tuple(nx))

    return res

def bfs(cap, target):
    start = (0, 0, 0)
    q = deque([start])
    parent = {start: None}

    def is_goal(s):
        return (s[0] == target) or (s[1] == target) or (s[2] == target)

    if is_goal(start):
        return [start]

    while q:
        cur = q.popleft()
        for nxt in neighbors(cur, cap):
            if nxt not in parent:
                parent[nxt] = cur
                if is_goal(nxt):
                    # truy vết đường đi
                    path = []
                    t = nxt
                    while t is not None:
                        path.append(t)
                        t = parent[t]
                    path.reverse()
                    return path
                q.append(nxt)

    return None

def main():
    data = sys.stdin.read().strip().split()
    if len(data) < 4:
        return

    A = int(data[0])
    B = int(data[1])
    C = int(data[2])
    target = int(data[3])

    path = bfs((A, B, C), target)
    if path is None:
        print("NO SOLUTION")
    else:
        k = len(path) - 1
        print(k)
        for a, b, c in path:
            print(a, b, c)

if __name__ == "__main__":
    main()

'''
3 8 12
1

3
0 0 0
0 0 12
3 0 9
3 8 1
'''