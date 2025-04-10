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

## 🧠 Các Thuật Toán Hỗ Trợ

| Thuật Toán | Loại | Mô Tả |
|------------|------|-------|
| **BFS** | Không định hướng | Tìm kiếm theo chiều rộng khám phá tất cả các nút ở độ sâu hiện tại trước khi chuyển sang độ sâu tiếp theo |
| **DFS** | Không định hướng | Tìm kiếm theo chiều sâu khám phá càng xa càng tốt theo mỗi nhánh trước khi quay lui |
| **UCS** | Không định hướng | Tìm kiếm chi phí đồng nhất mở rộng nút có chi phí đường đi thấp nhất |
| **Greedy** | Có định hướng | Tìm kiếm tham lam luôn chọn đường đi tốt nhất tại thời điểm hiện tại |
| **A*** | Có định hướng | A* kết hợp ưu điểm của UCS và Greedy bằng cách sử dụng cả chi phí đường đi và heuristic |
| **IDA*** | Có định hướng | Lặp sâu A* kết hợp tìm kiếm theo chiều sâu lặp với A* để tìm giải pháp tối ưu với bộ nhớ thấp hơn |
| **Hill Climbing** | Cục bộ | Thuật toán leo đồi luôn di chuyển theo hướng tăng giá trị để đạt cực đại cục bộ |
| **Simulated Annealing** | Cục bộ | Mô phỏng luyện kim đôi khi chấp nhận giải pháp tệ hơn để thoát khỏi cực đại cục bộ |
| **Beam Search** | Bộ nhớ giới hạn | Tìm kiếm chùm giới hạn độ rộng của cây tìm kiếm để tiết kiệm bộ nhớ nhưng vẫn đảm bảo chất lượng giải pháp |

---

## Tính Năng ⚙️
- **Chọn Thuật Toán**: Cung cấp lựa chọn cho người dùng để chọn thuật toán giải quyết bài toán.
- **Chế Độ Chỉnh Sửa**: Cho phép người dùng chỉnh sửa trạng thái ban đầu của puzzle (nhấp vào các ô để thay đổi giá trị).
- **Hiển Thị Tiến Trình**: Thể hiện số bước đi và thanh tiến trình khi thuật toán đang giải quyết bài toán.
- **Hỗ Trợ Nhiều Thuật Toán**: Chạy nhiều thuật toán tìm kiếm với các tiêu chí khác nhau để giải bài toán.
- **Giao Diện Đẹp**: Giao diện trực quan với các hiệu ứng đẹp mắt khi di chuyển các ô trong game.

---

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
