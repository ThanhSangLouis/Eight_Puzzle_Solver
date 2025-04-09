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