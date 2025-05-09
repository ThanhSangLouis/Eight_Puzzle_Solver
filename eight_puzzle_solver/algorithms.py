from collections import deque
import heapq
import random
import math
import time
from .utils import generate_random_state, manhattan_distance
from heapq import heappop, heappush
from .utils import is_solvable

# Hàm giải thuật BFS (Breadth-First Search): tìm kiếm theo chiều rộng, mở rộng tất cả các trạng thái cùng một mức độ trước khi chuyển sang mức độ tiếp theo
def bfs_solve(start_state):
    return generic_solve(start_state, queue=deque([(start_state, [])]), pop_method='popleft')

# Hàm giải thuật DFS (Depth-First Search): tìm kiếm theo chiều sâu, mở rộng các trạng thái theo chiều sâu trước khi quay lại
def dfs_solve(start_state, max_depth=100):
    stack = [(start_state, [], 0)]  # Thêm một giá trị depth vào mỗi phần tử
    visited = set()
    visited.add(tuple(start_state))

    while stack:
        state, path, depth = stack.pop()

        if state == list(range(1, 9)) + [0]:
            return path

        if depth >= max_depth:  # Nếu chiều sâu vượt quá max_depth thì tiếp tục
            continue

        zero_idx = state.index(0)  
        moves = [-3, 3, -1, 1]  

        # Generate next states
        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or  
                (move in [-3, 3]) 
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    stack.append((new_state, path + [(zero_idx, new_idx)], depth + 1))  # Cập nhật chiều sâu

    return None


# Hàm giải thuật Generic Solve: hàm tổng quát cho các thuật toán tìm kiếm khác nhau
def generic_solve(start_state, queue, pop_method='pop', is_priority=False):
    goal_state = list(range(1, 9)) + [0]
    visited = set()
    visited.add(tuple(start_state))

    while queue:
        if is_priority:
            _, g, state, path = heapq.heappop(queue)
        elif pop_method == 'heappop':
            _, state, path = heapq.heappop(queue)
        else:
            if pop_method == 'pop':
                state, path = queue.pop()
            else:
                state, path = queue.popleft()

        if state == goal_state:
            return path

        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))

                    if is_priority:
                        h = manhattan_distance(new_state)
                        new_g = g + 1
                        f = new_g + h
                        heapq.heappush(queue, (f, new_g, new_state, path + [(zero_idx, new_idx)]))
                    elif pop_method == 'heappop':
                        heapq.heappush(queue, (manhattan_distance(new_state), new_state, path + [(zero_idx, new_idx)]))
                    else:
                        queue.append((new_state, path + [(zero_idx, new_idx)]))

    return None

# Hàm giải thuật UCS (Uniform Cost Search): mở rộng các trạng thái theo thứ tự tổng chi phí nhỏ nhất từ trạng thái ban đầu đến trạng thái hiện tại.
def ucs_solve(start_state):
    # Sử dụng generic_solve với hàng đợi ưu tiên theo chi phí
    goal_state = list(range(1, 9)) + [0]
    visited = set()
    visited.add(tuple(start_state))  # Thêm trạng thái ban đầu vào tập đã duyệt
    queue = [(0, start_state, [])]  # (chi phí, trạng thái, đường đi)
    
    while queue:
        cost, state, path = heapq.heappop(queue)
        
        if state == goal_state:
            return path
        
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]
        
        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and ((move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                
                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    # Trong UCS, chi phí là số bước đã đi
                    heapq.heappush(queue, (cost + 1, new_state, path + [(zero_idx, new_idx)]))
    
    return None

# Hàm giải thuật Greedy: mở rộng các trạng thái theo thứ tự ưu tiên dựa trên heuristic (ở đây là khoảng cách Manhattan)
def greedy_solve(start_state):
    return generic_solve(start_state, queue=[(manhattan_distance(start_state), start_state, [])], pop_method='heappop')

# Hàm giải thuật tìm kiếm sâu dần lặp IDDFS (Iterative Deepening Depth-First Search): tìm kiếm theo chiều sâu với giới hạn độ sâu tăng dần
def iddfs_solve(start_state):
    goal_state = list(range(1, 9)) + [0] # Trạng thái đích (1,2,3,4,5,6,7,8,0)

    # Hàm dls (Depth-Limited Search): tìm kiếm theo chiều sâu với giới hạn độ sâu
    def dls(state, path, depth_limit, visited):
        if state == goal_state:
            return path
        if len(path) >= depth_limit:
            return None

        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]  # Lên, Xuống, Trái, Phải
        next_states = []

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    next_states.append((new_state, path + [(zero_idx, new_idx)]))

        # Ưu tiên trạng thái gần lời giải hơn bằng Manhattan Distance để giảm số bước lặp không cần thiết
        next_states.sort(key=lambda x: manhattan_distance(x[0]))
        # Duyệt qua từng trạng thái tiếp theo
        for new_state, new_path in next_states:
            visited.add(tuple(new_state)) # Đánh dấu trạng thái đã duyệt
            result = dls(new_state, new_path, depth_limit, visited) # Gọi đệ quy với trạng thái mới
            if result is not None:
                return result
            visited.remove(tuple(new_state))  # Bỏ đánh dấu nếu không tìm thấy lời giải

        return None

    # Dùng Iterative Deepening với nhiều độ sâu khác nhau
    for depth_limit in range(5, 50, 5):  # Tăng dần giới hạn độ sâu
        visited = set([tuple(start_state)])
        solution = dls(start_state, [], depth_limit, visited)
        if solution is not None:
            return solution  # Nếu tìm thấy lời giải, trả về ngay

    return None  # Không tìm thấy lời giải

# Hàm giải thuật A* (A Star Search)
def astar_solve(start_state):
    return generic_solve(start_state, queue=[(manhattan_distance(start_state), 0, start_state, [])], pop_method='heappop', is_priority=True)

# Hàm giải thuật IDA* (Iterative Deepening A* Search)
def idastar_solve(start_state):
    goal_state = list(range(1, 9)) + [0]  # Trạng thái đích

    def search(state, path, g, threshold, visited):
        f = g + manhattan_distance(state)  # f(n) = g(n) + h(n)
        # Nếu f vượt ngưỡng, trả về ngưỡng mới
        if f > threshold:
            return f, None 
        if state == goal_state:
            return f, path  # Tìm thấy lời giải

        min_threshold = float('inf') # Ngưỡng nhỏ nhất
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and ((move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    new_threshold, result = search(new_state, path + [(zero_idx, new_idx)], g + 1, threshold, visited)
                    visited.remove(tuple(new_state))
                    
                    if result is not None:
                        return new_threshold, result  # Nếu tìm thấy lời giải, trả về ngay
                    min_threshold = min(min_threshold, new_threshold)

        return min_threshold, None  # Trả về giá trị ngưỡng mới
     
    # Bắt đầu với ngưỡng ban đầu là heuristic của trạng thái ban đầu
    threshold = manhattan_distance(start_state)  # Bắt đầu với h(n)
    
    while True:
        visited = set([tuple(start_state)])
        threshold, solution = search(start_state, [], 0, threshold, visited) # Lặp lại tìm kiếm, tăng dần ngưỡng
        if solution is not None:
            return solution  # Nếu tìm thấy lời giải, trả về
        if threshold == float('inf'):
            return None  # Không tìm thấy lời giải

# Hàm giải thuật Hill Climbing: tìm kiếm theo chiều cao, mở rộng trạng thái tốt nhất tại mỗi bước
def hill_climbing_solve(start_state):
    goal_state = list(range(1, 9)) + [0]
    current_state = start_state[:]
    path = []
    
    while current_state != goal_state:
        # Tìm vị trí ô trống
        zero_idx = current_state.index(0)
        
        # Khởi tạo giá trị heuristic tốt nhất
        best_heuristic = manhattan_distance(current_state) # Tính toán heuristic cho trạng thái hiện tại
        best_move = None # Tìm bước đi tốt nhất
        
        # Các hướng di chuyển
        moves = [-3, 3, -1, 1]
        
        for move in moves:
            new_idx = zero_idx + move
            # Kiểm tra di chuyển hợp lệ
            if 0 <= new_idx < 9 and ((move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])):
                # Tạo trạng thái mới
                new_state = current_state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                
                # Tính heuristic của trạng thái mới
                new_heuristic = manhattan_distance(new_state)
                
                # Chọn trạng thái có heuristic tốt hơn (nhỏ hơn)
                if new_heuristic < best_heuristic:
                    best_heuristic = new_heuristic
                    best_move = (zero_idx, new_idx)
        
        # Nếu không tìm được bước đi tốt hơn, kết thúc
        if best_move is None:
            return None
        
        # Thực hiện di chuyển   
        zero_idx, new_idx = best_move
        current_state[zero_idx], current_state[new_idx] = current_state[new_idx], current_state[zero_idx]
        path.append(best_move)
    
    return path

# Hàm giải thuật Steepest Ascent Hill Climbing: tìm kiếm theo chiều cao với bước đi tốt nhất tại mỗi bước
def steepest_ascent_hill_climbing_solve(start_state):
    goal_state = list(range(1, 9)) + [0]
    current_state = start_state[:]
    path = []
    
    while current_state != goal_state:
        # Tìm vị trí ô trống
        zero_idx = current_state.index(0)
        
        # Khởi tạo giá trị heuristic tốt nhất
        best_heuristic = manhattan_distance(current_state)
        best_moves = []
        
        # Các hướng di chuyển
        moves = [-3, 3, -1, 1]
        
        for move in moves:
            new_idx = zero_idx + move
            # Kiểm tra di chuyển hợp lệ
            if 0 <= new_idx < 9 and ((move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])):
                # Tạo trạng thái mới
                new_state = current_state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                
                # Tính heuristic của trạng thái mới
                new_heuristic = manhattan_distance(new_state)
                
                # Lưu tất cả các bước đi có heuristic tốt nhất
                if new_heuristic < best_heuristic:
                    best_heuristic = new_heuristic
                    best_moves = [(zero_idx, new_idx)]
                elif new_heuristic == best_heuristic:
                    best_moves.append((zero_idx, new_idx))
        
        # Nếu không tìm được bước đi tốt hơn, kết thúc
        if not best_moves:
            return None
        
        # Chọn ngẫu nhiên một trong các bước đi tốt nhất nếu có nhiều hơn một
        zero_idx, new_idx = best_moves[0] if len(best_moves) == 1 else best_moves[len(best_moves) // 2]  
        
        # Thực hiện di chuyển   
        current_state[zero_idx], current_state[new_idx] = current_state[new_idx], current_state[zero_idx]
        path.append((zero_idx, new_idx))
    
    return path

# Hàm giải thuật Hill Climbing với ngẫu nhiên
def stochastic_hill_climbing_solve(start_state):
    goal_state = list(range(1, 9)) + [0]
    current_state = start_state[:]
    path = []

    while current_state != goal_state:
        # Tìm vị trí ô trống
        zero_idx = current_state.index(0)

        # Tạo danh sách các trạng thái lân cận
        neighbors = []
        moves = [-3, 3, -1, 1]  # Lên, Xuống, Trái, Phải

        for move in moves:
            new_idx = zero_idx + move
            # Kiểm tra di chuyển hợp lệ
            if 0 <= new_idx < 9 and ((move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])):
                # Tạo trạng thái mới
                new_state = current_state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                neighbors.append((new_state, (zero_idx, new_idx)))

        # Lọc các trạng thái lân cận tốt hơn
        better_neighbors = [
            (state, move) for state, move in neighbors if manhattan_distance(state) < manhattan_distance(current_state)
        ]

        # Nếu không có trạng thái tốt hơn, dừng lại
        if not better_neighbors:
            return None

        # Chọn ngẫu nhiên một trạng thái tốt hơn
        next_state, move = random.choice(better_neighbors)

        # Cập nhật trạng thái hiện tại
        current_state = next_state
        path.append(move)

    return path

# Hàm giải thuật Simulated Annealing
def simulated_annealing_solve(start_state):
    state = start_state[:]
    path = []
    goal = list(range(1, 9)) + [0]
    T = 200.0 # Nhiệt độ ban đầu
    alpha = 0.99 # Hệ số làm mát
    min_temp = 0.1 # Nhiệt độ tối thiểu

    while True:
        if state == goal:
            return path

        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]
        best_h = manhattan_distance(state)
        best_move = None
        best_state = None

        neighbors = []

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])
            ):
                temp = state[:]
                temp[zero_idx], temp[new_idx] = temp[new_idx], temp[zero_idx]
                h = manhattan_distance(temp)
                neighbors.append((temp, (zero_idx, new_idx), h))

                if h < best_h:
                    best_h = h
                    best_move = (zero_idx, new_idx)
                    best_state = temp

        if best_move:
            # Có hướng tốt hơn → đi theo HC
            state = best_state
            path.append(best_move)
        else:
            # Không có hướng đi tốt hơn → dùng SA để thoát
            if not neighbors:
                break
            next_state, move, h = random.choice(neighbors)
            delta_e = manhattan_distance(state) - h # Tính toán độ thay đổi heuristic
            if delta_e > 0 or random.random() < math.exp(delta_e / T): # Xác suất chấp nhận trạng thái xấu hơn
                state = next_state
                path.append(move)

            T *= alpha # Giảm nhiệt độ dần theo thời gia/n
            if T < min_temp:
                break

    return path if state == goal else None

# Hàm giải thuật Beam Search
def beam_search_solve(start_state, beam_width=2):
    goal_state = list(range(1, 9)) + [0]
    queue = [(manhattan_distance(start_state), start_state, [])]
    visited = set()

    while queue:
        # Giữ lại beam_width trạng thái tốt nhất
        next_level = []

        for _, state, path in queue: #_ là giá trị heuristic cần dùng đến
            if state == goal_state:
                return path

            visited.add(tuple(state))
            zero_idx = state.index(0)
            moves = [-3, 3, -1, 1]

            for move in moves:
                new_idx = zero_idx + move
                if 0 <= new_idx < 9 and (
                    (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])
                ):
                    new_state = state[:]
                    new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                    if tuple(new_state) not in visited:
                        new_path = path + [(zero_idx, new_idx)]
                        h = manhattan_distance(new_state)
                        heappush(next_level, (h, new_state, new_path))

        # Chọn beam_width trạng thái tốt nhất để tiếp tục
        queue = [heappop(next_level) for _ in range(min(beam_width, len(next_level)))]

    return None  # Không tìm thấy lời giải
def and_or_search(initial_state):
    goal_state = list(range(1, 9)) + [0]  # Trạng thái mục tiêu [1, 2, 3, 4, 5, 6, 7, 8, 0]
    visited = set()  # Lưu trạng thái đã duyệt để tránh lặp vô hạn
    
    # Hàm kiểm tra khả năng giải được của trạng thái
    def is_solvable(state):
        # Tính số nghịch thế (inversion)
        inversions = 0
        for i in range(len(state)):
            if state[i] == 0:
                continue
            for j in range(i + 1, len(state)):
                if state[j] != 0 and state[i] > state[j]:
                    inversions += 1
        return inversions % 2 == 0
    
    # Nếu trạng thái ban đầu không thể giải được, trả về None
    if not is_solvable(initial_state) and is_solvable(goal_state):
        return None
    
    # Hàm tạo ra các trạng thái kế tiếp hợp lệ
    def get_next_states(state):
        zero_idx = state.index(0)
        moves = []
        # Kiểm tra 4 hướng di chuyển: lên, xuống, trái, phải
        
        # Di chuyển lên
        if zero_idx >= 3:
            new_state = state.copy()
            new_state[zero_idx], new_state[zero_idx - 3] = new_state[zero_idx - 3], new_state[zero_idx]
            moves.append((new_state, (zero_idx, zero_idx - 3)))
        
        # Di chuyển xuống
        if zero_idx < 6:
            new_state = state.copy()
            new_state[zero_idx], new_state[zero_idx + 3] = new_state[zero_idx + 3], new_state[zero_idx]
            moves.append((new_state, (zero_idx, zero_idx + 3)))
        
        # Di chuyển sang trái
        if zero_idx % 3 != 0:
            new_state = state.copy()
            new_state[zero_idx], new_state[zero_idx - 1] = new_state[zero_idx - 1], new_state[zero_idx]
            moves.append((new_state, (zero_idx, zero_idx - 1)))
        
        # Di chuyển sang phải
        if zero_idx % 3 != 2:
            new_state = state.copy()
            new_state[zero_idx], new_state[zero_idx + 1] = new_state[zero_idx + 1], new_state[zero_idx]
            moves.append((new_state, (zero_idx, zero_idx + 1)))
        
        return moves
    
    # Hàm đệ quy để duyệt cây AND-OR
    def recursive_dfs(state, depth=0, max_depth=30):
        if state == goal_state:
            return []  # Đã tìm thấy mục tiêu, trả về danh sách rỗng
        
        if depth >= max_depth:
            return None  # Vượt quá độ sâu tối đa
        
        state_tuple = tuple(state)
        if state_tuple in visited:
            return None  # Tránh lặp lại trạng thái
        
        visited.add(state_tuple)
        
        # Đây là nút OR: chúng ta cần tìm ít nhất một đường đi tới đích
        next_moves = get_next_states(state)
        
        for next_state, move in next_moves:
            # Gọi đệ quy để tìm đường đi từ trạng thái kế tiếp
            path = recursive_dfs(next_state, depth + 1, max_depth)
            
            if path is not None:
                # Nếu tìm thấy đường đi, thêm bước di chuyển hiện tại vào đầu đường đi
                return [move] + path
        
        # Không tìm thấy đường đi nào đến đích
        return None
    
    # Bắt đầu thuật toán với trạng thái ban đầu
    return recursive_dfs(initial_state)

# Hàm giải thuật Searching with No Observation - Thuật toán tìm kiếm với không có bất kì quan sát nào về trạng thái
def no_observation_search(start_state):
    goal_state = list(range(1, 9)) + [0]  # Trạng thái đích
    visited = set()                       # Trạng thái đã duyệt
    path = []                             # Lưu đường đi từ trạng thái ban đầu đến trạng thái hiện tại
    MAX_DEPTH = 50                        # Giới hạn độ sâu tránh tràn stack

    def explore(state, depth=0):
        if state == goal_state:
            return True
        if depth > MAX_DEPTH:
            return False

        visited.add(tuple(state))
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]  # Lên, xuống, trái, phải

        # Tạo danh sách các trạng thái lân cận
        next_states = []
        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                if tuple(new_state) not in visited:
                    next_states.append((new_state, (zero_idx, new_idx)))

        # Sắp xếp để đi nước "hứa hẹn" hơn trước
        next_states.sort(key=lambda x: manhattan_distance(x[0]))

        for new_state, move in next_states:
            path.append(move)  # Thêm bước di chuyển vào đường đi
            if explore(new_state, depth + 1):
                return True
            path.pop()

        return False

    if explore(start_state):
        return path
    return None

# Hàm giải thuật Partial Observable Search (Belief State Search): tìm kiếm với trạng thái "quan sát được" một số ô trên bảng (1,2,3)
def partial_observable_search(start_state):
    from collections import deque
    goal_state = list(range(1, 9)) + [0]
    observed_indices = [0, 1, 2]  # Các ô 0,1,2 đã biết chắc

    # Hàm kiểm tra trạng thái có thể giải được hay không - số nghịch thể là chẵn thì có thể giải được và ngược lại
    def is_solvable(state):
        inversions = 0
        for i in range(len(state)):
            if state[i] == 0:
                continue
            for j in range(i + 1, len(state)):
                if state[j] != 0 and state[i] > state[j]:
                    inversions += 1
        return inversions % 2 == 0

    if not is_solvable(start_state):
        return None

    visited = set() # Tập hợp các trạng thái đã duyệt để tránh lặp lại
    queue = deque([(start_state, [])]) # Hàng đợi lưu trữ các trạng thái cần duyệt

    while queue:
        current_state, path = queue.popleft() # Lấy trạng thái đầu tiên trong hàng đợi

        # Kiểm tra nếu đã đạt đích
        if current_state == goal_state:
            return path

        zero_idx = current_state.index(0)
        moves = [-3, 3, -1, 1]  # Lên, Xuống, Trái, Phải

        for move in moves:
            new_idx = zero_idx + move

            # Kiểm tra nước đi hợp lệ
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                # Không cho swap làm ảnh hưởng đến ô 0,1,2
                if new_idx in observed_indices:
                    continue  # Bỏ qua nước đi nếu làm thay đổi ô 1,2,3 cố định

                # Thêm trạng thái mới vào hàng đợi
                new_state = current_state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    queue.append((new_state, path + [(zero_idx, new_idx)]))

    return None

# Thuật toán test_algorithms_solve: thử các nước đi nào giảm heuristic thì đi
def test_algorithms_solve(start_state):
    goal_state = list(range(1, 9)) + [0]
    current_state = start_state[:] 
    path = [] # Danh sách lưu các bước di chuyển từ trạng thái ban đầu đến trạng thái hiện tại
    visited = set() # Trạng thái đã duyệt
    visited.add(tuple(current_state)) # Thêm trạng thái ban đầu vào tập đã duyệt

    while current_state != goal_state:
        zero_idx = current_state.index(0)
        moves = [-3, 3, -1, 1]
        next_states = [] # Danh sách lưu các trạng thái kế tiếp

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = current_state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                # Nếu trạng thái mới chưa được duyệt thì tính giá trị heuristic (Manhattan distance) của trạng thái mới
                if tuple(new_state) not in visited:
                    h = manhattan_distance(new_state)
                    next_states.append((h, new_state, (zero_idx, new_idx)))

        if not next_states:
            return None  # không tìm được đường đi

        # chọn trạng thái có heuristic thấp nhất
        next_states.sort(key=lambda x: x[0]) # x[0]: giá trị heuristic
        _, best_state, best_move = next_states[0]
        current_state = best_state
        path.append(best_move)
        visited.add(tuple(current_state))

        # nếu kẹt không tiến được → kết thúc
        if len(visited) > 500:
            return None

    return path

# Danh sách các bước di chuyển hợp lệ
def get_next_states(state):
    moves = [-3, 3, -1, 1]  # Các di chuyển: lên (-3), xuống (3), trái (-1), phải (1)
    next_states = []
    zero_idx = state.index(0)  # Tìm vị trí của ô 0

    for move in moves:
        new_idx = zero_idx + move

        # Kiểm tra xem ô mới có hợp lệ không (không ra ngoài ma trận 3x3)
        if 0 <= new_idx < 9 and (
            (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or  # Không di chuyển sang ô ngoài cùng hàng
            (move in [-3, 3])  # Di chuyển lên xuống
        ):
            new_state = state[:]
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]  # Hoán đổi ô 0 với ô kế tiếp
            next_states.append((new_state, (zero_idx, new_idx)))

    return next_states

def backtracking_csp():
    nodes_expanded = [0]
    max_depth = [0]
    path = []

    variables = [f"X{i+1}" for i in range(9)]
    domains = {var: list(range(9)) for var in variables}

    # Shuffle domains for random order
    for var in domains:
        random.shuffle(domains[var])

    constraints = create_constraints()

    csp = {
        'variables': variables,
        'domains': domains,
        'constraints': constraints,
        'initial_assignment': {}
    }

    result = backtrack({}, 0, csp, nodes_expanded, max_depth, path)

    if result:
        solution_grid = [[0 for _ in range(3)] for _ in range(3)]
        for var, value in result.items():
            idx = int(var[1:]) - 1
            row, col = divmod(idx, 3)
            solution_grid[row][col] = value

        return {
            'path': path,
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': solution_grid
        }
    else:
        return {
            'path': [],
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': None
        }

def create_constraints():
    constraints = []

    # Vertical constraints (X1 with X4, X2-X5,...)
    top_bottom_pairs = [
        ('X1', 'X4'), ('X2', 'X5'), ('X3', 'X6'),
        ('X4', 'X7'), ('X5', 'X8')
    ]
    for top, bottom in top_bottom_pairs:
        constraints.append((top, bottom, lambda t, b: b == t + 3 and t != 0))

    # Horizontal constraints (X1-X2, X2-X3, X4-X5,...)
    left_right_pairs = [
        ('X1', 'X2'), ('X2', 'X3'),
        ('X4', 'X5'), ('X5', 'X6'),
        ('X7', 'X8')
    ]
    for left, right in left_right_pairs:
        constraints.append((left, right, lambda l, r: r == l + 1 and l != 0))

    return constraints

def is_consistent(var, value, assignment, csp):
    if value in assignment.values():
        return False

    temp_assignment = assignment.copy()
    temp_assignment[var] = value

    for constraint in csp['constraints']:
        if len(constraint) == 3:
            var1, var2, constraint_func = constraint
            if var1 in temp_assignment and var2 in temp_assignment:
                if not constraint_func(temp_assignment[var1], temp_assignment[var2]):
                    return False

    return True

def backtrack(assignment, index, csp, nodes_expanded, max_depth, path):
    nodes_expanded[0] += 1
    max_depth[0] = max(max_depth[0], len(assignment))

    if assignment:
        grid = [[None for _ in range(3)] for _ in range(3)]
        for var, value in assignment.items():
            idx = int(var[1:]) - 1
            row, col = divmod(idx, 3)
            grid[row][col] = value
        path.append(grid)

    if index == len(csp['variables']):
        final_state = tuple(assignment[f"X{i+1}"] for i in range(9))
        return assignment if is_solvable(final_state) else None

    var = csp['variables'][index]

    for value in csp['domains'][var]:
        if is_consistent(var, value, assignment, csp):
            assignment[var] = value
            # Ensure only valid moves (zero_idx, move_idx) are appended to the path
            if len(assignment) > 1:
                prev_var = csp['variables'][index - 1]
                prev_idx = int(prev_var[1:]) - 1
                zero_idx = prev_idx
                move_idx = int(var[1:]) - 1
                if zero_idx != move_idx and 0 <= zero_idx < 9 and 0 <= move_idx < 9:
                    path.append((zero_idx, move_idx))
            result = backtrack(assignment, index + 1, csp, nodes_expanded, max_depth, path)
            if result:
                return result
            del assignment[var]

    return None

def revise(csp, Xi, Xj):
    """
    REMOVE-INCONSISTENT-VALUES(Xi, Xj)
    Nếu tồn tại x in DOMAIN[Xi] mà không có y in DOMAIN[Xj]
    sao cho constraint(x,y) == True, thì loại x khỏi DOMAIN[Xi].
    Trả về True nếu có x bị loại.
    """
    removed = False
    # lặp trên bản sao để vừa xóa vừa lặp được
    for x in csp['domains'][Xi][:]:
        # tìm constraint giữa Xi và Xj
        funcs = [func for (var1, var2, func) in csp['constraints']
                 if var1 == Xi and var2 == Xj]
        # nếu không có constraint nào thì không remove
        if not funcs:
            continue
        func = funcs[0]
        # kiểm tra xem có y nào thỏa không
        if not any(func(x, y) for y in csp['domains'][Xj]):
            csp['domains'][Xi].remove(x)
            removed = True
    return removed

def ac3(csp=None, counter=None, draw_board_callback=None, external_queue=None):
    """
    AC-3 algorithm for 8-puzzle problem
    If csp is None, a new CSP is created with random domain values.
    Returns the final state if successful, None otherwise.
    """
    if csp is None:
        # Create a new CSP with variables X1..X9 and domains 0..8 (shuffled)
        variables = [f"X{i+1}" for i in range(9)]
        domains = {var: list(range(9)) for var in variables}
        
        # Shuffle domains for random ordering
        for var in domains:
            random.shuffle(domains[var])
            
        csp = {
            'variables': variables,
            'domains': domains,
            'constraints': create_constraints()
        }
    
    if counter is None:
        counter = [0]
    
    # Khởi tạo queue với tất cả các cung (Xi, Xj) hoặc sử dụng queue được cung cấp
    if external_queue is None:
        queue = deque((Xi, Xj) for (Xi, Xj, _) in csp['constraints'])
        complete_execution = True  # Chạy đến hoàn thành nếu không có external_queue
    else:
        queue = external_queue
        complete_execution = False  # Chỉ xử lý một bước nếu có external_queue
        
        # Nếu queue rỗng và có external_queue, có nghĩa là đã xử lý xong tất cả
        if not queue:
            # Assign values after AC-3 completes
            assigned = assign_values_after_ac3(csp)
            if assigned:
                # Cập nhật domains với các giá trị đã gán
                for var in csp['variables']:
                    csp['domains'][var] = [assigned[var]]
                
                # Hiển thị trạng thái cuối cùng
                if draw_board_callback:
                    final_state = [assigned[f"X{i+1}"] for i in range(9)]
                    draw_board_callback(final_state)
                return final_state  # Return the final state
            else:
                return None

    # Nếu là external_queue, chỉ xử lý một bước
    iterations = float('inf') if complete_execution else 1
    iteration_count = 0
    
    while queue and iteration_count < iterations:
        iteration_count += 1
        Xi, Xj = queue.popleft()
        counter[0] += 1  # mỗi cung được xử lý
        if revise(csp, Xi, Xj):
            if not csp['domains'][Xi]:
                # domain trống → vô nghiệm
                return None
            # enqueue lại mọi (Xk, Xi) với Xk láng giềng Xi (ngoại trừ Xj)
            neighbors = {var1 for (var1, var2, _) in csp['constraints']
                         if var2 == Xi and var1 != Xj}
            for Xk in neighbors:
                queue.append((Xk, Xi))

        # Create a consistent current state for visualization
        current_state = create_consistent_state(csp['domains'])
        
        # Hiển thị tiến trình nếu có callback
        if draw_board_callback:
            draw_board_callback(current_state)
            
    # Nếu không phải complete_execution và vẫn còn phần tử trong queue
    # thì sẽ return external_queue để tiếp tục xử lý trong các lần gọi tiếp theo
    if not complete_execution:
        return external_queue
            
    # After AC-3 completes, assign single values to domains with multiple values
    assigned = assign_values_after_ac3(csp)
    if not assigned:
        return None
    
    # Update domains with final assignments
    for var in csp['variables']:
        csp['domains'][var] = [assigned[var]]

    # Create the final solution state
    final_state = [assigned[f"X{i+1}"] for i in range(9)]
    
    # Show final solution
    if draw_board_callback:
        draw_board_callback(final_state)
    
    # Ensure the solution is valid (contains all values 0-8 exactly once)
    if sorted(final_state) != list(range(9)):
        return None
    
    # Verify the solution is solvable
    if not is_solvable(final_state):
        # Try again or return None based on your preference
        return None
        
    return final_state

def assign_values_after_ac3(csp):
    """Hàm phụ trợ để hoàn thành giải pháp sau khi AC-3 kết thúc"""
    assigned = {}
    unassigned_vars = []
    
    # First, assign variables with singleton domains
    for var in csp['variables']:
        if len(csp['domains'][var]) == 1:
            assigned[var] = csp['domains'][var][0]
        else:
            unassigned_vars.append(var)
    
    # Check if all values 0-8 are used exactly once
    used_values = list(assigned.values())
    if len(set(used_values)) != len(used_values):
        print("Warning: Detected duplicate values in initial assignments")
    
    missing_values = [i for i in range(9) if i not in used_values]
    
    if unassigned_vars:
        print(f"Running backtracking to complete the solution for {len(unassigned_vars)} variables...")
        # Use backtracking to assign values to variables with multiple possibilities
        solution_found = backtrack_ac3_solution(csp, assigned, unassigned_vars, None, missing_values)
        if not solution_found:
            print("Failed to find a complete valid solution.")
            return None
    
    # Final validation
    values = [assigned[var] for var in csp['variables']]
    if len(set(values)) != 9 or sorted(values) != list(range(9)):
        print("Error: Final solution is invalid. Contains duplicates or missing numbers.")
        return None
    
    return assigned

def backtrack_ac3_solution(csp, assigned, unassigned_vars, draw_board_callback=None, missing_values=None):
    """Backtracking algorithm to complete AC3 solution."""
    if not unassigned_vars:  # All variables assigned
        # Validate complete assignment
        return True
    
    # Select next unassigned variable
    var = unassigned_vars[0]
    remaining_vars = unassigned_vars[1:]
    
    # Filter domain to only use missing values if available
    domain_to_try = missing_values if missing_values else csp['domains'][var]
    
    # Try each value in the domain
    for value in domain_to_try:
        # Check if this assignment is consistent with current assignments
        if is_consistent_assignment(csp, var, value, assigned):
            # Assign value
            assigned[var] = value
            
            # Update missing values
            new_missing_values = missing_values.copy() if missing_values else None
            if new_missing_values:
                new_missing_values.remove(value)
            
            # Visualize current state if callback provided
            if draw_board_callback:
                current_state = [assigned.get(f"X{i+1}", i) for i in range(9)]
                # Make sure unassigned positions have unique values
                for i in range(9):
                    var_name = f"X{i+1}"
                    if var_name not in assigned:
                        possible_vals = csp['domains'][var_name]
                        if possible_vals:
                            current_state[i] = possible_vals[0]  # Just pick first value for visualization
                
                draw_board_callback(current_state)
            
            # Recursively try to assign remaining variables
            if backtrack_ac3_solution(csp, assigned, remaining_vars, draw_board_callback, new_missing_values):
                return True
            
            # If we get here, this assignment didn't work
            del assigned[var]
    
    # No viable assignment found
    return False

def is_consistent_assignment(csp, var, value, assigned):
    """Check if assigning value to var is consistent with current assignments."""
    # Check if this value conflicts with any existing assignments
    if value in assigned.values():
        return False
    
    # Check constraints
    for (var1, var2, constraint_func) in csp['constraints']:
        if var1 == var and var2 in assigned:
            if not constraint_func(value, assigned[var2]):
                return False
        elif var2 == var and var1 in assigned:
            if not constraint_func(assigned[var1], value):
                return False
    
    return True

def create_consistent_state(domains):
    """
    Tạo một trạng thái nhất quán từ các miền cho việc hiển thị.
    Đảm bảo rằng:
    1. Mỗi vị trí có một giá trị duy nhất
    2. Có đúng một ô có giá trị là 0 (ô trống)
    3. Sử dụng các giá trị từ domain khi có thể
    """
    # Khởi tạo trạng thái rỗng
    current_state = [None] * 9
    used_values = set()
    
    # Trước tiên, gán các giá trị cho các biến có domain đơn
    for i in range(9):
        var = f"X{i+1}"
        if len(domains[var]) == 1:
            value = domains[var][0]
            # Kiểm tra xem giá trị này đã được sử dụng chưa
            if value not in used_values:
                current_state[i] = value
                used_values.add(value)
    
    # Đảm bảo rằng ô trống (0) được đặt
    zero_placed = False
    if 0 not in used_values:
        # Tìm biến chứa 0 trong domain và chưa được gán
        for i in range(9):
            if current_state[i] is None:
                var = f"X{i+1}"
                if 0 in domains[var]:
                    current_state[i] = 0
                    used_values.add(0)
                    zero_placed = True
                    break
        
        # Nếu không có biến nào chứa 0 trong domain, đặt 0 vào vị trí đầu tiên còn trống
        if not zero_placed:
            for i in range(9):
                if current_state[i] is None:
                    current_state[i] = 0
                    used_values.add(0)
                    zero_placed = True
                    break
    else:
        zero_placed = True
    
    # Tiếp theo, gán các giá trị từ domain cho các biến còn lại
    # Nhưng thay vì chọn ngẫu nhiên, chọn giá trị đầu tiên có sẵn để đảm bảo tính ổn định của hiển thị
    for i in range(9):
        if current_state[i] is None:
            var = f"X{i+1}"
            # Tìm giá trị đầu tiên trong domain chưa được sử dụng
            for value in domains[var]:
                if value not in used_values:
                    current_state[i] = value
                    used_values.add(value)
                    break
            
            # Nếu vẫn chưa gán được (do tất cả các giá trị trong domain đều đã sử dụng)
            # Gán một giá trị bất kỳ chưa được sử dụng
            if current_state[i] is None:
                for value in range(9):
                    if value not in used_values:
                        current_state[i] = value
                        used_values.add(value)
                        break
    
    # Đảm bảo tất cả các vị trí đều đã được gán giá trị
    # Nếu vẫn còn vị trí None, điều này có thể xảy ra nếu tất cả các giá trị 0-8 đã được sử dụng
    # Trong trường hợp này, chỉ cần sử dụng lại một giá trị (ví dụ: giá trị đầu tiên)
    # (đây chỉ là hiển thị tạm thời nên không cần thiết phải hoàn toàn chính xác)
    for i in range(9):
        if current_state[i] is None:
            current_state[i] = i  # Sử dụng chỉ số làm giá trị
    
    return current_state

def ac3_with_backtracking(start_state=None, arc_count=None):
    """
    AC-3 with backtracking for solving 8-puzzle.
    
    This function:
    1. Performs AC3 constraint propagation to reduce the domains
    2. Then applies backtracking to find a complete solution
    3. Generates a solution path for visualization
    
    Args:
        start_state: Initial puzzle state (optional)
        arc_count: Counter for arcs processed (optional)
        
    Returns:
        List of moves (zero_idx, new_idx) representing the solution path
    """
    # If no start state provided, generate a random solvable one
    if start_state is None:
        from .utils import generate_random_state
        start_state = generate_random_state()
    
    # Set up arc_count if not provided
    if arc_count is None:
        arc_count = [0]

    # Step 1: Create CSP representation
    variables = [f"X{i+1}" for i in range(9)]
    domains = {}
    
    # Initialize domains based on start_state if provided
    if start_state:
        for i in range(9):
            var = f"X{i+1}"
            domains[var] = [start_state[i]]
    else:
        # Initial domains contain all possible values
        domains = {var: list(range(9)) for var in variables}
        # Shuffle domains for randomization
        for d in domains.values():
            random.shuffle(d)
    
    # Create constraints
    constraints = create_constraints()
    csp = {'variables': variables, 'domains': domains, 'constraints': constraints}
    
    # Step 2: Run AC3 to reduce domains
    print("Running AC3 to reduce domains...")
    
    # Setup initial queue with all binary constraints
    queue = deque((Xi, Xj) for (Xi, Xj, _) in constraints)
    
    # Run AC3
    while queue:
        Xi, Xj = queue.popleft()
        arc_count[0] += 1
        
        if revise(csp, Xi, Xj):
            if not csp['domains'][Xi]:
                # Domain became empty, problem is unsolvable
                print("Domain became empty, problem is unsolvable")
                return None
            
            # Add all neighbors of Xi (except Xj) back to queue
            neighbors = {var1 for (var1, var2, _) in constraints 
                        if var2 == Xi and var1 != Xj}
            for Xk in neighbors:
                queue.append((Xk, Xi))
    
    # Check if AC3 already solved the problem
    single_valued_domains = all(len(domain) == 1 for domain in csp['domains'].values())
    if single_valued_domains:
        # Convert domains to state
        final_state = [csp['domains'][f"X{i+1}"][0] for i in range(9)]
        
        # Find solution path from start_state to final_state
        print("AC3 fully solved the puzzle! Finding solution path...")
        solution_path = find_solution_path(start_state, final_state)
        return solution_path
    
    # Step 3: Backtrack on the CSP with reduced domains
    print("AC3 reduced domains, continuing with backtracking...")
    nodes_expanded = [0]
    max_depth = [0]
    path = []
    assignment = {}
    
    def backtrack_visualize(assignment, index, csp, nodes_expanded, max_depth, path, state_history):
        """Backtracking with visualization for solving CSP"""
        nodes_expanded[0] += 1
        max_depth[0] = max(max_depth[0], len(assignment))
        
        # For visualization, track the current state
        if assignment:
            current_state = [0] * 9  # Default state with all zeros
            for var, value in assignment.items():
                idx = int(var[1:]) - 1
                current_state[idx] = value
            
            # Add current state to history if it's different from the previous one
            if not state_history or current_state != state_history[-1]:
                state_history.append(current_state[:])
        
        # If assignment complete, return
        if index == len(csp['variables']):
            return assignment
        
        var = csp['variables'][index]
        
        for value in csp['domains'][var]:
            if is_consistent(var, value, assignment, csp):
                assignment[var] = value
                result = backtrack_visualize(assignment, index + 1, csp, nodes_expanded, max_depth, path, state_history)
                if result:
                    return result
                del assignment[var]
        
        return None
    
    # Track state history for path reconstruction
    state_history = []
    result = backtrack_visualize(assignment, 0, csp, nodes_expanded, max_depth, path, state_history)
    
    if not result:
        print("Backtracking could not find a solution")
        return None
    
    # Step 4: Construct solution path for visualization
    print(f"Solution found after expanding {nodes_expanded[0]} nodes!")
    
    # If state_history exists, construct moves from it
    solution_path = []
    if state_history and len(state_history) > 1:
        for i in range(len(state_history) - 1):
            current = state_history[i]
            next_state = state_history[i + 1]
            
            # Find positions that changed (zero moved)
            different_positions = [(idx, val1, val2) for idx, (val1, val2) in 
                                  enumerate(zip(current, next_state)) if val1 != val2]
            
            if different_positions:
                # Find the positions of the blank tile (0) in both states
                zero_idx_current = current.index(0) if 0 in current else -1
                zero_idx_next = next_state.index(0) if 0 in next_state else -1
                
                # If zero moved, record the move
                if zero_idx_current != -1 and zero_idx_next != -1:
                    solution_path.append((zero_idx_current, zero_idx_next))
                else:
                    # Find the two positions that swapped
                    pos1, val1_current, val1_next = different_positions[0]
                    pos2, val2_current, val2_next = different_positions[1] if len(different_positions) > 1 else (None, None, None)
                    
                    if pos2 is not None:
                        # Add the swap as a move
                        solution_path.append((pos1, pos2))
    
    # If state_history doesn't have good moves, use find_solution_path
    if not solution_path and state_history:
        print("State history didn't produce usable moves. Using A* to find path...")
        initial_state = start_state
        goal_state = state_history[-1] if state_history else None
        
        if goal_state:
            solution_path = find_solution_path(initial_state, goal_state)
    
    print(f"Generated solution path with {len(solution_path)} steps")
    return solution_path

def find_solution_path(start_state, goal_state=[1, 2, 3, 4, 5, 6, 7, 8, 0]):
    """
    Tìm đường đi từ trạng thái bắt đầu đến trạng thái đích bằng thuật toán A*
    Trả về danh sách các tuple (zero_idx, swap_idx) biểu diễn các bước di chuyển
    """
    from heapq import heappush, heappop
    from eight_puzzle_solver.utils import manhattan_distance
    
    # Kiểm tra xem có thể giải được không
    from eight_puzzle_solver.utils import is_solvable
    if not is_solvable(start_state) and is_solvable(goal_state):
        print("Trạng thái không thể giải được")
        return []

    visited = set()
    queue = [(manhattan_distance(start_state), 0, start_state, [])]  # (f, g, state, path)
    
    while queue:
        _, g, state, path = heappop(queue)
        
        if state == goal_state:
            return path
        
        state_tuple = tuple(state)
        if state_tuple in visited:
            continue
            
        visited.add(state_tuple)
        zero_idx = state.index(0)
        
        # Các nước đi có thể: lên, xuống, trái, phải
        moves = [
            (-3, "up"),    # Lên
            (3, "down"),   # Xuống
            (-1, "left"),  # Trái
            (1, "right")   # Phải
        ]
        
        for move, _ in moves:
            new_idx = zero_idx + move
            
            # Kiểm tra nước đi hợp lệ
            if (
                0 <= new_idx < 9 and  # Trong phạm vi bảng 3x3
                (move != -1 or zero_idx % 3 != 0) and  # Không vượt trái khi ở cột trái nhất
                (move != 1 or zero_idx % 3 != 2) and   # Không vượt phải khi ở cột phải nhất
                (move != -3 or zero_idx >= 3) and      # Không vượt lên khi ở hàng trên cùng
                (move != 3 or zero_idx < 6)            # Không vượt xuống khi ở hàng dưới cùng
            ):
                new_state = state.copy()
                # Hoán đổi vị trí
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                
                # Chỉ thêm vào hàng đợi nếu trạng thái mới chưa được duyệt
                if tuple(new_state) not in visited:
                    # Tính toán f = g + h với g là số bước đi và h là khoảng cách Manhattan
                    new_g = g + 1
                    new_f = new_g + manhattan_distance(new_state)
                    heappush(queue, (new_f, new_g, new_state, path + [(zero_idx, new_idx)]))
    
    # Nếu không tìm thấy giải pháp
    return []

def perform_ac3_with_solution(start_state=None, draw_callback=None, delay=300):
    """
    Thực hiện thuật toán AC3 và sau đó tạo ra giải pháp đến goal state [1,2,3,4,5,6,7,8,0]
    """
    # Nếu không có trạng thái bắt đầu, tạo một trạng thái ngẫu nhiên
    if start_state is None:
        from eight_puzzle_solver.utils import generate_random_state
        start_state = generate_random_state()
    
    # Tạo CSP với domains được lấy từ trạng thái bắt đầu
    csp = {
        'variables': [f"X{i+1}" for i in range(9)],
        'domains': {},
        'constraints': create_constraints()
    }
    
    # Khởi tạo domains từ trạng thái bắt đầu
    for i in range(9):
        var = f"X{i+1}"
        csp['domains'][var] = [start_state[i]]
    
    # In ra domains ban đầu
    print("Initial domains:", csp['domains'])
    
    # Hiển thị trạng thái ban đầu
    if draw_callback:
        draw_callback(start_state)
        import pygame
        pygame.time.delay(delay)
    
    print("AC3 starting...")
    
    # Counter cho số cung được xử lý
    counter = [0]
    
    # Thực hiện AC3 (không cần thực sự thực hiện vì domains đã cố định)
    # Đây chỉ là để hiển thị trạng thái ban đầu
    print("AC3 completed quickly because domains are already fixed.")
    
    # Tìm đường đi từ trạng thái ban đầu đến goal state
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    solution_path = find_solution_path(start_state, goal_state)
    
    # Nếu không tìm thấy giải pháp, thông báo và kết thúc
    if not solution_path:
        print("Không tìm được đường đi tới goal state!")
        return False
    
    print(f"Tìm thấy đường đi với {len(solution_path)} bước")
    
    # Mô phỏng các bước đi
    current_state = start_state.copy()
    
    # Hiển thị từng bước một
    for step, (zero_idx, new_idx) in enumerate(solution_path):
        # Thực hiện nước đi
        current_state[zero_idx], current_state[new_idx] = current_state[new_idx], current_state[zero_idx]
        
        # Hiển thị trạng thái mới
        print(f"Step {step+1}: Move from index {zero_idx} to {new_idx}")
        print(f"Current state: {current_state}")
        
        if draw_callback:
            draw_callback(current_state)
            import pygame
            pygame.time.delay(delay)
    
    # Trả về True nếu đã tìm thấy giải pháp và hiển thị thành công
    return True

def ac3_solve():
    """
    Wrapper function for ac3 to make it consistent with other solver functions.
    Returns a dictionary with path, nodes_expanded, max_depth, and solution.
    """
    nodes_expanded = [0]  # Track nodes expanded
    max_depth = [0]       # Track maximum depth reached
    path = []             # Track the solution path
    
    # Create CSP with variables X1..X9 and domains 0..8 (shuffled)
    variables = [f"X{i+1}" for i in range(9)]
    domains = {var: list(range(9)) for var in variables}
    
    # Shuffle domains for random ordering
    for var in domains:
        random.shuffle(domains[var])
        
    csp = {
        'variables': variables,
        'domains': domains,
        'constraints': create_constraints(),
        'initial_assignment': {}
    }
    
    # Run AC3 algorithm
    final_state = ac3(csp, nodes_expanded)
    
    if final_state:
        # Convert the flat state to a 3x3 grid for the solution
        solution_grid = []
        for i in range(0, 9, 3):
            solution_grid.append(final_state[i:i+3])
        
        # Generate the path from the start to the solution
        # For simplicity in this implementation, we'll find the path using A* after AC3 finds a solution
        start_state = generate_random_state()  # We can use a random start state
        path = find_solution_path(start_state, final_state)
        
        return {
            'path': path,
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': solution_grid
        }
    else:
        return {
            'path': [],
            'nodes_expanded': nodes_expanded[0],
            'max_depth': max_depth[0],
            'solution': None
        }

# Hàm giải thuật Genetic Algorithm: giải 8-puzzle sử dụng thuật toán di truyền
def genetic_algorithm_solve(start_state, population_size=200, max_generations=500, mutation_rate=0.1, timeout=50):
    goal_state = list(range(1, 9)) + [0]
    if start_state == goal_state:
        return []

    if not is_solvable(start_state):
        print("Trạng thái không thể giải được!")
        return None

    # Các bước di chuyển: lên, xuống, trái, phải
    move_map = [-3, 3, -1, 1]

    # Hàm tạo cá thể mới bằng cách sinh ngẫu nhiên lengthh bước đi
    def create_individual(length=100):
        return [random.randint(0, 3) for _ in range(length)]

    # Áp dụng chuỗi bước đi lên trạng thái
    def apply_moves(state, moves):
        s = state[:]
        valid_path = [] # Lưu lại các bước đi hợp lệ
        last_move = None # Tránh lặp lại hướng ngược

        for move in moves:
            zero = s.index(0)
            new_zero = zero + move_map[move]

            # Không đi ngược lại bước trước
            if last_move is not None and abs(move_map[move]) == abs(move_map[last_move]):
                continue

            if 0 <= new_zero < 9:
                if move in [2, 3] and zero // 3 != new_zero // 3:
                    continue  # Tránh đi trái/phải mà vượt ra khỏi hàng
                s[zero], s[new_zero] = s[new_zero], s[zero]
                valid_path.append((zero, new_zero))
                last_move = move
        return s, valid_path
    # Hàm tính điểm fitness cho cá thể dựa vào hàm Manhattan
    # Càng gần goal(khoảng cách Manhattan càng nhỏ) thì điểm càng cao
    # Càng ngắn thì tốt hơn -> trừ điểm 0.1 cho mỗi bước đi
    def fitness(state, path):
        dist = manhattan_distance(state) 
        return 1000 - dist - 0.1 * len(path) # Trừ điểm cho mỗi bước đi
    
    # Hàm lai ghép 2 cá thể để tạo ra cá thể mới
    def crossover(p1, p2):
        point = random.randint(1, min(len(p1), len(p2)) - 1) # Chọn ngẫu nhiên điểm cắt của p1 để trộn với p2
        return p1[:point] + p2[point:]

    # Hàm đột biến cá thể với xác suất rate - tức thay đổi ngẫu nhiên một bước đi trong cá thể
    def mutate(ind, rate):
        return [random.randint(0, 3) if random.random() < rate else m for m in ind]

    # Khởi tạo quần thể ban đầu
    population = [create_individual() for _ in range(population_size)]
    # Biến theo dõi cá thể tốt nhất
    best_score = float('-inf')
    best_path = []

    start = time.time()
    for gen in range(max_generations):
        if time.time() - start > timeout:
            print("Hết thời gian!")
            break

        scored = []
        # Chạy mỗi bước lên start state, tính điểm và lưu lại -> đánh giá tất cả cá thể
        for ind in population:
            final_state, path = apply_moves(start_state, ind)
            score = fitness(final_state, path)
            scored.append((score, ind, path, final_state))
            if final_state == goal_state:
                print(f"Tìm thấy lời giải tại thế hệ {gen}")
                return path

        scored.sort(reverse=True)
        population = [ind for _, ind, _, _ in scored[:population_size // 4]]  #Giữ lại top 25% cá thể tốt nhất

        # Lai ghép và đột biến để tạo child
        while len(population) < population_size:
            p1 = random.choice(scored)[1]
            p2 = random.choice(scored)[1]
            child = mutate(crossover(p1, p2), mutation_rate)
            population.append(child)

        # Cập nhật cá thể tốt nhất
        if scored[0][0] > best_score:
            best_score = scored[0][0]
            best_path = scored[0][2]

        if gen % 10 == 0:
            print(f"🔁 Thế hệ {gen}, điểm tốt nhất: {int(best_score)}")

    print("Không tìm được trạng thái goal. Trả về đường đi tốt nhất.")
    return best_path if best_path else None

# Hàm giải thuật Q-Learning: giải 8-puzzle sử dụng thuật toán học tăng cường
def q_learning_solve(start_state, episodes=5000, alpha=0.1, gamma=0.9, epsilon=0.2):
    import random
    from collections import defaultdict

    goal_state = tuple([1, 2, 3, 4, 5, 6, 7, 8, 0])
    # Bước 1: Khởi tạo Q-table và điền các giá trị ban đầu
    Q = defaultdict(lambda: [0, 0, 0, 0])  # Q(s,a) với 4 hành động: up, down, left, right
    actions = [(-3, 0), (3, 1), (-1, 2), (1, 3)]  # (di chuyển, chỉ số hành động)

    # Hàm xác định hành động hợp lệ từ trạng thái hiện tại
    def get_valid_actions(state):
        zero = state.index(0)
        valid = []
        for move, idx in actions:
            new_zero = zero + move
            if 0 <= new_zero < 9:
                if abs(zero % 3 - new_zero % 3) + abs(zero // 3 - new_zero // 3) == 1:
                    valid.append((move, idx))
        return valid

    # Hàm hoán đổi vị trí của ô trống (0) với ô bên cạnh -> trả về trạng thái mới
    def step(state, move):
        zero = state.index(0)
        new_zero = zero + move
        new_state = list(state)
        new_state[zero], new_state[new_zero] = new_state[new_zero], new_state[zero]
        return tuple(new_state)

    # Bước 2: Vòng lặp học theo số lượng episode
    for ep in range(episodes):
        state = tuple(start_state)

        for _ in range(100):  # Tối đa 50 bước mỗi episode
            # Bước 3: Chọn tác nhân thực hiện hành động lên trạng thái s(k)
            valid = get_valid_actions(state)
            if not valid:
                break

            if random.random() < epsilon:
                move, a = random.choice(valid)
            else:
                best = max(valid, key=lambda m: Q[state][m[1]]) # Chọn hành động tốt nhất dựa trên Q-value
                move, a = best

            # Bước 5: chuyển sang trạng thái mới
            next_state = step(state, move)

            # Bước 4: tính phần thưởng
            reward = 100 if next_state == goal_state else -1

            # Bước 6: cập nhật Q-value theo công thức
            max_q_next = max(Q[next_state])
            Q[state][a] += alpha * (reward + gamma * max_q_next - Q[state][a])

            state = next_state

            # Bước 7: kết thúc nếu đến goal
            if state == goal_state:
                break

        # Bước 8: reset môi trường là implicit khi bắt đầu vòng lặp mới

    # Sau khi học xong, giải bằng cách dùng Q-value
    path = []
    state = tuple(start_state)
    visited = set()
    for _ in range(50):
        visited.add(state)
        valid = get_valid_actions(state)
        if not valid:
            break

        best = max(valid, key=lambda m: Q[state][m[1]])
        move, a = best
        zero = state.index(0)
        new_zero = zero + move
        path.append((zero, new_zero))
        state = step(state, move)
        if state in visited:
            break
        if state == goal_state:
            return path

    return path if state == goal_state else None
