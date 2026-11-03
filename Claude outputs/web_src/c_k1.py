from h import *

SVG = """<svg viewBox="0 0 700 262" width="700" role="img" aria-label="Ba vùng của Git và các lệnh di chuyển giữa chúng">
<g font-size="13">
<path d="M95 50 C 250 22 450 22 605 50" class="ln dash"/><path d="M597 42 l8 8 l-10 2" class="ln"/><text x="350" y="14" text-anchor="middle" class="mono" font-size="12">git commit -a (chỉ file đã track)</text>
<rect x="10" y="50" width="170" height="90" rx="10" class="box"/><text x="22" y="74" font-weight="700">Working tree</text><text x="22" y="96" class="muted">bản checkout trên đĩa</text><text x="22" y="118" class="muted">trạng thái: modified</text>
<rect x="265" y="50" width="170" height="90" rx="10" class="boxa"/><text x="277" y="74" font-weight="700">Staging area</text><text x="277" y="96" class="muted">“the index” (trong .git)</text><text x="277" y="118" class="muted">trạng thái: staged</text>
<rect x="520" y="50" width="170" height="90" rx="10" class="box"/><text x="532" y="74" font-weight="700">Git directory (.git)</text><text x="532" y="96" class="muted">metadata + object DB</text><text x="532" y="118" class="muted">trạng thái: committed</text>
<path d="M180 95 h80" class="lna"/><path d="M254 90 l7 5 l-7 5" class="lna"/><text x="196" y="88" class="mono" font-size="12">git add</text>
<path d="M435 95 h80" class="lna"/><path d="M509 90 l7 5 l-7 5" class="lna"/><text x="440" y="88" class="mono" font-size="12">git commit</text>
<path d="M330 140 C 310 172 170 172 140 140" class="ln dash"/><path d="M146 147 l-6 -7 l9 0" class="ln"/>
<text x="180" y="188" class="mono" font-size="12">git restore --staged / git reset HEAD &lt;file&gt;</text>
<path d="M605 140 C 560 236 140 236 95 140" class="ln dash"/><path d="M101 147 l-6 -7 l9 0" class="ln"/>
<text x="210" y="226" class="mono" font-size="12">git restore &lt;file&gt; (bỏ thay đổi — mất luôn!)</text>
<text x="10" y="256" font-size="12.5">git diff = working tree ↔ staging · git diff --staged = staging ↔ commit cuối</text>
</g></svg>"""

P = {}
P["y"] = """<p><b>Git</b> là hệ quản lý phiên bản <b>phân tán</b> (DVCS): mỗi bản clone chứa toàn bộ lịch sử. Git lưu <b>snapshot</b> (ảnh chụp toàn bộ file được track) chứ không lưu diff; hầu hết thao tác chạy <b>local</b>; mọi thứ được checksum bằng <b>SHA-1</b> nên không thể sửa nội dung mà Git không biết.</p>
<p>Mô hình cần thuộc: <b>3 trạng thái</b> (modified, staged, committed) ↔ <b>3 vùng</b> (working tree, staging area, .git).</p>""" + src("week01.pdf tr.12, 18–33")

P["mohinh"] = diagram(SVG, "3 vùng của Git (week01.pdf tr.28–33, 53, 56, 64–65)") + """
<h3 id="k1-vcs">Ba kiểu hệ quản lý phiên bản</h3>""" + table(["Kiểu", "Ví dụ", "Đặc điểm"], [
    ["Local VCS", "chép thư mục, RCS", "RCS lưu patch set (khác biệt giữa các phiên bản); đơn giản nhưng dễ ghi đè nhầm"],
    ["Tập trung (CVCS)", "CVS, Subversion, Perforce", "một server trung tâm; dễ quản trị, phân quyền chi tiết; <b>điểm lỗi duy nhất</b>: server sập là không ai cộng tác được, hỏng đĩa không backup là mất hết lịch sử"],
    ["Phân tán (DVCS)", "<b>Git</b>, Mercurial, Darcs", "mỗi client mirror toàn bộ repo + lịch sử, <b>mỗi clone là một bản backup</b>; làm việc với nhiều remote"]]) + """
<h3 id="k1-objects">Commit lưu gì</h3><p><code>git add README test.rb LICENSE</code> + <code>git commit</code> → <b>3 blob</b> (nội dung file) + <b>1 tree</b> (cấu trúc thư mục) + <b>1 commit</b> (con trỏ tới tree, tác giả, email, message, con trỏ tới commit cha). Số cha: 0 = commit đầu tiên · 1 = commit thường · nhiều = merge commit. File không đổi không được lưu lại mà chỉ link tới bản trước.</p>""" + src("week01.pdf tr.7–14, 20, 81–84")

P["bang"] = """<h3 id="k1-config">Cấu hình</h3>""" + table(["Cấp", "Phạm vi", "File"], [
    ["System", "mọi user", "[path]/etc/gitconfig"], ["Global (<code>--global</code>)", "user hiện tại, mọi project", "~/.gitconfig hoặc ~/.config/git/config"],
    ["Local (không có --global)", "một repo", ".git/config"]]) + note("Ưu tiên: <b>Local &gt; Global &gt; System</b>. Muốn dùng tên/email khác cho một project: chạy lệnh <b>không</b> có <code>--global</code> trong repo đó.") + pre("""
git config --global user.name "Name"
git config --global user.email "email@example.com"
""", "bash") + src("week01.pdf tr.38–39") + """
<h3 id="k1-cmd">Lệnh cơ bản</h3>""" + table(["Lệnh", "Tác dụng"], [
    [c("git init"), "tạo thư mục con <code>.git</code> (khung repo); chưa track file nào"],
    [c("git clone <url>"), "tạo thư mục → <code>git init</code> → thêm remote <b>origin</b> → <code>git fetch</code> → checkout commit mới nhất. Chép <b>toàn bộ lịch sử</b>"],
    [c("git status") + " / " + c("git status -s"), "trạng thái đầy đủ / rút gọn hai cột"],
    [c("git add <file>"), "bắt đầu track file mới, hoặc stage file đã sửa"],
    [c("git diff"), "thay đổi <b>chưa stage</b> (working tree so với staging)"],
    [c("git diff --staged"), "thay đổi <b>đã stage</b> (staging so với commit cuối)"],
    [c("git commit -m \"msg\""), "commit snapshot đã stage, không mở editor"],
    [c("git commit -a -m \"msg\""), "tự stage mọi file <b>đã track</b> và đã sửa rồi commit (file untracked không được thêm)"],
    [c("git commit --amend"), "<b>thay thế</b> commit trước bằng commit mới (sửa message, thêm file quên)"],
    [c("git rm <file>"), "xoá khỏi working dir <b>và</b> stage việc xoá"],
    [c("git rm --cached <file>"), "ngừng track nhưng <b>giữ file</b> trên đĩa"],
    [c("git mv old new"), "= đổi tên + <code>git rm old</code> + <code>git add new</code>"],
    [c("git log --oneline / --graph / -p / --stat"), "lịch sử mới nhất trước; một dòng / đồ thị nhánh / kèm diff / thống kê"],
    [c("git reset HEAD <file>") + " · " + c("git restore --staged <file>"), "bỏ stage, giữ thay đổi trong working dir"],
    [c("git restore <file>"), "đưa file về bản commit cuối — <b>mất</b> thay đổi chưa commit"],
    [c("git remote -v"), "liệt kê remote kèm URL fetch/push"],
    [c("git remote add <name> <url>"), "thêm remote"], [c("git remote show <name>") + " · " + c("rename") + " · " + c("remove"), "xem chi tiết · đổi tên · xoá remote"],
    [c("git fetch <remote>"), "tải dữ liệu mới, cập nhật remote-tracking branch, <b>không merge</b>"],
    [c("git pull"), "= fetch + merge"],
    [c("git push <remote> <branch>"), "đẩy commit; <b>bị từ chối</b> nếu remote có commit bạn chưa có"],
    [c("git tag v1.0") + " · " + c("git tag -a v1.0 -m \"msg\""), "tag lightweight (chỉ con trỏ) · tag annotated (lưu người tag, email, ngày, message)"],
    [c("git push <remote> <tag>"), "tag <b>không</b> được push mặc định, phải push riêng"],
]) + src("week01.pdf tr.43–76; Pro Git tr.53–56, 59") + """
<h3 id="k1-short">Đọc <code>git status -s</code></h3>""" + pre("""
 M README
MM Rakefile
A  lib/git.rb
M  lib/simplegit.rb
?? LICENSE.txt
""", "text") + "<p>Cột <b>trái</b> = staging area, cột <b>phải</b> = working tree. <code>??</code> untracked · <code>A</code> mới được stage · <code>␣M</code> sửa chưa stage · <code>M␣</code> sửa đã stage · <code>MM</code> đã stage rồi lại sửa tiếp.</p>" + src("week01.pdf tr.51; Pro Git tr.37–38") + """
<h3 id="k1-ignore">.gitignore</h3>""" + pre("""
# ignore all .a files
*.a
# but do track lib.a, even though you're ignoring .a files above
!lib.a
# only ignore the TODO file in the current directory, not subdir/TODO
/TODO
# ignore all files in any directory named build
build/
# ignore doc/notes.txt, but not doc/server/arch.txt
doc/*.txt
# ignore all .pdf files in the doc/ directory and any of its subdirectories
doc/**/*.pdf
""", "bash") + ul(["Dòng trống hoặc bắt đầu bằng <code>#</code> bị bỏ qua.", "Glob áp dụng <b>đệ quy</b> toàn cây; <code>/</code> ở đầu = chỉ thư mục hiện tại; <code>/</code> ở cuối = thư mục; <code>!</code> = phủ định; <code>**</code> = thư mục lồng nhau.",
    "File <b>đã track</b> rồi thì thêm vào .gitignore không làm Git bỏ track → dùng <code>git rm --cached</code>."]) + src("week01.pdf tr.52; Pro Git tr.38–39, 44–45")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["CVCS vs DVCS", "CVCS: một server giữ mọi phiên bản, điểm lỗi duy nhất, SVN/CVS sửa offline được nhưng <b>không commit offline</b>. DVCS: clone = backup đầy đủ, commit offline rồi push sau."],
    ["Snapshot vs diff", "Đa số VCS lưu thay đổi theo file (diff); Git lưu chuỗi snapshot, file không đổi chỉ link tới bản cũ."],
    [c("git diff") + " vs " + c("git diff --staged"), "chưa stage vs đã stage. Stage hết rồi thì <code>git diff</code> trống."],
    [c("git rm") + " vs " + c("git rm --cached"), "xoá cả file trên đĩa vs chỉ ngừng track, giữ file."],
    [c("git fetch") + " vs " + c("git pull"), "fetch chỉ tải về, an toàn, không đụng working dir; pull = fetch + merge."],
    [c("git commit -a") + " vs " + c("git add") + " + commit", "-a chỉ tự stage file <b>đã track</b>; file mới vẫn phải <code>git add</code>."],
    [c("git restore <f>") + " vs " + c("git restore --staged <f>"), "bỏ thay đổi trong working dir (mất) vs bỏ stage (thay đổi còn)."],
    ["Tracked vs untracked", "Tracked: có trong snapshot cuối hoặc mới stage (unmodified/modified/staged). Untracked: mọi file còn lại."],
    ["Tag lightweight vs annotated", "lightweight: chỉ con trỏ; annotated: thêm người tag, email, ngày, message — khuyên dùng cho release. Tag không di chuyển như branch."],
    ["--global vs local config", "global: mọi project của user; không có --global: chỉ repo hiện tại và ghi đè global."],
]) + src("week01.pdf tr.9–12, 24, 38–39, 47, 53–76")

P["bay"] = trap("Bẫy 1 — <code>commit -a</code> với file mới", "Tạo <code>new.py</code> rồi <code>git commit -a -m \"x\"</code> → <code>new.py</code> <b>không</b> được commit (untracked).<br><b>Đổi một chỗ:</b> chạy <code>git add new.py</code> trước → được commit.", "k1-trap-a") + \
    trap("Bẫy 2 — <code>git diff</code> trống", "Sửa file rồi <code>git add</code> hết → <code>git diff</code> không in gì; thay đổi chỉ hiện ở <code>git diff --staged</code>.<br><b>Đổi một chỗ:</b> sửa tiếp sau khi add → file thành <code>MM</code>, <code>git diff</code> hiện phần sửa sau.", "k1-trap-diff") + \
    trap("Bẫy 3 — .gitignore không “untrack”", "File đã commit rồi mới thêm vào .gitignore → Git vẫn theo dõi. Phải <code>git rm --cached file</code> rồi commit.", "k1-trap-ignore") + \
    trap("Bẫy 4 — <code>/TODO</code> vs <code>TODO</code>", "<code>/TODO</code> chỉ bỏ qua TODO ở thư mục gốc, <code>subdir/TODO</code> vẫn track. <code>doc/*.txt</code> bỏ <code>doc/notes.txt</code> nhưng không bỏ <code>doc/server/arch.txt</code> (muốn đệ quy: <code>doc/**/*.txt</code>).", "k1-trap-glob") + \
    trap("Bẫy 5 — amend thay chứ không thêm", "<code>git commit -m 'Initial'</code> → <code>git add forgotten</code> → <code>git commit --amend</code> → lịch sử chỉ có <b>1 commit</b> chứa cả file quên. Chỉ amend commit chưa push.", "k1-trap-amend") + \
    trap("Bẫy 6 — push không kèm tag, push bị từ chối", "<code>git push origin main</code> không đẩy tag; cần <code>git push origin v1.0</code>. Người khác đã push trước → push của bạn bị từ chối → fetch/pull rồi push lại.", "k1-trap-push") + \
    trap("Bẫy 7 — <code>git restore</code> nguy hiểm", "Đưa file về bản commit cuối: thay đổi chưa commit <b>mất vĩnh viễn</b>. Muốn bỏ stage mà giữ thay đổi: <code>git restore --staged</code> / <code>git reset HEAD</code>.")

P["checklist"] = [
    "VCS cục bộ, tập trung (CVCS) và phân tán (DVCS): ưu/nhược, điểm lỗi duy nhất; Git lưu snapshot chứ không lưu diff; toàn vẹn dữ liệu bằng SHA-1",
    "3 trạng thái (modified, staged, committed) và 3 vùng (working dir, staging area, .git)",
    "Tracked và untracked; git config --global user.name/email; init, clone, status, add, commit -m, commit -a (chỉ áp dụng cho file đã track)",
    "git diff (working so với staging) và git diff --staged (staging so với commit cuối)",
    "git mv, git rm, git rm --cached, .gitignore (glob, /, !)",
    "git log (--oneline, --graph), hoàn tác: commit --amend, restore, restore --staged",
    "Remote: remote add/-v, push, fetch và pull (pull = fetch + merge)",
    "＋ 3 cấp git config (system/global/local, local ghi đè global)",
    "＋ git clone làm 5 việc (thư mục, init, remote origin, fetch, checkout)",
    "＋ git status -s: cột trái = staging, cột phải = working tree",
    "＋ Tag lightweight vs annotated; tag không tự push",
    "＋ Commit object: tree + blob; 0/1/nhiều cha",
]

P["quick"] = [
    QQ("Bạn sửa <code>a.py</code> (đã track) và tạo mới <code>b.py</code>, rồi chạy <code>git commit -a -m \"x\"</code>. Commit chứa gì?", ["Cả a.py và b.py", "Chỉ thay đổi của a.py", "Chỉ b.py", "Không có gì"], "b", "-a chỉ tự stage file đã track."),
    QQ("Đã <code>git add</code> toàn bộ thay đổi. Lệnh nào còn hiện ra thay đổi đó?", ["git diff", "git diff --staged", "git log", "git remote -v"], "b", "git diff chỉ hiện phần chưa stage."),
    QQ("<code>git fetch origin</code> làm gì?", ["Tải về và merge vào nhánh hiện tại", "Tải dữ liệu mới, cập nhật origin/*, không merge", "Đẩy commit lên origin", "Xoá remote origin"], "b", "fetch chỉ tải; pull = fetch + merge."),
]

P["docthem"] = ul([
    "Pro Git tr.53: <code>--amend</code> thực chất tạo commit mới thay thế commit cũ — chỉ dùng cho commit chưa push.",
    "Pro Git tr.54, 56: <code>git checkout -- &lt;file&gt;</code> (cách cũ) và <code>git restore &lt;file&gt;</code> đều nguy hiểm vì ghi đè file bằng bản đã commit.",
    "Pro Git tr.38: các ví dụ <code>*.[oa]</code>, <code>*~</code>; GitHub có sẵn kho mẫu .gitignore tại github.com/github/gitignore.",
    "Pro Git tr.45: <code>git rm log/\\*.log</code> — dấu <code>\\</code> để Git (không phải shell) tự mở rộng glob.",
])

BLOCK = dict(id="K1", mon="TTNT", title="Git cơ bản", src="week01.pdf · Pro Git ch.1–2", page=P)

QUESTIONS = [
    Q("K1-01", "single", "In a clean repository on <code>master</code>, you run the commands below. How does <code>git status</code> report README?",
      ["Under \"Changes to be committed: new file\"", "Under \"Untracked files\"", "Under \"Changes not staged for commit: modified\"", "It does not appear because it is ignored by default"], "b",
      "File mới chưa từng <code>git add</code> là untracked. Sau <code>git add README</code> nó mới vào “Changes to be committed”.", "week01.pdf tr.47–49", "k1-cmd",
      code="echo 'My Project' > README\ngit status", lang="bash"),
    Q("K1-02", "multi", "Which statements about <code>git commit -a -m \"Update notes.txt\"</code> are correct?",
      ["It automatically stages every tracked file that has been modified.", "A brand-new untracked file is not included in the commit.", "It also adds every new file in the working directory.", "It uploads the commit to origin."], "ab",
      "commit -a bỏ qua bước git add <b>chỉ cho file đã track</b>. Commit luôn là thao tác local; push mới đưa lên remote.", "week01.pdf tr.56; ex1.docx Part B.6", "k1-trap-a"),
    Q("K1-03", "multi", "Given this short status output, which statements are correct?",
      ["README is modified in the working tree but not staged.", "Rakefile has both staged and unstaged changes.", "LICENSE.txt is untracked.", "lib/simplegit.rb is modified but not yet staged."], "abc",
      "Cột trái = staging, cột phải = working tree. <code>M␣</code> ở lib/simplegit.rb nghĩa là đã sửa <b>và đã stage</b>.", "week01.pdf tr.51; Pro Git tr.37–38", "k1-short",
      code=" M README\nMM Rakefile\nA  lib/git.rb\nM  lib/simplegit.rb\n?? LICENSE.txt", lang="text"),
    Q("K1-04", "single", "You edit <code>notes.txt</code> (already tracked) and then run the commands below. What does the last command print?",
      ["The changes to notes.txt", "Nothing, because all changes are staged; use <code>git diff --staged</code> to see them", "The full history of notes.txt", "An error, because notes.txt is staged"], "b",
      "<code>git diff</code> so working tree với staging area → không còn gì khác biệt. <code>git diff --staged</code> mới so staging với commit cuối.", "week01.pdf tr.53; Pro Git tr.40", "k1-trap-diff",
      code="git add notes.txt\ngit diff", lang="bash"),
    Q("K1-05", "multi", "With this <code>.gitignore</code> at the repository root, which files are ignored?",
      ["<code>src/foo.a</code>", "<code>lib.a</code>", "<code>subdir/TODO</code>", "<code>doc/notes.txt</code>"], "ad",
      "<code>*.a</code> áp dụng đệ quy nên src/foo.a bị bỏ qua; <code>!lib.a</code> phủ định nên lib.a vẫn track; <code>/TODO</code> chỉ áp dụng ở gốc; <code>doc/*.txt</code> khớp doc/notes.txt.", "week01.pdf tr.52; Pro Git tr.38–39", "k1-trap-glob",
      code="*.a\n!lib.a\n/TODO\nbuild/\ndoc/*.txt", lang="bash"),
    Q("K1-06", "single", "You accidentally committed <code>config.env</code>. You run the command below and commit. What happens to the file?",
      ["Git stops tracking it, but the file stays on your disk.", "It is deleted from the disk and from Git.", "It is moved into .gitignore automatically.", "Nothing; --cached only affects the remote."], "a",
      "<code>git rm --cached</code> chỉ gỡ khỏi staging/tracking, giữ file local. Nên thêm nó vào .gitignore để không bị add lại.", "week01.pdf tr.57; Pro Git tr.44–45", "k1-trap-ignore",
      code="git rm --cached config.env", lang="bash"),
    Q("K1-07", "single", "<code>git mv draft.md README2.md</code> is a shortcut for which sequence?",
      ["<code>mv draft.md README2.md; git rm draft.md; git add README2.md</code>", "<code>cp draft.md README2.md; git add draft.md</code>", "<code>git rm --cached draft.md</code>", "<code>git commit -a</code>"], "a",
      "Slide: git mv = đổi tên + git rm tên cũ + git add tên mới; Git nhận diện rename bằng độ tương đồng.", "week01.pdf tr.58", "k1-cmd"),
    Q("K1-08", "multi", "A teammate edited README.md directly on GitHub. Which statements are correct?",
      ["<code>git fetch origin</code> downloads the new commit and moves origin/main, without merging it.", "<code>git pull</code> fetches and then merges it into your current branch.",
       "<code>git fetch</code> immediately changes README.md in your working directory.", "<code>git push</code> succeeds even though the remote has a commit you don't have."], "ab",
      "fetch chỉ tải và cập nhật remote-tracking branch; pull = fetch + merge. Push thất bại nếu remote có commit bạn chưa có.", "week01.pdf tr.69–70; week02.pdf tr.42–44; ex1.docx Part C", "k1-cmd"),
    Q("K1-09", "single", "Which email will commits made inside <code>project</code> use?",
      ["<code>a@x.com</code>, because --global always wins", "<code>b@y.com</code>, because the repository (local) level overrides global", "Both emails", "The system-level email"], "b",
      "Thứ tự ưu tiên: Local &gt; Global &gt; System.", "week01.pdf tr.38–39", "k1-config",
      code='git config --global user.email "a@x.com"\ncd project\ngit config user.email "b@y.com"', lang="bash"),
    Q("K1-10", "single", "After these commands, what does the history contain?",
      ["Two commits: 'Initial commit' and a second one with forgotten_file", "One commit, which now also includes forgotten_file", "One commit without forgotten_file; it stays staged", "An error: you cannot amend after adding files"], "b",
      "<code>--amend</code> thay thế commit trước bằng commit mới chứa nội dung staging hiện tại → chỉ còn 1 commit.", "week01.pdf tr.63; Pro Git tr.53", "k1-trap-amend",
      code="git commit -m 'Initial commit'\ngit add forgotten_file\ngit commit --amend", lang="bash"),
    Q("K1-11", "multi", "Which statements about these commands are correct?",
      ["The annotated tag stores the tagger name, email, date and message.", "<code>git push origin main</code> also uploads the tag v1.4.",
       "<code>git push origin v1.4</code> shares the tag with the remote.", "The tag moves forward automatically with new commits, like a branch."], "ac",
      "Tag không được push mặc định, phải push tên tag. Tag đánh dấu một điểm cố định, không di chuyển như branch.", "week01.pdf tr.73–76", "k1-trap-push",
      code='git tag -a v1.4 -m "my version 1.4"\ngit push origin main', lang="bash"),
    Q("K1-12", "multi", "Which statements about <code>git clone &lt;url&gt;</code> are correct?",
      ["It copies the entire project history, not just the latest snapshot.", "It adds a remote named origin by default.", "It downloads only the latest snapshot to save space.", "Every clone is effectively a full backup of the project."], "abd",
      "clone: tạo thư mục, git init, thêm remote origin, git fetch, checkout commit mới nhất. Vì chép toàn bộ lịch sử nên mỗi clone là một bản backup.", "week01.pdf tr.12, 45–46", "k1-cmd"),
    Q("K1-13", "single", "In a new repository you run the commands below. Which objects does Git store for this commit?",
      ["3 blobs + 1 tree + 1 commit", "3 diffs + 1 commit", "1 blob + 3 trees + 1 commit", "3 commits, one per file"], "a",
      "Mỗi nội dung file là một blob, cấu trúc thư mục là một tree, cộng một commit object trỏ tới tree.", "week01.pdf tr.81–83", "k1-objects",
      code="git add README test.rb LICENSE\ngit commit -m 'Initial commit'", lang="bash"),
]
