import random
# Hàm tính khoảng cách Manhattan
def manhattan_distance(state):
    goal_state = list(range(1, 9)) + [0]
    distance = 0
    for i in range(9):
        if state[i] != 0:
            current_row, current_col = i // 3, i % 3
            goal_idx = goal_state.index(state[i])
            goal_row, goal_col = goal_idx // 3, goal_idx % 3
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

# Kiểm tra ô có thể di chuyển (cạnh ô trống)    
def is_movable(tile_idx, zero_idx):
    dx = abs((tile_idx % 3) - (zero_idx % 3))
    dy = abs((tile_idx // 3) - (zero_idx // 3))
    return (dx + dy) == 1

def generate_fixed_puzzle():
    return [2, 6, 5, 0, 8, 7, 4, 3, 1]
"""
[2, 3, 6,
 1, 5, 0,
 4, 7, 8]
"""

# Kiểm tra xem trạng thái có thể giải được không (sử dụng nghịch thế)
def is_solvable(state):
    inversions = 0
    for i in range(len(state)):
        if state[i] == 0:
            continue
        for j in range(i + 1, len(state)):
            if state[j] != 0 and state[i] > state[j]:
                inversions += 1
    return inversions % 2 == 0  # Trạng thái giải được nếu số nghịch thế là chẵn

# Tạo trạng thái ngẫu nhiên hợp lệ
def generate_random_state():
    state = list(range(9))  # [0, 1, 2, ..., 8]
    random.shuffle(state)    # Trộn ngẫu nhiên
    while not is_solvable(state):  # Kiểm tra nếu trạng thái hợp lệ
        random.shuffle(state)  # Trộn lại nếu không hợp lệ
    return state
