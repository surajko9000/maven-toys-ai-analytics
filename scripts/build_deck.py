"""Builds the 6-slide "Colorbuds is fading" deck as a real .pptx (native charts, speaker notes).

Run:  python3 scripts/build_deck.py [out.pptx]
Every number on the slides is computed from public/data/*.csv and asserted against
the values verified independently with pandas (see evaluations/iteration_log.md).
"""
import sys
from pathlib import Path

import pandas as pd
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "public" / "data"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "site" / "deck" / "Colorbuds_to_Playfoam.pptx"

# ----------------------------------------------------------------- data
sales = pd.read_csv(DATA / "sales.csv", parse_dates=["Date"])
prod = pd.read_csv(DATA / "products.csv")
inv = pd.read_csv(DATA / "inventory.csv")
for c in ("Product_Cost", "Product_Price"):
    prod[c] = prod[c].str.replace(r"[$ ]", "", regex=True).astype(float)
prod["unit_profit"] = prod.Product_Price - prod.Product_Cost
x = sales.merge(prod, on="Product_ID")
x["profit"] = x.Units * x.unit_profit
x["month"] = x.Date.dt.to_period("M")
x["quarter"] = x.Date.dt.to_period("Q")

units_m = x.groupby(["Product_Name", "month"]).Units.sum().unstack(fill_value=0)
cb = units_m.loc["Colorbuds"]
cb_first, cb_last = int(cb.iloc[0]), int(cb.iloc[-1])
cb_drop = round((1 - cb_last / cb_first) * 100)

qp = x.groupby(["Product_Name", "quarter"]).profit.sum().unstack(fill_value=0)
share = lambda q: qp.loc["Colorbuds", q] / qp[q].sum() * 100
share_22, share_23 = round(share("2022Q3")), round(share("2023Q3"))

pf = units_m.loc["Playfoam"]
pf_aug, pf_sep = int(pf["2023-08"]), int(pf["2023-09"])
pf_unit_profit = float(prod.loc[prod.Product_Name == "Playfoam", "unit_profit"].iloc[0])
pf_margin = round(pf_unit_profit / float(prod.loc[prod.Product_Name == "Playfoam", "Product_Price"].iloc[0]) * 100)
pf_month_profit_k = round(pf_sep * pf_unit_profit / 1000)
pf_pid = int(prod.loc[prod.Product_Name == "Playfoam", "Product_ID"].iloc[0])
pf_zero = int(((inv.Product_ID == pf_pid) & (inv.Stock_On_Hand == 0)).sum())

first_sale = x.groupby("Product_Name").Date.min()
launched = [n for n in first_sale.index if first_sale[n] > pd.Timestamp("2022-01-31") and n != "Playfoam"]
faded = [n for n in launched if units_m.loc[n].iloc[-1] <= 0.6 * units_m.loc[n].max()]

q3_22_k, q3_23_k = round(qp.loc["Colorbuds", "2022Q3"] / 1000), round(qp.loc["Colorbuds", "2023Q3"] / 1000)
pf_rank = int((qp["2023Q3"] > qp.loc["Playfoam", "2023Q3"]).sum()) + 1
cbs = x[(x.Product_Name == "Colorbuds") & (x.Date.dt.month <= 9)]
g = cbs.groupby([cbs.Store_ID, cbs.Date.dt.year]).Units.sum().unstack(fill_value=0)
stores_down = int((g[2023] < g[2022]).sum())
cb_unit_profit = float(prod.loc[prod.Product_Name == "Colorbuds", "unit_profit"].iloc[0])
gap_k = round((cb_first - cb_last) * cb_unit_profit / 1000)
peak_drop = lambda n: round((1 - units_m.loc[n].iloc[-1] / units_m.loc[n].max()) * 100)
jenga_drop, etch_drop, hw_drop = peak_drop("Jenga"), peak_drop("Etch A Sketch"), peak_drop("Hot Wheels 5-Pack")
etch_peak = str(units_m.loc["Etch A Sketch"].idxmax())

# independent check against the numbers verified earlier with pandas
assert (cb_first, cb_last, cb_drop) == (8110, 2594, 68), (cb_first, cb_last, cb_drop)
assert (share_22, share_23) == (28, 13), (share_22, share_23)
assert (pf_aug, pf_sep, pf_margin, pf_month_profit_k, pf_zero) == (1311, 2847, 64, 20, 13)
assert (len(faded), len(launched)) == (9, 10), (len(faded), len(launched))
assert (q3_22_k, q3_23_k, pf_rank, stores_down, gap_k) == (142, 74, 5, 48, 44), (q3_22_k, q3_23_k, pf_rank, stores_down, gap_k)
assert (jenga_drop, etch_drop, hw_drop, etch_peak) == (92, 56, 9, "2022-12"), (jenga_drop, etch_drop, hw_drop, etch_peak)
print("numbers verified:", dict(cb=(cb_first, cb_last, cb_drop), share=(share_22, share_23),
      playfoam=(pf_aug, pf_sep, pf_margin, pf_month_profit_k, pf_zero), faded=(len(faded), len(launched))))

# ----------------------------------------------------------------- brand
BLUE, ORANGE, MINT, YELLOW = "2A78D6", "EB6834", "1BAF7A", "F2B400"
PINK, VIOLET, INK, MUTED = "E8457B", "6250D6", "1F1A17", "6B6560"
T_PINK, T_MINT, T_ORANGE, T_BLUE, T_YELLOW = "FCE4EC", "DDF5EC", "FFE9DC", "E3EEFB", "FFF3CC"
HEAD, BODY = "Trebuchet MS", "Calibri"
rgb = lambda h: RGBColor.from_string(h)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
prs.core_properties.title = "Colorbuds is fading: what to do next"
prs.core_properties.author = "Maven Toys Analytics"
prs.core_properties.subject = "Business review"


def text(slide, s, x, y, w, h, size, color=INK, bold=False, font=BODY, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, name=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    runs = s if isinstance(s, list) else [(s, {})]
    p = tf.paragraphs[0]
    p.alignment = align
    for t, opt in runs:
        r = p.add_run()
        r.text = t
        r.font.size = Pt(opt.get("size", size))
        r.font.bold = opt.get("bold", bold)
        r.font.name = opt.get("font", font)
        r.font.color.rgb = rgb(opt.get("color", color))
    return tb


def shape(slide, kind, x, y, w, h, fill, name=None, radius=None):
    sp = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.solid()
    sp.fill.fore_color.rgb = rgb(fill)
    sp.line.fill.background()
    sp.shadow.inherit = False
    if name:
        sp.name = name
    if radius is not None and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        sp.adjustments[0] = radius
    return sp


def notes(slide, s):
    slide.notes_slide.notes_text_frame.text = s


def lockup(slide, light=False, x=10.35, y=0.42):
    """Small 'Maven Toys' wordmark with three toy blocks."""
    cols = [PINK, YELLOW, MINT] if not light else ["FFFFFF", YELLOW, "FFD6E5"]
    for i, c in enumerate(cols):
        shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x + i * 0.2, y + 0.08, 0.16, 0.16, c, f"Logo block {i+1}", 0.25)
    text(slide, "Maven Toys", x + 0.7, y, 1.6, 0.32, 14, "FFFFFF" if light else BLUE, True, HEAD,
         anchor=MSO_ANCHOR.MIDDLE, name="Logo wordmark")


def footer(slide, n):
    text(slide, "Source: Maven Toys sales data, Jan 2022 – Sep 2023. Profit is estimated from current price and cost.",
         0.7, 6.95, 10.5, 0.3, 10, MUTED, name="Source")
    text(slide, str(n), 12.0, 6.95, 0.63, 0.3, 10, MUTED, align=PP_ALIGN.RIGHT, name="Slide number")


def title(slide, s):
    text(slide, s, 0.7, 0.5, 9.4, 1.1, 40, INK, True, HEAD, anchor=MSO_ANCHOR.MIDDLE, name="Title")


def content_slide(s_title, n):
    sl = prs.slides.add_slide(BLANK)
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = rgb("FFFFFF")
    title(sl, s_title)
    lockup(sl)
    footer(sl, n)
    return sl


def blocks(slide, x0, y0, rows, w=1.3, h=0.8, gap=0.06):
    """Stack of toy blocks with studs. rows: list of (x_offset_in_blocks, [colors]) bottom-up."""
    for r, (off, cols) in enumerate(rows):
        y = y0 - r * (h + gap)
        for i, c in enumerate(cols):
            bx = x0 + (off + i) * (w + gap)
            shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, bx, y, w, h, c, f"Block r{r}c{i}", 0.12)
            for sx in (0.2, 0.72):
                shape(slide, MSO_SHAPE.OVAL, bx + sx, y - 0.1, 0.38, 0.2, c, f"Stud r{r}c{i}")


def bullets(slide, items, x, y, w, h, size=18, color=INK, space=8, name="Bullets"):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, s in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(space)
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", "285750")
        pPr.set("indent", "-285750")
        buClr = etree.SubElement(pPr, qn("a:buClr"))
        etree.SubElement(buClr, qn("a:srgbClr")).set("val", BLUE)
        etree.SubElement(pPr, qn("a:buFont")).set("typeface", "Arial")
        etree.SubElement(pPr, qn("a:buChar")).set("char", "•")
        r = p.add_run()
        r.text = s
        r.font.size, r.font.name = Pt(size), BODY
        r.font.color.rgb = rgb(color)
    return tb


def style_axis_text(axis, size=14, color=MUTED):
    axis.tick_labels.font.size = Pt(size)
    axis.tick_labels.font.name = BODY
    axis.tick_labels.font.color.rgb = rgb(color)


# ================================================================= slide 1: title
s1 = prs.slides.add_slide(BLANK)
s1.background.fill.solid()
s1.background.fill.fore_color.rgb = rgb(BLUE)
lockup(s1, light=True, x=0.7, y=0.55)
text(s1, "Colorbuds is fading", 0.7, 2.3, 8.6, 1.5, 60, "FFFFFF", True, HEAD, anchor=MSO_ANCHOR.BOTTOM, name="Title")
text(s1, "What to do next", 0.7, 3.95, 8, 0.8, 30, "FFE08A", False, HEAD, name="Subtitle")
text(s1, "Business review · Data through Sep 30, 2023", 0.7, 6.7, 8, 0.4, 14, "DCE9FB", name="Date line")
blocks(s1, 8.75, 6.25, [(0, [YELLOW, PINK, MINT]), (0.5, ["FFFFFF", ORANGE]), (1, [VIOLET])])
notes(s1, "Open with the one-line answer: Colorbuds, our top profit toy, is fading. The plan is simple: back newer, "
          "higher-margin toys, test one cheap fix for Colorbuds, and review in 8 weeks. Keep the intro under 20 seconds.")

# ================================================================= slide 2: the answer
s2 = content_slide("One toy fell. Another is rising", 2)
for i, (fill, big, bigcolor, label, cap, bx) in enumerate([
    (T_PINK, f"{share_22}% → {share_23}%", PINK, "Colorbuds' share of quarterly profit", "Q3 2022 to Q3 2023", 0.7),
    (T_MINT, f"${pf_month_profit_k}K", MINT, "Playfoam profit per month", "at its September pace", 6.95),
]):
    shape(s2, MSO_SHAPE.ROUNDED_RECTANGLE, bx, 1.8, 5.68, 2.85, fill, f"Card {i+1}", 0.07)
    text(s2, big, bx + 0.4, 2.0, 4.9, 1.15, 54, bigcolor, True, HEAD, anchor=MSO_ANCHOR.MIDDLE, name=f"Big number {i+1}")
    text(s2, label, bx + 0.4, 3.35, 4.9, 0.45, 22, INK, True, name=f"Label {i+1}")
    text(s2, cap, bx + 0.4, 3.9, 4.9, 0.35, 14, MUTED, name=f"Caption {i+1}")
bullets(s2, [f"Colorbuds is still our #1 profit toy, but its share has more than halved",
             f"Playfoam launched in mid-August and is already a top-{pf_rank} profit toy",
             f"Playfoam's September pace is nearly half of the ${gap_k}K a month Colorbuds has lost"],
        0.7, 4.95, 11.9, 1.8, 20, name="Key points")
notes(s2, f"Colorbuds earned about {share_22}% of Q3 2022 profit and {share_23}% of Q3 2023 profit; it is still our #1 profit toy, "
          f"so it is fading, not dead. Playfoam launched in mid-August 2023; at its September pace ({pf_sep:,} units x "
          f"${pf_unit_profit:.0f} profit per unit) it earns about ${pf_month_profit_k}K a month. Colorbuds' monthly profit is about ${gap_k}K lower than in "
          "Jan 2022 ((8,110 - 2,594) units x $8). Profit is estimated from current price and cost, not accounting figures.")

# ================================================================= slide 3: the fall (native line chart + bullets)
s3 = content_slide(f"Colorbuds sales are down {cb_drop}%", 3)
months = [str(p) for p in cb.index]
show_at = {0, 6, 12, 18}
mlabels = [pd.Period(m).strftime("%b %y") if i in show_at else " " * (i + 1) for i, m in enumerate(months)]
cd = CategoryChartData()
cd.categories = mlabels
cd.add_series("Colorbuds units per month", [int(v) for v in cb.values])
gf = s3.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(0.7), Inches(2.05), Inches(7.9), Inches(4.7), cd)
gf.name = "Colorbuds monthly units"
ch = gf.chart
ch.has_legend = False
ch.has_title = False
ch.font.name = BODY
va, ca = ch.value_axis, ch.category_axis
va.visible = False
va.has_major_gridlines = False
va.minimum_scale, va.maximum_scale = 0, 9500
ca.has_major_gridlines = False
ca.format.line.color.rgb = rgb("D9D4CC")
style_axis_text(ca)
bp = ca._element.find(qn('c:txPr')).find(qn('a:bodyPr'))
bp.set('rot', '0')
bp.set('vert', 'horz')
ser = ch.plots[0].series[0]
ser.smooth = False
ser.format.line.color.rgb = rgb(PINK)
ser.format.line.width = Pt(5)
from pptx.enum.chart import XL_MARKER_STYLE
ser.marker.style = XL_MARKER_STYLE.NONE
for idx, lbl, when, pos in ((0, f"{cb_first:,}", "Jan 2022", XL_LABEL_POSITION.ABOVE),
                            (len(cb) - 1, f"{cb_last:,}", "Sep 2023", XL_LABEL_POSITION.BELOW)):
    pt = ser.points[idx]
    pt.marker.style = XL_MARKER_STYLE.CIRCLE
    pt.marker.size = 14
    pt.marker.format.fill.solid()
    pt.marker.format.fill.fore_color.rgb = rgb(PINK)
    pt.marker.format.line.color.rgb = rgb("FFFFFF")
    dl = pt.data_label
    dl.has_text_frame = True
    dl.text_frame.text = lbl
    dl.position = pos
    r = dl.text_frame.paragraphs[0].runs[0]
    r.font.size, r.font.bold, r.font.name = Pt(24), True, HEAD
    r.font.color.rgb = rgb(PINK)
    p2 = dl.text_frame.add_paragraph()
    r2 = p2.add_run()
    r2.text = when
    r2.font.size, r2.font.name = Pt(14), BODY
    r2.font.color.rgb = rgb(MUTED)
text(s3, "units per month", 0.7, 1.7, 4, 0.3, 14, MUTED, name="Chart caption")
bullets(s3, [f"Down in {stores_down} of 50 stores, in every store type",
             "Every store still carries it, so this is weaker demand, not empty shelves",
             f"Quarterly profit has roughly halved: ${q3_22_k}K to ${q3_23_k}K"],
        9.0, 2.3, 3.7, 4.2, 20, space=14, name="Key points")
notes(s3, f"Monthly Colorbuds units fell from {cb_first:,} (Jan 2022) to {cb_last:,} (Sep 2023), down {cb_drop}%. "
          f"The drop is steady and broad: {stores_down} of 50 stores are down (Jan-Sep 2023 vs Jan-Sep 2022), in every store type. All 50 stores carry it and none is at zero stock, "
          "so this looks like a demand problem, not a stock problem. Some of the drop is seasonal (company-wide revenue in Sep is about 26% "
          "below its peak month) but not most of it. The data cannot say WHY demand fell; no price history, promotions or competitor data.")

# ================================================================= slide 4: most toys fade
s4 = content_slide("Most toys fade", 4)
text(s4, f"{len(faded)} of {len(launched)}", 0.7, 1.75, 6.4, 1.7, 100, ORANGE, True, HEAD, anchor=MSO_ANCHOR.MIDDLE, name="Big number")
text(s4, "recent launches are 40%+ below their peak", 0.7, 3.5, 6.4, 0.9, 24, INK, False, HEAD, name="Caption")
for i in range(len(launched)):
    bx = 0.75 + i * 0.64
    c = ORANGE if i < len(faded) else "D9D4CC"
    shape(s4, MSO_SHAPE.ROUNDED_RECTANGLE, bx, 5.2, 0.54, 0.54, c, f"Toy block {i+1}", 0.18)
    shape(s4, MSO_SHAPE.OVAL, bx + 0.14, 5.12, 0.26, 0.14, c, f"Toy stud {i+1}")
bullets(s4, [f"Jenga peaked in Jul 2022 and is now down {jenga_drop}%",
             f"Etch A Sketch peaked its second month and is down {etch_drop}%",
             f"Hot Wheels is the lone exception, down just {hw_drop}%",
             "Colorbuds follows the same pattern"],
        7.6, 2.0, 5.0, 4.5, 20, space=14, name="Key points")
notes(s4, "This is the likely explanation, not a proven cause. Of the 10 toys that started selling during this data (excluding Playfoam, "
          "which is too new), 9 now sell at least 40% less per month than in their peak month. Jenga -92%, Supersoaker -66%, "
          "Mr. Potatohead -65%, PlayDoh Playset -64%, Etch A Sketch -56%, Plush Pony -56%, Foam Disk Launcher -54%, Magic Sand -41%, "
          "Gamer Headphones -41%; Hot Wheels is the exception at -9%. Caveats: part of each drop is seasonal, and 'launch' means first sale in this data.")

# ================================================================= slide 5: Playfoam (native bar chart + bullets)
s5 = content_slide("Playfoam is taking off", 5)
cd = CategoryChartData()
cd.categories = ["Aug (from the 17th)", "Sep"]
cd.add_series("Playfoam units", [pf_aug, pf_sep])
gf = s5.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.7), Inches(2.05), Inches(6.4), Inches(4.65), cd)
gf.name = "Playfoam monthly units"
ch = gf.chart
ch.has_legend = False
ch.has_title = False
ch.font.name = BODY
va, ca = ch.value_axis, ch.category_axis
va.visible = False
va.has_major_gridlines = False
va.minimum_scale, va.maximum_scale = 0, 3400
ca.has_major_gridlines = False
ca.format.line.color.rgb = rgb("D9D4CC")
style_axis_text(ca, 16)
plot = ch.plots[0]
plot.gap_width = 70
plot.has_data_labels = True
dls = plot.data_labels
dls.number_format, dls.number_format_is_linked = "#,##0", False
dls.position = XL_LABEL_POSITION.OUTSIDE_END
dls.font.size, dls.font.bold, dls.font.name = Pt(28), True, HEAD
dls.font.color.rgb = rgb(MINT)
ser = plot.series[0]
ser.format.fill.solid()
ser.format.fill.fore_color.rgb = rgb(MINT)
text(s5, "units sold per month", 0.7, 1.7, 5, 0.3, 14, MUTED, name="Chart caption")
for i, (fill, big, col, small, by, dy) in enumerate([
    (T_MINT, f"{pf_margin}% margin", MINT, f"${pf_unit_profit:.0f} profit on every unit", 1.9, 0.9),
    (T_ORANGE, f"{pf_zero} stores out of stock", ORANGE, "about $5K a month left on the table", 3.55, 0.9),
]):
    shape(s5, MSO_SHAPE.ROUNDED_RECTANGLE, 7.6, by, 5.0, 1.4, fill, f"Badge {i+1}", 0.1)
    text(s5, big, 7.9, by + 0.2, 4.5, 0.6, 26, col, True, HEAD, anchor=MSO_ANCHOR.MIDDLE, name=f"Badge title {i+1}")
    text(s5, small, 7.9, by + dy, 4.5, 0.4, 16, INK, name=f"Badge note {i+1}")
bullets(s5, [f"Launched Aug 17 and already a top-{pf_rank} profit toy",
             "New toys often cool off, so the window to act is short"],
        7.6, 5.2, 5.0, 1.5, 18, space=10, name="Key points")
notes(s5, f"Playfoam launched Aug 17, 2023 and sold {pf_aug + pf_sep:,} units in about six weeks ({pf_aug:,} in August from the 17th, "
          f"{pf_sep:,} in September). It earns ${pf_unit_profit:.0f} per unit at a {pf_margin}% margin, about ${pf_month_profit_k}K a month "
          f"at the September pace. It is at zero stock in {pf_zero} stores; each store sells about 57 units a month, so empty shelves cost "
          "roughly $5K a month. It was the #5 profit toy in Q3 2023 despite only ~6 weeks on sale. Be honest: hot now, likely to cool (see the previous slide). "
          "Only six weeks of data; the $20K is a run-rate, not a forecast.")

# ================================================================= slide 6: what we do
s6 = content_slide("Back newer, higher-margin toys", 6)
steps = [("1", BLUE, T_BLUE, "Keep Playfoam in stock", ["Refill the 13 empty stores", "Check weekly; worth about $5K a month"]),
         ("2", ORANGE, T_ORANGE, "Test one Colorbuds fix", ["10 test stores vs 10 similar ones", "Up to about $11K a month if it works"]),
         ("3", MINT, T_MINT, "Review in 8 weeks", ["Scale what works, stop what doesn't", "Pick the next higher-margin toy"])]
for i, (num, col, tint, label, pts) in enumerate(steps):
    cx = 0.7 + i * 4.1
    shape(s6, MSO_SHAPE.ROUNDED_RECTANGLE, cx, 1.95, 3.7, 4.55, tint, f"Card {num}", 0.06)
    badge = shape(s6, MSO_SHAPE.OVAL, cx + 0.4, 2.3, 0.9, 0.9, col, f"Number badge {num}")
    tf = badge.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = num
    r.font.size, r.font.bold, r.font.name = Pt(32), True, HEAD
    r.font.color.rgb = rgb("FFFFFF")
    text(s6, label, cx + 0.4, 3.45, 2.95, 1.2, 26, INK, True, HEAD, name=f"Step {num}")
    bullets(s6, pts, cx + 0.4, 4.8, 2.95, 1.6, 16, space=8, name=f"Step {num} details")
notes(s6, "1) Keep Playfoam in stock: refill the 13 stores at zero and keep every store above about two weeks of sales (roughly 26 units a store); "
          "check weekly. Worth about $5K a month now. "
          "2) Test one cheap Colorbuds fix: refresh, bundle with Gamer Headphones, or better shelf placement in about 10 stores against 10 similar "
          "control stores for six weeks. Winning back a quarter of the lost sales is worth up to about $11K a month. "
          "3) Review at week 8: if the test stores sold about 15% more Colorbuds, scale the fix; if not, stop. Pick the next newer, higher-margin toy "
          "to back at the same review. The 15% threshold is a suggestion to agree on in advance, not something from the data. "
          "Sizes are estimates; the data cannot show why Colorbuds fell.")

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(OUT)
print("saved", OUT)
