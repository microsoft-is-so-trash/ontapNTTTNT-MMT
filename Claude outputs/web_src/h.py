"""Authoring helpers for the study site content."""
import html as _html


def Q(id, loai, de, dap_an, dung, giai_thich, nguon, muc=None, code=None, lang=None, demo=None, mon="TTNT", hoi=None):
    """dung: letters like 'abd' (a = first option in dap_an)."""
    return dict(id=id, mon=mon, khoi=id.split("-")[0], loai=loai, de=de, code=code, lang=lang,
                dap_an=dap_an, dung=[ord(c) - 97 for c in dung], giai_thich=giai_thich,
                nguon=nguon, muc=muc, demo=demo, hoi=hoi)


def QQ(de, dap_an, dung, giai_thich, code=None, lang=None):
    """Quick question at the end of a review page (single answer)."""
    return dict(de=de, dap_an=dap_an, dung=[ord(dung) - 97], giai_thich=giai_thich, code=code, lang=lang)


def c(s):
    """inline code"""
    return "<code>" + _html.escape(s) + "</code>"


def pre(code, lang="text"):
    return '<pre data-lang="%s">%s</pre>' % (lang, _html.escape(code.strip("\n")))


def table(head, rows, cls=""):
    h = '<div class="tw"><table%s><tr>' % (' class="%s"' % cls if cls else "")
    h += "".join("<th>%s</th>" % x for x in head) + "</tr>"
    for r in rows:
        h += "<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>"
    return h + "</table></div>"


def src(s):
    return '<p class="src">Nguồn: %s</p>' % s


def note(s, kind=""):
    return '<div class="note %s">%s</div>' % (kind, s)


def diagram(svg, cap=""):
    return '<div class="diagram">%s%s</div>' % (svg, '<div class="cap">%s</div>' % cap if cap else "")


def flow(steps, active=()):
    out = '<div class="flow">'
    for i, s in enumerate(steps):
        if i:
            out += '<span class="ar">→</span>'
        out += '<span class="s%s">%s</span>' % (" a" if i in active else "", s)
    return out + "</div>"


def ul(items):
    return "<ul>" + "".join("<li>%s</li>" % i for i in items) + "</ul>"


def trap(title, body, id=None):
    return '<div class="card"%s><b>%s</b><div>%s</div></div>' % (' id="%s"' % id if id else "", title, body)
