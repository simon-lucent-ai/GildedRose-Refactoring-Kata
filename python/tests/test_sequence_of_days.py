"""
Tests following a single item through a sequence of days.
"""

from gilded_rose import GildedRose, make_item

# Item type:
BACKSTAGE_PASS: str = "Backstage passes to a TAFKAL80ETC concert"


def test_backstage_pass_over_several_days() -> None:
    """A pass gains more as its concert nears, then is worthless the day after.

    Taken from the requirements rather than recorded from the code, so the whole
    arc of an item is written down in one place.
    """
    item = make_item(BACKSTAGE_PASS, 11, 20)
    inn = GildedRose([item])

    days = []
    for _ in range(12):
        inn.update_quality()
        days.append((item.sell_in, item.quality))

    assert days == [
        (10, 21),  # More than 10 days left, so +1.
        (9, 23),  # 10 days or less, so +2.
        (8, 25),
        (7, 27),
        (6, 29),
        (5, 31),
        (4, 34),  # 5 days or less, so +3.
        (3, 37),
        (2, 40),
        (1, 43),
        (0, 46),
        (-1, 0),  # The concert has passed, so it is worthless.
    ]
