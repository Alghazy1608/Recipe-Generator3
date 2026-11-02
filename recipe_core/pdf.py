"""Create a printable recipe PDF in a standard recipe layout."""
from __future__ import annotations

import io
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .models import Recipe, RecipeImage
from .safety import health_flags

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
GREEN = colors.HexColor("#2F6B4F")
PALE = colors.HexColor("#EEF2EC")
INK = colors.HexColor("#22302A")
MUTED = colors.HexColor("#5F6B65")
RED = colors.HexColor("#A33A2C")
PALE_RED = colors.HexColor("#FBEDEA")
WIDTH = A4[0] - 36 * mm - 12  # Page width less margins and the 6 pt frame padding on each side.


def _fonts():
    pdfmetrics.registerFont(TTFont("Recipe", FONT_DIR / "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("Recipe-Bold", FONT_DIR / "DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Recipe-Italic", FONT_DIR / "DejaVuSans-Oblique.ttf"))
    pdfmetrics.registerFontFamily("Recipe", normal="Recipe", bold="Recipe-Bold", italic="Recipe-Italic", boldItalic="Recipe-Bold")


def _styles():
    base = ParagraphStyle("body", fontName="Recipe", fontSize=9.5, leading=13.5, textColor=INK)
    return {
        "body": base,
        "title": ParagraphStyle("title", parent=base, fontName="Recipe-Bold", fontSize=23, leading=28, textColor=GREEN, spaceAfter=4),
        "intro": ParagraphStyle("intro", parent=base, fontName="Recipe-Italic", fontSize=10.5, leading=15, textColor=MUTED, spaceAfter=7),
        "h2": ParagraphStyle("h2", parent=base, fontName="Recipe-Bold", fontSize=12.5, leading=16, textColor=GREEN, spaceBefore=10, spaceAfter=5),
        "small": ParagraphStyle("small", parent=base, fontSize=7.5, leading=10, textColor=MUTED),
        "cap": ParagraphStyle("cap", parent=base, fontSize=7, leading=9, textColor=MUTED, alignment=TA_CENTER),
        "stat": ParagraphStyle("stat", parent=base, fontName="Recipe-Bold", fontSize=10.5, leading=13, alignment=TA_CENTER),
        "statlabel": ParagraphStyle("statlabel", parent=base, fontSize=7, leading=9, textColor=MUTED, alignment=TA_CENTER),
        "warn": ParagraphStyle("warn", parent=base, fontSize=8.5, leading=12, textColor=RED),
    }


def _p(text, style):
    return Paragraph(escape(str(text)), style)


def _picture(img: RecipeImage, width, height):
    """Centre-crop a photo to the box so it is never stretched."""
    source = PILImage.open(io.BytesIO(img.data)).convert("RGB")
    target = width / height
    ratio = source.width / source.height
    if ratio > target:
        keep = int(source.height * target)
        left = (source.width - keep) // 2
        source = source.crop((left, 0, left + keep, source.height))
    else:
        keep = int(source.width / target)
        top = (source.height - keep) // 2
        source = source.crop((0, top, source.width, top + keep))
    out = io.BytesIO()
    source.save(out, "JPEG", quality=85)
    out.seek(0)
    return Image(out, width=width, height=height)


def _boxed(flowables, background, border):
    table = Table([[flowables]], colWidths=[WIDTH])
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), background), ("BOX", (0, 0), (-1, -1), 0.7, border),
                               ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                               ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return table


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Recipe", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 10 * mm, doc.title[:80])
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def build_recipe_pdf(recipe: Recipe, images: list[RecipeImage] | None = None, allergens: list[str] | None = None,
                     notes: list[str] | None = None) -> bytes:
    _fonts()
    s = _styles()
    images = images or []
    allergens = allergens or []
    story = [_p(recipe.title, s["title"]), _p(recipe.description, s["intro"])]

    dish = next((img for img in images if img.is_dish), None)
    thumbs = [img for img in images if img is not dish][:3]
    if dish:
        story += [_picture(dish, WIDTH, WIDTH * 0.42), Spacer(1, 2),
                  _p("Similar dish for illustration. Your result may look different.", s["cap"]), Spacer(1, 6)]

    stats = [("Serves", recipe.servings), ("Prep", f"{recipe.prep_minutes} min"), ("Cook", f"{recipe.cook_minutes} min"),
             ("Total", f"{recipe.total_minutes} min"), ("Level", recipe.difficulty),
             ("Calories", f"{recipe.nutrition.calories_per_serving:.0f} kcal")]
    bar = Table([[_p(v, s["stat"]) for _, v in stats], [_p(k, s["statlabel"]) for k, _ in stats]], colWidths=[WIDTH / 6] * 6)
    bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE), ("TOPPADDING", (0, 0), (-1, 0), 6),
                             ("BOTTOMPADDING", (0, 0), (-1, 0), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 6),
                             ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story += [bar, Spacer(1, 6)]

    if allergens:
        story.append(_boxed([_p("Allergens you asked to avoid: " + ", ".join(allergens) +
                                ". Automatic checks found none in this recipe, but always read product labels "
                                "and check for cross-contamination.", s["warn"])], PALE_RED, RED))
    elif recipe.allergens_present:
        story.append(_boxed([_p("Contains or may contain: " + ", ".join(recipe.allergens_present) + ".", s["warn"])], PALE_RED, RED))

    if notes:
        story += [Spacer(1, 4), _boxed([_p(note, s["warn"]) for note in notes], PALE_RED, RED)]

    ingredient_rows = [[_p(i.amount or "-", s["body"]), _p(i.name + (f" ({i.healthy_note})" if i.healthy_note else ""), s["body"])]
                       for i in recipe.ingredients]
    ingredient_table = Table(ingredient_rows, colWidths=[WIDTH * 0.2, WIDTH * 0.8], splitByRow=1)
    ingredient_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, PALE),
                                          ("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                                          ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    story += [_p("Ingredients", s["h2"]), ingredient_table,
              KeepTogether([_p("Utensils", s["h2"]), _p(", ".join(recipe.utensils) or "None listed", s["body"])]),
              _p("Method", s["h2"])]

    step_rows = [[_p(n, ParagraphStyle("n", parent=s["body"], fontName="Recipe-Bold", textColor=GREEN)), _p(step, s["body"])]
                 for n, step in enumerate(recipe.steps, 1)]
    steps = Table(step_rows, colWidths=[9 * mm, WIDTH - 9 * mm])
    steps.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5)]))
    story.append(steps)

    n = recipe.nutrition
    facts = [("Calories", f"{n.calories_per_serving:.0f} kcal"), ("Protein", f"{n.protein_g:.0f} g"), ("Carbs", f"{n.carbs_g:.0f} g"),
             ("Fat", f"{n.fat_g:.0f} g"), ("Sat. fat", f"{n.saturated_fat_g:.0f} g"), ("Sugar", f"{n.sugar_g:.0f} g"),
             ("Fibre", f"{n.fibre_g:.0f} g"), ("Sodium", f"{n.sodium_mg:.0f} mg")]
    nutrition = Table([[_p(k, s["statlabel"]) for k, _ in facts], [_p(v, s["stat"]) for _, v in facts]], colWidths=[WIDTH / 8] * 8)
    nutrition.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, GREEN), ("INNERGRID", (0, 0), (-1, -1), 0.25, PALE),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    block = [_p("Nutrition per serving (estimated)", s["h2"]), nutrition, Spacer(1, 3),
             _p(f"Whole recipe: about {recipe.total_calories:.0f} kcal for {recipe.servings} serving(s). " +
                ("AI estimates. " if recipe.origin == "ai" else "Estimated from a built-in food table. ") + "Figures vary with brands and portions.", s["small"])]
    block += [_p(flag, s["warn"]) for flag in health_flags(recipe)]
    story.append(KeepTogether(block))

    for heading, items in (("Why this is a healthy choice", recipe.healthy_choices), ("Add-on suggestions", recipe.add_on_suggestions)):
        if items:
            story.append(KeepTogether([_p(heading, s["h2"])] + [Paragraph("• " + escape(i), s["body"]) for i in items]))

    if thumbs:
        cell = (WIDTH - 8 * mm) / 3
        pictures = [_picture(t, cell, cell * 0.68) for t in thumbs] + [""] * (3 - len(thumbs))
        labels = [_p(t.label.title(), s["cap"]) for t in thumbs] + [""] * (3 - len(thumbs))
        grid = Table([pictures, labels], colWidths=[WIDTH / 3] * 3)
        grid.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
        story.append(KeepTogether([_p("Key ingredients", s["h2"]), grid]))

    if images:
        credits = [_p("Image credits", ParagraphStyle("c", parent=s["small"], fontName="Recipe-Bold", spaceBefore=9))]
        credits += [_p(f"{img.label.title()}: {img.credit}. {img.source_url}", s["small"]) for img in images]
        story.append(KeepTogether(credits))

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm, bottomMargin=17 * mm,
                            title=recipe.title, author="Healthy Recipe Generator")
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buffer.getvalue()
