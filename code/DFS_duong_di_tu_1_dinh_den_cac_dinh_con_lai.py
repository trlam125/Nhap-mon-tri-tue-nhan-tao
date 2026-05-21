import sys

def dfs(curr_node, target_node, adj_matrix, labels, visited, path):
    # Đánh dấu đỉnh hiện tại đã ghé thăm và thêm vào đường đi
    visited[curr_node] = True
    path.append(labels[curr_node])
    
    # Nếu tìm thấy đích, trả về True
    if curr_node == target_node:
        return True
    
    # Duyệt các đỉnh kề theo thứ tự tăng dần chỉ số (0 đến n-1)
    n = len(adj_matrix)
    for neighbor in range(n):
        # Nếu có cạnh nối và đỉnh kề chưa được ghé thăm
        if adj_matrix[curr_node][neighbor] == 1 and not visited[neighbor]:
            if dfs(neighbor, target_node, adj_matrix, labels, visited, path):
                return True
    
    # Nếu không tìm thấy đích từ hướng này, thực hiện Backtracking (quay lui)
    path.pop()
    return False

def solve():
    # Đọc toàn bộ dữ liệu từ input
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # 1. Xử lý dữ liệu đầu vào
    n = int(input_data[0])
    labels = input_data[1 : n + 1]
    
    # Ma trận kề n x n
    matrix_flat = input_data[n + 1 : n + 1 + n*n]
    adj_matrix = []
    for i in range(n):
        row = list(map(int, matrix_flat[i*n : (i+1)*n]))
        adj_matrix.append(row)
        
    # Nhãn đỉnh bắt đầu S và đích T
    s_label = input_data[-2]
    t_label = input_data[-1]

    # Ánh xạ nhãn sang chỉ số index
    label_to_idx = {label: i for i, label in enumerate(labels)}
    if s_label not in label_to_idx or t_label not in label_to_idx:
        print("UNREACHABLE")
        return
        
    start_idx = label_to_idx[s_label]
    target_idx = label_to_idx[t_label]

    # 2. Khởi tạo và chạy DFS
    visited = [False] * n
    path = []
    
    if dfs(start_idx, target_idx, adj_matrix, labels, visited, path):
        print(" ".join(path))
    else:
        print("UNREACHABLE")

if __name__ == "__main__":
    solve()