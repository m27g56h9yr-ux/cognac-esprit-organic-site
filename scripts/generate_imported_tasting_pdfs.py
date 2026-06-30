from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    BooleanObject,
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
    NumberObject,
    TextStringObject,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets/pdf/fiches-degustation"
TMP_DIR = ROOT / "tmp/pdfs/imported"
W, H = A4

SHEETS = [
    {
        "page": 1,
        "slug": "single-cask",
        "product": "Single Cask",
        "title": "Cognac Esprit Organic - Single Cask - Fiche dégustation PDF/UA",
    },
    {
        "page": 2,
        "slug": "pineau",
        "product": "Pineau blanc",
        "title": "Cognac Esprit Organic - Pineau blanc - Fiche dégustation PDF/UA",
    },
    {
        "page": 3,
        "slug": "pineau-rouge",
        "product": "Pineau rouge",
        "title": "Cognac Esprit Organic - Pineau rouge - Fiche dégustation PDF/UA",
    },
]


def xmp_metadata(title: str) -> bytes:
    return f"""<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="pypdf">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="" xmlns:pdfuaid="http://www.aiim.org/pdfua/ns/id/" pdfuaid:part="1"/>
  <rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/">
   <dc:title><rdf:Alt><rdf:li xml:lang="x-default">{title}</rdf:li></rdf:Alt></dc:title>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>""".encode("utf-8")


def add_pdf_ua_tags(src: Path, dest: Path, title: str, product: str) -> None:
    reader = PdfReader(str(src))
    writer = PdfWriter()
    page_refs = []
    parent_tree_nums = ArrayObject()

    for page_index, page in enumerate(reader.pages):
        stream = DecodedStreamObject()
        stream.set_data(b"/P <</MCID 0>> BDC\n" + page.get_contents().get_data() + b"\nEMC\n")
        page[NameObject("/Contents")] = writer._add_object(stream)
        writer.add_page(page)
        writer.pages[page_index][NameObject("/StructParents")] = NumberObject(page_index)
        page_refs.append(writer.pages[page_index].indirect_reference)

    writer.add_metadata(
        {
            "/Title": title,
            "/Author": "Cognac Esprit Organic",
            "/Subject": f"Fiche dégustation accessible pour {product}",
            "/Keywords": f"Cognac Esprit Organic, {product}, fiche dégustation, PDF/UA, accessibilité",
            "/Creator": "Codex imported PDF/UA semantic tagging pipeline",
        }
    )

    root = writer._root_object
    struct_root = DictionaryObject({NameObject("/Type"): NameObject("/StructTreeRoot")})
    struct_root_ref = writer._add_object(struct_root)
    document = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/StructElem"),
            NameObject("/S"): NameObject("/Document"),
            NameObject("/P"): struct_root_ref,
            NameObject("/Lang"): TextStringObject("fr-FR"),
        }
    )
    document_ref = writer._add_object(document)
    document_children = ArrayObject()

    for page_index, page_ref in enumerate(page_refs):
        paragraph = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/StructElem"),
                NameObject("/S"): NameObject("/P"),
                NameObject("/P"): document_ref,
                NameObject("/Pg"): page_ref,
                NameObject("/K"): NumberObject(0),
            }
        )
        paragraph_ref = writer._add_object(paragraph)
        document_children.append(paragraph_ref)
        parent_array_ref = writer._add_object(ArrayObject([paragraph_ref]))
        parent_tree_nums.extend([NumberObject(page_index), parent_array_ref])

    document[NameObject("/K")] = document_children
    parent_tree_ref = writer._add_object(DictionaryObject({NameObject("/Nums"): parent_tree_nums}))
    struct_root.update(
        {
            NameObject("/K"): document_ref,
            NameObject("/ParentTree"): parent_tree_ref,
            NameObject("/ParentTreeNextKey"): NumberObject(len(page_refs)),
        }
    )

    metadata = DecodedStreamObject()
    metadata.set_data(xmp_metadata(title))
    metadata.update(
        {
            NameObject("/Type"): NameObject("/Metadata"),
            NameObject("/Subtype"): NameObject("/XML"),
        }
    )
    root.update(
        {
            NameObject("/Lang"): TextStringObject("fr-FR"),
            NameObject("/MarkInfo"): DictionaryObject(
                {
                    NameObject("/Marked"): BooleanObject(True),
                    NameObject("/Suspects"): BooleanObject(False),
                }
            ),
            NameObject("/ViewerPreferences"): DictionaryObject(
                {NameObject("/DisplayDocTitle"): BooleanObject(True)}
            ),
            NameObject("/StructTreeRoot"): struct_root_ref,
            NameObject("/Metadata"): writer._add_object(metadata),
        }
    )

    with dest.open("wb") as fh:
        writer.write(fh)


def render_page(source_pdf: Path, sheet: dict[str, object], work_dir: Path, dpi: int) -> Path:
    prefix = work_dir / f"{sheet['slug']}"
    subprocess.run(
        [
            "pdftoppm",
            "-r",
            str(dpi),
            "-f",
            str(sheet["page"]),
            "-l",
            str(sheet["page"]),
            "-png",
            str(source_pdf),
            str(prefix),
        ],
        check=True,
    )
    rendered = work_dir / f"{sheet['slug']}-{sheet['page']}.png"
    jpeg = work_dir / f"{sheet['slug']}.jpg"
    with Image.open(rendered) as im:
        im.convert("RGB").save(jpeg, "JPEG", quality=90, optimize=True)
    return jpeg


def image_pdf(image: Path, dest: Path, title: str) -> None:
    c = canvas.Canvas(str(dest), pagesize=A4, pageCompression=1)
    c.setAuthor("Cognac Esprit Organic")
    c.setTitle(title)
    c.drawImage(ImageReader(str(image)), 0, 0, W, H, preserveAspectRatio=True, anchor="c")
    c.showPage()
    c.save()


def generate(source_pdf: Path, dpi: int) -> list[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []

    with tempfile.TemporaryDirectory(dir=TMP_DIR) as raw_tmp:
        work_dir = Path(raw_tmp)
        for sheet in SHEETS:
            jpeg = render_page(source_pdf, sheet, work_dir, dpi)
            final = OUT_DIR / f"cognac-esprit-organic-{sheet['slug']}-fiche-degustation.pdf"
            temp_pdf = work_dir / f"{sheet['slug']}.pdf"
            image_pdf(jpeg, temp_pdf, str(sheet["title"]))
            add_pdf_ua_tags(temp_pdf, final, str(sheet["title"]), str(sheet["product"]))
            generated.append(final)

    return generated


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate web-ready PDF/UA tasting sheets from an imported multi-page PDF.")
    parser.add_argument("source_pdf", type=Path, help="Source PDF containing one tasting sheet per page.")
    parser.add_argument("--dpi", type=int, default=190, help="Rasterisation resolution for the imported design.")
    args = parser.parse_args()

    for path in generate(args.source_pdf, args.dpi):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
