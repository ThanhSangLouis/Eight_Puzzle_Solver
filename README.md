# 8-Puzzle Solver Game 🎮

## Giới Thiệu
Chào mừng đến với **8-Puzzle Solver** – một ứng dụng giải đố 8-puzzle sử dụng các thuật toán tìm kiếm khác nhau. Game này hỗ trợ nhiều thuật toán giải quyết bài toán xếp hình, bao gồm:
- **BFS** (Breadth-First Search) 🔍
- **DFS** (Depth-First Search) 🌿
- **UCS** (Uniform Cost Search) 💰
- **Greedy Search** 😈
- **A\*** (A Star) ⭐
- **IDA\*** (Iterative Deepening A Star) 🧑‍💻
- **Hill Climbing** 🧗
- **Simulated Annealing** 🌡️
- **Beam Search** 🌟

Ứng dụng được xây dựng bằng **Python** 🐍 và sử dụng **Pygame** 🎮 để phát triển giao diện đồ họa.

---

## Tính Năng ⚙️
- **Chọn Thuật Toán**: Cung cấp lựa chọn cho người dùng để chọn thuật toán giải quyết bài toán.
- **Chế Độ Chỉnh Sửa**: Cho phép người dùng chỉnh sửa trạng thái ban đầu của puzzle (nhấp vào các ô để thay đổi giá trị).
- **Hiển Thị Tiến Trình**: Thể hiện số bước đi và thanh tiến trình khi thuật toán đang giải quyết bài toán.
- **Hỗ Trợ Nhiều Thuật Toán**: Chạy nhiều thuật toán tìm kiếm với các tiêu chí khác nhau để giải bài toán.
- **Giao Diện Đẹp**: Giao diện trực quan với các hiệu ứng đẹp mắt khi di chuyển các ô trong game.

---

## 📊 So Sánh Hiệu Suất Thuật Toán
```mermaid
graph TD
    title[So Sánh Hiệu Suất Các Thuật Toán 8-Puzzle]
    
    subgraph Chỉ Số
    time[Thời Gian Giải Trung Bình (ms)]
    memory[Sử Dụng Bộ Nhớ (MB)]
    optimal[Tính Tối Ưu (thấp hơn là tốt hơn)]
    steps[Số Bước Trung Bình]
    end
    subgraph Thuật Toán
    bfs[BFS]
    dfs[DFS]
    ucs[UCS]
    greedy[Greedy]
    astar[A*]
    ida[IDA*]
    hill[Hill Climbing]
    annealing[Simulated Annealing]
    beam[Beam Search]
    end
    time --> bfs_time[250]
    memory --> bfs_memory[Cao]
    optimal --> bfs_optimal[100%]
    steps --> bfs_steps[Trung bình]
    time --> dfs_time[150]
    memory --> dfs_memory[Trung bình]
    optimal --> dfs_optimal[Không]
    steps --> dfs_steps[Cao]
    time --> astar_time[180]
    memory --> astar_memory[Trung bình]
    optimal --> astar_optimal[100%]
    steps --> astar_steps[Thấp]
    time --> ida_time[220]
    memory --> ida_memory[Thấp]
    optimal --> ida_optimal[100%]
    steps --> ida_steps[Thấp]


## Cài Đặt và Chạy Game 💻

### Yêu Cầu

- Python 3.x 🐍
- Thư viện **Pygame** (Cài đặt qua `pip`):

```bash
pip install pygame
```

### Cách Tải và Cài Đặt

1. Clone dự án về máy của bạn:

```bash
https://github.com/ThanhSangLouis/Eight_Puzzle_Solver.git
```

2. Chạy ứng dụng:

```bash
python -m eight_puzzle_solver.main
```

---

## Hướng Dẫn Chơi 🎮

1. **Chỉnh Sửa Trạng Thái Ban Đầu**:
   - Nhấp vào các ô để thay đổi giá trị. Ô trống sẽ là số `0`.
   - Bạn có thể nhấp chuột phải để thay đổi giá trị của ô trống từ 8 đến 0.
2. **Chọn Thuật Toán**:

   - Chọn thuật toán từ danh sách để giải bài toán (ví dụ: BFS, A\*, hoặc Simulated Annealing).
   - Sau khi chọn thuật toán, ứng dụng sẽ bắt đầu giải quyết và hiển thị số bước đi và thanh tiến trình.

3. **Reset** 🔄:
   - Bạn có thể nhấn "Reset" để quay lại trạng thái ban đầu của puzzle.
4. **Hiển Thị Tiến Trình** 📊:
   - Số bước đi sẽ được cập nhật trong giao diện khi thuật toán đang chạy.
   - Thanh tiến trình sẽ cho bạn thấy tiến độ giải bài toán.

---

## Cấu Trúc Dự Án 🗂️

- **`main.py`**: Điểm vào của ứng dụng, nơi các sự kiện và logic chính được xử lý.
- **`gui.py`**: Các hàm liên quan đến giao diện người dùng của game.
- **`algorithms.py`**: Chứa các thuật toán giải bài toán 8-puzzle.
- **`utils.py`**: Các hàm hỗ trợ khác như tính toán khoảng cách Manhattan.

---

## Ảnh Minh Họa 🖼️

### Giao Diện Game

![Game_Interface](https://github.com/ThanhSangLouis/Eight_Puzzle_Solver/blob/69e09b1446bb4296cbca4962fa26cefcacfed678/game_interface.png)

### Bảng Xếp Hình

![Puzzle Board](images/puzzle_board.png)

---

## Cảm Ơn 🙏

Cảm ơn bạn đã sử dụng **8-Puzzle Solver**. Chúng tôi hy vọng bạn sẽ thích ứng dụng và thử nghiệm với các thuật toán khác nhau để giải quyết bài toán 8-puzzle!

---

Chúc bạn chơi vui! 🎮
