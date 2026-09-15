"""Main logic for Inn."""

from collections.abc import Sequence
from typing import Protocol

MIN_QUALITY = 0
MAX_QUALITY = 50

# Days left when a backstage pass starts gaining more than one quality a day.
BACKSTAGE_PASS_DOUBLE_DAYS = 10
BACKSTAGE_PASS_TRIPLE_DAYS = 5

AGED_BRIE = "Aged Brie"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"


class ItemLike(Protocol):
    """
    The parts of the goblin's Item class this module relies on.
    For type checking.
    """

    name: str
    sell_in: int
    quality: int


class GildedRose:
    """The inn's inventory, which can be updated at the end of each day."""

    def __init__(self, items: Sequence[ItemLike]) -> None:
        self.items = items

    def update_quality(self) -> None:
        """Update the sell_in and quality of every item."""

        for item in self.items:
            if item.name == SULFURAS:
                continue  # Legendary: never has to be sold and never changes.

            quality = item.quality + _quality_change(item)
            item.quality = max(MIN_QUALITY, min(MAX_QUALITY, quality))

            # Always track age of items. Do it after quality check as in original code.
            item.sell_in -= 1


def _quality_change(item: ItemLike) -> int:
    """Return how much an item's quality changes in a day, regardless of limits."""

    past_sell_date: bool = item.sell_in <= 0

    # Once the sell by date has passed, `Quality` degrades twice as fast.
    degradation = -2 if past_sell_date else -1

    if item.name == AGED_BRIE:
        return -degradation  # Positive change as brie gets better with age.

    if item.name == BACKSTAGE_PASS:
        if past_sell_date:
            return -item.quality  # Worthless after the concert so change to zero.
        if item.sell_in <= BACKSTAGE_PASS_TRIPLE_DAYS:
            return 3
        if item.sell_in <= BACKSTAGE_PASS_DOUBLE_DAYS:
            return 2
        return 1

    return degradation


# The Item class belongs to the goblin and must not be altered, so its warnings
# are silenced instead of fixed.
# pylint: disable=missing-class-docstring,consider-using-f-string
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
