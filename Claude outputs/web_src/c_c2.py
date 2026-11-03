from h import *


def M(*a, **k):
    k["mon"] = "MMT"
    return Q(*a, **k)


F = "chuong 2 v1.pdf"

DNS = """<svg viewBox="0 0 700 300" width="700" role="img" aria-label="Cây DNS và truy vấn lặp">
<g font-size="13">
<rect x="270" y="10" width="160" height="34" rx="8" class="boxa"/><text x="290" y="32" font-weight="700">Root DNS servers</text>
<rect x="90" y="80" width="120" height="30" rx="6" class="box"/><text x="104" y="100">com DNS</text>
<rect x="290" y="80" width="120" height="30" rx="6" class="box"/><text x="304" y="100">org DNS</text>
<rect x="490" y="80" width="120" height="30" rx="6" class="box"/><text x="504" y="100">edu DNS</text>
<text x="620" y="100" font-size="11.5" class="muted">← TLD</text>
<rect x="20" y="148" width="110" height="28" rx="6" class="box"/><text x="28" y="167" font-size="12">yahoo.com</text>
<rect x="140" y="148" width="120" height="28" rx="6" class="box"/><text x="148" y="167" font-size="12">amazon.com</text>
<rect x="290" y="148" width="110" height="28" rx="6" class="box"/><text x="298" y="167" font-size="12">pbs.org</text>
<rect x="440" y="148" width="100" height="28" rx="6" class="box"/><text x="448" y="167" font-size="12">poly.edu</text>
<rect x="550" y="148" width="120" height="28" rx="6" class="box"/><text x="558" y="167" font-size="12">umass.edu</text>
<text x="560" y="194" font-size="11.5" class="muted">← có thẩm quyền</text>
<path d="M350 44 L150 80 M350 44 L350 80 M350 44 L550 80 M150 110 L75 148 M150 110 L200 148 M350 110 L345 148 M550 110 L490 148 M550 110 L610 148" class="ln"/>
</g>
<g font-size="12.5">
<text x="10" y="222" font-weight="700">Truy vấn lặp:</text><text x="110" y="222">server được hỏi trả về “hãy hỏi server này” (root → TLD → có thẩm quyền)</text>
<text x="10" y="244" font-weight="700">Truy vấn đệ quy:</text><text x="130" y="244">server được hỏi tự phân giải thay bên hỏi → tải nặng ở cấp trên</text>
<text x="10" y="266" class="muted">Server cục bộ (của ISP) không hẳn thuộc cây: như proxy, có cache (hết hạn theo TTL).</text>
<text x="10" y="288" class="muted">Ví dụ www.amazon.com: root → .com TLD → amazon.com (có thẩm quyền) → IP.</text>
</g></svg>"""

P = {}
P["y"] = """<p>Tầng ứng dụng là nơi các <b>tiến trình</b> trên các host trao đổi <b>thông điệp</b> theo một giao thức (HTTP, FTP, SMTP/POP3/IMAP, DNS, BitTorrent). Ứng dụng chỉ chạy ở <b>thiết bị đầu cuối</b>, không cần viết cho thiết bị lõi. Tiến trình gửi/nhận qua <b>socket</b> và được định danh bằng <b>IP + số hiệu cổng</b>; tầng giao vận bên dưới cung cấp dịch vụ <b>TCP</b> hoặc <b>UDP</b>.</p>""" + src(F + " tr.5, 9–11, 15")

P["mohinh"] = diagram(DNS, "DNS: cơ sở dữ liệu phân tán, phân cấp (chuong 2 tr.53–59)") + """
<h3 id="c2-http-time">Thời gian tải trang HTTP</h3>""" + table(["Kiểu", "Mỗi đối tượng", "Trang = HTML gốc + N đối tượng (tuần tự, không song song)"], [
    ["Không liên tục (non-persistent, HTTP/1.0)", "1 RTT mở TCP + 1 RTT yêu cầu/đáp ứng + thời gian truyền tệp = <b>2RTT + t<sub>truyền</sub></b>", "(N+1) × 2RTT (+ thời gian truyền)"],
    ["Liên tục (persistent, HTTP/1.1)", "kết nối giữ mở; mỗi đối tượng tiếp theo 1 RTT (với pipelining: ít nhất 1 RTT cho tất cả)", "2RTT (TCP + HTML) + N × RTT"]]) + src(F + " tr.22–26") + """
<h3 id="c2-arch">Client-server và P2P</h3>""" + table(["", "Client-server", "P2P"], [
    ["Server", "host luôn hoạt động, IP cố định, ở data center", "không có server luôn hoạt động"],
    ["Bên kia", "client có thể không kết nối liên tục, IP có thể đổi, <b>không</b> nói chuyện trực tiếp với client khác", "peer nói chuyện trực tiếp, vừa yêu cầu vừa cung cấp dịch vụ; peer không kết nối liên tục, đổi IP"],
    ["Mở rộng / quản lý", "—", "tự mở rộng (peer mới mang thêm năng lực), quản lý phức tạp"],
    ["Ví dụ", "Web, mail", "BitTorrent, KanKan, Skype"]]) + src(F + " tr.6–8, 66")

P["bang"] = """<h3 id="c2-transport">Ứng dụng cần gì từ tầng giao vận</h3>""" + table(["Ứng dụng", "Mất dữ liệu", "Thông lượng", "Thời gian thực", "Giao thức ứng dụng / giao vận"], [
    ["Truyền file", "không", "mềm dẻo", "không", "FTP [RFC 959] / TCP"], ["Thư điện tử", "không", "mềm dẻo", "không", "SMTP [RFC 5321] / TCP"],
    ["Web", "không", "mềm dẻo", "không", "HTTP / TCP"], ["Audio/video thời gian thực", "chịu lỗi", "audio 5 kbps–1 Mbps, video 10 kbps–5 Mbps", "có, 100 ms", "—"],
    ["Trò chơi tương tác", "chịu lỗi", "vài kbps", "có, 100 ms", "—"], ["Streaming multimedia", "", "", "", "HTTP, RTP / <b>TCP hoặc UDP</b>"],
    ["Điện thoại Internet", "", "", "", "SIP, RTP, độc quyền (Skype) / <b>TCP hoặc UDP</b>"], ["Truy nhập từ xa", "", "", "", "Telnet / TCP"]]) + table(["TCP", "UDP"], [
    ["truyền tin cậy · điều khiển luồng (bên gửi không lấn át bên nhận) · điều khiển tắc nghẽn · <b>hướng kết nối</b>", "truyền <b>không tin cậy</b>; không có tin cậy, điều khiển luồng, tắc nghẽn, thiết lập kết nối"],
    ["không cung cấp: thời gian thực, đảm bảo băng thông, bảo mật", "không cung cấp: thời gian thực, băng thông, bảo mật"]]) + "<p>TCP/UDP <b>không mã hoá</b>; SSL/TLS là bảo mật ở tầng ứng dụng: ứng dụng dùng thư viện TLS gọi xuống TCP → kết nối mã hoá, toàn vẹn dữ liệu, xác thực đầu cuối.</p>" + src(F + " tr.13–17") + """
<h3 id="c2-http">HTTP</h3>""" + pre("""
GET /index.html HTTP/1.1\\r\\n          <- dòng yêu cầu: method sp URL sp version
Host: www-net.cs.umass.edu\\r\\n        <- các dòng tiêu đề
User-Agent: Firefox/3.6.10\\r\\n
Connection: keep-alive\\r\\n
\\r\\n                                   <- dòng trống: hết phần tiêu đề
(entity body)
""", "text") + table(["Mục", "Nội dung"], [
    ["Kết nối", "client mở TCP tới server <b>cổng 80</b>; trao đổi thông điệp HTTP; đóng TCP"],
    ["Không trạng thái", "server không lưu thông tin về các yêu cầu trước của client"],
    ["Method", "HTTP/1.0: GET, POST, HEAD (HEAD: server bỏ đối tượng ra khỏi đáp ứng). HTTP/1.1: thêm PUT (tải tệp lên theo URL), DELETE"],
    ["Mã trạng thái", "200 OK · 301 Moved Permanently (vị trí mới ở <code>Location:</code>) · 400 Bad Request · 404 Not Found · 505 HTTP Version Not Supported"],
    ["Cookie (4 thành phần)", "① dòng <code>set-cookie</code> trong <b>đáp ứng</b> ② dòng <code>cookie</code> trong <b>yêu cầu</b> tiếp theo ③ tệp cookie trên host người dùng, do trình duyệt quản lý ④ CSDL back-end tại website. Dùng cho cấp phép, giỏ hàng, khuyến nghị, phiên làm việc"],
    ["Web cache (proxy)", "trình duyệt gửi mọi yêu cầu tới cache: có thì trả ngay, không có thì cache hỏi server nguồn rồi trả về. Giảm thời gian đáp ứng và lưu lượng trên liên kết truy nhập; thường do ISP cài đặt; cache vừa là server (với client) vừa là client (với server nguồn)"]]) + src(F + " tr.19–35") + """
<h3 id="c2-ftp">FTP</h3>""" + ul(["Client/server, RFC 959; điều khiển: <b>TCP cổng 21</b>; dữ liệu: <b>TCP cổng 20</b> — mỗi file một kết nối dữ liệu mới, truyền xong server đóng.",
    "Điều khiển “out of band” (kênh riêng). Server duy trì <b>trạng thái</b>: thư mục hiện hành, cấp phép trước đó.",
    "Lệnh ASCII: USER, PASS, LIST, RETR (lấy file), STOR (đặt file). Mã trả về: 331 Username OK, password required · 125 data connection already open · 425 Can't open data connection · 452 Error writing file."]) + src(F + " tr.37–39") + """
<h3 id="c2-mail">Thư điện tử</h3>""" + table(["Thành phần", "Vai trò"], [
    ["User agent", "“mail reader”: soạn/đọc thư (Outlook, Thunderbird)"], ["Mail server", "hộp thư (mailbox) thư đến + hàng đợi thông điệp đi"],
    ["SMTP", "TCP <b>cổng 25</b>, truyền trực tiếp server gửi → server nhận; 3 bước: bắt tay, truyền, đóng; lệnh HELO, MAIL FROM, RCPT TO, DATA, QUIT; thông điệp ASCII 7-bit; kết thúc bằng CRLF.CRLF; kết nối bền vững; <b>đẩy</b> (push)"],
    ["POP3", "truy nhập thư: cấp phép (user, pass) + giao dịch (list, retr, dele, quit); “tải và xoá” (đổi client là không đọc lại được) hoặc “tải và giữ”; <b>không giữ trạng thái</b> giữa các phiên"],
    ["IMAP", "giữ mọi thư trên server, tổ chức theo thư mục, <b>giữ trạng thái</b> người dùng qua các phiên"],
    ["HTTP (webmail)", "gmail, Hotmail, Yahoo! Mail"]]) + "<p>Định dạng thư (RFC 822): dòng tiêu đề <code>To:</code>, <code>From:</code>, <code>Subject:</code> (khác lệnh SMTP MAIL FROM/RCPT TO) + dòng trống + thân.</p>" + src(F + " tr.41–49") + """
<h3 id="c2-dns">DNS</h3>""" + table(["Mục", "Nội dung"], [
    ["Dịch vụ", "dịch tên host → IP; bí danh host; bí danh mail server; phân tán tải (một tên nhiều IP)"],
    ["Vì sao không tập trung", "một điểm chịu lỗi, lưu lượng lớn, CSDL ở xa, khó bảo trì → không mở rộng được"],
    ["Root", "được server cục bộ hỏi khi không tự phân giải được; trả về cho server cục bộ"],
    ["TLD", "com, org, net, edu… và tên quốc gia uk, fr, jp"], ["Có thẩm quyền", "DNS server của tổ chức, ánh xạ tên → IP cho host của tổ chức"],
    ["Cục bộ (mặc định)", "mỗi ISP có một; nhận truy vấn của host, có cache, hoạt động như proxy"],
    ["Cache", "mục cache hết hạn theo TTL; host đổi IP thì Internet có thể chưa biết cho tới khi TTL hết"]]) + table(["Bản ghi RR (name, value, type, ttl)", "name → value"], [
    ["A", "tên host → địa chỉ IP"], ["NS", "tên miền (foo.com) → tên host của server có thẩm quyền"],
    ["CNAME", "tên bí danh → tên chuẩn (www.ibm.com → servereast.backup2.ibm.com)"], ["MX", "tên → tên mail server"]]) + "<p>Thông điệp truy vấn và trả lời <b>cùng định dạng</b>: identification 16 bit, flags (truy vấn/trả lời, đệ quy…), questions, answers, authority, additional. Đăng ký <code>networkutopia.com</code>: registrar chèn bản ghi NS + A của server có thẩm quyền vào TLD .com.</p>" + src(F + " tr.51–64") + """
<h3 id="c2-bt">BitTorrent</h3>""" + ul(["File chia thành <b>chunk</b> 256 Kb. <b>Torrent</b> = nhóm peer trao đổi chunk của một file; <b>tracker</b> theo dõi các peer trong torrent.",
    "Peer mới: đăng ký với tracker lấy danh sách peer, kết nối với tập con (lân cận); vừa download vừa upload; churn: peer đến và đi.",
    "Yêu cầu chunk: <b>hiếm nhất trước</b> (rarest first).",
    "Gửi chunk — <b>tit-for-tat</b>: gửi cho 4 peer đang gửi cho mình nhanh nhất, đánh giá lại top 4 mỗi <b>10 giây</b>; mỗi <b>30 giây</b> chọn ngẫu nhiên một peer khác để gửi (“optimistically unchoke”)."]) + src(F + " tr.66–69") + """
<h3 id="c2-socket">Lập trình socket</h3>""" + table(["UDP socket", "TCP socket"], [
    ["không “kết nối”, không bắt tay trước khi gửi", "client phải tiếp xúc server; tiến trình server phải chạy trước và tạo socket “cửa đón” (welcome)"],
    ["bên gửi gắn IP + cổng đích vào <b>mỗi gói</b>; bên nhận trích IP + cổng nguồn từ gói", "client tạo socket chỉ rõ IP + cổng server → TCP client thiết lập kết nối"],
    ["dữ liệu có thể mất hoặc sai thứ tự", "khi được tiếp xúc, server tạo <b>socket mới</b> cho client đó → nói chuyện với nhiều client; cổng nguồn phân biệt client"],
    ["truyền không tin cậy các nhóm byte", "truyền tin cậy, dòng byte đúng thứ tự"]]) + "<p>Ví dụ: client gửi một dòng → server đổi sang chữ hoa → gửi lại → client hiển thị.</p>" + src(F + " tr.71–75")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["HTTP không liên tục vs liên tục", "tối đa 1 đối tượng / kết nối TCP (2RTT mỗi đối tượng) vs nhiều đối tượng trên một kết nối giữ mở."],
    ["HTTP vs FTP", "HTTP: một kết nối cổng 80, không trạng thái. FTP: điều khiển cổng 21 + dữ liệu cổng 20 (out-of-band), có trạng thái."],
    ["HTTP vs SMTP", "HTTP <b>kéo</b> (pull), mỗi đối tượng trong một đáp ứng; SMTP <b>đẩy</b> (push), nhiều đối tượng trong thông điệp nhiều phần, ASCII 7-bit. Cả hai: lệnh/đáp ứng, mã trạng thái ASCII."],
    ["SMTP vs POP3/IMAP", "SMTP phân phối thư tới server người nhận; POP3/IMAP trích thư từ server về user agent."],
    ["POP3 vs IMAP", "POP3 tải (và xoá), không giữ trạng thái; IMAP giữ thư trên server, thư mục, giữ trạng thái."],
    ["Truy vấn lặp vs đệ quy", "lặp: server trả lời “tôi không biết, hãy hỏi server này”; đệ quy: server được hỏi tự phân giải hộ → tải nặng ở cấp trên."],
    ["A vs NS vs CNAME vs MX", "tên→IP · miền→server có thẩm quyền · bí danh→tên chuẩn · tên→mail server."],
    ["Client-server vs P2P", "server cố định, IP cố định vs peer tự do, tự mở rộng, quản lý phức tạp."],
    ["TCP vs UDP", "tin cậy, luồng, tắc nghẽn, hướng kết nối vs không có gì trong đó."],
    ["Socket TCP vs UDP", "TCP: socket cửa đón + socket riêng cho mỗi client; UDP: mỗi gói mang địa chỉ đích, không bắt tay."],
    ["set-cookie vs cookie", "set-cookie: trong đáp ứng của server (lần đầu); cookie: trong các yêu cầu sau của client."],
]) + src(F + " tr.7–8, 15, 22, 38, 45, 47–49, 57–58, 60, 73–74")

P["bay"] = trap("Bẫy 1 — IP có đủ định danh tiến trình?", "Không: nhiều tiến trình cùng chạy trên một host → cần <b>IP + số hiệu cổng</b> (HTTP server 80, mail server 25).", "c2-trap-id") + \
    trap("Bẫy 2 — đếm RTT", "Trang HTML + 10 ảnh, HTTP không liên tục, tuần tự: 11 × 2RTT = <b>22 RTT</b> (+ thời gian truyền). <b>Đổi một chỗ:</b> HTTP liên tục, không pipelining: 2RTT + 10 RTT = <b>12 RTT</b>.", "c2-trap-rtt") + \
    trap("Bẫy 3 — FTP mấy kết nối", "Mỗi lần truyền một file server mở một kết nối dữ liệu mới (cổng 20) và đóng sau khi xong; kết nối điều khiển (cổng 21) giữ suốt phiên.", "c2-trap-ftp") + \
    trap("Bẫy 4 — dòng To:/From: không phải lệnh SMTP", "<code>MAIL FROM</code>, <code>RCPT TO</code> là lệnh SMTP; <code>To:</code>, <code>From:</code>, <code>Subject:</code> là dòng tiêu đề trong nội dung thư (RFC 822).", "c2-trap-mail") + \
    trap("Bẫy 5 — POP3 “tải và xoá”", "Bob đọc thư bằng POP3 chế độ tải và xoá trên máy A → sang máy B không đọc lại được. IMAP giữ thư trên server nên đọc được ở mọi nơi.", "c2-trap-pop") + \
    trap("Bẫy 6 — cache DNS lỗi thời", "Đổi IP của web server nhưng người dùng vẫn vào IP cũ: bản ghi cũ còn trong cache cho tới khi <b>TTL</b> hết hạn.", "c2-trap-ttl") + \
    trap("Bẫy 7 — tit-for-tat", "Alice gửi chunk cho 4 peer <b>đang gửi cho cô nhanh nhất</b> (không phải 4 peer cô tải nhanh nhất từ đó theo kiểu ngẫu nhiên); top 4 xét lại mỗi 10 s; mỗi 30 s mở thêm một peer ngẫu nhiên.", "c2-trap-tft")

P["checklist"] = [
    "Kiến trúc client-server và P2P; process, socket, địa chỉ gồm IP + port",
    "Yêu cầu của ứng dụng (tin cậy, thông lượng, thời gian, bảo mật) và dịch vụ TCP so với UDP; ứng dụng nào dùng giao thức giao vận nào",
    "HTTP: stateless, non-persistent và persistent, tính thời gian theo RTT (2RTT + thời gian truyền), định dạng request/response, method, status code, cookie, web cache/proxy, conditional GET (304) — <i>conditional GET không có trong slide chương 2 v1 (xem Đọc thêm)</i>",
    "FTP: port 21 điều khiển, port 20 dữ liệu, out-of-band, stateful",
    "Email: user agent, mail server, SMTP (port 25, push), POP3 và IMAP (pull), so sánh với HTTP",
    "DNS: dịch vụ, cây phân cấp (root, TLD, authoritative, local), truy vấn lặp và đệ quy, cache, bản ghi A/NS/CNAME/MX, dùng UDP port 53 — <i>slide không ghi UDP 53</i>",
    "P2P: thời gian phân phối file client-server và P2P, BitTorrent (tracker, torrent, chunk, tit-for-tat) — <i>công thức phân phối file không có trong slide v1; có trong Bài tính MMT</i>",
    "Lập trình socket UDP và TCP: các bước, welcome socket và connection socket",
    "＋ SSL/TLS là bảo mật ở tầng ứng dụng; TCP/UDP không mã hoá",
    "＋ FTP lệnh USER/PASS/LIST/RETR/STOR và mã 331/125/425/452",
    "＋ Thông điệp DNS (identification, flags, 4 phần) và cách đăng ký tên miền với registrar; tấn công DNS (DDoS, đầu độc)",
]

P["quick"] = [
    QQ("HTTP không liên tục: thời gian để lấy một đối tượng là?", ["1 RTT", "2 RTT + thời gian truyền tệp", "3 RTT", "RTT/2"], "b", "1 RTT mở TCP, 1 RTT yêu cầu + đáp ứng, cộng thời gian truyền."),
    QQ("Bản ghi DNS nào ánh xạ tên miền tới tên server có thẩm quyền?", ["A", "NS", "CNAME", "MX"], "b", "NS: name = tên miền, value = tên host server có thẩm quyền."),
    QQ("FTP dùng cổng nào cho kết nối điều khiển?", ["20", "21", "25", "80"], "b", "Điều khiển 21, dữ liệu 20."),
]

P["docthem"] = ul([
    "<b>Conditional GET (304 Not Modified)</b> — Kurose &amp; Ross §2.2.5: cache gửi <code>If-modified-since: &lt;ngày&gt;</code>; nếu đối tượng chưa đổi server trả <code>304 Not Modified</code> không kèm đối tượng.",
    "<b>DNS chạy trên UDP cổng 53</b> — Kurose &amp; Ross §2.4 (slide không ghi).",
    "<b>Thời gian phân phối file</b> (Kurose &amp; Ross §2.5): client-server D<sub>cs</sub> ≥ max(NF/u<sub>s</sub>, F/d<sub>min</sub>); P2P D<sub>P2P</sub> ≥ max(F/u<sub>s</sub>, F/d<sub>min</sub>, NF/(u<sub>s</sub> + Σu<sub>i</sub>)) — luyện ở mục Bài tính MMT.",
    "Mã nguồn socket Python (UDPClient/TCPServer) trong giáo trình §2.7.",
])

BLOCK = dict(id="C2", mon="MMT", title="Tầng ứng dụng", src="chuong 2 v1.pdf", page=P)

QUESTIONS = [
    M("C2-01", "single", "Trong kiến trúc client-server, phát biểu nào đúng?", ["Server là host luôn hoạt động với địa chỉ IP cố định; client không truyền thông trực tiếp với client khác", "Client phải có IP cố định và luôn hoạt động", "Các client trao đổi dữ liệu trực tiếp với nhau", "Không cần server"], "a", "Tr.7.", F + " tr.7", "c2-arch"),
    M("C2-02", "single", "Đặc điểm nào thuộc kiến trúc P2P?", ["Mỗi peer vừa yêu cầu dịch vụ vừa cung cấp dịch vụ; hệ thống tự mở rộng nhưng quản lý phức tạp", "Có server luôn hoạt động với IP cố định", "Peer luôn kết nối liên tục với IP không đổi", "Chỉ dùng cho thư điện tử"], "a", "Tr.8.", F + " tr.8", "c2-arch"),
    M("C2-03", "single", "Vì sao địa chỉ IP của host không đủ để định danh một tiến trình?", ["Vì nhiều tiến trình có thể cùng chạy trên một host, nên cần thêm số hiệu cổng", "Vì IP chỉ dài 16 bit", "Vì IP thay đổi theo từng gói", "Vì tiến trình không cần định danh"], "a", "Định danh = IP + số hiệu cổng (tr.11).", F + " tr.11", "c2-trap-id"),
    M("C2-04", "single", "Socket được mô tả trong slide là:", ["Cửa vào/ra giữa tiến trình ứng dụng và tầng giao vận; phía trên do nhà phát triển điều khiển, phía dưới do hệ điều hành", "Một loại cáp mạng", "Bộ định tuyến ở biên", "Một bản ghi DNS"], "a", "Tr.10, 71.", F + " tr.10, 71", "c2-socket"),
    M("C2-05", "single", "Dịch vụ nào TCP cung cấp mà UDP không cung cấp?", ["Truyền tin cậy, điều khiển luồng, điều khiển tắc nghẽn và hướng kết nối", "Đảm bảo băng thông tối thiểu", "Đảm bảo thời gian thực", "Mã hoá dữ liệu"], "a", "TCP cũng không cung cấp thời gian thực, đảm bảo băng thông, bảo mật (tr.15).", F + " tr.15", "c2-transport"),
    M("C2-06", "single", "Theo bảng ứng dụng – giao thức, ứng dụng nào có thể dùng TCP hoặc UDP?", ["Điện thoại Internet (SIP, RTP, Skype)", "Thư điện tử (SMTP)", "Web (HTTP)", "Truyền file (FTP)"], "a", "Streaming multimedia và điện thoại Internet: TCP hoặc UDP; còn lại TCP.", F + " tr.16", "c2-transport"),
    M("C2-07", "single", "Ứng dụng nào chịu được mất mát dữ liệu nhưng yêu cầu độ trễ khoảng 100 ms?", ["Trò chơi tương tác", "Truyền file", "Thư điện tử", "Web"], "a", "Bảng tr.14: trò chơi tương tác chịu lỗi, vài kbps, có thời gian thực 100 ms.", F + " tr.13–14", "c2-transport"),
    M("C2-08", "single", "HTTP được gọi là “không trạng thái” vì:", ["Server không lưu giữ thông tin về các yêu cầu trước đó của client", "HTTP không dùng TCP", "Client không lưu cookie", "Mỗi trang chỉ có một đối tượng"], "a", "Tr.21. Trạng thái được thêm vào bằng cookie.", F + " tr.21", "c2-http"),
    M("C2-09", "single", "Khác biệt giữa HTTP không liên tục và HTTP liên tục là:", ["Không liên tục: tối đa một đối tượng trên một kết nối TCP; liên tục: nhiều đối tượng trên một kết nối giữ mở", "Không liên tục dùng UDP", "Liên tục cần 2 RTT cho mỗi đối tượng", "Không có khác biệt"], "a", "Tr.22, 26.", F + " tr.22, 26", "c2-http-time"),
    M("C2-10", "single", "Trang web gồm tệp HTML cơ bản và 10 ảnh JPEG. Dùng HTTP không liên tục, lấy tuần tự từng đối tượng (không song song), bỏ qua thời gian truyền. Tổng thời gian khoảng:", ["22 RTT", "11 RTT", "12 RTT", "2 RTT"], "a", "Mỗi đối tượng 2RTT (mở TCP + yêu cầu/đáp ứng); 11 đối tượng → 22 RTT.", F + " tr.23–25", "c2-trap-rtt"),
    M("C2-11", "single", "Cùng trang trên (HTML + 10 ảnh) nhưng dùng HTTP liên tục, gửi yêu cầu tuần tự mỗi đối tượng 1 RTT, bỏ qua thời gian truyền. Tổng thời gian khoảng:", ["12 RTT", "22 RTT", "11 RTT", "3 RTT"], "a", "2RTT cho TCP + HTML gốc, sau đó 10 × 1 RTT → 12 RTT.", F + " tr.25–26; kế hoạch (bảng bài tính)", "c2-trap-rtt"),
    M("C2-12", "single", "Trong thông điệp yêu cầu HTTP, điều gì đánh dấu kết thúc phần tiêu đề?", ["Một dòng chỉ gồm ký tự trở về đầu dòng và xuống dòng (\\r\\n)", "Dòng Host:", "Dòng Connection: keep-alive", "Mã trạng thái 200"], "a", "Dòng yêu cầu (method sp URL sp version) → các dòng tiêu đề → dòng trống → thân.", F + " tr.27–28", "c2-http"),
    M("C2-13", "single", "Server trả mã 301 Moved Permanently nghĩa là:", ["Đối tượng đã chuyển, vị trí mới được ghi trong Location:", "Yêu cầu thành công", "Server không hiểu yêu cầu", "Phiên bản HTTP không được hỗ trợ"], "a", "200 OK, 301 Moved Permanently, 400 Bad Request, 404 Not Found, 505 HTTP Version Not Supported.", F + " tr.30", "c2-http"),
    M("C2-14", "single", "Lần đầu Susan truy cập trang thương mại, server tạo ID 1678. Từ đó, cookie đi trong các thông điệp như thế nào?", ["Đáp ứng đầu tiên có dòng set-cookie: 1678; các yêu cầu sau của trình duyệt có dòng cookie: 1678", "Yêu cầu đầu tiên có set-cookie: 1678", "Cookie chỉ lưu ở server, không gửi đi", "Cookie được gửi qua DNS"], "a", "Bốn thành phần: set-cookie trong đáp ứng, cookie trong yêu cầu tiếp theo, tệp cookie do trình duyệt quản lý, CSDL back-end.", F + " tr.31–32", "c2-http"),
    M("C2-15", "single", "Web cache (proxy server) nhận yêu cầu cho một đối tượng không có trong cache. Nó sẽ:", ["Yêu cầu đối tượng từ server nguồn rồi trả về cho client", "Trả về 404 cho client", "Chuyển client sang dùng FTP", "Bỏ qua yêu cầu"], "a", "Có trong cache → trả ngay; không có → hỏi server nguồn rồi trả. Lợi ích: giảm thời gian đáp ứng và lưu lượng liên kết truy nhập.", F + " tr.34–35", "c2-http"),
    M("C2-16", "single", "Phát biểu nào đúng về FTP?", ["Kết nối điều khiển TCP cổng 21, kết nối dữ liệu TCP cổng 20; server duy trì trạng thái (thư mục hiện hành, cấp phép)", "FTP dùng một kết nối duy nhất cổng 80 và không trạng thái", "FTP dùng UDP cổng 21", "Kết nối dữ liệu giữ mở suốt phiên cho mọi file"], "a", "Điều khiển “out of band”; mỗi file một kết nối dữ liệu, truyền xong thì đóng.", F + " tr.37–38", "c2-trap-ftp"),
    M("C2-17", "single", "So sánh SMTP với HTTP, phát biểu nào đúng?", ["HTTP là giao thức kéo (pull), SMTP là giao thức đẩy (push)", "SMTP là kéo, HTTP là đẩy", "Cả hai đều không dùng mã trạng thái", "SMTP gửi mỗi đối tượng trong một đáp ứng riêng"], "a", "SMTP: đẩy, ASCII 7-bit, nhiều đối tượng trong thông điệp nhiều phần; HTTP: kéo.", F + " tr.45", "c2-sosanh"),
    M("C2-18", "single", "SMTP truyền thư giữa các mail server dùng:", ["TCP cổng 25, truyền trực tiếp từ server gửi tới server nhận", "UDP cổng 25", "TCP cổng 110 qua nhiều server trung gian", "HTTP cổng 80"], "a", "Tr.43: TCP, cổng 25, 3 bước bắt tay – truyền – đóng.", F + " tr.43", "c2-mail"),
    M("C2-19", "single", "Bob dùng POP3 chế độ “tải và xoá” trên laptop, sau đó mở thư trên điện thoại. Điều gì xảy ra?", ["Không đọc lại được các thư đã tải về laptop vì chúng đã bị xoá khỏi server", "Đọc được vì POP3 giữ thư trên server", "Thư tự động đồng bộ theo thư mục", "Điện thoại tải lại qua SMTP"], "a", "POP3 không giữ trạng thái phiên; IMAP giữ thư trên server và tổ chức theo thư mục.", F + " tr.49", "c2-trap-pop"),
    M("C2-20", "single", "Client muốn địa chỉ IP của www.amazon.com theo cấu trúc phân cấp. Thứ tự server được hỏi là:", ["Server gốc → server TLD .com → server có thẩm quyền amazon.com", "Server có thẩm quyền → TLD → gốc", "TLD .com → server gốc → amazon.com", "Chỉ hỏi server gốc"], "a", "Tr.53.", F + " tr.53–55", "c2-mohinh"),
    M("C2-21", "single", "Khác biệt giữa truy vấn DNS lặp và đệ quy là:", ["Lặp: server được hỏi trả về tên server nên hỏi tiếp; đệ quy: server được hỏi nhận trách nhiệm phân giải giùm", "Lặp chỉ dùng cho bản ghi MX", "Đệ quy giảm tải cho các cấp cao", "Không khác nhau"], "a", "Đệ quy đặt tải nặng ở các cấp cao hơn.", F + " tr.57–58", "c2-sosanh"),
    M("C2-22", "single", "Bản ghi <code>(networkutopia.com, dns1.networkutopia.com, NS)</code> có ý nghĩa gì?", ["dns1.networkutopia.com là server có thẩm quyền cho tên miền networkutopia.com", "networkutopia.com là bí danh của dns1", "dns1 là mail server của networkutopia.com", "networkutopia.com có IP là dns1"], "a", "type=NS: name là tên miền, value là tên host của server có thẩm quyền. Registrar chèn bản ghi NS và A này vào TLD .com.", F + " tr.60, 63", "c2-dns"),
    M("C2-23", "single", "Trong BitTorrent, Alice chọn gửi chunk cho ai?", ["4 peer đang gửi chunk cho cô với tốc độ cao nhất (đánh giá lại mỗi 10 s), cộng một peer chọn ngẫu nhiên mỗi 30 s", "Mọi peer trong torrent cùng lúc", "Chỉ tracker", "Peer có ít chunk nhất"], "a", "Tit-for-tat + optimistically unchoke; yêu cầu chunk thì hiếm nhất trước.", F + " tr.69", "c2-trap-tft"),
]
