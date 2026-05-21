import sys

def count_n_queens(n: int) -> int:
    # bit i (0..n-1) biểu thị cột i
    # diag1: đường chéo chính (r - c) -> dùng dịch trái
    # diag2: đường chéo phụ (r + c) -> dùng dịch phải
    full = (1 << n) - 1

    def dfs(cols: int, diag1: int, diag2: int) -> int:
        if cols == full:
            return 1  # đã đặt đủ n quân
        ways = 0
        # các cột trống ở hàng hiện tại
        avail = full & ~(cols | diag1 | diag2)
        while avail:
            p = avail & -avail      # lấy bit 1 thấp nhất
            avail -= p
            ways += dfs(cols | p, (diag1 | p) << 1 & full, (diag2 | p) >> 1)
        return ways

    return dfs(0, 0, 0)

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    print(count_n_queens(n))

if __name__ == "__main__":
    main()


'''
4

2
'''