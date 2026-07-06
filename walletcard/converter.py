"""Conversion engine — wires together config, rates, denominations, and formatting."""

from __future__ import annotations

from datetime import date

from walletcard.config import Currency, load_currency
from walletcard.denominations import generate_denominations
from walletcard.formatting import format_local, format_usd
from walletcard.rates import load_rate


def build_card_data(currency_code: str) -> dict:
    """Build a data dict suitable for ``render_card()``.

    Workflow
    --------
    1. Load the currency config.
    2. Fetch the live exchange rate.
    3. Generate the denomination list.
    4. Convert every denomination to USD.
    5. Format all rows as printable strings.

    Returns
    -------
    dict
        Keys: ``title``, ``exchange_rate_text``, ``generated_date``, ``rows``.
    """
    currency: Currency = load_currency(currency_code)
    rate, rate_text = load_rate(currency_code)

    denoms = generate_denominations(currency.denominations)

    rows = []
    for denom in denoms:
        usd_amount = denom * rate
        rows.append(
            {
                "local": format_local(denom, currency),
                "usd": format_usd(usd_amount),
            }
        )

    return {
        "title": f"{currency_code} → USD",
        "exchange_rate_text": rate_text,
        "generated_date": date.today().strftime("%B %d, %Y"),
        "rows": rows,
    }