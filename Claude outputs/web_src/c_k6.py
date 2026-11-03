from h import *

SVG = """<svg viewBox="0 0 660 250" width="660" role="img" aria-label="workflow chứa job, job chứa step, chạy trên runner">
<rect x="6" y="8" width="648" height="234" rx="10" class="box"/>
<text x="20" y="30" font-weight="700">workflow</text><text x="96" y="30" class="mono muted" font-size="13">.github/workflows/ci.yml · on: push, pull_request</text>
<rect x="22" y="44" width="400" height="186" rx="8" class="boxa"/>
<text x="36" y="66" font-weight="700">job: test</text><text x="110" y="66" class="mono muted" font-size="13">runs-on: ubuntu-latest</text><text x="300" y="66" font-size="11" class="muted">step chạy lần lượt ↓</text>
<g font-size="13" class="mono">
<rect x="40" y="78" width="364" height="24" rx="5" class="box"/><text x="50" y="95">1 uses: actions/checkout@v4</text>
<rect x="40" y="106" width="364" height="24" rx="5" class="box"/><text x="50" y="123">2 uses: actions/setup-python@v5</text>
<rect x="40" y="134" width="364" height="24" rx="5" class="box"/><text x="50" y="151">3 run: pip install -r requirements.txt</text>
<rect x="40" y="162" width="364" height="24" rx="5" class="box"/><text x="50" y="179">4 run: pytest</text>
<rect x="40" y="190" width="364" height="24" rx="5" class="box"/><text x="50" y="207">5 run: docker build -t chat-app .</text>
</g>
<path d="M412 90 v118" class="lna"/><path d="M406 200 l6 10 l6 -10" class="lna"/>

<rect x="450" y="70" width="190" height="150" rx="8" class="box"/>
<text x="462" y="92" font-weight="700">runner</text>
<text x="462" y="114" font-size="13">máy thực thi job</text>
<text x="462" y="134" font-size="13">GitHub tự cấp</text>
<text x="462" y="154" font-size="13">chạy xong thì bị xóa</text>
<text x="462" y="180" font-size="13">step fail → job fail</text>
<text x="462" y="200" font-size="13">→ lần chạy ĐỎ</text>
<path d="M422 140 h28" class="ln dash"/>
</svg>"""

P = {}
P["y"] = """<p><b>CI (Continuous Integration)</b>: mỗi khi mã nguồn thay đổi (push / pull request), GitHub Actions tự động <b>kiểm thử và build</b> trên một <b>runner</b> do GitHub cấp. Mục tiêu: không quên chạy test, ai push cũng chạy đúng các bước như nhau, phát hiện lỗi sớm. CD (tự triển khai sau khi test/build đạt) học ở khối K8.</p>""" + src("CI.pdf tr.4–7")

P["mohinh"] = diagram(SVG, "workflow → job → step; tất cả chạy trên runner do GitHub cấp (CI.pdf tr.10, 15)") + """
<h3 id="k6-pipeline">Workflow chạy như thế nào</h3>""" + flow(["push", "checkout", "setup python", "pip install", "pytest", "docker build", "finish"], active=(4,)) + src("CI.pdf tr.14")

P["bang"] = """<h3 id="k6-file">File workflow</h3>
<p>GitHub Actions chỉ đọc các file trong thư mục <code>.github/workflows/</code>. Một file = một quy trình tự động.</p>""" + pre("""
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
""", "yaml") + table(["Khóa", "Ý nghĩa"], [
    [c("on:"), "trigger — sự kiện làm workflow chạy (<code>push</code>, <code>pull_request</code>)"],
    [c("branches: [main]"), "lọc: chỉ chạy khi sự kiện xảy ra trên nhánh main"],
    [c("jobs: → test:"), "workflow chứa job; <code>test</code> là tên job"],
    [c("runs-on:"), "loại runner chạy job (ubuntu-latest)"],
    [c("steps:"), "danh sách step, chạy <b>lần lượt</b> trong job"],
    [c("uses:"), "dùng một action có sẵn (checkout code, cài Python, login Docker…)"],
    [c("run:"), "chạy lệnh shell trên runner"],
    [c("with:"), "tham số truyền cho action (ví dụ <code>python-version</code>)"],
]) + src("CI.pdf tr.10–15") + """
<h3 id="k6-trigger">Trigger</h3>""" + table(["Khai báo", "Chạy khi", "Không chạy khi"], [
    ["<code>on: push</code>", "đẩy commit lên GitHub (mọi nhánh)", "commit/sửa file ở local mà chưa push"],
    ["<code>on: pull_request</code>", "mở pull request → kiểm thử trước khi gộp", "chỉ push mà không có PR"],
    ["<code>on: push: branches: [main]</code>", "push lên nhánh main", "push lên nhánh khác (experiment…), mở PR không kèm push lên main"],
]) + src("CI.pdf tr.11; CD.pdf tr.13; đề mẫu Q7, Q15") + """
<h3 id="k6-pytest">pytest và cơ chế đỏ/xanh</h3>""" + pre("""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
""", "python") + ul([
    "Một bài test không đạt → step <code>pytest</code> báo lỗi → job hỏng → lần chạy workflow <b>ĐỎ</b>; có thể đặt để <b>chặn gộp</b> pull request đang đỏ.",
    "Tất cả test đạt → lần chạy <b>XANH</b>.",
    "Nên bắt đầu bằng test đơn giản như <code>/health</code> (không gọi LLM) để workflow nhanh, ổn định.",
    "Quy ước pytest: file <code>test_*.py</code>, hàm <code>test_...</code> (slide chỉ minh họa <code>test_health</code>).",
    "Kiểm tra cả status code và <b>toàn bộ</b> body: <code>assert response.json() == {...}</code> — phải có <code>()</code>."]) + src("CI.pdf tr.17–19; đề mẫu Q17") + """
<h3 id="k6-log">Đọc log khi workflow đỏ</h3>""" + flow(["Tab Actions", "chọn lần chạy đỏ", "mở job hỏng", "mở step lỗi", "đọc thông báo"]) + src("CI.pdf tr.23")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["CI vs CD", "CI: tự động <b>kiểm thử và build</b> mỗi khi mã thay đổi. CD: tự động <b>triển khai</b> sau khi test/build đạt (K8)."],
    ["workflow / job / step", "workflow (file .yml) chứa job; job chứa step chạy lần lượt."],
    ["runner vs registry", "Runner = máy/môi trường thực thi job. Registry (Docker Hub/ECR) = nơi lưu và phát hành image. Không lẫn."],
    ["workflow file vs runner", "File YAML khai báo sự kiện và các bước; runner là máy chạy các bước đó."],
    [c("uses") + " vs " + c("run"), "uses: gọi action có sẵn; run: chạy lệnh shell."],
    [c("push") + " vs " + c("pull_request"), "push: mỗi lần đẩy mã lên. pull_request: khi mở PR, kiểm thử trước khi gộp."],
    ["Kiểm thử tay vs CI", "Tay: dễ quên, mỗi người một kiểu, phát hiện muộn. CI: chuỗi kiểm tra nhất quán cho mọi sự kiện khớp, phản hồi sớm. CI <b>không</b> tự sửa lỗi."],
    [c("response.json()") + " vs " + c("response.json"), "Có ngoặc → dữ liệu body. Không ngoặc → method object (assert luôn đúng, không kiểm tra gì)."],
    [c(".github/workflows/") + " vs chỗ khác", "Chỉ <code>.github/workflows/</code> được nhận. <code>.git/workflows</code>, <code>.github/steps</code>, <code>app/actions</code> đều sai."],
]) + src("CI.pdf tr.4–15, 19")

P["bay"] = trap("Bẫy 1 — trigger có lọc nhánh (Q7)", "<code>on: push: branches: [main]</code>: chỉ push lên <b>main</b> mới chạy. Push lên <code>experiment</code>, commit local chưa push, hay mở PR mà không push lên main đều <b>không</b> chạy.<br><b>Đổi một chỗ:</b> thêm <code>pull_request:</code> → mở PR cũng chạy; bỏ <code>branches</code> → push nhánh nào cũng chạy.", "k6-trap-trigger") + \
    trap("Bẫy 2 — workflow có cả push và pull_request (Q15)", "Trigger là <b>push lên repo</b> và <b>mở pull request</b>. Mọi việc chỉ xảy ra ở máy local (sửa file, commit chưa push) không bao giờ kích hoạt workflow vì GitHub không biết.", "k6-trap-q15") + \
    trap("Bẫy 3 — runner là gì (Q14)", "Runner = <b>máy/môi trường thực thi job</b>, cung cấp môi trường cho các step. Không phải registry, không phải file YAML.", "k6-trap-runner") + \
    trap("Bẫy 4 — CI mang lại gì (Q12)", "Phản hồi sớm khi thay đổi làm hỏng test; chuỗi kiểm tra nhất quán cho các sự kiện khớp. CI <b>không tự sửa</b> lỗi build.<br><i>Lưu ý:</i> đáp án tham khảo của đề mẫu Q12 là <b>c “All the statements are correct”</b> dù phương án a (“Automatic correction of every failed build instruction”) trái với slide. Web chấm theo đáp án tham khảo; nếu gặp lại câu này trong đề thật, cân nhắc hỏi lại giảng viên.", "k6-trap-q12") + \
    trap("Bẫy 5 — đỏ ở step nào thì dừng ở đó", "Step <code>pytest</code> fail → job fail, các step sau (docker build) <b>không chạy</b>, lần chạy chuyển đỏ.<br><b>Đổi một chỗ:</b> đưa <code>docker build</code> lên trước <code>pytest</code> → Dockerfile hỏng sẽ làm đỏ trước khi test kịp chạy.", "k6-trap-red") + \
    trap("Bẫy 6 — test kiểm tra “toàn bộ JSON” (Q17)", "Chỉ <code>assert response.json() == {\"status\": \"ok\"}</code> kiểm tra cả body. <code>assert {\"status\": \"ok\"}</code> luôn đúng (dict khác rỗng); <code>assert response.json</code> chỉ kiểm tra method tồn tại; <code>is not None</code> không so nội dung.", "k6-trap-json")

P["checklist"] = [
    "Vì sao cần CI (kiểm thử thủ công dễ quên, không đồng nhất, phát hiện lỗi muộn); CI khác CD thế nào",
    "Phân cấp: workflow → job → step; runner là máy chạy job (GitHub cấp, chạy xong thì xóa)",
    "File đặt ở .github/workflows/*.yml; on: push / pull_request / branches: [main]; runs-on; uses và run; actions/checkout, actions/setup-python",
    "Pipeline: cài đặt → pytest → docker build; một step fail thì job fail (dấu đỏ); đọc log để sửa",
    "pytest: cách đặt tên file và hàm test_, assert, phân biệt json() và json",
    "＋ Có thể chặn gộp PR đang đỏ; thứ tự đọc log: Actions → lần chạy → job → step",
]

P["quick"] = [
    QQ("Workflow khai báo <code>on: pull_request:</code> (không có push). Việc nào làm nó chạy?",
       ["Push commit lên main", "Mở một pull request", "Commit ở máy local", "Sửa file trên laptop"], "b", "Chỉ sự kiện pull_request kích hoạt workflow này."),
    QQ("Trong job, step <code>run: pytest</code> có 1 test fail. Điều gì xảy ra?",
       ["Job vẫn xanh vì các test khác đạt", "Step lỗi → job hỏng → lần chạy chuyển đỏ", "GitHub tự sửa test", "Runner giữ lại máy để debug mãi mãi"], "b",
       "Một test fail → step pytest báo lỗi → job hỏng → workflow đỏ (CI.pdf tr.18)."),
    QQ("Runner là gì?", ["Nơi lưu image đã build", "File YAML khai báo sự kiện", "Máy thực thi job do GitHub cấp, chạy xong bị xóa", "Một nhánh Git"], "c",
       "Runner là máy thực thi workflow (CI.pdf tr.6)."),
]

BLOCK = dict(id="K6", mon="TTNT", title="CI với GitHub Actions", src="CI.pdf", page=P)

CI15 = """name: CI

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
      - run: docker build -t chat-app ."""

QUESTIONS = [
    Q("K6-D07", "single", "Consider:", ["Pushing a commit to a branch named experiment.", "Pushing a commit to the repository's main branch.", "Creating a commit locally without pushing it.", "Opening any pull request without a matching push to main."], "b",
      "<code>on: push</code> + <code>branches: [main]</code>: chỉ push lên nhánh main mới kích hoạt. Commit local không lên GitHub thì GitHub không biết; PR không phải sự kiện được khai báo.",
      "CI.pdf tr.11; CD.pdf tr.13; đề mẫu Q7", "k6-trap-trigger", code="on:\n  push:\n    branches: [main]", lang="yaml", demo=7, hoi="Which event matches this trigger?"),
    Q("K6-D12", "single", "Compared with relying on developers to run checks manually, what can a configured CI workflow provide?",
      ["Automatic correction of every failed build instruction.", "Earlier feedback when a change breaks an existing test.", "All the statements are correct.", "A consistent sequence of checks for matching events."], "c",
      "Đáp án tham khảo của đề: <b>c</b>. Theo slide, CI loại bỏ lỗi thao tác tay, quy trình lặp lại được (d) và phát hiện lỗi sớm (b).\n⚠ Lưu ý: phương án a (tự sửa mọi lỗi build) không có trong slide — CI chỉ phát hiện, không tự sửa. Web chấm theo đáp án tham khảo của đề; xem ghi chú ở trang ôn K6.",
      "CI.pdf tr.4, 7; đề mẫu Q12 (đáp án tham khảo)", "k6-trap-q12", demo=12),
    Q("K6-D13", "single", "Which hierarchy correctly describes GitHub Actions?",
      ["A runner contains triggers, and a trigger contains jobs.", "A workflow contains jobs, and a job contains steps.", "A job contains repositories, and a repository contains steps.", "A step contains workflows, and a workflow contains runners."], "b",
      "workflow chứa job · job chứa step (chạy lần lượt) · tất cả chạy trên runner do GitHub cấp.", "CI.pdf tr.10; đề mẫu Q13", "k6-file", demo=13),
    Q("K6-D14", "multi", "Which statements correctly describe a runner?",
      ["It is the registry where the built image is published.", "It is the YAML file that declares workflow events.", "It provides the environment in which job steps execute.", "It is the machine or execution environment that runs a job."], "cd",
      "Runner là máy thực thi workflow/job và cung cấp môi trường cho các step. Registry (a) là Docker Hub/ECR; file YAML (b) là workflow.", "CI.pdf tr.6, 10; đề mẫu Q14", "k6-trap-runner", demo=14),
    Q("K6-D15", "multi", "Consider the workflow:", ["Opening a pull request that matches this configuration.", "Editing a file locally without updating GitHub.", "Creation of a local Git commit without a push.", "A push to the repository."], "ad",
      "<code>on: push</code> và <code>on: pull_request</code> → hai trigger là push lên repo và mở PR. Việc chỉ diễn ra ở local không kích hoạt gì.", "CI.pdf tr.11, 15; đề mẫu Q15", "k6-trap-q15",
      code=CI15, lang="yaml", demo=15, hoi="Which event(s) is/are configured as workflow triggers?"),
    Q("K6-D16", "single", "Where should the repository store the lecture's workflow file so GitHub Actions recognizes it?",
      ["<code>app/actions/ci.yml</code>", "<code>.github/steps/ci.yml</code>", "<code>.github/workflows/ci.yml</code>", "<code>.git/workflows/ci.yml</code>"], "c",
      "GitHub Actions đọc các file workflow trong thư mục <code>.github/workflows</code>. <code>.git/</code> là thư mục nội bộ của Git, không phải nơi đặt workflow.", "CI.pdf tr.13; đề mẫu Q16", "k6-file", demo=16),
    Q("K6-D17", "single", "A student wants to check both the status code and the complete JSON response body.\nWhich test does that?",
      ["<pre>assert response.status_code == 200\nassert {\"status\": \"ok\"}</pre>", "<pre>assert response.status_code == 200\nassert response.json</pre>",
       "<pre>assert response.status_code == 200\nassert response.json() is not None</pre>", "<pre>assert response.status_code == 200\nassert response.json() == {\"status\": \"ok\"}</pre>"], "d",
      "Chỉ (d) so sánh toàn bộ body. (a) assert một dict khác rỗng → luôn đúng. (b) <code>response.json</code> không gọi hàm → luôn truthy. (c) chỉ kiểm tra khác None.", "CI.pdf tr.19; đề mẫu Q17", "k6-trap-json", demo=17),
    Q("K6-08", "single", "Which event triggers this workflow?", ["Pushing a commit to main.", "Opening a pull request.", "Creating a tag locally.", "Pushing to any branch."], "b",
      "Chỉ khai báo <code>pull_request</code> nên push (kể cả lên main) không kích hoạt workflow này.", "CI.pdf tr.11", "k6-trigger",
      code="name: PR checks\non:\n  pull_request:\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: pytest", lang="yaml"),
    Q("K6-09", "single", "In the workflow from the lecture, one assertion inside <code>pytest</code> fails. What is the result of that run?",
      ["The pytest step reports an error, the job fails and the run turns red; the later docker build step does not run.",
       "The job stays green because the remaining tests passed.", "GitHub automatically reverts the commit that broke the test.", "Only the docker build step is marked red."], "a",
      "Cơ chế đỏ/xanh: một test không đạt → step pytest báo lỗi → job hỏng → lần chạy chuyển đỏ. Step lỗi dừng job nên bước build sau đó không chạy. Có thể cấu hình chặn gộp PR đang đỏ.", "CI.pdf tr.18", "k6-trap-red", code=CI15, lang="yaml"),
    Q("K6-10", "multi", "Which statements about the steps of this job are correct?",
      ["<code>uses: actions/checkout@v4</code> runs a ready-made action that brings the repository code onto the runner.", "<code>run:</code> executes a shell command on the runner.",
       "<code>docker build</code> runs before <code>pytest</code> because it is the last line.", "All steps of the job run in parallel on different runners."], "ab",
      "Step trong một job chạy <b>lần lượt</b> theo thứ tự khai báo: checkout → setup python → pip install → pytest → docker build. <code>uses</code> gọi action có sẵn, <code>run</code> chạy lệnh shell.", "CI.pdf tr.10, 14–15", "k6-file", code=CI15, lang="yaml"),
    Q("K6-11", "single", "A workflow run is red. Following the lecture, what is the right way to find the cause?",
      ["Actions tab → open the red run → open the failed job → open the failed step → read the message.", "Delete the workflow file and push again.",
       "Re-run until it turns green.", "Read the Docker Hub repository page."], "a", "Thứ tự đọc log: tab Actions → lần chạy đỏ → job hỏng → step lỗi → đọc thông báo tìm nguyên nhân.", "CI.pdf tr.23", "k6-log"),
    Q("K6-12", "single", "Which description matches <b>CI</b> rather than CD?",
      ["Automatically test and build whenever the source code changes.", "Automatically deploy to the server after test and build pass.", "Manually copy files to EC2 with scp.", "Store images in a registry for EC2 to pull."], "a",
      "CI: tự động kiểm thử và build mỗi khi mã nguồn thay đổi. CD: tự động triển khai sau khi kiểm thử và build đạt.", "CI.pdf tr.5", "k6-file"),
    Q("K6-13", "single", "Why does the lecture add <code>docker build -t chat-app .</code> as a step after the tests?",
      ["To check that the image still builds after each change, so a broken Dockerfile is detected immediately in the workflow.", "To deploy the container to EC2.",
       "To publish the image to Docker Hub.", "To make pytest run faster."], "a",
      "Bước build image trong CI chỉ kiểm tra image vẫn build được; việc push lên registry và deploy thuộc CD (K8).", "CI.pdf tr.21", "k6-pipeline"),
]
