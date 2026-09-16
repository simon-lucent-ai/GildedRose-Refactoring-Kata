# Gilded Rose kata attempt, based on the starting position in the original repo.

For exercise instructions see [top level README](../README.md)


# Running

Needs [PDM](https://pdm-project.org/) and Python 3.10 or later.

```bash
pdm install        # create the environment and install dependencies
pdm run check_all  # formatting, linting, type checking and tests
```

Each check can also be run on its own:

| Command | What it does |
| --- | --- |
| `pdm run format` | Reformats the code with black |
| `pdm run lint` | Runs pylint over the module and the tests |
| `pdm run typecheck` | Runs mypy over the module and the tests |
| `pdm run test` | Runs pytest with branch coverage, which must stay at 100% |


# Python environment

We use pdm to manage the python environment, dependencies and scripts for code checks and testing.

We check code for types, linting and formatting using standard tools.


# Tests

The tests are split in two, because they answer different questions.

`tests/test_gilded_rose.py` is the refactoring safety net. It covers every
combination of item type, sell_in and quality that behaves differently, with
values taken at and either side of each boundary. The expected results were
recorded by running the original code, so they describe how the inn behaved
before any refactoring, and any change in behaviour shows up as a failure.

`tests/test_conjured_items.py` covers conjured items, which are a new feature.
Their expected results cannot be recorded from the original code, because it had
no conjured items, so they are taken from the requirements instead.


# Usage

Build stock with `make_item`, which picks the right class from the item's name,
then hand it to `GildedRose`:

```python
from gilded_rose import GildedRose, make_item

items = [make_item("Aged Brie", 2, 0), make_item("Conjured Mana Cake", 3, 6)]
GildedRose(items).update_quality()  # one day passes
```

Three names have rules of their own and must match exactly: `Aged Brie`,
`Backstage passes to a TAFKAL80ETC concert` and `Sulfuras, Hand of Ragnaros`.

Conjured stock is different. The requirements describe it as a category, not a
single product, so any name **starting with** `Conjured` degrades twice as fast:
`Conjured Mana Cake` and `Conjured Sword` are both conjured.

The legendary `Sulfuras, Hand of Ragnaros` item's quality is fixed at 80, so `make_item` ignores whatever quality is given for one.

Any other name is ordinary stock.


# Design notes

A further refactor was made, from the functional approach, to a polymorphic one.

Now each kind of stock is a class that knows what a day does to it,
so `GildedRose.update_quality` has no branching left at all, `Conjured` is
literally a `NormalItem` that degrades twice as fast, and `Sulfuras` sits outside
the aging hierarchy because it has no quality rule to give; adding a kind of stock
means adding a class and a name without touching any existing rule.

What that loses is size and directness. The functional version was 58 lines of
code across 5 top level definitions, against 95 across 10 here, about two thirds
more for identical behaviour, and a single day's update is now spread across the
codebase, where before it was one function read top to bottom.  It also needs a
factory and two abstract base classes, but this approach is worth it if the
number of products grows and it is conceptually much clearer.
