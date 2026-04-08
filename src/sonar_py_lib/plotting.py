"""Plotting helpers for educational notebooks."""

from __future__ import annotations

from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def make_figure(
    nrows: int = 1,
    ncols: int = 1,
    *,
    figsize: tuple[float, float] = (10.0, 4.5),
    sharex: bool = False,
    sharey: bool = False,
) -> tuple[Figure, Axes | np.ndarray]:
    """Create a figure with sensible defaults for notebook teaching plots."""
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize,
        sharex=sharex,
        sharey=sharey,
        constrained_layout=True,
    )
    return fig, axes


def plot_signal(
    x: Sequence[float],
    y: Sequence[float],
    *,
    ax: Axes | None = None,
    title: str = "",
    xlabel: str = "Sample",
    ylabel: str = "Amplitude",
    label: str | None = None,
    color: str | None = None,
    linewidth: float = 2.0,
) -> Axes:
    """Plot a 1D signal in the time or sample domain."""
    ax = ax if ax is not None else plt.gca()
    ax.plot(x, y, label=label, color=color, linewidth=linewidth)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    if label:
        ax.legend()
    return ax


def plot_signals(
    x: Sequence[float],
    ys: Iterable[Sequence[float]],
    *,
    labels: Sequence[str] | None = None,
    ax: Axes | None = None,
    title: str = "",
    xlabel: str = "Sample",
    ylabel: str = "Amplitude",
    linewidth: float = 2.0,
) -> Axes:
    """Plot multiple 1D signals on the same axes for comparison."""
    ax = ax if ax is not None else plt.gca()
    labels = labels or []
    for idx, values in enumerate(ys):
        label = labels[idx] if idx < len(labels) else None
        ax.plot(x, values, label=label, linewidth=linewidth)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    if labels:
        ax.legend()
    return ax


def plot_stem(
    x: Sequence[float],
    y: Sequence[float],
    *,
    ax: Axes | None = None,
    title: str = "",
    xlabel: str = "Sample",
    ylabel: str = "Amplitude",
) -> Axes:
    """Plot a discrete-time signal."""
    ax = ax if ax is not None else plt.gca()
    markerline, stemlines, baseline = ax.stem(x, y)
    plt.setp(markerline, markersize=6)
    plt.setp(stemlines, linewidth=1.5)
    plt.setp(baseline, linewidth=1.0)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    return ax


def plot_spectrum(
    frequencies: Sequence[float],
    magnitude: Sequence[float],
    *,
    ax: Axes | None = None,
    title: str = "",
    xlabel: str = "Frequency (Hz)",
    ylabel: str = "Magnitude",
    db: bool = False,
) -> Axes:
    """Plot a magnitude spectrum in linear or dB units."""
    ax = ax if ax is not None else plt.gca()
    spectrum = np.asarray(magnitude)
    if db:
        spectrum = 20.0 * np.log10(np.maximum(np.abs(spectrum), 1e-12))
        ylabel = "Magnitude (dB)"
    ax.plot(frequencies, spectrum, linewidth=2.0)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    return ax


def plot_heatmap(
    data: Sequence[Sequence[float]],
    *,
    ax: Axes | None = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    colorbar_label: str = "",
    extent: tuple[float, float, float, float] | None = None,
    origin: str = "lower",
    cmap: str = "viridis",
) -> Axes:
    """Display 2D data such as parameter sweeps or simple SAS images."""
    ax = ax if ax is not None else plt.gca()
    image = ax.imshow(
        np.asarray(data),
        aspect="auto",
        origin=origin,
        extent=extent,
        cmap=cmap,
    )
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if colorbar_label:
        colorbar = plt.colorbar(image, ax=ax)
        colorbar.set_label(colorbar_label)
    else:
        plt.colorbar(image, ax=ax)
    return ax


def plot_beam_pattern(
    angles_deg: Sequence[float],
    response: Sequence[float],
    *,
    ax: Axes | None = None,
    title: str = "Beam Pattern",
    db: bool = True,
) -> Axes:
    """Plot an array beam pattern versus angle."""
    ax = ax if ax is not None else plt.gca()
    values = np.asarray(response)
    if db:
        values = 20.0 * np.log10(np.maximum(np.abs(values), 1e-12))
        ylabel = "Response (dB)"
    else:
        ylabel = "Response"
    ax.plot(angles_deg, values, linewidth=2.0)
    ax.set_title(title)
    ax.set_xlabel("Angle (deg)")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    return ax


def plot_image(
    image: Sequence[Sequence[float]],
    *,
    ax: Axes | None = None,
    title: str = "",
    xlabel: str = "Cross-track",
    ylabel: str = "Along-track",
    cmap: str = "magma",
    colorbar_label: str = "Intensity",
) -> Axes:
    """Display an image-like product such as a focused SAS result."""
    return plot_heatmap(
        image,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        colorbar_label=colorbar_label,
        cmap=cmap,
    )
