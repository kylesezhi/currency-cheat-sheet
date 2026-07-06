"""Tests for walletcard.rates."""

import json
from unittest.mock import patch

import pytest

from walletcard.rates import load_rate


def _mock_response(data: dict) -> bytes:
    return json.dumps(data).encode()


@patch("walletcard.rates.urlopen")
def test_successful_rate_fetch(mock_urlopen) -> None:
    """A successful API response returns the expected rate and rate_text."""
    mock_urlopen.return_value.read.return_value = _mock_response(
        {"result": "success", "rates": {"USD": 0.0068}}
    )
    mock_urlopen.return_value.__enter__.return_value = mock_urlopen.return_value

    rate, rate_text = load_rate("JPY")

    assert rate == 0.0068
    assert "USD" in rate_text
    assert "JPY" in rate_text


@patch("walletcard.rates.urlopen")
def test_non_success_result(mock_urlopen) -> None:
    """If the API returns result != 'success', the program should exit."""
    mock_urlopen.return_value.read.return_value = _mock_response(
        {"result": "error", "rates": {}}
    )
    mock_urlopen.return_value.__enter__.return_value = mock_urlopen.return_value

    with pytest.raises(SystemExit):
        load_rate("JPY")


@patch("walletcard.rates.urlopen")
def test_network_error(mock_urlopen) -> None:
    """A URLError should cause a SystemExit."""
    from urllib.error import URLError

    mock_urlopen.side_effect = URLError("No network")

    with pytest.raises(SystemExit):
        load_rate("JPY")


@patch("walletcard.rates.urlopen")
def test_rate_text_large_inverse(mock_urlopen) -> None:
    """When 1 USD = many local units, rate_text should show integer format."""
    mock_urlopen.return_value.read.return_value = _mock_response(
        {"result": "success", "rates": {"USD": 0.00074}}
    )
    mock_urlopen.return_value.__enter__.return_value = mock_urlopen.return_value

    _, rate_text = load_rate("KRW")

    # 1 / 0.00074 ≈ 1351.35 → "1 USD ≈ 1,351 KRW"
    assert "1 USD ≈" in rate_text
    assert "KRW" in rate_text
    # Should be integer-formatted (no decimal places for values >= 1)
    assert "," in rate_text or "1 351" in rate_text


@patch("walletcard.rates.urlopen")
def test_rate_text_small_inverse(mock_urlopen) -> None:
    """When 1 USD = < 1 local unit, rate_text should show two decimal places."""
    mock_urlopen.return_value.read.return_value = _mock_response(
        {"result": "success", "rates": {"USD": 1.5}}
    )
    mock_urlopen.return_value.__enter__.return_value = mock_urlopen.return_value

    _, rate_text = load_rate("XXX")

    # 1 / 1.5 ≈ 0.67 → "1 USD ≈ 0.67 XXX"
    assert "1 USD ≈ 0" in rate_text