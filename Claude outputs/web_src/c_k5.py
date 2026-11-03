from h import *

SVG = """<svg viewBox="0 0 700 270" width="700" role="img" aria-label="Dockerfile tạo image, image tạo nhiều container; client, daemon, registry">
<g font-size="13">
<rect x="8" y="30" width="120" height="60" rx="8" class="box"/><text x="22" y="56" font-weight="700">Dockerfile</text><text x="22" y="76" class="muted">công thức</text>
<path d="M128 60 h40" class="ln"/><path d="M162 55 l7 5 l-7 5" class="ln"/><text x="132" y="50" class="mono" font-size="11">build</text>
<rect x="172" y="12" width="170" height="104" rx="8" class="boxa"/><text x="184" y="32" font-weight="700">Image (chỉ đọc)</text>
<rect x="186" y="42" width="142" height="18" class="box"/><text x="192" y="56" font-size="11.5">layer: COPY . .</text>
<rect x="186" y="62" width="142" height="18" class="box"/><text x="192" y="76" font-size="11.5">layer: RUN pip install</text>
<rect x="186" y="82" width="142" height="18" class="box"/><text x="192" y="96" font-size="11.5">base: python:3.12-slim</text>
<path d="M342 50 C380 30 390 30 410 30" class="ln"/><path d="M342 64 h68" class="ln"/><path d="M342 78 C380 98 390 98 410 98" class="ln"/>
<text x="350" y="134" class="mono" font-size="11">run (1 image → nhiều container)</text>
<rect x="412" y="12" width="140" height="34" rx="6" class="box"/><text x="420" y="34" font-size="12">container A + lớp ghi</text>
<rect x="412" y="50" width="140" height="30" rx="6" class="box"/><text x="420" y="70" font-size="12">container B + lớp ghi</text>
<rect x="412" y="84" width="140" height="30" rx="6" class="box"/><text x="420" y="104" font-size="12">container C + lớp ghi</text>
<text x="566" y="40" font-size="12" class="muted">mỗi container có</text><text x="566" y="56" font-size="12" class="muted">danh tính &amp; trạng thái</text><text x="566" y="72" font-size="12" class="muted">riêng, dùng chung</text><text x="566" y="88" font-size="12" class="muted">kernel của host</text>
<rect x="8" y="170" width="150" height="56" rx="8" class="box"/><text x="20" y="192" font-weight="700">Client</text><text x="20" y="212" class="mono" font-size="12">docker run/build…</text>
<path d="M158 198 h56" class="ln"/><path d="M208 193 l7 5 l-7 5" class="ln"/><text x="160" y="190" font-size="11" class="muted">gửi lệnh</text>
<rect x="218" y="160" width="230" height="76" rx="8" class="boxa"/><text x="230" y="182" font-weight="700">Docker daemon (host)</text><text x="230" y="202" font-size="12">tạo &amp; quản lý image, container,</text><text x="230" y="220" font-size="12">network, volume</text>
<path d="M448 198 h56" class="ln"/><path d="M498 193 l7 5 l-7 5" class="ln"/><path d="M506 210 h-56" class="ln dash"/><text x="452" y="190" font-size="11" class="muted">pull / push</text>
<rect x="508" y="170" width="180" height="56" rx="8" class="box"/><text x="520" y="192" font-weight="700">Registry</text><text x="520" y="212" font-size="12">Docker Hub: phân phối image</text>
<text x="8" y="258" font-size="12.5">Registry chỉ lưu/phân phối image — <tspan font-weight="700">không chạy</tspan> container. Daemon mới chạy container trên host.</text>
</g></svg>"""

P = {}
P["y"] = """<p><b>Docker</b> đóng gói ứng dụng + mọi thứ nó cần (thư viện, runtime, cấu hình) thành một <b>image</b> di động, rồi chạy image đó thành <b>container</b> cô lập. Giải bài toán “máy em chạy được, server thì không” (thiếu thư viện, khác phiên bản, khác cấu hình).</p>
<p>Ba động từ: <b>Build</b> (Dockerfile → image) · <b>Share</b> (registry như Docker Hub) · <b>Run</b> (image → một hoặc nhiều container).</p>""" + src("week5.pdf tr.2–4")

P["mohinh"] = diagram(SVG, "Dockerfile → Image → Container; Client → Daemon → Registry (week5.pdf tr.4, 6, 8–12)") + """
<h3 id="k5-run-steps">Điều gì xảy ra khi chạy <code>docker run --rm hello-world</code></h3>
<ol><li>Kiểm tra image hello-world có sẵn ở local chưa.</li><li>Chưa có → <b>pull</b> từ registry.</li><li>Tạo <b>container mới</b> từ image.</li><li>Chạy process mặc định của container.</li><li>In kết quả ra terminal.</li><li>Container thoát → <b>bị xoá</b> nhờ <code>--rm</code> (image vẫn còn).</li></ol>""" + src("week5.pdf tr.7")

P["bang"] = """<h3 id="k5-cmd">Lệnh hay dùng</h3>""" + table(["Lệnh", "Tác dụng"], [
    [c("docker run --rm IMAGE"), "chạy container ngắn hạn, tự xoá khi dừng"],
    [c("docker run -it --name ubuntu-lab ubuntu:24.04 bash"), "chạy tương tác (gắn terminal), đặt tên container"],
    [c("docker run -d --name web -p 8080:80 nginx:alpine"), "chạy nền (<code>-d</code>); map <b>host 8080 → container 80</b>"],
    [c("docker run ... --env-file .env chatbot-api:1.0"), "nạp biến môi trường từ file .env lúc chạy"],
    [c("docker ps") + " / " + c("docker ps -a"), "container đang chạy / tất cả, kể cả đã dừng"],
    [c("docker start -ai ubuntu-lab"), "khởi động lại container đã dừng và gắn vào"],
    [c("docker stop web") + " · " + c("docker rm web"), "dừng · xoá container (image vẫn còn)"],
    [c("docker logs web"), "xem log của container"],
    [c("docker exec -it web bash"), "chạy thêm một process trong container đang chạy"],
    [c("docker pull nginx:alpine") + " · " + c("docker images"), "tải image · liệt kê image local"],
    [c("docker image inspect nginx:alpine"), "xem chi tiết/metadata, danh sách layer"],
    [c("docker image history nginx:alpine"), "xem lịch sử build (các layer)"],
    [c("docker build -t chatbot-api:1.0 ."), "build image từ Dockerfile, <code>.</code> = build context"],
    [c("docker tag chatbot-api:1.0 yourusername/chatbot-api:1.0"), "gắn tên kèm namespace Docker Hub"],
    [c("docker login --username yourusername") + " → " + c("docker push yourusername/chatbot-api:1.0"), "đăng nhập rồi đẩy image lên Docker Hub"],
    [c("docker pull yourusername/chatbot-api:1.0"), "kéo về máy khác (repo private → login trước)"],
]) + note("Image <b>không được</b> chứa <code>.env</code>: phải tạo .env trên máy chạy container.", "warn") + src("week5.pdf tr.7–15; Docker Deep Dive tr.96 (exec)") + """
<h3 id="k5-naming">Tên image</h3><p><code>nginx:alpine</code> → <b>nginx</b> là repository, <b>alpine</b> là tag (biến thể/phiên bản). Repository gom các image liên quan; registry chứa nhiều repository. Không ghi tag → mặc định <code>latest</code>.</p>""" + src("week5.pdf tr.8; Docker Deep Dive tr.69–71") + """
<h3 id="k5-dockerfile">Dockerfile của app chatbot (llm_app)</h3>""" + pre("""
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
RUN useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
""", "dockerfile") + table(["Lệnh", "Vai trò"], [
    [c("FROM"), "image nền (lớp đầu tiên)"], [c("WORKDIR"), "thư mục làm việc trong image"], [c("COPY"), "chép file từ build context vào image (tạo layer)"],
    [c("RUN"), "chạy lệnh lúc build (tạo layer)"], [c("EXPOSE"), "<b>ghi chú</b> cổng app dùng (metadata) — không tự mở cổng ra host, vẫn cần <code>-p</code>"],
    [c("CMD"), "lệnh mặc định khi container khởi động (ghi đè được khi <code>docker run</code>)"]]) + """
<p id="k5-cache"><b>Layer cache &amp; .dockerignore</b> (từ code mẫu, slide không nói): <code>COPY requirements.txt .</code> + <code>RUN pip install</code> đặt <b>trước</b> <code>COPY . .</code> để khi chỉ sửa code, Docker dùng lại layer cài thư viện thay vì cài lại. <code>.dockerignore</code> của llm_app loại <code>.env</code>, <code>.git</code>, <code>__pycache__/</code>, <code>.venv/</code>… khỏi build context → .env không lọt vào image.</p>""" + src("materials/llm_app/completed/Dockerfile, .dockerignore; Docker Deep Dive tr.112–116 (layer vs metadata)")

P["sosanh"] = table(["Đặc điểm", "Image", "Container"], [
    ["Mục đích", "khuôn mẫu (template) để tạo container", "instance chạy được của image"],
    ["Trạng thái", "bất biến, chỉ đọc (các layer read-only)", "có <b>lớp ghi mỏng</b> (writable layer)"],
    ["Thực thi", "tự nó không chạy", "chạy một hoặc nhiều process"],
    ["Lưu ở", "cache image local hoặc registry", "trên Docker host"],
    ["Số lượng", "một image dùng lại nhiều lần", "mỗi container có danh tính &amp; trạng thái riêng"],
    ["Vòng đời", "pull, build, tag, push, remove", "create, start, stop, restart, remove"],
    ["Ví von", "class / gói cài đặt", "object / ứng dụng đang chạy"],
]) + src("week5.pdf tr.12") + table(["Cặp", "Phân biệt"], [
    ["Container vs VM", "Container dùng chung <b>kernel</b> của host OS → nhẹ, khởi động nhanh; VM mỗi máy một hệ điều hành riêng."],
    ["client vs daemon vs registry", "client gửi lệnh; daemon tạo/quản lý image, container, network, volume; registry phân phối image cho host pull. Registry <b>không</b> chạy container."],
    [c("-p 8080:80"), "<b>host:container</b> — truy cập <code>localhost:8080</code> trên máy host để tới cổng 80 trong container."],
    [c("-d") + " vs " + c("-it"), "-d chạy nền; -it tương tác, gắn terminal."],
    [c("stop") + " vs " + c("rm") + " vs " + c("--rm"), "stop: dừng, container còn (thấy ở ps -a). rm: xoá container. --rm: tự xoá container khi nó dừng. Không lệnh nào xoá image."],
    [c("docker run") + " vs " + c("docker start"), "run tạo container <b>mới</b> từ image; start khởi động lại container đã có."],
    ["repository vs tag", "nginx (repo) : alpine (tag)."],
]) + src("week5.pdf tr.5–6, 10–14; Docker Deep Dive tr.87–91")

P["bay"] = trap("Bẫy 1 — “máy em chạy được” (Q18)", "Thiếu thư viện trên server → giải pháp Docker trực tiếp: <b>đóng gói app + thư viện cần thiết vào image</b>. Không “thay kernel server”, không “dùng thư viện cài sẵn của server”, không “copy log vào registry”.", "k5-trap-q18") + \
    trap("Bẫy 2 — ai làm gì trong nền tảng Docker (Q19)", "Client gửi request tới daemon ✓ · daemon quản lý container &amp; image local ✓ · registry phân phối image để host pull ✓ · registry <b>chạy</b> process của container ✗.", "k5-trap-q19") + \
    trap("Bẫy 3 — image vs container (Q20)", "Container có lớp ghi cho thay đổi lúc chạy ✓ · image là template để tạo container ✓ · “mỗi image chỉ tạo được một container” ✗ (một image → nhiều container) · “dừng container biến lớp ghi thành image” ✗ (dừng thì container vẫn là container, dữ liệu còn đó).", "k5-trap-q20") + \
    trap("Bẫy 4 — <code>--rm</code> xoá gì?", "Chỉ xoá <b>container</b> sau khi nó thoát. Image vẫn còn trong <code>docker images</code>.<br><b>Đổi một chỗ:</b> bỏ <code>--rm</code> → container đã thoát vẫn nằm trong <code>docker ps -a</code>.", "k5-trap-rm") + \
    trap("Bẫy 5 — thứ tự cổng trong <code>-p</code>", "<code>-p 8080:80</code>: host 8080 → container 80. <b>Đổi một chỗ:</b> <code>-p 80:8080</code> → phải gọi cổng 80 trên host, app trong container phải nghe 8080.", "k5-trap-port") + \
    trap("Bẫy 6 — container sống bao lâu", "Container còn chạy khi <b>process chính</b> còn chạy. <code>docker run -it ubuntu bash</code> rồi gõ <code>exit</code> → bash kết thúc → container dừng (vẫn thấy bằng <code>docker ps -a</code>, khởi động lại bằng <code>docker start -ai</code>).", "k5-trap-life")

P["checklist"] = [
    "Bài toán “máy em chạy được” và cách Docker giải quyết; container và VM (container dùng chung kernel)",
    "Kiến trúc: client → daemon → registry; repository và tag (nginx:alpine)",
    "Image (các layer chỉ đọc, là template) và container (thêm một layer ghi được); một image tạo được nhiều container",
    "docker run (--rm, -it, -d, -p host:container, --name, -e), ps -a, stop, rm, images, pull, inspect, history, logs, exec",
    "Dockerfile cho app chatbot: FROM, WORKDIR, COPY, RUN, EXPOSE, CMD; thứ tự lệnh để tận dụng layer cache; .dockerignore; build -t, push",
    "＋ 6 bước của docker run --rm hello-world; --env-file .env; image KHÔNG chứa .env",
    "＋ docker tag + login + push lên Docker Hub; pull ở máy khác (repo private phải login)",
]

P["quick"] = [
    QQ("<code>docker run -d -p 5000:8000 api</code>. Gọi URL nào trên máy host để tới app nghe cổng 8000 trong container?", ["http://localhost:8000", "http://localhost:5000", "http://container:5000", "http://localhost:80"], "b", "-p host:container → host 5000."),
    QQ("Sau <code>docker run --rm hello-world</code> kết thúc, điều gì còn lại?", ["Container và image", "Chỉ container", "Chỉ image hello-world", "Không còn gì"], "c", "--rm xoá container khi thoát; image vẫn ở local."),
    QQ("Thành phần nào tạo và quản lý container trên host?", ["Registry", "Docker client", "Docker daemon", "Docker Hub"], "c", "Client gửi lệnh, daemon tạo/quản lý, registry phân phối image."),
]

P["docthem"] = ul([
    "<b>Multi-stage build</b>: một Dockerfile nhiều <code>FROM</code>, <code>COPY --from=stage</code> chỉ chép thứ cần chạy → image production nhỏ hơn (Docker Deep Dive tr.118–123).",
    "<b>Lệnh nào tạo layer</b>: FROM, RUN, COPY tạo layer; EXPOSE, WORKDIR, ENV, ENTRYPOINT chỉ thêm metadata (tr.116).",
    "<b>CMD và ENTRYPOINT</b>: cả hai đặt chương trình mặc định khi container chạy; lệnh mặc định (Cmd) bị ghi đè nếu truyền lệnh khác vào <code>docker container run</code> (tr.103, 116).",
    "<b>Tag có thể đổi, digest thì không</b>: cùng tag có thể trỏ image khác; digest sha256 là hash nội dung, pull theo <code>alpine@sha256:...</code> (tr.78–80). <code>latest</code> không đảm bảo là mới nhất (tr.71–73).",
    "<b>stop và rm -f</b>: <code>docker container stop</code> gửi SIGTERM cho PID 1, chờ 10 giây rồi SIGKILL; <code>rm -f</code> SIGKILL ngay (tr.100–101).",
    "<b>Không xoá được image</b> khi còn container (kể cả đã dừng) dùng nó → lỗi conflict (tr.66, 84).",
    "<b>exec vs exit</b>: thoát shell mở bằng <code>docker exec</code> không làm dừng container vì process chính vẫn chạy; Ctrl-PQ tách terminal mà không dừng (tr.95–96).",
])

BLOCK = dict(id="K5", mon="TTNT", title="Docker cơ bản", src="week5.pdf · Docker Deep Dive · llm_app/Dockerfile", page=P)

import os
DF = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "materials", "llm_app", "completed", "Dockerfile")).read().strip()

QUESTIONS = [
    Q("K5-D18", "single", "An application works on a developer's laptop but fails on a server because a required library is missing. Which Docker approach most directly addresses this problem?",
      ["Replace the server's operating-system kernel with the laptop's.", "Package the application and its required libraries in an image.", "Copy the application's logs into a shared registry.", "Run the application using the server's installed libraries."], "b",
      "Cách tiếp cận của Docker: đóng gói ứng dụng cùng môi trường nó cần (thư viện, runtime, cấu hình) rồi chạy nhất quán ở mọi nơi. Container dùng chung kernel của host nên không thay kernel.", "week5.pdf tr.3; đề mẫu Q18", "k5-trap-q18", demo=18),
    Q("K5-D19", "multi", "Which statements correctly describe the Docker platform?",
      ["The client sends requests to the Docker daemon.", "The daemon manages containers and local images.", "A registry distributes images that hosts can pull.", "A registry executes each container's main process."], "abc",
      "Kiến trúc: client gửi lệnh tới daemon; daemon tạo và quản lý image, container, network, volume; registry cung cấp image để host pull. Registry không chạy container.", "week5.pdf tr.6; đề mẫu Q19", "k5-trap-q19", demo=19),
    Q("K5-D20", "multi", "Which statement(s) correctly distinguish an Docker image from a container?",
      ["A container has a writable layer for runtime file changes.", "An image provides the template used to create containers.", "Each image can be used to create only one container.", "Stopping a container converts its writable layer into an image."], "ab",
      "Image: template bất biến, chỉ đọc. Container: instance chạy được, có lớp ghi mỏng. Một image tạo được nhiều container. Dừng container không biến nó thành image.", "week5.pdf tr.8, 10, 12; đề mẫu Q20", "k5-trap-q20", demo=20),
    Q("K5-04", "multi", "What does Docker do when this command is executed?",
      ["Checks whether the hello-world image exists locally and pulls it from a registry if it is missing.", "Creates a new container from the image and starts its default process.",
       "Removes the container after it exits because of <code>--rm</code>.", "Removes the hello-world image after the container exits."], "abc",
      "6 bước trong slide: kiểm tra image local → pull nếu chưa có → tạo container mới → chạy process mặc định → in kết quả → xoá container khi thoát (vì --rm). Image vẫn còn.", "week5.pdf tr.7", "k5-run-steps", code="docker run --rm hello-world", lang="bash"),
    Q("K5-05", "single", "After running the command below on your machine, which request reaches the nginx server inside the container?",
      ["<code>curl http://localhost:8080</code>", "<code>curl http://localhost:80</code> only", "<code>curl http://web:8080</code> from the registry", "No request can reach it because of <code>-d</code>"], "a",
      "<code>-p 8080:80</code> = host 8080 → container 80. <code>-d</code> chỉ cho container chạy nền.", "week5.pdf tr.13", "k5-trap-port", code="docker run -d --name web -p 8080:80 nginx:alpine", lang="bash"),
    Q("K5-06", "single", "In the image name <code>nginx:alpine</code>, what is <code>alpine</code>?", ["The repository name", "The tag identifying a variant/version", "The registry host", "The container name"], "b",
      "nginx là repository, alpine là tag.", "week5.pdf tr.8", "k5-naming"),
    Q("K5-07", "single", "What does the final command show?",
      ["The nginx image is still listed, because removing a container does not remove its image.", "Nothing, because <code>docker rm</code> deleted the image.", "The web container.", "An error: the image was removed by <code>docker stop</code>."], "a",
      "stop dừng container, rm xoá container; image vẫn còn trong cache local.", "week5.pdf tr.13", "k5-trap-rm",
      code="docker run -d --name web -p 8080:80 nginx:alpine\ndocker stop web\ndocker rm web\ndocker images nginx", lang="bash"),
    Q("K5-08", "multi", "Which statements match the lecture's image vs. container comparison?",
      ["An image does not execute by itself.", "Each container has its own identity and state.", "A container is stored only in the registry.", "An image's lifecycle includes pull, build, tag, push and remove."], "abd",
      "Container được lưu trên Docker host (không phải registry). Image lưu trong cache local hoặc registry.", "week5.pdf tr.12", "k5-sosanh"),
    Q("K5-09", "single", "Why do containers normally require fewer resources than complete virtual machines?",
      ["They share the host operating-system kernel instead of running a full OS each.", "They do not have a filesystem.", "They run only inside the registry.", "They cannot run more than one process."], "a",
      "Isolation: các ứng dụng chạy trong môi trường riêng nhưng dùng chung kernel của host OS; VM phải chạy hệ điều hành đầy đủ cho mỗi máy.", "week5.pdf tr.5; Docker Deep Dive tr.87, 91", "k5-sosanh"),
    Q("K5-10", "single", "You built <code>chatbot-api:1.0</code> locally and want it on Docker Hub under account <code>yourusername</code>. Which sequence matches the lecture?",
      ["<code>docker login</code> → <code>docker tag chatbot-api:1.0 yourusername/chatbot-api:1.0</code> → <code>docker push yourusername/chatbot-api:1.0</code>",
       "<code>docker push chatbot-api:1.0</code> → <code>docker tag</code> → <code>docker login</code>", "<code>docker commit</code> → <code>docker run</code> → <code>docker push</code>", "<code>docker pull yourusername/chatbot-api:1.0</code> → <code>docker build</code>"], "a",
      "Đăng nhập, gắn tag có namespace tài khoản, rồi push. Máy khác pull bằng cùng tên (repo private phải login trước).", "week5.pdf tr.15", "k5-cmd"),
    Q("K5-11", "multi", "Which statements about this command are correct?",
      ["<code>--env-file .env</code> passes the variables in .env to the container at run time.", "<code>-p 8000:8000</code> maps host port 8000 to container port 8000.",
       "<code>--rm</code> deletes the image <code>chatbot-api:1.0</code> when the container stops.", "The image must contain the .env file for this command to work."], "ab",
      "--rm chỉ xoá container. Slide nhấn mạnh image KHÔNG được chứa .env; tạo .env trên máy chạy và truyền vào bằng --env-file.", "week5.pdf tr.14–15", "k5-cmd",
      code="docker run --rm \\\n  --name chatbot-api \\\n  -p 8000:8000 \\\n  --env-file .env \\\n  chatbot-api:1.0", lang="bash"),
    Q("K5-12", "single", "You start a container, then type <code>exit</code> inside it. What is true afterwards?",
      ["The container stops because its main process (bash) ended; <code>docker ps -a</code> still lists it and <code>docker start -ai ubuntu-lab</code> can restart it.",
       "The container keeps running in the background.", "The container and the ubuntu image are both deleted.", "The container is converted into a new image."], "a",
      "Container hoạt động khi process chính còn chạy; process thoát → container dừng (không bị xoá vì không có --rm).", "week5.pdf tr.10–11", "k5-trap-life",
      code="docker run -it --name ubuntu-lab ubuntu:24.04 bash", lang="bash"),
    Q("K5-13", "multi", "Consider the course app's Dockerfile (its <code>.dockerignore</code> lists <code>.env</code>). Which statements are correct?",
      ["<code>python:3.12-slim</code> is the base image.", "<code>CMD</code> sets the default command run when a container starts.",
       "Because of .dockerignore, <code>COPY . .</code> does not put .env into the image.", "<code>EXPOSE 8000</code> alone publishes port 8000 on the host; <code>-p</code> is unnecessary."], "abc",
      "EXPOSE chỉ ghi chú (metadata) cổng app dùng; muốn truy cập từ host vẫn cần <code>-p host:container</code>. .dockerignore loại file khỏi build context nên .env không được COPY vào image.",
      "llm_app/completed/Dockerfile, .dockerignore; Docker Deep Dive tr.116; week5.pdf tr.15", "k5-dockerfile", code=DF, lang="dockerfile"),
]
