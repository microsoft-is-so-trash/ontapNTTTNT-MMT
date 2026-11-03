"""Assemble index.html from shell + content modules, with validation."""
import importlib, json, os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.environ.get("REPO") or os.path.abspath(os.path.join(HERE, "..", ".."))
OUTS = [os.path.join(REPO, "Claude outputs", "index.html"), os.path.join(REPO, "index.html")]

MODULES = ["c_k1", "c_k2", "c_k3", "c_k4", "c_k5", "c_k6", "c_k7", "c_k8", "c_k9",
           "c_c1", "c_c2", "c_c3", "c_c4", "c_meta", "c_mmt_soon", "c_cards"]


def load():
    blocks, questions, extra = [], [], {}
    for m in MODULES:
        if not os.path.exists(os.path.join(HERE, m + ".py")):
            continue
        mod = importlib.import_module(m)
        if hasattr(mod, "BLOCK"):
            blocks.append(mod.BLOCK)
        for b in getattr(mod, "BLOCKS", []):
            if b["id"] not in {x["id"] for x in blocks}:
                blocks.append(b)
        questions += getattr(mod, "QUESTIONS", [])
        for k in ("schedule", "tools", "flashcards", "calc"):
            if hasattr(mod, k.upper()):
                extra[k] = getattr(mod, k.upper())
    order = ["K%d" % i for i in range(1, 10)] + ["C%d" % i for i in range(1, 5)]
    blocks.sort(key=lambda b: order.index(b["id"]))
    return blocks, questions, extra


def validate(blocks, questions):
    errs = []
    ids = set()
    bids = {b["id"] for b in blocks}
    anchors = {}
    for b in blocks:
        p = b.get("page") or {}
        html = " ".join(v for v in p.values() if isinstance(v, str))
        anchors[b["id"]] = set(re.findall(r'id="([^"]+)"', html)) | {
            b["id"].lower() + "-" + s for s in ("y", "mohinh", "bang", "sosanh", "bay", "checklist", "nhanh", "docthem")}
        for i, q in enumerate(p.get("quick", [])):
            if not all(0 <= d < len(q["dap_an"]) for d in q["dung"]):
                errs.append("quick %s/%d bad dung" % (b["id"], i))
        if not b.get("soon") and len(p.get("quick", [])) != 3:
            errs.append("%s needs 3 quick questions" % b["id"])
    for q in questions:
        if q["id"] in ids:
            errs.append("dup id " + q["id"])
        ids.add(q["id"])
        if q["khoi"] not in bids:
            errs.append("unknown block " + q["id"])
        if not q["dung"] or not all(0 <= d < len(q["dap_an"]) for d in q["dung"]):
            errs.append("bad dung " + q["id"])
        if q["loai"] == "single" and len(q["dung"]) != 1:
            errs.append("single with %d answers %s" % (len(q["dung"]), q["id"]))
        if q["loai"] == "multi" and len(q["dung"]) < 2:
            errs.append("multi with <2 answers " + q["id"])
        if q.get("muc") and q["muc"] not in anchors.get(q["khoi"], set()):
            errs.append("missing anchor %s for %s" % (q["muc"], q["id"]))
        if len(set(q["dap_an"])) != len(q["dap_an"]):
            errs.append("duplicate options " + q["id"])
        if not q.get("nguon"):
            errs.append("no source " + q["id"])
    return errs


def main():
    blocks, questions, extra = load()
    errs = validate(blocks, questions)
    if errs:
        print("VALIDATION ERRORS:")
        print("\n".join(errs))
        sys.exit(1)
    data = dict(blocks=blocks, questions=questions, **extra)
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    shell = open(os.path.join(HERE, "shell.html"), encoding="utf-8").read()
    import glob
    tools_js = "const TOOLS = {}; window.TOOLS = TOOLS;\n"
    for tp in sorted(glob.glob(os.path.join(HERE, "tools_*.js"))):
        tools_js += open(tp, encoding="utf-8").read() + "\n"
    out = shell.replace("<!--DATA-->", '<script type="application/json" id="D">' + js + "</script>")
    out = out.replace("/*__TOOLS__*/", tools_js)
    for o in OUTS:
        os.makedirs(os.path.dirname(o), exist_ok=True)
        open(o, "w", encoding="utf-8").write(out)
    # stats
    from collections import Counter
    cnt = Counter(q["khoi"] for q in questions)
    multi = Counter(q["khoi"] for q in questions if q["loai"] == "multi")
    code = Counter(q["khoi"] for q in questions if q.get("code") or "<code>" in q["de"])
    print("blocks:", [b["id"] for b in blocks])
    for b in blocks:
        print("  %s: %d q (multi %d, code/cmd %d)" % (b["id"], cnt[b["id"]], multi[b["id"]], code[b["id"]]))
    for mon in ("TTNT", "MMT"):
        qs = [q for q in questions if q["mon"] == mon]
        print(mon, "total", len(qs), "multi", sum(q["loai"] == "multi" for q in qs),
              "demo", sum(1 for q in qs if q.get("demo")))
    print("size %.1f KB" % (len(out.encode()) / 1024))


if __name__ == "__main__":
    main()
