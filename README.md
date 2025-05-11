<div align="center">
  <img src="https://github.com/user-attachments/assets/ab688f57-deb7-4268-b556-9c1435e86aed" alt="8-Puzzle Solver Logo" width="200"/>
  <h1>8-Puzzle Solver Game 🧩</h1>
  <p>Trò chơi giải đố 8-puzzle với nhiều nhóm thuật toán tìm kiếm AI</p>

  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.x-blue.svg" alt="Python 3.x"></a>
  <a href="https://www.pygame.org/"><img src="https://img.shields.io/badge/pygame-2.x-green.svg" alt="Pygame"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</div>

---

# BÁO CÁO TỔNG KẾT DỰ ÁN

## 1. Mục Tiêu

- Xây dựng trò chơi giải đố 8-puzzle với giao diện trực quan
- Cài đặt và so sánh hiệu suất của các thuật toán tìm kiếm AI khác nhau
- Phân tích ưu nhược điểm của từng thuật toán khi áp dụng vào các trường hợp giải đố cụ thể
- Trực quan hóa quá trình giải quyết bài toán thông qua giao diện đồ họa

## 2. Nội Dung

### 2.1. Nhóm 1: Tìm Kiếm Không Có Thông Tin (Uninformed Search)

#### Thành phần chính của bài toán tìm kiếm:
- **Trạng thái ban đầu**: Cấu hình ban đầu của bảng 8-puzzle
- **Trạng thái đích**: Cấu hình mục tiêu cần đạt được
- **Solution**: Chuỗi các bước di chuyển từ trạng thái ban đầu đến trạng thái đích

#### Các thuật toán tìm kiếm không có thông tin:

##### BFS (Breadth-First Search) 🔍
- **Mô tả**: Duyệt theo từng lớp, mở rộng tất cả các đỉnh ở cùng độ sâu trước khi đi sâu hơn
- **Minh họa**:

![BFS](https://github.com/user-attachments/assets/b89768a5-b798-40ac-b91a-17ab2bd7ba18)

##### DFS (Depth-First Search) 🌿
- **Mô tả**: Đi sâu nhất có thể theo từng nhánh trước khi quay lại
- **Minh họa**:

![DFS](https://github.com/user-attachments/assets/3475f27f-38ab-479c-8ee1-c3398b9a37bc)

##### UCS (Uniform Cost Search) 💰
- **Mô tả**: Luôn chọn mở rộng nút có chi phí thấp nhất
- **Minh họa**:

![UCS](https://github.com/user-attachments/assets/ccd7971c-8a6b-4936-88b2-60b64502d36c)

##### IDDFS (Iterative Deepening Depth-First Search) 🔄
- **Mô tả**: Kết hợp DFS và BFS bằng cách lặp DFS theo từng mức độ sâu tăng dần
- **Minh họa**:

![IDDFS](https://github.com/user-attachments/assets/8d6b945d-7bfe-4848-80d3-ba0763fbacec)

#### So sánh hiệu suất:

| Thuật toán | Thời gian giải (ms) | Bộ nhớ sử dụng | Số bước tối ưu |
|------------|---------------------|----------------|----------------|
| **BFS**    | 250-500             | Cao            | Luôn tối ưu    |
| **DFS**    | 50-100              | Thấp           | Thường không tối ưu |
| **UCS**    | 150-250             | Trung bình     | Luôn tối ưu    |
| **IDDFS**  | 100-200             | Trung bình     | Luôn tối ưu    |

#### Nhận xét:
- **BFS** đảm bảo tìm được đường đi ngắn nhất nhưng tiêu tốn nhiều bộ nhớ khi độ sâu của giải pháp tăng
- **DFS** tiết kiệm bộ nhớ nhưng không đảm bảo tìm được đường đi ngắn nhất và có thể rơi vào vòng lặp vô hạn
- **UCS** tương tự BFS trong bài toán 8-puzzle (vì mỗi bước di chuyển có chi phí bằng nhau), nhưng hiệu quả hơn trong các bài toán có chi phí khác nhau
- **IDDFS** kết hợp ưu điểm của BFS (đảm bảo tìm được đường đi ngắn nhất) và DFS (tiết kiệm bộ nhớ), nhưng có thể tốn thời gian do phải duyệt lại các nút nhiều lần

### 2.2. Nhóm 2: Thuật Toán Tìm Kiếm Có Thông Tin (Informed Search)

#### Thành phần chính của bài toán tìm kiếm:
- **Trạng thái ban đầu**: Cấu hình ban đầu của bảng 8-puzzle
- **Trạng thái đích**: Cấu hình mục tiêu mong muốn
- **Hàm heuristic (h(n))**: Ước lượng chi phí còn lại từ trạng thái hiện tại đến đích
- **Manhattan distance**: Tổng khoảng cách Manhattan từ vị trí hiện tại của mỗi ô đến vị trí đích
- **Solution**: Chuỗi các bước đi từ trạng thái ban đầu đến đích có tổng chi phí thấp nhất

#### Các thuật toán tìm kiếm có thông tin:

##### Greedy Search 😈
- **Mô tả**: Ưu tiên chọn nút gần đích nhất theo hàm heuristic
- **Minh họa**:

![Greedy](https://github.com/user-attachments/assets/0d8ad8f2-050a-43b1-9cb4-1f4408e461b0)

##### A* (A Star) ⭐
- **Mô tả**: Kết hợp giữa chi phí thực tế (g(n)) và chi phí ước lượng đến đích (h(n)) để tìm đường tốt nhất
- **Minh họa**:

![AStar](https://github.com/user-attachments/assets/b775f791-56aa-410d-b07a-d47472143b31)

##### IDA* (Iterative Deepening A Star) 🧑‍💻
- **Mô tả**: Phiên bản tiết kiệm bộ nhớ của A*, thực hiện theo tầng
- **Minh họa**:

![IDAStar](https://github.com/user-attachments/assets/8755251d-c694-4356-94ad-d7e0d6800df7)

#### So sánh hiệu suất:

| Thuật toán     | Thời gian giải (ms) | Bộ nhớ sử dụng | Số bước tối ưu |
|----------------|---------------------|----------------|----------------|
| **Greedy**     | 50-150              | Thấp           | Thường không tối ưu |
| **A***         | 100-200             | Trung bình     | Luôn tối ưu    |
| **IDA***       | 150-300             | Thấp           | Luôn tối ưu    |

#### Nhận xét:
- **Greedy Search** rất nhanh nhưng không đảm bảo tìm được đường đi ngắn nhất
- **A*** kết hợp hiệu quả giữa UCS và Greedy, đảm bảo tìm được đường đi ngắn nhất nếu heuristic admissible
- **IDA*** có hiệu suất bộ nhớ tốt hơn A* nhưng có thể chậm hơn do phải duyệt lại các nút

### 2.3. Nhóm 3: Thuật Toán Tìm Kiếm Cục Bộ (Local Search)

#### Thành phần chính của bài toán tìm kiếm:
- **Trạng thái ban đầu**: Một cấu hình 8-puzzle ban đầu
- **Hàm đánh giá**: Xác định chất lượng của mỗi trạng thái
- **Hàng xóm (neighbors)**: Tập các trạng thái có thể đạt được từ trạng thái hiện tại
- **Solution**: Trạng thái có giá trị đánh giá tốt nhất sau quá trình cải thiện lặp lại

#### Các thuật toán tìm kiếm cục bộ:

##### Hill Climbing 🧗
- **Mô tả**: Luôn di chuyển đến trạng thái tốt hơn nếu có
- **Minh họa**:

![HillClimbing](https://github.com/user-attachments/assets/2e125602-5792-4a00-9746-aef14f7377f3)

##### Steepest-Ascent Hill Climbing 🏔️
- **Mô tả**: Chọn trạng thái tốt nhất trong tất cả hàng xóm
- **Minh họa**:

![SA_HC](https://github.com/user-attachments/assets/0a25e2df-74d7-4f0f-a02a-d698dfead65a)

##### Stochastic Hill Climbing 🎲
- **Mô tả**: Chọn ngẫu nhiên trong các trạng thái tốt hơn
- **Minh họa**:

![Sto_HC](https://github.com/user-attachments/assets/8a9a7152-355c-46ac-aba3-bc0e84f1cf4a)

##### Simulated Annealing ❄️
- **Mô tả**: Chấp nhận trạng thái tệ hơn để thoát khỏi cực trị cục bộ
- **Minh họa**:

![Simu](https://github.com/user-attachments/assets/ab7ed3c6-0ed9-47c2-8338-744e802b26f6)

##### Genetic Algorithm 🧬
- **Mô tả**: Sử dụng các nguyên tắc di truyền để tiến hóa dần đến giải pháp tốt
- **Minh họa**:

![Genetic](https://github.com/user-attachments/assets/cbbe1f4d-d54d-4482-bb7a-b8d2b65ef191)

##### Beam Search 🌟
- **Mô tả**: Duy trì K trạng thái tốt nhất tại mỗi cấp độ
- **Minh họa**:

![Beam](https://github.com/user-attachments/assets/6efa88a7-c770-4ac0-af47-d45d716da5ae)

#### So sánh hiệu suất:

| Thuật toán                | Thời gian giải (ms) | Bộ nhớ sử dụng | Khả năng tìm lời giải |
|---------------------------|---------------------|----------------|------------------------|
| **Hill Climbing**         | 30-50               | Rất thấp       | Có thể bị kẹt          |
| **Steepest-Ascent HC**    | 30-50               | Rất thấp       | Có thể bị kẹt          |
| **Stochastic HC**         | 40-60               | Rất thấp       | Có thể bị kẹt          |
| **Simulated Annealing**   | 100-150             | Rất thấp       | Thường gần tối ưu      |
| **Genetic Algorithm**     | 200-350             | Trung bình     | Có thể tìm ra giải pháp tốt |
| **Beam Search**| 100-250             | Trung bình     | Tìm được giải pháp tốt nhất |

#### Nhận xét:
- Các thuật toán **Hill Climbing** rất nhanh và ít tốn bộ nhớ, nhưng dễ bị kẹt ở cực trị cục bộ
- **Simulated Annealing** giải quyết được vấn đề kẹt ở cực trị cục bộ nhưng có thể mất nhiều thời gian hơn
- **Genetic Algorithm** đa dạng trong việc tìm kiếm không gian trạng thái nhưng phức tạp hơn và tốn thời gian
- **Beam Search** cho tốc độ tốt nhưng không đảm bảo tìm được đường đi tối ưu nếu beam_width quá nhỏ
  
### 2.4. Nhóm 4: Thuật Toán Tìm Kiếm Trong Môi Trường Phức Tạp

#### Thành phần chính của bài toán tìm kiếm:
- **Trạng thái ban đầu**: Có thể là một tập hợp trạng thái (belief state)
- **Hành động**: Có thể mang tính bất định, không dẫn tới một kết quả duy nhất
- **Quan sát**: Thông tin gián tiếp giúp điều chỉnh belief state
- **Solution**: Một kế hoạch hoặc cây hành động thỏa mãn mục tiêu bất chấp thiếu quan sát đầy đủ

##### And-Or Search 🤝
- **Mô tả**: Phù hợp cho bài toán có nhiều khả năng lựa chọn và rẽ nhánh
- **Minh họa**:

![AndORFIX](https://github.com/user-attachments/assets/5df70f82-15ca-497e-99bf-6d1a3fc2e281)

##### No Observation Search 👁️‍🗨️
- **Mô tả**: Giải trong điều kiện không biết rõ trạng thái ban đầu
- **Minh họa**:

![NoObser](https://github.com/user-attachments/assets/6605b443-8229-4293-85a0-b86b506e089a)

##### Partial Observable Search 🕵️
- **Mô tả**: Xử lý bài toán khi chỉ biết một phần trạng thái môi trường
- **Minh họa**:

![Partial](https://github.com/user-attachments/assets/5996b2f8-14e6-4219-bccb-30c867c258b9)

#### So sánh hiệu suất:

| Thuật toán             | Thời gian giải (ms) | Bộ nhớ sử dụng | Đặc điểm |
|------------------------|---------------------|----------------|----------|
| **And-Or Search**      | 300-500             | Cao            | Tìm giải pháp tối ưu trong cây AND-OR |
| **No Observation**     | 200-400             | Thấp           | Đưa ra kết quả chính xác trong điều kiện không quan sát |
| **Partial Observable** | 150-300             | Trung bình     | Đưa ra kết quả với thông tin quan sát một phần |

#### Nhận xét:
- **And-Or Search** hiệu quả cho các bài toán có nhiều khả năng lựa chọn nhưng tốn nhiều bộ nhớ
- **No Observation** và **Partial Observable** giải quyết được các bài toán với thông tin không đầy đủ
- **Partial Observable** đặc biệt hữu ích trong môi trường mà người giải không thể biết chính xác trạng thái hiện tại, buộc phải dựa vào tập hợp các trạng thái khả thi (belief state) để ra quyết định

### 2.5. Nhóm 5: Thuật Toán Tìm Kiếm Trong Môi Trường Có Ràng Buộc (CSP)

#### Thành phần chính của bài toán tìm kiếm:
- **Biến (variables)**: Các thành phần cần được gán giá trị
- **Miền giá trị (domains)**: Tập hợp các giá trị có thể gán cho biến
- **Ràng buộc (constraints)**: Các điều kiện cần thỏa mãn giữa các biến
- **Solution**: Một phép gán giá trị cho tất cả các biến sao cho thỏa mãn toàn bộ ràng buộc

##### Backtracking 🔙
- **Mô tả**: Tìm kiếm bằng cách thử và quay lại khi rơi vào ngõ cụt
- **Minh họa**:

![Backing](https://github.com/user-attachments/assets/abc81e2d-a3d9-4818-809f-a88eb5673ed2)

##### AC3 (Arc Consistency Algorithm #3) 🔄
- **Mô tả**: Thuật toán kiểm tra tính nhất quán giữa các ràng buộc
- **Minh họa**:

![ac3](https://github.com/user-attachments/assets/0f3f8569-2966-415c-a2f3-8bcb827e6976)

##### Constraint Checking ✅
- **Mô tả**: Kiểm tra các ràng buộc trong quá trình tìm kiếm
- **Minh họa**:

![Const_Checking](https://github.com/user-attachments/assets/bf6f4086-583b-45ab-8a3c-1c1ba08a47a6)

#### So sánh hiệu suất:

| Thuật toán             | Thời gian giải (ms) | Bộ nhớ sử dụng | Đặc điểm |
|------------------------|---------------------|----------------|----------|
| **Backtracking**       | 50-150              | Thấp           | Tìm tất cả các giải pháp khả thi |
| **AC3**                | 100-200             | Trung bình     | Cải thiện hiệu suất tìm kiếm bằng cách loại bỏ giá trị không hợp lệ |
| **Constraint Checking**| 80-150              | Thấp           | Kiểm tra tính hợp lệ của các trạng thái |

#### Nhận xét:
- **Backtracking** đơn giản và hiệu quả cho các bài toán nhỏ, nhưng có thể chậm với không gian trạng thái lớn
- **AC3** và **Constraint Checking** cải thiện hiệu suất tìm kiếm bằng cách loại bỏ sớm các giá trị không hợp lệ

### 2.6. Nhóm 6: Thuật Toán Học Tăng Cường (Reinforcement Learning)

#### Thành phần chính của bài toán tìm kiếm:
- **Trạng thái (state)**: Cấu hình hiện tại của môi trường (bảng 8-puzzle)
- **Hành động (action)**: Các nước đi mà agent có thể thực hiện
- **Phần thưởng (reward)**: Giá trị phản hồi từ môi trường sau mỗi hành động áp dụng lên trạng thái
- **Chính sách (policy)**: Quy tắc chọn hành động dựa trên trạng thái
- **Solution**: Một chuỗi hành động tối ưu được học thông qua tương tác với môi trường

##### Q-Learning 🧠
- **Mô tả**: Thuật toán học tăng cường để tìm chiến lược tối ưu
- **Minh họa**:

![Q_Learning](https://github.com/user-attachments/assets/d0596a0e-3ac9-4119-8718-c3d201369d4d)

#### So sánh hiệu suất:

| Thuật toán             | Thời gian giải (ms) | Bộ nhớ sử dụng | Đặc điểm |
|------------------------|---------------------|----------------|----------|
| **Q-Learning**         | 1000ms - vài giây             | Cao            | Học dần dần chiến lược tối ưu |

#### Nhận xét:
- **Q-Learning** có khả năng học và cải thiện hiệu suất theo thời gian, nhưng đòi hỏi nhiều tài nguyên

## 3. Kết Luận

### Kết quả đạt được

- Triển khai thành công 20 thuật toán tìm kiếm, bao gồm đầy đủ 6 nhóm: từ tìm kiếm không có thông tin, có thông tin, cục bộ, cho đến học tăng cường và môi trường ràng buộc phức tạp.
- Xây dựng một giao diện trực quan và dễ sử dụng bằng Pygame, giúp người dùng theo dõi trực tiếp quá trình giải quyết bài toán theo từng bước.
- Tổ chức lại toàn bộ nội dung thuật toán theo nhóm, kết hợp minh hoạ hình ảnh và bảng hiệu suất để trực quan và dễ tiếp cận.
- Phân tích chi tiết điểm mạnh và hạn chế của từng thuật toán khi áp dụng cụ thể vào trò chơi 8-puzzle.

### Nhận xét tổng quát

- Các thuật toán tìm kiếm **không có thông tin** (BFS, DFS, UCS, IDDFS) phù hợp với bài toán nhỏ, ổn định nhưng dễ bị giới hạn bởi bộ nhớ hoặc thời gian trong các bài toán lớn hơn.
- Nhóm thuật toán tìm kiếm **có thông tin** (A*, IDA*, Greedy) mang lại hiệu quả vượt trội nhờ tận dụng heuristic, đặc biệt A* cho kết quả tối ưu một cách đáng tin cậy.
- **Local Search** cho thấy ưu thế về tốc độ và tiết kiệm bộ nhớ, tuy nhiên dễ bị rơi vào trạng thái cục bộ, trừ khi áp dụng các kỹ thuật như Simulated Annealing hoặc Genetic Algorithm.
- Nhóm thuật toán tìm kiếm trong **môi trường phức tạp** như And-Or Search, Partial Observable, No Observation thể hiện khả năng thích nghi cao trong điều kiện thiếu thông tin hoặc không chắc chắn.
- Các thuật toán tìm kiếm có **ràng buộc (CSP)** như Backtracking, AC3, Constraint Checking giúp nhanh chóng loại bỏ trạng thái không hợp lệ và làm nền tảng cho sinh lời giải ban đầu.
- Thuật toán học tăng cường **Q-Learning** mang lại một góc nhìn khác khi bài toán được học thông qua tương tác thay vì duyệt toàn bộ không gian trạng thái.

### Hướng phát triển

- Cải thiện tốc độ và bộ nhớ thông qua tối ưu thuật toán và cấu trúc dữ liệu.
- Bổ sung các loại heuristic khác và cho phép người dùng tùy chọn trong giao diện.
- Mở rộng trò chơi sang phiên bản lớn hơn như 15-puzzle hoặc 24-puzzle.
- Tích hợp hệ thống giải thích trực quan từng bước tìm kiếm cho mục đích học tập và trình bày.
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
   - Nhấp vào các ô hoặc cuộn con lăn chuột để thay đổi giá trị. Ô trống sẽ là số `0`.
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

Cảm ơn bạn đã sử dụng game **8-Puzzle Solver**. Chúng tôi hy vọng bạn sẽ thích ứng dụng và thử nghiệm với các thuật toán khác nhau để giải quyết bài toán 8-puzzle!
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
