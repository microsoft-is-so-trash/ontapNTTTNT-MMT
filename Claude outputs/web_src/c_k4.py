from h import *

P = {}
P["y"] = """
<p>Biến app chatbot từ một script thành <b>dịch vụ web bền</b>: <b>FastAPI</b> ánh xạ “path + method” sang hàm Python, <b>Uvicorn</b> (ASGI server) nghe cổng mạng và chuyển request vào app, <b>Pydantic</b> kiểm tra dữ liệu vào/ra, <b>.env</b> giữ bí mật ngoài mã nguồn, <b>PostgreSQL</b> lưu dữ liệu qua connection pool.</p>
<p>Ba câu hỏi của buổi: app tổ chức thế nào (routers/schemas/db) · bí mật nằm đâu (.env) · dữ liệu lưu đâu (PostgreSQL).</p>
""" + src("week4.pdf tr.4–6, 35; fastapi_llm.pdf tr.4–11")

P["mohinh"] = """
<h3 id="k4-journey">Hành trình một request <code>POST /chat</code></h3>
""" + flow(["Client gửi JSON", "Uvicorn (ASGI) nhận", "Router khớp path + method", "Pydantic kiểm tra ChatRequest", "Depends(get_conn) lấy kết nối từ pool", "INSERT vào PostgreSQL", "Lọc qua response_model", "Trả JSON"], active=(3, 6)) + """
<p class="small">Sai dữ liệu → dừng ở bước kiểm tra, trả <b>422</b>, hàm endpoint <b>không chạy</b>, DB không bị chạm tới.</p>
<h3 id="k4-structure">Cấu trúc project</h3>
""" + pre("""
app/
|-- main.py          # tạo FastAPI(), include_router(...)
|-- routers/chat.py  # endpoint /chat
|-- schemas/chat.py  # Pydantic request/response models
|-- db/database.py   # connection pool, get_conn dependency
+-- .env             # bí mật, KHÔNG commit
""", "text") + """
<h3 id="k4-proxy">FastAPI đóng hai vai khi gọi LLM</h3>
""" + flow(["Client", "FastAPI (server với client)", "FastAPI (client với Gemini)", "Gemini API"], active=(1, 2)) + """
<p class="small">FastAPI vừa là Server (đối với Client) vừa là Client (đối với Gemini), giống một proxy.</p>
""" + src("week4.pdf tr.6, 10, 35; fastapi_llm.pdf tr.15")

P["bang"] = """
<h3 id="k4-uvicorn">Chạy app bằng Uvicorn</h3>
""" + pre("uvicorn app.main:app --reload --port 8000", "bash") + table(
    ["Phần", "Ý nghĩa"],
    [[c("app.main"), "đường dẫn module Python = file <code>app/main.py</code> (dấu chấm thay dấu /, bỏ .py)"],
     [c(":app"), "tên <b>biến</b> giữ đối tượng <code>FastAPI()</code> trong file đó"],
     [c("--reload"), "tự khởi động lại khi sửa code — <b>chỉ dùng khi dev</b>"],
     [c("--port 8000"), "cổng mạng để nghe"]]) + note("Quy tắc: <code>uvicorn &lt;thư_mục&gt;.&lt;file&gt;:&lt;biến&gt;</code>. File <code>app/main.py</code> có <code>api = FastAPI()</code> → <code>uvicorn app.main:api</code>.") + src("week4.pdf tr.9") + """
<h3 id="k4-router">APIRouter</h3>
""" + pre('''
# app/routers/chat.py
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")          # -> POST /chat/
async def send_message(...): ...

@router.get("/history")    # -> GET /chat/history
async def get_history(...): ...

# app/main.py
app.include_router(chat.router)
''', "python") + "<p>URL = <code>prefix</code> + path của decorator. <code>tags</code> chỉ dùng để nhóm endpoint trên trang <code>/docs</code>, <b>không</b> nằm trong URL.</p>" + src("week4.pdf tr.11; materials/llm_app/completed/main.py, routers/chat.py") + """
<h3 id="k4-pydantic">Pydantic: model vào và model ra</h3>
""" + pre('''
class ChatRequest(BaseModel):      # dữ liệu VÀO
    role: str
    content: str

class ChatResponse(BaseModel):     # dữ liệu RA
    id: int
    role: str
    content: str
    created_at: datetime

@router.post("/", response_model=ChatResponse)
async def send_message(msg: ChatRequest, conn=Depends(get_conn)): ...
''', "python") + ul([
    "Thiếu field bắt buộc (ví dụ thiếu <code>content</code>) → FastAPI tự trả <b>422 Unprocessable Entity</b>, hàm không chạy.",
    "<code>response_model</code> định hình dữ liệu ra và <b>ẩn field nội bộ</b> (password, token) — field thừa bị bỏ đi, không phải thành <code>null</code>.",
    "Code mẫu llm_app dùng thêm <code>Field(..., min_length=1, max_length=20_000)</code> để chặn chuỗi rỗng; <code>title: str | None = None</code> là field tùy chọn có mặc định."]) + src("week4.pdf tr.12–14; fastapi_llm.pdf tr.10–11; llm_app/completed/schemas/chat.py") + """
<h3 id="k4-status">HTTP status code</h3>
""" + table(["Mã", "Ý nghĩa", "Gặp khi"], [
    ["2xx · <b>200</b> OK", "thành công", "request bình thường"],
    ["<b>401</b> Unauthorized", "lỗi phía client", "sai API key (Gemini)"],
    ["<b>404</b> Not Found", "lỗi phía client", "sai đường dẫn / không có tài nguyên (llm_app: conversation không tồn tại)"],
    ["<b>422</b> Unprocessable Entity", "lỗi phía client", "body không khớp model Pydantic"],
    ["<b>429</b> Rate Limit", "quá số lượt cho phép", "gọi LLM quá nhiều → chờ, giảm tần suất, đổi provider"],
    ["5xx · <b>500</b> Internal Server Error", "lỗi phía server", "code crash (llm_app: lỗi PostgreSQL → 500)"],
    ["<b>502</b>", "lỗi phía server (upstream)", "llm_app: Gemini không sinh được câu trả lời"],
    ["<b>503</b>", "lỗi phía server", "dịch vụ chưa sẵn sàng (đề mẫu Q10: healthcheck gặp 503 → fail)"],
]) + "<p class='small muted'>Artifact còn liệt kê 201 (Created), 400 (Bad Request), 3xx (chuyển hướng): slide chỉ nêu theo nhóm 2xx/4xx/5xx nên chỉ cần nhớ nhóm. Timeout khi gọi LLM: đặt thời gian chờ hợp lý và retry; 5xx/429 kéo dài → dự phòng Groq.</p>" + src("fastapi_llm.pdf tr.6, 16–17; week4.pdf tr.13; llm_app/completed/routers/chat.py") + """
<h3 id="k4-env">.env và cấu hình</h3>
""" + pre('''
# .env (KHÔNG commit, nằm trong .gitignore)
DATABASE_URL=postgresql://user:secret@localhost:5432/chatdb
''', "bash") + pre('''
# Cách 1: python-dotenv
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")   # thiếu -> None
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set")

# Cách 2: pydantic-settings (gom và kiểm tra mọi biến ở một chỗ)
class Settings(BaseSettings):
    database_url: str                 # bắt buộc: thiếu -> lỗi rõ ràng khi khởi động
    app_env: str = "development"      # có mặc định
    class Config:
        env_file = ".env"
settings = Settings()
''', "python") + table(["Đoạn", "Ý nghĩa"], [
    [c("postgresql"), "driver/scheme"], [c("user:password"), "thông tin đăng nhập"],
    [c("localhost:5432"), "host + port (5432 = cổng mặc định của PostgreSQL)"], [c("chatdb"), "tên database"]]) + src("week4.pdf tr.20–24; fastapi_llm.pdf tr.12–13") + """
<h3 id="k4-sql">PostgreSQL: bảng, CRUD, JOIN</h3>
""" + pre('''
CREATE TABLE messages (
  id SERIAL PRIMARY KEY,          -- số tự tăng, định danh duy nhất
  role VARCHAR(20) NOT NULL,      -- "user" / "assistant"
  content TEXT NOT NULL,          -- TEXT không giới hạn độ dài
  created_at TIMESTAMP DEFAULT now()
);
INSERT INTO messages (role, content) VALUES ('user', 'Xin chao');   -- Create
SELECT * FROM messages ORDER BY created_at;                         -- Read
UPDATE messages SET content = 'Da sua' WHERE id = 1;                -- Update
DELETE FROM messages WHERE id = 1;                                  -- Delete

ALTER TABLE messages ADD COLUMN conversation_id INTEGER
  REFERENCES conversations(id);                                     -- khóa ngoại
SELECT c.title, m.role, m.content
FROM messages m JOIN conversations c ON m.conversation_id = c.id
WHERE c.id = 5 ORDER BY m.created_at;
''', "sql") + table(["Log lỗi", "Nguyên nhân / cách xử lý"], [
    [c("connection refused"), "sai connection string (host/port) hoặc container DB chưa chạy → kiểm tra <code>docker ps</code>"],
    [c('relation "messages" does not exist'), "chưa tạo bảng / chưa chạy migration trên DB này"],
    [c("invalid input syntax for type integer"), "sai kiểu dữ liệu, ví dụ chèn chuỗi \"abc\" vào cột INTEGER"]]) + """
<p id="k4-pool"><b>Connection pool:</b> mở sẵn vài kết nối (<code>min_size=2, max_size=10</code>), tạo <b>một lần khi server khởi động</b> và đóng một lần khi tắt (llm_app dùng <code>lifespan</code>), không tạo theo từng request. <b>Migration</b> (Alembic): script đổi schema có phiên bản, commit vào Git: <code>alembic revision --autogenerate -m "..."</code>, <code>alembic upgrade head</code>.</p>
""" + src("week4.pdf tr.25–34; llm_app/completed/db/database.py, main.py") + """
<h3 id="k4-test">Kiểm thử endpoint</h3>
""" + pre('''
curl -X POST http://localhost:8000/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Xin chào"}'
''', "bash") + pre('''
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}   # so sánh TOÀN BỘ body
''', "python") + "<p>Hoặc mở <code>localhost:8000/docs</code> (Swagger UI tự sinh) → chọn endpoint → <b>Try it out</b> → <b>Execute</b>.</p>" + src("fastapi_llm.pdf tr.18–19; CI.pdf tr.19; đề mẫu Q17")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["WSGI vs <b>ASGI</b>", "WSGI: chỉ đồng bộ, mỗi worker một request (Flask/Django cũ). ASGI: sync + async, nhiều request đồng thời — hợp chat/streaming/WebSocket, không bị chặn khi chờ LLM/DB."],
    [c("app.main:api") + " vs " + c("main.app:api"), "Trước dấu <code>:</code> là <b>module path</b> (thư mục.file), sau dấu <code>:</code> là <b>biến</b>. Đảo vị trí là sai."],
    ["<code>prefix</code> vs <code>tags</code>", "prefix ghép vào URL; tags chỉ nhóm trên /docs."],
    ["Request model vs <code>response_model</code>", "Request model kiểm tra dữ liệu vào (sai → 422). response_model định hình/lọc dữ liệu ra (bỏ field thừa)."],
    ["Thiếu field vs chuỗi rỗng", "<code>{\"role\":\"user\"}</code> thiếu content → 422. <code>\"content\": \"\"</code> vẫn là <code>str</code> hợp lệ (trừ khi có <code>min_length=1</code>)."],
    ["Kiểu dữ liệu vs giá trị cho phép", "<code>role: str</code> chỉ kiểm tra kiểu: \"moderator\" vẫn hợp lệ."],
    [c("os.getenv()") + " vs " + c("BaseSettings"), "getenv trả None khi thiếu biến (phải tự kiểm tra). BaseSettings gom về một chỗ, kiểm tra kiểu, thiếu biến bắt buộc → lỗi rõ ràng."],
    ["401 vs 429 vs timeout (LLM)", "401 sai key → kiểm tra .env/tạo key mới. 429 rate limit → chờ, giảm tần suất, đổi provider. Timeout → đặt thời gian chờ hợp lý và retry."],
    ["<code>response.json()</code> vs <code>response.json</code>", "Có ngoặc → dict body. Không ngoặc → đối tượng method (luôn truthy, không kiểm tra gì)."],
    ["PRIMARY KEY vs khóa ngoại (REFERENCES)", "PK định danh từng dòng. Khóa ngoại liên kết dòng sang bảng khác; JOIN “đi theo” liên kết đó."],
    ["TEXT vs VARCHAR(n)", "TEXT không giới hạn độ dài; VARCHAR(n) giới hạn n ký tự."],
    ["curl vs /docs", "curl: gõ lệnh trong terminal. /docs: Swagger UI tự sinh, bấm Try it out → Execute."],
]) + src("week4.pdf tr.8–9, 11, 13, 23–26; fastapi_llm.pdf tr.16, 18–19")

P["bay"] = trap("Bẫy 1 — đường dẫn uvicorn (đề mẫu Q1)", "File <code>app/main.py</code>, biến <code>api = FastAPI()</code>. Đúng: <code>uvicorn app.main:api</code>. Sai kiểu đảo: <code>main.app:api</code>, <code>app.api:main</code>, hoặc giữ <code>:app</code> theo thói quen.<br><b>Đổi một chỗ:</b> đổi tên biến thành <code>server</code> → lệnh thành <code>app.main:server</code>; chuyển file ra gốc <code>main.py</code> → <code>main:api</code>.", "k4-trap-uvicorn") + \
    trap("Bẫy 2 — prefix + path (đề mẫu Q2)", "<code>APIRouter(prefix=\"/chat\", tags=[\"messages\"])</code> + <code>@router.get(\"/history\")</code> → <code>GET /chat/history</code>. Không có <code>/messages/...</code> vì tags không vào URL.<br><b>Đổi một chỗ:</b> <code>@router.post(\"/history\")</code> → chỉ <code>POST /chat/history</code> khớp; gọi GET sẽ không khớp route này.", "k4-trap-prefix") + \
    trap("Bẫy 3 — thiếu field (Q3) và luật kiểm tra (Q4)", "<code>{\"role\": \"user\"}</code> thiếu <code>content</code> → <b>422</b> trước khi vào hàm (PostgreSQL không liên quan, không tự gán chuỗi rỗng/None).<br>Chỉ xét luật đã khai báo: <code>{\"role\":\"moderator\",\"content\":\"Hello\"}</code> và <code>{\"role\":\"assistant\",\"content\":\"\"}</code> đều <b>hợp lệ</b>.<br><b>Đổi một chỗ:</b> thêm <code>content: str = Field(..., min_length=1)</code> → chuỗi rỗng bị 422. Đổi thành <code>content: str | None = None</code> → thiếu content vẫn hợp lệ, content = None.", "k4-trap-422") + \
    trap("Bẫy 4 — response_model lọc field (Q5)", "Hàm trả <code>{\"id\":7,\"content\":\"Hello\",\"internal_token\":\"secret\"}</code> với <code>response_model=PublicMessage(id, content)</code> → client nhận <code>{\"id\": 7, \"content\": \"Hello\"}</code>. Field thừa bị <b>bỏ hẳn</b>, không thành <code>null</code>.<br><b>Đổi một chỗ:</b> bỏ <code>response_model</code> → token bị lộ ra client.", "k4-trap-respmodel") + \
    trap("Bẫy 5 — .env và lịch sử Git", "Lỡ commit password rồi xóa dòng đó ở commit sau: <b>vẫn lộ</b> vì commit cũ còn trong lịch sử. Cách đúng: .env + .gitignore ngay từ đầu.") + \
    trap("Bẫy 6 — pool và Depends", "Pool tạo <b>một lần</b> lúc khởi động (lifespan), không phải mỗi request. <code>Depends(get_conn)</code> chạy trước endpoint và đưa connection vào; gọi cùng dependency hai lần trong <b>một request</b> thì dùng lại kết quả đầu (cache). Lợi ích: test có thể override <code>get_conn</code> bằng kết nối giả.", "k4-depends") + \
    trap("Bẫy 7 — so sánh JSON trong test", "<code>/health</code> trong llm_app trả <code>{\"status\":\"ok\",\"model\":...}</code> → <code>assert response.json() == {\"status\": \"ok\"}</code> <b>FAIL</b> (thiếu key model). Muốn kiểm tra một phần: <code>response.json()[\"status\"] == \"ok\"</code>.")

P["checklist"] = [
    "Client-server, cấu trúc HTTP request/response (method, header, body), status code 2xx/3xx/4xx/5xx (200, 201, 400, 401, 404, 422, 500, 503)",
    "REST, endpoint, JSON; GET và POST",
    "Cấu trúc project: main.py, routers/, schemas/, db/, .env; APIRouter(prefix=..., tags=...) + include_router (tags chỉ dùng cho /docs)",
    "Uvicorn là ASGI server; ASGI và WSGI; cú pháp uvicorn package.module:biến --reload --port; trang /docs tự sinh",
    "Pydantic BaseModel: thiếu field hoặc sai kiểu thì trả 422; Optional/giá trị mặc định; response_model lọc bỏ field thừa",
    ".env + python-dotenv/settings, .env phải nằm trong .gitignore; tích hợp Gemini API key; các lỗi 401/429/timeout khi gọi LLM",
    "PostgreSQL: thiết kế bảng, khóa chính/ngoại, DATABASE_URL, connection pool, session dependency (Depends), SQL cơ bản và JOIN",
    "Test endpoint: /health, TestClient, assert response.status_code, response.json() == ...",
    "＋ Depends cache kết quả trong một request; pool tạo một lần lúc startup (lifespan)",
    "＋ 3 lỗi SQL hay gặp: connection refused · relation does not exist · invalid input syntax",
    "＋ Migration với Alembic (revision --autogenerate, upgrade head)",
    "＋ FastAPI vừa là server vừa là client khi gọi Gemini; 502 khi upstream lỗi; dự phòng Groq",
]

P["quick"] = [
    QQ("File <code>src/server.py</code> chứa <code>web = FastAPI()</code>. Lệnh uvicorn nào đúng?",
       ["<code>uvicorn src.server:web</code>", "<code>uvicorn server.src:web</code>", "<code>uvicorn src.web:server</code>", "<code>uvicorn src.server:app</code>"], "a",
       "Module path <code>src.server</code> (file src/server.py) + <code>:web</code> (tên biến)."),
    QQ("<code>APIRouter(prefix=\"/users\", tags=[\"account\"])</code> và <code>@router.get(\"/me\")</code>. URL nào khớp?",
       ["<code>GET /account/me</code>", "<code>GET /users/me</code>", "<code>GET /me/users</code>", "<code>GET /users/account/me</code>"], "b",
       "URL = prefix + path. tags chỉ dùng cho /docs."),
    QQ("Endpoint có <code>response_model=Out(id: int)</code> nhưng hàm trả <code>{\"id\": 1, \"pw\": \"x\"}</code>. Client nhận gì?",
       ["<code>{\"id\": 1, \"pw\": \"x\"}</code>", "<code>{\"id\": 1, \"pw\": null}</code>", "<code>{\"id\": 1}</code>", "Lỗi 422"], "c",
       "response_model lọc bỏ field không khai báo."),
]

P["docthem"] = "<p>Sách tham khảo của môn (Pro Git, Linux, Docker Deep Dive) không có chương về FastAPI/PostgreSQL. Nguồn chuẩn cho khối này là slide week4, fastapi_llm và code <code>materials/llm_app/</code> (bản <code>single_file/app.py</code> và <code>completed/</code>).</p>"

BLOCK = dict(id="K4", mon="TTNT", title="API app, .env, database", src="week4.pdf · fastapi_llm.pdf · llm_app", page=P)

S1 = "week4.pdf tr.9"
QUESTIONS = [
    Q("K4-D01", "single", "Consider the following file:",
      ["<code>uvicorn main.app:api --port 9000</code>", "<code>uvicorn app.api:main --port 9000</code>", "<code>uvicorn app.main:api --port 9000</code>", "<code>uvicorn app.main:app --port 9000</code>"], "c",
      "Cú pháp <code>uvicorn module_path:biến</code>. File <code>app/main.py</code> → <code>app.main</code>; biến là <code>api</code> → <code>:api</code>. Phương án a/b đảo vị trí; d dùng nhầm tên biến <code>app</code>.",
      S1 + "; đề mẫu Q1", "k4-uvicorn", code="# app/main.py\nfrom fastapi import FastAPI\n\napi = FastAPI()", lang="python", demo=1, hoi="Which command correctly serves this application on port 9000?"),
    Q("K4-D02", "single", "Consider:",
      ["<code>GET /history/chat</code>", "<code>GET /chat/ messages</code>", "<code>GET /messages/history</code>", "<code>GET /chat/history</code>"], "d",
      "URL = prefix <code>/chat</code> + path <code>/history</code> = <code>/chat/history</code>. <code>tags=[\"messages\"]</code> chỉ nhóm endpoint trên /docs, không vào URL.",
      "week4.pdf tr.11; đề mẫu Q2", "k4-router", code='router = APIRouter(prefix="/chat", tags=["messages"])\n\n@router.get("/history")\nasync def history():\n    return []', lang="python", demo=2, hoi="The router is included without an additional prefix. Which request directly matches this route?"),
    Q("K4-D03", "single", "The endpoint accepts this request model:",
      ["PostgreSQL rejects the request before FastAPI validates it.", "FastAPI returns a 422 response for the missing field.", "FastAPI assigns an empty string to content", "The endpoint receives content=None and continues."], "b",
      "Thiếu field bắt buộc <code>content</code> → Pydantic từ chối, FastAPI trả <b>422 Unprocessable Entity</b> trước khi hàm chạy. Không có giá trị mặc định nên không tự gán \"\" hay None; DB chưa hề được chạm tới.",
      "week4.pdf tr.12–13; đề mẫu Q3", "k4-trap-422", code="class ChatRequest(BaseModel):\n    role: str\n    content: str", lang="python", demo=3, hoi='The client sends: <code>{"role": "user"}</code>\nWhat is the standard result?'),
    Q("K4-D04", "multi", "Consider only the validation rules declared here:",
      ['<code>{"role": "moderator", "content": "Hello"}</code>', '<code>{"role": "user", "content": "Hello"}</code>', '<code>{"role": "user"}</code>', '<code>{"role": "assistant", "content": ""}</code>'], "abd",
      "Luật chỉ là: có <code>role</code> kiểu str và <code>content</code> kiểu str. \"moderator\" vẫn là str (không có ràng buộc giá trị); chuỗi rỗng \"\" vẫn là str (không có min_length). Chỉ (c) thiếu content → 422.",
      "week4.pdf tr.13; đề mẫu Q4", "k4-trap-422", code="class ChatRequest(BaseModel):\n    role: str\n    content: str", lang="python", demo=4, hoi="Which JSON bodies satisfy these rules?"),
    Q("K4-D05", "single", "Consider:",
      ['<code>{"id": 7, "content": "Hello", "internal_token": null}</code>', '<code>{"id": 7, "content": "Hello", "internal_token": "secret"}</code>', '<code>{"id": 7, "content": "Hello"}</code>', '<code>{"content": "Hello"}</code>'], "c",
      "<code>response_model=PublicMessage</code> định hình dữ liệu ra: chỉ giữ field đã khai báo (<code>id</code>, <code>content</code>), bỏ hẳn <code>internal_token</code> (không thành null). Đây là cách ẩn field nội bộ.",
      "week4.pdf tr.13; đề mẫu Q5", "k4-trap-respmodel",
      code='class PublicMessage(BaseModel):\n    id: int\n    content: str\n\n@app.get("/message", response_model=PublicMessage)\nasync def message():\n    return {\n        "id": 7,\n        "content": "Hello",\n        "internal_token": "secret"\n    }', lang="python", demo=5, hoi="Which JSON object is returned to the client?"),
    Q("K4-06", "multi", "Which statements about Uvicorn and ASGI are correct?",
      ["Uvicorn is an ASGI server that listens on a network port and hands each HTTP request to the FastAPI app.",
       "Without a server such as Uvicorn, <code>app = FastAPI()</code> is just an object in memory that nobody outside can reach.",
       "WSGI is preferred for a chat app because it serves other users while one request waits on an LLM call.",
       "<code>--reload</code> is recommended in production so the server restarts on every change."], "ab",
      "ASGI (không phải WSGI) phục vụ nhiều request đồng thời khi một request đang chờ LLM/DB. <code>--reload</code> chỉ dùng khi phát triển (dev only).",
      "week4.pdf tr.7–9", "k4-uvicorn"),
    Q("K4-07", "single", "Based on this router (from the course sample app), which request returns the stored messages of conversation 5?",
      ["<code>GET /chat/history?conversation_id=5</code>", "<code>GET /history/chat/5</code>", "<code>POST /chat/history</code> with body <code>5</code>", "<code>GET /conversations/5/history</code>"], "a",
      "prefix <code>/chat</code> + <code>/history</code>; tham số <code>conversation_id: int</code> không nằm trong path nên được truyền qua query string <code>?conversation_id=5</code>.",
      "materials/llm_app/completed/routers/chat.py", "k4-router",
      code='router = APIRouter(prefix="/chat", tags=["chat"])\n\n@router.get("/history", response_model=list[MessageResponse])\nasync def get_history(conversation_id: int, conn=Depends(get_conn)):\n    ...', lang="python"),
    Q("K4-08", "multi", "The project uses this settings class, and <code>.env</code> contains only one line: <code>DATABASE_URL=postgresql://user:secret@localhost:5432/chatdb</code>. Which statements are correct?",
      ["<code>settings.app_env</code> equals <code>\"development\"</code>.", "<code>settings.database_url</code> is loaded from the .env file.",
       "If DATABASE_URL were removed from .env, <code>settings.database_url</code> would silently become None.", "The .env file should be committed so teammates share the same password."], "ab",
      "<code>app_env</code> có giá trị mặc định. <code>database_url: str</code> bắt buộc: thiếu thì app lỗi rõ ràng khi khởi động (không âm thầm thành None — đó là hành vi của <code>os.getenv</code>). .env không bao giờ commit.",
      "week4.pdf tr.22–24", "k4-env",
      code='from pydantic_settings import BaseSettings\n\nclass Settings(BaseSettings):\n    database_url: str\n    app_env: str = "development"\n\n    class Config:\n        env_file = ".env"\n\nsettings = Settings()', lang="python"),
    Q("K4-09", "multi", "Consider <code>DATABASE_URL=postgresql://user:password@localhost:5432/chatdb</code>. Which statements are correct?",
      ["<code>chatdb</code> is the target database name.", "<code>5432</code> is PostgreSQL's default port.",
       "<code>user:password</code> names the table where messages are stored.", "A typo in the host gives a warning but still connects to the closest match."], "ab",
      "Các phần: scheme/driver · user:password (đăng nhập) · host:port (5432 là cổng mặc định PG) · tên DB. Sai một phần là bị từ chối hẳn, không có “gần đúng”.",
      "week4.pdf tr.20–21", "k4-env"),
    Q("K4-10", "single", "After deploying, the log shows:\n<code>relation \"messages\" does not exist</code>\nWhat is the most likely cause?",
      ["The table was never created, or the migration was never run against this database.", "The password in DATABASE_URL is wrong.",
       "A string was inserted into an INTEGER column.", "The PostgreSQL container is not running."], "a",
      "Ba lỗi hay gặp: <code>connection refused</code> (sai host/port, DB chưa chạy) · <code>relation ... does not exist</code> (chưa tạo bảng/chưa migrate) · <code>invalid input syntax for type integer</code> (sai kiểu).",
      "week4.pdf tr.32", "k4-sql"),
    Q("K4-11", "multi", "Which statements about <code>Depends(get_conn)</code> and the connection pool are correct?",
      ["FastAPI calls <code>get_conn</code> before the endpoint runs and passes its result in.", "Within a single request, calling the same dependency twice reuses the first result.",
       "A new connection pool is created for every incoming request.", "Dependency injection makes it impossible to replace <code>get_conn</code> in tests."], "ab",
      "Pool được tạo <b>một lần</b> khi server khởi động và đóng khi tắt. Dependency injection còn giúp test override <code>get_conn</code> bằng kết nối giả.",
      "week4.pdf tr.15–16, 30–31", "k4-depends"),
    Q("K4-12", "single", "The FastAPI app calls the Gemini API and receives HTTP 429. What does it mean and what is the recommended reaction?",
      ["The API key is wrong; create a new key in .env.", "Rate limit exceeded; wait, reduce the request rate or switch provider.",
       "The server code crashed; restart Uvicorn with --reload.", "The request body failed Pydantic validation; fix the JSON."], "b",
      "401 = sai API key; 429 = rate limit (chờ, giảm tần suất, đổi provider như Groq); timeout = đặt thời gian chờ và retry; 422 = lỗi validation.",
      "fastapi_llm.pdf tr.16–17", "k4-status"),
    Q("K4-13", "multi", "In the course sample app, <code>/health</code> is defined as below. Which test assertions pass?",
      ["<code>assert response.status_code == 200</code>", '<code>assert response.json()["status"] == "ok"</code>',
       '<code>assert response.json() == {"status": "ok"}</code>', "<code>assert response.json == 200</code>"], "ab",
      "Body thật là <code>{\"status\": \"ok\", \"model\": ...}</code> nên so sánh toàn bộ với <code>{\"status\": \"ok\"}</code> sẽ fail. <code>response.json</code> (không ngoặc) là method, không phải dữ liệu.",
      "llm_app/completed/main.py; CI.pdf tr.19", "k4-test",
      code='@app.get("/health", tags=["health"])\nasync def health():\n    return {\n        "status": "ok",\n        "model": settings.gemini_model,\n    }\n\n# test\nresponse = client.get("/health")', lang="python"),
    Q("K4-14", "single", "Given the table definition, which statement succeeds?",
      ["<code>INSERT INTO messages (role, content) VALUES ('user', 'Xin chao');</code>", "<code>INSERT INTO messages (content) VALUES ('hi');</code>",
       "<code>INSERT INTO messages (role, content) VALUES ('user', NULL);</code>", "<code>INSERT INTO messages (id, role, content) VALUES ('abc', 'user', 'hi');</code>"], "a",
      "<code>role</code> và <code>content</code> đều NOT NULL nên (b), (c) lỗi. (d) chèn 'abc' vào cột số → <code>invalid input syntax for type integer</code>. id tự tăng (SERIAL), created_at mặc định now().",
      "week4.pdf tr.26–27, 32", "k4-sql",
      code="CREATE TABLE messages (\n  id SERIAL PRIMARY KEY,\n  role VARCHAR(20) NOT NULL,\n  content TEXT NOT NULL,\n  created_at TIMESTAMP DEFAULT now()\n);", lang="sql"),
]
