import sys
import random
import math

INF = 10**18
SEED = 0  # seed cố định để kết quả ổn định khi chấm

def solve_sa(n: int, k_move: int, max_restarts: int, max_steps: int, X: int):
    rng = random.Random(SEED)
    diag_len = 2 * n - 1

    # cập nhật nhanh tổng số cặp xung đột (pairs) khi tăng/giảm count một line
    # line có k quân -> đóng góp C(k,2)
    # remove: C(k,2)-C(k-1,2)=k-1 ; add: C(k+1,2)-C(k,2)=k
    def dec_line(cnt, idx, total):
        total -= (cnt[idx] - 1)
        cnt[idx] -= 1
        return total

    def inc_line(cnt, idx, total):
        total += cnt[idx]
        cnt[idx] += 1
        return total

    def init_state():
        # Khởi tạo bằng hoán vị để tránh xung đột hàng ngay từ đầu (rất có lợi cho n lớn)
        pos = list(range(n))
        rng.shuffle(pos)

        row = [0] * n
        d1 = [0] * diag_len  # r - c + (n-1)
        d2 = [0] * diag_len  # r + c

        total = 0
        for c, r in enumerate(pos):
            # add queen
            total = inc_line(row, r, total)
            total = inc_line(d1, r - c + (n - 1), total)
            total = inc_line(d2, r + c, total)
        return pos, row, d1, d2, total

    def col_conflicted(c, pos, row, d1, d2):
        r = pos[c]
        return (row[r] > 1) or (d1[r - c + (n - 1)] > 1) or (d2[r + c] > 1)

    def pick_conflicted_col(pos, row, d1, d2):
        # random thử vài lần cho nhanh
        for _ in range(30):
            c = rng.randrange(n)
            if col_conflicted(c, pos, row, d1, d2):
                return c
        # fallback: quét
        for c in range(n):
            if col_conflicted(c, pos, row, d1, d2):
                return c
        return None

    def best_row_for_col(c, old_r, row, d1, d2):
        # counts hiện tại là sau khi đã remove queen khỏi (c, old_r)
        base_d1 = -c + (n - 1)
        base_d2 = c
        best = INF
        chosen = 0
        ties = 0
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
        return chosen

    best_conflicts = INF
    steps_used = 0
    restarts_used = 0

    # tham số nhiệt độ
    T0 = max(1.0, 2.0 * n)   # nhiệt độ đầu
    Tmin = 0.01

    for r in range(max_restarts):
        if steps_used >= X:
            break

        restarts_used = r + 1
        pos, row, d1, d2, total = init_state()
        if total < best_conflicts:
            best_conflicts = total

        used_in_restart = 0

        while total != 0 and used_in_restart < max_steps and steps_used < X:
            # mỗi "vòng" thực hiện k_move bước liên tiếp
            for _ in range(k_move):
                if total == 0 or used_in_restart >= max_steps or steps_used >= X:
                    break

                c = pick_conflicted_col(pos, row, d1, d2)
                if c is None:
                    total = 0
                    break

                old_r = pos[c]

                # temperature theo lịch làm nguội tuyến tính trong mỗi restart
                frac = used_in_restart / max_steps
                T = max(Tmin, T0 * (1.0 - frac))

                # remove queen khỏi vị trí cũ
                total = dec_line(row, old_r, total)
                total = dec_line(d1, old_r - c + (n - 1), total)
                total = dec_line(d2, old_r + c, total)

                # số cặp sẽ thêm lại nếu đặt về old_r (sau khi remove)
                base_d1 = -c + (n - 1)
                base_d2 = c
                add_old = row[old_r] + d1[old_r + base_d1] + d2[old_r + base_d2]

                # đề xuất new_r:
                # đa phần chọn best (min-conflicts), thỉnh thoảng random để "thoát kẹt" đúng tinh thần SA
                if rng.random() < min(0.2, T / T0 * 0.2):
                    new_r = rng.randrange(n)
                else:
                    new_r = best_row_for_col(c, old_r, row, d1, d2)

                add_new = row[new_r] + d1[new_r + base_d1] + d2[new_r + base_d2]
                delta = add_new - add_old  # >0 là xấu hơn

                accept = False
                if delta <= 0:
                    accept = True
                else:
                    # SA acceptance
                    # p = exp(-delta / T)
                    if rng.random() < math.exp(-delta / T):
                        accept = True

                if accept:
                    pos[c] = new_r
                    total = inc_line(row, new_r, total)
                    total = inc_line(d1, new_r - c + (n - 1), total)
                    total = inc_line(d2, new_r + c, total)
                else:
                    # revert về old_r
                    pos[c] = old_r
                    total = inc_line(row, old_r, total)
                    total = inc_line(d1, old_r - c + (n - 1), total)
                    total = inc_line(d2, old_r + c, total)

                steps_used += 1
                used_in_restart += 1

                if total < best_conflicts:
                    best_conflicts = total

        if best_conflicts == 0:
            break

    return best_conflicts, steps_used, restarts_used


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    n = int(data[0])
    k_move = int(data[1])
    restarts = int(data[2])
    max_steps = int(data[3])
    X = int(data[4])

    best_conf, steps_used, restarts_used = solve_sa(n, k_move, restarts, max_steps, X)

    print(f"best_conflicts={best_conf}")
    print(f"steps_used={steps_used}")
    print(f"restarts_used={restarts_used}")

if __name__ == "__main__":
    main()

'''
1000
1
10 5000
50000
1

Criteria:
- best_conflicts == 0
- steps_used <= 50000
'''