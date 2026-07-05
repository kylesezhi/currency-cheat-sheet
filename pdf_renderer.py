from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import date


PAGE_WIDTH = 85.6 * mm   # credit card size
PAGE_HEIGHT = 54 * mm


MOCK_DATA = [
    # (local currency, usd equivalent)
    ("100 JPY", "$0.68"),
    ("200 JPY", "$1.36"),
    ("500 JPY", "$3.40"),
    ("1,000 JPY", "$6.80"),
    ("2,000 JPY", "$13.60"),
    ("5,000 JPY", "$34.00"),
    ("10,000 JPY", "$68.00"),
]


def build_pdf(filename="wallet_card.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape((PAGE_WIDTH, PAGE_HEIGHT)),
        leftMargin=3 * mm,
        rightMargin=3 * mm,
        topMargin=3 * mm,
        bottomMargin=3 * mm,
    )

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Courier"
    style.fontSize = 6
    style.leading = 7

    elements = []

    # Header
    header = Paragraph(
        "<b>JPY → USD</b>   |   1 USD = ~147 JPY",
        style
    )
    elements.append(header)
    elements.append(Spacer(1, 2 * mm))

    # Table data
    table_data = [["Local", "USD"]] + MOCK_DATA

    table = Table(table_data, colWidths=[35 * mm, 35 * mm])

    table.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Courier", 6),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
    ]))

    elements.append(table)

    # Footer
    footer = Paragraph(
        f"Generated {date.today().isoformat()}",
        style
    )
    elements.append(Spacer(1, 2 * mm))
    elements.append(footer)

    doc.build(elements)


if __name__ == "__main__":
    build_pdf()