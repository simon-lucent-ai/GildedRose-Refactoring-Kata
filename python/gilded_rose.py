"""Main logic for Inn.

Each kind of stock is a class that knows what a day does to it, and make_item
picks that class from an item's name. GildedRose moves a whole inventory on by
a day without knowing any of the rules itself.
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import ClassVar


# The Item class belongs to the goblin and must not be altered, so its warnings
# are silenced instead of fixed. The disables sit on the class line so that they
# cover this class only, rather than everything after it in the file.
class Item:  # pylint: disable=missing-class-docstring,consider-using-f-string
    def __init__(self, name, sell_in, quality):  # type: ignore[no-untyped-def]
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):  # type: ignore[no-untyped-def]
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class InnItem(Item, ABC):
    """Anything in the inn's stock, which a day may or may not change."""

    # The exact name of the product this class is for.
    NAME: ClassVar[str]

    @abstractmethod
    def update(self) -> None:
        """Move the item on by one day."""


class AgingItem(InnItem, ABC):
    """
    Stock that ages.

    Its "sell_in" runs down and its quality changes by
    a defined amount each day and stays constrained within limits.
    """

    MIN_QUALITY = 0
    MAX_QUALITY = 50

    def update(self) -> None:
        """Apply one day's quality change, then age the item."""

        quality = self.quality + self._quality_change()
        self.quality = max(self.MIN_QUALITY, min(self.MAX_QUALITY, quality))
        self.sell_in -= 1

    @abstractmethod
    def _quality_change(self) -> int:
        """Return the day's quality change, before the limits are applied."""

    @property
    def _past_sell_date(self) -> bool:
        """Whether the sell by date has already gone."""

        # bool() because sell_in comes from the goblin's untyped class, so the
        # comparison is Any as far as the type checker is concerned.
        return bool(self.sell_in <= 0)


class NormalItem(AgingItem):
    """An ordinary item, which loses quality as it ages."""

    def _quality_change(self) -> int:
        # Once the sell by date has passed, `Quality` degrades twice as fast.
        return -2 if self._past_sell_date else -1


class AgedBrie(AgingItem):
    """
    Aged Brie gains quality with age, rather than losing it.

    Explicitally:  The quality also increases faster after the sell by date.
    """

    NAME = "Aged Brie"

    def _quality_change(self) -> int:
        return 2 if self._past_sell_date else 1


class BackstagePass(AgingItem):
    """A backstage pass gains quality as its concert nears, then is worthless."""

    NAME = "Backstage passes to a TAFKAL80ETC concert"

    # Days left at or below which the pass gains that much quality a day.
    GAINS_TWO_FROM = 10
    GAINS_THREE_FROM = 5

    def _quality_change(self) -> int:
        if self._past_sell_date:
            return -self.quality  # Worthless after the concert so change to zero.
        if self.sell_in <= self.GAINS_THREE_FROM:
            return 3
        if self.sell_in <= self.GAINS_TWO_FROM:
            return 2
        return 1


class Conjured(NormalItem):
    """Conjured stock degrades twice as fast as ordinary stock.

    The requirements describe conjured items as a category rather than a single
    product, so any name starting with NAME_PREFIX is conjured.
    """

    NAME_PREFIX = "Conjured"

    def _quality_change(self) -> int:
        return 2 * super()._quality_change()


class Sulfuras(InnItem):
    """Sulfuras is a legendary InnItem: it never has to be sold and never changes.

    Its quality belongs to the item itself rather than assigned, so the
    caller gives only a name and a sell_in.
    """

    NAME = "Sulfuras, Hand of Ragnaros"
    QUALITY = 80

    def __init__(self, name: str, sell_in: int, _quality: int = QUALITY) -> None:
        """Build a legendary item, ignoring any quality given for it."""

        super().__init__(name, sell_in, self.QUALITY)

    def update(self) -> None:
        """Leave the item exactly as it is."""


# The one product names with rules of their own.
_ITEM_CLASSES: dict[str, type[InnItem]] = {
    cls.NAME: cls for cls in (AgedBrie, BackstagePass, Sulfuras)
}


def make_item(name: str, sell_in: int, quality: int) -> InnItem:
    """Build the right kind of item for a name.

    Conjured stock is a category, so it is matched on the start of the name.
    Any other name the inn does not know is an ordinary item.
    """

    if name in _ITEM_CLASSES:
        return _ITEM_CLASSES[name](name, sell_in, quality)
    if name.startswith(Conjured.NAME_PREFIX):
        return Conjured(name, sell_in, quality)
    return NormalItem(name, sell_in, quality)


class GildedRose:
    """The inn's inventory, which can be updated at the end of each day."""

    def __init__(self, items: Sequence[InnItem]) -> None:
        self.items = items

    def update_quality(self) -> None:
        """Move every item on by one day."""

        for item in self.items:
            item.update()
