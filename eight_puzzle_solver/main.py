# main.py
# Entry point for the 8-puzzle solver application.

import random
from eight_puzzle_solver.utils import generate_fixed_puzzle
import pygame
from collections import deque
from eight_puzzle_solver.gui import draw_board, draw_buttons, draw_selected_algorithm, draw_status_bar, draw_input_board, draw_progress_bar, get_clicked_button, get_clicked_input_cell
from eight_puzzle_solver.algorithms import ac3, and_or_search, bfs_solve, constraint_checking_solve, create_consistent_state, create_constraints, dfs_solve, find_solution_path, perform_ac3_with_solution, ucs_solve, greedy_solve, iddfs_solve, astar_solve, idastar_solve, hill_climbing_solve, steepest_ascent_hill_climbing_solve, stochastic_hill_climbing_solve, simulated_annealing_solve, beam_search_solve, no_observation_search
from eight_puzzle_solver.algorithms import backtracking_csp, ac3_solve, genetic_algorithm_solve, q_learning_solve

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 900, 800

WINDOW = pygame.display.set_mode((900, 800))
clock = pygame.time.Clock()
white = (255, 255, 255)
def show_log_surface(screen, log_lines, scroll_position=0, font_size=24, max_height=700, max_width=800):
    # Create a semi-transparent overlay for the background
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black overlay
    screen.blit(overlay, (0, 0))
    
    # Create the log surface
    pygame.font.init()
    font = pygame.font.SysFont("consolas", font_size)
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    padding = 20

    surface_height = min(max_height + 2 * padding, screen.get_height() - 40)
    surface_width = min(max_width + 2 * padding, screen.get_width() - 40)

    log_surface = pygame.Surface((surface_width, surface_height))
    log_surface.fill(background_color)

    # Calculate how many lines can be displayed
    lines_per_page = (surface_height - 2 * padding) // font_size
    
    # Ensure scroll position is within valid range
    max_scroll = max(0, len(log_lines) - lines_per_page)
    scroll_position = min(max_scroll, max(0, scroll_position))
    
    visible_lines = log_lines[scroll_position:scroll_position + lines_per_page]
    
    # Render each visible line
    for i, line in enumerate(visible_lines):
        try:
            text_surface = font.render(str(line), True, text_color)
            log_surface.blit(text_surface, (padding, padding + i * font_size))
        except pygame.error:
            # If there's an error rendering text, display a placeholder
            error_text = font.render(f"[Error rendering line {i}]", True, (255, 0, 0))
            log_surface.blit(error_text, (padding, padding + i * font_size))
    
    # Draw a border around the log surface
    pygame.draw.rect(log_surface, (0, 0, 0), log_surface.get_rect(), 2)
    
    # Draw scrollbar if needed
    if len(log_lines) > lines_per_page:
        scrollbar_width = 10
        scrollbar_height = surface_height * (lines_per_page / max(len(log_lines), 1))
        scrollbar_y = padding + (surface_height - 2 * padding - scrollbar_height) * (
            scroll_position / max(len(log_lines) - lines_per_page, 1))
        
        # Draw scrollbar background
        pygame.draw.rect(log_surface, (200, 200, 200), 
                         (surface_width - scrollbar_width - padding, padding, 
                          scrollbar_width, surface_height - 2 * padding))
        
        # Draw scrollbar thumb
        pygame.draw.rect(log_surface, (100, 100, 100), 
                         (surface_width - scrollbar_width - padding, scrollbar_y, 
                          scrollbar_width, scrollbar_height))
    
    # Draw instructions
    instruction_font = pygame.font.SysFont("consolas", 16)
    instruction_text = instruction_font.render("ESC/Click: Close | ↑/↓: Scroll | PgUp/PgDn: Page", True, (100, 100, 100))
    log_surface.blit(instruction_text, 
                    (padding, surface_height - padding - instruction_font.get_height()))
    
    # Position the log surface in the center of the screen
    log_pos = ((screen.get_width() - surface_width) // 2, 
               (screen.get_height() - surface_height) // 2)
    
    # Blit the log surface to the screen and update the display
    screen.blit(log_surface, log_pos)
    pygame.display.update()
    
    return scroll_position

# 2. Add this function to handle log display and interaction in the main loop
def handle_log_display(screen, log_lines, current_scroll=0):
    showing_log = True
    scroll_position = current_scroll
    
    # Initial render of the log
    scroll_position = show_log_surface(screen, log_lines, scroll_position)
    
    # Handle events while log is displayed
    while showing_log:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    showing_log = False
                elif event.key == pygame.K_UP:
                    scroll_position = max(0, scroll_position - 1)
                    scroll_position = show_log_surface(screen, log_lines, scroll_position)
                elif event.key == pygame.K_DOWN:
                    lines_per_page = (700 - 40) // 24  # max_height - 2*padding // font_size
                    max_scroll = max(0, len(log_lines) - lines_per_page)
                    scroll_position = min(max_scroll, scroll_position + 1)
                    scroll_position = show_log_surface(screen, log_lines, scroll_position)
                elif event.key == pygame.K_PAGEUP:
                    lines_per_page = (700 - 40) // 24
                    scroll_position = max(0, scroll_position - lines_per_page)
                    scroll_position = show_log_surface(screen, log_lines, scroll_position)
                elif event.key == pygame.K_PAGEDOWN:
                    lines_per_page = (700 - 40) // 24
                    max_scroll = max(0, len(log_lines) - lines_per_page)
                    scroll_position = min(max_scroll, scroll_position + lines_per_page)
                    scroll_position = show_log_surface(screen, log_lines, scroll_position)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    showing_log = False
                elif event.button == 4:  # Mouse wheel up
                    scroll_position = max(0, scroll_position - 3)
                    scroll_position = show_log_surface(screen, log_lines, scroll_position)
                elif event.button == 5:  # Mouse wheel down
                    lines_per_page = (700 - 40) // 24
                    max_scroll = max(0, len(log_lines) - lines_per_page)
                    scroll_position = min(max_scroll, scroll_position + 3)
                    scroll_position = show_log_surface(screen, log_lines, scroll_position)
        
        # Small delay to avoid high CPU usage
        pygame.time.delay(30)

    return scroll_position


# Main Function
def main():
    
    original_state = generate_fixed_puzzle()    
    input_state = [None] * 9
    editing_state = True
    start_state = original_state[:]

    running = True
    solving = False
    solution = []
    step = 0
    selected_algorithm = None
    selected_algorithm_name = None
    step_count = 0
    ac3_data = None
    last_ran_algorithm_name = None
    elapsed = 0
    expansions = 0
    showing_log = False
    solution_log_lines = []
    log_scroll_position = 0     


    while running:
        WINDOW.fill(white)
        draw_board(start_state)
        draw_buttons()
        if selected_algorithm_name:
            draw_selected_algorithm(selected_algorithm_name)
        draw_status_bar("Ready" if not solving else "Solving...")  # Hiển thị trạng thái
        if editing_state:
            draw_input_board(input_state)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if editing_state:
                    clicked_cell = get_clicked_input_cell(event.pos)
                    if clicked_cell is not None:
                        if event.button == 3:  # Chuột phải
                            if input_state[clicked_cell] is None or input_state[clicked_cell] == 0:
                                input_state[clicked_cell] = 8
                            else:
                                input_state[clicked_cell] = (input_state[clicked_cell] - 1) % 9
                        else:  # Chuột trái
                            input_state[clicked_cell] = (input_state[clicked_cell] + 1) % 9 if input_state[clicked_cell] is not None else 0

                selected_algorithm, selected_algorithm_name = get_clicked_button(event.pos)
                if selected_algorithm:
                    if selected_algorithm == "reset":
                        start_state = original_state[:]
                        solving = False
                        step = 0
                        step_count = 0
                        selected_algorithm_name = None
                        editing_state = True
                        input_state = [None] * 9
                    elif selected_algorithm == "random":  # Thêm xử lý cho nút Random
                        # Sử dụng hàm generate_random_state từ utils để tạo trạng thái ngẫu nhiên
                        from eight_puzzle_solver.utils import generate_random_state
                        random_state = generate_random_state()
                        # Gán trạng thái ngẫu nhiên vào input_state
                        input_state = random_state[:]
                        # Hiển thị trạng thái ngẫu nhiên
                        draw_input_board(input_state)
                        pygame.display.flip()
                        print(f"Đã tạo trạng thái ngẫu nhiên: {random_state}")
                    elif selected_algorithm == "Show Log":
                        if solution and selected_algorithm_name:
                            try:
                                # Tạo log như cũ
                                solution_log_lines = []
                                solution_log_lines.append(f"Thuật toán: {last_ran_algorithm_name}")
                                solution_log_lines.append(f"Số bước: {len(solution)}")
                                if elapsed > 0:
                                    solution_log_lines.append(f"Thời gian thực thi: {elapsed:.4f} giây")
                                if expansions > 0:
                                    solution_log_lines.append(f"Số node đã mở rộng: {expansions}")
                                solution_log_lines.append("")

                                temp_state = original_state[:]
                                solution_log_lines.append("Trạng thái ban đầu:")
                                for r in range(3):
                                    row_str = " ".join(str(temp_state[r * 3 + c]) if temp_state[r * 3 + c] != 0 else "_" for c in range(3))
                                    solution_log_lines.append(row_str)
                                solution_log_lines.append("")

                                for i, move in enumerate(solution):
                                    if isinstance(move, tuple) and len(move) == 2:
                                        zero, swap = move
                                        temp_state[zero], temp_state[swap] = temp_state[swap], temp_state[zero]
                                        solution_log_lines.append(f"Bước {i + 1}: (swap {zero} ↔ {swap})")
                                        for r in range(3):
                                            row_str = " ".join(str(temp_state[r * 3 + c]) if temp_state[r * 3 + c] != 0 else "_" for c in range(3))
                                            solution_log_lines.append(row_str)
                                        solution_log_lines.append("")

                                # 🟡 Gọi hàm scroll popup
                                log_scroll_position = handle_log_display(WINDOW, solution_log_lines, log_scroll_position)

                            except Exception as e:
                                print(f"⚠️ Error displaying log: {e}")
                        else:
                            print("⚠️ Không có lời giải để hiển thị log.")


                    elif selected_algorithm == "apply":
                        if selected_algorithm_name == "Backtracking":
                            result = backtracking_csp()

                            if result and result["solution"]:
                                # Start with an empty board
                                start_state = [0] * 9
                                solution_path = result["path"]
                                solving = True
                                step = 0
                                step_count = 0
                                expansions = result["nodes_expanded"]
                                print(f"Đã sinh trạng thái hợp lệ bằng CSP. Đã mở rộng {expansions} node.")

                                # Animate the solution path step by step
                                for state in solution_path:
                                    if isinstance(state, list) and len(state) == 3:
                                        start_state = [num for row in state for num in row]
                                        if 0 not in start_state:
                                            start_state.append(0)  # Safeguard to ensure 0 is present
                                        draw_board(start_state)
                                        pygame.display.flip()
                                        pygame.time.delay(500)  # Delay for animation

                                # Display the final solution
                                if result["solution"]:
                                    start_state = [num for row in result["solution"] for num in row]
                                    if 0 not in start_state:
                                        start_state.append(0)  # Safeguard to ensure 0 is present
                                    draw_board(start_state)
                                    pygame.display.flip()
                            else:
                                print("Không thể sinh trạng thái hợp lệ bằng Backtracking CSP.")
                            # Removed the return statement to prevent premature exit
                            solving = False  # Ensure solving is set to False if no solution is found

                        # Xử lý các thuật toán còn lại
                        valid_input = sorted(filter(lambda x: x is not None, input_state)) == list(range(9))
                        if valid_input:
                            start_state = input_state[:]
                            original_state = input_state[:]
                            editing_state = False
                            print(f"Trạng thái hợp lệ: {start_state}")
                        else:
                            print("Trạng thái không hợp lệ. Vui lòng nhập đủ số từ 0 đến 8.")
                    elif callable(selected_algorithm):
                        if selected_algorithm_name == "Backtracking":
                            # Run Backtracking directly without requiring input state validation
                            result = backtracking_csp()

                            if result and result["solution"]:
                                # Start with an empty board
                                start_state = [0] * 9
                                solution_path = result["path"]
                                solving = True
                                step = 0
                                step_count = 0
                                expansions = result["nodes_expanded"]
                                print(f"Đã sinh trạng thái hợp lệ bằng CSP. Đã mở rộng {expansions} node.")

                                # Animate the solution path step by step
                                for state in solution_path:
                                    if isinstance(state, list) and len(state) == 3:
                                        start_state = [num for row in state for num in row]
                                        if 0 not in start_state:
                                            start_state.append(0)  # Safeguard to ensure 0 is present
                                        draw_board(start_state)
                                        pygame.display.flip()
                                        pygame.time.delay(500)  # Delay for animation

                                # Display the final solution
                                if result["solution"]:
                                    start_state = [num for row in result["solution"] for num in row]
                                    if 0 not in start_state:
                                        start_state.append(0)  # Safeguard to ensure 0 is present
                                    draw_board(start_state)
                                    pygame.display.flip()
                            else:
                                print("Không thể sinh trạng thái hợp lệ bằng Backtracking CSP.")
                            # Removed the return statement to prevent premature exit
                            solving = False  # Ensure solving is set to False if no solution is found
                        elif selected_algorithm_name == "Genetic Algo":
                            solving = True
                            solution = genetic_algorithm_solve(start_state)
                            step = 0
                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print(f"Không tìm thấy giải pháp cho trạng thái: {start_state}")
                        elif selected_algorithm_name == "BFS":
                            last_ran_algorithm_name = selected_algorithm_name
                            solving = True
                            print("▶️ Đang chạy BFS...")
                            import time
                            start_time = time.time()
                            solution, expansions = bfs_solve(start_state)
                            elapsed = time.time() - start_time  # Ghi lại thời gian chạy
                            step = 0
                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print(f"Không tìm thấy giải pháp cho trạng thái: {start_state}")
                        elif selected_algorithm_name == "Q-Learning":
                            solving = True
                            print("Đang chạy thuật toán Q-Learning...")
                            # Giới hạn số tập huấn luyện để không mất quá nhiều thời gian
                            solution = q_learning_solve(start_state, episodes=5000, alpha=0.1, gamma=0.9, epsilon=0.2)
                            step = 0
                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print(f"Không tìm thấy giải pháp cho trạng thái: {start_state}")

                        elif selected_algorithm_name == "Const Checking":
                            solving = True
                            result = constraint_checking_solve()
                            if result and result['solution']:
                                solution_path = result['path']
                                step = 0
                                step_count = 0

                                # Animate the solution path step by step
                                for state in solution_path:
                                    start_state[:] = [val for row in state for val in row]
                                    draw_board(start_state)
                                    pygame.display.flip()
                                    pygame.time.delay(500)  # Delay to visualize each step

                                print(f"Solution found after expanding {result['nodes_expanded']} nodes!")
                            else:
                                print("No solution found using Constraint Checking.")
                            solving = False
                            
                        elif selected_algorithm_name == "And-Or Search":
                            solving = True
                            print("Đang chạy thuật toán And-Or Tree Search...")
                            for _ in range(5):
                                result = and_or_search(max_depth=30)
                                if result and result['moves']:
                                    solution = result['moves']
                                    start_state[:] = list(result['start'])
                                    step = 0
                                    step_count = 0
                                    print(f"Đã tìm được giải pháp từ trạng thái: {result['start']}")
                                    break
                            else:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print("Không tìm được lời giải với thuật toán And-Or.")

                        elif selected_algorithm_name == "No Observation Search":
                            solving = True
                            print("🔍 Đang chạy thuật toán No Observation Search...")
                            solution = no_observation_search(start_state)
                            step = 0
                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print("Không tìm được lời giải với No Observation Search.")
                            else:
                                print(f"Đã tìm thấy chuỗi hành động ({len(solution)} bước):")
                                print(solution)
                        

                        elif selected_algorithm_name == "AC3":
                            solving = True
                            print("Running AC3 algorithm to create and solve a valid 8-puzzle state...")
                            
                            # Khởi tạo bảng trống khi sử dụng AC3
                            empty_state = [None] * 9  # Board trống không có số
                            start_state = empty_state[:]  # Cập nhật bảng chính thành trạng thái trống
                            draw_board(start_state)  # Hiển thị bảng trống
                            pygame.display.flip()
                            pygame.time.delay(500)  # Delay để hiển thị bảng trống trước khi bắt đầu thuật toán
                            
                            # Run AC3 directly without requiring input state validation
                            result = ac3_solve()
                            
                            if result and result["solution"]:
                                # Bắt đầu với bảng trống
                                solution_path = result["path"]
                                solving = True
                                step = 0
                                step_count = 0
                                expansions = result["nodes_expanded"]
                                print(f"Generated valid state using AC3. Expanded {expansions} nodes.")

                                # Animate the solution path step by step
                                for state in solution_path:
                                    if isinstance(state, list) and len(state) == 3:
                                        start_state = [num for row in state for num in row]
                                        if 0 not in start_state:
                                            start_state.append(0)  # Safeguard to ensure 0 is present
                                        draw_board(start_state)
                                        pygame.display.flip()
                                        pygame.time.delay(500)  # Delay for animation

                                # Display the final solution
                                if result["solution"]:
                                    start_state = [num for row in result["solution"] for num in row]
                                    if 0 not in start_state:
                                        start_state.append(0)  # Safeguard to ensure 0 is present
                                    draw_board(start_state)
                                    pygame.display.flip()
                            else:
                                print("Could not generate valid state using AC3 algorithm.")
                            solving = False  # Ensure solving is set to False after processing
                        else:
                            last_ran_algorithm_name = selected_algorithm_name
                            solving = True
                            solution = selected_algorithm(start_state)
                            step = 0
                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print(f"Không tìm thấy giải pháp cho trạng thái: {start_state}")

        if showing_log:
            show_log_surface(WINDOW, solution_log_lines, scroll_position=log_scroll_position)

        if solving and solution:
            draw_progress_bar(step, len(solution))
            if step < len(solution):
                # Ensure solution[step] is a tuple of two values
                if isinstance(solution[step], tuple) and len(solution[step]) == 2:
                    zero_idx, move_idx = solution[step]
                    start_state[zero_idx], start_state[move_idx] = start_state[move_idx], start_state[zero_idx]
                    step += 1
                    step_count += 1
                    pygame.display.flip()
                    pygame.time.delay(200)
                else:
                    print("Invalid step format in solution. Expected a tuple of two values.")
                    solving = False
            else:
                solving = False

        if ac3_data and ac3_data['auto_running']:
            current_time = pygame.time.get_ticks()
            # Giảm tần suất cập nhật để giảm hiện tượng giật
            if current_time - ac3_data['last_update_time'] > 500:  # Update mỗi 500ms
                ac3_data['last_update_time'] = current_time

                # Kiểm tra trạng thái hội tụ - nếu không có thay đổi trong domains trong vài bước
                if 'previous_domains' in ac3_data:
                    # So sánh domains hiện tại với domains trước đó
                    current_domains_str = str(ac3_data['csp']['domains'])
                    if current_domains_str == ac3_data['previous_domains']:
                        ac3_data['unchanged_count'] += 1
                    else:
                        ac3_data['unchanged_count'] = 0
                        ac3_data['previous_domains'] = current_domains_str

                    # Nếu domains không thay đổi sau 5 lần kiểm tra liên tiếp, kết thúc thuật toán
                    if ac3_data['unchanged_count'] >= 5:
                        print("Thuật toán AC3 đã hội tụ - không có sự thay đổi sau nhiều bước.")
                        # Kết thúc thuật toán và hiển thị kết quả
                        ac3_data['queue'].clear()  # Xóa queue để kết thúc thuật toán
                        
                        # Hiển thị kết quả cuối cùng và dừng vòng lặp
                        print(f"AC3 đã hoàn thành. Số cung đã xử lý: {ac3_data['counter'][0]}")
                        # Tạo trạng thái kết quả từ domains đã được thu hẹp
                        final_state = [ac3_data['csp']['domains'][f"X{i+1}"][0] for i in range(9)]
                        print(f"Final state: {final_state}")
                        
                        # Áp dụng trạng thái cuối cùng
                        start_state[:] = final_state
                        # Vẽ trạng thái cuối cùng
                        draw_board(start_state)
                        pygame.display.flip()
                        pygame.time.delay(1000)  # Dừng lâu hơn để người dùng xem trạng thái cuối
                        print("AC3 đã tìm được giải pháp hợp lệ!")
                        
                        # Kết thúc AC3
                        ac3_data['auto_running'] = False
                        solving = False
                        continue  # Bỏ qua phần còn lại của vòng lặp
                else:
                    # Khởi tạo biến theo dõi sự hội tụ lần đầu
                    ac3_data['previous_domains'] = str(ac3_data['csp']['domains'])
                    ac3_data['unchanged_count'] = 0
                
                # Tạo hàm callback để vẽ trạng thái hiện tại
                def draw_board_callback(state):
                    # Kiểm tra xem state có hợp lệ không
                    if state and len(state) == 9 and None not in state:
                        # Kiểm tra xem mỗi giá trị từ 0-8 xuất hiện đúng một lần
                        if sorted(state) == list(range(9)):
                            print(f"Displaying state: {state}")
                            # Đảm bảo state được sao chép sang start_state
                            for i in range(9):
                            # Vẽ trạng thái mới
                                draw_board(start_state)
                            pygame.display.flip()
                            # Dừng một chút để người dùng có thể nhìn thấy thay đổi
                            pygame.time.delay(50)
                
                # Chỉ thực hiện một bước AC3 nếu vẫn chưa hội tụ và queue không rỗng
                if ac3_data['auto_running'] and ac3_data['queue']:
                    result = ac3(ac3_data['csp'], ac3_data['counter'], draw_board_callback, ac3_data['queue'])
                    ac3_data['step'] += 1
                    
                    # Nếu queue rỗng hoặc thuật toán thất bại
                    if not ac3_data['queue'] or not result:
                        if result:
                            print(f"AC3 đã hoàn thành. Số cung đã xử lý: {ac3_data['counter'][0]}")
                            # Tạo trạng thái kết quả từ domains đã được thu hẹp
                            final_state = [ac3_data['csp']['domains'][f"X{i+1}"][0] for i in range(9)]
                            print(f"Final state: {final_state}")
                            
                            # Kiểm tra xem kết quả có hợp lệ không
                            if 0 in final_state and len(set(final_state)) == 9:
                                # Áp dụng trạng thái cuối cùng
                                start_state[:] = final_state
                                # Vẽ trạng thái cuối cùng
                                draw_board(start_state)
                                pygame.display.flip()
                                pygame.time.delay(1000)  # Dừng lâu hơn để người dùng xem trạng thái cuối
                                print("AC3 đã tìm được giải pháp hợp lệ!")
                            else:
                                print("Lỗi: Trạng thái kết quả không hợp lệ")
                                # Hiển thị lại trạng thái ban đầu
                                start_state[:] = ac3_data['initial_state']
                        else:
                            print("AC3 không tìm được giải pháp hợp lệ.")
                            # Khôi phục trạng thái ban đầu
                            start_state[:] = ac3_data['initial_state']
                        
                        # Vẽ lại board sau khi đã cập nhật start_state
                        draw_board(start_state)
                        pygame.display.flip()
                        
                        # Kết thúc AC3
                        ac3_data['auto_running'] = False
                        solving = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()