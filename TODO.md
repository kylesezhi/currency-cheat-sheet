# TODO: Replace ReportLab PDF Generation with HTML + WeasyPrint

## Goal

Replace the hand-drawn ReportLab renderer with an HTML/CSS-based renderer while preserving the existing visual design and wallet-card dimensions.

New rendering pipeline:

```
Python Data
    ↓
Jinja2 Template
    ↓
HTML
    ↓
CSS
    ↓
WeasyPrint
    ↓
wallet-card.pdf
```

---

# Milestone 1: Add Dependencies

Install:

- weasyprint
- jinja2

Optional:

- playwright (for HTML preview/testing)

---

# Milestone 2: Project Structure

```
wallet-card/
├── main.py
├── templates/
│   └── card.html
├── static/
│   └── card.css
├── walletcard/
│   ├── renderer.py
│   ├── formatting.py
│   ├── rates.py
│   ├── denominations.py
│   └── ...
└── output/
```

---

# Milestone 3: Create HTML Template

Create:

```
templates/card.html
```

Template receives:

```
title
exchange_rate_text
rows
generated_date
```

Example context:

```python
{
    "title": "JPY → USD",
    "exchange_rate_text": "1 USD ≈ 147 JPY",
    "generated_date": "July 5, 2026",
    "rows": [
        {
            "local": "¥100",
            "usd": "$0.68"
        },
        ...
    ]
}
```

---

# Milestone 4: Create CSS

Create:

```
static/card.css
```

Requirements:

- Exact ISO ID-1 card dimensions
- Landscape orientation
- Monospace font
- Thin margins
- Zebra striping
- Right-aligned USD column
- Header rule
- Footer right aligned
- Optimized for grayscale printing

Use CSS variables for:

```
--margin
--row-height
--font-size
--stripe-color
--rule-color
```

---

# Milestone 5: Match Existing Layout

Reproduce the current design exactly.

Header:

```
JPY → USD
1 USD ≈ 147 JPY
────────────────────────
```

Body:

```
¥100          $0.68
¥200          $1.36
¥500          $3.40
...
```

Features:

- alternating row background
- no vertical lines
- no interior horizontal rules
- bold rule under header
- bold rule above footer

Footer:

```
Generated July 5, 2026
```

right aligned.

---

# Milestone 6: CSS Print Layout

Use:

```css
@page {
    size: 85.6mm 53.98mm;
    margin: 0;
}
```

Card container:

```
85.6mm × 53.98mm
```

Verify:

- prints actual size
- no scaling
- no clipping

---

# Milestone 7: Renderer

Implement:

```python
render_card(data, output_path)
```

Responsibilities:

- Load Jinja template
- Render HTML
- Load CSS
- Generate PDF via WeasyPrint
- Save output

---

# Milestone 8: HTML Preview

Optional but recommended.

Implement:

```
render_preview(data)
```

Outputs:

```
output/card.html
```

Benefits:

- Open in browser
- Instant iteration
- Browser DevTools
- No PDF generation required during design

---

# Milestone 9: Responsive Layout

Avoid absolute positioning.

Use CSS Grid or Flexbox.

Requirements:

- Local currency left aligned
- USD right aligned
- Columns remain visually close together
- Rows automatically size to available height

No hardcoded pixel coordinates.

---

# Milestone 10: Typography

Investigate fonts.

Candidates:

- IBM Plex Mono
- JetBrains Mono
- Fira Mono
- Courier New
- Cascadia Mono

Goal:

- Excellent readability
- Narrow glyphs
- Good printed appearance

---

# Milestone 11: Print Validation

Verify:

- Credit-card dimensions
- Wallet fit
- Black-and-white laser printer
- Inkjet printer
- Browser print preview
- WeasyPrint output

---

# Milestone 12: Regression Testing

Ensure visual parity with the ReportLab version.

Checklist:

- Header spacing
- Footer alignment
- Zebra striping
- Column spacing
- Typography
- Margins
- Card dimensions

---

# Stretch Goals

- Browser live preview during development
- Multiple cards on one US Letter page
- Cut marks
- QR code linking to live exchange rates
- Optional dark preview theme (HTML only)
- Theme support
- Custom fonts
- SVG currency symbols
- Automatic font scaling for long values

---

# Definition of Done

Running:

```
python main.py JPY
```

should:

1. Retrieve the exchange rate.
2. Generate denomination rows.
3. Render HTML using Jinja2.
4. Apply CSS styling.
5. Produce a wallet-sized PDF via WeasyPrint.
6. Save:

```
output/JPY-wallet-card.pdf
```

Additionally, during development:

```
python main.py JPY --preview
```

should generate:

```
output/JPY-wallet-card.html
```

that can be opened in any modern browser for rapid visual iteration before generating the final PDF.


# Wallet Currency Cheat Sheet

## Goal

Generate a wallet-sized PDF containing a lookup table that converts common local currency amounts into USD. The card is intended for travelers to quickly estimate prices without using a phone.

---

# Milestone 1: Project Skeleton

- [x] PDF renderer
- [ ] Command-line interface
- [ ] Configuration loading
- [ ] Exchange rate retrieval
- [ ] Denomination generation
- [ ] Currency formatting
- [ ] End-to-end integration

Suggested structure:

```
wallet-card/
├── main.py
├── config/
│   └── currencies.json
├── walletcard/
│   ├── __init__.py
│   ├── config.py
│   ├── rates.py
│   ├── denominations.py
│   ├── formatting.py
│   ├── pdf_renderer.py
│   └── cache.py
├── cache/
├── output/
└── README.md
```

---

# Milestone 2: Configuration

Create `config/currencies.json`

Initially support:

- JPY
- CLP

Each currency should contain:

```json
{
  "JPY": {
    "country": "Japan",
    "symbol": "¥",
    "locale": "ja-JP",
    "denominations": [
      100,
      500,
      1000,
      2000,
      5000,
      10000
    ]
  },
  "CLP": {
    "country": "Chile",
    "symbol": "$",
    "locale": "es-CL",
    "denominations": [
      100,
      500,
      1000,
      2000,
      5000,
      10000,
      20000
    ]
  }
}
```

Write a loader that returns a Currency object.

---

# Milestone 3: Exchange Rates

Use:

https://api.frankfurter.app

Request:

```
GET /latest?from=JPY&to=USD
```

Return:

```
1 JPY -> USD
```

Cache:

```
cache/rates.json
```

Behavior:

- Try API
- Save successful response
- If API unavailable, use cache
- If neither exists, exit with a friendly error

---

# Milestone 4: Denomination Generation

Input:

```
[100, 500, 1000, 2000, 5000, 10000]
```

Generate a printable list.

Rules:

- Preserve configured denominations.
- Extend downward if useful.
- Extend upward until approximately a new-car purchase.
- Follow a 1-2-5 progression.
- Remove duplicates.
- Sort ascending.

Example output:

```
100
200
500
1000
2000
5000
10000
20000
50000
100000
200000
500000
1000000
2000000
5000000
```

---

# Milestone 5: Currency Formatting

Use locale-aware formatting where practical.

Examples:

JPY

```
100
1,000
10,000
```

CLP

```
1.000
10.000
```

USD

```
$0.68
$13.60
$345
$4,560
```

Rules:

- Always include the local currency symbol.
- Always include the USD "$".
- Keep formatting compact.

---

# Milestone 6: Conversion Engine

Input:

```
JPY
```

Workflow:

```
load config
↓

load exchange rate

↓

generate denominations

↓

convert every denomination to USD

↓

format strings

↓

return printable rows
```

Example:

```
¥100        $0.68
¥200        $1.36
¥500        $3.40
¥1,000      $6.80
...
```

---

# Milestone 7: PDF Integration

Replace mock rows with generated rows.

Inputs:

- Currency code
- Exchange rate
- Generated date
- Converted rows

Header:

```
JPY → USD
1 USD ≈ 147 JPY
```

Footer:

```
Generated July 5, 2026
```

---

# Milestone 8: Command-Line Interface

Example:

```
python main.py JPY
```

Produces:

```
output/JPY-wallet-card.pdf
```

Optional future flags:

```
--output
--force-refresh
--open
--verbose
```

---

# Milestone 9: Testing

Unit tests:

- denomination generation
- exchange rate parsing
- cache fallback
- currency formatting
- config loading

Integration test:

```
JPY

↓

Generated PDF

↓

Visual inspection
```

---

# Milestone 10: Nice-to-Haves

- Support EUR as alternate home currency
- Support GBP, CAD, AUD, etc.
- QR code linking to live exchange rates
- Multiple cards on a US Letter page with cut marks
- Automatic row density adjustment
- Dark mode (screen preview only)
- Optional logarithmic denomination generation
- Configurable home currency
- Batch generation for multiple countries

---

# Definition of Done

Running:

```
python main.py JPY
```

should:

1. Download the latest exchange rate.
2. Fall back to cache if offline.
3. Generate useful denominations.
4. Convert every amount into USD.
5. Render a wallet-sized PDF.
6. Save it to:

```
output/JPY-wallet-card.pdf
```

without requiring any manual editing.