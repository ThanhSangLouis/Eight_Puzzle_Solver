# gui.py
# This module contains all GUI-related functions for the 8-puzzle problem.

import pygame
from .utils import manhattan_distance
from .utils import is_movable
from .algorithms import and_or_search, backtracking_csp, bfs_solve, constraint_checking_solve, dfs_solve, no_observation_search, ucs_solve, greedy_solve, iddfs_solve, astar_solve, idastar_solve, hill_climbing_solve, steepest_ascent_hill_climbing_solve, stochastic_hill_climbing_solve, simulated_annealing_solve, beam_search_solve, partial_observable_search,  ac3, genetic_algorithm_solve, q_learning_solve

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle")
TILE_SIZE = 120
PADDING = 20
MARGIN_TOP_INPUT = 420

# Colors
background_color = (230, 240, 250)
board_color = (0, 128, 128)
tile_gradient_top = (70, 190, 255)
tile_gradient_bottom = (0, 120, 215)
white = (255, 255, 255)
black = (50, 50, 50)
button_color = (255, 185, 15)
button_hover_color = (255, 207, 90)
reset_color = (205, 38, 38)
reset_hover_color = (230, 60, 60)

# Fonts
tile_font = pygame.font.SysFont("arial", 60, bold=True)
button_font = pygame.font.SysFont("arial", 32, bold=True)

selected_algorithm_name = None

# Vẽ bảng 8-Puzzle
def draw_board(state):
    WINDOW.fill(background_color)
    board_rect = pygame.Rect(PADDING, PADDING, TILE_SIZE * 3, TILE_SIZE * 3)
    pygame.draw.rect(WINDOW, board_color, board_rect, border_radius=10)

    mouse_pos = pygame.mouse.get_pos()

    # Kiểm tra nếu trạng thái không chứa số 0
    if 0 not in state:
        print("Error: State does not contain a zero tile.")
        return  # Safeguard to prevent crashes if 0 is missing

    zero_idx = state.index(0)

    for i, num in enumerate(state):
        x, y = (i % 3) * TILE_SIZE + PADDING, (i // 3) * TILE_SIZE + PADDING
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

# Vẽ các nút chọn thuật toán + Reset + Apply
def draw_buttons():
    buttons = ["BFS", "DFS", "UCS", "Greedy", "IDDFS", 
               "A*", "IDA*", "Hill Climbing", "SA HC", "Stochastic HC", 
               "Simu Annealing", "Beam Search", "And-Or Search",
               "No Observation", "Partial Obser", "Const Checking", "Backtracking", "AC3", "Genetic", "Q-Learning", "Reset", "Apply"]
    
    colors = [button_color] * (len(buttons) - 2) + [reset_color, reset_color]
    hover_colors = [button_hover_color] * (len(buttons) - 2) + [reset_hover_color, reset_hover_color]

    button_width, button_height = 200, 50
    spacing = 5

    # Chia đều nút giữa 2 cột
    col_count = 2
    total = len(buttons)
    rows_per_col = (total + col_count - 1) // col_count  # Làm tròn lên

    start_y = PADDING
    start_x1 = WIDTH - 2 * button_width - 60
    start_x2 = WIDTH - button_width - 40
    

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for i, (btn_text, color, hover_color) in enumerate(zip(buttons, colors, hover_colors)):
        col = i % col_count
        row = i // col_count

        x = start_x1 if col == 0 else start_x2
        y = start_y + row * (button_height + spacing)

        rect = pygame.Rect(x, y, button_width, button_height)
        current_color = (50, 150, 255) if rect.collidepoint(mouse_x, mouse_y) else color

        if btn_text == selected_algorithm_name:
            current_color = (50, 150, 255)
            pygame.draw.rect(WINDOW, (255, 255, 255), rect, width=3, border_radius=20)

        shadow = pygame.Rect(rect.x + 2, rect.y + 2, rect.width, rect.height)
        pygame.draw.rect(WINDOW, (180, 180, 180), shadow, border_radius=20)
        pygame.draw.rect(WINDOW, current_color, rect, border_radius=20)
        pygame.draw.rect(WINDOW, white, rect, width=2, border_radius=20)

        text = button_font.render(btn_text, True, white)
        text_rect = text.get_rect(center=rect.center)
        WINDOW.blit(text, text_rect)

# Vẽ ô nhập liệu
def draw_input_board(state):
    guide_font = pygame.font.SysFont("arial", 23, bold=True)
    guide_text = guide_font.render("Input initial state (click cells to change values):", True, black)
    WINDOW.blit(guide_text, (PADDING, MARGIN_TOP_INPUT - 30))
    mouse_pos = pygame.mouse.get_pos()  # Define mouse_pos here

    board_rect = pygame.Rect(PADDING, MARGIN_TOP_INPUT, TILE_SIZE * 3, TILE_SIZE * 3)
    pygame.draw.rect(WINDOW, board_color, board_rect, border_radius=10)

    for i in range(9):
        row, col = i // 3, i % 3
        x = col * TILE_SIZE + PADDING
        y = row * TILE_SIZE + MARGIN_TOP_INPUT
        tile_rect = pygame.Rect(x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10)
        draw_tile_with_gradient(WINDOW, tile_rect)
        pygame.draw.rect(WINDOW, tile_gradient_bottom, tile_rect, border_radius=15, width=2)
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

# Hiển thị số bước
def draw_step_count(step_count):
    step_text = button_font.render(f"Steps: {step_count}", True, black)
    step_rect = step_text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 5)) # Hiển thị ở góc duới bên phải
    WINDOW.blit(step_text, step_rect)

# Kiểm tra click vào ô nhập liệu
def get_clicked_input_cell(pos):
    for i in range(9):
        row, col = i // 3, i % 3
        x = col * TILE_SIZE + PADDING
        y = row * TILE_SIZE + MARGIN_TOP_INPUT  # Sử dụng MARGIN_TOP_INPUT thay vì 400
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        if rect.collidepoint(pos):
            return i
    return None

# Kiểm tra click vào nút để trả về hàm tương ứng
def get_clicked_button(pos):
    button_width = 200
    button_height = 50
    spacing = 5
    start_y = PADDING
    start_x1 = WIDTH - 2 * button_width - 60
    start_x2 = WIDTH - button_width - 40
    
    algorithms = [
        ("BFS", bfs_solve), 
        ("DFS", dfs_solve), 
        ("UCS", ucs_solve), 
        ("Greedy", greedy_solve), 
        ("IDDFS", iddfs_solve), 
        ("A*", astar_solve), 
        ("IDA*", idastar_solve),
        ("Hill Climbing", hill_climbing_solve),
        ("SA HC", steepest_ascent_hill_climbing_solve),
        ("Stochastic HC", stochastic_hill_climbing_solve),
        ("Simu Annealing", simulated_annealing_solve), 
        ("Beam Search", beam_search_solve),
        ("And-Or Search", and_or_search), 
        ("No Observation", no_observation_search),
        ("Partial Obser", partial_observable_search),
        ("Const Checking", constraint_checking_solve),
        ("Backtracking", backtracking_csp), 
        ("AC3", ac3),
        ("Genetic", genetic_algorithm_solve),
        ("Q-Learning", q_learning_solve),
        ("Reset", "reset"),
        ("Apply", "apply")
    ]

    col_count = 2
    rows_per_col = (len(algorithms) + col_count - 1) // col_count

    for i, (btn_text, algorithm) in enumerate(algorithms):
        col = i % col_count
        row = i // col_count

        x_min = start_x1 if col == 0 else start_x2
        y_min = start_y + row * (button_height + spacing)
        x_max = x_min + button_width
        y_max = y_min + button_height

        if x_min <= pos[0] <= x_max and y_min <= pos[1] <= y_max:
            return algorithm, btn_text
    return None, None


# Vẽ tên thuật toán đã chọn
def draw_selected_algorithm(algorithm_name):
    if algorithm_name:
        # Tăng kích thước font chữ
        large_font = pygame.font.SysFont("arial", 36, bold=True)  # Font lớn hơn
        algorithm_text = large_font.render(f"Algorithm: {algorithm_name}", True, (50, 50, 150))
        algorithm_rect = algorithm_text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 60))  # Căn góc dưới bên phải, trên "Steps"
        WINDOW.blit(algorithm_text, algorithm_rect)

# Vẽ thanh trạng thái
def draw_status_bar(status_text):
    # Tăng kích thước font chữ
    larger_status_font = pygame.font.SysFont("arial", 28, bold=True)  # Font lớn hơn
    status_render = larger_status_font.render(status_text, True, (70, 70, 70))
    status_rect = status_render.get_rect(bottomright=(WIDTH - 20, HEIGHT - 110))  # Căn góc dưới bên phải, cao hơn "Algorithm"
    WINDOW.blit(status_render, status_rect)

# Vẽ thanh tiến trình
def draw_progress_bar(current_step, total_steps):
    bar_width = 200
    bar_height = 30
    progress = current_step / total_steps if total_steps > 0 else 0
    progress_width = int(bar_width * progress)

    # Vẽ khung thanh tiến trình
    pygame.draw.rect(WINDOW, black, (WIDTH - 220, HEIGHT - 230, bar_width, bar_height), 2)
    # Vẽ thanh tiến trình
    pygame.draw.rect(WINDOW, (50, 200, 50), (WIDTH - 220, HEIGHT - 230, progress_width, bar_height))

# Vẽ ô với gradient
def draw_tile_with_gradient(surface, rect):
    height = rect.height
    for y in range(height):
        ratio = y / height
        color = [
            tile_gradient_top[0] + (tile_gradient_bottom[0] - tile_gradient_top[0]) * ratio,
            tile_gradient_top[1] + (tile_gradient_bottom[1] - tile_gradient_top[1]) * ratio,
            tile_gradient_top[2] + (tile_gradient_bottom[2] - tile_gradient_top[2]) * ratio
        ]
        pygame.draw.line(surface, color, (rect.x, rect.y + y), (rect.x + rect.width - 1, rect.y + y), 1)
    pygame.draw.rect(surface, (255, 255, 255), rect, width=2, border_radius=15)

def draw_and_or_state(state):
    """
    Hiển thị trạng thái hiện tại trong quá trình thực thi thuật toán AND-OR Search.
    """
    draw_board(state)
    pygame.display.flip()
    pygame.time.delay(500)  # Delay để người dùng có thể quan sát trạng thái