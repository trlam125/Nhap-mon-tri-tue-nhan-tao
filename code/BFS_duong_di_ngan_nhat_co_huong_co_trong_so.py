import sys
import heapq

def solve():
    # 1. Đọc dữ liệu đầu vào
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    labels = input_data[1 : n + 1]
    
    # Ma trận kề n x n
    matrix_flat = input_data[n + 1 : n + 1 + n*n]
    adj_matrix = []
    for i in range(n):
        row = list(map(int, matrix_flat[i*n : (i+1)*n]))
        adj_matrix.append(row)
        
    # S và T
    s_label = input_data[-2]
    t_label = input_data[-1]

    # Ánh xạ nhãn đỉnh sang index
    label_to_idx = {label: i for i, label in enumerate(labels)}
    if s_label not in label_to_idx or t_label not in label_to_idx:
        print("UNREACHABLE")
        return
        
    start_idx = label_to_idx[s_label]
    target_idx = label_to_idx[t_label]

    # 2. Thuật toán Uniform Cost Search (UCS)
    # Priority Queue lưu: (tổng_chi_phí, index_đỉnh_hiện_tại, [danh_sách_đường_đi])
    pq = [(0, start_idx, [s_label])]
    visited = {} # Lưu chi phí nhỏ nhất từng đỉnh đã đạt được

    while pq:
        cost, u_idx, path = heapq.heappop(pq)

        # Nếu tìm thấy đích, vì dùng PQ nên đây chắc chắn là chi phí thấp nhất
        if u_idx == target_idx:
            print(cost)
            print(" ".join(path))
            return

        # Nếu đã ghé thăm đỉnh này với chi phí thấp hơn, bỏ qua
        if u_idx in visited and visited[u_idx] <= cost:
            continue
        visited[u_idx] = cost

        # Duyệt các đỉnh kề v
        for v_idx in range(n):
            weight = adj_matrix[u_idx][v_idx]
            if weight > 0:
                new_cost = cost + weight
                # Chỉ thêm vào PQ nếu chi phí mới tốt hơn chi phí cũ đã biết
                if v_idx not in visited or new_cost < visited[v_idx]:
                    heapq.heappush(pq, (new_cost, v_idx, path + [labels[v_idx]]))

    print("UNREACHABLE")

if __name__ == "__main__":
    solve()