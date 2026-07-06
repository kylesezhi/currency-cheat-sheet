"""Exchange rate retrieval from the ExchangeRate-API (open.er-api.com)."""

from __future__ import annotations

import json
from urllib.request import urlopen, Request
from urllib.error import URLError

EXCHANGE_RATE_API = "https://open.er-api.com/v6/latest/{from_cur}"


def load_rate(from_cur: str) -> tuple[float, str]:
    """Return the exchange rate from *from_cur* to USD.

    Calls the ExchangeRate-API (open.er-api.com).  Exits with a
    friendly message if the API is unavailable.

    Returns
    -------
    (rate, rate_text)
        *rate* is the multiplier to convert *from_cur* → USD.
        *rate_text* is a human-readable string like ``"1 USD ≈ 147 JPY"``.
    """
    url = EXCHANGE_RATE_API.format(from_cur=from_cur)
    req = Request(url, headers={"User-Agent": "currency-cheat-sheet/0.1.0"})
    try:
        with urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode())
        if body.get("result") != "success":
            raise KeyError("API returned non-success result")
        rate = float(body["rates"]["USD"])
    except (URLError, json.JSONDecodeError, KeyError, TypeError):
        print(
            f"❌ Could not fetch exchange rate for {from_cur}.\n"
            f"   Check your internet connection and try again later.",
        )
        raise SystemExit(1)

    # Build the human-readable rate text.
    # 1 unit of from_cur = rate USD  →  1 USD = 1/rate from_cur
    inverse = 1.0 / rate
    if inverse >= 1:
        rate_text = f"1 USD ≈ {inverse:,.0f} {from_cur}"
    else:
        rate_text = f"1 USD ≈ {inverse:,.2f} {from_cur}"

    return rate, rate_text