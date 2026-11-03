# Nguồn soạn web ôn thi (index.html)

Web là một file tự chứa: `../index.html` (và bản sao `../../index.html`). Thư mục này chỉ để sửa nội dung rồi build lại.

- `shell.html`: khung HTML/CSS/JS (menu, trang ôn, quiz, lưu tiến độ).
- `c_k1.py` … `c_k9.py`, `c_c1.py` … `c_c4.py`: nội dung trang ôn + câu hỏi từng khối (`Q(...)`: đáp án đúng ghi bằng chữ cái, ví dụ `"abd"`).
- `c_cards.py`: flashcard · `c_meta.py`: lịch ôn, danh sách chế độ.
- `tools_calc.js`: bài tính MMT sinh số ngẫu nhiên · `tools_p3.js`: flashcard, thi thử, sổ lỗi, tiến độ.

Build (kiểm tra dữ liệu rồi ghi đè cả hai bản index.html):

```bash
python3 build.py
```
