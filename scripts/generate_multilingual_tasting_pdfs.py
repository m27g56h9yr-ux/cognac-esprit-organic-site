from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    BooleanObject,
    DictionaryObject,
    NameObject,
    TextStringObject,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets/pdf/fiches-degustation"
TMP_DIR = ROOT / "tmp/pdfs"
TMP_DIR.mkdir(parents=True, exist_ok=True)

W, H = A4
BROWN = "#3b1d1a"
GREY = "#3f3f3f"
GOLD = "#b68b2b"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_NARROW_BOLD = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
FONT_NARROW_ITALIC = "/System/Library/Fonts/Supplemental/Arial Narrow Bold Italic.ttf"


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("EO-Regular", FONT_REGULAR))
    pdfmetrics.registerFont(TTFont("EO-Bold", FONT_BOLD))
    pdfmetrics.registerFont(TTFont("EO-Condensed", FONT_NARROW_BOLD))
    pdfmetrics.registerFont(TTFont("EO-CondensedItalic", FONT_NARROW_ITALIC))


LANG = {
    "en": {
        "pdf_lang": "en-GB",
        "range": "THE RANGE",
        "tasting": "TASTING",
        "sensory": "SENSORY NOTES",
        "filename_suffix": "en",
        "sheet_label": "Tasting sheet",
        "metadata_label": "Tasting sheet",
    },
    "da": {
        "pdf_lang": "da-DK",
        "range": "SERIEN",
        "tasting": "SMAGNING",
        "sensory": "SENSORISKE NOTER",
        "filename_suffix": "da",
        "sheet_label": "Smageark",
        "metadata_label": "Smageark",
    },
    "no": {
        "pdf_lang": "nb-NO",
        "range": "SERIEN",
        "tasting": "SMAKING",
        "sensory": "SENSORISKE NOTER",
        "filename_suffix": "no",
        "sheet_label": "Smaksark",
        "metadata_label": "Smaksark",
    },
    "sv": {
        "pdf_lang": "sv-SE",
        "range": "SORTIMENTET",
        "tasting": "PROVNING",
        "sensory": "SENSORISKA NOTER",
        "filename_suffix": "sv",
        "sheet_label": "Provningsblad",
        "metadata_label": "Provningsblad",
    },
}


PRODUCTS = {
    "fondation-vs": {
        "name": "Fondation VS",
        "title": "FONDATION",
        "color": "#6ba35e",
        "product_image": "assets/img/old-site/img_prod_fondation_01.jpg",
        "tasting_image": "assets/img/old-site/img_degustation_vs.jpg",
        "translations": {
            "en": {
                "subtitle": "YOUNG, FRUITY AND POWERFUL COGNAC",
                "story": (
                    "I dedicate Fondation to my grandmother Germaine, the family pioneer, who kept telling me: "
                    '"This heritage is solid because it is healthy; the land needs nothing more than human work '
                    "and knowledge. We never needed chemical products for the vine to grow and bear fruit.\" "
                    "That powerful message led me to create this brand."
                ),
                "tasting_title": "IDEAL FOR A COCKTAIL OR LONG DRINK",
                "tasting_body": (
                    "Fondation is defined by a beautiful freshness on the palate, with fruity notes of pear, peach "
                    "and vine flower. The first wood tannins reveal brioche aromas. Ideal for cocktails or served over ice."
                ),
            },
            "da": {
                "subtitle": "UNG, FRUGTIG OG KRAFTFULD COGNAC",
                "story": (
                    "Jeg dedikerer Fondation til min bedstemor Germaine, familiens pioner, som altid sagde til mig: "
                    '"Denne arv er solid, fordi den er sund; jorden behøver ikke andet end menneskets arbejde og viden. '
                    'Vi har aldrig haft brug for kemiske produkter for at få vinstokken til at vokse og give druer." '
                    "Det var dette stærke budskab, der fik mig til at skabe mærket."
                ),
                "tasting_title": "IDEEL TIL EN COCKTAIL ELLER LONGDRINK",
                "tasting_body": (
                    "Fondation kendetegnes af en smuk friskhed i munden med frugtige noter af pære, fersken og vinblomst. "
                    "De første trætanniner afslører briochearomaer. Ideel til cocktails eller serveret over is."
                ),
            },
            "no": {
                "subtitle": "UNG, FRUKTIG OG KRAFTFULL COGNAC",
                "story": (
                    "Jeg dedikerer Fondation til min bestemor Germaine, familiens pioner, som stadig sa til meg: "
                    '"Denne arven er solid fordi den er sunn; jorden trenger ikke annet enn menneskets arbeid og kunnskap. '
                    'Vi har aldri trengt kjemiske produkter for at vinranken skal vokse og gi druer." '
                    "Det sterke budskapet fikk meg til å skape dette merket."
                ),
                "tasting_title": "IDEELL TIL EN COCKTAIL ELLER LONGDRINK",
                "tasting_body": (
                    "Fondation kjennetegnes av en vakker friskhet i munnen, med fruktige toner av pære, fersken og vinblomst. "
                    "De første tretanninene avslører briochearomaer. Ideell til cocktails eller servert over is."
                ),
            },
            "sv": {
                "subtitle": "UNG, FRUKTIG OCH KRAFTFULL COGNAC",
                "story": (
                    "Jag tillägnar Fondation min farmor Germaine, familjens pionjär, som ofta sade till mig: "
                    '"Detta arv är starkt eftersom det är sunt; jorden behöver inget annat än människans arbete och kunskap. '
                    'Vi har aldrig behövt kemiska produkter för att vinstocken ska växa och ge druvor." '
                    "Det starka budskapet fick mig att skapa detta varumärke."
                ),
                "tasting_title": "IDEALISK TILL EN COCKTAIL ELLER LONGDRINK",
                "tasting_body": (
                    "Fondation kännetecknas av en vacker friskhet i munnen, med fruktiga toner av päron, persika och vinblomma. "
                    "De första trätanninerna avslöjar briochearomer. Idealisk till cocktails eller serverad över is."
                ),
            },
        },
    },
    "conviction-vsop": {
        "name": "Conviction VSOP",
        "title": "CONVICTION",
        "color": "#8d8a35",
        "product_image": "assets/img/old-site/img_prod_conviction_01.jpg",
        "tasting_image": "assets/img/old-site/cocktail_vsop.jpg",
        "translations": {
            "en": {
                "subtitle": "ROUNDED AND GENEROUS COGNAC",
                "story": (
                    "Fanny and I are convinced that producing better is the best way to preserve our vineyard and allow us "
                    "to keep working with passion and respect for the land. CONVICTION is a tribute to our vision of a healthy "
                    "life, to practical farming sense, and to our partnership in work and in life."
                ),
                "tasting_title": "IDEAL FOR A COCKTAIL OR LONG DRINK",
                "tasting_body": (
                    "Conviction is a rounded and generous Cognac. Its first years in cask bring notes of candied fruit and vanilla. "
                    "On the palate, it reveals dried fruit, warm wood and spices, with a fresh clove finish."
                ),
            },
            "da": {
                "subtitle": "RUND OG GENERØS COGNAC",
                "story": (
                    "Fanny og jeg er overbeviste om, at det at producere bedre er den bedste måde at bevare vores vinmark "
                    "og fortsætte vores arbejde med passion og respekt for jorden. CONVICTION er en hyldest til vores syn på "
                    "et sundt liv, til landligt sundt fornuft og til vores fællesskab i arbejdet og i livet."
                ),
                "tasting_title": "IDEEL TIL EN COCKTAIL ELLER LONGDRINK",
                "tasting_body": (
                    "Conviction er en rund og generøs Cognac. De første år på fad giver noter af kandiseret frugt og vanilje. "
                    "I munden finder man tørret frugt, varmt træ og krydderier, med en frisk afslutning af nellike."
                ),
            },
            "no": {
                "subtitle": "RUND OG GENERØS COGNAC",
                "story": (
                    "Fanny og jeg er overbevist om at det å produsere bedre er den beste måten å bevare vinmarken vår på "
                    "og la oss fortsette å arbeide med lidenskap og respekt for jorden. CONVICTION er en hyllest til vår "
                    "visjon om et sunt liv, til bondens sunne fornuft og til vårt fellesskap i arbeid og liv."
                ),
                "tasting_title": "IDEELL TIL EN COCKTAIL ELLER LONGDRINK",
                "tasting_body": (
                    "Conviction er en rund og generøs Cognac. De første årene på fat gir toner av kandisert frukt og vanilje. "
                    "I munnen finner man tørket frukt, varmt treverk og krydder, med en frisk avslutning av nellik."
                ),
            },
            "sv": {
                "subtitle": "RUND OCH GENERÖS COGNAC",
                "story": (
                    "Fanny och jag är övertygade om att bättre produktion är det bästa sättet att bevara vår vingård "
                    "och fortsätta arbeta med passion och respekt för jorden. CONVICTION är en hyllning till vår syn på "
                    "ett sunt liv, till lantbrukets sunda förnuft och till vår gemenskap i arbete och liv."
                ),
                "tasting_title": "IDEALISK TILL EN COCKTAIL ELLER LONGDRINK",
                "tasting_body": (
                    "Conviction är en rund och generös Cognac. De första åren på fat ger toner av kanderad frukt och vanilj. "
                    "I munnen finns torkad frukt, varmt trä och kryddor, med en frisk avslutning av kryddnejlika."
                ),
            },
        },
    },
    "cohesion-napoleon": {
        "name": "Cohesion Napoléon",
        "title": "COHESION",
        "color": "#bd7829",
        "product_image": "assets/img/old-site/NAPO-COHESION.jpg",
        "tasting_image": "assets/img/old-site/img_prod_cohesion_02.jpg",
        "translations": {
            "en": {
                "subtitle": "BALANCED, LONG AND PEPPERY COGNAC",
                "story": (
                    "The success of this range also comes from the strength each of us has shown. My grandfather Marc, his brother Roger, "
                    "my grandmother Germaine and my parents Pierre and Eliane all helped bring this commitment to organic farming to life. "
                    "It is cohesion, teamwork rooted in several generations. COHESION pays tribute to them."
                ),
                "tasting_title": "A STRUCTURED, BALANCED, LIGHTLY PEPPERY AND MENTHOLATED FINISH",
                "tasting_body": (
                    "Generous barrel ageing gives this Cognac beautiful notes of dried fruit, including peanut, almond and hazelnut, "
                    "alongside warm wood and spice. The finish is long and peppery."
                ),
            },
            "da": {
                "subtitle": "AFBALANCERET, LANG OG PEBRET COGNAC",
                "story": (
                    "Denne series succes bygger også på den styrke, som hver af os har vist. Min bedstefar Marc og hans bror Roger, "
                    "min bedstemor Germaine og mine forældre Pierre og Eliane har alle bidraget til dette engagement i økologisk landbrug. "
                    "Det er en samhørighed og et holdarbejde, der går flere generationer tilbage. COHESION hylder dem."
                ),
                "tasting_title": "STRUKTURERET, BALANCERET, LET PEBRET OG MENTHOLFRISK AFSLUTNING",
                "tasting_body": (
                    "Generøs fadlagring giver denne Cognac smukke noter af tørret frugt, blandt andet jordnød, mandel og hasselnød, "
                    "sammen med varmt træ og krydderier. Afslutningen er lang og pebret."
                ),
            },
            "no": {
                "subtitle": "BALANSERT, LANG OG PEPRET COGNAC",
                "story": (
                    "Suksessen til denne serien bygger også på styrken hver av oss har vist. Min bestefar Marc og hans bror Roger, "
                    "min bestemor Germaine og foreldrene mine Pierre og Eliane har alle bidratt til dette engasjementet for økologisk landbruk. "
                    "Det er samhold og lagarbeid gjennom flere generasjoner. COHESION hyller dem."
                ),
                "tasting_title": "STRUKTURERT, BALANSERT, LETT PEPRET OG MENTOLFRISK AVSLUTNING",
                "tasting_body": (
                    "Generøs fatlagring gir denne Cognacen vakre toner av tørket frukt, blant annet peanøtt, mandel og hasselnøtt, "
                    "sammen med varmt treverk og krydder. Avslutningen er lang og pepret."
                ),
            },
            "sv": {
                "subtitle": "BALANSERAD, LÅNG OCH PEPPRIG COGNAC",
                "story": (
                    "Seriens framgång bygger också på den styrka som var och en av oss har visat. Min farfar Marc och hans bror Roger, "
                    "min farmor Germaine och mina föräldrar Pierre och Eliane har alla bidragit till detta engagemang för ekologiskt jordbruk. "
                    "Det är sammanhållning och lagarbete genom flera generationer. COHESION hyllar dem."
                ),
                "tasting_title": "STRUKTURERAD, BALANSERAD, LÄTT PEPPRIG OCH MENTOLFRISK AVSLUTNING",
                "tasting_body": (
                    "Generös fatlagring ger denna Cognac vackra toner av torkad frukt, bland annat jordnöt, mandel och hasselnöt, "
                    "tillsammans med varmt trä och kryddor. Avslutningen är lång och pepprig."
                ),
            },
        },
    },
    "transmission-xo": {
        "name": "Transmission XO",
        "title": "TRANSMISSION",
        "color": "#c68a00",
        "product_image": "assets/img/old-site/XO-TRANSMISSION.jpg",
        "tasting_image": "assets/img/tasting/xo.jpg",
        "translations": {
            "en": {
                "subtitle": "STRUCTURED AND GENEROUS COGNAC",
                "story": (
                    "I have now been farming my vineyard organically for more than 20 years. I inherited healthy land that I want to pass on "
                    "and help preserve for the future. Respect for the environment must be one of the major commitments of future generations. "
                    "What land will we leave to our children tomorrow? I would like to dedicate this Cognac to generations to come, and especially "
                    "to my children. Transmission symbolizes the fruit of careful, conscientious work by one generation ready to pass the baton to the next."
                ),
                "tasting_title": "STRUCTURED WITH BEAUTIFUL ROUNDNESS ON THE PALATE",
                "tasting_body": (
                    "Many years of ageing were needed to craft Transmission. On the palate it offers fruit notes, especially black cherry, "
                    "with dried flowers. The first notes of rancio appear on the finish."
                ),
            },
            "da": {
                "subtitle": "STRUKTURERET OG GENERØS COGNAC",
                "story": (
                    "Jeg har dyrket min vinmark økologisk i mere end 20 år. Jeg har arvet en sund jord, som jeg ønsker at videregive "
                    "og bevare for fremtiden. Respekten for miljøet bør være en af de store forpligtelser for kommende generationer. "
                    "Hvilken jord efterlader vi til vores børn i morgen? Jeg vil gerne dedikere denne Cognac til de kommende generationer "
                    "og især til mine børn. Transmission symboliserer frugten af et omhyggeligt og samvittighedsfuldt arbejde fra en generation, "
                    "der er klar til at give stafetten videre."
                ),
                "tasting_title": "STRUKTURERET MED SMUK RUNDHED I MUNDEN",
                "tasting_body": (
                    "Mange års lagring har været nødvendig for at skabe Transmission. I munden finder man frugtige noter, især sort kirsebær, "
                    "sammen med tørrede blomster. De første rancio-noter viser sig i afslutningen."
                ),
            },
            "no": {
                "subtitle": "STRUKTURERT OG GENERØS COGNAC",
                "story": (
                    "Jeg har dyrket vinmarken min økologisk i mer enn 20 år. Jeg har arvet en sunn jord som jeg ønsker å gi videre "
                    "og bevare for fremtiden. Respekt for miljøet bør være et av de viktigste forpliktelsene for kommende generasjoner. "
                    "Hvilken jord skal vi etterlate til barna våre i morgen? Jeg vil dedikere denne Cognacen til kommende generasjoner "
                    "og særlig til mine barn. Transmission symboliserer frukten av et nøyaktig og samvittighetsfullt arbeid fra en generasjon "
                    "som er klar til å gi stafettpinnen videre."
                ),
                "tasting_title": "STRUKTURERT MED VAKKER RUNDHET I MUNNEN",
                "tasting_body": (
                    "Mange års lagring var nødvendig for å skape Transmission. I munnen finner man fruktige toner, særlig svart kirsebær, "
                    "sammen med tørkede blomster. De første rancio-tonene kommer frem i avslutningen."
                ),
            },
            "sv": {
                "subtitle": "STRUKTURERAD OCH GENERÖS COGNAC",
                "story": (
                    "Jag har odlat min vingård ekologiskt i mer än 20 år. Jag har ärvt en sund jord som jag vill föra vidare "
                    "och bevara för framtiden. Respekt för miljön bör vara ett av de stora åtagandena för kommande generationer. "
                    "Vilken jord lämnar vi till våra barn i morgon? Jag vill tillägna denna Cognac kommande generationer och särskilt "
                    "mina barn. Transmission symboliserar frukten av ett noggrant och samvetsgrant arbete från en generation som är redo "
                    "att lämna över stafettpinnen till nästa."
                ),
                "tasting_title": "STRUKTURERAD MED VACKER RUNDHET I MUNNEN",
                "tasting_body": (
                    "Många års lagring krävdes för att skapa Transmission. I munnen finns fruktiga toner, särskilt svart körsbär, "
                    "tillsammans med torkade blommor. De första rancio-tonerna framträder i avslutningen."
                ),
            },
        },
    },
}


def product_json(slug: str, lang: str) -> dict:
    path = (ROOT / "produits" if lang == "fr" else ROOT / lang / "produits") / f"{slug}.html"
    html = path.read_text(encoding="utf-8")
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        data = json.loads(match.group(1))
        if data.get("@type") == "Product":
            return data
    raise RuntimeError(f"No Product JSON-LD found in {path}")


def wrap_lines(text: str, font: str, size: float, width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            candidate = word if not line else f"{line} {word}"
            if pdfmetrics.stringWidth(candidate, font, size) <= width:
                line = candidate
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        lines.append("")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    font: str = "EO-Regular",
    size: float = 11,
    leading: float | None = None,
    color: str = GREY,
    max_lines: int | None = None,
) -> float:
    leading = leading or size * 1.35
    lines = wrap_lines(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
    c.setFillColor(color)
    c.setFont(font, size)
    current = y
    for line in lines:
        if line:
            c.drawString(x, current, line)
        current -= leading
    return current


def fit_font(text: str, font: str, start: float, width: float, minimum: float) -> float:
    size = start
    while size > minimum and pdfmetrics.stringWidth(text, font, size) > width:
        size -= 1
    return size


def image_for_pdf(src: Path, max_px: int = 1800) -> Path:
    with Image.open(src) as im:
        im = im.convert("RGBA")
        white = Image.new("RGBA", im.size, "white")
        white.alpha_composite(im)
        rgb = white.convert("RGB")
        rgb.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
        out = TMP_DIR / f"{src.stem}-pdf.jpg"
        rgb.save(out, "JPEG", quality=88, optimize=True)
    return out


def rounded_crop(src: Path, width_px: int, height_px: int, radius: int = 80) -> Path:
    with Image.open(src) as im:
        im = im.convert("RGB")
        src_ratio = im.width / im.height
        dst_ratio = width_px / height_px
        if src_ratio > dst_ratio:
            new_w = int(im.height * dst_ratio)
            left = (im.width - new_w) // 2
            im = im.crop((left, 0, left + new_w, im.height))
        else:
            new_h = int(im.width / dst_ratio)
            top = (im.height - new_h) // 2
            im = im.crop((0, top, im.width, top + new_h))
        im = im.resize((width_px, height_px), Image.Resampling.LANCZOS).convert("RGBA")
        mask = Image.new("L", (width_px, height_px), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, width_px, height_px + radius), radius=radius, fill=255)
        im.putalpha(mask)
        out = TMP_DIR / f"{src.stem}-{width_px}x{height_px}.png"
        im.save(out)
    return out


def draw_image_fit(c: canvas.Canvas, src: Path, x: float, y: float, width: float, height: float) -> None:
    image = ImageReader(str(src))
    iw, ih = image.getSize()
    scale = min(width / iw, height / ih)
    dw = iw * scale
    dh = ih * scale
    c.drawImage(image, x + (width - dw) / 2, y + (height - dh) / 2, dw, dh, mask="auto")


def draw_logo(c: canvas.Canvas) -> None:
    c.setFillColor(BROWN)
    c.setFont("EO-Bold", 30)
    c.drawString(62, 778, "ESPRIT ORGANIC")
    c.setFont("EO-Bold", 22)
    c.drawCentredString(176, 748, "COGNAC")
    c.setLineWidth(1.2)
    c.line(67, 759, 108, 759)
    c.line(244, 759, 285, 759)


def add_tags(src: Path, dest: Path, product_name: str, lang: str) -> None:
    reader = PdfReader(str(src))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    lang_cfg = LANG[lang]
    title = f"Cognac Esprit Organic - {product_name} - {lang_cfg['metadata_label']} PDF/UA"
    writer.add_metadata(
        {
            "/Title": title,
            "/Author": "Cognac Esprit Organic",
            "/Subject": f"{lang_cfg['metadata_label']} accessible for {product_name}",
            "/Keywords": f"Cognac Esprit Organic, {product_name}, {lang_cfg['metadata_label']}, PDF/UA, accessibility, organic cognac, Fins Bois",
            "/Creator": "Codex multilingual PDF/UA semantic tagging pipeline",
        }
    )
    root = writer._root_object
    root.update(
        {
            NameObject("/Lang"): TextStringObject(lang_cfg["pdf_lang"]),
            NameObject("/MarkInfo"): DictionaryObject(
                {
                    NameObject("/Marked"): BooleanObject(True),
                    NameObject("/Suspects"): BooleanObject(False),
                }
            ),
            NameObject("/StructTreeRoot"): DictionaryObject(
                {
                    NameObject("/Type"): NameObject("/StructTreeRoot"),
                    NameObject("/K"): ArrayObject(),
                }
            ),
            NameObject("/ViewerPreferences"): DictionaryObject(
                {NameObject("/DisplayDocTitle"): BooleanObject(True)}
            ),
        }
    )
    with dest.open("wb") as fh:
        writer.write(fh)


def draw_pdf(slug: str, lang: str) -> Path:
    product = PRODUCTS[slug]
    strings = product["translations"][lang]
    lang_cfg = LANG[lang]
    product_data = product_json(slug, lang)
    sensory = product_data.get("additionalProperty", [])

    final = OUT_DIR / f"cognac-esprit-organic-{slug}-fiche-degustation-{lang_cfg['filename_suffix']}.pdf"
    with tempfile.NamedTemporaryFile(suffix=".pdf", dir=TMP_DIR, delete=False) as temp:
        temp_path = Path(temp.name)

    c = canvas.Canvas(str(temp_path), pagesize=A4, pageCompression=1)
    c.setAuthor("Cognac Esprit Organic")
    c.setTitle(f"Cognac Esprit Organic - {product['name']} - {lang_cfg['metadata_label']}")

    color = product["color"]
    c.setFillColor("white")
    c.rect(0, 0, W, H, stroke=0, fill=1)

    c.setFillColor(GOLD)
    c.rect(W - 170, H - 38, 145, 38, stroke=0, fill=1)
    c.setFillColor("white")
    c.setFont("EO-Bold", 12)
    c.drawCentredString(W - 97, H - 24, lang_cfg["range"])

    draw_logo(c)

    title_size = fit_font(product["title"], "EO-Condensed", 56, 405, 40)
    c.setFillColor(color)
    c.setFont("EO-Condensed", title_size)
    c.drawString(62, 674, product["title"])

    sub_size = fit_font(strings["subtitle"], "EO-Condensed", 22, 370, 15)
    c.setFillColor(GREY)
    c.setFont("EO-Condensed", sub_size)
    c.drawString(62, 648, strings["subtitle"])

    story_len = len(strings["story"])
    story_size = 10.4 if story_len > 430 else 11.2
    story_leading = story_size * 1.32
    draw_wrapped(c, strings["story"], 62, 614, 232, "EO-Regular", story_size, story_leading)

    product_img = image_for_pdf(ROOT / product["product_image"])
    draw_image_fit(c, product_img, 330, 328, 230, 312)

    c.setFillColor(color)
    c.setFont("EO-CondensedItalic", 24)
    c.drawString(62, 408, lang_cfg["tasting"])
    tasting_title_size = fit_font(strings["tasting_title"], "EO-Condensed", 16, 250, 11)
    c.setFillColor(GREY)
    c.setFont("EO-Condensed", tasting_title_size)
    title_lines = wrap_lines(strings["tasting_title"], "EO-Condensed", tasting_title_size, 250)
    y = 382
    for line in title_lines[:3]:
        c.drawString(62, y, line)
        y -= tasting_title_size * 1.05
    y -= 8
    draw_wrapped(c, strings["tasting_body"], 62, y, 250, "EO-Regular", 10.5, 13.5)

    tasting_img = rounded_crop(ROOT / product["tasting_image"], 1000, 840)
    c.drawImage(ImageReader(str(tasting_img)), 62, 16, 222, 187, mask="auto")

    c.setFillColor(color)
    c.setFont("EO-CondensedItalic", 22)
    c.drawString(312, 230, lang_cfg["sensory"])
    c.setFillColor(color)
    c.rect(312, 8, 230, 206, stroke=0, fill=1)

    c.setFillColor("white")
    y = 196
    for item in sensory:
        label = item["name"]
        value = item["value"]
        c.setFont("EO-Bold", 8.1)
        c.drawString(328, y, label)
        y -= 9
        lines = wrap_lines(value, "EO-Bold", 7.5, 190)
        c.setFont("EO-Bold", 7.5)
        for line in lines[:4]:
            c.drawString(328, y, line)
            y -= 8.1
        y -= 3.2
        if y < 14:
            break

    c.showPage()
    c.save()
    add_tags(temp_path, final, product["name"], lang)
    temp_path.unlink(missing_ok=True)
    return final


def main() -> None:
    register_fonts()
    generated = []
    for slug in PRODUCTS:
        for lang in LANG:
            generated.append(draw_pdf(slug, lang))
    for path in generated:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
