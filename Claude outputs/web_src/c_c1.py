from h import *


def M(*a, **k):
    k["mon"] = "MMT"
    return Q(*a, **k)


F = "chuong 1 v2.pdf"

STACK = """<svg viewBox="0 0 700 300" width="700" role="img" aria-label="OSI 7 tầng, TCP/IP và đóng gói">
<g font-size="13">
<text x="10" y="18" font-weight="700">OSI (7 tầng)</text><text x="200" y="18" font-weight="700">TCP/IP (slide: 4 tầng)</text><text x="400" y="18" font-weight="700">Đóng gói (5 tầng Kurose)</text>
<g>
<rect x="10" y="28" width="160" height="26" class="box"/><text x="18" y="46">7 Application · Data</text>
<rect x="10" y="56" width="160" height="26" class="box"/><text x="18" y="74">6 Presentation · Data</text>
<rect x="10" y="84" width="160" height="26" class="box"/><text x="18" y="102">5 Session · Data</text>
<rect x="10" y="112" width="160" height="26" class="boxa"/><text x="18" y="130">4 Transport · Segments</text>
<rect x="10" y="140" width="160" height="26" class="box"/><text x="18" y="158">3 Network · Packets</text>
<rect x="10" y="168" width="160" height="26" class="box"/><text x="18" y="186">2 Data link · Frames</text>
<rect x="10" y="196" width="160" height="26" class="box"/><text x="18" y="214">1 Physical · Bits</text>
<rect x="200" y="28" width="170" height="82" class="box"/><text x="208" y="66">Application</text><text x="208" y="84" font-size="11" class="muted">FTP HTTP SMTP DNS TFTP</text>
<rect x="200" y="112" width="170" height="26" class="boxa"/><text x="208" y="130">Transport · TCP UDP</text>
<rect x="200" y="140" width="170" height="26" class="box"/><text x="208" y="158">Internet · IP</text>
<rect x="200" y="168" width="170" height="54" class="box"/><text x="208" y="192">Network access</text><text x="208" y="210" font-size="11" class="muted">LAN, WAN</text>
</g>
<g class="mono" font-size="12.5">
<text x="400" y="46">message</text><rect x="520" y="32" width="40" height="20" class="boxa"/><text x="533" y="46">M</text><text x="580" y="46" font-size="12" class="muted">ứng dụng</text>
<text x="400" y="80">segment</text><rect x="490" y="66" width="28" height="20" class="box"/><text x="496" y="80">Ht</text><rect x="520" y="66" width="40" height="20" class="boxa"/><text x="533" y="80">M</text><text x="580" y="80" font-size="12" class="muted">giao vận</text>
<text x="400" y="114">datagram</text><rect x="460" y="100" width="28" height="20" class="box"/><text x="465" y="114">Hn</text><rect x="490" y="100" width="28" height="20" class="box"/><text x="496" y="114">Ht</text><rect x="520" y="100" width="40" height="20" class="boxa"/><text x="533" y="114">M</text><text x="580" y="114" font-size="12" class="muted">mạng</text>
<text x="400" y="148">frame</text><rect x="430" y="134" width="28" height="20" class="box"/><text x="436" y="148">Hl</text><rect x="460" y="134" width="28" height="20" class="box"/><text x="465" y="148">Hn</text><rect x="490" y="134" width="28" height="20" class="box"/><text x="496" y="148">Ht</text><rect x="520" y="134" width="40" height="20" class="boxa"/><text x="533" y="148">M</text><text x="580" y="148" font-size="12" class="muted">liên kết</text>
<text x="400" y="182" font-size="12" class="muted">vật lý: bits</text>
</g>
<text x="400" y="212" font-size="12">switch: xử lý tới tầng liên kết (2)</text><text x="400" y="230" font-size="12">router: xử lý tới tầng mạng (3)</text>
<text x="10" y="252" font-size="12" class="muted">OSI: Application + Presentation + Session ≈ Application của TCP/IP; Data link + Physical ≈ Network access.</text>
<text x="10" y="272" font-size="12" class="muted">Đi xuống: mỗi tầng thêm header (H) vào phía trước; đi lên ở đích: bóc header theo thứ tự ngược lại.</text>
</g></svg>"""

P = {}
P["y"] = """<p><b>Mạng máy tính</b> = tập hợp các máy tính nối với nhau bằng đường truyền vật lý theo một kiến trúc (topology + giao thức). <b>Internet</b> là “mạng của các mạng”: <b>phần biên</b> (host chạy ứng dụng, mạng truy nhập) và <b>phần lõi</b> (lưới router chuyển mạch gói). Chương này cho bức tranh tổng thể: phân loại mạng, OSI và TCP/IP, đóng gói, 4 loại trễ, thông lượng, an ninh và lịch sử.</p>
<p>Học theo tầng: mỗi tầng phải trả lời được <b>dịch vụ cho tầng trên · nhờ tầng dưới làm gì · đơn vị dữ liệu</b> (message, segment, datagram, frame).</p>""" + src(F + " tr.2, 5, 30, 35–37")

P["mohinh"] = diagram(STACK, "OSI, TCP/IP và đóng gói (chuong 1 tr.22–28)") + """
<h3 id="c1-edgecore">Biên và lõi</h3>""" + table(["Phần", "Gồm", "Ghi chú"], [
    ["Biên (edge)", "host: client và server (server thường ở data center)", "chạy ứng dụng mạng"],
    ["Mạng truy nhập", "khu dân cư: xDSL, cable modem, FTTx · tổ chức: mạng trường/công ty · di động: WiFi, 4G/5G", "nối host tới router biên; có dây và không dây"],
    ["Lõi (core)", "lưới router kết nối với nhau, chuyển mạch gói", "chuyển tiếp gói từ router này sang router kế tiếp"]]) + """
<h3 id="c1-isp">Cấu trúc Internet</h3><p>Nối trực tiếp mọi ISP truy nhập với nhau cần O(N²) kết nối → thay vào đó: ISP truy nhập → <b>ISP khu vực</b> → <b>ISP lớp 1</b> (Level 3, Sprint, AT&amp;T, NTT); các ISP nối nhau qua <b>IXP</b> (Internet exchange point) và <b>peering link</b>; <b>mạng cung cấp nội dung</b> (Google, Microsoft, Akamai) chạy mạng riêng để tới gần người dùng.</p>""" + src(F + " tr.35–51")

P["bang"] = """<h3 id="c1-delay">4 loại trễ tại một nút</h3>
<p style="font-size:18px;text-align:center"><b>d<sub>nodal</sub> = d<sub>proc</sub> + d<sub>queue</sub> + d<sub>trans</sub> + d<sub>prop</sub></b></p>""" + table(["Trễ", "Công thức / đặc điểm"], [
    ["d<sub>proc</sub> xử lý", "kiểm tra lỗi bit, xác định liên kết ra; thường &lt; msec"],
    ["d<sub>queue</sub> hàng đợi", "thời gian chờ ở đầu ra; phụ thuộc mức tắc nghẽn của router"],
    ["d<sub>trans</sub> truyền", "<b>L/R</b> — L độ dài gói (bit), R băng thông liên kết (bps)"],
    ["d<sub>prop</sub> lan truyền", "<b>d/s</b> — d chiều dài liên kết, s tốc độ lan truyền (~2×10<sup>8</sup> m/s)"]]) + note("Ví dụ: L = 1500 byte = 12 000 bit, R = 10 Mbps → d<sub>trans</sub> = 1,2 ms. d = 2000 km, s = 2×10<sup>8</sup> m/s → d<sub>prop</sub> = 10 ms. Nhớ đổi byte → bit (×8), Mbps = 10<sup>6</sup> bps.") + src(F + " tr.54–55") + """
<h3 id="c1-thr">Thông lượng</h3>""" + ul([
    "Thông lượng: tốc độ (bit/đơn vị thời gian) bit được truyền giữa bên gửi và bên nhận; <b>tức thời</b> (tại một thời điểm) và <b>trung bình</b> (trong một khoảng).",
    "Đường gồm các liên kết R<sub>s</sub>, R<sub>c</sub>: thông lượng đầu-cuối = <b>min(R<sub>s</sub>, R<sub>c</sub>)</b>. Liên kết giới hạn thông lượng gọi là <b>nút cổ chai</b>.",
    "Truyền file F bit với thông lượng T → thời gian ≈ F/T."]) + src(F + " tr.58–59") + """
<h3 id="c1-loss">Hàng đợi, mất gói, traceroute</h3>""" + ul([
    "Tốc độ đến liên kết (tạm thời) vượt khả năng truyền → gói <b>xếp hàng</b> trong bộ đệm; bộ đệm <b>đầy</b> → gói đến bị <b>bỏ (mất)</b>. Gói mất có thể được nút trước/host nguồn gửi lại hoặc không.",
    "<b>traceroute</b>: với mỗi i, gửi <b>3 gói thăm dò</b> tới router thứ i (trường thời gian sống = i); router i gửi phản hồi, bên gửi đo thời gian khứ hồi."]) + src(F + " tr.42, 53, 56–57") + """
<h3 id="c1-class">Phân loại mạng</h3>""" + table(["Theo", "Loại"], [
    ["Quy mô", "LAN (toà nhà, trường; rẻ, quản trị đơn giản) · MAN (một đô thị; phức tạp, đắt hơn) · WAN (quốc gia, lục địa; dùng công nghệ ISP) · GAN (toàn cầu, trường hợp đặc biệt của WAN, dùng TCP/IP)"],
    ["Kỹ thuật chuyển mạch", "chuyển mạch kênh · chuyển mạch thông báo · chuyển mạch gói"],
    ["Chức năng", "PAN, WLAN, VLAN, VPN…"],
    ["Topology", "bus, star, extended star, ring, hierarchical, mesh"],
    ["Đường truyền", "cáp đồng trục, cáp xoắn đôi, cáp quang, vô tuyến (radio, di động, viba, vệ tinh, hồng ngoại)"]]) + src(F + " tr.6–19")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["Chuyển mạch kênh vs gói", "Kênh: thiết lập đường riêng A→B rồi dữ liệu đi trên đường đó. Gói: message chia thành gói, mỗi gói có thể đi đường khác, đến đích có thể <b>sai thứ tự</b>; chia sẻ tài nguyên nên có hàng đợi/mất gói."],
    ["Chuyển mạch thông báo vs gói", "Thông báo: <b>cả message</b> được lưu rồi chuyển tiếp qua từng nút. Gói: chia nhỏ thành các gói."],
    ["OSI vs TCP/IP", "OSI 7 tầng (có Presentation, Session); TCP/IP gộp 3 tầng trên thành Application, gộp Data link + Physical thành Network access."],
    ["Forwarding vs routing", "Chuyển tiếp: <b>cục bộ</b>, đưa gói từ đầu vào ra đầu ra phù hợp theo bảng chuyển tiếp. Định tuyến: <b>toàn cục</b>, xác định đường nguồn → đích bằng giải thuật định tuyến."],
    ["Switch vs router", "Switch xử lý tới tầng liên kết (frame); router xử lý tới tầng mạng (datagram)."],
    ["d<sub>trans</sub> vs d<sub>prop</sub>", "L/R phụ thuộc kích thước gói và băng thông; d/s phụ thuộc khoảng cách và môi trường. Hai đại lượng rất khác nhau."],
    ["Virus vs worm", "Virus: tự sao chép khi người nhận <b>thực thi</b> đối tượng (tệp đính kèm). Worm: lây qua đối tượng nhận <b>thụ động</b> và tự thực thi."],
    ["DoS vs sniffing vs spoofing", "DoS: làm cạn tài nguyên bằng lưu lượng giả (DDoS dùng botnet). Sniffing: bắt gói trên đường truyền chung (Wireshark). Spoofing: gửi gói với <b>địa chỉ nguồn sai</b>."],
    ["Thông lượng tức thời vs trung bình", "tại một thời điểm vs đo trong một khoảng thời gian."],
]) + src(F + " tr.17–19, 22–28, 41, 54–55, 58, 66–69")

P["bay"] = trap("Bẫy 1 — byte và bit", "Gói 1 KB truyền trên 1 Mbps: L = 8 000 bit (hoặc 8 192 nếu đề dùng 1024) → 8 ms, không phải 1 ms. Luôn đổi byte → bit.", "c1-trap-unit") + \
    trap("Bẫy 2 — trễ truyền không phụ thuộc khoảng cách", "Tăng gấp đôi chiều dài cáp → chỉ d<sub>prop</sub> tăng gấp đôi; d<sub>trans</sub> giữ nguyên. Tăng gấp đôi băng thông → d<sub>trans</sub> giảm một nửa, d<sub>prop</sub> giữ nguyên.", "c1-trap-dist") + \
    trap("Bẫy 3 — thông lượng là min, không phải tổng hay trung bình", "R<sub>s</sub> = 2 Mbps, R<sub>c</sub> = 1 Mbps → thông lượng 1 Mbps. <b>Đổi một chỗ:</b> R<sub>c</sub> = 5 Mbps → nút cổ chai thành R<sub>s</sub>, thông lượng 2 Mbps.", "c1-trap-thr") + \
    trap("Bẫy 4 — TCP/IP mấy tầng?", "Slide chương 1 vẽ TCP/IP <b>4 tầng</b> (Application, Transport, Internet, Network access); sơ đồ đóng gói lại dùng <b>5 tầng</b> Kurose (ứng dụng, giao vận, mạng, liên kết, vật lý). Đọc kỹ đề hỏi mô hình nào.", "c1-trap-layers") + \
    trap("Bẫy 5 — đơn vị dữ liệu", "Ứng dụng: message · giao vận: segment · mạng: datagram (OSI gọi packet) · liên kết: frame · vật lý: bit.", "c1-trap-pdu") + \
    trap("Bẫy 6 — mất gói xảy ra ở đâu", "Do bộ đệm (hàng đợi) có hạn bị <b>đầy</b> khi tốc độ đến vượt tốc độ truyền — không phải do d<sub>prop</sub> lớn.", "c1-trap-loss")

P["checklist"] = [
    "Khái niệm mạng, đường truyền (cáp xoắn đôi, cáp đồng trục, cáp quang, vô tuyến), topology (bus, star, ring, mesh)",
    "Giao thức là gì (định dạng, thứ tự thông điệp, hành động khi nhận)",
    "Phân loại mạng theo quy mô (LAN, MAN, WAN, GAN) và theo kỹ thuật chuyển mạch",
    "Phần biên (host, mạng truy nhập: DSL, cable, FTTH, Wi-Fi, 4G/5G) và phần lõi",
    "Chuyển mạch ghép kênh (FDM, TDM) và chuyển mạch gói (store-and-forward, hàng đợi, mất gói); kiến trúc mạng của các ISP — <i>slide chương 1 v2 không trình bày FDM/TDM; chỉ có sơ đồ chuyển mạch kênh/thông báo/gói (tr.17–19)</i>",
    "Hiệu năng: 4 loại trễ d_proc, d_queue, d_trans = L/R, d_prop = d/s; cường độ lưu lượng La/R; traceroute; thông lượng và nút cổ chai — <i>La/R không có trong slide v2</i>",
    "Mô hình OSI 7 tầng và TCP/IP 5 tầng; đóng gói (encapsulation); thiết bị nào xử lý tới tầng nào (switch tầng 2, router tầng 3)",
    "An ninh mạng (malware, DoS/DDoS, nghe lén, giả mạo IP), lịch sử Internet",
    "＋ Forwarding vs routing (hai chức năng của mạng lõi)",
    "＋ Chuyển mạch thông báo (cả message lưu–chuyển tiếp)",
    "＋ IXP, peering link, ISP lớp 1, mạng cung cấp nội dung",
    "＋ RFC / IETF; lịch sử Internet Việt Nam (1997 chính thức kết nối)",
]

P["quick"] = [
    QQ("Gói 2000 byte, liên kết 8 Mbps. d<sub>trans</sub> = ?", ["0,25 ms", "2 ms", "0,25 s", "16 ms"], "b", "L = 16 000 bit; 16 000 / 8×10<sup>6</sup> = 2 ms."),
    QQ("Đơn vị dữ liệu ở tầng giao vận gọi là gì?", ["frame", "datagram", "segment", "message"], "c", "Ht + M = segment."),
    QQ("Router xử lý gói tới tầng nào?", ["Vật lý", "Liên kết", "Mạng", "Ứng dụng"], "c", "Router: tầng mạng; switch: tầng liên kết."),
]

P["docthem"] = ul([
    "Kurose &amp; Ross bản 8 mục 1.3 (ghép kênh FDM/TDM trong chuyển mạch kênh) và 1.4 (cường độ lưu lượng La/R) — artifact có nêu nhưng slide chương 1 v2 không trình bày; ôn nếu giảng viên nhắc trên lớp.",
    "Lịch sử: 1961 Kleinrock (lý thuyết hàng đợi), 1969 nút ARPAnet đầu tiên, 1974 Cerf &amp; Kahn, 1983 TCP/IP và DNS, 1988 điều khiển tắc nghẽn TCP, đầu 1990 Web (Berners-Lee), 2008 SDN; Việt Nam kết nối Internet chính thức năm 1997 (tr.71–77).",
])

BLOCK = dict(id="C1", mon="MMT", title="Tổng quan về mạng máy tính", src="chuong 1 v2.pdf", page=P)

QUESTIONS = [
    M("C1-01", "single", "Theo slide, mạng máy tính là gì?", ["Tập hợp các máy tính được nối với nhau bởi các đường truyền vật lý theo một kiến trúc nào đó", "Tập hợp các phần mềm chạy trên một máy chủ", "Một máy tính có nhiều card mạng", "Tập hợp các giao thức của Internet"], "a",
      "Định nghĩa ở tr.5: máy tính + đường truyền vật lý + kiến trúc.", F + " tr.5", "c1-y"),
    M("C1-02", "single", "Giao thức mạng định nghĩa những gì?", ["Định dạng, thứ tự các thông điệp gửi/nhận giữa các thực thể mạng và các hành động khi truyền/nhận thông điệp", "Chỉ tốc độ truyền của đường truyền", "Chỉ địa chỉ IP của các host", "Loại cáp được sử dụng"], "a",
      "Giao thức: định dạng, thứ tự thông điệp, hành động thực hiện khi gửi/nhận (tr.10).", F + " tr.10–11", "c1-y"),
    M("C1-03", "single", "Mạng được cài đặt trong phạm vi một toà nhà hoặc khu trường học, chi phí rẻ, quản trị đơn giản là:", ["LAN", "MAN", "WAN", "GAN"], "a", "LAN: phạm vi nhỏ, thiết bị gần nhau, rẻ, dễ quản trị.", F + " tr.13", "c1-class"),
    M("C1-04", "single", "Phát biểu nào đúng về mạng MAN?", ["Cài đặt trong phạm vi một đô thị hoặc trung tâm kinh tế – xã hội, phức tạp và đắt hơn LAN", "Phủ khắp địa cầu, là trường hợp đặc biệt của WAN", "Chỉ dùng trong một phòng", "Không cần router"], "a",
      "MAN: một đô thị; GAN mới là phạm vi toàn cầu.", F + " tr.14, 16", "c1-class"),
    M("C1-05", "single", "Topology trong đó mỗi nút nối trực tiếp tới nhiều (hoặc tất cả) nút khác gọi là:", ["Mesh", "Bus", "Ring", "Star"], "a", "Sơ đồ topology tr.9: mesh = lưới, nhiều đường nối trực tiếp.", F + " tr.9", "c1-class"),
    M("C1-06", "single", "So sánh chuyển mạch kênh và chuyển mạch gói, phát biểu nào đúng?", ["Trong chuyển mạch gói, các gói của cùng một thông điệp có thể đi theo các đường khác nhau và đến đích không theo thứ tự", "Chuyển mạch gói luôn thiết lập trước một đường dành riêng", "Chuyển mạch kênh chia thông điệp thành các gói nhỏ", "Chuyển mạch gói không bao giờ có hàng đợi"], "a",
      "Sơ đồ tr.19: gói 1–4 đi các đường khác nhau, đến B theo thứ tự 1,3,4,2. Chuyển mạch kênh dùng một đường cố định (tr.17).", F + " tr.17, 19, 42", "c1-sosanh"),
    M("C1-07", "single", "Kỹ thuật chuyển mạch trong đó toàn bộ thông báo được lưu ở từng nút rồi mới chuyển tiếp là:", ["Chuyển mạch thông báo", "Chuyển mạch kênh", "Chuyển mạch gói", "Ghép kênh"], "a", "Sơ đồ tr.18: Mess 1, Mess 2 đi nguyên khối qua các nút.", F + " tr.18", "c1-sosanh"),
    M("C1-08", "single", "Trong mô hình OSI, tầng thứ 4 và đơn vị dữ liệu tương ứng là:", ["Transport – Segments", "Network – Packets", "Data link – Frames", "Session – Data"], "a", "OSI: 7 Application, 6 Presentation, 5 Session, 4 Transport (Segments), 3 Network (Packets), 2 Data link (Frames), 1 Physical (Bits).", F + " tr.22", "c1-mohinh"),
    M("C1-09", "single", "Những tầng OSI nào tương ứng với tầng Application của TCP/IP?", ["Application, Presentation, Session", "Application, Transport", "Session, Transport, Network", "Chỉ Application"], "a", "Bảng so sánh tr.28.", F + " tr.28", "c1-trap-layers"),
    M("C1-10", "single", "Trong mô hình TCP/IP, tầng nào đảm nhiệm chọn đường đi tốt nhất, gán địa chỉ, đóng gói và định tuyến dữ liệu?", ["Tầng liên mạng (Internet)", "Tầng giao vận", "Tầng ứng dụng", "Tầng giao diện mạng"], "a", "Tr.25: Internet Layer chọn đường tốt nhất, gán địa chỉ, đóng gói, định tuyến.", F + " tr.25", "c1-mohinh"),
    M("C1-11", "single", "Ở bên gửi, gói ở tầng liên kết có cấu trúc nào?", ["Hl Hn Ht M (frame)", "Ht M (frame)", "Hn Ht M (segment)", "M Hl Hn Ht (datagram)"], "a", "Đi xuống mỗi tầng thêm header phía trước: message M → segment Ht M → datagram Hn Ht M → frame Hl Hn Ht M.", F + " tr.27", "c1-trap-pdu"),
    M("C1-12", "single", "Theo sơ đồ đóng gói, switch và router lần lượt xử lý gói tới tầng nào?", ["Switch: tầng liên kết; router: tầng mạng", "Switch: tầng mạng; router: tầng liên kết", "Cả hai: tầng giao vận", "Switch: tầng ứng dụng; router: tầng vật lý"], "a", "Sơ đồ tr.27: switch có tầng liên kết + vật lý; router có thêm tầng mạng.", F + " tr.27", "c1-mohinh"),
    M("C1-13", "single", "Hai chức năng chính của mạng lõi là chuyển tiếp (forwarding) và định tuyến (routing). Phát biểu nào đúng?", ["Chuyển tiếp: chuyển gói từ đầu vào tới đầu ra phù hợp của router theo bảng chuyển tiếp; định tuyến: xác định đường đi từ nguồn đến đích bằng giải thuật", "Chuyển tiếp xác định toàn bộ đường đi; định tuyến chỉ đọc header", "Hai chức năng giống nhau", "Định tuyến do host thực hiện"], "a",
      "Tr.41: bảng chuyển tiếp cục bộ ánh xạ giá trị header → liên kết ra; giải thuật định tuyến xác định tuyến đường.", F + " tr.41", "c1-sosanh"),
    M("C1-14", "single", "Khi nào gói tin bị mất tại router?", ["Khi gói đến hàng đợi mà bộ đệm đã đầy", "Khi trễ lan truyền lớn hơn 1 ms", "Khi gói có TTL bằng 64", "Khi liên kết là cáp quang"], "a", "Bộ đệm có dung lượng hữu hạn; đầy thì gói đến bị bỏ.", F + " tr.42, 53, 57", "c1-trap-loss"),
    M("C1-15", "single", "Thành phần trễ nào gồm việc kiểm tra lỗi bit và xác định liên kết ra, thường nhỏ hơn mili giây?", ["d_proc (xử lý)", "d_queue (hàng đợi)", "d_trans (truyền)", "d_prop (lan truyền)"], "a", "Tr.54.", F + " tr.54", "c1-delay"),
    M("C1-16", "single", "Trễ hàng đợi d_queue phụ thuộc chủ yếu vào:", ["Mức độ tắc nghẽn tại router", "Chiều dài cáp", "Tốc độ ánh sáng", "Kích thước màn hình"], "a", "d_queue = thời gian chờ tại đầu ra liên kết, phụ thuộc mức tắc nghẽn.", F + " tr.54", "c1-delay"),
    M("C1-17", "single", "Gói tin dài 1500 byte được đẩy lên liên kết 10 Mbps. Trễ truyền d_trans là:", ["1,2 ms", "0,15 ms", "12 ms", "1,5 s"], "a", "L = 1500×8 = 12 000 bit; d_trans = L/R = 12 000 / 10<sup>7</sup> = 1,2×10<sup>-3</sup> s.", F + " tr.55", "c1-trap-unit"),
    M("C1-18", "single", "Liên kết dài 2000 km, tốc độ lan truyền 2×10<sup>8</sup> m/s. Trễ lan truyền d_prop là:", ["10 ms", "1 ms", "100 ms", "0,1 ms"], "a", "d_prop = d/s = 2×10<sup>6</sup> m / 2×10<sup>8</sup> m/s = 0,01 s.", F + " tr.55", "c1-trap-dist"),
    M("C1-19", "single", "Server gửi file cho client qua hai liên kết nối tiếp R<sub>s</sub> = 2 Mbps và R<sub>c</sub> = 1 Mbps. Thông lượng trung bình đầu-cuối là:", ["1 Mbps", "2 Mbps", "3 Mbps", "1,5 Mbps"], "a", "Thông lượng = min(R<sub>s</sub>, R<sub>c</sub>); liên kết 1 Mbps là nút cổ chai.", F + " tr.58–59", "c1-trap-thr"),
    M("C1-20", "single", "Chương trình traceroute đo độ trễ tới router thứ i bằng cách:", ["Gửi 3 gói thăm dò có trường thời gian sống bằng i; router i gửi phản hồi và bên gửi đo thời gian", "Gửi 1 gói với TTL = 255 tới đích", "Hỏi DNS về độ trễ", "Gửi gói tới mọi router cùng lúc"], "a", "Tr.56.", F + " tr.56", "c1-loss"),
    M("C1-21", "single", "Điểm mà nhiều ISP kết nối với nhau để trao đổi lưu lượng gọi là:", ["IXP (Internet exchange point)", "Mạng truy nhập", "Host", "Gateway mặc định"], "a", "Tr.48: IXP và peering link.", F + " tr.48–51", "c1-isp"),
    M("C1-22", "single", "Khác biệt giữa virus và sâu mạng (worm) là:", ["Virus lây khi người nhận thực thi đối tượng (vd tệp đính kèm); worm lây qua đối tượng nhận thụ động và tự thực thi", "Worm chỉ lây qua email, virus qua mạng", "Virus không tự sao chép", "Hai loại giống nhau"], "a", "Tr.66.", F + " tr.66", "c1-sosanh"),
    M("C1-23", "single", "Kẻ tấn công gửi gói tin với địa chỉ nguồn sai. Đây là:", ["Giả mạo địa chỉ IP (IP spoofing)", "Bắt gói tin (sniffing)", "Tấn công từ chối dịch vụ (DoS)", "Botnet"], "a", "Tr.69: IP spoofing.", F + " tr.67–69", "c1-sosanh"),
]
