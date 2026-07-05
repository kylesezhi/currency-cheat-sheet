from dataclasses import dataclass
from datetime import date

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

###############################################################################
# Card
###############################################################################

CARD_WIDTH = 85.60 * mm
CARD_HEIGHT = 53.98 * mm

###############################################################################
# Mock data
###############################################################################

ROWS = [
    ("100 JPY", "$0.68"),
    ("200 JPY", "$1.36"),
    ("500 JPY", "$3.40"),
    ("1,000 JPY", "$6.80"),
    ("2,000 JPY", "$13.60"),
    ("5,000 JPY", "$34.00"),
    ("10,000 JPY", "$68.00"),
]

###############################################################################
# Styling
###############################################################################


@dataclass(frozen=True)
class Style:
    left_margin = 20 * mm
    right_margin = 20 * mm
    top_margin = 3 * mm
    bottom_margin = 3 * mm

    header_gap = 1.0 * mm
    footer_gap = 1.2 * mm

    title_size = 8
    subtitle_size = 6
    body_size = 6
    footer_size = 5

    zebra = colors.HexColor("#FCFCFC")

    heavy_rule = 0.6
    rule_color = colors.black


S = Style()


###############################################################################


def pretty_date():
    return date.today().strftime("%B %d, %Y").replace(" 0", " ")


def draw_header(c):

    title_y = CARD_HEIGHT - S.top_margin

    c.setFont("Courier-Bold", S.title_size)
    c.drawString(
        S.left_margin,
        title_y,
        "JPY → USD",
    )

    subtitle_y = title_y - 3.3 * mm

    c.setFont("Courier", S.subtitle_size)
    c.drawString(
        S.left_margin,
        subtitle_y,
        "1 USD ≈ 147 JPY",
    )

    rule_y = subtitle_y - 2.8 * mm

    c.setStrokeColor(S.rule_color)
    c.setLineWidth(S.heavy_rule)

    c.line(
        S.left_margin,
        rule_y,
        CARD_WIDTH - S.right_margin,
        rule_y,
    )

    return rule_y


def draw_footer(c):

    text = f"Generated {pretty_date()}"

    c.setFont("Courier", S.footer_size)

    width = c.stringWidth(
        text,
        "Courier",
        S.footer_size,
    )

    baseline = S.bottom_margin

    c.drawString(
        CARD_WIDTH - S.right_margin - width,
        baseline,
        text,
    )

    return baseline + S.footer_size + 1 * mm


def draw_table(c, header_rule_y, footer_top):

    table_top = header_rule_y - S.header_gap
    table_bottom = footer_top + S.footer_gap

    table_height = table_top - table_bottom

    row_height = table_height / len(ROWS)

    left = S.left_margin
    right = CARD_WIDTH - S.right_margin

    usd_x = right

    c.setFont("Courier", S.body_size)

    for i, (local, usd) in enumerate(ROWS):

        row_top = table_top - i * row_height
        row_bottom = row_top - row_height

        #
        # alternating background
        #

        if i % 2 == 1:

            c.setFillColor(S.zebra)

            c.rect(
                left,
                row_bottom,
                right - left,
                row_height,
                stroke=0,
                fill=1,
            )

        #
        # text
        #

        baseline = row_bottom + (row_height - S.body_size) / 2 + 0.5

        c.setFillColor(colors.black)

        c.drawString(
            left,
            baseline,
            local,
        )

        c.drawRightString(
            usd_x,
            baseline,
            usd,
        )

    #
    # closing rule
    #

    c.setStrokeColor(S.rule_color)
    c.setLineWidth(S.heavy_rule)

    c.line(
        left,
        table_bottom,
        right,
        table_bottom,
    )


def build_pdf(filename="wallet_card.pdf"):

    c = canvas.Canvas(
        filename,
        pagesize=(CARD_WIDTH, CARD_HEIGHT),
    )

    footer_top = draw_footer(c)

    header_rule_y = draw_header(c)

    draw_table(
        c,
        header_rule_y,
        footer_top,
    )

    c.showPage()
    c.save()


if __name__ == "__main__":
    build_pdf()