#!/usr/bin/env python3
"""Chuyển các file question_bank/<KHOI>.txt (định dạng gọn) thành câu hỏi JSON
và chèn vào artifact HTML gốc.

Định dạng mỗi file:
  ## <muc> | <nguon> [| <lang>]     -> mục ôn + nguồn mặc định cho các câu phía sau
  Q: đề bài (dùng `code` cho mã nội dòng, **đậm**)
  > dòng code (khối code, nhiều dòng)
  L: lang (tuỳ chọn, ghi đè lang mặc định)
  - đáp án sai
  + đáp án đúng   (>1 dấu + => câu chọn nhiều)
  = giải thích
  (dòng trống kết thúc câu)
"""
import re, json, sys, html, glob, os

def inline(s):
    out = []; parts = re.split(r'(`[^`]+`)', s)
    for p in parts:
        if p.startswith('`') and p.endswith('`') and len(p) > 1:
            out.append('<code>' + html.escape(p[1:-1], quote=False) + '</code>')
        else:
            e = html.escape(p, quote=False)
            e = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', e)
            out.append(e)
    return ''.join(out)

def parse(path, khoi, mon):
    qs = []; muc = None; nguon = ''; dlang = None; cur = None
    def flush():
        nonlocal cur
        if cur:
            assert cur['de'] and len(cur['opts']) >= 2 and any(o[0] for o in cur['opts']), (path, cur)
            qs.append(cur)
        cur = None
    for raw in open(path, encoding='utf8').read().splitlines() + ['']:
        line = raw.rstrip('\n')
        if line.startswith('## '):
            flush(); parts = [x.strip() for x in line[3:].split('|')]
            muc = parts[0] or None; nguon = parts[1] if len(parts) > 1 else ''
            dlang = parts[2] if len(parts) > 2 and parts[2] else None
            continue
        if not line.strip():
            flush(); continue
        if line.startswith('#'): continue
        if line.startswith('Q: '):
            flush(); cur = dict(de=line[3:], code=[], lang=dlang, opts=[], g='', muc=muc, nguon=nguon); continue
        assert cur is not None, (path, line)
        if line.startswith('> ') or line == '>': cur['code'].append(line[2:])
        elif line.startswith('L: '): cur['lang'] = line[3:].strip()
        elif line.startswith('N: '): cur['nguon'] = line[3:].strip()
        elif line.startswith('- '): cur['opts'].append((False, line[2:]))
        elif line.startswith('+ '): cur['opts'].append((True, line[2:]))
        elif line.startswith('= '): cur['g'] += (' ' if cur['g'] else '') + line[2:]
        else: raise ValueError((path, line))
    out = []
    for i, c in enumerate(qs, 1):
        dung = [j for j, o in enumerate(c['opts']) if o[0]]
        out.append({
            'id': f'{khoi}-{100+i}', 'mon': mon, 'khoi': khoi,
            'loai': 'multi' if len(dung) > 1 else 'single',
            'de': inline(c['de']),
            'code': '\n'.join(c['code']) if c['code'] else None,
            'lang': (c['lang'] or 'text') if c['code'] else None,
            'dap_an': [inline(o[1]) for o in c['opts']], 'dung': dung,
            'giai_thich': inline(c['g']), 'nguon': c['nguon'], 'muc': c['muc'],
            'demo': None, 'hoi': None, 'bo': 'luyentap'})
    return out


PATCHES = [
 # chọn số câu cho quiz từng khối
 ("""  h += '<div class="donebar"><button class="btn pri" id="go">Bắt đầu</button>'+(back?""",
  """  if(back && qs.length>25) h += '<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0" class="small"><span>Số câu mỗi lượt:</span><select id="qN" style="padding:5px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)">'+[20,40,60].filter(x=>x<qs.length).map(x=>'<option value="'+x+'"'+(x===20?' selected':'')+'>'+x+' câu</option>').join("")+'<option value="0">Tất cả '+qs.length+' câu</option></select><label style="display:flex;gap:6px;align-items:center"><input type="checkbox" id="qNew" checked> Ưu tiên câu chưa làm / ít làm</label></div>';
  h += '<div class="donebar"><button class="btn pri" id="go">Bắt đầu</button>'+(back?"""),
 ("""  $("#go").onclick=()=>startQuiz(kind, qs, title, {block:back?back.id:null});""",
  """  $("#go").onclick=()=>{ let pick=qs; const sN=$("#qN");
    if(sN && +sN.value>0){ const n=+sN.value; const pre=$("#qNew")&&$("#qNew").checked; pick = pre ? shuffle(qs).sort((a,b)=>(S.seen[a.id]||0)-(S.seen[b.id]||0)).slice(0,n) : shuffle(qs).slice(0,n); }
    startQuiz(kind, pick, title, {block:back?back.id:null}); };"""),
 # mục "Lý thuyết chuyên sâu" chèn sau mục 3 khi khối có page.sau
 ("""  const p=b.page||{};
  let h = '<div class="kicker">""",
  """  const p=b.page||{};
  const SX = p.sau ? SECS.slice(0,3).concat([["sau","Lý thuyết chuyên sâu (slide + giáo trình)"]], SECS.slice(3)) : SECS;
  let h = '<div class="kicker">"""),
 ("""  h += '<div class="flow small">'+SECS.map(""", """  h += '<div class="flow small">'+SX.map("""),
 ("""  SECS.forEach((s,i)=>{
    const id = bid.toLowerCase()+"-"+s[0];""", """  SX.forEach((s,i)=>{
    const id = bid.toLowerCase()+"-"+s[0];"""),
]

def main(src, dst):
    h = open(src, encoding='utf8').read()
    for a, b in PATCHES:
        assert h.count(a) == 1, a[:60]
        h = h.replace(a, b)
    m = re.search(r'(<script type="application/json" id="D">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    mon_of = {b['id']: b['mon'] for b in d['blocks']}
    d['questions'] = [q for q in d['questions'] if q.get('bo') != 'luyentap']
    here = os.path.dirname(os.path.abspath(__file__))
    for b in d['blocks']:
        tp = os.path.join(here, 'theory', b['id'] + '.html')
        if os.path.exists(tp):
            b['page']['sau'] = open(tp, encoding='utf8').read()
    stats = {}
    for b in d['blocks']:
        p = os.path.join(here, b['id'] + '.txt')
        if not os.path.exists(p): continue
        new = parse(p, b['id'], b['mon'])
        anchors = set(re.findall(r'id="([a-z0-9-]+)"', ''.join(v for v in b['page'].values() if isinstance(v, str))))
        anchors |= {b['id'].lower() + '-' + x for x in ('y', 'sau', 'mohinh', 'bang', 'sosanh', 'bay', 'checklist', 'nhanh', 'docthem')}
        for q in new:
            if q['muc'] and q['muc'] not in anchors:
                print('WARN muc khong ton tai', q['id'], q['muc'])
        d['questions'].extend(new); stats[b['id']] = len(new)
    js = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    h = h[:m.start(2)] + js + h[m.end(2):]
    open(dst, 'w', encoding='utf8').write(h)
    print(stats, 'tong moi =', sum(stats.values()), 'tong =', len(d['questions']))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
