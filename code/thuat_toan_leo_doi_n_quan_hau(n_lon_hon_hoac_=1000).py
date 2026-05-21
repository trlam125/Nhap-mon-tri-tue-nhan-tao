import sys
import random

INF = 10**18
BETA_SEED = 0  # seed cố định để dễ chấm (có thể đổi nếu muốn ngẫu nhiên)

def comb2(x: int) -> int:
    return x * (x - 1) // 2

def solve(n: int, k_move: int, max_restarts: int, max_steps: int, X: int):
    rng = random.Random(BETA_SEED)

    diag_len = 2 * n - 1
    full_mask = (1 << n) - 1  # không dùng bitmask ở đây, giữ cho dễ hiểu

    best_conf = INF
    steps_used = 0
    restarts_used = 0

    def init_state():
        # Khởi tạo ngẫu nhiên: 1 hậu / cột, dùng hoán vị để giảm xung đột hàng (nhanh hơn thực tế)
        pos = list(range(n))
        rng.shuffle(pos)

        row = [0] * n
        d1 = [0] * diag_len  # r - c + (n-1)
        d2 = [0] * diag_len  # r + c

        for c, r in enumerate(pos):
            row[r] += 1
            d1[r - c + (n - 1)] += 1
            d2[r + c] += 1

        total = 0
        for x in row: total += comb2(x)
        for x in d1:  total += comb2(x)
        for x in d2:  total += comb2(x)
        return pos, row, d1, d2, total

    def col_conflicted(c, pos, row, d1, d2):
        r = pos[c]
        return (row[r] > 1) or (d1[r - c + (n - 1)] > 1) or (d2[r + c] > 1)

    def pick_conflicted_col(pos, row, d1, d2):
        # thử random vài lần để nhanh
        for _ in range(30):
            c = rng.randrange(n)
            if col_conflicted(c, pos, row, d1, d2):
                return c
        # fallback: quét
        for c in range(n):
            if col_conflicted(c, pos, row, d1, d2):
                return c
        return None  # không còn xung đột

    def update_total(counts, idx, delta, total):
        old = counts[idx]
        total -= comb2(old)
        new = old + delta
        counts[idx] = new
        total += comb2(new)
        return total

    def move_min_conflicts(c, pos, row, d1, d2, total):
        # bỏ hậu khỏi vị trí cũ
        old_r = pos[c]
        total = update_total(row, old_r, -1, total)
        total = update_total(d1, old_r - c + (n - 1), -1, total)
        total = update_total(d2, old_r + c, -1, total)

        # chọn hàng r làm xung đột nhỏ nhất: row[r] + d1[r-c+n-1] + d2[r+c]
        base_d1 = -c + (n - 1)
        base_d2 = c

        best = INF
        chosen = 0
        ties = 0

        # reservoir sampling để random khi hòa
        for r in range(n):
            conf = row[r] + d1[r + base_d1] + d2[r + base_d2]
            if conf < best:
                best = conf
                chosen = r
                ties = 1
            elif conf == best:
                ties += 1
                if rng.randrange(ties) == 0:
                    chosen = r

        # đặt hậu vào hàng mới
        pos[c] = chosen
        total = update_total(row, chosen, +1, total)
        total = update_total(d1, chosen - c + (n - 1), +1, total)
        total = update_total(d2, chosen + c, +1, total)

        return total

    for r in range(max_restarts):
        if steps_used >= X:
            break

        restarts_used = r + 1
        pos, row, d1, d2, total = init_state()
        best_conf = min(best_conf, total)

        used_in_restart = 0

        while total != 0 and used_in_restart < max_steps and steps_used < X:
            # kiểu chuyển động k quân: làm k move liên tiếp trong 1 vòng
            for _ in range(k_move):
                if total == 0 or used_in_restart >= max_steps or steps_used >= X:
                    break
                c = pick_conflicted_col(pos, row, d1, d2)
                if c is None:
                    total = 0
                    break

                total = move_min_conflicts(c, pos, row, d1, d2, total)
                steps_used += 1
                used_in_restart += 1
                if total < best_conf:
                    best_conf = total

        if best_conf == 0:
            break

    return best_conf, steps_used, restarts_used

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    n = int(data[0])
    k_move = int(data[1])
    max_restarts = int(data[2])
    max_steps = int(data[3])
    X = int(data[4])

    best_conf, steps_used, restarts_used = solve(n, k_move, max_restarts, max_steps, X)

    print(f"best_conflicts={best_conf}")
    print(f"steps_used={steps_used}")
    print(f"restarts_used={restarts_used}")

if __name__ == "__main__":
    main()

'''
1000
2
10 5000
50000
2

Criteria:
- best_conflicts == 0
- steps_used <= 50000
'''