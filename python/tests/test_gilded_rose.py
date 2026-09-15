# -*- coding: utf-8 -*-

# This module is to provide all tests necessary for refactoring


from gilded_rose import Item, GildedRose


def test_foo():
    items = [Item("foo", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert "fixme" == items[0].name
