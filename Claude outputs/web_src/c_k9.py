from h import *

SVG = """<svg viewBox="0 0 700 220" width="700" role="img" aria-label="Caddy đứng trước app, nhận HTTPS và chuyển vào localhost:8000">
<g font-size="13">
<rect x="8" y="70" width="130" height="56" rx="8" class="box"/><text x="20" y="92" font-weight="700">Trình duyệt</text><text x="20" y="112" class="mono" font-size="12">https://tên-miền</text>
<rect x="8" y="160" width="130" height="44" rx="8" class="box"/><text x="20" y="180" font-weight="700">Let's Encrypt</text><text x="20" y="196" font-size="11.5" class="muted">xác minh qua port 80</text>
<rect x="200" y="10" width="480" height="200" rx="12" class="box" stroke-dasharray="7 4"/><text x="214" y="30" font-weight="700">EC2 · Security Group: chỉ mở 80, 443 (không mở 8000)</text>
<rect x="230" y="60" width="200" height="80" rx="8" class="boxa"/><text x="244" y="82" font-weight="700">Caddy (reverse proxy)</text><text x="244" y="102" font-size="12">TLS termination, tự cấp &amp;</text><text x="244" y="118" font-size="12">gia hạn chứng chỉ</text>
<rect x="480" y="60" width="180" height="80" rx="8" class="box"/><text x="494" y="82" font-weight="700">App (container)</text><text x="494" y="102" class="mono" font-size="12">localhost:8000</text><text x="494" y="118" font-size="12">chỉ chạy HTTP thường</text>
<path d="M138 98 h88" class="lna"/><path d="M220 93 l7 5 l-7 5" class="lna"/><text x="146" y="90" class="mono" font-size="11">HTTPS :443</text>
<path d="M430 100 h46" class="ln"/><path d="M470 95 l7 5 l-7 5" class="ln"/><text x="434" y="92" class="mono" font-size="11">HTTP</text>
<path d="M138 182 C 190 182 200 150 240 140" class="ln dash"/><text x="150" y="160" class="mono" font-size="11">:80</text>
<text x="230" y="170" font-size="12" class="muted">Caddyfile: tên-miền { reverse_proxy localhost:8000 }</text>
<text x="230" y="190" font-size="12" class="muted">DNS: bản ghi A tên-miền → Public IP (hoặc IP.nip.io)</text>
</g></svg>"""

TLS = """<svg viewBox="0 0 560 200" width="560" role="img" aria-label="Bắt tay TLS 3 bước">
<g font-size="13">
<text x="60" y="20" font-weight="700">trình duyệt</text><text x="420" y="20" font-weight="700">máy chủ</text>
<line x1="100" y1="28" x2="100" y2="190" class="ln dash"/><line x1="460" y1="28" x2="460" y2="190" class="ln dash"/>
<path d="M460 60 H104" class="lna"/><path d="M110 55 l-7 5 l7 5" class="lna"/><text x="200" y="52">① gửi chứng chỉ → trình duyệt kiểm tra</text>
<path d="M104 110 H456" class="lna"/><path d="M110 105 l-7 5 l7 5" class="lna"/><path d="M450 105 l7 5 l-7 5" class="lna"/><text x="210" y="102">② thống nhất một khóa chung</text>
<rect x="104" y="140" width="352" height="30" rx="15" class="nodea"/><text x="170" y="160" fill="#fff" style="fill:#fff">③ dữ liệu sau đó được mã hóa 🔒</text>
</g></svg>"""

P = {}
P["y"] = """<p>Đưa hệ thống ra Internet qua <b>một địa chỉ HTTPS công khai</b>: đặt <b>reverse proxy Caddy</b> đứng trước ứng dụng. Caddy nhận request từ Internet (HTTPS), lo phần mã hoá (<b>TLS termination</b>) và chuyển vào app chạy HTTP thường ở <code>localhost:8000</code>. Caddy <b>tự xin và tự gia hạn</b> chứng chỉ từ <b>Let's Encrypt</b> cho <b>tên miền</b> trỏ về IP của instance.</p>""" + src("reverse_proxy_https.pdf tr.2–6, 11")

P["mohinh"] = diagram(SVG, "Toàn hệ thống qua địa chỉ HTTPS công khai (reverse_proxy_https.pdf tr.5–6, 12, 16, 19–22)") + """
<h3 id="k9-tls">Chứng chỉ và bắt tay TLS</h3>""" + diagram(TLS, "reverse_proxy_https.pdf tr.9") + """
<p><b>Chứng chỉ gồm:</b> tên miền · bên cấp · hạn dùng · khóa công khai. Chứng chỉ chứng minh danh tính trang và cho phép mã hoá HTTPS. <b>Ổ khóa xanh</b> = chứng chỉ hợp lệ và dữ liệu đang được mã hoá.</p>""" + src("reverse_proxy_https.pdf tr.8–10")

P["bang"] = """<h3 id="k9-caddy">Caddyfile và lệnh</h3>""" + pre("""
myapp.example.com {
    reverse_proxy localhost:8000
}
""", "caddy") + table(["Dòng / lệnh", "Ý nghĩa"], [
    [c("myapp.example.com {"), "dòng đầu: <b>tên miền</b> (Caddy xin chứng chỉ cho tên này)"],
    [c("reverse_proxy localhost:8000"), "dòng trong: địa chỉ app bên trong mà Caddy chuyển request tới"],
    [c("sudo nano /etc/caddy/Caddyfile"), "sửa cấu hình trên instance"],
    [c("sudo systemctl reload caddy"), "nạp lại cấu hình"],
    [c("sudo journalctl -u caddy -f"), "đọc log chung khi chứng chỉ không cấp được"],
    [c("curl -v https://tên-miền"), "xem chứng chỉ và kết nối HTTPS"],
]) + src("reverse_proxy_https.pdf tr.12–13, 23–24") + """
<h3 id="k9-domain">Tên miền</h3>""" + table(["Cách", "Mô tả"], [
    ["Vì sao cần", "Let's Encrypt cấp chứng chỉ cho <b>tên miền</b>, không cấp cho địa chỉ IP thuần"],
    ["Bản ghi A", "tên miền có bản ghi A trỏ tới một IP; gõ tên miền → DNS trả IP để trình duyệt biết đi đâu"],
    ["nip.io", "dịch vụ tên miền miễn phí trỏ sẵn về IP: ghép IP vào tên, vd <code>203.0.113.25.nip.io</code> — không cấu hình thêm"],
    ["Tên miền riêng", "vào trang quản lý tên miền, thêm bản ghi A trỏ về Public IP của instance"]]) + src("reverse_proxy_https.pdf tr.15–18") + """
<h3 id="k9-sg">Security Group cho HTTPS</h3>""" + table(["Port", "Giao thức", "Nguồn", "Mục đích"], [
    ["80", "TCP", "0.0.0.0/0", "cho Let's Encrypt gửi request xác minh quyền sở hữu tên miền"], ["443", "TCP", "0.0.0.0/0", "người dùng truy cập HTTPS"], ["8000", "—", "—", "<b>không thêm rule</b> (app chỉ nhận qua Caddy)"]]) + src("reverse_proxy_https.pdf tr.19–21") + """
<h3 id="k9-debug">Ba lỗi khi chứng chỉ không cấp được</h3>""" + table(["Lỗi", "Hiện tượng", "Cách sửa"], [
    ["Port 80 đóng", "Let's Encrypt không xác minh được; log Caddy báo lỗi cấp chứng chỉ", "mở port 80"],
    ["Tên miền chưa trỏ đúng", "thử thách của Let's Encrypt gửi sai chỗ", "kiểm tra bản ghi A hoặc chuỗi nip.io đúng IP"],
    ["Chạm rate limit", "xin chứng chỉ quá nhiều lần → tạm thời không cấp thêm", "dùng tên miền con mới hoặc chờ hết giới hạn"]]) + "<p>Kiểm tra đạt: mở địa chỉ HTTPS thấy ổ khóa xanh · <code>curl -v</code> thấy chứng chỉ · xem hạn chứng chỉ còn hiệu lực.</p>" + src("reverse_proxy_https.pdf tr.23–24")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["HTTP vs HTTPS", "HTTPS = HTTP + mã hoá; dữ liệu giữa trình duyệt và máy chủ được bảo vệ."],
    ["Reverse proxy vs app", "Proxy đứng trước, nhận request Internet, định tuyến, lo HTTPS; app bên trong chỉ cần HTTP."],
    ["Chứng chỉ vs Let's Encrypt", "Chứng chỉ chứng minh danh tính + cho phép mã hoá; Let's Encrypt là tổ chức cấp chứng chỉ miễn phí."],
    ["Caddy vs cài chứng chỉ tay", "Caddy tự xin và tự gia hạn qua Let's Encrypt khi khởi động; không phải tự xin/cài."],
    ["Port 80 vs 443", "80: Let's Encrypt xác minh (và HTTP); 443: người dùng truy cập HTTPS."],
    ["nip.io vs tên miền riêng", "nip.io: ghép IP vào tên, không cấu hình. Tên miền riêng: tự thêm bản ghi A."],
    ["Tên miền vs IP thuần", "Let's Encrypt chỉ cấp cho tên miền."],
    [c("reload caddy") + " vs sửa file", "Sửa Caddyfile chưa có tác dụng cho tới khi <code>systemctl reload caddy</code>."],
]) + src("reverse_proxy_https.pdf tr.5–21")

P["bay"] = trap("Bẫy 1 — mở port 8000 cho “chắc”", "Đã có Caddy thì <b>không</b> mở port app (8000) ra Internet; chỉ 80 và 443. Caddy gọi app qua <code>localhost:8000</code> ngay trên instance.", "k9-trap-8000") + \
    trap("Bẫy 2 — đóng port 80 vì “đã có HTTPS”", "Let's Encrypt xác minh tên miền bằng request tới <b>port 80</b>. Đóng 80 → không cấp được chứng chỉ (log Caddy báo lỗi).", "k9-trap-80") + \
    trap("Bẫy 3 — dùng IP thuần trong Caddyfile", "<code>203.0.113.25 { reverse_proxy localhost:8000 }</code> → không xin được chứng chỉ Let's Encrypt cho IP thuần. <b>Đổi một chỗ:</b> dùng <code>203.0.113.25.nip.io</code> → được.", "k9-trap-ip") + \
    trap("Bẫy 4 — đọc Caddyfile", "Dòng ngoài ngoặc là <b>tên miền</b>; <code>reverse_proxy</code> là <b>đích bên trong</b>. Đổi app sang port 9000 → sửa thành <code>reverse_proxy localhost:9000</code> rồi <code>systemctl reload caddy</code>.", "k9-trap-file") + \
    trap("Bẫy 5 — xin chứng chỉ liên tục", "Thử đi thử lại khi cấu hình sai → chạm <b>rate limit</b>, Let's Encrypt tạm ngừng cấp. Sửa: tên miền con mới hoặc chờ; đọc <code>journalctl -u caddy -f</code> trước khi thử lại.", "k9-trap-rate")

P["checklist"] = [
    "Reverse proxy là gì, vì sao cần (một cổng vào duy nhất, ẩn port app, TLS termination)",
    "HTTP và HTTPS, chứng chỉ chứa gì, bắt tay TLS, CA, Let's Encrypt, ý nghĩa ổ khóa",
    "Caddy: Caddyfile domain { reverse_proxy localhost:8000 }, systemctl reload caddy, tự cấp và gia hạn chứng chỉ",
    "Tên miền, bản ghi A trỏ về IP, nip.io; cần mở port 80/443 trong SG; chẩn đoán lỗi chứng chỉ và DNS",
    "＋ Let's Encrypt chỉ cấp cho tên miền, xác minh qua port 80",
    "＋ 3 lỗi: port 80 đóng · tên miền trỏ sai · rate limit; journalctl -u caddy -f; curl -v https://...",
]

P["quick"] = [
    QQ("Trong Caddyfile <code>api.10.0.0.5.nip.io { reverse_proxy localhost:8000 }</code>, <code>localhost:8000</code> là gì?", ["Tên miền công khai", "Địa chỉ app bên trong mà Caddy chuyển request tới", "Port của Let's Encrypt", "Địa chỉ DNS"], "b", "Dòng trong là đích bên trong."),
    QQ("Vì sao phải mở port 80 dù người dùng vào bằng HTTPS?", ["Để SSH", "Để Let's Encrypt xác minh tên miền", "Để app nhận request trực tiếp", "Không cần mở"], "b", "Let's Encrypt gửi request xác minh qua port 80."),
    QQ("Ổ khóa xanh trên trình duyệt nghĩa là gì?", ["Server không có lỗi", "Chứng chỉ hợp lệ và dữ liệu đang được mã hoá", "Trang không có quảng cáo", "Port 8000 đang mở"], "b", "reverse_proxy_https.pdf tr.9–10."),
]

BLOCK = dict(id="K9", mon="TTNT", title="Reverse proxy và HTTPS", src="reverse_proxy_https.pdf", page=P)

CF = "myapp.example.com {\n    reverse_proxy localhost:8000\n}"

QUESTIONS = [
    Q("K9-01", "single", "What is a reverse proxy in the lecture's architecture?",
      ["A layer in front of the application that receives requests from the Internet and forwards them to the application inside.", "A DNS record that maps a domain to an IP.", "A GitHub Action that deploys to EC2.", "A firewall rule for port 22."], "a",
      "Reverse proxy là lớp đứng trước ứng dụng, nhận request từ Internet rồi chuyển vào ứng dụng bên trong.", "reverse_proxy_https.pdf tr.5", "k9-y"),
    Q("K9-02", "multi", "Why does the system use a reverse proxy?",
      ["It routes each request to the right application.", "It handles HTTPS encryption so the application inside only needs plain HTTP (TLS termination).",
       "It lets the application port (8000) stay closed in the Security Group.", "It replaces the need for a domain name."], "abc",
      "Lợi ích: định tuyến, TLS termination; nhờ đó chỉ mở 80/443, không mở port app. Vẫn cần tên miền để có chứng chỉ.", "reverse_proxy_https.pdf tr.6, 15, 20", "k9-trap-8000"),
    Q("K9-03", "single", "Consider this Caddyfile on the instance. Which statements are correct?",
      ["The first line is the domain name.", "<code>localhost:8000</code> is the internal application address that Caddy forwards requests to.", "Caddy automatically obtains and renews a Let's Encrypt certificate for that domain.", "All the statements are correct."], "d",
      "Caddyfile tối giản: dòng đầu là tên miền, dòng trong là địa chỉ app; khi khởi động Caddy tự xin chứng chỉ Let's Encrypt cho tên miền đó và tự gia hạn.", "reverse_proxy_https.pdf tr.11–14", "k9-caddy", code=CF, lang="caddy"),
    Q("K9-04", "single", "You edited <code>/etc/caddy/Caddyfile</code> on the instance. Which command applies the new configuration?",
      ["<code>sudo systemctl reload caddy</code>", "<code>docker compose pull</code>", "<code>git push origin main</code>", "<code>sudo journalctl -u caddy -f</code>"], "a",
      "systemctl reload caddy nạp lại cấu hình; journalctl dùng để đọc log.", "reverse_proxy_https.pdf tr.13", "k9-caddy"),
    Q("K9-05", "single", "Why does the HTTPS setup require a domain name pointing to the instance?",
      ["Let's Encrypt issues certificates for domain names, not for bare IP addresses.", "Caddy cannot listen on an IP address.", "Browsers block every IP address.", "Docker requires a domain name."], "a",
      "Vì Let's Encrypt chỉ cấp cho tên miền nên cần tên miền (nip.io hoặc tên riêng) trỏ về IP của instance.", "reverse_proxy_https.pdf tr.15", "k9-trap-ip"),
    Q("K9-06", "single", "The instance's public IP is <code>203.0.113.25</code> and you have no domain of your own. Which address can you put in the Caddyfile without any DNS configuration?",
      ["<code>203.0.113.25.nip.io</code>", "<code>203.0.113.25</code>", "<code>localhost:8000</code>", "<code>nip.io/203.0.113.25</code>"], "a",
      "nip.io: ghép IP của instance vào tên miền, đã trỏ sẵn về IP đó.", "reverse_proxy_https.pdf tr.17–18", "k9-domain"),
    Q("K9-07", "multi", "Which Security Group rules match the lecture for serving the app over HTTPS with Caddy?",
      ["Port 80/TCP from 0.0.0.0/0, so Let's Encrypt can verify the domain.", "Port 443/TCP from 0.0.0.0/0, so users can access HTTPS.",
       "Port 8000 from 0.0.0.0/0, so Caddy can reach the application.", "Close port 80 once HTTPS works."], "ab",
      "Chỉ mở 80 và 443 ra Internet; không thêm rule cho 8000 (Caddy gọi app qua localhost). Port 80 vẫn cần cho việc xác minh/gia hạn.", "reverse_proxy_https.pdf tr.19–21", "k9-sg"),
    Q("K9-08", "single", "The certificate is not issued and the Caddy log shows a certificate error. The domain's A record is correct. Which cause from the lecture fits, and what is the fix?",
      ["Port 80 is closed, so Let's Encrypt cannot verify the domain → open port 80.", "Port 22 is closed → open port 22.", "The app uses FastAPI → switch to Flask.", "The image has no latest tag → retag it."], "a",
      "Ba lỗi: port 80 đóng (mở port 80) · tên miền trỏ sai (sửa bản ghi A/chuỗi nip.io) · rate limit (tên miền con mới hoặc chờ). Log chung: <code>sudo journalctl -u caddy -f</code>.", "reverse_proxy_https.pdf tr.23", "k9-debug"),
    Q("K9-09", "multi", "According to the lecture, which items does a certificate contain?",
      ["The domain name", "The issuer", "The validity period", "The server's private key"], "abc",
      "Chứng chỉ gồm tên miền, bên cấp, hạn dùng và khóa công khai — không bao giờ chứa khóa riêng.", "reverse_proxy_https.pdf tr.9", "k9-tls"),
    Q("K9-10", "single", "Which order matches the TLS handshake shown in the lecture?",
      ["Server sends its certificate and the browser checks it → both agree on a shared key → data is encrypted.", "Browser sends its private key → server stores it → data is sent in plain text.",
       "Data is encrypted → certificate is sent → key is agreed.", "DNS sends the certificate → Caddy decrypts → browser restarts."], "a",
      "Sơ đồ slide: ① máy chủ gửi chứng chỉ, trình duyệt kiểm tra ② thống nhất khóa chung ③ dữ liệu sau đó được mã hoá.", "reverse_proxy_https.pdf tr.9", "k9-tls"),
    Q("K9-11", "single", "After many failed attempts while fixing the configuration, Let's Encrypt temporarily refuses to issue more certificates for your domain. What does the lecture suggest?",
      ["Use a new subdomain or wait until the limit expires.", "Open port 8000.", "Restart the browser.", "Delete the Security Group."], "a", "Đó là rate limit; cách sửa: dùng tên miền con mới hoặc chờ hết giới hạn.", "reverse_proxy_https.pdf tr.23", "k9-trap-rate"),
    Q("K9-12", "single", "Which check confirms the HTTPS deployment from the command line by showing the certificate and the HTTPS connection?",
      ["<code>curl -v https://tên-miền</code>", "<code>ping tên-miền</code>", "<code>docker ps</code>", "<code>git log --oneline</code>"], "a",
      "Tiêu chí đạt: ổ khóa xanh trên trình duyệt, curl -v thấy chứng chỉ và kết nối HTTPS, chứng chỉ còn hạn.", "reverse_proxy_https.pdf tr.24", "k9-debug"),
]
