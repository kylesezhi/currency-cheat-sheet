"""Tests for walletcard.config."""

import json
from pathlib import Path

import pytest

from walletcard.config import Currency, load_currency

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def valid_config(tmp_path: Path) -> Path:
    """Write a minimal valid currencies.json and return its path."""
    data = {
        "JPY": {
            "country": "Japan",
            "symbol": "¥",
            "locale": "ja-JP",
            "denominations": [100, 500, 1000],
        }
    }
    config_path = tmp_path / "config" / "currencies.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(json.dumps(data), encoding="utf-8")
    return config_path


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_load_currency_success(monkeypatch, valid_config: Path) -> None:
    """Loading a known currency code returns a populated Currency object."""
    monkeypatch.setattr("walletcard.config.CONFIG_PATH", valid_config)

    currency = load_currency("JPY")

    assert isinstance(currency, Currency)
    assert currency.code == "JPY"
    assert currency.country == "Japan"
    assert currency.symbol == "¥"
    assert currency.locale == "ja-JP"
    assert currency.denominations == [100, 500, 1000]


def test_load_currency_missing_code(monkeypatch, valid_config: Path) -> None:
    """An unknown currency code should raise KeyError."""
    monkeypatch.setattr("walletcard.config.CONFIG_PATH", valid_config)

    with pytest.raises(KeyError, match="CLP"):
        load_currency("CLP")


def test_load_currency_missing_file(monkeypatch, tmp_path: Path) -> None:
    """If the config file doesn't exist, raise FileNotFoundError."""
    missing = tmp_path / "nonexistent.json"
    monkeypatch.setattr("walletcard.config.CONFIG_PATH", missing)

    with pytest.raises(FileNotFoundError):
        load_currency("JPY")


def test_load_currency_invalid_json(monkeypatch, tmp_path: Path) -> None:
    """Invalid JSON in the config file should raise JSONDecodeError."""
    bad_path = tmp_path / "config" / "currencies.json"
    bad_path.parent.mkdir(parents=True)
    bad_path.write_text("not valid json", encoding="utf-8")
    monkeypatch.setattr("walletcard.config.CONFIG_PATH", bad_path)

    with pytest.raises(json.JSONDecodeError):
        load_currency("JPY")