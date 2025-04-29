# main.py
# Entry point for the 8-puzzle solver application.

import pygame
from eight_puzzle_solver.gui import draw_board, draw_buttons, draw_step_count, draw_selected_algorithm, draw_status_bar, draw_input_board, draw_progress_bar, get_clicked_button, get_clicked_input_cell
from eight_puzzle_solver.algorithms import backtracking_search, bfs_solve, dfs_solve, ucs_solve, greedy_solve, iddfs_solve, astar_solve, idastar_solve, hill_climbing_solve, steepest_ascent_hill_climbing_solve, stochastic_hill_climbing_solve, simulated_annealing_solve, beam_search_solve, no_observation_search
from eight_puzzle_solver.utils import generate_fixed_puzzle, is_movable

# Initialize Pygame
pygame.init()

WINDOW = pygame.display.set_mode((900, 800))
clock = pygame.time.Clock()
white = (255, 255, 255)

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

    while running:
        WINDOW.fill(white)
        draw_board(start_state)
        draw_buttons()
        draw_step_count(step_count)
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

                    elif selected_algorithm == "apply":
                        if selected_algorithm_name == "Backtracking Search":
                            # Nếu chọn Backtracking thì không cần input hợp lệ
                            start_state = [None] * 9  # Đưa Main board về trống
                            original_state = [None] * 9
                            input_state = [None] * 9
                            editing_state = False
                            print("Backtracking mode: Không yêu cầu trạng thái hợp lệ. Sử dụng trạng thái random.")
                        else:
                            # Các thuật toán khác vẫn phải kiểm tra đủ 0–8
                            valid_input = sorted(filter(lambda x: x is not None, input_state)) == list(range(9))
                            if valid_input:
                                start_state = input_state[:]
                                original_state = input_state[:]
                                editing_state = False
                                print(f"Trạng thái hợp lệ: {start_state}")
                            else:
                                print("Trạng thái không hợp lệ. Vui lòng nhập đủ số từ 0 đến 8.")
                                continue   
                    elif callable(selected_algorithm):
                        solving = True
                        solution = selected_algorithm(start_state)
                        step = 0
                        if solution is None:
                            solving = False
                            selected_algorithm_name += " (No Solution)"
                            print(f"Không tìm thấy giải pháp cho trạng thái: {start_state}")

        if solving and solution:
            draw_progress_bar(step, len(solution))
            if step < len(solution):
                zero_idx, move_idx = solution[step]
                start_state[zero_idx], start_state[move_idx] = start_state[move_idx], start_state[zero_idx]
                step += 1
                step_count += 1
                pygame.display.flip()
                pygame.time.delay(200)
            else:
                solving = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()