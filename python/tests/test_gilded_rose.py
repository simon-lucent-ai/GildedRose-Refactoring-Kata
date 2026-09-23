"""
Combinatorial tests running update_quality for one day over every input option.
Useful for refactoring.
"""

import itertools

from gilded_rose import GildedRose, InnItem, Item, Sulfuras, make_item

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

# Every significantly different case, as what an item starts the day with and
# what it ends it with: (name, sell_in, quality, expected_sell_in,
# expected_quality). The starting values are every combination of the lists
# above, so between them they cover every significantly different set of items
# GildedRose.update_quality() can be given. The expected values were recorded by
# running the original code, as in approval testing, so they describe the
# behaviour of the unrefactored, assumed to be correct code.
CASES: list[tuple[str, int, int, int, int]] = [
    # Ordinary stock: -1 a day, -2 once the sell date has passed.
    (NORMAL, 11, 0, 10, 0),
    (NORMAL, 11, 1, 10, 0),
    (NORMAL, 11, 2, 10, 1),
    (NORMAL, 11, 47, 10, 46),
    (NORMAL, 11, 48, 10, 47),
    (NORMAL, 11, 49, 10, 48),
    (NORMAL, 11, 50, 10, 49),
    (NORMAL, 10, 0, 9, 0),
    (NORMAL, 10, 1, 9, 0),
    (NORMAL, 10, 2, 9, 1),
    (NORMAL, 10, 47, 9, 46),
    (NORMAL, 10, 48, 9, 47),
    (NORMAL, 10, 49, 9, 48),
    (NORMAL, 10, 50, 9, 49),
    (NORMAL, 6, 0, 5, 0),
    (NORMAL, 6, 1, 5, 0),
    (NORMAL, 6, 2, 5, 1),
    (NORMAL, 6, 47, 5, 46),
    (NORMAL, 6, 48, 5, 47),
    (NORMAL, 6, 49, 5, 48),
    (NORMAL, 6, 50, 5, 49),
    (NORMAL, 5, 0, 4, 0),
    (NORMAL, 5, 1, 4, 0),
    (NORMAL, 5, 2, 4, 1),
    (NORMAL, 5, 47, 4, 46),
    (NORMAL, 5, 48, 4, 47),
    (NORMAL, 5, 49, 4, 48),
    (NORMAL, 5, 50, 4, 49),
    (NORMAL, 1, 0, 0, 0),
    (NORMAL, 1, 1, 0, 0),
    (NORMAL, 1, 2, 0, 1),
    (NORMAL, 1, 47, 0, 46),
    (NORMAL, 1, 48, 0, 47),
    (NORMAL, 1, 49, 0, 48),
    (NORMAL, 1, 50, 0, 49),
    (NORMAL, 0, 0, -1, 0),
    (NORMAL, 0, 1, -1, 0),
    (NORMAL, 0, 2, -1, 0),
    (NORMAL, 0, 47, -1, 45),
    (NORMAL, 0, 48, -1, 46),
    (NORMAL, 0, 49, -1, 47),
    (NORMAL, 0, 50, -1, 48),
    (NORMAL, -1, 0, -2, 0),
    (NORMAL, -1, 1, -2, 0),
    (NORMAL, -1, 2, -2, 0),
    (NORMAL, -1, 47, -2, 45),
    (NORMAL, -1, 48, -2, 46),
    (NORMAL, -1, 49, -2, 47),
    (NORMAL, -1, 50, -2, 48),
    # Aged Brie: +1 a day, +2 once the sell date has passed.
    (AGED_BRIE, 11, 0, 10, 1),
    (AGED_BRIE, 11, 1, 10, 2),
    (AGED_BRIE, 11, 2, 10, 3),
    (AGED_BRIE, 11, 47, 10, 48),
    (AGED_BRIE, 11, 48, 10, 49),
    (AGED_BRIE, 11, 49, 10, 50),
    (AGED_BRIE, 11, 50, 10, 50),
    (AGED_BRIE, 10, 0, 9, 1),
    (AGED_BRIE, 10, 1, 9, 2),
    (AGED_BRIE, 10, 2, 9, 3),
    (AGED_BRIE, 10, 47, 9, 48),
    (AGED_BRIE, 10, 48, 9, 49),
    (AGED_BRIE, 10, 49, 9, 50),
    (AGED_BRIE, 10, 50, 9, 50),
    (AGED_BRIE, 6, 0, 5, 1),
    (AGED_BRIE, 6, 1, 5, 2),
    (AGED_BRIE, 6, 2, 5, 3),
    (AGED_BRIE, 6, 47, 5, 48),
    (AGED_BRIE, 6, 48, 5, 49),
    (AGED_BRIE, 6, 49, 5, 50),
    (AGED_BRIE, 6, 50, 5, 50),
    (AGED_BRIE, 5, 0, 4, 1),
    (AGED_BRIE, 5, 1, 4, 2),
    (AGED_BRIE, 5, 2, 4, 3),
    (AGED_BRIE, 5, 47, 4, 48),
    (AGED_BRIE, 5, 48, 4, 49),
    (AGED_BRIE, 5, 49, 4, 50),
    (AGED_BRIE, 5, 50, 4, 50),
    (AGED_BRIE, 1, 0, 0, 1),
    (AGED_BRIE, 1, 1, 0, 2),
    (AGED_BRIE, 1, 2, 0, 3),
    (AGED_BRIE, 1, 47, 0, 48),
    (AGED_BRIE, 1, 48, 0, 49),
    (AGED_BRIE, 1, 49, 0, 50),
    (AGED_BRIE, 1, 50, 0, 50),
    (AGED_BRIE, 0, 0, -1, 2),
    (AGED_BRIE, 0, 1, -1, 3),
    (AGED_BRIE, 0, 2, -1, 4),
    (AGED_BRIE, 0, 47, -1, 49),
    (AGED_BRIE, 0, 48, -1, 50),
    (AGED_BRIE, 0, 49, -1, 50),
    (AGED_BRIE, 0, 50, -1, 50),
    (AGED_BRIE, -1, 0, -2, 2),
    (AGED_BRIE, -1, 1, -2, 3),
    (AGED_BRIE, -1, 2, -2, 4),
    (AGED_BRIE, -1, 47, -2, 49),
    (AGED_BRIE, -1, 48, -2, 50),
    (AGED_BRIE, -1, 49, -2, 50),
    (AGED_BRIE, -1, 50, -2, 50),
    # Backstage passes: +1, +2 from 10 days, +3 from 5, then worthless.
    (BACKSTAGE_PASS, 11, 0, 10, 1),
    (BACKSTAGE_PASS, 11, 1, 10, 2),
    (BACKSTAGE_PASS, 11, 2, 10, 3),
    (BACKSTAGE_PASS, 11, 47, 10, 48),
    (BACKSTAGE_PASS, 11, 48, 10, 49),
    (BACKSTAGE_PASS, 11, 49, 10, 50),
    (BACKSTAGE_PASS, 11, 50, 10, 50),
    (BACKSTAGE_PASS, 10, 0, 9, 2),
    (BACKSTAGE_PASS, 10, 1, 9, 3),
    (BACKSTAGE_PASS, 10, 2, 9, 4),
    (BACKSTAGE_PASS, 10, 47, 9, 49),
    (BACKSTAGE_PASS, 10, 48, 9, 50),
    (BACKSTAGE_PASS, 10, 49, 9, 50),
    (BACKSTAGE_PASS, 10, 50, 9, 50),
    (BACKSTAGE_PASS, 6, 0, 5, 2),
    (BACKSTAGE_PASS, 6, 1, 5, 3),
    (BACKSTAGE_PASS, 6, 2, 5, 4),
    (BACKSTAGE_PASS, 6, 47, 5, 49),
    (BACKSTAGE_PASS, 6, 48, 5, 50),
    (BACKSTAGE_PASS, 6, 49, 5, 50),
    (BACKSTAGE_PASS, 6, 50, 5, 50),
    (BACKSTAGE_PASS, 5, 0, 4, 3),
    (BACKSTAGE_PASS, 5, 1, 4, 4),
    (BACKSTAGE_PASS, 5, 2, 4, 5),
    (BACKSTAGE_PASS, 5, 47, 4, 50),
    (BACKSTAGE_PASS, 5, 48, 4, 50),
    (BACKSTAGE_PASS, 5, 49, 4, 50),
    (BACKSTAGE_PASS, 5, 50, 4, 50),
    (BACKSTAGE_PASS, 1, 0, 0, 3),
    (BACKSTAGE_PASS, 1, 1, 0, 4),
    (BACKSTAGE_PASS, 1, 2, 0, 5),
    (BACKSTAGE_PASS, 1, 47, 0, 50),
    (BACKSTAGE_PASS, 1, 48, 0, 50),
    (BACKSTAGE_PASS, 1, 49, 0, 50),
    (BACKSTAGE_PASS, 1, 50, 0, 50),
    (BACKSTAGE_PASS, 0, 0, -1, 0),
    (BACKSTAGE_PASS, 0, 1, -1, 0),
    (BACKSTAGE_PASS, 0, 2, -1, 0),
    (BACKSTAGE_PASS, 0, 47, -1, 0),
    (BACKSTAGE_PASS, 0, 48, -1, 0),
    (BACKSTAGE_PASS, 0, 49, -1, 0),
    (BACKSTAGE_PASS, 0, 50, -1, 0),
    (BACKSTAGE_PASS, -1, 0, -2, 0),
    (BACKSTAGE_PASS, -1, 1, -2, 0),
    (BACKSTAGE_PASS, -1, 2, -2, 0),
    (BACKSTAGE_PASS, -1, 47, -2, 0),
    (BACKSTAGE_PASS, -1, 48, -2, 0),
    (BACKSTAGE_PASS, -1, 49, -2, 0),
    (BACKSTAGE_PASS, -1, 50, -2, 0),
    # Sulfuras: never changes, and its quality comes from its own class.
    (SULFURAS, 11, Sulfuras.QUALITY, 11, 80),
    (SULFURAS, 10, Sulfuras.QUALITY, 10, 80),
    (SULFURAS, 6, Sulfuras.QUALITY, 6, 80),
    (SULFURAS, 5, Sulfuras.QUALITY, 5, 80),
    (SULFURAS, 1, Sulfuras.QUALITY, 1, 80),
    (SULFURAS, 0, Sulfuras.QUALITY, 0, 80),
    (SULFURAS, -1, Sulfuras.QUALITY, -1, 80),
]


def test_cases_cover_every_combination() -> None:
    """Double check the hard coded cases are exactly what they claim to cover.

    Guards the test data itself: a case left out would otherwise go unnoticed.
    """
    combinations = {
        *itertools.product((NORMAL, AGED_BRIE, BACKSTAGE_PASS), SELL_INS, QUALITIES),
        *itertools.product((SULFURAS,), SELL_INS, (Sulfuras.QUALITY,)),
    }
    starts = [(name, sell_in, quality) for name, sell_in, quality, _, _ in CASES]
    assert set(starts) == combinations
    assert len(starts) == len(combinations)  # no case written twice


def test_update_quality_one_day() -> None:
    """One day's update over an inventory of every case gives the expected values."""
    items: list[InnItem] = [
        make_item(name, sell_in, quality) for name, sell_in, quality, _, _ in CASES
    ]
    GildedRose(items).update_quality()
    assert [(item.sell_in, item.quality) for item in items] == [
        (sell_in, quality) for _, _, _, sell_in, quality in CASES
    ]


def test_unrecognised_names_degrade_like_normal_items() -> None:
    """A second ordinary name is treated the same as the one used elsewhere.

    Guards against a refactor that looks each name up in a table and handles
    only the ordinary name the other tests happen to use. It says nothing about
    names that near miss a special one, such as a different case or a trailing
    space.
    """
    vest = make_item(NORMAL, 5, 7)
    elixir = make_item("Elixir of the Mongoose", 5, 7)
    GildedRose([vest, elixir]).update_quality()
    assert (elixir.sell_in, elixir.quality) == (vest.sell_in, vest.quality)


def test_sulfuras_quality_comes_from_its_name() -> None:
    """The legendary item is worth 80 whatever quality it is built with.

    The recorded cases cannot show this, as every Sulfuras row in CASES
    already starts at 80.
    """
    assert make_item(SULFURAS, 5, 20).quality == 80


def test_item_repr() -> None:
    """Items describe themselves as name, sell_in and quality."""
    assert repr(Item(AGED_BRIE, 2, 0)) == "Aged Brie, 2, 0"
