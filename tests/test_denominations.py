"""Tests for walletcard.denominations."""

from walletcard.denominations import generate_denominations


def test_jpy_default_progression() -> None:
    """JPY's configured list should produce the expected 1-2-5 progression."""
    configured = [100, 500, 1000, 2000, 5000, 10000]
    result = generate_denominations(configured)
    expected = [
        100,
        200,
        500,
        1000,
        2000,
        5000,
        10000,
        20000,
        50000,
        100000,
        200000,
        500000,
        1000000,
        2000000,
        5000000,
    ]
    assert result == expected


def test_downward_extension() -> None:
    """The progression starts at the power of 10 of the smallest configured value,
    so values below that power are not included."""
    configured = [1000, 5000]
    result = generate_denominations(configured)
    # start_power = 10 ** (4 - 1) = 1000
    # So the progression is: 1000, 2000, 5000, 10000, 20000, ...
    assert result[0] == 1000
    assert 100 not in result
    assert 200 not in result
    assert 500 not in result
    assert 1000 in result
    assert 2000 in result
    assert 5000 in result


def test_deduplication() -> None:
    """Configured values that overlap the progression should not be duplicated."""
    configured = [100, 200, 500]
    result = generate_denominations(configured)
    # Count occurrences of each value
    assert result.count(100) == 1
    assert result.count(200) == 1
    assert result.count(500) == 1


def test_sorted_ascending() -> None:
    """The returned list must always be sorted ascending."""
    configured = [10000, 100, 5000]
    result = generate_denominations(configured)
    assert result == sorted(result)


def test_custom_max_value() -> None:
    """The max_local_value parameter caps the progression."""
    configured = [100]
    result = generate_denominations(configured, max_local_value=1000)
    assert result == [100, 200, 500, 1000]


def test_single_configured_value() -> None:
    """A single configured value should still produce a full progression
    from its power-of-10 base up to the default max."""
    result = generate_denominations([500])
    # start_power = 10 ** (3 - 1) = 100
    # progression: 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000,
    #              100000, 200000, 500000, 1000000, 2000000, 5000000
    assert result[0] == 100
    assert result[-1] == 5_000_000
    assert 500 in result
    assert 1000 in result
    assert 50000 in result