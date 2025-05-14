# gui.py
# This module contains all GUI-related functions for the 8-puzzle problem.

import pygame
import time
from .utils import manhattan_distance
from .utils import is_movable
from .algorithms import and_or_search, backtracking_csp, bfs_solve, constraint_checking_solve, dfs_solve, no_observation_search, ucs_solve, greedy_solve, iddfs_solve, astar_solve, idastar_solve, hill_climbing_solve, steepest_ascent_hill_climbing_solve, stochastic_hill_climbing_solve, simulated_annealing_solve, beam_search_solve, partial_observable_search, ac3, genetic_algorithm_solve, q_learning_solve

# Initialize Pygame
pygame.init()

# Constants - Adjust window size 
WIDTH, HEIGHT = 970, 800  # Tăng chiều rộng để có đủ không gian cho các thành phần
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle Solver")
TILE_SIZE = 105 # Giảm nhẹ kích thước từ 110 xuống 100
PADDING = 20
PADDING_RIGHT = 20
PADDING_TOP = 10  # Giảm để di chuyển mọi thứ lên trên
MARGIN_TOP_INPUT = 355  # Điều chỉnh vị trí bảng nhập liệu

# Các hằng số mới để đặt bảng ở bên trái
BOARD_LEFT_X = PADDING

# Colors
background_color = (230, 24, 250)
board_color = (0, 128, 128)
tile_gradient_top = (70, 190, 255)
tile_gradient_bottom = (0, 120, 215)
white = (255, 255, 255)
black = (50, 50, 50)
button_color = (255, 185, 15)
button_hover_color = (255, 207, 90)
reset_color = (205, 38, 38)
reset_hover_color = (230, 60, 60)
section_color = (80, 120, 180)
chart_colors = [(255, 99, 132), (54, 162, 235), (255, 206, 86), 
               (75, 192, 192), (153, 102, 255), (255, 159, 64)]

# Thêm màu cho từng nhóm thuật toán
group_button_colors = {
    "Uninformed Search": (255,160,122),      # Steel Blue
    "Informed Search": (255,165,0),        # Royal Blue
    "Local Search": (0,206,209),            # Sea Green
    "Complex Environments Search": (100,149,237),  # Dark Violet
    "Constraint Satisfaction": (244,164,96),  # Chocolate
    "Reinforcement Learning": (220, 20, 60)    # Crimson
    # "Controls" không được định nghĩa ở đây để giữ màu mặc định
}
# Fonts
tile_font = pygame.font.SysFont("arial", 60, bold=True)
button_font = pygame.font.SysFont("arial", 24, bold=True)
section_font = pygame.font.SysFont("arial", 22, bold=True)
stats_font = pygame.font.SysFont("arial", 22)

selected_algorithm_name = None

# Performance tracking
algorithm_stats = {}
current_benchmark = {
    "time_taken": 0,
    "nodes_expanded": 0,
    "max_memory": 0,
    "solution_length": 0
}

# Algorithm grouping - Better organized to fit the screenshot layout
algorithm_groups = {
    "Uninformed Search": ["BFS", "DFS", "UCS", "IDDFS"],
    "Informed Search": ["Greedy", "A*", "IDA*"],
    "Local Search": ["Hill Climbing", "SA HC", "Stochastic HC", "Simu Annealing", "Genetic", "Beam Search"],
    "Complex Environments Search": ["And-Or Search", "No Observation", "Partial Obser"],
    "Constraint Satisfaction": ["Const Checking", "Backtracking", "AC3"],
    "Reinforcement Learning": ["Q-Learning"],
    "Controls": ["Reset", "Apply", "Random"]
}

# Create a flattened list of all algorithms
all_algorithms = sum([algs for group, algs in algorithm_groups.items() 
                     if group != "Controls"], [])

# Vẽ bảng 8-Puzzle - chuyển sang bên trái
def draw_board(state):
    board_rect = pygame.Rect(BOARD_LEFT_X + 30, PADDING_TOP, TILE_SIZE * 3, TILE_SIZE * 3)

    pygame.draw.rect(WINDOW, board_color, board_rect, border_radius=10)

    mouse_pos = pygame.mouse.get_pos()

    # Kiểm tra nếu trạng thái không chứa số 0
    if 0 not in state:
        print("Error: State does not contain a zero tile.")
        return  # Safeguard to prevent crashes if 0 is missing

    zero_idx = state.index(0)

    for i, num in enumerate(state):
        x = (i % 3) * TILE_SIZE + BOARD_LEFT_X+30
        y = (i // 3) * TILE_SIZE + PADDING_TOP
        if num != 0:
            tile_rect = pygame.Rect(x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10)
            shadow_rect = pygame.Rect(x + 8, y + 8, TILE_SIZE - 10, TILE_SIZE - 10)
            pygame.draw.rect(WINDOW, (30, 30, 30, 100), shadow_rect, border_radius=15)
            draw_tile_with_gradient(WINDOW, tile_rect)
            pygame.draw.rect(WINDOW, tile_gradient_bottom, tile_rect, border_radius=15, width=2)
            text = tile_font.render(str(num), True, white)
            text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
            WINDOW.blit(text, text_rect)

            # Thêm highlight nếu rê chuột vào ô có thể di chuyển
            if pygame.Rect(x, y, TILE_SIZE, TILE_SIZE).collidepoint(mouse_pos):
                if is_movable(i, zero_idx):
                    highlight = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10), pygame.SRCALPHA)
                    highlight.fill((255, 255, 255, 50))  # Alpha = 50
                    WINDOW.blit(highlight, (x + 5, y + 5))

# Vẽ các nút chọn thuật toán theo từng nhóm - chuyển sang bên phải
def draw_buttons():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_width, button_height = 150, 35  # Giảm chiều cao nút một chút
    spacing = 12  # Giảm khoảng cách giữa các nút
    
    # Calculate starting positions - Chuyển sang bên phải
    menu_start_x = WIDTH - PADDING_RIGHT - 3 * button_width - spacing
    menu_start_y = PADDING_TOP
    group_spacing = 3  # Giảm khoảng cách giữa các nhóm xuống 10px
    
    y_offset = menu_start_y
    
    for group_name, algorithms in algorithm_groups.items():
        # Draw group heading
        heading_text = section_font.render(group_name, True, section_color)
        heading_rect = heading_text.get_rect()
        WINDOW.blit(heading_text, (menu_start_x, y_offset))
        y_offset += 25  # Giảm khoảng cách giữa heading và nút xuống còn 25px
        
        # Lấy màu mặc định cho nhóm hiện tại hoặc sử dụng màu mặc định nếu không có
        current_group_color = group_button_colors.get(group_name, button_color)
        
        # Draw buttons for this group in rows of 2
        for i, btn_text in enumerate(algorithms):
            x = menu_start_x + (i % 2) * (button_width + spacing)
            y = y_offset + (i // 2) * (button_height + 5)  # Giảm khoảng cách dọc giữa các nút
            
            rect = pygame.Rect(x, y, button_width, button_height)
            
            # Determine button color
            if btn_text in ["Reset", "Apply", "Random"]:
                base_color = reset_color if btn_text == "Reset" else button_color
                hover_color = reset_hover_color if btn_text == "Reset" else button_hover_color
            else:
                # Sử dụng màu nhóm cho các nút thuật toán
                base_color = current_group_color
                hover_color = button_hover_color
                
            current_color = hover_color if rect.collidepoint(mouse_x, mouse_y) else base_color
            
            # Highlight selected algorithm
            if btn_text == selected_algorithm_name:
                current_color = (50, 150, 255)
            
            # Draw button with rounded corners like in screenshot
            pygame.draw.rect(WINDOW, current_color, rect, border_radius=15)
            
            text = button_font.render(btn_text, True, white)
            text_rect = text.get_rect(center=rect.center)
            WINDOW.blit(text, text_rect)
        
        # Update offset for next group
        button_count = len(algorithms)
        rows = (button_count + 1) // 2
        y_offset += rows * (button_height + 5) + group_spacing

# Vẽ ô nhập liệu - chuyển sang bên trái
def draw_input_board(state):
    guide_font = pygame.font.SysFont("arial", 26, bold=True)
    guide_text = guide_font.render("Input initial state ", True, black)
    WINDOW.blit(guide_text, (BOARD_LEFT_X + 80, MARGIN_TOP_INPUT - 30))

    mouse_pos = pygame.mouse.get_pos()  # Define mouse_pos here

    board_rect = pygame.Rect(BOARD_LEFT_X + 30, MARGIN_TOP_INPUT, TILE_SIZE * 3, TILE_SIZE * 3)

    pygame.draw.rect(WINDOW, board_color, board_rect, border_radius=10)

    for i in range(9):
        row, col = i // 3, i % 3
        x = col * TILE_SIZE + BOARD_LEFT_X + 30
        y = row * TILE_SIZE + MARGIN_TOP_INPUT
        tile_rect = pygame.Rect(x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10)
        draw_tile_with_gradient(WINDOW, tile_rect)
        
        # Làm nổi bật ô được chọn
        if tile_rect.collidepoint(mouse_pos):
            pygame.draw.rect(WINDOW, (255, 255, 255), tile_rect, width=3, border_radius=15)
        num = state[i]
        if num is not None:
            font_size = 30 if num == "None" else 60  # Adjust font size for 'None'
            text_font = pygame.font.SysFont("arial", font_size, bold=True)
            text = text_font.render(str(num), True, white)
            text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
            WINDOW.blit(text, text_rect)
            
def get_clicked_input_cell(pos):
    for i in range(9):
        row, col = i // 3, i % 3
        x = col * TILE_SIZE + BOARD_LEFT_X
        y = row * TILE_SIZE + MARGIN_TOP_INPUT
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        if rect.collidepoint(pos):
            return i
    return None

# Kiểm tra click vào nút để trả về hàm tương ứng - điều chỉnh cho layout mới
def get_clicked_button(pos):
    button_width, button_height = 150, 35  # Khớp với draw_buttons
    spacing = 12  # Khớp với draw_buttons - Sửa từ 30 xuống 12
    
    # Calculate starting positions - Điều chỉnh cho vị trí mới
    menu_start_x = WIDTH - PADDING_RIGHT - 3 * button_width - spacing  # Sửa từ 2 lên 3
    menu_start_y = PADDING_TOP
    group_spacing = 3  # Khớp với draw_buttons - Sửa từ 5 xuống 3
    
    y_offset = menu_start_y
    
    algorithm_functions = {
        "BFS": bfs_solve, 
        "DFS": dfs_solve, 
        "UCS": ucs_solve, 
        "Greedy": greedy_solve, 
        "IDDFS": iddfs_solve, 
        "A*": astar_solve, 
        "IDA*": idastar_solve,
        "Hill Climbing": hill_climbing_solve,
        "SA HC": steepest_ascent_hill_climbing_solve,
        "Stochastic HC": stochastic_hill_climbing_solve,
        "Simu Annealing": simulated_annealing_solve, 
        "Beam Search": beam_search_solve,
        "And-Or Search": and_or_search, 
        "No Observation": no_observation_search,
        "Partial Obser": partial_observable_search,
        "Const Checking": constraint_checking_solve,
        "Backtracking": backtracking_csp, 
        "AC3": ac3,
        "Genetic": genetic_algorithm_solve,
        "Q-Learning": q_learning_solve,
        "Reset": "reset",
        "Apply": "apply",
        "Random": "random"
    }
    
    for group_name, algorithms in algorithm_groups.items():
        # Skip group heading
        y_offset += 25  # Sửa từ 35 xuống 25 để khớp với draw_buttons
        
        # Check buttons in this group
        for i, btn_text in enumerate(algorithms):
            x = menu_start_x + (i % 2) * (button_width + spacing)
            y = y_offset + (i // 2) * (button_height + 5)  # Khớp với draw_buttons
            
            rect = pygame.Rect(x, y, button_width, button_height)
            
            if rect.collidepoint(pos):
                return algorithm_functions.get(btn_text), btn_text
        
        # Update offset for next group
        button_count = len(algorithms)
        rows = (button_count + 1) // 2
        y_offset += rows * (button_height + 5) + group_spacing
    
    return None, None

# Adjust status display locations
def draw_selected_algorithm(algorithm_name):
    if algorithm_name:
        text = button_font.render(f"Algorithm: {algorithm_name}", True, (50, 50, 150))
        WINDOW.blit(text, (PADDING , HEIGHT - 90))

def draw_status_bar(status_text):
    status_font = pygame.font.SysFont("arial", 24, bold=True)
    status_text_render = status_font.render(status_text, True, (70, 70, 70))
    status_rect = status_text_render.get_rect(center=(WIDTH // 2 - 420, HEIGHT - 106))
    WINDOW.blit(status_text_render, status_rect)

# Vẽ thanh tiến trình - Khôi phục lại để hiển thị tiến trình
def draw_progress_bar(current_step, total_steps):
    if total_steps > 0:
        bar_width = 840
        bar_height = 20
        bar_x = 30
        bar_y = HEIGHT - 30
        
        # Vẽ nền cho thanh tiến trình
        pygame.draw.rect(WINDOW, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height))
        
        # Vẽ phần tiến trình đã hoàn thành
        progress_width = (current_step / total_steps) * bar_width
        pygame.draw.rect(WINDOW, (50, 180, 50), (bar_x, bar_y, progress_width, bar_height))
        
        # Vẽ viền
        pygame.draw.rect(WINDOW, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Hiển thị số bước
        step_text = button_font.render(f"Step: {current_step}/{total_steps}", True, black)
        WINDOW.blit(step_text, (PADDING, HEIGHT - 60))

# Vẽ ô với gradient - simplified to match screenshot
def draw_tile_with_gradient(surface, rect):
    # Draw a simple blue tile with rounded corners like in the screenshot
    pygame.draw.rect(surface, tile_gradient_top, rect, border_radius=10)
    pygame.draw.rect(surface, tile_gradient_bottom, rect, width=2, border_radius=10)

def draw_and_or_state(state):
    """
    Hiển thị trạng thái hiện tại trong quá trình thực thi thuật toán AND-OR Search.
    """
    draw_board(state)
    pygame.display.flip()
    pygame.time.delay(500)  # Delay để người dùng có thể quan sát trạng thái


# Sửa hàm draw_everything để thêm hiển thị biểu đồ
def draw_everything(state, input_state, step_count, progress=(0, 1)):
    WINDOW.fill(background_color)
    draw_board(state)
    draw_buttons()
    draw_input_board(input_state)
    draw_selected_algorithm(selected_algorithm_name)
    pygame.display.flip()