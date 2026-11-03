from h import *


def M(*a, **k):
    k["mon"] = "MMT"
    return Q(*a, **k)


F = "chuong 3 Tang giao van.pdf"

HS = """<svg viewBox="0 0 700 330" width="700" role="img" aria-label="Bắt tay 3 bước và đóng kết nối TCP">
<g font-size="12.5">
<text x="70" y="16" font-weight="700">client</text><text x="560" y="16" font-weight="700">server</text>
<line x1="100" y1="24" x2="100" y2="322" class="ln dash"/><line x1="590" y1="24" x2="590" y2="322" class="ln dash"/>
<text x="10" y="40" class="mono" font-size="11">LISTEN</text><text x="600" y="40" class="mono" font-size="11">LISTEN</text>
<path d="M100 50 L586 80" class="lna"/><path d="M580 74 l7 6 l-9 2" class="lna"/><text x="220" y="56" class="mono">SYNbit=1, Seq=x</text>
<text x="10" y="58" class="mono" font-size="11">SYNSENT</text><text x="600" y="86" class="mono" font-size="11">SYN RCVD</text>
<path d="M590 92 L104 122" class="lna"/><path d="M112 116 l-8 6 l9 2" class="lna"/><text x="250" y="100" class="mono">SYNbit=1, Seq=y · ACKbit=1, ACKnum=x+1</text>
<text x="10" y="128" class="mono" font-size="11">ESTAB</text>
<path d="M100 132 L586 162" class="lna"/><path d="M580 156 l7 6 l-9 2" class="lna"/><text x="250" y="140" class="mono">ACKbit=1, ACKnum=y+1 (có thể kèm dữ liệu)</text>
<text x="600" y="168" class="mono" font-size="11">ESTAB</text>
<path d="M100 196 L586 214" class="ln"/><path d="M580 208 l7 6 l-9 2" class="ln"/><text x="250" y="198" class="mono">FINbit=1, seq=x</text><text x="10" y="200" class="mono" font-size="11">FIN_WAIT_1</text>
<path d="M590 220 L104 238" class="ln"/><path d="M112 232 l-8 6 l9 2" class="ln"/><text x="300" y="224" class="mono">ACKbit=1; ACKnum=x+1</text><text x="600" y="224" class="mono" font-size="11">CLOSE_WAIT</text>
<text x="10" y="244" class="mono" font-size="11">FIN_WAIT_2</text>
<path d="M590 256 L104 274" class="ln"/><path d="M112 268 l-8 6 l9 2" class="ln"/><text x="300" y="260" class="mono">FINbit=1, seq=y</text><text x="600" y="260" class="mono" font-size="11">LAST_ACK</text>
<text x="10" y="282" class="mono" font-size="11">TIMED_WAIT</text>
<path d="M100 288 L586 306" class="ln"/><path d="M580 300 l7 6 l-9 2" class="ln"/><text x="250" y="290" class="mono">ACKbit=1; ACKnum=y+1</text><text x="600" y="312" class="mono" font-size="11">CLOSED</text>
<text x="10" y="318" font-size="11" class="muted">chờ 2 × thời gian sống tối đa của segment → CLOSED</text>
</g></svg>"""


def cwnd_svg():
    reno = [1, 2, 4, 8, 9, 10, 11, 12, 6, 7, 8, 9, 10, 11]
    tahoe = [1, 2, 4, 8, 9, 10, 11, 12, 1, 2, 4, 6, 7, 8]
    X = lambda i: 50 + i * 44
    Y = lambda v: 250 - v * 17
    s = '<svg viewBox="0 0 700 330" width="700" role="img" aria-label="Đồ thị cwnd TCP Tahoe và Reno">'
    s += '<line x1="50" y1="250" x2="680" y2="250" class="ln"/><line x1="50" y1="250" x2="50" y2="20" class="ln"/>'
    for v in (2, 4, 6, 8, 10, 12):
        s += '<text x="30" y="%d" font-size="11" class="muted">%d</text><line x1="46" y1="%d" x2="680" y2="%d" stroke="currentColor" stroke-opacity=".08"/>' % (Y(v) + 4, v, Y(v), Y(v))
    for i in range(14):
        s += '<text x="%d" y="266" font-size="11" class="muted" text-anchor="middle">%d</text>' % (X(i), i + 1)
    s += '<text x="365" y="288" font-size="12" text-anchor="middle">vòng truyền (RTT)</text><text x="8" y="14" font-size="12">cwnd (MSS)</text>'
    s += '<line x1="50" y1="%d" x2="400" y2="%d" class="ln dash"/><text x="56" y="%d" font-size="11" class="muted">ssthresh = 8</text>' % (Y(8), Y(8), Y(8) - 4)
    s += '<line x1="400" y1="%d" x2="680" y2="%d" class="ln dash"/><text x="560" y="%d" font-size="11" class="muted">ssthresh mới = 6</text>' % (Y(6), Y(6), Y(6) + 14)
    s += '<polyline fill="none" stroke="var(--bad)" stroke-width="2" points="%s"/>' % " ".join("%d,%d" % (X(i), Y(v)) for i, v in enumerate(tahoe))
    s += '<polyline fill="none" stroke="var(--acc)" stroke-width="2.4" points="%s"/>' % " ".join("%d,%d" % (X(i), Y(v)) for i, v in enumerate(reno))
    for i, v in enumerate(reno):
        s += '<circle cx="%d" cy="%d" r="3" fill="var(--acc)"/>' % (X(i), Y(v))
    s += '<text x="%d" y="%d" font-size="11.5">← 3 ACK trùng ở cwnd = 12</text>' % (X(7) + 12, Y(12) + 4)
    s += '<text x="60" y="314" font-size="12" style="fill:var(--acc)">━ TCP Reno: cwnd = ssthresh = 6</text><text x="330" y="314" font-size="12" style="fill:var(--bad)">━ TCP Tahoe: cwnd = 1 MSS rồi khởi động chậm</text>'
    s += '<text x="64" y="30" font-size="11.5" class="muted">khởi động chậm (×2)</text><text x="210" y="30" font-size="11.5" class="muted">tránh tắc nghẽn (+1 MSS/RTT)</text>'
    return s + '</svg>'


P = {}
P["y"] = """<p>Tầng giao vận cung cấp <b>truyền thông logic giữa các tiến trình</b> (tầng mạng: giữa các <b>host</b>). Bên gửi cắt thông điệp thành <b>segment</b>, bên nhận ráp lại. Internet có hai giao thức: <b>UDP</b> (không kết nối, “best effort”) và <b>TCP</b> (tin cậy, đúng thứ tự, điều khiển luồng, điều khiển tắc nghẽn, thiết lập kết nối). Không giao thức nào đảm bảo trễ hay băng thông.</p>
<p>Ví dụ nhà Ann – nhà Bill: host = ngôi nhà · tiến trình = các em bé · thông điệp = lá thư · giao thức giao vận = quy ước giữa Ann và Bill · giao thức tầng mạng = dịch vụ bưu điện.</p>""" + src(F + " tr.4–6")

P["mohinh"] = """<h3 id="c3-hs">Bắt tay 3 bước và đóng kết nối</h3>""" + diagram(HS, "chuong 3 tr.80–83") + """
<h3 id="c3-cwnd">Đồ thị cwnd</h3>""" + diagram(cwnd_svg(), "Khởi động chậm, tránh tắc nghẽn, phản ứng khi mất gói (chuong 3 tr.97–103) — số liệu minh hoạ") + """
<h3 id="c3-win">Cửa sổ Go-Back-N và Selective Repeat (N = 4, mất pkt2)</h3>""" + table(["", "Go-Back-N", "Selective Repeat"], [
    ["Bên nhận gặp pkt3, pkt4, pkt5", "<b>huỷ</b> (không đệm), gửi lại ack1 mỗi lần", "<b>đệm</b>, gửi ack3, ack4, ack5"],
    ["Bên gửi", "hết giờ → gửi lại pkt2, 3, 4, 5", "chỉ gửi lại pkt2 (timer riêng của pkt2)"],
    ["Khi pkt2 tới", "nhận pkt2…5 lần lượt, ack2…ack5", "giao pkt2, 3, 4, 5 lên trên, gửi ack2"]]) + src(F + " tr.50, 54")

P["bang"] = """<h3 id="c3-demux">Ghép kênh / phân kênh</h3>""" + table(["", "UDP (không kết nối)", "TCP (hướng kết nối)"], [
    ["Socket xác định bởi", "(IP đích, cổng đích)", "bộ 4: IP nguồn, cổng nguồn, IP đích, cổng đích"],
    ["Hệ quả", "datagram cùng cổng đích nhưng khác IP/cổng nguồn → <b>cùng một socket</b>", "server có nhiều socket đồng thời; web server mỗi kết nối client một socket (HTTP không bền: mỗi yêu cầu một socket)"]]) + "<p>Bên gửi ghép kênh: gom dữ liệu từ nhiều socket, thêm header giao vận. Bên nhận phân kênh: dùng IP + số cổng trong header để đưa segment tới đúng socket.</p>" + src(F + " tr.8–14") + """
<h3 id="c3-udp">UDP</h3>""" + ul([
    "Header 4 trường × 16 bit = <b>8 byte</b>: source port, dest port, <b>length</b> (số byte của cả segment, gồm header), checksum.",
    "Vì sao dùng: không thiết lập kết nối (đỡ trễ), không lưu trạng thái, header nhỏ, <b>không điều khiển tắc nghẽn</b> (gửi nhanh tuỳ ý). Dùng cho streaming multimedia, DNS, SNMP; muốn tin cậy thì thêm ở tầng ứng dụng.",
    "<b>Checksum</b>: coi segment là dãy số 16 bit, <b>cộng</b>, bit nhớ tràn ra ngoài thì <b>cộng vòng</b> vào bit thấp nhất (wraparound), rồi <b>đảo bit</b> (bù 1). Bên nhận tính lại: khác → có lỗi; bằng → không phát hiện lỗi (vẫn có thể có lỗi)."]) + pre("""
  1110011001100110
+ 1101010101010101
= 1 1011101110111011   (tràn 1 bit)
wraparound → 1011101110111100   (tổng)
checksum   → 0100010001000011   (đảo bit)
""", "text") + src(F + " tr.16–19") + """
<h3 id="c3-rdt">Truyền tin cậy: rdt1.0 → 3.0</h3>""" + table(["Phiên bản", "Giả thiết kênh", "Cơ chế thêm"], [
    ["rdt1.0", "hoàn toàn tin cậy", "gửi/nhận thẳng"], ["rdt2.0", "có lỗi bit", "checksum + phản hồi <b>ACK/NAK</b>, gửi lại khi NAK (dừng và chờ)"],
    ["rdt2.1", "ACK/NAK cũng có thể hỏng", "<b>số thứ tự</b> 0/1 để bên nhận bỏ gói trùng"], ["rdt2.2", "như 2.1", "<b>bỏ NAK</b>: ACK kèm số thứ tự gói nhận tốt cuối; ACK trùng = NAK"],
    ["rdt3.0", "có lỗi <b>và mất gói</b>", "<b>bộ định thời</b>: không có ACK trong thời gian “chấp nhận được” → gửi lại; gói trễ gây trùng thì số thứ tự xử lý"]]) + src(F + " tr.26–41") + """
<h3 id="c3-util">Hiệu suất dừng-và-chờ và pipeline</h3>
<p style="text-align:center;font-size:17px"><b>U<sub>sender</sub> = (L/R) / (RTT + L/R)</b> · pipeline N gói: <b>U = (N·L/R) / (RTT + L/R)</b></p>""" + note("Ví dụ slide: 1 Gbps, trễ lan truyền 15 ms (RTT 30 ms), gói 8000 bit → L/R = 8 μs; U = 0,008/30,008 = <b>0,00027</b>. Pipeline 3 gói → 0,00081. Thông lượng chỉ 33 kB/s trên đường 1 Gbps!") + src(F + " tr.42–45") + """
<h3 id="c3-tcp">TCP segment, SEQ/ACK, RTT</h3>""" + ul([
    "TCP: điểm-tới-điểm, dòng byte tin cậy đúng thứ tự (không có ranh giới thông điệp), pipeline, <b>song công</b>, MSS, hướng kết nối, điều khiển luồng.",
    "Header: cổng nguồn/đích, <b>sequence number</b>, <b>acknowledgement number</b>, cờ U A P R S F, <b>receive window</b> (rwnd), checksum, options.",
    "<b>Số thứ tự</b> = số thứ tự trong dòng byte của <b>byte đầu tiên</b> trong segment. <b>ACK</b> = số thứ tự của <b>byte tiếp theo mong đợi</b>, ACK tích lũy.",
    "Telnet: A gửi <code>Seq=42, ACK=79, data='C'</code> → B trả <code>Seq=79, ACK=43, data='C'</code> → A gửi <code>Seq=43, ACK=80</code>."]) + pre("""
EstimatedRTT    = (1 − α)·EstimatedRTT + α·SampleRTT          α = 0,125
DevRTT          = (1 − β)·DevRTT + β·|SampleRTT − EstimatedRTT|   β = 0,25
TimeoutInterval = EstimatedRTT + 4·DevRTT
""", "text") + src(F + " tr.57–63") + """
<h3 id="c3-rel">Truyền tin cậy trong TCP</h3>""" + ul([
    "Một bộ định thời cho segment chưa được ACK lâu nhất; timeout → gửi lại segment đó, khởi động lại timer.",
    "Tình huống: <b>mất ACK</b> (gửi lại Seq=92), <b>timeout sớm</b>, <b>ACK tích luỹ</b> (ACK=100 mất nhưng ACK=120 tới → không cần gửi lại).",
    "<b>Fast retransmit</b>: nhận <b>3 ACK trùng</b> cho cùng dữ liệu → gửi lại ngay segment chưa ACK có số thứ tự nhỏ nhất, không chờ timeout.",
    "Bên nhận: segment đúng thứ tự, mọi thứ trước đã ACK → <b>ACK trễ</b>, chờ 500 ms; segment sai thứ tự (lớn hơn mong đợi) → gửi ngay <b>ACK trùng</b>."]) + src(F + " tr.65–72") + """
<h3 id="c3-flow">Điều khiển luồng</h3><p>Bên nhận báo không gian đệm còn trống qua trường <b>rwnd</b>; bên gửi giới hạn dữ liệu chưa được ACK ≤ rwnd → không làm tràn bộ đệm bên nhận. RcvBuffer thường mặc định 4096 byte. Công thức (giáo trình): <b>rwnd = RcvBuffer − (LastByteRcvd − LastByteRead)</b>.</p>""" + src(F + " tr.74–75") + """
<h3 id="c3-cc">Điều khiển tắc nghẽn TCP</h3>""" + table(["Sự kiện / giai đoạn", "Hành động"], [
    ["Bắt đầu (khởi động chậm)", "cwnd = 1 MSS, <b>tăng gấp đôi mỗi RTT</b> (tăng mỗi ACK); ssthresh ban đầu 64 KB"],
    ["cwnd ≥ ssthresh (tránh tắc nghẽn)", "tăng <b>tuyến tính</b> +1 MSS mỗi RTT (AIMD: tăng cộng)"],
    ["3 ACK trùng — <b>Reno</b>", "ssthresh = cwnd/2, <b>cwnd = ssthresh</b> (một nửa), rồi tăng tuyến tính (FSM ghi cwnd = ssthresh + 3 MSS, pha khôi phục nhanh)"],
    ["Timeout (Reno &amp; Tahoe)", "ssthresh = cwnd/2, <b>cwnd = 1 MSS</b>, khởi động chậm lại"],
    ["<b>Tahoe</b>", "luôn đặt cwnd = 1 MSS cho cả timeout lẫn 3 ACK trùng"]]) + ul([
    "Tốc độ ≈ cwnd / RTT byte/s; bên gửi giữ LastByteSent − LastByteAcked ≤ cwnd.",
    "Thông lượng trung bình ≈ <b>(3/4)·W / RTT</b> (W = cửa sổ khi mất gói).",
    "Công bằng: K kết nối chung nút cổ chai R → mỗi kết nối ~R/K. Đường R đang có 9 kết nối: app mới mở 1 kết nối được R/10, mở 11 kết nối được ~R/2.",
    "Tắc nghẽn ≠ điều khiển luồng: quá nhiều nguồn gửi quá nhanh vào <b>mạng</b> → mất gói (tràn đệm router), trễ dài. TCP dùng cách tiếp cận <b>end-end</b> (suy ra từ mất gói/trễ); cách khác: mạng hỗ trợ (ECN, DECbit, ATM)."]) + src(F + " tr.85–108")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["Tầng giao vận vs tầng mạng", "giữa các tiến trình vs giữa các host."],
    ["UDP vs TCP demux", "UDP: (IP, cổng) đích; TCP: bộ 4 giá trị."],
    ["Go-Back-N vs Selective Repeat", "GBN: ACK tích luỹ, bên nhận không đệm gói sai thứ tự, một timer, timeout gửi lại <b>mọi</b> gói chưa ACK. SR: ACK riêng từng gói, đệm gói sai thứ tự, timer cho mỗi gói, chỉ gửi lại gói đó; cửa sổ ≤ nửa không gian số thứ tự."],
    ["rdt2.0 vs 2.1 vs 2.2 vs 3.0", "ACK/NAK · + số thứ tự · bỏ NAK · + timer cho kênh mất gói."],
    ["Điều khiển luồng vs tắc nghẽn", "luồng: bảo vệ <b>bộ đệm bên nhận</b> (rwnd); tắc nghẽn: bảo vệ <b>mạng</b> (cwnd)."],
    ["Khởi động chậm vs tránh tắc nghẽn", "×2 mỗi RTT khi cwnd &lt; ssthresh vs +1 MSS mỗi RTT khi cwnd ≥ ssthresh."],
    ["Timeout vs 3 ACK trùng (Reno)", "timeout: cwnd = 1 MSS (nặng hơn); 3 ACK trùng: cwnd giảm một nửa (mạng vẫn chuyển được segment)."],
    ["Tahoe vs Reno", "Tahoe: luôn về 1 MSS; Reno: 3 ACK trùng thì giảm một nửa."],
    ["ACK của GBN vs ACK của TCP", "GBN: ACK(n) = đã nhận tới gói n. TCP: ACK = byte tiếp theo mong đợi."],
    ["Bắt tay 2 bước vs 3 bước", "2 bước hỏng khi thông điệp bị trễ/gửi lại/đổi thứ tự → kết nối mở nửa, nhận trùng dữ liệu; 3 bước (SYN, SYNACK, ACK) cho hai bên biết nhau đang hoạt động."],
]) + src(F + " tr.5, 10–12, 36–38, 46, 51, 55, 74–80, 85, 100–102")

P["bay"] = trap("Bẫy 1 — checksum quên wraparound", "Cộng hai từ 16 bit mà bỏ bit nhớ tràn là sai; phải cộng bit nhớ vào bit thấp nhất rồi mới đảo bit.", "c3-trap-csum") + \
    trap("Bẫy 2 — ACK của TCP là byte tiếp theo", "Segment Seq=92 mang 8 byte → ACK = <b>100</b> (không phải 92 hay 99). Segment kế Seq=100 mang 20 byte → ACK = 120.", "c3-trap-ack") + \
    trap("Bẫy 3 — SR với cửa sổ quá lớn", "Số thứ tự 0..3 (4 số), cửa sổ 3: bên nhận không phân biệt gói 0 mới với gói 0 gửi lại → nhận trùng như dữ liệu mới. Điều kiện: <b>cửa sổ ≤ ½ không gian số thứ tự</b> (ở đây ≤ 2).", "c3-trap-sr") + \
    trap("Bẫy 4 — Reno vs Tahoe khi 3 ACK trùng", "cwnd = 12: Reno → ssthresh = 6, cwnd = 6 rồi tăng tuyến tính. Tahoe → ssthresh = 6, cwnd = 1 rồi khởi động chậm tới 6. <b>Đổi một chỗ:</b> thay 3 ACK trùng bằng timeout → cả hai đều về cwnd = 1.", "c3-trap-reno") + \
    trap("Bẫy 5 — khởi động chậm không “chậm”", "Tên gọi “chậm” vì bắt đầu từ 1 MSS, nhưng tăng <b>theo cấp số nhân</b>: 1 → 2 → 4 → 8 sau 3 RTT.", "c3-trap-ss") + \
    trap("Bẫy 6 — U với pipeline", "Nhân N vào <b>tử số</b>, mẫu vẫn là RTT + L/R; U không vượt 1 (N đủ lớn thì kênh bận liên tục).", "c3-trap-util") + \
    trap("Bẫy 7 — UDP length", "Trường length tính <b>cả header</b> (8 byte). Dữ liệu 100 byte → length = 108.", "c3-trap-len")

P["checklist"] = [
    "Dịch vụ tầng giao vận (truyền thông logic giữa các process) so với tầng mạng (giữa các host), ví dụ nhà Ann và nhà Bill",
    "Ghép kênh và phân kênh: UDP xác định bằng (IP đích, port đích); TCP xác định bằng bộ 4 giá trị",
    "UDP: header 8 byte, không kết nối, lý do vẫn dùng; cách tính checksum (cộng bù 1, wraparound)",
    "Nguyên lý truyền tin cậy: rdt1.0 → 2.0 (ACK/NAK) → 2.1 (số thứ tự) → 2.2 (bỏ NAK) → 3.0 (timer, kênh có mất gói); hiệu suất stop-and-wait U = (L/R)/(RTT + L/R)",
    "Pipelining: Go-Back-N (ACK tích lũy, một timer, gửi lại cả cửa sổ) và Selective Repeat (ACK từng gói, đệm phía nhận, kích thước cửa sổ ≤ nửa không gian số thứ tự)",
    "TCP segment: các trường header, số thứ tự tính theo byte, ACK là byte kế tiếp mong đợi; ước lượng RTT: EstimatedRTT, DevRTT, TimeoutInterval",
    "Truyền tin cậy trong TCP: các tình huống gửi lại, fast retransmit khi nhận 3 ACK trùng",
    "Điều khiển luồng: rwnd = RcvBuffer − (LastByteRcvd − LastByteRead)",
    "Quản lý kết nối: bắt tay 3 bước (SYN, SYN-ACK, ACK), đóng kết nối (FIN, ACK, TIME_WAIT)",
    "Nguyên lý điều khiển tắc nghẽn (nguyên nhân, chi phí); TCP: AIMD, slow start (cwnd tăng gấp đôi mỗi RTT), ssthresh, congestion avoidance, khi timeout (cwnd = 1 MSS) và khi 3 ACK trùng (Reno: cwnd giảm một nửa); TCP Tahoe và Reno; thông lượng TCP và tính công bằng",
    "＋ Bảng sinh ACK của bên nhận TCP (ACK trễ 500 ms, ACK trùng khi có khoảng trống)",
    "＋ Thông lượng TB = 3/4·W/RTT; công bằng R/K và mẹo mở nhiều kết nối song song",
    "＋ Điều khiển tắc nghẽn end-end vs có hỗ trợ từ mạng (ECN)",
]

P["quick"] = [
    QQ("Segment TCP có Seq = 200 mang 50 byte, nhận đúng. ACK bên nhận gửi về là?", ["200", "249", "250", "251"], "c", "ACK = byte tiếp theo mong đợi = 200 + 50."),
    QQ("Go-Back-N, timeout xảy ra. Bên gửi gửi lại gì?", ["Chỉ gói hết giờ", "Gói hết giờ và mọi gói có số thứ tự lớn hơn trong cửa sổ", "Không gửi gì", "Gói cuối cùng"], "b", "timeout(n): gửi lại n và mọi gói sau trong cửa sổ."),
    QQ("TCP Reno, cwnd = 16 MSS, nhận 3 ACK trùng. cwnd mới?", ["1 MSS", "8 MSS", "16 MSS", "17 MSS"], "b", "ssthresh = cwnd/2 = 8, cwnd = ssthresh."),
]

P["docthem"] = ul([
    "Công thức Mathis (tr.105): thông lượng ≈ 1,22·MSS / (RTT·√L) — để đạt 10 Gbps với segment 1500 byte, RTT 100 ms cần tỷ lệ mất 2·10<sup>-10</sup>.",
    "Pha khôi phục nhanh (fast recovery) của Reno trong FSM tr.103: cwnd = ssthresh + 3 MSS, mỗi ACK trùng thêm +1 MSS, ACK mới thì cwnd = ssthresh.",
    "Giáo trình §3.5.6: giá trị khởi tạo TimeoutInterval là 1 s, và nhân đôi khi timeout.",
])

BLOCK = dict(id="C3", mon="MMT", title="Tầng giao vận", src="chuong 3 Tang giao van.pdf", page=P)

QUESTIONS = [
    M("C3-01", "single", "Tầng giao vận cung cấp truyền thông logic giữa:", ["Các tiến trình ứng dụng chạy trên các host khác nhau", "Các host trên Internet", "Các router liền kề", "Các card mạng trong một LAN"], "a", "Tầng mạng: giữa các host; tầng giao vận: giữa các tiến trình (tr.4–5).", F + " tr.4–5", "c3-y"),
    M("C3-02", "single", "Host B nhận ba UDP segment cùng cổng đích 6428 nhưng đến từ ba địa chỉ IP nguồn khác nhau. Chúng được đưa tới:", ["Cùng một socket", "Ba socket khác nhau", "Socket nào còn trống", "Bị huỷ vì trùng cổng"], "a", "Socket UDP xác định bởi (IP đích, cổng đích): cùng cổng đích → cùng socket bất kể nguồn.", F + " tr.10–11", "c3-demux"),
    M("C3-03", "single", "Web server B:80 nhận ba TCP segment: từ A:9157, từ C:9157 và từ C:5775. Phát biểu nào đúng?", ["Ba segment được phân kênh tới ba socket khác nhau vì bộ 4 giá trị khác nhau", "Cả ba vào cùng một socket vì cùng cổng đích 80", "Hai segment từ C vào cùng một socket", "Server từ chối vì trùng cổng nguồn 9157"], "a", "TCP dùng bộ 4 (IP nguồn, cổng nguồn, IP đích, cổng đích) (tr.12–13).", F + " tr.12–14", "c3-demux"),
    M("C3-04", "single", "Phát biểu nào đúng về header UDP?", ["Gồm 4 trường 16 bit (source port, dest port, length, checksum); length tính cả header", "Dài 20 byte và có số thứ tự", "Có trường receive window", "Length chỉ tính phần dữ liệu"], "a", "Header UDP 8 byte; length = số byte của cả segment gồm header.", F + " tr.17", "c3-trap-len"),
    M("C3-05", "single", "Lý do nào KHÔNG phải là lý do để dùng UDP theo slide?", ["UDP đảm bảo các segment đến đúng thứ tự", "Không cần thiết lập kết nối", "Header nhỏ", "Không điều khiển tắc nghẽn nên có thể gửi nhanh theo mong muốn"], "a", "UDP có thể mất gói và giao không đúng thứ tự; lý do dùng: không bắt tay, đơn giản, header nhỏ, không điều khiển tắc nghẽn.", F + " tr.16–17", "c3-udp"),
    M("C3-06", "single", "Tính checksum UDP cho hai từ 16 bit 1110011001100110 và 1101010101010101:", ["0100010001000011", "1011101110111100", "1011101110111011", "0100010001000100"], "a", "Tổng = 1 1011101110111011 → cộng vòng bit tràn → 1011101110111100 → đảo bit → 0100010001000011.", F + " tr.18–19", "c3-trap-csum"),
    M("C3-07", "single", "rdt2.0 bổ sung những cơ chế nào so với rdt1.0?", ["Phát hiện lỗi (checksum) và phản hồi ACK/NAK từ bên nhận, gửi lại khi nhận NAK", "Bộ định thời và số thứ tự", "Cửa sổ trượt kích thước N", "Điều khiển tắc nghẽn"], "a", "Kênh rdt2.0 có lỗi bit nhưng không mất gói.", F + " tr.27–28", "c3-rdt"),
    M("C3-08", "single", "Vì sao rdt2.1 cần thêm số thứ tự cho gói tin?", ["Vì ACK/NAK có thể bị hỏng, bên gửi phải gửi lại và bên nhận cần phát hiện gói trùng", "Để tính checksum", "Để gửi nhiều gói cùng lúc", "Để đo RTT"], "a", "rdt2.0 có lỗ hổng khi ACK/NAK hỏng; số thứ tự 0/1 là đủ (tr.32–35).", F + " tr.32–35", "c3-rdt"),
    M("C3-09", "single", "Trong rdt2.2 (không dùng NAK), khi bên gửi nhận được ACK trùng lặp thì:", ["Hành động giống như nhận NAK: gửi lại gói tin hiện tại", "Bỏ qua và gửi gói mới", "Đóng kết nối", "Tăng cửa sổ"], "a", "Bên nhận ACK gói nhận tốt cuối cùng kèm số thứ tự (tr.36).", F + " tr.36", "c3-rdt"),
    M("C3-10", "single", "rdt3.0 xử lý kênh có thể mất gói bằng cách:", ["Bên gửi chờ ACK trong một khoảng thời gian; không nhận được thì gửi lại (cần bộ định thời đếm ngược)", "Bên nhận gửi NAK cho mọi gói", "Bỏ số thứ tự", "Gửi mỗi gói hai lần"], "a", "Gói chỉ đến trễ thì gửi lại gây trùng nhưng số thứ tự xử lý được (tr.38).", F + " tr.38–41", "c3-rdt"),
    M("C3-11", "single", "Liên kết 1 Gbps, RTT 30 ms, gói 8000 bit, giao thức dừng-và-chờ. Độ khả dụng bên gửi U xấp xỉ:", ["0,00027", "0,027", "0,27", "0,0027"], "a", "L/R = 8000/10<sup>9</sup> = 8 μs = 0,008 ms; U = 0,008 / (30 + 0,008) ≈ 0,00027.", F + " tr.42–43", "c3-util"),
    M("C3-12", "single", "L/R = 1 ms, RTT = 9 ms. Dùng pipeline gửi 5 gói liên tiếp rồi chờ ACK. Độ khả dụng U là:", ["0,5", "0,1", "0,9", "1"], "a", "U = (N·L/R)/(RTT + L/R) = 5·1/(9 + 1) = 0,5. Dừng-và-chờ chỉ được 0,1.", F + " tr.43–45", "c3-trap-util"),
    M("C3-13", "single", "Đặc điểm nào thuộc Go-Back-N?", ["Bên nhận gửi ACK tích luỹ và huỷ gói đến không đúng thứ tự; hết giờ thì gửi lại mọi gói chưa được ACK", "Bên nhận đệm gói sai thứ tự", "Mỗi gói có bộ định thời riêng", "Chỉ gửi lại gói bị mất"], "a", "Tr.46–49.", F + " tr.46–49", "c3-sosanh"),
    M("C3-14", "single", "Đặc điểm nào thuộc Selective Repeat?", ["Bên nhận báo nhận riêng từng gói và đệm gói sai thứ tự; bên gửi có timer cho mỗi gói chưa ACK và chỉ gửi lại gói đó", "ACK tích luỹ, một timer", "Bên nhận huỷ mọi gói sai thứ tự", "Không cần cửa sổ"], "a", "Tr.46, 51–53.", F + " tr.46, 51–53", "c3-sosanh"),
    M("C3-15", "single", "GBN với N = 4: bên gửi gửi pkt0–pkt3, pkt2 bị mất. Bên nhận đã nhận pkt0, pkt1 rồi nhận pkt3. Bên nhận làm gì?", ["Huỷ pkt3 và gửi lại ack1", "Đệm pkt3 và gửi ack3", "Gửi ack2", "Không gửi gì"], "a", "GBN bên nhận chỉ nhớ expectedseqnum; gói sai thứ tự bị huỷ, gửi lại ACK cho gói đúng thứ tự cao nhất (ack1).", F + " tr.49–50", "c3-win"),
    M("C3-16", "single", "Cùng tình huống (N = 4, mất pkt2) nhưng dùng Selective Repeat. Khi pkt2 gửi lại tới nơi, bên nhận:", ["Giao pkt2, pkt3, pkt4, pkt5 (đã đệm) lên tầng trên theo đúng thứ tự", "Chỉ giao pkt2, huỷ các gói đã đệm", "Yêu cầu gửi lại pkt3–pkt5", "Gửi NAK"], "a", "SR đệm gói sai thứ tự (gửi ack3, ack4, ack5), khi lỗ trống được lấp thì giao cả dãy (tr.54).", F + " tr.54", "c3-win"),
    M("C3-17", "single", "Selective Repeat dùng số thứ tự 0, 1, 2, 3. Kích thước cửa sổ lớn nhất tránh được việc nhận nhầm gói cũ thành gói mới là:", ["2", "3", "4", "1"], "a", "Ví dụ tr.55 với cửa sổ 3 bị lỗi. Điều kiện (giáo trình): cửa sổ ≤ một nửa không gian số thứ tự = 4/2 = 2.", F + " tr.55", "c3-trap-sr"),
    M("C3-18", "single", "Host A gửi segment Seq = 92 chứa 8 byte dữ liệu và B nhận đúng. Số ACK trong segment B gửi về là:", ["100", "92", "99", "93"], "a", "ACK = số thứ tự byte tiếp theo mong đợi = 92 + 8.", F + " tr.59, 68–69", "c3-trap-ack"),
    M("C3-19", "single", "EstimatedRTT hiện tại 100 ms, SampleRTT mới đo 120 ms, α = 0,125. EstimatedRTT mới là:", ["102,5 ms", "120 ms", "110 ms", "97,5 ms"], "a", "(1 − 0,125)·100 + 0,125·120 = 87,5 + 15 = 102,5 ms.", F + " tr.62", "c3-tcp"),
    M("C3-20", "single", "EstimatedRTT = 100 ms, DevRTT = 10 ms. TimeoutInterval của TCP là:", ["140 ms", "110 ms", "100 ms", "400 ms"], "a", "TimeoutInterval = EstimatedRTT + 4·DevRTT = 100 + 40.", F + " tr.63", "c3-tcp"),
    M("C3-21", "single", "Fast retransmit trong TCP được kích hoạt khi:", ["Bên gửi nhận 3 ACK trùng lặp cho cùng dữ liệu; gửi lại segment chưa ACK có số thứ tự nhỏ nhất", "Timeout xảy ra hai lần", "rwnd bằng 0", "Nhận được FIN"], "a", "Không cần chờ timeout vốn tương đối dài (tr.71).", F + " tr.71–72", "c3-rel"),
    M("C3-22", "single", "RcvBuffer = 4096 byte, LastByteRcvd = 3000, LastByteRead = 1000. Giá trị rwnd bên nhận quảng bá là:", ["2096 byte", "1096 byte", "2000 byte", "3000 byte"], "a", "rwnd = RcvBuffer − (LastByteRcvd − LastByteRead) = 4096 − 2000.", F + " tr.75 (công thức theo giáo trình)", "c3-flow"),
    M("C3-23", "single", "Trong bắt tay 3 bước, client gửi SYN với Seq = x, server chọn số thứ tự khởi tạo y. Segment SYNACK của server có:", ["SYNbit = 1, Seq = y, ACKbit = 1, ACKnum = x + 1", "SYNbit = 1, Seq = x + 1, ACKnum = y", "FINbit = 1, Seq = y", "ACKnum = y + 1"], "a", "Sau đó client gửi ACKbit = 1, ACKnum = y + 1 (có thể kèm dữ liệu).", F + " tr.80", "c3-hs"),
    M("C3-24", "single", "Phát biểu nào phân biệt đúng điều khiển luồng và điều khiển tắc nghẽn?", ["Điều khiển luồng tránh làm tràn bộ đệm bên nhận; điều khiển tắc nghẽn tránh quá nhiều nguồn gửi quá nhanh vào mạng", "Hai khái niệm là một", "Điều khiển luồng do router thực hiện", "Điều khiển tắc nghẽn dùng trường rwnd"], "a", "Tr.74, 85.", F + " tr.74, 85", "c3-sosanh"),
    M("C3-25", "single", "Nguyên tắc AIMD của TCP là:", ["Tăng cwnd 1 MSS mỗi RTT cho tới khi mất gói, rồi giảm cwnd một nửa", "Tăng gấp đôi cwnd mỗi RTT mãi mãi", "Giảm cwnd về 0 khi mất gói", "Giữ cwnd cố định"], "a", "Additive Increase, Multiplicative Decrease (tr.97).", F + " tr.97", "c3-cc"),
    M("C3-26", "single", "Kết nối TCP bắt đầu với cwnd = 1 MSS, ssthresh = 16 MSS, không mất gói. Sau 3 RTT, cwnd bằng:", ["8 MSS", "4 MSS", "3 MSS", "16 MSS"], "a", "Khởi động chậm nhân đôi mỗi RTT: 1 → 2 → 4 → 8 (vẫn dưới ssthresh).", F + " tr.99", "c3-trap-ss"),
    M("C3-27", "single", "TCP Reno đang có cwnd = 12 MSS thì nhận 3 ACK trùng lặp. Giá trị mới:", ["ssthresh = 6, cwnd = 6 MSS", "ssthresh = 6, cwnd = 1 MSS", "ssthresh = 12, cwnd = 6", "ssthresh = 24, cwnd = 12"], "a", "Tr.102: 3 ACK trùng → ssthresh = cwnd/2, cwnd = ssthresh. Tahoe mới đặt cwnd = 1.", F + " tr.100–102", "c3-trap-reno"),
    M("C3-28", "single", "Khi xảy ra timeout (Reno hoặc Tahoe), TCP đặt:", ["ssthresh = cwnd/2 và cwnd = 1 MSS", "ssthresh = cwnd và cwnd = cwnd/2", "cwnd = ssthresh + 3", "Không thay đổi"], "a", "Tr.100, 102.", F + " tr.100–102", "c3-cc"),
    M("C3-29", "single", "Cửa sổ khi mất gói W = 80 KB, RTT = 100 ms. Thông lượng trung bình của TCP xấp xỉ:", ["600 KB/s", "800 KB/s", "400 KB/s", "60 KB/s"], "a", "Thông lượng TB = (3/4)·W/RTT = 0,75·80 KB / 0,1 s = 600 KB/s.", F + " tr.104", "c3-cc"),
    M("C3-30", "single", "Liên kết nút cổ chai tốc độ R đang có 9 kết nối TCP. Một ứng dụng mới mở 11 kết nối TCP song song sẽ nhận được xấp xỉ:", ["R/2", "R/10", "R/20", "R"], "a", "Mỗi kết nối ~R/20 (tổng 20 kết nối); 11 kết nối → 11R/20 ≈ R/2. Mở 1 kết nối chỉ được R/10.", F + " tr.106–108", "c3-cc"),
]
