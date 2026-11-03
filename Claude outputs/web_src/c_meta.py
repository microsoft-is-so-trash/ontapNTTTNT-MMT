SCHEDULE = [
    dict(date="3/11", label="T3 3/11 (tối)", mon="TTNT", nd="Ôn K4 (FastAPI, Pydantic) + chạy thử 422 và response_model; ôn K1, K2 Git"),
    dict(date="4/11", label="T4 4/11", mon="TTNT", nd="Sáng: K3 Linux, K5 Docker. Chiều: K6 CI. Tối: quiz K1–K6"),
    dict(date="5/11", label="T5 5/11", mon="TTNT", nd="Sáng: K7 EC2, K8 CD, K9 HTTPS. Chiều: quiz K7–K9, làm lại đề Demo_MidTerm. Tối: thi thử và sổ lỗi"),
    dict(date="6/11", label="T6 6/11", mon="TTNT", nd="Trước giờ thi: flashcard và sổ lỗi, không học thêm phần mới. Thi TTNT"),
    dict(date="7/11", label="T7 7/11", mon="MMT", nd="Ôn C1 + bài tính trễ; ôn C2 (HTTP, FTP, email)"),
    dict(date="8/11", label="CN 8/11", mon="MMT", nd="Ôn C2 (DNS, P2P, socket), quiz C1, C2; ôn C3 (UDP, checksum, rdt, GBN/SR)"),
    dict(date="9/11", label="T2 9/11", mon="MMT", nd="Ôn C3 (TCP, điều khiển luồng, điều khiển tắc nghẽn), bài tính cwnd, quiz C3"),
    dict(date="10/11", label="T3 10/11", mon="MMT", nd="Sáng: ôn C4 (router, IPv4, subnet, NAT, định tuyến), bài tính subnet và Dijkstra, quiz C4. Chiều/tối: thi thử và sổ lỗi"),
    dict(date="11/11", label="T4 11/11", mon="MMT", nd="Trước giờ thi: flashcard và sổ lỗi. Thi MMT"),
]

TOOLS = [
    dict(id="flash", title="Flashcard", soon=False, desc="Thẻ thuật ngữ, lệnh, port, công thức; lặp lại ngắt quãng 1 / 3 / 7 ngày."),
    dict(id="tinh", title="Bài tính MMT", soon=False, desc="Sinh số ngẫu nhiên cho các dạng bài tính MMT, có lời giải từng bước."),
    dict(id="thithu", title="Thi thử", soon=False, desc="Trộn câu nhiều khối, chọn số câu và thời gian, chấm sau khi nộp."),
    dict(id="solo", title="Sổ lỗi", soon=False, desc="Các câu từng sai; làm lại tới khi đúng 2 lần liên tiếp."),
    dict(id="tiendo", title="Tiến độ", soon=False, desc="% ôn xong, điểm quiz từng khối, khối yếu nhất."),
]
