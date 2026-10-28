"""Shared pytest setup for the three starter projects.

Why this file exists: ``train.py`` appears in BOTH the beginner and the
advanced starter. A plain ``import train`` inside a test file therefore
resolves to whichever folder pytest reached first, so one run over the whole
folder — ``python -m pytest examples/starter-projects -q`` — used to load the
*wrong* ``train`` for one of them and fail with a confusing AttributeError
(``module 'train' has no attribute 'train'``).

This hook runs just before pytest imports each test file and points the name
``train`` at *that folder's own* ``train.py``. The starter code itself stays
untouched and beginner-readable; only the test-runner wiring is aware of the
collision.

Verified locally: the combined command above, and each folder on its own,
both pass.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys


def _load_own_train(folder: pathlib.Path) -> None:
    """Alias ``train`` to the train.py sitting next to this test file."""
    train_file = folder / "train.py"
    if not train_file.is_file():
        return

    unique_name = f"_starter_train_{folder.name}"
    if unique_name not in sys.modules:
        # beginner/train.py does `import churndata`, so its folder must be
        # importable while the module executes.
        if str(folder) not in sys.path:
            sys.path.insert(0, str(folder))
        spec = importlib.util.spec_from_file_location(unique_name, train_file)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[unique_name] = module
        spec.loader.exec_module(module)

    # The plain name every starter test uses.
    sys.modules["train"] = sys.modules[unique_name]


def pytest_pycollect_makemodule(module_path, parent):  # pytest 8/9 signature
    """Runs before pytest imports each test module; returns None = default."""
    _load_own_train(pathlib.Path(module_path).parent)
    return None
