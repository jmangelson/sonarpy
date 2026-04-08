"""Notebook-local helpers for importing the src-layout package."""

from __future__ import annotations

import sys
from pathlib import Path


def bootstrap_src_path() -> Path:
    """Add the repository's src directory to sys.path for notebook execution."""
    current = Path.cwd().resolve()

    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "src").exists():
            src = candidate / "src"
            if str(src) not in sys.path:
                sys.path.insert(0, str(src))
            return src

    raise RuntimeError("Could not locate the repository root from the notebook working directory.")
