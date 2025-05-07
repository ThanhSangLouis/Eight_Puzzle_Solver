# main.py
# Entry point for the 8-puzzle solver application.

import pygame
from eight_puzzle_solver.gui import draw_board, draw_buttons, draw_step_count, draw_selected_algorithm, draw_status_bar, draw_input_board, draw_progress_bar, get_clicked_button, get_clicked_input_cell
from eight_puzzle_solver.algorithms import bfs_solve, dfs_solve, ucs_solve, greedy_solve, iddfs_solve, astar_solve, idastar_solve, hill_climbing_solve, steepest_ascent_hill_climbing_solve, stochastic_hill_climbing_solve, simulated_annealing_solve, beam_search_solve, no_observation_search
from eight_puzzle_solver.utils import generate_fixed_puzzle, is_movable
from eight_puzzle_solver.algorithms import backtracking_csp

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
                        elif selected_algorithm_name == "No Observation":
                            solving = True
                            solution = no_observation_search(start_state)
                            step = 0
                            if solution is None:
                                solving = False
                                selected_algorithm_name += " (No Solution)"
                                print(f"Không tìm thấy giải pháp cho trạng thái: {start_state}")
                        elif selected_algorithm_name == "AC3":
                            # Run AC3 directly without requiring input state validation
                            result = ac3()

                            if result:
                                print("AC3 completed successfully. Domains:")
                                for var, domain in result.items():
                                    print(f"{var}: {domain}")
                            else:
                                print("AC3 failed due to domain wipeout.")
                        else:
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

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()