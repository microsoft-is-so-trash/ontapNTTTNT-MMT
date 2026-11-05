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

def main(src, dst):
    h = open(src, encoding='utf8').read()
    m = re.search(r'(<script type="application/json" id="D">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    mon_of = {b['id']: b['mon'] for b in d['blocks']}
    d['questions'] = [q for q in d['questions'] if q.get('bo') != 'luyentap']
    here = os.path.dirname(os.path.abspath(__file__))
    stats = {}
    for b in d['blocks']:
        p = os.path.join(here, b['id'] + '.txt')
        if not os.path.exists(p): continue
        new = parse(p, b['id'], b['mon'])
        anchors = set(re.findall(r'id="([a-z0-9-]+)"', ''.join(v for v in b['page'].values() if isinstance(v, str))))
        anchors |= {b['id'].lower() + '-' + x for x in ('y', 'mohinh', 'bang', 'sosanh', 'bay', 'checklist', 'nhanh', 'docthem')}
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
