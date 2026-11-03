from h import *


def node(x, y, label, cls="node"):
    return '<circle cx="%d" cy="%d" r="15" class="%s"/><text x="%d" y="%d" text-anchor="middle" font-size="12" class="mono">%s</text>' % (x, y, cls, x, y + 4, label)


def arrow(x1, y1, x2, y2):
    # child -> parent arrow (Git style)
    return '<line x1="%d" y1="%d" x2="%d" y2="%d" class="ln"/>' % (x1, y1, x2, y2)


def lab(x, y, t, cls="acc"):
    return '<text x="%d" y="%d" font-size="12" class="%s" font-weight="700">%s</text>' % (x, y, cls, t)


g1 = arrow(55, 60, 85, 60) + arrow(115, 60, 145, 60) + arrow(175, 60, 205, 60) + arrow(175, 60, 205, 25) + arrow(235, 25, 265, 25)
g1 += node(40, 60, "C0") + node(100, 60, "C1") + node(160, 60, "C2") + node(220, 60, "C5") + node(220, 25, "C3") + node(280, 25, "C4")
g1 += lab(200, 92, "main") + lab(268, 52, "experiment")
g1 = '<g transform="translate(0,20)">' + '<text x="10" y="-2" font-weight="700" font-size="13">① Hai nhánh đã rẽ (diverged)</text>' + g1 + '</g>'

g2 = arrow(55, 60, 85, 60) + arrow(115, 60, 145, 60) + arrow(175, 60, 205, 60) + arrow(175, 60, 205, 25) + arrow(235, 25, 265, 25) + arrow(235, 60, 325, 60) + arrow(295, 25, 328, 50)
g2 += node(40, 60, "C0") + node(100, 60, "C1") + node(160, 60, "C2", "nodea") + node(220, 60, "C5") + node(220, 25, "C3") + node(280, 25, "C4") + node(340, 60, "C6", "nodea")
g2 += lab(325, 92, "main") + '<text x="372" y="56" font-size="11.5" class="muted">merge commit, 2 cha (C5, C4)</text><text x="372" y="72" font-size="11.5" class="muted">C2 = tổ tiên chung</text>'
g2 = '<g transform="translate(360,20)">' + '<text x="10" y="-2" font-weight="700" font-size="13">② git checkout main; git merge experiment</text>' + g2 + '</g>'

g3 = arrow(55, 60, 85, 60) + arrow(115, 60, 145, 60) + arrow(175, 60, 205, 60) + arrow(235, 60, 265, 60) + arrow(295, 60, 325, 60)
g3 += node(40, 60, "C0") + node(100, 60, "C1") + node(160, 60, "C2") + node(220, 60, "C5") + node(280, 60, "C3'", "nodea") + node(340, 60, "C4'", "nodea")
g3 += lab(205, 92, "main") + lab(318, 92, "experiment")
g3 += '<text x="372" y="56" font-size="11.5" class="muted">commit được phát lại = commit MỚI</text><text x="372" y="72" font-size="11.5" class="muted">rồi: git checkout main; git merge experiment</text><text x="372" y="88" font-size="11.5" class="muted">→ fast-forward main tới C4\'</text>'
g3 = '<g transform="translate(0,150)">' + '<text x="10" y="-2" font-weight="700" font-size="13">③ git checkout experiment; git rebase main  (thay cho ②)</text>' + g3 + '</g>'

SVG = '<svg viewBox="0 0 720 260" width="720" role="img" aria-label="So sánh merge và rebase">' + g1 + g2 + g3 + '</svg>'

P = {}
P["y"] = """<p><b>Branch</b> chỉ là một <b>con trỏ di động</b> tới một commit; <b>HEAD</b> trỏ tới branch đang đứng. Tạo nhánh rẻ và gần như tức thì, nên Git khuyến khích rẽ nhánh và gộp thường xuyên. Có hai cách gộp công việc: <b>merge</b> (giữ đúng dòng thời gian song song) và <b>rebase</b> (phát lại commit lên base mới cho lịch sử thẳng).</p>""" + src("week01.pdf tr.78–85; week02.pdf tr.4–15, 58–62")

P["mohinh"] = diagram(SVG, "Merge tạo merge commit; rebase phát lại commit rồi fast-forward (week02.pdf tr.14–15, 58–62)") + """
<h3 id="k2-ff">Fast-forward</h3><p>Nhánh được merge <b>đi thẳng trước</b> commit hiện tại (không có công việc rẽ nhánh) → Git chỉ <b>dời con trỏ lên</b>, không tạo commit mới; output in <code>Fast-forward</code>. Ví dụ hotfix: main ở C2, hotfix ở C4 (con của C2) → <code>git checkout main; git merge hotfix</code> → main nhảy tới C4, sau đó <code>git branch -d hotfix</code>.</p>
<h3 id="k2-switch">Đổi nhánh thì working dir đổi theo</h3><p><code>git checkout testing</code> dời HEAD sang testing <b>và</b> đưa file trong working dir về snapshot của testing. Commit tiếp theo làm nhánh HEAD đang trỏ tiến lên. Nếu không đổi nhánh sạch được (thay đổi chưa commit bị xung đột), Git không cho đổi.</p>""" + src("week02.pdf tr.5–9; Pro Git tr.74, 78–80")

P["bang"] = """<h3 id="k2-cmd">Tạo, đổi, quản lý nhánh</h3>""" + table(["Lệnh", "Tác dụng"], [
    [c("git branch <name>"), "tạo con trỏ mới tại commit hiện tại — <b>không</b> tự chuyển sang"],
    [c("git checkout <name>") + " · " + c("git switch <name>"), "chuyển nhánh (HEAD + working dir)"],
    [c("git checkout -b <name>") + " · " + c("git switch -c <name>"), "tạo và chuyển trong một lệnh"],
    [c("git switch -"), "quay về nhánh trước đó"],
    [c("git branch"), "liệt kê nhánh local; <code>*</code> = nhánh đang checkout"],
    [c("git branch -v"), "commit mới nhất của mỗi nhánh"],
    [c("git branch --merged") + " / " + c("--no-merged"), "nhánh đã / chưa được merge vào <b>nhánh hiện tại</b>"],
    [c("git branch -d <b>"), "xoá nhánh đã merge (an toàn); chưa merge → lỗi “not fully merged”"],
    [c("git branch -D <b>"), "xoá cưỡng bức, mất công việc chưa merge"],
    [c("git branch --move old new"), "đổi tên local (lịch sử giữ nguyên)"],
    [c("git push --set-upstream origin new"), "đẩy tên mới lên remote"],
    [c("git push origin --delete old"), "xoá tên cũ trên remote"],
    [c("git log --oneline --decorate --graph --all"), "xem con trỏ nhánh, HEAD và đồ thị mọi nhánh"],
]) + src("week02.pdf tr.4–35") + """
<h3 id="k2-conflict">Merge conflict</h3>""" + pre("""
$ git merge iss53
Auto-merging index.html
CONFLICT (content): Merge conflict in index.html
Automatic merge failed; fix conflicts and then commit the result.
""", "text") + pre("""
<<<<<<< HEAD:index.html
<div id="footer">contact : email.support@github.com</div>
=======
<div id="footer">
 please contact us at support@github.com
</div>
>>>>>>> iss53:index.html
""", "text") + ul(["Phía trên <code>=======</code> = bản ở <b>HEAD</b> (nhánh đang đứng khi chạy merge); phía dưới = bản của nhánh được merge (iss53).",
    "Git <b>chưa</b> tạo merge commit; <code>git status</code> báo <i>Unmerged paths … both modified</i>.",
    "Sửa file, <b>xoá hết</b> các dòng <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code> <code>=======</code> <code>&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code> → <code>git add index.html</code> (đánh dấu đã giải quyết) → <code>git commit</code>."]) + src("Pro Git tr.83–84 (slide week02 tr.14 chỉ nêu 3-way merge)") + """
<h3 id="k2-remote">Remote branch &amp; tracking</h3>""" + table(["Lệnh / khái niệm", "Ý nghĩa"], [
    [c("origin/master"), "remote-tracking branch: bookmark “remote ở đâu lần sync trước”; không tự di chuyển, chỉ đổi khi fetch/push"],
    [c("git ls-remote <remote>") + " · " + c("git remote show <remote>"), "liệt kê tham chiếu trên remote"],
    [c("git push origin serverfix"), "đẩy nhánh local serverfix lên serverfix của remote"],
    [c("git merge origin/serverfix"), "gộp nhánh vừa fetch vào nhánh hiện tại"],
    [c("git checkout -b serverfix origin/serverfix"), "tạo nhánh local để sửa, theo dõi origin/serverfix"],
    [c("git checkout --track origin/serverfix"), "dạng rút gọn; <code>git checkout serverfix</code> cũng được nếu tên không trùng"],
    [c("git checkout -b sf origin/serverfix"), "nhánh local tên khác (sf) vẫn track origin/serverfix"],
    [c("git branch -u origin/serverfix"), "đặt/đổi upstream (= <code>--set-upstream-to</code>)"],
    [c("git branch -vv"), "upstream của mỗi nhánh + ahead/behind (chỉ mới bằng lần fetch cuối; cần số mới: <code>git fetch --all; git branch -vv</code>)"],
    [c("git push origin --delete serverfix"), "xoá nhánh trên server"],
]) + src("week02.pdf tr.38–56; Pro Git tr.99–100") + """
<h3 id="k2-rebase">Rebase</h3>""" + table(["Lệnh", "Tác dụng"], [
    [c("git checkout experiment; git rebase master"), "tìm tổ tiên chung → lấy diff từng commit của experiment → reset về master → áp lại từng patch"],
    [c("git checkout master; git merge experiment"), "sau rebase lịch sử thẳng nên đây là fast-forward"],
    [c("git rebase master server"), "rebase server lên master mà không cần checkout trước"],
    [c("git rebase --onto master server client"), "lấy các commit của client kể từ khi tách khỏi server, phát lại lên master (bỏ qua phần của server)"],
]) + note("Quy tắc vàng: rebase thoải mái commit <b>local chưa push</b> để dọn lịch sử; <b>không bao giờ rebase thứ đã push công khai</b>.", "warn") + src("week02.pdf tr.58–67; Pro Git tr.104, 106")

P["sosanh"] = table(["Cặp", "Phân biệt"], [
    ["Merge vs rebase", "Snapshot cuối <b>giống nhau</b>. Merge: 3-way merge (2 đầu nhánh + tổ tiên chung), tạo merge commit 2 cha, giữ timeline song song. Rebase: phát lại patch thành commit mới, lịch sử thẳng."],
    ["Fast-forward vs 3-way merge", "FF: không rẽ nhánh → dời con trỏ, không có commit mới. 3-way: hai nhánh đã rẽ → tạo merge commit."],
    [c("git branch x") + " vs " + c("git checkout -b x"), "chỉ tạo vs tạo + chuyển."],
    [c("-d") + " vs " + c("-D"), "xoá an toàn (đã merge) vs xoá cưỡng bức."],
    [c("--merged") + " vs " + c("--no-merged"), "đã gộp (thường xoá được) vs còn công việc chưa gộp — so với nhánh <b>hiện tại</b>."],
    ["Nhánh local vs remote-tracking", "local: bạn di chuyển bằng commit. origin/x: Git di chuyển khi fetch/push; không sửa tay được."],
    [c("git fetch") + " vs " + c("git pull"), "fetch không đụng working dir; pull = fetch + merge (hoặc rebase)."],
    ["Đổi tên nhánh vs đổi tên nhánh mặc định", "Nhánh thường: branch --move + push -u + push --delete. master/main: có thể làm hỏng CI/CD, script build, tích hợp — phải hỏi cả nhóm."],
    ["HEAD vs branch", "branch trỏ tới commit; HEAD trỏ tới branch đang đứng (nhánh sẽ tiến lên khi commit)."],
]) + src("week02.pdf tr.14, 22–27, 39–44, 58–62")

P["bay"] = trap("Bẫy 1 — tạo nhánh không chuyển nhánh", "<code>git branch testing</code> rồi commit → <b>master</b> tiến lên (HEAD vẫn ở master), testing đứng yên.<br><b>Đổi một chỗ:</b> dùng <code>git checkout -b testing</code> → testing tiến lên.", "k2-trap-branch") + \
    trap("Bẫy 2 — đổi nhánh làm “mất” nội dung file", "Ở week2 thêm dòng vào week2.md, commit, rồi <code>git switch master</code> → week2.md trở về nội dung trên master (dòng mới không thấy). Không mất: nó nằm ở commit của nhánh week2.", "k2-trap-switch") + \
    trap("Bẫy 3 — chiều của merge", "Muốn đưa hotfix vào main: đứng ở <b>main</b> rồi <code>git merge hotfix</code>. Đứng ở hotfix mà merge main thì hotfix mới là nhánh thay đổi.", "k2-trap-dir") + \
    trap("Bẫy 4 — conflict: HEAD ở trên", "Khối giữa <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> và <code>=======</code> là bản của nhánh <b>đang đứng</b>. Sau khi sửa phải <code>git add</code> rồi <code>git commit</code> — Git không tự tạo merge commit khi có conflict.", "k2-trap-conflict") + \
    trap("Bẫy 5 — rebase tạo commit mới", "Sau <code>git rebase master</code>, C3, C4 trở thành C3', C4' (hash mới). Ai đã dựa trên C3, C4 cũ sẽ bị rối → không rebase commit đã public.<br><b>Đổi một chỗ:</b> sau rebase, merge từ master là <b>fast-forward</b>; nếu không rebase thì merge là 3-way.", "k2-trap-rebase") + \
    trap("Bẫy 6 — ahead/behind không tự cập nhật", "<code>git branch -vv</code> chỉ đúng tới lần fetch cuối. <code>ahead 3, behind 1</code> = 3 commit local chưa push, 1 commit trên server chưa merge.", "k2-trap-vv") + \
    trap("Bẫy 7 — đổi tên xong nhánh cũ vẫn còn trên remote", "<code>git branch --move bad good</code> + <code>git push --set-upstream origin good</code> → remote có <b>cả hai</b> tên; phải <code>git push origin --delete bad</code>.", "k2-trap-rename")

P["checklist"] = [
    "Branch là con trỏ tới commit; HEAD trỏ tới branch hiện tại; branch, checkout, switch, switch -c, checkout -b, switch -",
    "Khi switch nhánh, working dir thay đổi theo snapshot của nhánh đó",
    "Merge fast-forward và 3-way merge (tạo merge commit, dùng common ancestor); conflict: dấu <<<<<<< ======= >>>>>>>, sửa xong thì add rồi commit",
    "Quản lý nhánh: branch -v, --merged, --no-merged, -d và -D, đổi tên branch -m + push -u origin mới + xóa nhánh cũ trên remote",
    "Remote branch: origin/master, tracking branch, branch -vv (ahead/behind), push -u, push origin --delete",
    "Rebase: phát lại commit lên base mới, lịch sử thẳng; rebase xong thì merge fast-forward; quy tắc không rebase commit đã public",
    "Pull request, quy trình feature branch, hotfix",
    "＋ rebase --onto master server client; git rebase <base> <topic>",
    "＋ checkout --track, checkout -b sf origin/serverfix, branch -u (--set-upstream-to)",
    "＋ Đổi tên nhánh mặc định (master→main) có thể làm hỏng CI/CD, script — phải bàn với nhóm",
]

P["quick"] = [
    QQ("Đang ở main, chạy <code>git branch feat</code> rồi <code>git commit -a -m x</code>. Nhánh nào tiến lên?", ["feat", "main", "cả hai", "không nhánh nào"], "b", "git branch không chuyển nhánh; HEAD vẫn trỏ main."),
    QQ("main ở C2, hotfix ở C4 (C4 là hậu duệ trực tiếp của C2). <code>git checkout main; git merge hotfix</code> sẽ:", ["Tạo merge commit 2 cha", "Fast-forward: dời main tới C4", "Báo conflict", "Rebase hotfix"], "b", "Không có công việc rẽ nhánh → fast-forward."),
    QQ("Quy tắc an toàn khi dùng rebase là gì?", ["Chỉ rebase nhánh main", "Không rebase commit đã push công khai", "Luôn rebase trước khi fetch", "Rebase thay cho commit"], "b", "Rebase local chưa push; không rebase thứ đã public."),
]

P["docthem"] = ul([
    "Pro Git tr.74: <code>git log</code> mặc định chỉ hiện lịch sử của nhánh đang checkout; thêm <code>--all</code> để xem mọi nhánh.",
    "Pro Git tr.109: <code>git pull --rebase</code> thay cho pull thường (fetch + rebase).",
    "Pro Git tr.106 (The Perils of Rebasing): rebase bỏ commit cũ và tạo commit mới giống nội dung nhưng khác hash; người khác đã dựa trên commit cũ sẽ phải merge lại và lịch sử bị lặp.",
])

BLOCK = dict(id="K2", mon="TTNT", title="Branch, merge, rebase", src="week02.pdf · Pro Git ch.3", page=P)

VV = """$ git branch -vv
  iss53     7e424c3 [origin/iss53: ahead 2] Add forgotten brackets
  master    1ae2a45 [origin/master] Deploy index fix
* serverfix f8674d9 [teamone/server-fix-good: ahead 3, behind 1] This should do it
  testing   5ea463a Try something new"""

CONF = """<<<<<<< HEAD:index.html
<div id="footer">contact : email.support@github.com</div>
=======
<div id="footer">please contact us at support@github.com</div>
>>>>>>> iss53:index.html"""

QUESTIONS = [
    Q("K2-01", "single", "You are on <code>master</code> and run the commands below. Which branch pointer moves to the new commit?",
      ["testing", "master", "Both master and testing", "Neither; the commit is detached"], "b",
      "<code>git branch</code> chỉ tạo con trỏ, không chuyển HEAD. HEAD vẫn trỏ master nên master tiến lên.", "week02.pdf tr.4–7", "k2-trap-branch",
      code="git branch testing\nvim test.rb\ngit commit -a -m 'Make a change'", lang="bash"),
    Q("K2-02", "multi", "Which commands create a branch named <code>iss53</code> and switch to it?",
      ["<code>git branch iss53</code> followed by <code>git checkout iss53</code>", "<code>git switch -c iss53</code>", "<code>git switch iss53</code> (when iss53 does not exist yet)", "<code>git branch -d iss53</code>"], "ab",
      "<code>checkout -b</code> / <code>switch -c</code> tạo và chuyển trong một lệnh. <code>switch</code> không có -c chỉ chuyển sang nhánh đã tồn tại.", "week02.pdf tr.10–11", "k2-cmd"),
    Q("K2-03", "single", "<code>master</code> points to C2 and <code>hotfix</code> points to C4, a direct descendant of C2. What does Git do?",
      ["Moves master forward to C4 without creating a new commit (fast-forward).", "Creates a merge commit with two parents.", "Reports a conflict because history diverged.", "Rewrites C4 on top of master."], "a",
      "Commit được merge có thể đi tới bằng cách theo lịch sử của commit hiện tại → không có công việc rẽ nhánh → fast-forward.", "week02.pdf tr.12–13; Pro Git tr.79", "k2-ff",
      code="git checkout master\ngit merge hotfix", lang="bash"),
    Q("K2-04", "multi", "<code>master</code> and <code>iss53</code> have diverged. You run <code>git checkout master; git merge iss53</code> with no conflicts. Which statements are correct?",
      ["Git uses the two branch tips and their common ancestor.", "The result is a new merge commit with two parents.", "It is a fast-forward.", "Git rewrites the commits of iss53."], "ab",
      "Three-way merge khi hai nhánh đã rẽ: hai đầu nhánh + tổ tiên chung → merge commit có 2 cha. Merge không viết lại commit (rebase mới làm vậy).", "week02.pdf tr.14; week01.pdf tr.82", "k2-mohinh"),
    Q("K2-05", "multi", "You ran <code>git merge iss53</code> while on <code>master</code> and index.html now contains the block below. Which statements are correct?",
      ["The part above <code>=======</code> is the version from master (HEAD).", "After editing the file and removing all markers, run <code>git add index.html</code> and then <code>git commit</code>.",
       "Git has already created the merge commit automatically.", "The part above <code>=======</code> comes from iss53."], "ab",
      "HEAD = nhánh đang đứng (master) ở phía trên. Khi conflict, Git dừng lại, chưa tạo merge commit; sửa xong add để đánh dấu đã giải quyết rồi commit.", "Pro Git tr.83–84", "k2-conflict", code=CONF, lang="text"),
    Q("K2-06", "single", "What happens, and how can you delete the branch anyway?",
      ["It fails with 'not fully merged'; <code>git branch -D testing</code> forces the deletion and discards the unmerged work.", "It succeeds silently.",
       "It fails; <code>git push origin --delete testing</code> is required first.", "It merges testing into the current branch, then deletes it."], "a",
      "<code>-d</code> chặn xoá nhánh còn công việc chưa merge; <code>-D</code> bỏ qua kiểm tra và mất công việc đó vĩnh viễn.", "week02.pdf tr.25–27", "k2-cmd",
      code="$ git branch --no-merged\n  testing\n$ git branch -d testing", lang="bash"),
    Q("K2-07", "single", "Which command lists the branches whose work is <b>not yet</b> merged into the branch you currently have checked out?",
      ["<code>git branch --no-merged</code>", "<code>git branch --merged</code>", "<code>git branch -v</code>", "<code>git log --graph</code>"], "a",
      "--merged / --no-merged lọc theo trạng thái merge so với nhánh hiện tại.", "week02.pdf tr.22–25; ex2.docx Part B.2", "k2-cmd"),
    Q("K2-08", "single", "You want to rename the shared branch <code>wip</code> to <code>work-in-progress</code> so collaborators see the new name. Which sequence is correct?",
      ["<code>git branch --move wip work-in-progress</code> → <code>git push --set-upstream origin work-in-progress</code> → <code>git push origin --delete wip</code>",
       "<code>git push origin --delete wip</code> only", "<code>git checkout -b work-in-progress</code> → <code>git branch -D wip</code>", "<code>git remote rename wip work-in-progress</code>"], "a",
      "Đổi tên local, đẩy tên mới lên và đặt upstream, rồi xoá tên cũ trên remote (tên cũ vẫn còn cho tới khi xoá).", "week02.pdf tr.29–31; ex2.docx Part B.4", "k2-trap-rename"),
    Q("K2-09", "multi", "Consider this output. Which statements are correct?",
      ["serverfix has 3 local commits not pushed and 1 commit on the server not yet merged locally.", "testing has no upstream branch.",
       "The ahead/behind numbers are always live, even without fetching.", "master tracks origin/master and was up to date at the last fetch."], "abd",
      "Số ahead/behind chỉ mới bằng lần fetch cuối; muốn số mới: <code>git fetch --all; git branch -vv</code>.", "week02.pdf tr.54; Pro Git tr.100", "k2-trap-vv", code=VV, lang="text"),
    Q("K2-10", "multi", "Which statements about this sequence are correct?",
      ["The final snapshot equals what a three-way merge would produce.", "The history becomes linear.", "The final <code>git merge experiment</code> is a fast-forward.", "The original experiment commits keep their hashes."], "abc",
      "Rebase phát lại các patch thành commit mới (C3', C4' — hash mới). Sau đó merge từ master là fast-forward. Snapshot cuối giống merge.", "week02.pdf tr.58–62", "k2-trap-rebase",
      code="git checkout experiment\ngit rebase master\ngit checkout master\ngit merge experiment", lang="bash"),
    Q("K2-11", "single", "Which practice follows the lecture's guidance on rebase vs. merge?",
      ["Rebase local, unpushed commits to clean up; never rebase anything already pushed publicly.", "Always rebase the shared main branch after every push.", "Never use merge once rebase is available.", "Rebase is always correct; merge is always wrong."], "a",
      "Không có cách nào đúng tuyệt đối; thỏa hiệp: rebase thay đổi local chưa push, không rebase thứ đã public.", "week02.pdf tr.67; Pro Git tr.106", "k2-rebase"),
    Q("K2-12", "single", "<code>client</code> branched off <code>server</code>, which branched off <code>master</code>. What does this command do?",
      ["Replays the commits of client made since it diverged from server onto master.", "Replays server onto client.", "Merges master into server and client.", "Deletes server after rebasing client."], "a",
      "--onto master server client: lấy client, tìm các patch kể từ khi tách khỏi server, phát lại như thể dựa trực tiếp trên master; sau đó có thể fast-forward master.", "week02.pdf tr.63–64; Pro Git tr.104", "k2-rebase",
      code="git rebase --onto master server client", lang="bash"),
    Q("K2-13", "single", "A collaborator pushed <code>serverfix</code>. After <code>git fetch origin</code>, what does this command create?",
      ["A local branch <code>sf</code> that tracks <code>origin/serverfix</code>; <code>git pull</code> on sf pulls from it.", "A remote branch named sf.", "A tag called sf.", "Nothing; fetch already created an editable local serverfix."], "a",
      "Fetch chỉ tạo remote-tracking branch origin/serverfix (không sửa được). <code>checkout -b sf origin/serverfix</code> tạo nhánh local (tên khác) có upstream là origin/serverfix.", "week02.pdf tr.48–52", "k2-remote",
      code="git checkout -b sf origin/serverfix", lang="bash"),
]
