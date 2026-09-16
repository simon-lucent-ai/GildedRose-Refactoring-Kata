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
