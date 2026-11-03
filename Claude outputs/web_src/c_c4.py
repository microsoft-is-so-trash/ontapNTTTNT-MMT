from h import *


def M(*a, **k):
    k["mon"] = "MMT"
    return Q(*a, **k)


F = "chuong 4 v1.pdf"

POS = dict(u=(50, 130), v=(210, 40), w=(210, 130), x=(210, 222), y=(390, 80), z=(540, 160))
EDGES = [("u", "v", 7), ("u", "w", 3), ("u", "x", 5), ("w", "v", 3), ("w", "x", 4), ("w", "y", 8), ("v", "y", 4), ("x", "y", 7), ("x", "z", 9), ("y", "z", 2)]
TREE = {("u", "w"), ("w", "v"), ("u", "x"), ("v", "y"), ("y", "z")}


def graph_svg():
    s = '<svg viewBox="0 0 600 260" width="600" role="img" aria-label="Đồ thị ví dụ Dijkstra">'
    for a, b, cst in EDGES:
        (x1, y1), (x2, y2) = POS[a], POS[b]
        t = (a, b) in TREE
        s += '<line x1="%d" y1="%d" x2="%d" y2="%d" class="%s"/>' % (x1, y1, x2, y2, "lna" if t else "ln")
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s += '<rect x="%d" y="%d" width="18" height="16" rx="3" style="fill:var(--bg)"/><text x="%d" y="%d" font-size="12" text-anchor="middle" font-weight="%s">%d</text>' % (mx - 9, my - 9, mx, my + 4, "700" if t else "400", cst)
    for n, (x, y) in POS.items():
        s += '<circle cx="%d" cy="%d" r="15" class="%s"/><text x="%d" y="%d" text-anchor="middle" class="mono" font-size="13" %s>%s</text>' % (x, y, "nodea" if n == "u" else "node", x, y + 4, 'style="fill:#fff"' if n == "u" else "", n)
    s += '<text x="300" y="252" font-size="12" class="muted" text-anchor="middle">Nét đậm = cây đường đi ngắn nhất từ u (kết quả bảng Dijkstra tr.51)</text>'
    return s + '</svg>'


P = {}
P["y"] = """<p>Tầng mạng đưa <b>datagram</b> từ host nguồn tới host đích qua nhiều router. Hai chức năng: <b>chuyển tiếp</b> (forwarding, cục bộ trong từng router — <b>mặt phẳng dữ liệu</b>) và <b>định tuyến</b> (routing, chọn đường toàn mạng — <b>mặt phẳng điều khiển</b>). Internet dùng giao thức <b>IP</b> (định dạng datagram, địa chỉ), <b>ICMP</b> (báo lỗi) và các giao thức định tuyến <b>RIP, OSPF</b> (trong AS) và <b>BGP</b> (giữa các AS).</p>
<p>Ví dụ chuyến đi: định tuyến = lập kế hoạch đường đi từ nguồn đến đích; chuyển tiếp = đi qua một giao điểm.</p>""" + src(F + " tr.4–6, 19")

P["mohinh"] = """<h3 id="c4-planes">Hai mặt phẳng</h3>""" + table(["", "Mặt phẳng dữ liệu", "Mặt phẳng điều khiển"], [
    ["Phạm vi", "cục bộ, trong từng router", "logic toàn mạng"], ["Việc", "datagram đến cổng vào → cổng ra nào (theo bảng chuyển tiếp)", "datagram đi qua những router nào từ nguồn tới đích"],
    ["Thực hiện", "phần cứng, cỡ <b>nano giây</b>", "phần mềm (bộ xử lý định tuyến), cỡ <b>mili giây</b>"],
    ["Cách tổ chức", "—", "truyền thống: thuật toán chạy <b>trên mỗi router</b> · <b>SDN</b>: bộ điều khiển từ xa (trên server) tính và cài bảng chuyển tiếp"]]) + flow(["Cổng vào: vật lý → liên kết → tra bảng chuyển tiếp, xếp hàng", "Switching fabric (memory / bus / crossbar)", "Cổng ra: xếp hàng (đệm), lập lịch → liên kết → vật lý"], active=(1,)) + """
<h3 id="c4-graph">Đồ thị định tuyến và Dijkstra</h3>""" + diagram(graph_svg(), "Ví dụ Dijkstra từ nút u (chuong 4 tr.51)") + table(["Bước", "N'", "D(v),p(v)", "D(w),p(w)", "D(x),p(x)", "D(y),p(y)", "D(z),p(z)"], [
    ["0", "u", "7,u", "<b>3,u</b>", "5,u", "∞", "∞"], ["1", "uw", "6,w", "", "<b>5,u</b>", "11,w", "∞"], ["2", "uwx", "<b>6,w</b>", "", "", "11,w", "14,x"],
    ["3", "uwxv", "", "", "", "<b>10,v</b>", "14,x"], ["4", "uwxvy", "", "", "", "", "<b>12,y</b>"], ["5", "uwxvyz", "", "", "", "", ""]]) + "<p>Đường ngắn nhất u→z: lần ngược nút trước z ← y ← v ← w ← u, tức <b>u–w–v–y–z, chi phí 12</b>. Bảng chuyển tiếp của u: tới v, y, z đi qua <b>w</b>; tới x đi thẳng.</p>" + src(F + " tr.45–51")

P["bang"] = """<h3 id="c4-router">Kiến trúc router</h3>""" + table(["Thành phần", "Đặc điểm"], [
    ["Cổng vào", "chuyển mạch <b>không tập trung</b>: biết đích → tìm cổng ra bằng bảng chuyển tiếp lưu ở cổng vào, xử lý theo “tốc độ dòng”; <b>xếp hàng</b> nếu datagram đến nhanh hơn tốc độ fabric"],
    ["Fabric: memory", "thế hệ đầu, CPU điều khiển, gói sao chép vào bộ nhớ hệ thống; giới hạn bởi băng thông bộ nhớ"],
    ["Fabric: bus", "bus chung từ bộ nhớ cổng vào tới cổng ra; tranh chấp bus, giới hạn bởi băng thông bus (Cisco 5600: 32 Gbps)"],
    ["Fabric: crossbar / mạng kết nối", "chuyển mạch đa tầng n×n từ các chuyển mạch nhỏ; có thể cắt datagram thành cell cố định (Cisco 12000: 60 Gbps)"],
    ["Tốc độ fabric", "N đầu vào → nên bằng N lần tốc độ dòng"],
    ["Cổng ra", "đệm khi datagram từ fabric tới nhanh hơn tốc độ truyền; bộ lập lịch chọn datagram để gửi"]]) + src(F + " tr.11–17") + """
<h3 id="c4-ip">IPv4 datagram</h3>""" + table(["Trường", "Ý nghĩa"], [
    ["ver · head len · type of service · length", "phiên bản · độ dài header (byte) · loại dịch vụ · tổng chiều dài datagram (byte)"],
    ["16-bit identifier · flgs · fragment offset", "dùng cho phân mảnh/tập hợp lại"],
    ["time to live (TTL)", "số hop tối đa còn lại, <b>giảm 1 tại mỗi router</b>"], ["upper layer", "giao thức tầng trên (TCP hoặc UDP)"],
    ["header checksum", "kiểm tra lỗi header"], ["source / destination IP", "32 bit mỗi địa chỉ"], ["options", "timestamp, ghi đường đi…"]]) + "<p>Overhead: 20 byte TCP + 20 byte IP = <b>40 byte</b> + header tầng ứng dụng.</p>" + src(F + " tr.20") + """
<h3 id="c4-addr">Địa chỉ IPv4, subnet, CIDR</h3>""" + ul([
    "Địa chỉ IP: <b>32 bit</b> định danh một <b>giao diện</b> (interface) của host/router. Router có nhiều giao diện; host thường 1–2 (Ethernet, 802.11). Ví dụ 223.1.1.1 = 11011111 00000001 00000001 00000001.",
    "<b>Subnet</b>: các giao diện có cùng phần subnet (bit cao) của địa chỉ, tới được nhau <b>không qua router</b>. Cách xác định: tách mỗi giao diện khỏi host/router, mỗi “đảo” còn lại là một subnet. Mặt nạ /24.",
    "Phân lớp A, B, C, D, E cứng nhắc → <b>lãng phí</b> không gian địa chỉ. <b>CIDR</b>: a.b.c.d/x, x = số bit phần subnet, độ dài tuỳ ý (vd 200.23.16.0/23).",
    "ISP lấy khối địa chỉ từ <b>ICANN</b> (phân bổ địa chỉ, quản lý DNS, gán tên miền)."]) + table(["Với a.b.c.d/x", "Cách tính (bài tính)"], [
    ["Số địa chỉ trong khối", "2<sup>32−x</sup>"], ["Số host dùng được", "2<sup>32−x</sup> − 2 (trừ địa chỉ mạng và broadcast)"],
    ["Địa chỉ mạng", "giữ x bit đầu, các bit host = 0"], ["Địa chỉ broadcast", "giữ x bit đầu, các bit host = 1"],
    ["Ví dụ 192.168.10.77/26", "khối 64 địa chỉ → mạng 192.168.10.64, broadcast 192.168.10.127, 62 host"]]) + src(F + " tr.21–27, 29; cách tính theo bảng bài tính của kế hoạch") + """
<h3 id="c4-nat">DHCP, NAT, ICMP</h3>""" + ul([
    "<b>DHCP</b>: host mới (DHCP client) cần địa chỉ trong mạng thì xin từ DHCP server (thường nằm ở router). 4 thông điệp theo giáo trình: DISCOVER → OFFER → REQUEST → ACK (slide chỉ có sơ đồ kịch bản).",
    "<b>NAT</b>: mạng nhà 10.0.0/24 dùng địa chỉ riêng; <b>mọi datagram đi ra</b> có cùng địa chỉ nguồn NAT 138.76.29.7 với <b>số cổng nguồn khác nhau</b>; trong mạng cục bộ datagram dùng địa chỉ 10.0.0.x.",
    "<b>ICMP</b>: báo lỗi và yêu cầu/đáp ứng, mang trong IP datagram, gồm type, code + 8 byte đầu datagram gây lỗi. 0/0 echo reply · 8/0 echo request (ping) · 3/0..3 network/host/protocol/<b>port unreachable</b> · <b>11/0 TTL expired</b> · 12/0 bad IP header.",
    "<b>Traceroute</b>: gửi UDP segment TTL = 1, 2, …; router thứ n bỏ datagram và gửi ICMP <b>type 11 code 0</b> (kèm tên, IP router); tới đích thì đích trả ICMP <b>port unreachable (3/3)</b> → dừng."]) + src(F + " tr.28, 30–32") + """
<h3 id="c4-v6">IPv6</h3>""" + ul([
    "Lý do: hết không gian 32 bit; header cố định giúp xử lý nhanh, hỗ trợ QoS.",
    "Header <b>cố định 40 byte</b>, địa chỉ <b>128 bit</b>, trường priority, <b>flow label</b>, next header, hop limit.",
    "<b>Không phân mảnh</b> tại router, <b>bỏ checksum</b>, options nằm ngoài header (qua Next Header), ICMPv6 (vd “Packet Too Big”).",
    "<b>Tunneling</b>: không thể nâng cấp mọi router cùng lúc → IPv6 datagram được mang làm <b>payload</b> trong IPv4 datagram giữa các router IPv4 (B→C, D→E)."]) + src(F + " tr.33–38") + """
<h3 id="c4-algo">Thuật toán định tuyến</h3>""" + table(["", "Link state (Dijkstra)", "Distance vector (Bellman-Ford)"], [
    ["Thông tin", "<b>tập trung</b>: mọi router biết toàn bộ cấu trúc và chi phí (quảng bá trạng thái liên kết)", "<b>không tập trung</b>: chỉ biết hàng xóm và chi phí tới hàng xóm; lặp, trao đổi với hàng xóm"],
    ["Công thức", "D(v) = min(D(v), D(w) + c(w,v)); sau k vòng biết chi phí thấp nhất tới k đích", "d<sub>x</sub>(y) = min<sub>v</sub>{ c(x,v) + d<sub>v</sub>(y) }; v đạt min là hop kế tiếp"],
    ["Giao thức", "OSPF, IS-IS", "RIP"]]) + note("Ví dụ Bellman-Ford tr.54: c(u,v)=2, c(u,x)=1, c(u,w)=5; d<sub>v</sub>(z)=5, d<sub>x</sub>(z)=3, d<sub>w</sub>(z)=3 → d<sub>u</sub>(z) = min{2+5, 1+3, 5+3} = <b>4</b>, hop kế tiếp là x.") + "<p>Phân loại khác: <b>tĩnh</b> (đổi chậm) vs <b>động</b> (cập nhật định kỳ, phản ứng thay đổi chi phí).</p>" + src(F + " tr.47–54") + """
<h3 id="c4-inet">Định tuyến trên Internet</h3>""" + table(["Giao thức", "Đặc điểm"], [
    ["Phân cấp (AS)", "router gom thành <b>hệ thống tự trị (AS)</b>; trong AS chạy cùng giao thức intra-AS (IGP); <b>gateway router</b> ở cạnh AS nối sang AS khác. Bảng chuyển tiếp do cả intra- và inter-AS cấu hình"],
    ["RIP", "distance vector; độ đo = <b>số hop</b> (mỗi liên kết = 1, <b>tối đa 15</b>); trao đổi DV mỗi <b>30 s</b> (advertisement, tối đa 25 subnet); 180 s không nghe → lân cận chết; <b>poison reverse</b> (vô hạn = 16) chống vòng lặp ping-pong"],
    ["OSPF", "link state + Dijkstra; quảng bá (flooding) toàn AS; mang <b>trực tiếp trên IP</b>; cải tiến so với RIP: xác thực, nhiều đường cùng chi phí, nhiều độ đo theo TOS, multicast (MOSPF), <b>phân cấp 2 mức</b>: vùng cục bộ + vùng xương sống (router biên vùng, router xương sống, router biên AS)"],
    ["BGP", "định tuyến liên miền (inter-AS) thực tế; <b>eBGP</b> lấy thông tin tới subnet từ AS lân cận, <b>iBGP</b> lan truyền trong AS; giao thức <b>path vector</b>, qua <b>kết nối TCP</b> bán bền vững; thuộc tính <b>AS-PATH</b>, <b>NEXT-HOP</b>; import policy; chọn tuyến: ① local preference ② AS-PATH ngắn nhất ③ NEXT-HOP gần nhất (hot potato) ④ tiêu chí khác; thông điệp OPEN, UPDATE, KEEPALIVE, NOTIFICATION"],
    ["Vì sao intra ≠ inter", "chính sách (inter: kiểm soát ai đi qua mạng mình) · quy mô (phân cấp giảm bảng và lưu lượng cập nhật) · hiệu năng (intra tập trung hiệu năng, inter chính sách quan trọng hơn)"]]) + src(F + " tr.56–74")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["Forwarding vs routing", "cục bộ, mặt phẳng dữ liệu, ns vs toàn mạng, mặt phẳng điều khiển, ms."],
    ["Điều khiển trên mỗi router vs SDN", "thuật toán định tuyến chạy trong từng router vs bộ điều khiển từ xa tính và cài bảng chuyển tiếp."],
    ["Best effort vs ATM CBR", "Internet không đảm bảo băng thông, mất mát, thứ tự, thời gian; ATM CBR đảm bảo tốc độ ổn định, không mất, đúng thứ tự, thời gian."],
    ["Memory vs bus vs crossbar", "giới hạn bởi băng thông bộ nhớ (CPU sao chép) · tranh chấp bus · mạng kết nối song song, nhanh nhất."],
    ["Link state vs distance vector", "toàn cục + Dijkstra vs hàng xóm + Bellman-Ford lặp."],
    ["RIP vs OSPF", "DV, số hop ≤ 15, 30 s, một tuyến vs LS, Dijkstra, flooding, xác thực, nhiều tuyến cùng chi phí, phân vùng."],
    ["Intra-AS vs inter-AS", "IGP (RIP, OSPF, IGRP) trong AS, tập trung hiệu năng vs BGP giữa các AS, theo chính sách."],
    ["eBGP vs iBGP", "giữa router của hai AS khác nhau vs lan truyền trong cùng AS."],
    ["IPv4 vs IPv6", "32 vs 128 bit; header biến đổi (≥ 20 byte) vs cố định 40 byte; có vs không phân mảnh tại router; có vs không checksum."],
    ["Địa chỉ riêng vs địa chỉ NAT", "10.0.0.x dùng trong mạng nhà; ra ngoài thay bằng một IP công khai + cổng khác nhau."],
]) + src(F + " tr.4–9, 13–16, 33–35, 47, 61–74")

P["bay"] = trap("Bẫy 1 — số host", "/24 có 256 địa chỉ nhưng <b>254</b> host (trừ mạng và broadcast). /23 (200.23.16.0/23) → 512 địa chỉ, 510 host. /30 → 2 host.", "c4-trap-host") + \
    trap("Bẫy 2 — đếm subnet", "Ba router nối nhau từng cặp (3 liên kết điểm-điểm) và mỗi router nối một LAN → <b>6 subnet</b> (mỗi liên kết giữa hai router cũng là một subnet).", "c4-trap-subnet") + \
    trap("Bẫy 3 — Dijkstra cập nhật sai", "Chỉ cập nhật D(v) cho nút <b>kề với w vừa thêm</b> và <b>chưa thuộc N'</b>; chọn nút có D nhỏ nhất <b>ngoài N'</b>. Hoà nhau thì chọn tuỳ ý.", "c4-trap-dij") + \
    trap("Bẫy 4 — traceroute dừng khi nào", "Router trung gian trả ICMP <b>11/0 (TTL expired)</b>; host đích trả <b>3/3 (port unreachable)</b> vì UDP gửi tới cổng không có → nguồn dừng.", "c4-trap-icmp") + \
    trap("Bẫy 5 — RIP vô hạn = 16", "Đường tối đa 15 hop; 16 nghĩa là không tới được (dùng trong poison reverse).", "c4-trap-rip") + \
    trap("Bẫy 6 — OSPF không chạy trên TCP/UDP", "Thông điệp OSPF mang <b>trực tiếp trên IP</b>; BGP thì chạy trên <b>TCP</b>.", "c4-trap-ospf") + \
    trap("Bẫy 7 — IPv6 không phân mảnh, không checksum", "Router IPv6 không phân mảnh (gói quá lớn → ICMPv6 “Packet Too Big”); checksum bị bỏ để giảm xử lý tại mỗi hop.", "c4-trap-v6")

P["checklist"] = [
    "Forwarding (cục bộ, data plane) và routing (toàn mạng, control plane); control plane truyền thống so với SDN",
    "Các mô hình dịch vụ tầng mạng (best effort, ATM CBR/ABR…)",
    "Kiến trúc router: cổng vào, switching fabric (bộ nhớ, bus, mạng kết nối), cổng ra, hàng đợi, HOL blocking; longest prefix match — <i>slide v1 không nêu HOL blocking và longest prefix match (xem Đọc thêm)</i>",
    "IPv4 datagram: TTL, protocol, checksum, phân mảnh (ID, flag, offset tính theo đơn vị 8 byte) — <i>slide chỉ nêu các trường; cách tính offset có trong Bài tính MMT</i>",
    "Địa chỉ IPv4: subnet, CIDR a.b.c.d/x, tính địa chỉ mạng, broadcast, số host; chia subnet; DHCP (DISCOVER, OFFER, REQUEST, ACK); NAT; tổng quan IPv6 và tunneling",
    "Thuật toán định tuyến: link state (Dijkstra, chạy tay được bảng) và distance vector (Bellman-Ford, count-to-infinity, poisoned reverse); định tuyến phân cấp, AS",
    "Định tuyến trên Internet: RIP (DV, số hop, tối đa 15), OSPF (LS, phân vùng area), BGP (giữa các AS, eBGP/iBGP, chính sách)",
    "＋ ICMP type/code và traceroute (11/0, 3/3)",
    "＋ BGP: AS-PATH, NEXT-HOP, thứ tự chọn tuyến (local pref → AS-PATH ngắn → hot potato), 4 loại thông điệp",
    "＋ Vì sao intra-AS và inter-AS khác nhau (chính sách, quy mô, hiệu năng)",
]

P["quick"] = [
    QQ("Khối 10.1.4.0/22 có bao nhiêu host dùng được?", ["1024", "1022", "512", "254"], "b", "2<sup>10</sup> − 2 = 1022."),
    QQ("RIP dùng độ đo gì?", ["Băng thông", "Số hop (tối đa 15)", "Độ trễ", "Chính sách"], "b", "RIP: distance vector, đếm hop."),
    QQ("Giao thức định tuyến nào chạy giữa các AS?", ["RIP", "OSPF", "BGP", "ICMP"], "c", "BGP là giao thức inter-AS."),
]

P["docthem"] = ul([
    "<b>Longest prefix match</b> (Kurose &amp; Ross §4.2.1): khi nhiều mục trong bảng chuyển tiếp khớp địa chỉ đích, chọn mục có tiền tố <b>dài nhất</b>.",
    "<b>HOL blocking</b> (§4.2.4): datagram đầu hàng đợi cổng vào bị chặn (chờ cổng ra bận) làm các datagram phía sau dù đi cổng ra khác cũng phải chờ.",
    "<b>Phân mảnh IPv4</b> (§4.3.2): datagram lớn hơn MTU được cắt; các mảnh cùng ID, cờ = 1 trừ mảnh cuối, offset tính theo đơn vị <b>8 byte</b>. Ví dụ 4000 byte (20 header) qua MTU 1500 → 3 mảnh dữ liệu 1480, 1480, 1020; offset 0, 185, 370. Luyện ở Bài tính MMT.",
    "<b>Count-to-infinity</b> (§5.2.2): khi chi phí liên kết tăng, DV có thể hội tụ rất chậm (tin xấu lan chậm); poisoned reverse chỉ chữa được vòng lặp 2 nút.",
])

BLOCK = dict(id="C4", mon="MMT", title="Tầng mạng", src="chuong 4 v1.pdf", page=P)

QUESTIONS = [
    M("C4-01", "single", "Phát biểu nào phân biệt đúng chuyển tiếp (forwarding) và định tuyến (routing)?", ["Chuyển tiếp: chuyển gói từ cổng vào tới cổng ra phù hợp của một router; định tuyến: xác định đường đi từ nguồn tới đích", "Chuyển tiếp xác định đường đi toàn mạng; định tuyến là việc cục bộ", "Cả hai đều do host thực hiện", "Định tuyến chạy ở mặt phẳng dữ liệu"], "a", "Tr.4–6.", F + " tr.4–6", "c4-planes"),
    M("C4-02", "single", "Trong cách tiếp cận SDN cho mặt phẳng điều khiển:", ["Một bộ điều khiển từ xa tính toán và cài đặt bảng chuyển tiếp vào các router", "Mỗi router tự chạy thuật toán định tuyến riêng", "Không cần bảng chuyển tiếp", "Host quyết định đường đi"], "a", "Tr.6, 8, 42.", F + " tr.6–8", "c4-planes"),
    M("C4-03", "single", "Mô hình dịch vụ “best effort” của Internet đảm bảo những gì?", ["Không đảm bảo băng thông, mất mát, thứ tự hay thời gian", "Đảm bảo không mất gói", "Đảm bảo đúng thứ tự", "Đảm bảo băng thông tối thiểu"], "a", "Bảng mô hình dịch vụ tr.9; ATM CBR mới đảm bảo các yếu tố này.", F + " tr.9", "c4-sosanh"),
    M("C4-04", "single", "Trong router, chức năng định tuyến và chuyển tiếp khác nhau về cách thực hiện như thế nào?", ["Định tuyến chạy bằng phần mềm trên bộ xử lý (cỡ mili giây); chuyển tiếp chạy bằng phần cứng (cỡ nano giây)", "Cả hai chạy bằng phần cứng", "Chuyển tiếp bằng phần mềm, cỡ giây", "Định tuyến chỉ chạy ở cổng ra"], "a", "Tr.11.", F + " tr.11", "c4-planes"),
    M("C4-05", "single", "Loại switching fabric nào bị giới hạn bởi băng thông bộ nhớ vì gói phải được CPU sao chép vào bộ nhớ hệ thống?", ["Chuyển mạch qua memory", "Chuyển mạch qua bus", "Crossbar", "Mạng kết nối đa tầng"], "a", "Router thế hệ đầu; bus bị giới hạn bởi tranh chấp bus; crossbar nhanh nhất.", F + " tr.13–16", "c4-router"),
    M("C4-06", "single", "Việc đệm (xếp hàng) tại cổng ra cần thiết khi:", ["Datagram từ fabric đến nhanh hơn tốc độ truyền của liên kết ra", "Bảng chuyển tiếp rỗng", "TTL bằng 0", "Gói có lỗi checksum"], "a", "Bộ lập lịch chọn datagram trong hàng đợi để truyền (tr.17).", F + " tr.17", "c4-router"),
    M("C4-07", "single", "Trường time to live (TTL) trong IPv4 datagram:", ["Là số hop tối đa còn lại, bị giảm tại mỗi router", "Là thời gian sống tính bằng giây ở host đích", "Xác định giao thức tầng trên", "Dùng để tập hợp các mảnh"], "a", "Tr.20.", F + " tr.20", "c4-ip"),
    M("C4-08", "single", "Một TCP segment mang trong IPv4 datagram (không có options). Tổng phần header của TCP và IP là:", ["40 byte", "20 byte", "28 byte", "60 byte"], "a", "20 byte TCP + 20 byte IP = 40 byte + header tầng ứng dụng.", F + " tr.20", "c4-ip"),
    M("C4-09", "single", "Địa chỉ IP được gán cho:", ["Từng giao diện (interface) của host hoặc router", "Từng host, mỗi host đúng một địa chỉ", "Từng router, mỗi router một địa chỉ", "Từng ứng dụng"], "a", "Router thường có nhiều giao diện, mỗi giao diện một địa chỉ (tr.21).", F + " tr.21", "c4-addr"),
    M("C4-10", "single", "Các giao diện thuộc cùng một subnet có đặc điểm gì?", ["Có cùng phần subnet của địa chỉ IP và tới được nhau mà không cần router", "Có cùng địa chỉ IP", "Phải đi qua ít nhất một router", "Có cùng địa chỉ MAC"], "a", "Tr.23.", F + " tr.23–24", "c4-addr"),
    M("C4-11", "single", "Ba router nối với nhau từng cặp bằng ba liên kết điểm-điểm, mỗi router còn nối với một LAN riêng. Mạng có bao nhiêu subnet?", ["6", "3", "4", "9"], "a", "3 LAN + 3 liên kết router–router (mỗi liên kết cũng là một subnet) — ví dụ “Có bao nhiêu subnet?” tr.25.", F + " tr.24–25", "c4-trap-subnet"),
    M("C4-12", "single", "Khối CIDR 200.23.16.0/23 chứa bao nhiêu địa chỉ host dùng được?", ["510", "512", "254", "1022"], "a", "Phần host có 32 − 23 = 9 bit → 2<sup>9</sup> = 512 địa chỉ, trừ địa chỉ mạng và broadcast → 510.", F + " tr.27; bảng bài tính", "c4-trap-host"),
    M("C4-13", "single", "Host có địa chỉ 192.168.10.77/26. Địa chỉ mạng và địa chỉ broadcast của subnet này là:", ["192.168.10.64 và 192.168.10.127", "192.168.10.0 và 192.168.10.255", "192.168.10.77 và 192.168.10.127", "192.168.10.64 và 192.168.10.128"], "a", "/26 → khối 64 địa chỉ; 77 nằm trong khối 64–127. Mạng: bit host = 0 → .64; broadcast: bit host = 1 → .127.", F + " tr.27 (CIDR); cách tính theo bảng bài tính", "c4-addr"),
    M("C4-14", "single", "Với NAT ở mạng nhà 10.0.0/24, router có địa chỉ công khai 138.76.29.7. Các datagram đi ra Internet có đặc điểm:", ["Cùng địa chỉ IP nguồn 138.76.29.7 nhưng số cổng nguồn khác nhau", "Giữ nguyên địa chỉ nguồn 10.0.0.x", "Mỗi host có một IP công khai riêng", "Không có cổng nguồn"], "a", "Tr.30.", F + " tr.30", "c4-nat"),
    M("C4-15", "single", "Khi traceroute gửi UDP segment có TTL = n tới router thứ n, router đó:", ["Bỏ datagram và gửi về nguồn thông điệp ICMP type 11 code 0 (TTL expired)", "Chuyển tiếp bình thường", "Gửi ICMP port unreachable (type 3 code 3)", "Gửi ICMP echo reply"], "a", "Tới host đích mới nhận được ICMP 3/3 port unreachable và nguồn dừng (tr.32).", F + " tr.31–32", "c4-trap-icmp"),
    M("C4-16", "single", "So với IPv4, header IPv6:", ["Có độ dài cố định 40 byte, không cho phân mảnh tại router và bỏ checksum", "Dài 20 byte và có checksum", "Có trường fragment offset", "Dùng địa chỉ 64 bit"], "a", "Tr.33–35: địa chỉ 128 bit, flow label, next header.", F + " tr.33–35", "c4-trap-v6"),
    M("C4-17", "single", "Tunneling trong chuyển đổi IPv4 sang IPv6 nghĩa là:", ["IPv6 datagram được mang làm payload trong IPv4 datagram khi đi qua các router IPv4", "Đổi mọi router sang IPv6 trong một ngày", "Dịch địa chỉ IPv6 sang IPv4 bằng NAT", "Chia IPv6 datagram thành các mảnh IPv4"], "a", "Tr.36–38.", F + " tr.36–38", "c4-v6"),
    M("C4-18", "single", "Khác biệt giữa giải thuật link state và distance vector là:", ["Link state: mọi router biết toàn bộ cấu trúc mạng và chi phí (Dijkstra); distance vector: router chỉ biết hàng xóm và lặp trao đổi (Bellman-Ford)", "Link state dùng Bellman-Ford", "Distance vector cần thông tin toàn cục", "Hai loại giống nhau"], "a", "Tr.47.", F + " tr.47", "c4-algo"),
    M("C4-19", "single", "Đồ thị: u–v 7, u–w 3, u–x 5, w–v 3, w–x 4, w–y 8, v–y 4, x–y 7, x–z 9, y–z 2. Chạy Dijkstra từ u, chi phí thấp nhất u→z và đường đi là:", ["12, u–w–v–y–z", "14, u–x–z", "11, u–w–y–z", "13, u–w–y–z"], "a", "Bảng tr.51: D(z) = 12 với p(z) = y; lần ngược y ← v ← w ← u.", F + " tr.51", "c4-graph"),
    M("C4-20", "single", "Cho c(u,v) = 2, c(u,x) = 1, c(u,w) = 5 và d<sub>v</sub>(z) = 5, d<sub>x</sub>(z) = 3, d<sub>w</sub>(z) = 3. Theo Bellman-Ford, d<sub>u</sub>(z) và hop kế tiếp là:", ["4, qua x", "7, qua v", "8, qua w", "3, qua x"], "a", "min{2+5, 1+3, 5+3} = 4, đạt tại x.", F + " tr.53–54", "c4-algo"),
    M("C4-21", "single", "Phát biểu nào đúng về RIP?", ["Dùng distance vector, độ đo là số hop (tối đa 15), trao đổi thông báo mỗi 30 giây; dùng poison reverse với vô hạn = 16", "Dùng link state và Dijkstra", "Chạy giữa các AS", "Độ đo là băng thông"], "a", "Tr.62–63.", F + " tr.62–63", "c4-trap-rip"),
    M("C4-22", "single", "Đặc tính nào có ở OSPF mà không có ở RIP?", ["Xác thực thông điệp, cho phép nhiều đường cùng chi phí và phân cấp thành các vùng", "Đếm số hop tối đa 15", "Trao đổi DV với hàng xóm mỗi 30 giây", "Chạy trên TCP"], "a", "OSPF mang trực tiếp trên IP, flooding toàn AS (tr.64–67).", F + " tr.64–67", "c4-inet"),
    M("C4-23", "single", "Trong BGP, iBGP được dùng để:", ["Lan truyền thông tin đến subnet tới tất cả router bên trong cùng một AS", "Lấy thông tin đến subnet từ AS lân cận", "Tính đường ngắn nhất bằng Dijkstra", "Gửi thông báo ICMP"], "a", "eBGP: giữa các AS lân cận; iBGP: trong AS (tr.68–70).", F + " tr.68–70", "c4-sosanh"),
    M("C4-24", "single", "Router BGP học được nhiều tuyến tới cùng một prefix. Tiêu chí được xét đầu tiên là:", ["Thuộc tính giá trị ưu tiên cục bộ (quyết định chính sách)", "AS-PATH ngắn nhất", "NEXT-HOP gần nhất (hot potato)", "Số hop RIP"], "a", "Thứ tự: local preference → AS-PATH ngắn nhất → NEXT-HOP gần nhất → tiêu chí bổ sung (tr.72).", F + " tr.71–72", "c4-inet"),
]
