"""Splice data + illustrations + Ask phrasing bank/eval set into the single-file site.
Usage: python3 scripts/build_site.py <template.html> <data.json> <illustrations.json>"""
import sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
tpl, data, ill = (pathlib.Path(a).read_text() for a in sys.argv[1:4])
para = (root / "evaluations" / "ask_paraphrases.json").read_text()
ev = (root / "evaluations" / "ask_eval.json").read_text()
out = tpl.replace("__DATA__", data).replace("__ILLUS__", ill).replace("__PARA__", para).replace("__EVAL__", ev)
(root / "site" / "index.html").write_text(out)
print("wrote site/index.html", len(out))
