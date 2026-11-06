# Bộ prompt video NotebookLM: CI, EC2, CD, Reverse proxy & HTTPS

## Cách dùng

| Video | Chủ đề | Nguồn cần chọn |
|---|---|---|
| 1 | CI với GitHub Actions | `CI.pdf` |
| 2 | Điện toán đám mây và EC2 | `cloudcomputing.pdf` (thêm `week3.pdf` nếu muốn có phần SSH) |
| 3 | CD và triển khai tự động | `CD.pdf` |
| 4 | Reverse proxy và HTTPS | `reverse_proxy_https.pdf` |

- Chọn **Video giải thích**, ngôn ngữ **Tiếng Việt**, phong cách **Cổ điển** (khối code trên nền sáng dễ đọc nhất).
- Mỗi prompt dán độc lập. Đầu mỗi prompt là cùng một khối **QUY TẮC HIỂN THỊ BẮT BUỘC**, áp dụng cho cả code lẫn quá trình: code, lệnh, YAML, cấu hình hiện nguyên văn trên màn hình; mọi quá trình (pipeline, luồng request, các bước thao tác) hiện thành sơ đồ hoặc danh sách bước đánh số. Đặt khối này ở đầu prompt để NotebookLM ưu tiên nó.
- Các đoạn code trong prompt chép từ slide. Ở chỗ slide chỉ có từng mảnh (ví dụ workflow push image), mình ghép các mảnh lại thành một file hoàn chỉnh để hiện trên màn hình.

---

## Video 1: CI với GitHub Actions

```
QUY TẮC HIỂN THỊ BẮT BUỘC (áp dụng cho TOÀN BỘ video, mọi phần, không có ngoại lệ):
1. Mọi đoạn code, lệnh, file YAML, file cấu hình và log lỗi được nhắc tới đều PHẢI hiện nguyên văn trên màn hình thành khối chữ font monospace, có tên file hoặc đường dẫn ở góc trên. Tuyệt đối không chỉ đọc code thành lời và không thay code bằng hình minh họa.
2. Mọi quá trình (luồng chạy, chuỗi các bước, đường đi trong giao diện web) đều PHẢI hiện thành sơ đồ có mũi tên hoặc danh sách bước đánh số trên màn hình. Khi đang nói tới bước nào thì tô sáng bước đó.
3. Lời thoại chỉ giải thích: chỉ vào từng dòng hoặc từng bước đang tô sáng và nói nó làm gì, vì sao cần nó. Không đọc lại nguyên văn nội dung đã có trên màn hình.

Chủ đề: video duy nhất về Buổi 7 "CI: Tự động kiểm thử và build" (slide CI) cho sinh viên năm 2 sắp thi, dài khoảng 10 phút. Giảng chi tiết, dễ hiểu, cô đọng vào những điểm quan trọng nhất phải nhớ. Chỉ nói về CI; phần CD chỉ nhắc trong một câu.

Trình tự:

1. Vấn đề khi kiểm thử và build bằng tay (khoảng 1:00): dễ quên chạy test trước khi push, mỗi người làm một kiểu, lỗi phát hiện muộn. Hiện bảng so sánh "làm tay" và "tự động": loại bỏ lỗi thao tác tay, ai push cũng chạy đúng các bước như nhau, phát hiện lỗi sớm.

2. CI và CD (khoảng 0:45): hiện hai ô cạnh nhau. CI tự động test và build mỗi khi code thay đổi; CD tự động triển khai sau khi test và build đạt.

3. Các khái niệm của GitHub Actions (khoảng 1:30): vẽ sơ đồ lồng nhau gồm workflow chứa các job, job chứa các step chạy lần lượt, tất cả chạy trên runner. Runner là máy thực thi do GitHub cấp và bị xóa sau khi chạy xong. Trigger: push (mỗi lần push là chạy) và pull_request (test trước khi gộp). Thêm ví dụ trigger có lọc nhánh:
on:
  push:
    branches: [main]
và giải thích chỉ push lên main mới kích hoạt workflow.

4. Vị trí file (khoảng 0:30): hiện cây thư mục
repo/
└── .github/
    └── workflows/
        └── ci.yml
Một file là một workflow. Hiện thêm các vị trí SAI hay bị nhầm (.git/workflows, .github/steps, app/actions) và gạch chéo từng vị trí.

5. File ci.yml đầy đủ (khoảng 2:30), hiện nguyên văn:
name: CI
on:
  push:
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest
      - run: docker build -t chat-app .
Tô sáng và giải thích lần lượt từng dòng: name, on, jobs, tên job test, runs-on, steps. Phân biệt uses (dùng một action có sẵn) và run (chạy lệnh shell). checkout lấy code về runner, vì runner ban đầu trống; setup-python và tham số with. Bên cạnh file, vẽ sơ đồ 5 bước checkout → cài Python → cài thư viện → pytest → build image, nối từng bước với dòng tương ứng trong file.

6. pytest và cơ chế đỏ/xanh (khoảng 2:00). Hiện file test:
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
Giải thích: tên file và tên hàm bắt đầu bằng test_ để pytest tìm thấy; TestClient gọi app mà không cần chạy server; vì sao chọn test /health (không gọi LLM nên nhanh và ổn định). Hiện thêm biến thể kiểm tra cả body và chỉ ra lỗi hay gặp:
assert response.json() == {"status": "ok"}   # đúng: gọi hàm json()
assert response.json                          # sai: không gọi hàm, luôn đúng
Vẽ sơ đồ đỏ/xanh: một test fail → step pytest lỗi → job hỏng → lần chạy workflow ĐỎ (có thể chặn gộp pull request); tất cả test đạt → XANH.

7. Build image trong workflow (khoảng 0:45): tô sáng lại dòng docker build trong ci.yml; một thay đổi làm hỏng Dockerfile sẽ bị phát hiện ngay.

8. Đọc log để sửa workflow đỏ (khoảng 0:45): hiện đường đi dạng sơ đồ: tab Actions → chọn lần chạy đỏ → mở job hỏng → mở step lỗi → đọc dòng lỗi đầu tiên. Hiện một đoạn log mẫu của step pytest bị fail (AssertionError: assert 500 == 200).

9. Tổng kết (khoảng 0:30): checklist 4 dòng của bài lab buổi 7, cùng 5 điểm phải nhớ: workflow → job → step; runner là máy do GitHub cấp; file đặt ở .github/workflows; uses khác run; test fail thì workflow đỏ.

Lời giảng bằng tiếng Việt; giữ nguyên code và thuật ngữ bằng tiếng Anh.
```

---

## Video 2: Điện toán đám mây và EC2

```
QUY TẮC HIỂN THỊ BẮT BUỘC (áp dụng cho TOÀN BỘ video, mọi phần, không có ngoại lệ):
1. Mọi đoạn code, lệnh, file YAML, file cấu hình và log lỗi được nhắc tới đều PHẢI hiện nguyên văn trên màn hình thành khối chữ font monospace, có tên file hoặc đường dẫn ở góc trên. Tuyệt đối không chỉ đọc code thành lời và không thay code bằng hình minh họa.
2. Mọi quá trình (luồng chạy, chuỗi các bước, đường đi trong giao diện web) đều PHẢI hiện thành sơ đồ có mũi tên hoặc danh sách bước đánh số trên màn hình. Khi đang nói tới bước nào thì tô sáng bước đó.
3. Lời thoại chỉ giải thích: chỉ vào từng dòng hoặc từng bước đang tô sáng và nói nó làm gì, vì sao cần nó. Không đọc lại nguyên văn nội dung đã có trên màn hình.

Chủ đề: video duy nhất về Buổi 8 "Điện toán đám mây và EC2" (slide cloudcomputing) cho sinh viên năm 2 sắp thi, dài khoảng 10 phút. Giảng chi tiết, dễ hiểu, cô đọng vào những điểm quan trọng nhất phải nhớ.

Trình tự:

1. Vấn đề xuyên suốt (khoảng 1:00): hiện bảng hai cột. Bên trái là app chạy trên laptop: chỉ chạy khi máy bật, chỉ truy cập được từ máy cá nhân, không có địa chỉ công khai ổn định. Bên phải là app chạy trên EC2: chạy liên tục, có Public IP, người khác truy cập được qua Internet.

2. Điện toán đám mây và IaaS (khoảng 1:30): thuê tài nguyên qua Internet thay vì mua máy chủ vật lý; tạo máy trong vài phút, tăng giảm tài nguyên khi cần, trả tiền theo mức dùng, xóa khi không cần. Vẽ sơ đồ chồng tầng IaaS / PaaS / SaaS và tô màu phần người dùng tự quản lý ở mỗi mô hình; chỉ ra EC2 thuộc IaaS, người dùng tự cài và quản lý phần mềm trên máy.

3. Tạo EC2 instance (khoảng 2:00): instance là một máy chủ ảo. Hiện 4 bước đánh số và tô sáng lần lượt: (1) chọn AMI, tức ảnh hệ điều hành, ví dụ Ubuntu; (2) chọn loại máy nằm trong Free Tier; (3) tạo key pair; (4) khởi tạo instance và chờ máy sẵn sàng. Vẽ sơ đồ key pair: AWS giữ public key trên instance, sinh viên giữ private key (file .pem). Hiện lệnh:
$ chmod 400 my-key.pem
$ ssh -i my-key.pem ubuntu@<dia-chi-cong-khai>
ubuntu@ip-172-31-xx-xx:~$
Tách từng phần của lệnh ssh: -i là file khóa riêng, ubuntu là user mặc định của AMI Ubuntu, sau dấu @ là địa chỉ công khai. Giải thích vì sao phải chmod 400.

4. Security Group (khoảng 2:30): đây là bộ quy tắc tường lửa cho instance, mặc định chặn phần lớn lưu lượng đi vào. Vẽ sơ đồ Internet → Security Group (inbound và outbound) → instance. Hiện bảng inbound rule:
| Port | Giao thức | Nguồn       | Mục đích                     |
| 22   | TCP       | My IP       | SSH, chỉ cho máy của mình    |
| 80   | TCP       | 0.0.0.0/0   | HTTP cho mọi người           |
| 443  | TCP       | 0.0.0.0/0   | HTTPS (dùng ở buổi 10)       |
Giải thích vì sao port 22 phải giới hạn còn 80 và 443 mở cho mọi nơi. Hiện bảng "Nên làm / Không nên" về nguyên tắc tối thiểu quyền: chỉ mở port cần dùng và không mở tất cả; SSH chỉ cho My IP, không để 0.0.0.0/0; xóa rule không còn dùng. Hiện tình huống chẩn đoán lỗi: gọi http://<ip>:8000 bị "Connection timed out" vì Security Group chưa mở port đó; cách sửa là thêm rule. So sánh với lỗi "Permission denied (publickey)", đây là lỗi khóa chứ không phải lỗi mạng.

5. Free Tier và chi phí (khoảng 0:45): chọn loại máy trong Free Tier; tắt hoặc xóa instance khi không dùng. Hiện một hộp cảnh báo nổi bật về việc bị tính phí ngoài ý muốn.

6. Đưa stack Docker lên EC2 (khoảng 1:30). Hiện chuỗi lệnh chạy trên instance:
$ ssh -i my-key.pem ubuntu@<ip>
$ sudo apt update && sudo apt install -y docker.io docker-compose-plugin
$ sudo usermod -aG docker ubuntu
$ cd ~/app
$ nano .env
$ docker compose up -d
$ docker ps
$ curl http://<ip>/health
Giải thích từng lệnh: usermod -aG docker để chạy docker không cần sudo; secret đặt trong .env trên server, không đưa lên Git; docker compose up -d chạy cả stack ở chế độ nền. Vẽ sơ đồ: trình duyệt → Public IP → Security Group (port 80) → container app. Ở buổi này app truy cập qua HTTP; HTTPS để buổi 10.

7. Tổng kết (khoảng 0:30): 5 điểm phải nhớ: EC2 thuộc IaaS; AMI là ảnh hệ điều hành; private key ở máy mình, public key trên instance; Security Group mặc định chặn inbound và port 22 chỉ mở cho My IP; tắt instance để tránh mất tiền.

Lời giảng bằng tiếng Việt; giữ nguyên lệnh và thuật ngữ bằng tiếng Anh.
```

---

## Video 3: CD và triển khai tự động

```
QUY TẮC HIỂN THỊ BẮT BUỘC (áp dụng cho TOÀN BỘ video, mọi phần, không có ngoại lệ):
1. Mọi đoạn code, lệnh, file YAML, file cấu hình và log lỗi được nhắc tới đều PHẢI hiện nguyên văn trên màn hình thành khối chữ font monospace, có tên file hoặc đường dẫn ở góc trên. Tuyệt đối không chỉ đọc code thành lời và không thay code bằng hình minh họa.
2. Mọi quá trình (luồng chạy, chuỗi các bước, đường đi trong giao diện web) đều PHẢI hiện thành sơ đồ có mũi tên hoặc danh sách bước đánh số trên màn hình. Khi đang nói tới bước nào thì tô sáng bước đó.
3. Lời thoại chỉ giải thích: chỉ vào từng dòng hoặc từng bước đang tô sáng và nói nó làm gì, vì sao cần nó. Không đọc lại nguyên văn nội dung đã có trên màn hình.

Chủ đề: video duy nhất về Buổi 9 "Continuous Delivery (CD) & triển khai tự động" (slide CD) cho sinh viên năm 2 sắp thi, dài khoảng 10 phút. Giảng chi tiết, dễ hiểu, cô đọng vào những điểm quan trọng nhất phải nhớ.

Trình tự:

1. Deploy thủ công và deploy tự động (khoảng 0:45): hiện bảng so sánh. Thủ công: SSH gõ lệnh dễ sai, mất 30–40 phút, phụ thuộc vào một người. Tự động: push là tự chạy, dưới 3 phút, dễ rollback.

2. Continuous Delivery và Continuous Deployment (khoảng 0:45): vẽ hai pipeline cạnh nhau. Delivery có một nút "Manual Approval" trước Production; Deployment đi thẳng tới Production không cần duyệt.

3. Toàn cảnh pipeline (khoảng 1:00): vẽ sơ đồ ngang 6 bước và tô sáng lần lượt: (1) Developer push code → (2) GitHub Actions test và build → (3) push image lên Registry (Docker Hub) → (4) SSH vào EC2 → (5) EC2 pull image và chạy → (6) healthcheck. Ghi chú bước 1–2 là CI, bước 3–6 là CD. Giải thích vì sao build trên runner rồi đẩy qua registry thay vì build trên EC2: EC2 không bị quá tải, image giống nhau ở mọi môi trường.

4. Rủi ro lộ secret và GitHub Secrets (khoảng 1:30). Hiện hai ví dụ SAI, mỗi ví dụ có dấu X đỏ:
env:
  API_KEY: "sk-live-123456"     # hardcode, lưu vĩnh viễn trong lịch sử commit
- run: echo $DB_PASSWORD        # in secret ra log
Vẽ cơ chế 3 bước của GitHub Secrets: nhập và được mã hóa → nạp vào RAM của runner khi chạy → tự che thành *** trong log. Hiện bảng 3 loại secret: Organization, Repository (loại dùng trong bài), Environment. Hiện đường đi Settings › Secrets and variables › Actions › New repository secret, cùng danh sách 5 secret cần tạo: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, EC2_HOST, EC2_USERNAME, EC2_SSH_KEY. Vẽ timeline bảo mật xuyên suốt khóa học: .gitignore → .env → Security Group → GitHub Secrets.

5. Workflow build và push image (khoảng 2:00). Hiện file hoàn chỉnh:
# .github/workflows/push-image.yml
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
        with:
          push: true
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/chatbot-api:latest
            ${{ secrets.DOCKERHUB_USERNAME }}/chatbot-api:${{ github.sha }}
Giải thích từng step; cú pháp ${{ secrets.TEN }}; dùng Docker Access Token thay mật khẩu thật vì token thu hồi được ngay. Hiện bảng chiến lược tag: chỉ dùng :latest thì tiện nhưng khó rollback; :<git-sha> là duy nhất và truy vết được; nên gắn cả hai tag. Hiện cách kiểm tra: step push báo xanh trên tab Actions, và tag mới xuất hiện trên Docker Hub.

6. SSH từ runner vào EC2 và deploy (khoảng 2:00). Vẽ sơ đồ "chìa và ổ khóa": runner giữ private key (toàn bộ nội dung file .pem dán vào secret EC2_SSH_KEY); EC2 giữ public key trong ~/.ssh/authorized_keys; kết nối qua port 22. Hiện checklist chuẩn bị trên EC2: đã có Docker và Compose plugin; đã chạy usermod -aG docker ubuntu; có docker-compose.yml trong thư mục dự án. Hiện file:
# .github/workflows/deploy.yml (step deploy)
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
Nhấn mạnh: các lệnh trong script chạy TRÊN EC2 qua SSH, không chạy trên runner. Giải thích từng lệnh trong script; docker image prune -f dọn các image cũ, kèm hình thanh dung lượng đĩa đi từ 99% xuống 30%. Hiện hai cách quản lý .env trên server: tạo sẵn file thủ công một lần, hoặc ghi file .env từ Secrets ngay trong script.

7. Healthcheck và đọc log (khoảng 1:00). Hiện:
- name: Healthcheck
  run: curl -f http://${{ secrets.EC2_HOST }}:8080/health || exit 1
Giải thích -f khiến HTTP ≥ 400 (ví dụ 503) bị coi là lỗi, || exit 1 làm step fail và workflow ĐỎ; step này không tự retry và không tự rollback. Hiện log mẫu có secret bị che thành ***.

8. Ba nhóm lỗi hay gặp (khoảng 1:00). Hiện từng log lỗi kèm nguyên nhân và cách sửa:
Error: ... port 22: Permission denied (publickey)
(private key dán thiếu dòng -----BEGIN ... KEY-----; IP của EC2 đổi sau khi restart mà không dùng Elastic IP; Security Group chặn port 22 với runner)
Error: Cannot perform an interactive login ... / unauthorized
(sai username hoặc dùng mật khẩu thay vì Access Token)
Container exited (1) / (137)
(thiếu biến trong .env hoặc lỗi app) → chạy: $ docker logs <container_id>

9. Tổng kết (khoảng 0:30): 4 best practice: không hardcode secret; build image một lần và dùng lại để test và deploy (immutable artifact); dọn image sau mỗi lần deploy; fail fast và có healthcheck.

Lời giảng bằng tiếng Việt; giữ nguyên code và thuật ngữ bằng tiếng Anh.
```

---

## Video 4: Reverse proxy và HTTPS

```
QUY TẮC HIỂN THỊ BẮT BUỘC (áp dụng cho TOÀN BỘ video, mọi phần, không có ngoại lệ):
1. Mọi đoạn code, lệnh, file YAML, file cấu hình và log lỗi được nhắc tới đều PHẢI hiện nguyên văn trên màn hình thành khối chữ font monospace, có tên file hoặc đường dẫn ở góc trên. Tuyệt đối không chỉ đọc code thành lời và không thay code bằng hình minh họa.
2. Mọi quá trình (luồng chạy, chuỗi các bước, đường đi trong giao diện web) đều PHẢI hiện thành sơ đồ có mũi tên hoặc danh sách bước đánh số trên màn hình. Khi đang nói tới bước nào thì tô sáng bước đó.
3. Lời thoại chỉ giải thích: chỉ vào từng dòng hoặc từng bước đang tô sáng và nói nó làm gì, vì sao cần nó. Không đọc lại nguyên văn nội dung đã có trên màn hình.

Chủ đề: video duy nhất về Buổi 10 "Reverse proxy và HTTPS" (slide reverse_proxy_https) cho sinh viên năm 2 sắp thi, dài khoảng 10 phút. Giảng chi tiết, dễ hiểu, cô đọng vào những điểm quan trọng nhất phải nhớ.

Trình tự:

1. Vị trí trong dự án (khoảng 0:30): sau buổi 9, app đã chạy trên EC2 nhưng mới truy cập qua HTTP. Đích đến là một địa chỉ HTTPS công khai có ổ khóa trên trình duyệt.

2. Reverse proxy là gì và vì sao cần (khoảng 1:30): vẽ sơ đồ Internet → reverse proxy → app (localhost:8000). Hai vai trò chính, mỗi vai trò một hình: định tuyến request tới đúng app; TLS termination, tức proxy lo phần mã hóa HTTPS để app bên trong chỉ cần chạy HTTP thường. Thêm ý: chỉ có proxy lộ ra Internet, port của app được ẩn đi.

3. HTTP, HTTPS và chứng chỉ (khoảng 2:00): hiện phương trình HTTP + mã hóa = HTTPS. So sánh hai gói tin: HTTP để lộ nội dung (ví dụ mật khẩu đọc được), HTTPS chỉ thấy chuỗi đã mã hóa. Chứng chỉ chứng minh danh tính của trang và cho phép mã hóa; hiện các trường của một chứng chỉ (tên miền, tổ chức cấp CA, ngày hết hạn, public key). Vẽ sơ đồ bắt tay TLS rút gọn: trình duyệt chào → server gửi chứng chỉ → trình duyệt kiểm tra với CA → hai bên thống nhất khóa phiên → dữ liệu được mã hóa. Let's Encrypt là CA cấp chứng chỉ miễn phí. Ý nghĩa ổ khóa: chứng chỉ hợp lệ và kết nối đang được mã hóa.

4. Caddy và Caddyfile (khoảng 2:00): Caddy là reverse proxy tự xin và tự gia hạn chứng chỉ qua Let's Encrypt. Hiện file:
# /etc/caddy/Caddyfile
myapp.example.com {
    reverse_proxy localhost:8000
}
Tô sáng dòng đầu (tên miền) và dòng bên trong (địa chỉ app mà Caddy chuyển request tới). Hiện các lệnh trên instance:
$ sudo nano /etc/caddy/Caddyfile
$ sudo systemctl reload caddy
$ sudo journalctl -u caddy -f
Vẽ quá trình Caddy tự cấp HTTPS: khởi động → đọc tên miền trong Caddyfile → xin chứng chỉ từ Let's Encrypt → tự gia hạn trước khi hết hạn.

5. Tên miền (khoảng 1:30): Let's Encrypt chỉ cấp chứng chỉ cho tên miền, không cấp cho IP thuần. Vẽ quá trình DNS: gõ tên miền → DNS tra bản ghi A → trả về IP của instance → trình duyệt kết nối tới IP đó. Hiện bảng so sánh hai cách:
| nip.io                        | Tên miền riêng                          |
| 203.0.113.25.nip.io           | Thêm bản ghi A: myapp → 203.0.113.25    |
| Không cần cấu hình gì thêm    | Vào trang quản lý tên miền để thêm      |
Kèm Caddyfile tương ứng khi dùng nip.io:
203.0.113.25.nip.io {
    reverse_proxy localhost:8000
}

6. Mở port và cách Let's Encrypt xác minh (khoảng 1:00): vẽ quá trình xác minh: Let's Encrypt gửi request tới tên miền qua port 80 → Caddy trả lời đúng → chứng chỉ được cấp. Hiện bảng inbound rule:
| Port | Giao thức | Nguồn     | Mục đích                          |
| 80   | TCP       | 0.0.0.0/0 | Để Let's Encrypt xác minh và cấp chứng chỉ |
| 443  | TCP       | 0.0.0.0/0 | Người dùng truy cập HTTPS         |
| 8000 | —         | —         | KHÔNG mở, chỉ Caddy gọi nội bộ    |
Vẽ sơ đồ toàn hệ thống: người dùng → HTTPS 443 → Security Group → Caddy → localhost:8000 → container app → LLM API và PostgreSQL.

7. Chẩn đoán và kiểm tra (khoảng 1:00). Hiện bảng 3 lỗi khi chứng chỉ không cấp được, mỗi lỗi có nguyên nhân và cách sửa: port 80 đóng (mở port 80); tên miền chưa trỏ đúng (kiểm tra bản ghi A hoặc chuỗi nip.io); chạm rate limit vì xin quá nhiều lần (chờ hết thời hạn giới hạn). Lệnh đọc log chung: sudo journalctl -u caddy -f. Hiện lệnh kiểm tra:
$ curl -v https://203.0.113.25.nip.io/health
kèm vài dòng output mẫu có thông tin chứng chỉ (subject, issuer Let's Encrypt, expire date) và HTTP/2 200.

8. Tổng kết (khoảng 0:30): checklist 3 dòng của bài lab, cùng 5 điểm phải nhớ: reverse proxy đứng trước app và lo TLS termination; Let's Encrypt cấp chứng chỉ miễn phí nhưng chỉ cho tên miền; Caddyfile gồm tên miền và reverse_proxy localhost:8000; mở 80 và 443, không mở 8000; lỗi cấp chứng chỉ thì xem journalctl -u caddy.

Lời giảng bằng tiếng Việt; giữ nguyên code và thuật ngữ bằng tiếng Anh.
```

---

## Nếu video vẫn chỉ đọc code mà không hiện lên màn hình

- Thêm câu này vào dòng đầu tiên của prompt: *"Đây là bài giảng lập trình dạng hướng dẫn trên màn hình: hơn một nửa số cảnh phải là khối code hoặc sơ đồ quá trình chiếm phần lớn khung hình."*
- Nếu một video bị lướt nhanh, video 3 (CD) là video dài nhất. Có thể tách làm hai: mục 1–5 (pipeline, Secrets, push image) và mục 6–9 (SSH deploy, healthcheck, lỗi).
- Một số chi tiết không có nguyên văn trong slide mà mình thêm vào cho trọn vẹn: phần `push: true` và `tags` trong push-image.yml, các lệnh cài Docker trên EC2, nội dung log lỗi mẫu, và output mẫu của `curl -v`. Nếu muốn video bám đúng slide 100%, xóa các phần này.
