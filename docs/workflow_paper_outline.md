# Workflow document: outline and bullets

Target: 2 to 3 pages. Suggested length per section is in brackets. Items marked **[you fill]** are things only you know.

---

## 1. The job function [about 1/4 page]

- **Role:** business / data analyst at a retail company. This project plays that role for a fictional toy chain, Maven Toys (50 stores across Mexico, 35 toys, Jan 2022 to Sep 2023).
- **Who asks, and for what:** managers and leaders ask an analyst for three kinds of deliverable:
  1. a **dashboard** (people explore the numbers themselves)
  2. a **presentation** (a short story with a recommendation)
  3. **ad hoc data requests** (one-off questions such as "which stores ran out of Playfoam?")
- **What the work really involves:** turning a vague question into a measurable one, getting the data ready, checking it, building the deliverable, and being accountable for the numbers.
- **Concrete example used in this project:** "Is our top profit toy in trouble?" It turned out to be Colorbuds: 8,110 units a month in Jan 2022, 2,594 in Sep 2023, down 68%.

## 2. The current workflow [about 1/2 page]

Write this as numbered steps with a tool and a rough time next to each. **[you fill the times]**

1. **Receive the request** and clarify it (email or meeting). Decide the metric, period and comparison.
2. **Get the data.** Usually already cleaned up and delivered as files or a database. Here: four CSVs (829,262 sales lines, products, stores, inventory).
3. **Prepare and check it.** Load, join, fix problems (price stored as text, a misspelled city, a partial inventory snapshot), and confirm totals.
4. **Analyze** in a spreadsheet, SQL or Python.
5. **Build the deliverable** by hand in a BI tool (dashboard) and PowerPoint (deck). Charts, filters, layout, speaker notes.
6. **Answer ad hoc requests** one at a time: write a query, run it, paste a result, explain it.
7. **Review and share.** Check numbers again, present, then handle follow-up questions.

- **Where the time goes today:** building and restyling deliverables (steps 5 and 6), and repeating work every time a new question comes in.

## 3. The AI-augmented workflow [about 1/2 page]

Same seven steps, with Claude Code doing the building and the human doing the judging. A small table works well:

| Step | Claude does | I still do |
|---|---|---|
| Clarify the request | Turns a vague ask into specific questions and flags ambiguity ("best" means units, revenue or profit?) | Decide what matters |
| Prepare the data | Profiles the files, finds issues, writes the cleaning rules | Confirm the fixes make sense |
| Build the dashboard | Writes the whole page from a plain-language description and reworks it in minutes | Check every number |
| Build the deck | Drafts slides, charts and speaker notes | Choose the message, cut words, check each claim |
| Ad hoc requests | Understands the question and finds the matching calculation (a demo of this) | Sanity-check the answer |
| Review | Writes tests and checks totals against an independent calculation | Accountable for the result |

- **What changed:** the human moves from builder to director and checker. Iteration is cheap, so I could test many versions (the deck went through about ten rounds of restyling).
- **Human checkpoints I kept:** I read every number, and I made every decision about message, tone and design.

## 4. The specific tools and prompts [about 3/4 page]

Tools: **Claude Code** (builds everything), a small **in-browser embedding model** (optional, Ask tab only), GitHub Pages (hosting).

Include at least two prompts verbatim, each with "first version, what was wrong, refined version, result". **[you fill the exact text from your chat history]** Candidates:

- **Prompt A: dashboard.** Starting point: "Build me a dashboard" on the four CSVs, with a time filter and a toy dropdown.
  - *Refinements that mattered:* a collapsible filter bar, values vs. percent-of-selection toggle, a gross-margin measure, clearer sorting.
  - *Output:* the Dashboard tab (KPIs, trend, category / toy / store charts, sortable table with CSV export).
- **Prompt B: presentation.** Starting point: "Build me a presentation" about the main finding.
  - *Refinements that mattered:* "6 slides, short text, one message per slide", "more professional, consulting style", "give me options for the recommendation", "show Playfoam's rise in a way people can understand".
  - *Output:* the six-slide deck (Colorbuds is declining, Playfoam is the next bet), as PowerPoint and PDF.
- **Prompt C (optional): ad hoc questions.** "Let people ask questions in plain English." Refined into 15 approved questions, about 200 example phrasings, follow-up memory, and an optional embedding model.

## 5. Evidence it works [about 1/2 page]

Show with screenshots or links. **[add screenshots]**

- **Live site:** https://surajko9000.github.io/maven-toys-ai-analytics/ and the repo https://github.com/surajko9000/maven-toys-ai-analytics.
- **The four artifacts:** Dashboard, Toy Finder (a custom data app), the 6-slide deck, the Ask demo.
- **Numbers are checked, not trusted:**
  - Totals match an independent pandas calculation (829,262 rows, 1,090,565 units, $14.44M revenue, $4.01M estimated gross profit).
  - Every number on the slides is asserted against the CSVs when the deck is built.
  - An automated test suite (8 tests) runs on the data, the build, the deck and the Ask matcher.
- **A measured result:** on 106 held-out Ask questions, the first keyword matcher scored **66.0%**. After adding a phrasing bank, synonyms and typo repair it scored **90.6%**, and it still declined all 12 out-of-scope questions. The in-browser model result: **[you fill: the number from "Test accuracy"]**.
- **The iteration log** (`evaluations/iteration_log.md`) records what happened at each step.

## 6. Honest limitations [about 3/4 page]

Group these under three headings.

**Where AI helps a lot**
- Speed: a working dashboard, a branded deck and 35 original toy illustrations in days, not weeks.
- Cheap iteration: restyling or restructuring takes minutes.

**Where it needs a lot of human effort**
- **Polish is slow.** Getting to a final look took many rounds. Because the output is Python or JavaScript, small changes are possible, but I often had to ask for a section to be rebuilt.
- **Recommendations were weak at first.** Example: the first slide showed Playfoam going from $9K to $20K a month, which looked like growth. The real cause was a partial first month; weekly sales were actually flat. I caught it, and the slide was changed to rank-based facts. Getting useful metrics took real effort and judgment.
- **Wrong defaults.** It assumed the data covered 2017 to 2018 before profiling showed 2022 to 2023.
- **I did not write or read the code line by line.** Claude first produced it as one very large file, which is confusing and not best practice. A developer would split it by tab. I had to ask for that cleanup separately (it now has css and js modules, a one-command build and tests).

**Ad hoc conversational analytics was the weakest part**
- It misread questions at first (a typo like "margn" was read as "March"), and picked the wrong question for natural wording. Accuracy on held-out questions was 66% before work, 90.6% after.
- The risk of wrong data or wrong interpretation is highest here, because the answer sounds confident.
- **Hard to share a working version.** A real AI answering questions cannot be hosted for free on GitHub, so the public Ask tab is a demo that picks from 15 prepared questions. In a company the blockers are different: access to databases and tools, permissions, and cost per question. Those are common problems and not a huge lift, but they are real.

**Bottom line:** extremely useful, but experimental and directional. It is not something to hand to leadership to explore the data unsupervised.

## 7. Risk note [about 1/2 page]

Use a small table: risk, how likely or severe, how I manage it. **[pick at least one to develop in detail, tied to your module 8 thinking]**

| Risk | Impact | How I manage it |
|---|---|---|
| **Data validation is wrong** (bad join, wrong metric definition, hidden data quirk) | Confidently wrong dashboard or deck | Independent pandas check of totals; shared definitions in one function; automated tests against the raw CSVs; assertions on every slide number |
| **Nobody can fix the code if it breaks** (I did not write it) | Dashboard stops working, nobody knows why | Ask Claude to diagnose; dashboards are far simpler than full apps; code is split into small files with a README and tests |
| **Conversational answers that sound right but are wrong** | Misleading decisions; unclear who is accountable | Prepared questions only; show how each answer was calculated; decline questions the data cannot answer; a human reviews before anything is shared; test against held-out questions |
| **Estimates presented as facts** (revenue is units times one current price; profit ignores other costs) | Overstated confidence | Label it "estimated" everywhere; list assumptions |
| **Recommendations that look good but are not supported** (the Playfoam "growth" example) | Bad business decision | A human checks each claim against a second cut of the data before it reaches a slide |
| **Image and data rights** | Legal exposure | Original drawings, not copied photos; public sample dataset only |
| **Over-trusting a polished result** | Skipped review | Treat output as a draft; reviewer signs off |

- **Accountability point to make explicitly:** the analyst remains accountable for any number that leaves the team, whoever (or whatever) produced it.

---

## Rubric check

| Criterion (weight) | Where it is covered |
|---|---|
| Specificity of the workflow (25%) | Sections 1 to 3: a named role, seven concrete steps, a real example (Colorbuds) |
| Quality of AI integration (25%) | Sections 3 to 5: verbatim prompts with refinements, working outputs, a measured result |
| Honest assessment of limits (20%) | Section 6: specific failures (Ask accuracy, weak recommendations, one-file code) |
| Risk awareness (15%) | Section 7: validation, accountability, conversational risk, estimates |
| Presentation clarity (15%) | Plain words, one table per section, screenshots, no jargon without explanation |

## Things to gather before writing

- [ ] The exact text of your prompts from your chat history (dashboard, presentation).
- [ ] Rough time per step in your current workflow, and total time for this project.
- [ ] The accuracy number from the Ask tab's "Test accuracy" button.
- [ ] Screenshots: dashboard, one deck slide, Toy Finder, an Ask answer.
- [ ] Note that `evaluations/prompts.md` and `evaluations/limitations.md` are still empty stubs, and the iteration log stops at item 10. I can fill them in from this conversation if you want them as supporting evidence.
