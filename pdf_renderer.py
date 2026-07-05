from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import date


CARD_WIDTH = 85.60 * mm
CARD_HEIGHT = 53.98 * mm


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
    return d.strftime("%B %d, %Y")


def draw_card(c: canvas.Canvas):
    # ─────────────────────────────
    # Layout constants (tuned for wallet readability)
    # ─────────────────────────────
    left_margin = 3 * mm
    top_margin = 4 * mm

    row_height = 4.6 * mm
    font_size = 5.8

    # Header
    c.setFont("Courier-Bold", 6.5)
    c.drawString(left_margin, CARD_HEIGHT - top_margin, "JPY → USD")

    c.setFont("Courier", 5.5)
    c.drawString(left_margin, CARD_HEIGHT - top_margin - 3 * mm, "1 USD ≈ 147 JPY")

    # Table header line
    y = CARD_HEIGHT - top_margin - 7 * mm

    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    c.line(left_margin, y, CARD_WIDTH - left_margin, y)

    y -= row_height

    # Rows
    c.setFont("Courier", font_size)

    for i, (local, usd) in enumerate(MOCK_DATA):
        # Zebra stripe (very subtle gray background)
        if i % 2 == 1:
            c.setFillColor(colors.whitesmoke)
            c.rect(
                0,
                y - 1.2 * mm,
                CARD_WIDTH,
                row_height,
                fill=1,
                stroke=0,
            )
            c.setFillColor(colors.black)

        # Text columns
        c.drawString(left_margin, y, local)
        c.drawString(CARD_WIDTH / 2, y, usd)

        # Row separator (light)
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(0.3)
        c.line(left_margin, y - 1.5 * mm, CARD_WIDTH - left_margin, y - 1.5 * mm)

        y -= row_height

        # Hard stop if we run out of space (prevents overflow entirely)
        if y < 8 * mm:
            break

    # Footer (right-aligned)
    c.setFont("Courier", 5)
    footer_text = f"Generated {format_date(date.today())}"
    text_width = c.stringWidth(footer_text, "Courier", 5)

    c.drawString(
        CARD_WIDTH - text_width - left_margin,
        3 * mm,
        footer_text
    )


def build_pdf(filename="wallet_card.pdf"):
    c = canvas.Canvas(filename, pagesize=(CARD_WIDTH, CARD_HEIGHT))

    draw_card(c)

    c.showPage()
    c.save()


if __name__ == "__main__":
    build_pdf()