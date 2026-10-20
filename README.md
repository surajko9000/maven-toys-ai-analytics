# Maven Toys AI Analytics Lab

An AI-generated analytics hub built on public data, hosted free on GitHub Pages. Built as a Chicago Booth
AI Essentials capstone and a portfolio project: how does AI change an analytics engineer's workflow, from
hand-assembling dashboards to describing data applications in plain language?

**Data:** [Maven Analytics – Mexico Toy Sales](https://mavenanalytics.io/data-playground/mexico-toy-sales)
(fictional retailer, public sample data). The app reads the four original CSVs directly in the browser. No database,
no server, no API keys.

## Four tabs, one dataset, one set of definitions

| Tab | Purpose |
|---|---|
| **Dashboard** | KPI cards, filters, trend and breakdown charts, sortable table, CSV export |
| **Presentation** | A paged mini-deck: one headline insight per slide, every number computed from the data |
| **Toy Finder** | Visual catalog of the 35 toys with detail view, comparison, stock by store |
| **Ask** | Chat-style Q&A that matches a typed question to ~20-30 verified questions; declines what it can't answer |

All tabs share one `agg()` function in the template, so revenue, profit and margin mean the same thing everywhere.

## Status

Planning and data validation complete. Front-end build in progress. See `docs/architecture.md`.

## Honest limitations (so far)

- Revenue and profit are **reconstructed** (units x current price/cost); the data has no price history.
- Inventory is a single undated snapshot, not a history.
- "Latest week/quarter" means latest in the data (through 2023-09-30), not today.
- Ask answers only approved questions. It does not generate SQL or free-form answers.

## Repository layout

```
site-src/                the app source (edit these)
  index.html               page shell: header and tab containers
  css/01-05-*.css          styles: base, home, presentation, toys, ask
  js/*.js                  scripts in load order: data, metrics, charts, one file per tab (Ask is 4 files), confetti, router
site/                    the published site: index.html (generated), deck files, fonts, images
public/data/             original CSVs (unmodified)
data/                    data dictionary and validation notes
scripts/                 build_site.py, gen_data.py, build_deck.py, toy_illustrations*.py, verify_totals.py
tests/                   data, build, deck and browser checks
evaluations/             Ask phrasing bank and test set, prompt log, iteration log, limitations, risks
docs/                    architecture notes and design mockups
.github/workflows/       deploy.yml publishes site/ to GitHub Pages on every push
```

## Verify the headline numbers

```
python3 scripts/verify_totals.py
```

## Rebuild the deck

```
python3 scripts/build_deck.py            # writes site/deck/Colorbuds_to_Playfoam.pptx (asserts every number against the CSVs)
# then export the PDF and slide previews the site shows (needs LibreOffice + poppler):
soffice --headless --convert-to pdf --outdir site/deck site/deck/Colorbuds_to_Playfoam.pptx
pdftoppm -jpeg -r 110 site/deck/Colorbuds_to_Playfoam.pdf site/deck/preview/slide
```

## Rebuild the site and test the Ask matcher

```
python3 scripts/build_site.py      # no arguments: rebuilds site/index.html from its parts
```

`site/index.html` is a generated file. Do not edit it by hand. Edit the parts instead:

| Part | What it is |
|---|---|
| `site-src/index.html`, `css/`, `js/` | The app. Files load in name order, so the numeric prefixes matter |
| `public/data/*.csv` | The four original CSVs, unmodified. `scripts/gen_data.py` compacts them for the browser |
| `scripts/toy_illustrations.py` | The 35 original toy drawings (SVG) |
| `evaluations/ask_paraphrases.json` | About 200 example phrasings for the 15 approved Ask questions |
| `evaluations/ask_eval.json` | Held-out test phrasings for the Ask matcher |

## Run the tests

```
python3 -m unittest discover -s tests -v
```

Checks the reference totals against the raw CSVs, that `site/index.html` is up to date with its source, that the deck builds (and its
numbers hold), that the Ask data is consistent, and, if Chromium is installed, that every tab renders and the Ask matcher scores at least 85% on the held-out set.

The Ask tab matches questions against the phrasing bank. Open `site/index.html#ask-eval` to see the accuracy of the old and new keyword matchers, or turn on
"Smarter matching" in the Ask tab and press "Test accuracy" to test the in-browser model.
