"""
Tests for conjured items, which are a new feature.
Unlike the refactoring tests, these expectations come from
GildedRoseRequirements.md, as the original code had no conjured items to record.
"""

from gilded_rose import GildedRose, Item

# Item type:
CONJURED: str = "Conjured Mana Cake"

# (sell_in, quality, expected_sell_in, expected_quality) after one day.
CONJURED_CASES: list[tuple[int, int, int, int]] = [
    # Twice as fast as a normal item's -1 before the sell date.
    (11, 10, 10, 8),
    (1, 10, 0, 8),
    # Twice as fast again once the sell date has passed.
    (0, 10, -1, 6),
    (-1, 10, -2, 6),
    (0, 50, -1, 46),
    # Landing exactly on the minimum quality.
    (5, 2, 4, 0),
    (0, 4, -1, 0),
    # Never below the minimum quality.
    (5, 1, 4, 0),
    (0, 3, -1, 0),
    # Already at the minimum quality.
    (5, 0, 4, 0),
    (0, 0, -1, 0),
]


def test_update_quality_one_day_for_conjured_items() -> None:
    """Conjured items degrade twice as fast as normal items, never below the floor."""
    items: list[Item] = [
        Item(CONJURED, sell_in, quality) for sell_in, quality, _, _ in CONJURED_CASES
    ]
    GildedRose(items).update_quality()
    assert [(item.sell_in, item.quality) for item in items] == [
        (sell_in, quality) for _, _, sell_in, quality in CONJURED_CASES
    ]
