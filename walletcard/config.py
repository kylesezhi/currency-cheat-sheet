"""Configuration loading — reads currencies.json and returns Currency objects."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "currencies.json"


@dataclass(frozen=True)
class Currency:
    """A single currency definition loaded from the config file."""

    code: str
    country: str
    symbol: str
    locale: str
    denominations: list[int] = field(default_factory=list)


def load_currency(code: str) -> Currency:
    """Look up *code* (e.g. ``"JPY"``) in the config file and return a Currency.

    Raises
    ------
    FileNotFoundError
        If the config file does not exist.
    KeyError
        If *code* is not present in the config file.
    json.JSONDecodeError
        If the config file contains invalid JSON.
    """
    if not CONFIG_PATH.is_file():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with CONFIG_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    if code not in data:
        raise KeyError(f"Currency code '{code}' not found in config file.")

    entry = data[code]
    return Currency(
        code=code,
        country=entry["country"],
        symbol=entry["symbol"],
        locale=entry["locale"],
        denominations=entry["denominations"],
    )