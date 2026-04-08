"""Shared notebook utilities for SonarPy."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib as mpl
import numpy as np


DEFAULT_SEED = 7


@dataclass(frozen=True)
class Callout:
    """Simple container for notebook teaching callouts."""

    title: str
    body: str


def seeded_rng(seed: int = DEFAULT_SEED) -> np.random.Generator:
    """Return a reproducible random number generator."""
    return np.random.default_rng(seed)


def set_plot_style() -> None:
    """Apply a consistent plotting style across notebooks."""
    mpl.rcParams.update(
        {
            "figure.figsize": (10, 4.5),
            "axes.grid": True,
            "grid.alpha": 0.3,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "legend.frameon": False,
            "lines.linewidth": 2.0,
        }
    )


def assumptions_callout(*items: str) -> str:
    """Format an assumptions block for markdown cells."""
    return _format_callout(
        Callout(
            title="Assumptions",
            body="\n".join(f"- {item}" for item in items),
        )
    )


def key_takeaways_callout(*items: str) -> str:
    """Format a key takeaways block for markdown cells."""
    return _format_callout(
        Callout(
            title="Key Takeaways",
            body="\n".join(f"- {item}" for item in items),
        )
    )


def next_steps_callout(*items: str) -> str:
    """Format a next-steps block for markdown cells."""
    return _format_callout(
        Callout(
            title="Next Questions",
            body="\n".join(f"- {item}" for item in items),
        )
    )


def _format_callout(callout: Callout) -> str:
    return f"### {callout.title}\n\n{callout.body}\n"
