<div align="center">
  <img src="https://github.com/user-attachments/assets/ab688f57-deb7-4268-b556-9c1435e86aed" alt="8-Puzzle Solver Logo" width="200"/>
  <h1>8-Puzzle Solver Game 🧩</h1>
  <p>Ứng dụng giải đố 8-puzzle với nhiều thuật toán AI</p>

  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.x-blue.svg" alt="Python 3.x"></a>
  <a href="https://www.pygame.org/"><img src="https://img.shields.io/badge/pygame-2.x-green.svg" alt="Pygame"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</div>

---

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
- **Partial Observable**
- **Test Algorithm** 🧪
- **Backtracking** 🔄

Ứng dụng được xây dựng bằng **Python** 🐍 và sử dụng **Pygame** 🎮 để phát triển giao diện đồ họa.

## 🧠 Các Thuật Toán Hỗ Trợ

| Thuật toán              | Phân loại         | Mô tả                                                                               |
|-------------------------|-------------------|-------------------------------------------------------------------------------------|
| **BFS**                 | Không định hướng  | Khám phá tất cả các nút ở cùng độ sâu trước khi đi sâu hơn                          |
| **DFS**                 | Không định hướng  | Đi sâu nhất có thể theo một nhánh trước khi quay lui                                |
| **UCS**                 | Không định hướng  | Mở rộng nút có chi phí đường đi thấp nhất                                           |
| **Greedy**              | Có định hướng     | Dựa vào heuristic để đánh giá nút tốt nhất tại thời điểm hiện tại                   |
| **IDDFS**               | Có định hướng     | Tìm kiếm chiều sâu với giới hạn độ sâu tăng dần, tránh việc lặp lại trạng thái      |
| **A\***                 | Có định hướng     | Kết hợp chi phí thực tế và heuristic để tìm đường đi tối ưu                         |
| **IDA\***               | Có định hướng     | Kết hợp tìm kiếm sâu dần với A* để tiết kiệm bộ nhớ                                 |
| **Hill Climbing**       | Cục bộ            | Di chuyển theo hướng cải thiện giá trị để tìm cực đại cục bộ                        |
| **Steepest-Ascent HC**  | Cục bộ            | Chọn nước đi với mức cải thiện tốt nhất                                             |
| **Stochastic HC**       | Cục bộ            | Chọn ngẫu nhiên trong các nước đi cải thiện                                         |
| **Simulated Annealing** | Cục bộ            | Chấp nhận các giải pháp kém hơn với xác suất nhất định để thoát khỏi cực đại cục bộ |
| **Beam Search**         | Bộ nhớ giới hạn   | Giữ k trạng thái tốt nhất ở mỗi độ sâu                                              |
| **And-Or Search**       | Cây AND-OR        | Giải quyết bài toán thông qua cây AND-OR                                            |
| **No Observation**      | Không quan sát    | Tìm kiếm không có thông tin quan sát                                                |
| **Partial Observable**  | Quan sát một phần | Tìm kiếm với thông tin được quan sát một phần                                       |
| **Test Algorithm**      | Kiểm tra          | Thuật toán thử nghiệm các nước đi có giảm heuristic thì chọn đi                     |
| **Backtracking**        | Quay lui          | Thử các khả năng cho đến khi tìm được giải pháp hoặc hết khả năng                   |

---

## 📊 So sánh hiệu suất thuật toán

Với bảng 8-puzzle phức tạp (cần 20+ bước để giải):

| Thuật toán               | Thời gian giải (ms) | Bộ nhớ sử dụng | Số bước tối ưu                                          |
|--------------------------|---------------------|----------------|---------------------------------------------------------|
| **BFS**                  | 250-500             | Cao            | Luôn tối ưu                                             |
| **DFS**                  | 50-100              | Thấp           | Thường không tối ưu                                     |
| **UCS**                  | 150-250             | Trung bình     | Luôn tối ưu                                             |
| **Greedy**               | 50-150              | Thấp           | Thường không tối ưu                                     |
| **IDDFS**                | 100-200             | Trung bình     | Luôn tối ưu                                             |
| **A\***                  | 100-200             | Trung bình     | Luôn tối ưu                                             |
| **IDA\***                | 150-300             | Thấp           | Luôn tối ưu                                             |
| **Hill Climbing**        | 30-50               | Rất thấp       | Có thể bị kẹt                                           |
| **Steepest-Ascent HC**   | 30-50               | Rất thấp       | Có thể bị kẹt                                           |
| **Stochastic HC**        | 40-60               | Rất thấp       | Có thể bị kẹt                                           |
| **Simulated Annealing**  | 100-150             | Rất thấp       | Thường gần tối ưu                                       |
| **Beam Search**          | 100-250             | Trung bình     | Tìm được giải pháp tốt nhất                             |
| **And-Or Search**        | 300-500             | Cao            | Tìm giải pháp tối ưu trong cây AND-OR                   |
| **No Observation**       | 200-400             | Thấp           | Đưa ra kết quả chính xác trong điều kiện không quan sát |
| **Partial Observable**   | 150-300             | Trung bình     | Đưa ra kết quả với thông tin quan sát một phần          |
| **Test Algorithm**       | 50-100              | Thấp           | Có thể tìm giải pháp với các bước giảm heuristic        |
| **Backtracking**         | 50-150              | Thấp           | Tìm tất cả các giải pháp khả thi                        |

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
├── images/              # Hình ảnh
└── README.md            # Tài liệu dự án
```
---
## 🌟 Minh hoạ các thuật toán tìm kiếm

> 🧠 Các hình ảnh trực quan mô phỏng cách hoạt động của các thuật toán trong việc giải bài toán 8-Puzzle.

---

### 🔍 **BFS – Tìm kiếm theo chiều rộng**  
📚 Duyệt theo từng lớp, mở rộng tất cả các đỉnh ở cùng độ sâu trước khi đi sâu hơn.  
![BFS](https://github.com/user-attachments/assets/b89768a5-b798-40ac-b91a-17ab2bd7ba18)

---

### 🧭 **DFS – Tìm kiếm theo chiều sâu**  
🌊 Đi sâu nhất có thể theo từng nhánh trước khi quay lại.  
![DFS](https://github.com/user-attachments/assets/3475f27f-38ab-479c-8ee1-c3398b9a37bc)

---

### 💰 **UCS – Tìm kiếm theo chi phí đồng đều**  
📈 Luôn chọn mở rộng nút có chi phí thấp nhất.  
![UCS](https://github.com/user-attachments/assets/ccd7971c-8a6b-4936-88b2-60b64502d36c)

---

### 🎯 **Greedy – Tìm kiếm tham lam**  
🚀 Ưu tiên chọn nút gần đích nhất theo hàm heuristic.  
![Greedy](https://github.com/user-attachments/assets/0d8ad8f2-050a-43b1-9cb4-1f4408e461b0)

---

### 🔁 **IDDFS – Tìm kiếm chiều sâu lặp lại**  
🔄 Kết hợp DFS và BFS bằng cách lặp DFS theo từng mức độ sâu tăng dần.  
![IDDFS](https://github.com/user-attachments/assets/8d6b945d-7bfe-4848-80d3-ba0763fbacec)

---

### 🌟 **A\* – Tìm kiếm A sao**  
🧮 Kết hợp giữa chi phí thực tế và ước lượng đến đích để tìm đường tốt nhất.  
![AStar](https://github.com/user-attachments/assets/b775f791-56aa-410d-b07a-d47472143b31)

---

### 💫 **IDA\* – Tìm kiếm A sao lặp lại**  
⏳ Phiên bản tiết kiệm bộ nhớ của A\*, thực hiện theo tầng.  
![IDAStar](https://github.com/user-attachments/assets/8755251d-c694-4356-94ad-d7e0d6800df7)

---

### 🧗 **Hill Climbing – Leo đồi**  
📈 Luôn di chuyển đến trạng thái tốt hơn nếu có.  
![HillClimbing](https://github.com/user-attachments/assets/2e125602-5792-4a00-9746-aef14f7377f3)

---

### 🏔️ **Steepest-Ascent Hill Climbing**  
🔝 Chọn trạng thái tốt nhất trong tất cả hàng xóm.  
![SA_HC](https://github.com/user-attachments/assets/0a25e2df-74d7-4f0f-a02a-d698dfead65a)

---

### 🎲 **Stochastic Hill Climbing**  
🎰 Chọn ngẫu nhiên trong các trạng thái tốt hơn.  
![Sto_HC](https://github.com/user-attachments/assets/8a9a7152-355c-46ac-aba3-bc0e84f1cf4a)

---

### ❄️ **Simulated Annealing – Tìm kiếm tôi luyện**  
🔥 Chấp nhận trạng thái tệ hơn để thoát khỏi cực trị cục bộ.  
![Simu](https://github.com/user-attachments/assets/ab7ed3c6-0ed9-47c2-8338-744e802b26f6)

---

### 🌬️ **Beam Search – Tia sáng**  
🪞 Duy trì K trạng thái tốt nhất tại mỗi cấp độ.  
![Beam](https://github.com/user-attachments/assets/6efa88a7-c770-4ac0-af47-d45d716da5ae)

### **Genetic**
![Genetic](https://github.com/user-attachments/assets/cbbe1f4d-d54d-4482-bb7a-b8d2b65ef191)

---

### 🤝 **And-Or Search**  
🔀 Phù hợp cho bài toán có nhiều khả năng lựa chọn và rẽ nhánh.  
![AndORFIX](https://github.com/user-attachments/assets/5df70f82-15ca-497e-99bf-6d1a3fc2e281)


---

### 👁️‍🗨️ **No Observation – Không quan sát**  
🙈 Giải trong điều kiện không biết rõ trạng thái ban đầu.  
![NoObser](https://github.com/user-attachments/assets/6605b443-8229-4293-85a0-b86b506e089a)

---

### 🕵️ **Partial Observable – Quan sát không đầy đủ**  
🧩 Xử lý bài toán khi chỉ biết một phần trạng thái môi trường.  
![Partial](https://github.com/user-attachments/assets/5996b2f8-14e6-4219-bccb-30c867c258b9)

---

### 🔙 **Backtracking – Quay lui** ❤️ **ADVANCED ALGORITHM**
🔁 Tìm kiếm bằng cách thử và quay lại khi rơi vào ngõ cụt.  
![Backing](https://github.com/user-attachments/assets/abc81e2d-a3d9-4818-809f-a88eb5673ed2)

### AC3
![ac3](https://github.com/user-attachments/assets/0f3f8569-2966-415c-a2f3-8bcb827e6976)

### **Constraint Checking - Kiểm thử**
![Const_Checking](https://github.com/user-attachments/assets/bf6f4086-583b-45ab-8a3c-1c1ba08a47a6)

### **Q-Learning**
![Q_Learning](https://github.com/user-attachments/assets/d0596a0e-3ac9-4119-8718-c3d201369d4d)


---
## Ảnh Minh Họa 🖼️

### Giao Diện Game

![GameInterface](https://github.com/user-attachments/assets/b8045e20-910b-4c29-9b21-37a7b4316aee)

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
Chúc bạn chơi vui nhé! 🎮

---
<div align="center">
  <p>
    <sub>Built with ❤️ by Thanh Sang</sub>
  </p>
  <p>
    <a href="https://github.com/ThanhSangLouis/Eight_Puzzle_Solver/stargazers">
      <img src="https://img.shields.io/github/stars/ThanhSangLouis/Eight_Puzzle_Solver?style=social" alt="Stars"/>
    </a>
    <a href="https://github.com/ThanhSangLouis/Eight_Puzzle_Solver/network/members">
      <img src="https://img.shields.io/github/forks/ThanhSangLouis/Eight_Puzzle_Solver?style=social" alt="Forks"/>
    </a>
  </p>
  <p>
    <a href="#top">⬆️ Về đầu trang</a>
  </p>
</div>
---

