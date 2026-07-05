from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import date


PAGE_WIDTH = 85.6 * mm
PAGE_HEIGHT = 54 * mm


MOCK_DATA = [
    ("100 JPY", "$0.68"),
    ("200 JPY", "$1.36"),
    ("500 JPY", "$3.40"),
    ("1,000 JPY", "$6.80"),
    ("2,000 JPY", "$13.60"),
    ("5,000 JPY", "$34.00"),
    ("10,000 JPY", "$68.00"),
]


def format_date(d: date) -> str:
    # "July 5, 2026"
    return d.strftime("%B %-d, %Y") if hasattr(d, "strftime") else str(d)


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

    # Table
    table_data = [["Local", "USD"]] + MOCK_DATA

    table = Table(table_data, colWidths=[35 * mm, 35 * mm])

    style_list = [
        ("FONT", (0, 0), (-1, -1), "Courier", 6),

        # Header emphasis
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),

        # Light horizontal rules for scanability
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.grey),

        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]

    # Zebra striping (very subtle, print-safe)
    for i in range(1, len(table_data)):
        if i % 2 == 1:
            style_list.append(
                ("BACKGROUND", (0, i), (-1, i), colors.whitesmoke)
            )

    table.setStyle(TableStyle(style_list))
    elements.append(table)

    # Footer (right aligned)
    footer = Paragraph(
        f'<para alignment="right">Generated {format_date(date.today())}</para>',
        style
    )
    elements.append(Spacer(1, 2 * mm))
    elements.append(footer)

    doc.build(elements)


if __name__ == "__main__":
    build_pdf()