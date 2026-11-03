# Prompt: Xây web ôn thi giữa kỳ Nền tảng TTNT + Mạng máy tính

> Dùng với Claude Opus 5 (hoặc Claude Code), effort `high`. Mở phiên có quyền truy cập thư mục `NenTangTTNT + MMT` và artifact kế hoạch. Dán toàn bộ phần dưới đây vào lượt đầu tiên.

---

Bạn là người soạn tài liệu ôn thi và là frontend developer. Nhiệm vụ: xây một website ôn tập **đơn giản, dễ dùng, làm nhanh** cho sinh viên PTIT (năm 2, ngành AI) chuẩn bị thi giữa kỳ hai môn. Người dùng sẽ học trên web này **ngay tối nay**, nên tốc độ ra bản dùng được quan trọng hơn tính năng phụ.

<context>
<exam_dates>
- Hôm nay: thứ Ba 3/11/2026.
- Nền tảng TTNT: thi thứ Sáu 6/11 (còn 3 ngày). Đây là môn gấp nhất.
- Mạng máy tính (MMT): thi thứ Tư 11/11.
</exam_dates>

<plan_artifact>
Kế hoạch đã chốt nằm ở artifact: https://claude.ai/artifact/WkYxxkbQLq6u8P56uz6JFP
Đọc toàn bộ artifact trước khi làm. Bám sát các phần: Tổng quan (phạm vi, format đề), checklist K1–K9 và C1–C4, bảng bài tính MMT, Kế hoạch làm web (7 chế độ, ngân hàng câu hỏi, thứ tự xây), Lịch ôn. Nếu tài liệu môn học có nội dung quan trọng mà checklist bỏ sót, thêm vào web và ghi chú lại; không bỏ mục nào trong checklist.
</plan_artifact>

<source_materials>
Thư mục `NenTangTTNT + MMT`:

Nền tảng TTNT (phạm vi giữa kỳ = toàn bộ):
- `slides/week01.pdf` Git cơ bản · `slides/week02.pdf` branch/merge/rebase · `slides/week3.pdf` Linux, quyền, SSH · `slides/week4.pdf` FastAPI, .env, PostgreSQL · `slides/fastapi_llm.pdf` HTTP, REST, FastAPI + Gemini · `slides/week5.pdf` Docker · `slides/CI.pdf` GitHub Actions, pytest · `slides/cloudcomputing.pdf` EC2, Security Group · `slides/CD.pdf` CD, Secrets, registry, ssh-action · `slides/reverse_proxy_https.pdf` Caddy, HTTPS
- `exercises/ex1–ex3.docx`, `project.docx`, `Topics and grading.docx`
- `materials/llm_app/` (code mẫu app FastAPI chạy thật, lấy ví dụ code từ đây)
- Ba sách tham khảo, **bắt buộc đọc**: `materials/progit.pdf` (501 trang), `materials/linux.pdf` (597 trang), `materials/Docker Deep Dive.pdf` (191 trang). Slide được soạn từ các sách này, nên sách là nguồn để giải thích sâu hơn, lấy ví dụ và bắt những chi tiết dễ ra đề mà slide chỉ nhắc qua
- Đề mẫu `Demo_MidTerm_questions.md` (20 câu, đã đính kèm trong hội thoại)

MMT (phạm vi = chương 1–4, Kurose & Ross bản 8):
- `chuong 1 v2.pdf`, `chuong 2 v1.pdf`, `chuong 3 Tang giao van.pdf`, `chuong 4 v1.pdf`

Không mở `test.pem` (khóa riêng tư, không liên quan).
</source_materials>

<exam_format>
Nền tảng TTNT, theo đề mẫu: trắc nghiệm tiếng Anh; khoảng 60% câu đọc code/YAML/lệnh rồi đoán kết quả; nhiều câu chọn nhiều đáp án nhưng đề không báo trước (câu có "statements", "Which ... (s)"); đáp án nhiễu kiểu đảo vị trí (`app.main:api` và `main.app:api`; private key ở runner hay ở EC2); có đáp án "All the statements are correct".
MMT: trắc nghiệm 4 đáp án, 1 đáp án đúng; câu khái niệm, so sánh, cơ chế và bài tính.
</exam_format>
</context>

<instructions>
1. **Đọc tài liệu trước khi viết bất cứ nội dung nào.** Trích text bằng `pdftotext -layout`, sau đó đọc:
   - Toàn bộ slide của cả hai môn (khoảng 900 trang), các file docx và code trong `llm_app`.
   - Toàn bộ ba cuốn sách (khoảng 1.300 trang). Đọc theo thứ tự ưu tiên để kịp giai đoạn 1: trước hết là các chương ứng với slide (Pro Git: Getting Started, Git Basics, Git Branching, phần remote/GitHub; sách Linux: shell, navigation, file manipulation, redirection/pipeline, permissions, processes, networking/SSH; Docker Deep Dive: toàn bộ), sau đó mới đến các chương còn lại. Nếu số lượng quá lớn so với ngữ cảnh, chia sách theo chương rồi tóm tắt từng chương ra file ghi chú trước khi soạn nội dung.
   - Cách dùng sách: **phạm vi ôn vẫn là những gì slide dạy.** Sách dùng để giải thích rõ hơn, bổ sung ví dụ, chỉ ra các trường hợp đặc biệt và lỗi hay gặp (ví dụ chi tiết về merge base, `.gitignore`, umask, inode, layer cache, `CMD` và `ENTRYPOINT`), và để soạn đáp án nhiễu sát thực tế. Chủ đề chỉ có trong sách mà slide không nhắc tới thì không đưa vào quiz, chỉ gom vào một mục "Đọc thêm" riêng ở cuối trang ôn.

   Mọi khái niệm, lệnh, con số đưa lên web phải lấy từ các tài liệu này, kèm nguồn (tên file + số trang slide hoặc chương/trang sách) để người học tra lại.

2. **Trước khi code, gửi một bản kế hoạch ngắn (tối đa 1 màn hình)** gồm: danh sách trang ôn kèm các mục chính của từng trang, những điểm tài liệu có mà checklist trong artifact còn thiếu, cấu trúc file. Sau đó làm tiếp ngay, không chờ duyệt, vì người dùng cần học tối nay.

3. **Xây theo giai đoạn, giao từng phần ngay khi dùng được:**
   - Giai đoạn 1 (giao trước, ưu tiên cao nhất): khung web + 9 trang ôn K1–K9 của Nền tảng TTNT + quiz TTNT (khoảng 100 câu, gồm 20 câu đề mẫu kèm đáp án và giải thích).
   - Giai đoạn 2 (xong trước thứ Bảy 7/11): 4 trang ôn C1–C4 của MMT + quiz MMT (khoảng 100 câu, tỉ lệ C1 23, C2 23, C3 30, C4 24) + bài tính MMT sinh số ngẫu nhiên.
   - Giai đoạn 3: flashcard, thi thử, sổ lỗi, trang tiến độ.

4. **Mỗi trang ôn có cùng khung** để người học quen mắt:
   1. Ý chính: 2–3 câu nói khối này dùng để làm gì
   2. Mô hình cốt lõi: sơ đồ SVG/HTML đơn giản (ví dụ đồ thị commit merge và rebase, 3 vùng của Git, Dockerfile → image → container, pipeline push → test → build → registry → EC2 → Caddy, chồng giao thức và đóng gói, bắt tay TCP, cửa sổ GBN/SR, đồ thị cwnd, cây DNS)
   3. Bảng lệnh/cú pháp hoặc công thức
   4. Bảng so sánh các cặp hay nhầm
   5. Bẫy hay gặp + ví dụ "đổi một chỗ thì kết quả đổi ra sao", theo kiểu đề mẫu
   6. Checklist tự đánh dấu (lấy từ artifact)
   7. 3 câu hỏi nhanh cuối trang; trả lời xong mới cho bấm "Đã ôn xong"

   Viết ngắn gọn, ưu tiên bảng và sơ đồ hơn đoạn văn dài. Nội dung tiếng Việt, giữ thuật ngữ và lệnh bằng tiếng Anh.

5. **Quiz:** mỗi câu là một object `{id, mon, khoi, loai: "single"|"multi", de, code?, dap_an[], dung[], giai_thich, nguon}`. Câu TTNT viết bằng tiếng Anh, có giải thích tiếng Việt. Câu "multi" dùng checkbox, chỉ tính điểm khi chọn đúng tất cả. Trộn thứ tự câu và đáp án, nhưng giữ nguyên vị trí đáp án "All the statements are correct". Sau khi trả lời, hiện giải thích và link về đúng mục trên trang ôn. Câu sai tự động đưa vào sổ lỗi.

6. **Quy tắc mở khóa:** flashcard và quiz của một khối chỉ mở khi khối đó đã được đánh dấu "Đã ôn xong". Có nút "Bỏ qua khóa" cho trường hợp cần làm gấp.
</instructions>

<tech_constraints>
- Một file `index.html` duy nhất (HTML + CSS + JS thuần, không framework, không build, không cần internet). Dữ liệu câu hỏi và nội dung ôn đặt trong `<script>` dạng JSON ngay trong file.
- Lưu tiến độ, điểm, sổ lỗi bằng `localStorage`, bọc trong try/catch.
- Dùng tốt trên điện thoại (từ 380px trở lên) và laptop. Chữ code dùng font monospace, khối code có highlight đơn giản.
- Giao diện: một cột nội dung rộng tối đa khoảng 760px, menu bên trái (trên điện thoại thì chuyển thành menu trên cùng) chia hai nhóm TTNT và MMT, mỗi mục có huy hiệu trạng thái (chưa ôn / đã ôn / điểm quiz). Nền `#FAFAF7`, chữ `#1F2328`, màu nhấn TTNT `#1F6FEB`, màu nhấn MMT `#B35900`, đúng `#1A7F37`, sai `#CF222E`. Font chữ thường: `"Be Vietnam Pro", system-ui`; font code: `"JetBrains Mono", monospace`. Không gradient, không hiệu ứng thừa, chế độ tối là tùy chọn.
- Phím tắt trong quiz: 1–4 chọn đáp án, Enter để nộp hoặc sang câu tiếp.
- Không thêm đăng nhập, backend, hay bất kỳ thứ gì ngoài phạm vi trên.
</tech_constraints>

<guardrails>
- Mọi đáp án và giải thích phải đúng theo slide. Nếu slide mơ hồ hoặc mâu thuẫn với sách, theo slide và ghi chú lại.
- Không bịa số trang; không chắc thì chỉ ghi tên file.
- Không đổi nội dung kế hoạch trong artifact. Đề xuất thay đổi thì ghi riêng ở phần ghi chú khi giao.
- Trước khi giao mỗi giai đoạn: mở trang bằng trình duyệt headless, chụp màn hình bản desktop và bản mobile, bấm thử một lượt quiz, kiểm tra 20 câu đề mẫu chấm đúng (đáp án tham khảo: 1c, 2d, 3b, 4abd, 5c, 6d, 7b, 8d, 9d, 10a, 11b, 12c, 13b, 14cd, 15ad, 16c, 17d, 18b, 19abc, 20ab).
</guardrails>

<output_format>
Mỗi giai đoạn giao:
1. File `index.html` (ghi đè bản trước, đồng thời lưu bản sao vào thư mục môn học).
2. Ghi chú tối đa 5 dòng: đã có gì, số câu theo từng khối/chương, những điểm đã bổ sung so với checklist, phần còn thiếu.
</output_format>
