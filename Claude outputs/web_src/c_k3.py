from h import *

PERM = """<svg viewBox="0 0 640 150" width="640" role="img" aria-label="Đọc chuỗi quyền">
<g font-size="15" class="mono">
<rect x="10" y="20" width="40" height="40" class="box"/><text x="23" y="46">-</text>
<rect x="56" y="20" width="120" height="40" class="boxa"/><text x="90" y="46">r w x</text>
<rect x="182" y="20" width="120" height="40" class="box"/><text x="216" y="46">r - x</text>
<rect x="308" y="20" width="120" height="40" class="box"/><text x="342" y="46">- - -</text>
</g>
<g font-size="12.5">
<text x="8" y="80">loại</text><text x="8" y="96" class="muted">- file</text><text x="8" y="112" class="muted">d thư mục</text><text x="8" y="128" class="muted">l symlink</text>
<text x="92" y="80">owner (u)</text><text x="88" y="100" class="mono">4+2+1 = 7</text>
<text x="218" y="80">group (g)</text><text x="214" y="100" class="mono">4+0+1 = 5</text>
<text x="340" y="80">others (o)</text><text x="344" y="100" class="mono">0+0+0 = 0</text>
<text x="450" y="36">→ chmod 750 file</text><text x="450" y="58" class="muted">r = 4 · w = 2 · x = 1</text>
<text x="450" y="80" class="muted">umask = bit bị TẮT</text><text x="450" y="100" class="muted">file gốc rw-rw-rw- (666)</text><text x="450" y="120" class="muted">thư mục gốc rwxrwxrwx (777)</text>
</g></svg>"""

LINK = """<svg viewBox="0 0 640 170" width="640" role="img" aria-label="Hard link và symbolic link">
<g font-size="13">
<rect x="10" y="20" width="110" height="32" rx="6" class="box"/><text x="22" y="41" class="mono">Hi.txt</text>
<rect x="10" y="66" width="110" height="32" rx="6" class="box"/><text x="22" y="87" class="mono">Hi-hard</text>
<rect x="210" y="40" width="150" height="40" rx="6" class="boxa"/><text x="222" y="58">inode 1234</text><text x="222" y="74" class="muted" font-size="11.5">link count = 2</text>
<rect x="440" y="40" width="150" height="40" rx="6" class="box"/><text x="452" y="65">dữ liệu trên đĩa</text>
<path d="M120 36 L206 54" class="ln"/><path d="M120 82 L206 66" class="ln"/><path d="M360 60 h76" class="ln"/>
<rect x="10" y="120" width="110" height="32" rx="6" class="box"/><text x="22" y="141" class="mono">Hi-sym</text>
<path d="M120 136 C 160 136 150 40 120 40" class="ln dash"/>
<text x="150" y="138" font-size="12" class="muted">symlink chứa đường dẫn "Hi.txt" (inode riêng).</text><text x="150" y="156" font-size="12" class="muted">Xoá Hi.txt → Hi-sym hỏng; Hi-hard vẫn đọc được.</text>
</g></svg>"""

P = {}
P["y"] = """<p>Server (VPS/EC2) thường <b>không có giao diện đồ hoạ</b> — mọi thao tác qua <b>shell</b> (bash) và <b>SSH</b>. Khối này gồm: đi lại trong cây thư mục, thao tác file, ghép lệnh bằng pipeline, mô hình nhiều người dùng với quyền rwx, và kết nối/copy an toàn bằng cặp khoá SSH.</p>""" + src("week3.pdf tr.3, 20, 29")

P["mohinh"] = """<h3 id="k3-perm-model">Chuỗi quyền trong <code>ls -l</code></h3>""" + diagram(PERM, "week3.pdf tr.21–25") + """
<h3 id="k3-link-model">Hard link và symbolic link</h3>""" + diagram(LINK, "week3.pdf tr.17–18; TLCL tr.59, 63–65") + """
<h3 id="k3-ssh-model">Xác thực SSH bằng cặp khoá</h3>""" + flow(["Máy local: private key (giữ bí mật)", "tạo yêu cầu kết nối", "Server: public key (~/.ssh/authorized_keys) kiểm tra", "hợp lệ → phiên mã hoá"], active=(0, 2)) + src("week3.pdf tr.30; CD.pdf tr.17")

P["bang"] = """<h3 id="k3-nav">Shell &amp; điều hướng</h3>""" + table(["Lệnh / ký hiệu", "Ý nghĩa"], [
    [c("me@linuxbox:~$"), "user@máy:thư-mục-hiện-tại, kết thúc bằng <code>$</code>; kết thúc bằng <code>#</code> = <b>superuser</b>"],
    ["↑ ↓ · Ctrl-r · ~/.bash_history", "lịch sử lệnh (mặc định nhớ 1000 lệnh) · tìm lịch sử"],
    [c("exit") + " · Ctrl-d", "kết thúc phiên"], [c("/"), "thư mục gốc; một cây duy nhất, thiết bị được mount vào cây (xem <code>df -h</code>)"],
    [c("pwd") + " · " + c("cd") + " · " + c("ls"), "thư mục hiện tại · đổi thư mục · liệt kê"],
    ["Đường dẫn tuyệt đối / tương đối", "bắt đầu bằng <code>/</code> / tính từ thư mục hiện tại"],
    [c(".") + " " + c("..") + " " + c("~") + " " + c("cd -"), "hiện tại · cha · home · quay lại thư mục trước"],
    [c("ls -a") + " / " + c("ls -l") + " / " + c("ls -li"), "kể cả file ẩn (bắt đầu bằng .) / chi tiết / kèm số inode"]]) + src("week3.pdf tr.4–12") + """
<h3 id="k3-files">Thao tác file</h3>""" + table(["Lệnh", "Ý nghĩa"], [
    [c("mkdir dir1 dir2") + " · " + c("mkdir -p a/b/c"), "tạo thư mục · tạo kèm thư mục cha (TLCL tr.71)"],
    [c("cp a b") + " · " + c("cp -r dir1 dir2") + " · " + c("cp -i") + " · " + c("-a -u -v"), "copy · copy thư mục (bắt buộc -r) · hỏi trước khi ghi đè · giữ thuộc tính / chỉ file mới hơn / in chi tiết"],
    [c("mv a b"), "đổi tên hoặc di chuyển; đích là thư mục có sẵn → chuyển vào trong; chưa có → đổi tên"],
    [c("rm file") + " · " + c("rm -r dir") + " · " + c("rm -rf dir"), "xoá; Linux <b>không có undelete</b>. Thử wildcard bằng <code>ls</code> trước (<code>rm * .html</code> có dấu cách là xoá sạch!)"],
    [c("ln file link"), "hard link: cùng inode, không vượt filesystem, không link thư mục"],
    [c("ln -s item link"), "symlink: file chứa đường dẫn tới đích; vượt filesystem, link được thư mục; <code>ls -l</code> hiện <code>l... link -&gt; target</code>"],
    [c("touch f") + " · " + c("> f"), "tạo file rỗng"]]) + table(["Wildcard", "Khớp"], [
    [c("*"), "mọi ký tự, kể cả không ký tự nào"], [c("?"), "đúng một ký tự"], [c("[abc]") + " · " + c("[!abc]"), "một ký tự trong / ngoài tập"],
    [c("[[:upper:]]*"), "bắt đầu bằng chữ hoa (lớp: alnum, alpha, digit, lower, upper)"], [c("BACKUP.[0-9][0-9][0-9]"), "BACKUP. + đúng 3 chữ số"],
    [c(".[!.]*"), "file ẩn nhưng loại <code>.</code> và <code>..</code>"]]) + src("week3.pdf tr.10–18") + """
<h3 id="k3-pipe">Pipeline &amp; redirect</h3>""" + pre("""
ls /bin | sort | uniq | wc -l      # đếm tên duy nhất (uniq cần dữ liệu đã sort)
ls /bin | grep zip                 # chỉ dòng chứa "zip"
tail -f /var/log/messages          # theo dõi file log liên tục
ls /bin | tee list.txt             # ghi ra file VÀ vẫn in ra màn hình
head -n 5 f · tail -n 5 f · wc -l / -w / -c f   # 5 dòng đầu/cuối · đếm dòng/từ/byte
""", "bash") + table(["Toán tử (sách TLCL, không có trong slide)", "Ý nghĩa"], [
    [c("cmd > file"), "ghi stdout vào file, <b>ghi đè từ đầu</b>; lệnh lỗi → file bị cắt về 0 byte"],
    [c("cmd >> file"), "nối thêm vào cuối (chưa có thì tạo)"], [c("cmd 2> err.txt"), "chuyển stderr"],
    [c("cmd > out 2>&1") + " · " + c("cmd &> out"), "gom cả stdout và stderr vào một file"]]) + src("week3.pdf tr.19; ex3.docx Part C; TLCL tr.81–85, 89") + """
<h3 id="k3-perm">Quyền</h3>""" + table(["Thuộc tính", "Với file", "Với thư mục"], [
    ["r", "mở/đọc file", "liệt kê nội dung"], ["w", "ghi/cắt file", "tạo/xoá/đổi tên file bên trong (cần thêm x)"], ["x", "chạy như chương trình", "vào thư mục (cd), truy cập metadata"]]) + table(["Lệnh", "Kết quả"], [
    [c("chmod 600 foo.txt"), "rw------- (chỉ owner đọc/ghi)"], [c("chmod 664 f"), "rw-rw-r--"], [c("chmod 755 script.sh"), "rwxr-xr-x"], [c("chmod 777 f"), "rwxrwxrwx (mọi người toàn quyền)"],
    [c("chmod u+x s.sh") + " · " + c("u-x") + " · " + c("o-rw"), "thêm/bớt quyền theo ký hiệu: u g o a, + - ="],
    [c("chmod go+rx,u+x file"), "nhiều chỉ định, cách nhau dấu phẩy"],
    [c("umask") + " · " + c("umask 0022"), "xem / đặt mask. 0002 → file mới rw-rw-r-- (664); 0022 → rw-r--r-- (644); thư mục mới với 0002 → rwxrwxr-x"],
    [c("chown bob:users f") + " · " + c("chown :admins f") + " · " + c("chgrp admins f"), "đổi owner và group · chỉ group · lệnh cũ chỉ đổi group (cần quyền superuser)"],
    [c("id"), "uid, gid, các group của bạn"],
    [c("su -") + " · " + c("su -c \"ls -l /root\""), "mở login shell user khác (mặc định root), cần <b>mật khẩu user đó</b>"],
    [c("sudo systemctl restart nginx") + " · " + c("sudo -l"), "chạy <b>một lệnh</b> với quyền cao, cần <b>mật khẩu của bạn</b>, không mở shell mới · xem quyền sudo"],
    [c("sudo chmod g+s /usr/local/share/Music"), "file mới trong thư mục kế thừa group (thư mục chia sẻ)"]]) + note("umask là <b>mask theo bit</b>: chỗ nào bit = 1 thì quyền đó bị tắt. Mẹo “666 − umask” chỉ đúng với các mask thường gặp (002, 022, 077); ví dụ umask 003 cho file 664, không phải 663.", "warn") + src("week3.pdf tr.20–28; TLCL tr.60, 126–127") + """
<h3 id="k3-ssh">SSH, copy file, kiểm tra mạng</h3>""" + pre("""
ssh-keygen                                   # tạo cặp khoá trên máy LOCAL
ssh user@<vps-address>                       # đăng nhập
ssh -i my-key.pem ubuntu@<dia-chi-cong-khai> # EC2: dùng private key .pem, user ubuntu
scp file.txt user@<vps-address>:/path/       # copy một file qua kết nối mã hoá
rsync -av folder/ user@<vps-address>:/path/  # đồng bộ cả thư mục, cập nhật nhiều lần
ping host · traceroute host                  # kiểm tra mạng trước khi nghi key/firewall
""", "bash") + "<p>SSH vừa <b>xác thực</b> server trước khi trao đổi dữ liệu, vừa <b>mã hoá</b> toàn bộ phiên. <code>sftp</code>: bản thay thế an toàn, tương tác cho ftp.</p>" + src("week3.pdf tr.29–33; cloudcomputing.pdf tr.13")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["Hard link vs symlink", "Hard: cùng inode, link count tăng, xoá file gốc vẫn đọc được qua hard link; không vượt filesystem, không link thư mục. Sym: file riêng chứa đường dẫn; xoá đích → link hỏng; link được thư mục, vượt filesystem."],
    ["Tuyệt đối vs tương đối", "<code>/home/me/a</code> luôn từ gốc; <code>../a</code> tính từ thư mục hiện tại."],
    [c("$") + " vs " + c("#"), "user thường vs superuser."],
    [c("su") + " vs " + c("sudo"), "su: shell user khác, mật khẩu của user đó. sudo: một lệnh, mật khẩu của bạn, không mở shell mới; Ubuntu tắt đăng nhập root trực tiếp, dựa vào sudo."],
    ["Octal vs ký hiệu", "<code>chmod 640</code> đặt toàn bộ; <code>chmod g+w</code> chỉ thêm/bớt phần được nêu."],
    [c("chmod") + " vs " + c("chown"), "đổi quyền vs đổi chủ sở hữu/nhóm (chown cần superuser)."],
    [c("scp") + " vs " + c("rsync"), "scp: một file, nhanh gọn. rsync: đồng bộ thư mục, nhiều file, cập nhật lặp lại."],
    ["Private key vs public key", "Private: ở máy local, tuyệt đối bí mật. Public: đặt trên server để xác thực user."],
    [c("cp -i") + " vs " + c("cp"), "-i hỏi trước khi ghi đè (ex3 Part A.5)."],
    [c("|") + " vs " + c("tee"), "pipe chuyển output sang lệnh khác; tee vừa ghi file vừa đưa tiếp ra màn hình."],
]) + src("week3.pdf tr.9, 14, 17–18, 22–32")

P["bay"] = trap("Bẫy 1 — xoá file gốc", "Thứ tự trong ex3: <code>ln Hi.txt Hi-hard</code>, <code>ln -s Hi.txt Hi-sym</code>, <code>rm Hi.txt</code> → <code>cat Hi-hard</code> vẫn ra nội dung (inode còn, link count giảm 1); <code>cat Hi-sym</code> báo không tìm thấy (link hỏng, ls tô đỏ).", "k3-trap-link") + \
    trap("Bẫy 2 — uniq không sort", "<code>ls /bin /usr/bin | uniq | wc -l</code> đếm sai vì uniq chỉ bỏ dòng trùng <b>liền kề</b>. Phải <code>sort</code> trước: <code>ls /bin /usr/bin | sort | uniq | wc -l</code>.", "k3-trap-uniq") + \
    trap("Bẫy 3 — umask", "umask 0002 → file mới <code>rw-rw-r--</code>. <b>Đổi một chỗ:</b> umask 0022 → <code>rw-r--r--</code>; umask 0000 → <code>rw-rw-rw-</code>. File mới không bao giờ có x mặc định (gốc là 666).", "k3-trap-umask") + \
    trap("Bẫy 4 — quyền thư mục", "Có <code>w</code> mà thiếu <code>x</code> trên thư mục thì vẫn không tạo/xoá file được. Có <code>r</code> mà thiếu <code>x</code>: liệt kê tên nhưng không cd vào được.", "k3-trap-dir") + \
    trap("Bẫy 5 — octal hay nhầm", "600 = rw------- · 640 = rw-r----- · 644 = rw-r--r-- · 664 = rw-rw-r-- · 700 = rwx------ · 755 = rwxr-xr-x · 777 = rwxrwxrwx.", "k3-trap-octal") + \
    trap("Bẫy 6 — khoá nào ở đâu", "Private key ở <b>máy mình</b> (hoặc trong secret của runner); public key ở <b>server</b>. Server dùng public key để kiểm tra, không bao giờ cần private key.", "k3-trap-key") + \
    trap("Bẫy 7 — <code>&gt;</code> ghi đè cả khi lệnh lỗi", "<code>ls -l /khong-co &gt; out.txt</code>: lỗi vẫn in ra màn hình (stderr không bị chuyển) và out.txt bị cắt còn 0 byte (TLCL tr.81–82, ngoài slide).")

P["checklist"] = [
    "Prompt $ và #, lịch sử lệnh, cây thư mục bắt đầu từ /, đường dẫn tuyệt đối và tương đối, . .. ~",
    "pwd, cd, ls -l/-a/-li, mkdir -p, cp -i/-r, mv, rm -r, touch, wildcard",
    "Hard link và symlink (ln, ln -s): inode, link count, xóa file gốc thì symlink bị hỏng còn hard link vẫn đọc được",
    "Pipe và redirect: >, >>, 2>, |, sort, uniq (cần sort trước), wc -l/-w/-c, grep, head, tail, tee",
    "Quyền rwx cho user/group/other, số bát phân (r=4, w=2, x=1), chmod 600/664/777, chmod u+x, chown, sudo; umask: file mặc định 666 − umask, thư mục 777 − umask",
    "SSH: cặp khóa (private giữ ở máy mình, public đặt trong ~/.ssh/authorized_keys trên server), ssh-keygen, ssh -i key.pem user@host, chmod 400 key.pem, scp",
    "＋ su vs sudo; chown/chgrp; chmod g+s cho thư mục chia sẻ; id",
    "＋ scp vs rsync; ping/traceroute trước khi nghi key",
    "＋ Ý nghĩa r/w/x trên thư mục khác trên file",
]

P["quick"] = [
    QQ("Prompt <code>root@server:/etc#</code> cho biết gì?", ["Đang ở home, user thường", "Phiên có quyền superuser, đang ở /etc", "Lệnh trước bị lỗi", "Đang trong container Docker"], "b", "Dấu # = superuser; phần trước là thư mục hiện tại."),
    QQ("umask 0022, tạo file mới bằng <code>&gt; f</code>. <code>ls -l f</code> hiện quyền nào?", ["rw-rw-rw-", "rw-r--r--", "rwxr-xr-x", "rw-rw-r--"], "b", "666 bỏ bit w của group và others → 644."),
    QQ("Xoá file gốc thì loại link nào vẫn đọc được nội dung?", ["Symbolic link", "Hard link", "Cả hai", "Không loại nào"], "b", "Hard link dùng chung inode."),
]

P["docthem"] = ul([
    "TLCL tr.81–85: chuyển hướng I/O chi tiết (<code>&gt;</code>, <code>&gt;&gt;</code>, <code>2&gt;</code>, <code>2&gt;&amp;1</code>, <code>&amp;&gt;</code>, <code>/dev/null</code>).",
    "TLCL tr.127: các quyền đặc biệt setuid (4000), setgid (2000), sticky bit (1000) — lý do umask viết 4 chữ số.",
    "TLCL tr.251: cảnh báo host key đổi trong <code>~/.ssh/known_hosts</code>, xoá dòng cũ bằng <code>ssh-keygen -R</code>.",
    "Chương Processes (TLCL tr.137+): <code>ps</code>, <code>top</code>, <code>kill</code>, job control — slide không dạy.",
])

BLOCK = dict(id="K3", mon="TTNT", title="Linux shell, file, quyền, SSH", src="week3.pdf · The Linux Command Line", page=P)

QUESTIONS = [
    Q("K3-01", "single", "A prompt reads <code>admin@web01:/var/log#</code>. Which statement is correct?",
      ["The session has superuser privileges and the current directory is /var/log.", "The user is admin without privileges, in the home directory.", "The last command failed.", "The shell is not bash."], "a",
      "Định dạng prompt: user@máy:thư-mục; kết thúc bằng # thay vì $ = superuser.", "week3.pdf tr.4", "k3-nav"),
    Q("K3-02", "single", "What does the last command print?", ["<code>/home</code>", "<code>/home/me</code>", "<code>/</code>", "<code>/home/me/Desktop/../..</code>"], "a",
      "<code>..</code> lên một cấp: Desktop → me → home.", "week3.pdf tr.8–9", "k3-nav", code="me@linuxbox:~$ cd Desktop\nme@linuxbox:~/Desktop$ cd ../..\n$ pwd", lang="bash"),
    Q("K3-03", "multi", "Which file names match the pattern <code>BACKUP.[0-9][0-9][0-9]</code>?", ["<code>BACKUP.001</code>", "<code>BACKUP.1</code>", "<code>BACKUP.123</code>", "<code>backup.123</code>"], "ac",
      "Pattern yêu cầu đúng “BACKUP.” (phân biệt hoa thường) và đúng ba chữ số.", "week3.pdf tr.11", "k3-files"),
    Q("K3-04", "multi", "In <code>dir2</code>, <code>Hi.txt</code> contains \"hello\". After running the commands below, which statements are correct?",
      ["<code>cat Hi-hard</code> still prints hello.", "<code>Hi-sym</code> is now a broken link.", "Before the rm, Hi-hard and Hi.txt showed the same inode number in <code>ls -li</code>.", "Hi-sym has the same inode number as Hi.txt."], "abc",
      "Hard link chia sẻ inode nên dữ liệu còn khi xoá một tên. Symlink là file riêng chứa đường dẫn, đích mất thì link hỏng.", "week3.pdf tr.17–18; ex3.docx Part B; TLCL tr.63–65", "k3-trap-link",
      code="ln Hi.txt Hi-hard\nln -s Hi.txt Hi-sym\nrm Hi.txt", lang="bash"),
    Q("K3-05", "multi", "Which statements about these pipelines are correct?",
      ["<code>ls /bin | sort | uniq | wc -l</code> counts unique program names.", "<code>ls /bin | grep zip</code> prints only names containing \"zip\".",
       "<code>ls /bin | tee list.txt</code> saves the list to list.txt and still shows it on the screen.", "<code>uniq</code> removes all duplicates correctly even if its input is not sorted."], "abc",
      "uniq chỉ bỏ dòng trùng liền kề → cần sort trước. tee ghi file đồng thời chuyển tiếp ra stdout.", "week3.pdf tr.19; ex3.docx Part C; TLCL tr.89", "k3-trap-uniq"),
    Q("K3-06", "multi", "Exercise 3 asks: secret.txt → only the owner can read/write; shared.txt → owner and group read/write, others read only; public.txt → everyone can read, write and execute. Which commands are correct?",
      ["<code>chmod 600 secret.txt</code>", "<code>chmod 664 shared.txt</code>", "<code>chmod 777 public.txt</code>", "<code>chmod 644 shared.txt</code>"], "abc",
      "rw- = 6, r-- = 4, rwx = 7, --- = 0. 644 cho group chỉ đọc nên sai yêu cầu của shared.txt.", "week3.pdf tr.23; ex3.docx Part D", "k3-trap-octal"),
    Q("K3-07", "single", "What permissions does the new file get?", ["<code>-rw-r--r--</code>", "<code>-rw-rw-r--</code>", "<code>-rwxr-xr-x</code>", "<code>-rw-rw-rw-</code>"], "a",
      "Quyền gốc của file rw-rw-rw-; mask 0022 tắt bit w của group và others → rw-r--r--.", "week3.pdf tr.25; TLCL tr.126–127", "k3-trap-umask",
      code="umask 0022\n> foo.txt\nls -l foo.txt", lang="bash"),
    Q("K3-08", "single", "<code>file</code> currently has mode <code>rw-------</code>. What is its mode after this command?", ["<code>rwxr-xr-x</code>", "<code>rw-r-xr-x</code>", "<code>rwx------</code>", "<code>r-xr-xr-x</code>"], "a",
      "u+x thêm x cho owner → rwx; go+rx thêm r và x cho group và others → r-x. Ký hiệu chỉ thêm phần được nêu, giữ nguyên phần còn lại.", "week3.pdf tr.24", "k3-perm",
      code="chmod go+rx,u+x file", lang="bash"),
    Q("K3-09", "multi", "Which statements about the r, w, x attributes are correct?",
      ["r on a directory allows listing its contents.", "x on a directory allows entering it with cd.", "w on a directory alone (without x) is enough to delete files inside it.", "x on a file allows executing it as a program."], "abd",
      "w trên thư mục cho tạo/xoá/đổi tên file bên trong nhưng cần kèm x.", "week3.pdf tr.22", "k3-trap-dir"),
    Q("K3-10", "multi", "Which statements about SSH key-pair authentication are correct?",
      ["The private key stays on the local machine and must never be shared.", "The public key is stored on the server and used to verify the user.",
       "<code>ssh-keygen</code> creates the key pair on the local machine.", "The server needs a copy of the private key to verify the connection."], "abc",
      "Local dùng private key tạo yêu cầu kết nối; server dùng public key để xác minh; hợp lệ thì lập kết nối mã hoá.", "week3.pdf tr.30–31", "k3-trap-key"),
    Q("K3-11", "single", "You must repeatedly synchronise a whole project folder with many files to the VPS. Which command fits the lecture's recommendation?",
      ["<code>rsync -av folder/ user@&lt;vps-address&gt;:/path/</code>", "<code>scp file.txt user@&lt;vps-address&gt;:/path/</code>", "<code>ssh-keygen folder/</code>", "<code>ln -s folder/ user@&lt;vps-address&gt;</code>"], "a",
      "scp hợp với copy một file nhanh; rsync đồng bộ cả thư mục, nhiều file, cập nhật lặp lại.", "week3.pdf tr.32", "k3-ssh"),
    Q("K3-12", "multi", "Which statements about <code>su</code> and <code>sudo</code> are correct?",
      ["<code>sudo command</code> runs a single command with elevated privileges and asks for your own password.", "<code>su -</code> starts a login shell as another user (root by default) and needs that user's password.",
       "<code>sudo</code> always starts a new root shell.", "Ubuntu enables direct root login and does not rely on sudo."], "ab",
      "sudo không mở shell/môi trường mới; Ubuntu tắt đăng nhập root trực tiếp và dựa vào sudo.", "week3.pdf tr.26", "k3-perm"),
    Q("K3-13", "multi", "Consider this line from <code>ls -l</code>. Which statements are correct?",
      ["reports is a directory.", "Members of group dev can list it and enter it.", "Other users can enter it.", "The owner can create files inside it."], "abd",
      "d = thư mục; owner rwx; group r-x (đọc + vào); others --- (không có quyền gì).", "week3.pdf tr.21–22", "k3-perm-model",
      code="drwxr-x--- 2 me dev 4096 2026-09-10 10:00 reports", lang="text"),
    Q("K3-14", "single", "<code>ssh ubuntu@203.0.113.25</code> cannot connect. According to the lecture, what should you check first?",
      ["Network reachability with <code>ping</code> (and <code>traceroute</code>), before suspecting key configuration or firewall issues.", "Regenerate the key pair immediately.",
       "Run <code>chmod 777</code> on the home directory.", "Reinstall bash on the server."], "a",
      "Ghi chú cuối slide: ssh không kết nối được → kiểm tra mạng bằng ping trước khi nghi key/firewall.", "week3.pdf tr.33", "k3-ssh"),
]
