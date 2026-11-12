"""Ekspor LAPORAN.md menjadi DOCX tanpa mengisi hasil uji yang belum dilakukan.

Pasang dependensi: python -m pip install python-docx
Jalankan: python buat_laporan.py
"""

from pathlib import Path
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


ROOT = Path(__file__).resolve().parent


def plain(text):
    return re.sub(r"[*`]", "", text).strip()


def add_link(paragraph, url):
    """Simpan sebagai hyperlink Word sungguhan, bukan sekadar teks URL."""
    relationship_id = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), relationship_id)
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    style = OxmlElement("w:rStyle")
    style.set(qn("w:val"), "Hyperlink")
    properties.append(style)
    run.append(properties)
    text = OxmlElement("w:t")
    text.text = url
    run.append(text)
    link.append(run)
    paragraph._p.append(link)


def main():
    doc = Document()
    section = doc.sections[0]
    section.page_height, section.page_width = Cm(29.7), Cm(21)
    section.top_margin = section.bottom_margin = Cm(2.4)
    section.left_margin = section.right_margin = Cm(2.6)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(7)

    lines = (ROOT / "LAPORAN.md").read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("| "):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [plain(c) for c in lines[index].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"[-:]+", cell) for cell in cells):
                    rows.append(cells)
                index += 1
            if rows:
                table = doc.add_table(rows=0, cols=len(rows[0]))
                table.style = "Table Grid"
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                for row in rows:
                    cells = table.add_row().cells
                    for cell, text in zip(cells, row):
                        cell.text = text
                for cell in table.rows[0].cells:
                    for run in cell.paragraphs[0].runs:
                        run.bold = True
            continue
        if line.startswith("# "):
            doc.add_heading(plain(line[2:]), 0)
        elif line.startswith("## "):
            doc.add_heading(plain(line[3:]), 1)
        elif line.startswith("> "):
            doc.add_paragraph(plain(line[2:]), style="Subtitle")
        elif line.startswith("- Link GitHub: "):
            paragraph = doc.add_paragraph("Link GitHub: ", style="List Bullet")
            add_link(paragraph, plain(line.split(": ", 1)[1]))
        elif line.startswith("- "):
            doc.add_paragraph(plain(line[2:]), style="List Bullet")
        else:
            doc.add_paragraph(plain(line))
        index += 1

    output = ROOT / "Laporan_Praktikum_Minggu11.docx"
    doc.save(output)
    print(f"Laporan disimpan: {output}")


if __name__ == "__main__":
    main()
