"""Checks for the site and deck. Run:  python3 -m unittest discover -s tests -v

Needs pandas and python-pptx. The browser tests are skipped if no Chromium is found
(set CHROME=/path/to/chrome to point at one)."""
import glob, json, os, pathlib, re, shutil, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def find_chrome():
    for c in [os.environ.get("CHROME"), shutil.which("chromium"), shutil.which("google-chrome"), shutil.which("chromium-browser"),
              *sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))]:
        if c and os.path.exists(c):
            return c
    return None


def dump_dom(chrome, route, budget=15000):
    r = subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--window-size=1300,900", f"--virtual-time-budget={budget}",
                        "--dump-dom", f"file://{ROOT / 'site' / 'index.html'}#{route}"], capture_output=True, text=True, timeout=120)
    return r.stdout


class DataTests(unittest.TestCase):
    def test_reference_totals(self):
        import pandas as pd
        d = ROOT / "public" / "data"
        s = pd.read_csv(d / "sales.csv"); p = pd.read_csv(d / "products.csv")
        for c in ("Product_Cost", "Product_Price"):
            p[c] = p[c].str.replace(r"[$ ]", "", regex=True).astype(float)
        x = s.merge(p, on="Product_ID")
        self.assertEqual(len(x), 829262)
        self.assertEqual(int(x.Units.sum()), 1090565)
        self.assertAlmostEqual((x.Units * x.Product_Price).sum(), 14444572.35, places=2)
        self.assertAlmostEqual((x.Units * (x.Product_Price - x.Product_Cost)).sum(), 4014029.00, places=2)

    def test_sale_ids_unique_and_keys_join(self):
        import pandas as pd
        d = ROOT / "public" / "data"
        s = pd.read_csv(d / "sales.csv")
        self.assertTrue(s.Sale_ID.is_unique)
        self.assertTrue(s.Product_ID.isin(pd.read_csv(d / "products.csv").Product_ID).all())
        self.assertTrue(s.Store_ID.isin(pd.read_csv(d / "stores.csv").Store_ID).all())


class BuildTests(unittest.TestCase):
    def test_site_is_up_to_date_with_its_source(self):
        import build_site
        self.assertEqual(build_site.build(), (ROOT / "site" / "index.html").read_text(),
                         "site/index.html is stale: run python3 scripts/build_site.py and commit it")

    def test_deck_builds_and_its_numbers_hold(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp) / "deck.pptx"
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_deck.py"), str(out)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr[-800:])
            self.assertTrue(out.exists())


class AskDataTests(unittest.TestCase):
    def setUp(self):
        src = (ROOT / "site-src" / "js" / "50-ask-questions.js").read_text()
        self.ids = set(re.findall(r'\{id:"([a-z_]+)",group:', src))
        self.para = json.loads((ROOT / "evaluations" / "ask_paraphrases.json").read_text())
        self.ev = json.loads((ROOT / "evaluations" / "ask_eval.json").read_text())["cases"]

    def test_fifteen_questions_each_with_phrasings(self):
        self.assertEqual(len(self.ids), 15)
        self.assertEqual(set(self.para), self.ids)
        for k, v in self.para.items():
            self.assertGreaterEqual(len(v), 10, k)

    def test_eval_cases_use_valid_ids_and_do_not_leak_into_the_bank(self):
        bank = {p.lower() for v in self.para.values() for p in v}
        for q, exp in self.ev:
            self.assertTrue(exp == "none" or exp in self.ids, (q, exp))
            self.assertNotIn(q.lower(), bank, f"held-out question also in the phrasing bank: {q}")


@unittest.skipUnless(find_chrome(), "no Chromium available")
class BrowserTests(unittest.TestCase):
    def test_every_tab_renders(self):
        chrome = find_chrome()
        expect = {"start": "Maven Toys Analytics Hub", "dashboard": "Sales Performance Dashboard", "toys": "Toy Catalog",
                  "presentation": "From Colorbuds to Playfoam", "ask": "Ask the Data"}
        for route, text in expect.items():
            self.assertIn(text, dump_dom(chrome, route), route)

    def test_ask_matcher_accuracy_on_held_out_questions(self):
        dom = dump_dom(find_chrome(), "ask-eval")
        m = re.search(r'<pre id="evalout">([^<]*)', dom)
        self.assertIsNotNone(m, "ask-eval hook did not run")
        o = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&"))
        self.assertGreaterEqual(o["neu"] / o["n"], 0.85, o)
        self.assertGreater(o["neu"], o["old"])


if __name__ == "__main__":
    unittest.main()
