"""Generate a wallet-sized currency cheat-sheet PDF.

Usage
-----
    python main.py JPY
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from walletcard.converter import build_card_data
from walletcard.renderer import render_card

OUTPUT_DIR = Path("output")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a wallet-sized currency cheat-sheet PDF.",
    )
    parser.add_argument(
        "currency",
        type=str.upper,
        help="Three-letter currency code (e.g. JPY, CLP).",
    )
    args = parser.parse_args()

    try:
        data = build_card_data(args.currency)
    except (FileNotFoundError, KeyError) as exc:
        print(f"❌ {exc}")
        sys.exit(1)

    output_path = OUTPUT_DIR / f"{args.currency}-wallet-card.pdf"
    render_card(data, output_path)
    print(f"✅ Wallet card saved to {output_path}")


if __name__ == "__main__":
    main()