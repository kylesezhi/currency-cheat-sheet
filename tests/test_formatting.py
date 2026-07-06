"""Tests for walletcard.formatting."""

import locale as locale_mod
from unittest.mock import patch

import pytest

from walletcard.config import Currency
from walletcard.formatting import format_local, format_usd


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def jpy() -> Currency:
    return Currency(code="JPY", country="Japan", symbol="¥", locale="ja-JP")


@pytest.fixture
def clp() -> Currency:
    return Currency(code="CLP", country="Chile", symbol="$", locale="es-CL")


# ---------------------------------------------------------------------------
# format_local
# ---------------------------------------------------------------------------


@patch("walletcard.formatting.locale.setlocale")
def test_format_local_jpy(mock_setlocale, jpy: Currency) -> None:
    """JPY should use comma grouping (ja-JP locale)."""
    mock_setlocale.return_value = "C"

    with patch(
        "walletcard.formatting.locale.format_string", return_value="1,000"
    ) as mock_fmt:
        result = format_local(1000, jpy)
        assert result == "¥1,000"
        mock_fmt.assert_called_once_with("%d", 1000, grouping=True)


@patch("walletcard.formatting.locale.setlocale")
def test_format_local_clp(mock_setlocale, clp: Currency) -> None:
    """CLP should use dot grouping (es-CL locale)."""
    mock_setlocale.return_value = "C"

    with patch(
        "walletcard.formatting.locale.format_string", return_value="1.000"
    ) as mock_fmt:
        result = format_local(1000, clp)
        assert result == "$1.000"
        mock_fmt.assert_called_once_with("%d", 1000, grouping=True)


@patch("walletcard.formatting.locale.setlocale", side_effect=locale_mod.Error)
def test_format_local_locale_fallback(mock_setlocale, jpy: Currency) -> None:
    """If locale is unavailable, fall back to plain symbol+number."""
    result = format_local(1000, jpy)
    assert result == "¥1000"


# ---------------------------------------------------------------------------
# format_usd
# ---------------------------------------------------------------------------


@patch("walletcard.formatting.locale.setlocale")
def test_format_usd_small_amount(mock_setlocale) -> None:
    """Amounts < $1.00 should show two decimal places."""
    mock_setlocale.return_value = "C"

    with patch(
        "walletcard.formatting.locale.format_string", return_value="0.68"
    ) as mock_fmt:
        result = format_usd(0.68)
        assert result == "$0.68"
        mock_fmt.assert_called_once_with("%.2f", 0.68, grouping=True)


@patch("walletcard.formatting.locale.setlocale")
def test_format_usd_whole_number(mock_setlocale) -> None:
    """Whole-number USD amounts should show no decimal places."""
    mock_setlocale.return_value = "C"

    with patch(
        "walletcard.formatting.locale.format_string", return_value="345"
    ) as mock_fmt:
        result = format_usd(345.0)
        assert result == "$345"
        mock_fmt.assert_called_once_with("%.0f", 345.0, grouping=True)


@patch("walletcard.formatting.locale.setlocale")
def test_format_usd_mixed(mock_setlocale) -> None:
    """Non-whole amounts >= $1.00 should show two decimal places."""
    mock_setlocale.return_value = "C"

    with patch(
        "walletcard.formatting.locale.format_string", return_value="13.60"
    ) as mock_fmt:
        result = format_usd(13.60)
        assert result == "$13.60"
        mock_fmt.assert_called_once_with("%.2f", 13.60, grouping=True)


@patch("walletcard.formatting.locale.setlocale", side_effect=locale_mod.Error)
def test_format_usd_fallback(mock_setlocale) -> None:
    """If locale is unavailable, use plain Python formatting."""
    assert format_usd(0.68) == "$0.68"
    assert format_usd(345.0) == "$345"
    assert format_usd(13.60) == "$13.60"
