import sys

def dls(curr_idx, target_idx, limit, adj_matrix, labels, path):
    """
    Hàm Depth-Limited Search (DLS)
    """
    # Thêm đỉnh hiện tại vào đường đi
    path.append(labels[curr_idx])
    
    # Nếu tìm thấy đích, trả về True
    if curr_idx == target_idx:
        return True
    
    # Nếu đã chạm giới hạn độ sâu mà chưa thấy đích, quay lui
    if limit <= 0:
        path.pop()
        return False
    
    # Duyệt các đỉnh kề theo thứ tự chỉ số tăng dần
    n = len(adj_matrix)
    for neighbor_idx in range(n):
        if adj_matrix[curr_idx][neighbor_idx] == 1:
            # Gọi đệ quy với giới hạn độ sâu giảm đi 1
            if dls(neighbor_idx, target_idx, limit - 1, adj_matrix, labels, path):
                return True
                
    # Không tìm thấy ở nhánh này, quay lui
    path.pop()
    return False

def solve():
    # 1. Đọc và xử lý dữ liệu đầu vào
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    labels = input_data[1 : n + 1]
    
    # Ma trận kề n x n
    matrix_start = n + 1
    matrix_end = matrix_start + n * n
    matrix_flat = input_data[matrix_start : matrix_end]
    
    adj_matrix = []
    for i in range(n):
        row = list(map(int, matrix_flat[i*n : (i+1)*n]))
        adj_matrix.append(row)
        
    s_label = input_data[-2]
    t_label = input_data[-1]

    # Ánh xạ nhãn sang index
    label_to_idx = {label: i for i, label in enumerate(labels)}
    if s_label not in label_to_idx or t_label not in label_to_idx:
        print("UNREACHABLE")
        return
        
    start_idx = label_to_idx[s_label]
    target_idx = label_to_idx[t_label]

    # 2. Thuật toán Iterative Deepening Search (IDS)
    # Thử độ sâu từ 0 đến tối đa n-1 cạnh
    for limit in range(n):
        path = []
        if dls(start_idx, target_idx, limit, adj_matrix, labels, path):
            print(" ".join(path))
            return

    print("UNREACHABLE")

if __name__ == "__main__":
    solve()