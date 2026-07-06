"""Generate an extended list of denominations using a 1-2-5 progression."""

from __future__ import annotations


def generate_denominations(
    configured: list[int],
    *,
    max_local_value: int = 5_000_000,
) -> list[int]:
    """Extend a list of configured denominations with a 1-2-5 progression.

    Preserves all configured values, then fills in any missing 1-2-5 values
    between the smallest configured denomination and *max_local_value*.

    A "1-2-5 progression" means values of the form ``n × 10^k`` where
    ``n ∈ {1, 2, 5}`` and ``k ≥ 0``.

    Parameters
    ----------
    configured : list[int]
        The configured denominations for a currency (e.g. ``[100, 500, …]``).
    max_local_value : int
        Upper bound for generated denominations (default 5,000 000).

    Returns
    -------
    list[int]
        Sorted, deduplicated denominations covering the 1-2-5 progression
        from the smallest configured value up to *max_local_value*.

    Example
    -------
    >>> generate_denominations([100, 500, 1000, 2000, 5000, 10000])
    [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000,
     200000, 500000, 1000000, 2000000, 5000000]
    """
    min_val = min(configured)
    values: set[int] = set(configured)

    # Determine the starting power of 10 at or below the smallest configured
    # value — e.g.  100 for 100,  1 for 800.  This naturally extends the list
    # "downward" with any missing 1-2-5 entries between the configured values.
    start_power = 10 ** (len(str(min_val)) - 1)

    power = start_power
    while power <= max_local_value:
        for n in (1, 2, 5):
            v = n * power
            if v <= max_local_value:
                values.add(v)
        power *= 10

    return sorted(values)