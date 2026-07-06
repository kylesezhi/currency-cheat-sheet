"""Locale-aware currency formatting for the wallet card.

Provides two formatting functions used by the conversion engine:

* ``format_local`` — formats an integer amount with the local currency
  symbol and the locale-appropriate thousands separator (e.g. ¥1,000
  for JPY, $1.000 for CLP).
* ``format_usd`` — formats a float USD amount with a ``$`` prefix,
  comma grouping, and the correct number of decimal places.
"""

from __future__ import annotations

import locale
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from walletcard.config import Currency


def format_local(amount: int, currency: Currency) -> str:
    """Format *amount* with *currency*'s symbol and locale-aware grouping.

    Falls back to a plain ``{symbol}{amount}`` string if the locale is
    not available on the current system.
    """
    try:
        # Save the current locale setting so we can restore it later.
        prev = locale.setlocale(locale.LC_NUMERIC)

        try:
            locale.setlocale(locale.LC_NUMERIC, _normalise_locale(currency.locale))
            grouped = locale.format_string("%d", amount, grouping=True)
        except locale.Error:
            grouped = str(amount)

        if prev is not None:
            locale.setlocale(locale.LC_NUMERIC, prev)

        return f"{currency.symbol}{grouped}"

    except locale.Error:
        # Cannot save/restore locale at all — use plain fallback.
        return f"{currency.symbol}{amount}"


def format_usd(amount: float) -> str:
    """Format a USD amount with ``$`` prefix and comma grouping.

    Rules
    -----
    * Amount < 1.00  →  two decimal places (e.g. ``$0.68``)
    * Whole number   →  no decimal places   (e.g. ``$345``)
    * Otherwise      →  two decimal places  (e.g. ``$13.60``)
    """
    try:
        prev = locale.setlocale(locale.LC_NUMERIC)

        try:
            locale.setlocale(locale.LC_NUMERIC, _normalise_locale("en-US"))
        except locale.Error:
            locale.setlocale(locale.LC_NUMERIC, "C")

        if amount < 1.0:
            fmt = locale.format_string("%.2f", amount, grouping=True)
        elif amount == round(amount):
            fmt = locale.format_string("%.0f", amount, grouping=True)
        else:
            fmt = locale.format_string("%.2f", amount, grouping=True)

        if prev is not None:
            locale.setlocale(locale.LC_NUMERIC, prev)

        return f"${fmt}"

    except locale.Error:
        # Fallback: plain formatting without locale.
        if amount < 1.0:
            return f"${amount:.2f}"
        if amount == round(amount):
            return f"${amount:.0f}"
        return f"${amount:.2f}"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_LOCALE_MAP: dict[str, str] = {
    "ja-JP": "ja_JP.UTF-8",
    "es-CL": "es_CL.UTF-8",
    "en-US": "en_US.UTF-8",
}


def _normalise_locale(tag: str) -> str:
    """Convert a BCP 47-like tag (``ja-JP``) to a system locale (``ja_JP.UTF-8``)."""
    try:
        return _LOCALE_MAP[tag]
    except KeyError:
        # Generic conversion: replace hyphen with underscore, append UTF-8.
        return tag.replace("-", "_") + ".UTF-8"