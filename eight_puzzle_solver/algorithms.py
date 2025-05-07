from collections import deque
import heapq
import random
import math
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


