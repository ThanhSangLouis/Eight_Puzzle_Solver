# 8-Puzzle Solver Game 🎮

## Giới Thiệu
Chào mừng đến với **8-Puzzle Solver** – một ứng dụng giải đố trò chơi 8-puzzle sử dụng các thuật toán tìm kiếm khác nhau. Game này hỗ trợ nhiều thuật toán giải quyết bài toán xếp hình, bao gồm:
- **BFS** (Breadth-First Search) 🔍
- **DFS** (Depth-First Search) 🌿
- **UCS** (Uniform Cost Search) 💰
- **Greedy Search** 😈
- **A\*** (A Star) ⭐
- **IDA\*** (Iterative Deepening A Star) 🧑‍💻
- **Hill Climbing** 🧗
- **Simulated Annealing** 🌡️
- **Beam Search** 🌟
- **And-Or Search** 🔀
- **No Observation Search** ❓
- **Partial Observable Search** 🔍

Ứng dụng được xây dựng bằng **Python** 🐍 và sử dụng **Pygame** 🎮 để phát triển giao diện đồ họa.

---

## 🧠 Các Thuật Toán Hỗ Trợ

| Thuật toán | Phân loại | Mô tả |
|------------|-----------|-------|
| **BFS** | Không định hướng | Khám phá tất cả các nút ở cùng độ sâu trước khi đi sâu hơn |
| **DFS** | Không định hướng | Đi sâu nhất có thể theo một nhánh trước khi quay lui |
| **UCS** | Không định hướng | Mở rộng nút có chi phí đường đi thấp nhất |
| **Greedy** | Có định hướng | Dựa vào heuristic để đánh giá nút tốt nhất tại thời điểm hiện tại |
| **A\*** | Có định hướng | Kết hợp chi phí thực tế và heuristic để tìm đường đi tối ưu |
| **IDA\*** | Có định hướng | Kết hợp tìm kiếm sâu dần với A* để tiết kiệm bộ nhớ |
| **Hill Climbing** | Cục bộ | Di chuyển theo hướng cải thiện giá trị để tìm cực đại cục bộ |
| **Steepest-Ascent HC** | Cục bộ | Chọn nước đi với mức cải thiện lớn nhất |
| **Stochastic HC** | Cục bộ | Chọn ngẫu nhiên trong các nước đi cải thiện |
| **Simulated Annealing** | Cục bộ | Chấp nhận các giải pháp kém hơn với xác suất nhất định để thoát khỏi cực đại cục bộ |
| **Beam Search** | Bộ nhớ giới hạn | Giữ k trạng thái tốt nhất ở mỗi độ sâu |
| **And-Or Search** | Cây AND-OR | Giải quyết bài toán thông qua cây AND-OR |
| **No Observation** | Không quan sát | Tìm kiếm không có thông tin quan sát |
| **Partial Observable** | Quan sát một phần | Tìm kiếm với thông tin được quan sát một phần |
| **Backtracking** | Quay lui | Thử các khả năng cho đến khi tìm được giải pháp hoặc hết khả năng |

---
## 📊 So sánh hiệu suất thuật toán

Với bảng 8-puzzle phức tạp (cần 20+ bước để giải):

| Thuật toán | Thời gian giải (ms) | Bộ nhớ sử dụng | Số bước tối ưu |
|------------|---------------------|----------------|---------------|
| BFS        | 250-500             | Cao            | Luôn tối ưu   |
| DFS        | 50-100              | Thấp           | Thường không tối ưu |
| A*         | 100-200             | Trung bình     | Luôn tối ưu   |
| IDA*       | 150-300             | Thấp           | Luôn tối ưu   |
| Hill Climbing | 30-50            | Rất thấp       | Có thể bị kẹt |
| Simulated Annealing | 100-150    | Rất thấp       | Thường gần tối ưu |

## Tính Năng ⚙️
- **Chọn Thuật Toán**: Cung cấp lựa chọn cho người dùng để chọn thuật toán giải quyết bài toán.
- **Chế Độ Chỉnh Sửa**: Cho phép người dùng chỉnh sửa trạng thái ban đầu của puzzle (hoặc nhấp vào các ô hoặc cuộn con lăn chuột để thay đổi giá trị).
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

## 🧩 Cấu trúc dự án

```
Eight_Puzzle_Solver/
├── eight_puzzle_solver/
│   ├── __init__.py
│   ├── main.py          # Điểm vào chính của ứng dụng
│   ├── gui.py           # Xử lý giao diện đồ họa
│   ├── algorithms.py    # Các thuật toán giải 8-puzzle
│   └── utils.py         # Các hàm tiện ích
├── assets/              # Hình ảnh, âm thanh và tài nguyên
├── tests/               # Unit tests
├── requirements.txt     # Các thư viện phụ thuộc
└── README.md            # Tài liệu dự án
```
---
## Minh hoạ các thuật toán

### Enter input board with BFS Algorithm

![Use_with_BFS](https://github.com/user-attachments/assets/b89768a5-b798-40ac-b91a-17ab2bd7ba18)

### DFS

![DFS](https://github.com/user-attachments/assets/3475f27f-38ab-479c-8ee1-c3398b9a37bc)

### UCS

![UCS](https://github.com/user-attachments/assets/ccd7971c-8a6b-4936-88b2-60b64502d36c)

### Greedy

![Greedy](https://github.com/user-attachments/assets/0d8ad8f2-050a-43b1-9cb4-1f4408e461b0)

### IDDFS

![IDDFS](https://github.com/user-attachments/assets/8d6b945d-7bfe-4848-80d3-ba0763fbacec)

### A*
![AStar](https://github.com/user-attachments/assets/b775f791-56aa-410d-b07a-d47472143b31)

### IDA*

![IDAStar](https://github.com/user-attachments/assets/8755251d-c694-4356-94ad-d7e0d6800df7)

### Hill Climbing

![HillClimbing](https://github.com/user-attachments/assets/2e125602-5792-4a00-9746-aef14f7377f3)

### Steepest-Ascent Hill Climbing
![SA_HC](https://github.com/user-attachments/assets/0a25e2df-74d7-4f0f-a02a-d698dfead65a)

### Stochastic hill climbing

![Sto_HC](https://github.com/user-attachments/assets/8a9a7152-355c-46ac-aba3-bc0e84f1cf4a)

### Test Algorithm

![TestAlgo](https://github.com/user-attachments/assets/59f4023d-ad81-4943-b34f-ac5fa6113181)

### Backtracking

![BackTracking](https://github.com/user-attachments/assets/c3ed0468-49d1-4a95-aad8-00525e484e0a)


---
## Ảnh Minh Họa 🖼️

### Giao Diện Game

![Game_Interface](https://github.com/ThanhSangLouis/Eight_Puzzle_Solver/blob/69e09b1446bb4296cbca4962fa26cefcacfed678/game_interface.png)

---
## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh! Nếu bạn muốn đóng góp, vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/amazing-feature`)
3. Commit thay đổi (`git commit -m 'Add some amazing feature'`)
4. Push lên branch (`git push origin feature/amazing-feature`)
5. Mở Pull Request

## 📞 Liên hệ

Thanh Sang - [@ThanhSangLouis](https://github.com/ThanhSangLouis)

Project Link: [https://github.com/ThanhSangLouis/Eight_Puzzle_Solver](https://github.com/ThanhSangLouis/Eight_Puzzle_Solver)

---
## Cảm Ơn 🙏

Cảm ơn bạn đã sử dụng **8-Puzzle Solver**. Chúng tôi hy vọng bạn sẽ thích ứng dụng và thử nghiệm với các thuật toán khác nhau để giải quyết bài toán 8-puzzle!

---

Chúc bạn chơi vui nhé! 🎮
