"""Generate a wallet-sized currency cheat-sheet PDF."""

from pathlib import Path

from walletcard.renderer import render_card

OUTPUT_DIR = Path("output")


def main() -> None:
    """Render a sample wallet card with dummy data."""
    data = {
        "title": "JPY → USD",
        "exchange_rate_text": "1 USD ≈ 147 JPY",
        "generated_date": "July 5, 2026",
        "rows": [
            {"local": "¥100", "usd": "$0.68"},
            {"local": "¥200", "usd": "$1.36"},
            {"local": "¥500", "usd": "$3.40"},
            {"local": "¥1,000", "usd": "$6.80"},
            {"local": "¥2,000", "usd": "$13.60"},
            {"local": "¥5,000", "usd": "$34.00"},
            {"local": "¥10,000", "usd": "$68.00"},
        ],
    }

    output_path = OUTPUT_DIR / "JPY-wallet-card.pdf"
    render_card(data, output_path)
    print(f"✅ Wallet card saved to {output_path}")


if __name__ == "__main__":
    main()