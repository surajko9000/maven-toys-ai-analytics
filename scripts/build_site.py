"""Build site/index.html from its source parts. One command, no arguments:

    python3 scripts/build_site.py

Parts:
  site-src/template.html                 the app (HTML + CSS + JS) with __DATA__, __ILLUS__, __PARA__, __EVAL__ placeholders
  public/data/*.csv  -> scripts/gen_data.py          compact sales/product/store/inventory data
  scripts/mockup_illustrations_all.py                the 35 toy drawings (SVG)
  evaluations/ask_paraphrases.json, ask_eval.json    Ask-tab phrasing bank and held-out test set
"""
import json, pathlib, subprocess, sys, tempfile
root = pathlib.Path(__file__).resolve().parent.parent
py = sys.executable
data = subprocess.run([py, str(root / "scripts" / "gen_data.py"), str(root / "public" / "data")], check=True, capture_output=True, text=True).stdout
with tempfile.TemporaryDirectory() as tmp:
    ill_path = pathlib.Path(tmp) / "illus.json"
    subprocess.run([py, str(root / "scripts" / "mockup_illustrations_all.py"), str(ill_path), str(pathlib.Path(tmp) / "sheet")], check=True, capture_output=True)
    ill = ill_path.read_text()
tpl = (root / "site-src" / "template.html").read_text()
para = (root / "evaluations" / "ask_paraphrases.json").read_text()
ev = (root / "evaluations" / "ask_eval.json").read_text()
out = tpl.replace("__DATA__", data.strip()).replace("__ILLUS__", ill).replace("__PARA__", para).replace("__EVAL__", ev)
(root / "site" / "index.html").write_text(out)
print("wrote site/index.html", len(out))
