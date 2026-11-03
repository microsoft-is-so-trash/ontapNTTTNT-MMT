from h import *

SVG = """<svg viewBox="0 0 680 230" width="680" role="img" aria-label="Security Group bao quanh EC2 instance">
<g font-size="13">
<rect x="8" y="20" width="140" height="44" rx="8" class="box"/><text x="20" y="40" font-weight="700">Sinh viên</text><text x="20" y="56" class="muted" font-size="12">My IP · private key .pem</text>
<rect x="8" y="150" width="140" height="44" rx="8" class="box"/><text x="20" y="170" font-weight="700">Người dùng</text><text x="20" y="186" class="muted" font-size="12">bất kỳ đâu (0.0.0.0/0)</text>
<rect x="230" y="10" width="300" height="200" rx="12" class="boxa" stroke-dasharray="7 4"/><text x="244" y="32" font-weight="700" class="acc">Security Group (tường lửa)</text>
<text x="244" y="52" font-size="12" class="mono">inbound 22  ← My IP</text><text x="244" y="68" font-size="12" class="mono">inbound 80, 443 ← 0.0.0.0/0</text><text x="244" y="84" font-size="12" class="mono muted">mặc định: chặn phần lớn lưu lượng vào</text>
<rect x="270" y="100" width="220" height="96" rx="8" class="box"/><text x="284" y="122" font-weight="700">EC2 instance (IaaS)</text><text x="284" y="142" font-size="12">AMI: Ubuntu · Public IP</text><text x="284" y="160" font-size="12">public key do AWS đặt sẵn</text><text x="284" y="178" font-size="12" class="mono">docker compose up -d</text>
<path d="M148 42 h118" class="ln"/><path d="M260 37 l7 5 l-7 5" class="ln"/><text x="160" y="36" font-size="11" class="mono">ssh :22</text>
<path d="M148 172 h118" class="ln"/><path d="M260 167 l7 5 l-7 5" class="ln"/><text x="160" y="166" font-size="11" class="mono">:80 :443</text>
<text x="548" y="60" font-size="12" class="muted">Không mở rule</text><text x="548" y="76" font-size="12" class="muted">→ timeout</text><text x="548" y="110" font-size="12" class="muted">Không dùng nữa</text><text x="548" y="126" font-size="12" class="muted">→ stop/terminate</text><text x="548" y="142" font-size="12" class="muted">tránh mất tiền</text>
</g></svg>"""

P = {}
P["y"] = """<p>Laptop chỉ chạy khi máy bật, không có địa chỉ công khai ổn định. Để ứng dụng thành <b>dịch vụ thật</b>, ta <b>thuê máy chủ ảo</b> trên đám mây: <b>AWS EC2</b> (mô hình <b>IaaS</b>) — chạy liên tục, có <b>Public IP</b>, người khác truy cập qua Internet. Truy cập được kiểm soát bởi <b>Security Group</b> theo nguyên tắc <b>quyền tối thiểu</b>.</p>""" + src("cloudcomputing.pdf tr.3, 6–9")

P["mohinh"] = diagram(SVG, "EC2 nằm sau Security Group (cloudcomputing.pdf tr.12–16, 18–19)") + """
<h3 id="k7-steps">Các bước tạo instance</h3>""" + flow(["Chọn AMI (ảnh HĐH, vd Ubuntu)", "Chọn instance type (ưu tiên Free Tier)", "Tạo key pair (.pem)", "Launch, chờ sẵn sàng", "ssh -i my-key.pem ubuntu@&lt;Public IP&gt;"]) + src("cloudcomputing.pdf tr.10–13")

P["bang"] = """<h3 id="k7-terms">Thuật ngữ</h3>""" + table(["Thuật ngữ", "Ý nghĩa"], [
    ["Điện toán đám mây", "thuê tài nguyên máy tính qua Internet thay vì tự mua/vận hành máy chủ vật lý: tạo máy trong vài phút, tăng/giảm khi cần, trả theo mức dùng, xoá khi không cần"],
    ["IaaS", "thuê <b>hạ tầng</b> (vd máy chủ ảo); người dùng <b>tự cài và quản lý</b> phần mềm trên đó. EC2 thuộc IaaS"],
    ["EC2 / instance", "dịch vụ tạo máy chủ ảo của AWS / mỗi máy chủ ảo tạo ra"],
    ["AMI", "ảnh hệ điều hành dùng để tạo instance — chọn AMI nào, instance chạy HĐH đó"],
    ["Instance type", "loại máy (CPU/RAM); chọn loại nằm trong Free Tier"],
    ["Key pair", "khóa công khai + khóa riêng để SSH; AWS giữ public key trên instance, bạn giữ private key (.pem) và phải bảo quản an toàn"],
    ["Public IP", "địa chỉ công khai để SSH và để người dùng truy cập. Restart instance có thể đổi IP nếu không dùng Elastic IP (CD.pdf tr.25)"],
    ["Security Group", "bộ quy tắc tường lửa kiểm soát lưu lượng <b>vào (inbound)</b> và <b>ra (outbound)</b>; mặc định phần lớn lưu lượng vào bị chặn"],
    ["Free Tier", "gói miễn phí giới hạn loại máy và thời lượng — tắt/xóa instance khi không dùng"]]) + """
<h3 id="k7-ports">Port cần mở cho dự án</h3>""" + table(["Port", "Dùng cho", "Nguồn"], [
    ["22", "SSH", "<b>chỉ My IP</b> (vì là cửa quản trị)"], ["80", "HTTP (và để Let's Encrypt xác minh — K9)", "0.0.0.0/0"], ["443", "HTTPS (buổi 10)", "0.0.0.0/0"],
    ["8000", "port app trong stack", "không mở khi đã có reverse proxy (K9)"]]) + """
<h3 id="k7-deploy">Đưa stack Docker lên EC2</h3>""" + pre("""
ssh -i my-key.pem ubuntu@<dia-chi-cong-khai>
# trên instance: cài Docker và Docker Compose
# đưa mã nguồn + docker-compose.yml lên, tạo .env cho thông tin nhạy cảm
docker compose up -d
# mở đúng port trong Security Group rồi gọi http://<dia-chi-cong-khai>
""", "bash") + src("cloudcomputing.pdf tr.6–19")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["Laptop vs EC2", "Laptop: chỉ chạy khi bật, chỉ truy cập trong máy, không có địa chỉ công khai ổn định. EC2: chạy liên tục, Public IP, truy cập qua Internet."],
    ["IaaS (EC2) vs phần mềm bạn cài", "AWS cho thuê máy ảo; HĐH (từ AMI), Docker, app là phần bạn tự cài và quản lý."],
    ["Inbound vs outbound rule", "Vào instance vs ra khỏi instance."],
    ["My IP vs 0.0.0.0/0", "Chỉ địa chỉ của bạn vs mọi nơi trên Internet."],
    ["Nên vs không nên (quyền tối thiểu)", "Nên: chỉ mở port cần dùng, SSH chỉ My IP, xoá rule không dùng. Không nên: mở tất cả port, SSH Anywhere, giữ rule cũ sau bài thực hành."],
    ["Stop/xoá vs để chạy", "Không dùng thì tắt hoặc xoá instance để tránh phát sinh phí."],
    ["Public key vs private key (EC2)", "AWS giữ public key trên instance; sinh viên giữ private key (.pem)."],
    ["Lỗi timeout vs Permission denied", "Timeout khi truy cập app/SSH thường do <b>Security Group chưa mở port</b>; Permission denied (publickey) là server từ chối xác thực (sai key/user)."],
]) + src("cloudcomputing.pdf tr.3, 7, 12, 14–17; CD.pdf tr.25")

P["bay"] = trap("Bẫy 1 — app chạy nhưng trình duyệt timeout", "Container chạy, <code>curl localhost</code> trên instance OK, nhưng từ ngoài vào bị <b>timeout</b> → Security Group chưa có inbound rule cho port đó. Mặc định phần lớn lưu lượng vào bị chặn.<br><b>Đổi một chỗ:</b> thêm rule port 80 nguồn 0.0.0.0/0 → truy cập được.", "k7-trap-timeout") + \
    trap("Bẫy 2 — SSH Anywhere", "Mở port 22 cho 0.0.0.0/0 vi phạm quyền tối thiểu. Port 22 chỉ cho My IP; 80/443 mở rộng vì người dùng cần truy cập. (Riêng CD: runner của GitHub cần vào được port 22 — slide CD tr.25 ghi “mở cho IP runner hoặc 0.0.0.0/0”.)", "k7-trap-ssh") + \
    trap("Bẫy 3 — EC2 thuộc mô hình nào", "EC2 = <b>IaaS</b> (thuê máy chủ ảo, tự cài phần mềm). Không phải SaaS/PaaS.", "k7-trap-iaas") + \
    trap("Bẫy 4 — user và key khi SSH", "<code>ssh -i my-key.pem ubuntu@&lt;IP&gt;</code>: <code>my-key.pem</code> là <b>private key</b>, <code>ubuntu</code> là user của AMI Ubuntu. Đổi IP sau khi restart instance → cập nhật địa chỉ (và secret EC2_HOST).", "k7-trap-key") + \
    trap("Bẫy 5 — quên tắt máy", "Free Tier có giới hạn; instance chạy ngoài giới hạn vẫn tính tiền → tắt hoặc xoá khi không dùng, xoá rule cũ.", "k7-trap-cost")

P["checklist"] = [
    "Điện toán đám mây, IaaS/PaaS/SaaS; EC2 thuộc IaaS",
    "Tạo instance: AMI, instance type, key pair (.pem), Public IP; SSH với user ubuntu",
    "Security Group: inbound/outbound, port 22/80/443/8000, nguồn 0.0.0.0/0 hay IP cụ thể, nguyên tắc quyền tối thiểu; chẩn đoán lỗi timeout do SG",
    "Free Tier, dừng/xóa instance để tránh mất tiền; đưa Docker/Compose lên EC2",
    "＋ Vì sao triển khai thật: chạy liên tục, Public IP, truy cập qua Internet",
    "＋ Bảng Nên/Không nên của quyền tối thiểu (xoá rule cũ)",
]

P["quick"] = [
    QQ("EC2 thuộc mô hình dịch vụ nào?", ["SaaS", "PaaS", "IaaS", "On-premise"], "c", "EC2 cho thuê máy chủ ảo — IaaS."),
    QQ("App chạy trên EC2 port 80 nhưng từ trình duyệt bị timeout. Nghi đầu tiên?", ["Thiếu tag latest", "Security Group chưa mở inbound port 80", "Sai Pydantic model", "Thiếu .gitignore"], "b", "SG mặc định chặn phần lớn lưu lượng vào."),
    QQ("Cấu hình nào đúng nguyên tắc quyền tối thiểu?", ["Mở mọi port cho 0.0.0.0/0", "22 cho My IP; 80, 443 cho 0.0.0.0/0", "22 cho 0.0.0.0/0", "Giữ mọi rule cũ"], "b", "Chỉ mở cái cần, SSH giới hạn."),
]

BLOCK = dict(id="K7", mon="TTNT", title="Cloud và EC2", src="cloudcomputing_compressed.pdf", page=P)

QUESTIONS = [
    Q("K7-01", "single", "Which cloud service model does AWS EC2 belong to?", ["Infrastructure as a Service (IaaS)", "Software as a Service (SaaS)", "Platform as a Service (PaaS)", "On-premises hosting"], "a",
      "IaaS: thuê hạ tầng như một dịch vụ, ví dụ máy chủ ảo; người dùng tự cài và quản lý phần mềm. EC2 là dịch vụ IaaS của AWS.", "cloudcomputing.pdf tr.7, 9", "k7-trap-iaas"),
    Q("K7-02", "single", "Which statements about cloud computing (as presented in the lecture) are correct?",
      ["Instead of buying and operating physical servers, you rent computing resources over the Internet.", "Servers can be created in minutes and resources scaled up or down when needed.",
       "You pay for the resources you use and can delete machines when no longer needed.", "All the statements are correct."], "d",
      "Cả ba ý đều là định nghĩa/lợi ích của điện toán đám mây trong slide → “All the statements are correct”.", "cloudcomputing.pdf tr.6", "k7-terms"),
    Q("K7-03", "single", "Which order matches the lecture's steps to create an EC2 instance?",
      ["Choose an AMI → choose an instance type (Free Tier) → create a key pair → launch and wait until ready", "Create a key pair → install Docker → choose an AMI → push to GitHub",
       "Launch → choose an AMI → choose the region's SaaS plan", "Open port 8000 → choose an AMI → delete the key pair"], "a",
      "Thứ tự: AMI → loại máy (ưu tiên Free Tier) → key pair để SSH → khởi tạo và chờ sẵn sàng.", "cloudcomputing.pdf tr.10", "k7-steps"),
    Q("K7-04", "single", "What is an AMI?", ["The operating-system image used to create an instance (for example Ubuntu)", "The firewall attached to the instance", "The private key file used for SSH", "The public IP of the instance"], "a",
      "AMI là ảnh hệ điều hành; chọn AMI nào thì instance chạy hệ điều hành đó.", "cloudcomputing.pdf tr.11", "k7-terms"),
    Q("K7-05", "multi", "You connect with the command below. Which statements are correct?",
      ["<code>my-key.pem</code> is the private key of the key pair.", "<code>ubuntu</code> is the user name used to log in to the instance.", "The .pem file should be committed to GitHub as a backup.", "AWS keeps the matching public key on the instance."], "abd",
      "Key pair: AWS giữ public key trên instance, sinh viên giữ private key và phải bảo quản an toàn — không bao giờ đưa lên Git.", "cloudcomputing.pdf tr.12–13", "k7-trap-key",
      code="ssh -i my-key.pem ubuntu@203.0.113.25", lang="bash"),
    Q("K7-06", "single", "Your container serves HTTP on port 80 of the instance and works with curl from inside the instance, but a browser on your laptop times out. The Security Group only has an inbound rule for port 22. What is the fix?",
      ["Add an inbound rule for port 80 from 0.0.0.0/0.", "Add an outbound rule for port 22.", "Re-create the key pair.", "Change the AMI."], "a",
      "Security Group mặc định chặn phần lớn lưu lượng vào; phải mở đúng port cần dùng. Lỗi timeout khi truy cập từ ngoài là dấu hiệu điển hình.", "cloudcomputing.pdf tr.14–15, 19", "k7-trap-timeout"),
    Q("K7-07", "single", "Which Security Group configuration follows the principle of least privilege for the course project?",
      ["Port 22 from My IP only; ports 80 and 443 from 0.0.0.0/0; remove rules no longer used.", "All ports open to 0.0.0.0/0 to avoid connection problems.",
       "Port 22 from 0.0.0.0/0 so you can connect from anywhere.", "Keep all old rules after the lab in case they are needed again."], "a",
      "Nên: chỉ mở port cần dùng, SSH chỉ My IP, xoá rule thừa. Không nên: mở tất cả, SSH Anywhere, giữ rule cũ.", "cloudcomputing.pdf tr.15–16", "k7-trap-ssh"),
    Q("K7-08", "single", "Why should port 22 be restricted while ports 80 and 443 are open to everyone?",
      ["Port 22 is administrative SSH access only you need; users must reach the website over HTTP/HTTPS from anywhere.", "Port 22 is slower than 80.", "AWS charges extra for port 22.", "Ports 80/443 are encrypted, so they cannot be attacked."], "a",
      "Ghi chú trong slide: giải thích vì sao 22 nên giới hạn còn 80/443 mở rộng để người dùng truy cập.", "cloudcomputing.pdf tr.15", "k7-ports"),
    Q("K7-09", "single", "How do you avoid unexpected AWS charges according to the lecture?",
      ["Choose instance types within the Free Tier and stop or delete instances when not in use.", "Open every port so AWS does not throttle traffic.", "Use a bigger instance type.", "Never create a key pair."], "a",
      "Free Tier có giới hạn loại máy và thời lượng; tắt hoặc xoá instance khi không dùng.", "cloudcomputing.pdf tr.17", "k7-trap-cost"),
    Q("K7-10", "multi", "Which steps belong to putting the Docker stack on EC2 in this lecture?",
      ["SSH into the instance and install Docker and Docker Compose.", "Copy the source and docker-compose.yml to the instance, then run <code>docker compose up -d</code>.",
       "Pass sensitive information through a .env file as in previous sessions.", "Disable the Security Group so the app is reachable."], "abc",
      "Không tắt Security Group; chỉ mở đúng port cần dùng rồi gọi endpoint qua địa chỉ công khai.", "cloudcomputing.pdf tr.18–19", "k7-deploy"),
    Q("K7-11", "single", "Why does the course deploy the application to a cloud server instead of keeping it on the developer's laptop?",
      ["A cloud server runs continuously, has a public IP and can be reached by other people over the Internet.", "The laptop cannot run Docker.", "Cloud servers do not need a firewall.", "It avoids writing a Dockerfile."], "a",
      "Laptop chỉ chạy khi bật, chỉ truy cập trong máy, không có địa chỉ công khai ổn định.", "cloudcomputing.pdf tr.3, 8", "k7-y"),
]
