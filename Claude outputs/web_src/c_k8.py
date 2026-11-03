from h import *

SVG = """<svg viewBox="0 0 700 300" width="700" role="img" aria-label="Pipeline CD dùng registry">
<g font-size="13">
<rect x="8" y="20" width="120" height="54" rx="8" class="box"/><text x="20" y="42" font-weight="700">1 Developer</text><text x="20" y="62">git push</text>
<rect x="160" y="20" width="160" height="54" rx="8" class="boxa"/><text x="172" y="42" font-weight="700">2 GitHub Actions</text><text x="172" y="62">runner: test &amp; build</text>
<rect x="352" y="20" width="160" height="54" rx="8" class="box"/><text x="364" y="42" font-weight="700">3 Registry</text><text x="364" y="62">Docker Hub / ECR</text>
<rect x="160" y="170" width="160" height="54" rx="8" class="boxa"/><text x="172" y="192" font-weight="700">4 SSH trigger</text><text x="172" y="212">appleboy/ssh-action</text>
<rect x="352" y="170" width="160" height="70" rx="8" class="box"/><text x="364" y="192" font-weight="700">5 EC2</text><text x="364" y="210" class="mono" font-size="12">docker compose pull</text><text x="364" y="228" class="mono" font-size="12">docker compose up -d</text>
<rect x="548" y="170" width="140" height="54" rx="8" class="box"/><text x="560" y="192" font-weight="700">6 Live</text><text x="560" y="212">restart container</text>
</g>
<path d="M128 47 h28" class="ln"/><path d="M150 42 l7 5 l-7 5" class="ln"/>
<path d="M320 47 h28" class="ln"/><path d="M342 42 l7 5 l-7 5" class="ln"/>
<text x="300" y="13" font-size="11" class="muted">push image →</text>
<path d="M240 74 v92" class="ln"/><path d="M235 160 l5 7 l5 -7" class="ln"/>
<path d="M320 197 h28" class="ln"/><path d="M342 192 l7 5 l-7 5" class="ln"/>
<text x="300" y="163" font-size="11" class="muted">SSH :22 →</text>
<path d="M432 74 v92" class="ln dash"/><path d="M427 160 l5 7 l5 -7" class="ln"/>
<text x="440" y="122" font-size="11.5" class="muted">EC2 pull image về</text>
<path d="M512 197 h32" class="ln"/><path d="M538 192 l7 5 l-7 5" class="ln"/>
<text x="8" y="112" font-size="12" class="acc">Bước 1–2 = CI (K6)</text><text x="8" y="130" font-size="12" class="acc">Bước 3–6 = CD (K8)</text>
<text x="8" y="270" font-size="12.5">🔑 Private key: secret EC2_SSH_KEY → nạp vào runner · 🔒 Public key: ~/.ssh/authorized_keys trên EC2</text>
<text x="8" y="290" font-size="12.5">Lệnh trong <tspan class="mono">script:</tspan> chạy TRÊN EC2 · step <tspan class="mono">run: curl ...</tspan> (healthcheck) chạy trên runner</text>
</svg>"""

P = {}
P["y"] = """<p><b>CD</b> tự động hoá bước đưa ứng dụng ra máy chủ: sau khi CI test/build đạt, workflow <b>push image lên registry</b>, rồi <b>SSH vào EC2</b> để EC2 <b>pull image mới và chạy</b>. Bí mật (token Docker Hub, IP, SSH key) nằm trong <b>GitHub Secrets</b>, không bao giờ ghi cứng trong YAML hay code.</p>
<p>Câu hỏi cốt lõi của khối: <b>cái gì nằm ở đâu, lệnh nào chạy ở đâu</b> (laptop, runner, registry, EC2).</p>""" + src("CD.pdf tr.2–6")

P["mohinh"] = diagram(SVG, "Kiến trúc CD dùng registry (CD.pdf tr.6, 12, 17, 20)") + table(["Thứ", "Nằm / chạy ở đâu"], [
    ["Build image", "trên <b>runner</b> (không build trên EC2)"],
    ["Image đã build", "<b>registry</b> (Docker Hub / AWS ECR)"],
    ["Private key (.pem)", "secret <code>EC2_SSH_KEY</code> → runner dùng để SSH"],
    ["Public key", "<code>~/.ssh/authorized_keys</code> trên EC2 (tạo ở buổi 8)"],
    ["Lệnh trong <code>script: |</code> của ssh-action", "chạy <b>trên EC2</b> qua kết nối SSH"],
    ["Step <code>run: curl -f ...</code>", "chạy trên <b>runner</b>, gọi vào EC2 qua HTTP"],
    ["File <code>.env</code> production", "trên EC2 (tạo tay hoặc ghi từ Secrets), không có trong Git, không có trong image"],
    ["<code>docker-compose.yml</code>", "trong thư mục dự án trên EC2 (vd <code>/home/ubuntu/app</code>)"],
], ) + src("CD.pdf tr.12, 17–20, 22–23; week5.pdf tr.15")

P["bang"] = """<h3 id="k8-secrets">GitHub Secrets</h3>""" + table(["Secret", "Dùng cho"], [
    [c("DOCKERHUB_USERNAME"), "đăng nhập Docker Hub"], [c("DOCKERHUB_TOKEN"), "Docker <b>Access Token</b> (thay mật khẩu thật, revoke được ngay khi lộ)"],
    [c("EC2_HOST"), "IP / domain của EC2"], [c("EC2_USERNAME"), "user đăng nhập (vd <code>ubuntu</code>)"], [c("EC2_SSH_KEY"), "toàn bộ nội dung file <b>.pem</b> (private key), kể cả dòng <code>-----BEGIN ... PRIVATE KEY-----</code>"]]) + ul([
    "Tạo ở: <b>Settings › Secrets and variables › Actions › New repository secret</b>. Cú pháp dùng: <code>${{ secrets.TEN }}</code>.",
    "Cơ chế: nhập → GitHub <b>mã hoá</b>; workflow chạy mới giải mã, nạp làm biến môi trường trong <b>RAM runner</b> (không lưu đĩa); lỡ in ra log → tự <b>che thành ***</b> (masking).",
    "3 cấp: <b>Organization</b> (dùng chung công ty) · <b>Repository</b> (mọi branch/workflow trong repo — dùng trong bài) · <b>Environment</b> (riêng staging/production, có thể cần Reviewers duyệt).",
    "Rủi ro: hardcode vào .yml/source (lịch sử commit giữ vĩnh viễn) hoặc <code>echo $DB_PASSWORD</code> ra log."]) + src("CD.pdf tr.7–11, 24") + """
<h3 id="k8-push">Build &amp; push image (push-image.yml)</h3>""" + pre("""
name: Build and Push
on:
  push:
    branches: [main]
jobs:
  build-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - name: Build and push
        uses: docker/build-push-action@v5
""", "yaml") + table(["Tag", "Đặc điểm"], [
    [c(":latest"), "luôn trỏ bản build mới nhất trong pipeline → tiện nhưng khó rollback, không biết đang chạy bản nào"],
    [c(":<git-commit-sha>"), "mỗi build một tag duy nhất theo <code>github.sha</code> → truy vết, rollback chính xác"],
    ["Best practice", "gán <b>cả hai</b> tag latest + sha khi push"]]) + "<p>Kiểm tra: log job Build and Push báo xanh → mở Docker Hub/ECR xem Image Digest và Tags vừa xuất hiện.</p>" + src("CD.pdf tr.13–16") + """
<h3 id="k8-ssh">Deploy qua SSH (deploy.yml)</h3>""" + pre("""
- name: Deploy to EC2 via SSH
  uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.EC2_HOST }}
    username: ${{ secrets.EC2_USERNAME }}
    key: ${{ secrets.EC2_SSH_KEY }}
    script: |
      cd /home/ubuntu/app
      docker compose pull
      docker compose up -d
      docker image prune -f

- name: Healthcheck
  run: curl -f http://${{ secrets.EC2_HOST }}:8080/health || exit 1
""", "yaml") + table(["Phần", "Ý nghĩa"], [
    [c("host / username / key"), "thông tin kết nối, lấy từ Secrets (key = private key)"],
    [c("script: |"), "chuỗi lệnh shell chạy <b>trên server EC2</b>"],
    [c("docker compose pull"), "kéo image mới từ registry"], [c("docker compose up -d"), "khởi động lại container ở nền"],
    [c("docker image prune -f"), "xoá dangling image cũ → tránh <b>đầy ổ đĩa</b> sau nhiều lần deploy"],
    [c("curl -f ... || exit 1"), "<code>-f</code>: HTTP lỗi (4xx/5xx) → curl thất bại → <code>exit 1</code> → step đỏ ngay. 200 OK → xanh"]]) + "<p>Chuẩn bị EC2 (buổi 8): Docker + Compose plugin; user chạy docker không cần sudo: <code>usermod -aG docker ubuntu</code>; <code>docker-compose.yml</code> nằm trong thư mục dự án.</p>" + src("CD.pdf tr.18–21, 23") + """
<h3 id="k8-env">.env trên server</h3>""" + table(["Cách", "Mô tả"], [
    ["1 · Tạo sẵn trên EC2", "SSH vào, tạo .env thủ công một lần trong thư mục dự án — đơn giản, hợp cấu hình ít đổi"],
    ["2 · Ghi động từ Secrets", "trong script SSH, dùng Secrets ghi đè tạo .env ngay trước <code>docker compose up</code> — luôn đồng bộ"]]) + "<p>Tuyệt đối không push .env lên Git; image cũng <b>không chứa</b> .env.</p>" + src("CD.pdf tr.22; week5.pdf tr.15") + """
<h3 id="k8-debug">Xử lý sự cố</h3>""" + table(["Triệu chứng", "Nguyên nhân thường gặp", "Cách xử lý"], [
    [c("Permission denied (publickey)"), "private key sai/thiếu (copy thiếu dòng BEGIN…); user không khớp tài khoản trên server; IP EC2 đổi sau restart (không có Elastic IP); SG chặn port 22", "kiểm tra username + key khớp tài khoản được authorize; cập nhật EC2_HOST; mở port 22 cho runner"],
    ["Docker login failed", "sai username, hoặc dùng mật khẩu thật thay vì Access Token", "dùng DOCKERHUB_TOKEN"],
    ["Container crash (Exit Code 1 / 137)", "thiếu biến môi trường trong .env, xung đột port trên EC2", "trên EC2: <code>docker logs &lt;container_id&gt;</code>"],
    ["Healthcheck đỏ", "app chưa lên / trả 5xx", "đọc log từng step, tìm dòng lỗi đầu tiên"]]) + src("CD.pdf tr.24–26")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["Continuous <b>Delivery</b> vs Continuous <b>Deployment</b>", "Delivery: tự động build/test/đóng gói, bước lên Production cần <b>bấm duyệt tay</b>. Deployment: mọi commit qua test đều <b>tự động</b> lên Production, không cần người."],
    ["Build trên runner vs build trên EC2", "Đúng: build ở runner → registry → EC2 chỉ pull về chạy (EC2 nhẹ, image đồng nhất). Sai: build trên EC2 (quá tải CPU/RAM, môi trường không đồng nhất)."],
    ["Private key vs public key", "Private: runner giữ (secret EC2_SSH_KEY) — “chìa”. Public: EC2 giữ trong authorized_keys — “ổ khoá”."],
    [c("script:") + " vs " + c("run:"), "<code>script</code> của ssh-action chạy trên EC2; <code>run</code> của step thường chạy trên runner."],
    [c("docker/login-action") + " vs " + c("docker/build-push-action"), "login: đăng nhập registry bằng Secrets. build-push: build và push image trong một bước."],
    [c(":latest") + " vs " + c(":sha"), "latest tiện nhưng khó rollback; sha duy nhất, rollback chính xác. Gán cả hai."],
    ["Access Token vs mật khẩu", "Token an toàn hơn, revoke được ngay khi lộ; dùng mật khẩu thật dễ gây login failed."],
    ["Thao tác tay vs CD", "Tay: SSH gõ lệnh, 30–40 phút, dễ sai, phụ thuộc cá nhân. CD: push là chạy, &lt;3 phút, chuẩn hoá, rollback dễ."],
    [c("Permission denied (publickey)") + " vs timeout", "publickey: server đã trả lời nhưng <b>từ chối xác thực</b> → kiểm tra user/key. Timeout: không tới được (SG/IP/mạng)."],
]) + src("CD.pdf tr.4–5, 12, 14–15, 17, 25–26; cloudcomputing.pdf tr.15")

P["bay"] = trap("Bẫy 1 — trình tự kiến trúc (Q6)", "Đúng: <b>Push code → test/build → publish image → EC2 pulls and runs it</b>. Các phương án “build on EC2”, “SSH to EC2 then build locally”, “publish source files” đều sai mô hình registry.", "k8-trap-arch") + \
    trap("Bẫy 2 — ai giữ khoá nào (Q8)", "<b>Private key cấp cho runner</b> (qua secret), <b>public key được authorize trên EC2</b>. Đảo lại (public key trong EC2_SSH_KEY, private key nằm trên EC2/ trong image/ trong log) đều sai.", "k8-trap-key") + \
    trap("Bẫy 3 — <code>script</code> chạy ở đâu (Q9)", "Lệnh dưới <code>script:</code> chạy <b>trên EC2</b> (host đã SSH tới) — không phải trong runner, không phải terminal local, không phải Docker Hub.<br><b>Đổi một chỗ:</b> viết cùng các lệnh đó trong một step <code>run:</code> → chúng chạy trên runner (sai chỗ).", "k8-trap-script") + \
    trap("Bẫy 4 — healthcheck gặp 503 (Q10)", "<code>curl -f</code> coi HTTP ≥ 400 là thất bại → <code>|| exit 1</code> → step đỏ ngay. Không tự rollback, không tự retry, nhận được response không có nghĩa là pass.<br><b>Đổi một chỗ:</b> bỏ <code>-f</code> → curl coi 503 là thành công (vẫn nhận được trang lỗi) → step xanh dù app lỗi.", "k8-trap-health") + \
    trap("Bẫy 5 — <code>Permission denied (publickey)</code> (Q11)", "Server đã phản hồi và <b>từ chối xác thực</b> → kiểm tra <b>username và key có khớp tài khoản được authorize</b>. Port container, tag latest, endpoint JSON không liên quan.", "k8-trap-perm") + \
    trap("Bẫy 6 — lộ secret", "In <code>echo ${{ secrets.X }}</code> ra log: GitHub che thành <code>***</code>, nhưng hardcode trong YAML thì lộ vĩnh viễn trong lịch sử commit.")

P["checklist"] = [
    "Continuous Delivery (cần duyệt tay trước khi deploy) và Continuous Deployment (deploy tự động)",
    "Kiến trúc dùng registry: push → test/build → push image → EC2 pull về và chạy; vì sao không build trên EC2",
    "GitHub Secrets: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, EC2_HOST, EC2_USERNAME, EC2_SSH_KEY; cú pháp ${{ secrets.X }}; rủi ro lộ key",
    "docker/login-action, build-push-action, tag image (latest, SHA); appleboy/ssh-action: phần script chạy trên EC2",
    "Healthcheck bằng curl -f ... || exit 1; debug các lỗi Permission denied (publickey), timeout, pull thất bại",
    "＋ Secret masking ***, 3 cấp Secrets (Organization / Repository / Environment)",
    "＋ docker image prune -f sau deploy; usermod -aG docker ubuntu; 2 cách tạo .env trên EC2",
    "＋ Container crash Exit 1/137 → docker logs; Docker login failed → dùng Access Token",
]

P["quick"] = [
    QQ("Trong <code>appleboy/ssh-action</code>, các lệnh dưới <code>script: |</code> chạy ở đâu?", ["Trên runner", "Trên EC2", "Trên Docker Hub", "Trên laptop"], "b", "Script chạy trên host đã SSH tới (EC2)."),
    QQ("Healthcheck <code>curl -f http://host:8080/health || exit 1</code>, server trả 500. Kết quả?", ["Step xanh vì có response", "Step đỏ (exit 1)", "GitHub tự rollback", "Tự retry đến khi khỏe"], "b", "-f làm curl thất bại với HTTP lỗi → exit 1."),
    QQ("Mọi commit qua test đều tự lên Production, không cần người duyệt. Đó là:", ["Continuous Integration", "Continuous Delivery", "Continuous Deployment", "Manual deploy"], "c", "Delivery cần một nút duyệt tay; Deployment thì không."),
]

BLOCK = dict(id="K8", mon="TTNT", title="CD và triển khai tự động", src="CD.pdf", page=P)

SSH = """- uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.EC2_HOST }}
    username: ${{ secrets.EC2_USERNAME }}
    key: ${{ secrets.EC2_SSH_KEY }}
    script: |
      cd /home/ubuntu/app
      docker compose pull
      docker compose up -d"""

QUESTIONS = [
    Q("K8-D06", "single", "Which sequence matches the registry-based continuous deployment architecture?",
      ["Push code → SSH to EC2 → build locally → run tests on GitHub.", "Push code → pull an image → build on EC2 → upload test results.",
       "Push code → restart EC2 → publish source files → create an image.", "Push code → test/build → publish image → EC2 pulls and runs it."], "d",
      "Kiến trúc CD: developer push → GitHub Actions test & build → push image lên registry → SSH trigger → EC2 pull image mới → restart container. Không build trên EC2.", "CD.pdf tr.6, 12; đề mẫu Q6", "k8-trap-arch", demo=6),
    Q("K8-D08", "single", "For SSH public-key authentication from the runner to EC2, which pairing is appropriate?",
      ["Docker token in EC2_SSH_KEY; public key in the image registry.", "Private key in the Docker image; matching password in the workflow name.",
       "Public key in EC2_SSH_KEY; private key in EC2's application logs.", "Private key supplied to the runner; matching public key authorized on EC2."], "d",
      "Runner giữ “chìa” (private key từ secret EC2_SSH_KEY), EC2 giữ “ổ khoá” (public key trong ~/.ssh/authorized_keys).", "CD.pdf tr.17; đề mẫu Q8", "k8-trap-key", demo=8),
    Q("K8-D09", "single", "Consider:", ["Inside Docker Hub's image-storage environment.", "In the developer's currently open local terminal.", "Inside the GitHub Actions' runner.", "On the EC2 host reached through the SSH connection"], "d",
      "appleboy/ssh-action mở kết nối SSH từ runner tới EC2; <code>script</code> là chuỗi lệnh shell sẽ chạy <b>trên server</b>.", "CD.pdf tr.19–20; đề mẫu Q9", "k8-trap-script",
      code=SSH, lang="yaml", demo=9, hoi="Where do the commands under <code>script</code> execute?"),
    Q("K8-D10", "single", "A GitHub Actions step runs the command below. The server returns HTTP 503.", ["Curl reports failure, and the shell command exits unsuccessfully.", "GitHub automatically restores the previously deployed image.",
       "The step passes because an HTTP response was received.", "The step retries until the application becomes healthy."], "a",
      "<code>curl -f</code> thất bại với mã HTTP lỗi (503) → vế <code>|| exit 1</code> chạy → step fail, workflow đỏ ngay (Fail Fast). Không có rollback/retry tự động.", "CD.pdf tr.23; đề mẫu Q10", "k8-trap-health",
      code="- name: Healthcheck\n  run: curl -f http://${{ secrets.EC2_HOST }}:8080/health || exit 1", lang="yaml", demo=10, hoi="What happens?"),
    Q("K8-D11", "single", "SSH reports: <code>Permission denied (publickey)</code>\nThe error is an authentication rejection from the intended server. Which check is most directly relevant?",
      ["Whether the application exposes container port 8000.", "Whether the SSH username and key match the server's authorized account.", "Whether the Docker image has a latest tag.", "Whether the HTTP health endpoint returns JSON."], "b",
      "Lỗi xác thực SSH → kiểm tra cặp username + private key có khớp tài khoản đã authorize public key trên server (copy thiếu dòng BEGIN, sai user…). Các phương án khác không liên quan tới SSH.", "CD.pdf tr.25; đề mẫu Q11", "k8-trap-perm", demo=11),
    Q("K8-06", "single", "A team's pipeline builds, tests and packages automatically, but a person must press an approval button before the release reaches production. Which practice is this?",
      ["Continuous Integration only", "Continuous Delivery", "Continuous Deployment", "Infrastructure as a Service"], "b",
      "Continuous Delivery: bước đẩy lên Production cần một nút bấm duyệt thủ công. Continuous Deployment: tự động hoàn toàn.", "CD.pdf tr.5", "k8-y"),
    Q("K8-07", "single", "Which statements about GitHub Secrets are correct?",
      ["Secret values are encrypted after being entered in Settings.", "They are decrypted only when a workflow runs and loaded as environment variables in the runner's memory.",
       "If a secret is accidentally printed to the log, GitHub replaces it with <code>***</code>.", "All the statements are correct."], "d",
      "Ba cơ chế trong slide: nhập &amp; mã hoá · nạp vào RAM runner khi chạy (không lưu đĩa) · tự che (masking) thành ***. Cả ba đều đúng → chọn “All the statements are correct”.", "CD.pdf tr.8, 24", "k8-secrets"),
    Q("K8-08", "single", "Why does the lecture build the image on the runner and push it through a registry instead of copying the source to EC2 and building there?",
      ["Building on EC2 overloads its CPU/RAM and gives inconsistent build environments; EC2 should only pull and run.", "EC2 cannot run Docker.", "Registries run the containers for EC2.", "SSH cannot copy files."], "a",
      "Cách đúng: build ở runner → Docker Hub/ECR → EC2 chỉ pull về chạy: EC2 nhẹ, image đồng nhất ở mọi môi trường.", "CD.pdf tr.12", "k8-trap-arch"),
    Q("K8-09", "multi", "Which statements about tagging images in this pipeline are correct?",
      ["Pushing <code>:latest</code> on every build is convenient but makes it hard to know which version is running.", "A tag based on the commit SHA (<code>github.sha</code>) lets you trace and roll back exactly.",
       "Best practice is to push both the latest tag and the commit-SHA tag.", "A SHA tag forces EC2 to rebuild the image from source."], "abc",
      "Slide: latest tiện nhưng khó rollback; sha duy nhất cho mỗi build; best practice gán cả hai. Tag không liên quan tới việc build lại.", "CD.pdf tr.15", "k8-push"),
    Q("K8-10", "single", "Why does the deploy script end with <code>docker image prune -f</code>?",
      ["To delete dangling old images so the EC2 disk does not fill up after many deployments.", "To stop all running containers.", "To push the new image to Docker Hub.", "To remove the .env file."], "a",
      "Mỗi lần deploy tải image mới, image cũ tích tụ → đầy ổ đĩa; prune xoá các dangling image không còn dùng.", "CD.pdf tr.21", "k8-ssh",
      code="script: |\n  cd /home/ubuntu/app\n  docker compose pull\n  docker compose up -d\n  docker image prune -f", lang="yaml"),
    Q("K8-11", "multi", "Consider the login step. Which statements are correct?",
      ["It logs in using a Docker access token instead of the real password, which can be revoked if leaked.", "Secret values are referenced with the <code>${{ secrets.NAME }}</code> syntax.",
       "The token will appear in plain text in the job log.", "This step also builds and pushes the image."], "ab",
      "login-action chỉ đăng nhập; build &amp; push là việc của <code>docker/build-push-action</code>. Secret in ra log bị che thành ***.", "CD.pdf tr.13–14, 24", "k8-push",
      code="- name: Log in to Docker Hub\n  uses: docker/login-action@v3\n  with:\n    username: ${{ secrets.DOCKERHUB_USERNAME }}\n    password: ${{ secrets.DOCKERHUB_TOKEN }}", lang="yaml"),
    Q("K8-12", "single", "After a deploy, the container on EC2 keeps crashing with exit code 1. Following the lecture, what should you run on EC2 first?",
      ["<code>docker logs &lt;container_id&gt;</code>", "<code>git push --force</code>", "<code>docker image prune -f</code>", "<code>ssh-keygen</code>"], "a",
      "Container crash (Exit 1/137) thường do thiếu biến môi trường trong .env hoặc xung đột port; <code>docker logs</code> hiển thị nguyên nhân lỗi của ứng dụng.", "CD.pdf tr.26", "k8-debug"),
    Q("K8-13", "multi", "How can the production <code>.env</code> be provided on EC2 according to the lecture?",
      ["Create it manually once on EC2 in the project directory.", "Write it from GitHub Secrets inside the SSH script right before <code>docker compose up</code>.",
       "Commit it to the repository so the runner can copy it.", "Bake it into the Docker image so EC2 does not need it."], "ab",
      "Hai cách hợp lệ: tạo sẵn thủ công, hoặc ghi động từ Secrets. Không push .env lên Git; image cũng không được chứa .env.", "CD.pdf tr.22; week5.pdf tr.15", "k8-env"),
]
