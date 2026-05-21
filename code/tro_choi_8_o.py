from collections import deque

def count_inversions(s):
    a = [x for x in s if x != 0]
    inv_count = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] > a[j]:
                inv_count += 1
    return inv_count

def is_solvable(st, goal):
    return count_inversions(st) % 2 == count_inversions(goal) % 2

def find_zero(s):
    return s.index(0)

def bfs(st, goal):
    if st == goal:
        return 0
    visited = {st}
    q = deque([(st, find_zero(st), 0)])
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        state, z_idx, dist = q.popleft()
        x, y = divmod(z_idx, 3)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                nz_idx = nx * 3 + ny
                new_state = list(state)
                new_state[z_idx], new_state[nz_idx] = new_state[nz_idx], new_state[z_idx]
                new_state_tuple = tuple(new_state)
                if new_state_tuple == goal:
                    return dist + 1
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    q.append((new_state_tuple, nz_idx, dist + 1))
    return -1

st_list = []
tmp1 = input()
for _ in range(3):
    st_list.extend(map(int, input().split()))
st = tuple(st_list)
goal_list = []
tmp2 = input()
for _ in range(3):
    goal_list.extend(map(int, input().split()))
goal = tuple(goal_list)
if not is_solvable(st, goal):
    print("UNSOLVABLE")
else:
    result = bfs(st, goal)
    if result == -1:
        print("UNSOLVABLE")
    else:
        print(result)

'''
Case 1
Input

1 2 3
4 5 6
7 8 0

1 2 3
4 5 6
7 8 0

Output
0

Case 2
Input

1 2 3
4 5 6
7 8 0

1 2 3
4 5 6
7 0 8

Output
1

Case 3
Input

1 2 3
4 5 6
7 8 0

1 2 3
4 5 6
0 7 8

Output
2

Case 4
Input

1 2 3
4 5 6
7 8 0

1 2 3
5 0 6
4 7 8

Output

4

Case 5
Input

1 2 3
4 5 6
7 8 0

1 2 3
4 5 6
8 7 0

Output
UNSOLVABLE
'''