"""Build site/index.html from its source parts. One command, no arguments:

    python3 scripts/build_site.py

site/index.html is generated. Edit the parts, then rebuild:

  site-src/index.html          page shell (header, tab containers) with __STYLES__ / __SCRIPTS__ slots
  site-src/css/*.css           styles, concatenated in file-name order (01- to 05-)
  site-src/js/*.js             scripts, concatenated in file-name order (data, metrics, charts, one file per tab, router)
  public/data/*.csv            original data; scripts/gen_data.py compacts it for the browser (fills __DATA__)
  scripts/toy_illustrations.py the 35 toy drawings (fills __ILLUS__)
  evaluations/ask_*.json       Ask phrasing bank and held-out test set (fill __PARA__ and __EVAL__)
"""
import pathlib, subprocess, sys, tempfile

root = pathlib.Path(__file__).resolve().parent.parent
src = root / "site-src"
py = sys.executable


def read_all(folder, pattern):
    return "".join(p.read_text() for p in sorted((src / folder).glob(pattern)))


def build():
    data = subprocess.run([py, str(root / "scripts" / "gen_data.py"), str(root / "public" / "data")],
                          check=True, capture_output=True, text=True).stdout.strip()
    with tempfile.TemporaryDirectory() as tmp:
        ill_path = pathlib.Path(tmp) / "illus.json"
        subprocess.run([py, str(root / "scripts" / "toy_illustrations.py"), str(ill_path), str(pathlib.Path(tmp) / "sheet")],
                       check=True, capture_output=True)
        illus = ill_path.read_text()
    html = (src / "index.html").read_text()
    html = html.replace("__STYLES__", read_all("css", "*.css")).replace("__SCRIPTS__", read_all("js", "*.js"))
    para = (root / "evaluations" / "ask_paraphrases.json").read_text()
    ev = (root / "evaluations" / "ask_eval.json").read_text()
    return html.replace("__DATA__", data).replace("__ILLUS__", illus).replace("__PARA__", para).replace("__EVAL__", ev)


if __name__ == "__main__":
    out = build()
    (root / "site" / "index.html").write_text(out)
    print("wrote site/index.html", len(out))
