"""
Combinatorial tests running update_quality for one day over every input option.
Useful for refactoring.
"""

import itertools

from gilded_rose import GildedRose, Item

# All significantly different inputs to GildedRose.update_quality().
# I.e. all significantly different sets of items.

# Item types:
NORMAL: str = "+5 Dexterity Vest"
AGED_BRIE: str = "Aged Brie"
BACKSTAGE_PASS: str = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS: str = "Sulfuras, Hand of Ragnaros"

# Either side of the 10 day, 5 day and sell by date boundaries.
SELL_INS: tuple[int, ...] = (11, 10, 6, 5, 1, 0, -1)

# Qualities:
# At the quality floor of 0 and ceiling of 50, and for each daily step size
# (-1, -2 and +1, +2, +3): landing exactly on the limit and overshooting it.
QUALITIES: tuple[int, ...] = (0, 1, 2, 47, 48, 49, 50)
SULFURAS_QUALITY: int = 80

# Every combination of (name, sell_in, quality) the inventory can start with.
# Brute force coverage of all valid combinations, as quick to write and run.
INPUTS: list[tuple[str, int, int]] = [
    *itertools.product((NORMAL, AGED_BRIE, BACKSTAGE_PASS), SELL_INS, QUALITIES),
    *itertools.product((SULFURAS,), SELL_INS, (SULFURAS_QUALITY,)),
]

# (sell_in, quality) of each item in INPUTS after one day, in the same order.
# Recorded by running update_quality on INPUTS, as in approval testing, so these
# describe the behaviour of the original, unrefactored, assumed to be correct code.
EXPECTED_OUTPUTS: list[tuple[int, int]] = [
    (10, 0),  # +5 Dexterity Vest, sell_in=11, quality=0
    (10, 0),  # +5 Dexterity Vest, sell_in=11, quality=1
    (10, 1),  # +5 Dexterity Vest, sell_in=11, quality=2
    (10, 46),  # +5 Dexterity Vest, sell_in=11, quality=47
    (10, 47),  # +5 Dexterity Vest, sell_in=11, quality=48
    (10, 48),  # +5 Dexterity Vest, sell_in=11, quality=49
    (10, 49),  # +5 Dexterity Vest, sell_in=11, quality=50
    (9, 0),  # +5 Dexterity Vest, sell_in=10, quality=0
    (9, 0),  # +5 Dexterity Vest, sell_in=10, quality=1
    (9, 1),  # +5 Dexterity Vest, sell_in=10, quality=2
    (9, 46),  # +5 Dexterity Vest, sell_in=10, quality=47
    (9, 47),  # +5 Dexterity Vest, sell_in=10, quality=48
    (9, 48),  # +5 Dexterity Vest, sell_in=10, quality=49
    (9, 49),  # +5 Dexterity Vest, sell_in=10, quality=50
    (5, 0),  # +5 Dexterity Vest, sell_in=6, quality=0
    (5, 0),  # +5 Dexterity Vest, sell_in=6, quality=1
    (5, 1),  # +5 Dexterity Vest, sell_in=6, quality=2
    (5, 46),  # +5 Dexterity Vest, sell_in=6, quality=47
    (5, 47),  # +5 Dexterity Vest, sell_in=6, quality=48
    (5, 48),  # +5 Dexterity Vest, sell_in=6, quality=49
    (5, 49),  # +5 Dexterity Vest, sell_in=6, quality=50
    (4, 0),  # +5 Dexterity Vest, sell_in=5, quality=0
    (4, 0),  # +5 Dexterity Vest, sell_in=5, quality=1
    (4, 1),  # +5 Dexterity Vest, sell_in=5, quality=2
    (4, 46),  # +5 Dexterity Vest, sell_in=5, quality=47
    (4, 47),  # +5 Dexterity Vest, sell_in=5, quality=48
    (4, 48),  # +5 Dexterity Vest, sell_in=5, quality=49
    (4, 49),  # +5 Dexterity Vest, sell_in=5, quality=50
    (0, 0),  # +5 Dexterity Vest, sell_in=1, quality=0
    (0, 0),  # +5 Dexterity Vest, sell_in=1, quality=1
    (0, 1),  # +5 Dexterity Vest, sell_in=1, quality=2
    (0, 46),  # +5 Dexterity Vest, sell_in=1, quality=47
    (0, 47),  # +5 Dexterity Vest, sell_in=1, quality=48
    (0, 48),  # +5 Dexterity Vest, sell_in=1, quality=49
    (0, 49),  # +5 Dexterity Vest, sell_in=1, quality=50
    (-1, 0),  # +5 Dexterity Vest, sell_in=0, quality=0
    (-1, 0),  # +5 Dexterity Vest, sell_in=0, quality=1
    (-1, 0),  # +5 Dexterity Vest, sell_in=0, quality=2
    (-1, 45),  # +5 Dexterity Vest, sell_in=0, quality=47
    (-1, 46),  # +5 Dexterity Vest, sell_in=0, quality=48
    (-1, 47),  # +5 Dexterity Vest, sell_in=0, quality=49
    (-1, 48),  # +5 Dexterity Vest, sell_in=0, quality=50
    (-2, 0),  # +5 Dexterity Vest, sell_in=-1, quality=0
    (-2, 0),  # +5 Dexterity Vest, sell_in=-1, quality=1
    (-2, 0),  # +5 Dexterity Vest, sell_in=-1, quality=2
    (-2, 45),  # +5 Dexterity Vest, sell_in=-1, quality=47
    (-2, 46),  # +5 Dexterity Vest, sell_in=-1, quality=48
    (-2, 47),  # +5 Dexterity Vest, sell_in=-1, quality=49
    (-2, 48),  # +5 Dexterity Vest, sell_in=-1, quality=50
    (10, 1),  # Aged Brie, sell_in=11, quality=0
    (10, 2),  # Aged Brie, sell_in=11, quality=1
    (10, 3),  # Aged Brie, sell_in=11, quality=2
    (10, 48),  # Aged Brie, sell_in=11, quality=47
    (10, 49),  # Aged Brie, sell_in=11, quality=48
    (10, 50),  # Aged Brie, sell_in=11, quality=49
    (10, 50),  # Aged Brie, sell_in=11, quality=50
    (9, 1),  # Aged Brie, sell_in=10, quality=0
    (9, 2),  # Aged Brie, sell_in=10, quality=1
    (9, 3),  # Aged Brie, sell_in=10, quality=2
    (9, 48),  # Aged Brie, sell_in=10, quality=47
    (9, 49),  # Aged Brie, sell_in=10, quality=48
    (9, 50),  # Aged Brie, sell_in=10, quality=49
    (9, 50),  # Aged Brie, sell_in=10, quality=50
    (5, 1),  # Aged Brie, sell_in=6, quality=0
    (5, 2),  # Aged Brie, sell_in=6, quality=1
    (5, 3),  # Aged Brie, sell_in=6, quality=2
    (5, 48),  # Aged Brie, sell_in=6, quality=47
    (5, 49),  # Aged Brie, sell_in=6, quality=48
    (5, 50),  # Aged Brie, sell_in=6, quality=49
    (5, 50),  # Aged Brie, sell_in=6, quality=50
    (4, 1),  # Aged Brie, sell_in=5, quality=0
    (4, 2),  # Aged Brie, sell_in=5, quality=1
    (4, 3),  # Aged Brie, sell_in=5, quality=2
    (4, 48),  # Aged Brie, sell_in=5, quality=47
    (4, 49),  # Aged Brie, sell_in=5, quality=48
    (4, 50),  # Aged Brie, sell_in=5, quality=49
    (4, 50),  # Aged Brie, sell_in=5, quality=50
    (0, 1),  # Aged Brie, sell_in=1, quality=0
    (0, 2),  # Aged Brie, sell_in=1, quality=1
    (0, 3),  # Aged Brie, sell_in=1, quality=2
    (0, 48),  # Aged Brie, sell_in=1, quality=47
    (0, 49),  # Aged Brie, sell_in=1, quality=48
    (0, 50),  # Aged Brie, sell_in=1, quality=49
    (0, 50),  # Aged Brie, sell_in=1, quality=50
    (-1, 2),  # Aged Brie, sell_in=0, quality=0
    (-1, 3),  # Aged Brie, sell_in=0, quality=1
    (-1, 4),  # Aged Brie, sell_in=0, quality=2
    (-1, 49),  # Aged Brie, sell_in=0, quality=47
    (-1, 50),  # Aged Brie, sell_in=0, quality=48
    (-1, 50),  # Aged Brie, sell_in=0, quality=49
    (-1, 50),  # Aged Brie, sell_in=0, quality=50
    (-2, 2),  # Aged Brie, sell_in=-1, quality=0
    (-2, 3),  # Aged Brie, sell_in=-1, quality=1
    (-2, 4),  # Aged Brie, sell_in=-1, quality=2
    (-2, 49),  # Aged Brie, sell_in=-1, quality=47
    (-2, 50),  # Aged Brie, sell_in=-1, quality=48
    (-2, 50),  # Aged Brie, sell_in=-1, quality=49
    (-2, 50),  # Aged Brie, sell_in=-1, quality=50
    (10, 1),  # Backstage passes to a TAFKAL80ETC concert, sell_in=11, quality=0
    (10, 2),  # Backstage passes to a TAFKAL80ETC concert, sell_in=11, quality=1
    (10, 3),  # Backstage passes to a TAFKAL80ETC concert, sell_in=11, quality=2
    (10, 48),  # Backstage passes to a TAFKAL80ETC concert, sell_in=11, quality=47
    (10, 49),  # Backstage passes to a TAFKAL80ETC concert, sell_in=11, quality=48
    (10, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=11, quality=49
    (10, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=11, quality=50
    (9, 2),  # Backstage passes to a TAFKAL80ETC concert, sell_in=10, quality=0
    (9, 3),  # Backstage passes to a TAFKAL80ETC concert, sell_in=10, quality=1
    (9, 4),  # Backstage passes to a TAFKAL80ETC concert, sell_in=10, quality=2
    (9, 49),  # Backstage passes to a TAFKAL80ETC concert, sell_in=10, quality=47
    (9, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=10, quality=48
    (9, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=10, quality=49
    (9, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=10, quality=50
    (5, 2),  # Backstage passes to a TAFKAL80ETC concert, sell_in=6, quality=0
    (5, 3),  # Backstage passes to a TAFKAL80ETC concert, sell_in=6, quality=1
    (5, 4),  # Backstage passes to a TAFKAL80ETC concert, sell_in=6, quality=2
    (5, 49),  # Backstage passes to a TAFKAL80ETC concert, sell_in=6, quality=47
    (5, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=6, quality=48
    (5, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=6, quality=49
    (5, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=6, quality=50
    (4, 3),  # Backstage passes to a TAFKAL80ETC concert, sell_in=5, quality=0
    (4, 4),  # Backstage passes to a TAFKAL80ETC concert, sell_in=5, quality=1
    (4, 5),  # Backstage passes to a TAFKAL80ETC concert, sell_in=5, quality=2
    (4, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=5, quality=47
    (4, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=5, quality=48
    (4, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=5, quality=49
    (4, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=5, quality=50
    (0, 3),  # Backstage passes to a TAFKAL80ETC concert, sell_in=1, quality=0
    (0, 4),  # Backstage passes to a TAFKAL80ETC concert, sell_in=1, quality=1
    (0, 5),  # Backstage passes to a TAFKAL80ETC concert, sell_in=1, quality=2
    (0, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=1, quality=47
    (0, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=1, quality=48
    (0, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=1, quality=49
    (0, 50),  # Backstage passes to a TAFKAL80ETC concert, sell_in=1, quality=50
    (-1, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=0, quality=0
    (-1, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=0, quality=1
    (-1, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=0, quality=2
    (-1, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=0, quality=47
    (-1, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=0, quality=48
    (-1, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=0, quality=49
    (-1, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=0, quality=50
    (-2, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=-1, quality=0
    (-2, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=-1, quality=1
    (-2, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=-1, quality=2
    (-2, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=-1, quality=47
    (-2, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=-1, quality=48
    (-2, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=-1, quality=49
    (-2, 0),  # Backstage passes to a TAFKAL80ETC concert, sell_in=-1, quality=50
    (11, 80),  # Sulfuras, Hand of Ragnaros, sell_in=11, quality=80
    (10, 80),  # Sulfuras, Hand of Ragnaros, sell_in=10, quality=80
    (6, 80),  # Sulfuras, Hand of Ragnaros, sell_in=6, quality=80
    (5, 80),  # Sulfuras, Hand of Ragnaros, sell_in=5, quality=80
    (1, 80),  # Sulfuras, Hand of Ragnaros, sell_in=1, quality=80
    (0, 80),  # Sulfuras, Hand of Ragnaros, sell_in=0, quality=80
    (-1, 80),  # Sulfuras, Hand of Ragnaros, sell_in=-1, quality=80
]


def test_expected_outputs_match_inputs() -> None:
    """Double check the hard coded (approved) outputs have one row per input."""
    assert len(EXPECTED_OUTPUTS) == len(INPUTS)


def test_update_quality_one_day() -> None:
    """One day's update over an inventory of every input gives the expected outputs."""
    items: list[Item] = [
        Item(name, sell_in, quality) for name, sell_in, quality in INPUTS
    ]
    GildedRose(items).update_quality()
    assert [(item.sell_in, item.quality) for item in items] == EXPECTED_OUTPUTS


def test_item_repr() -> None:
    """Items describe themselves as name, sell_in and quality."""
    assert repr(Item(AGED_BRIE, 2, 0)) == "Aged Brie, 2, 0"
