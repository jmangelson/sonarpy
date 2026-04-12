"""Sonar-specific helpers for educational notebooks."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .dsp import time_axis


def pulse_train(num_samples: int, start_idx: int, width: int, *, amplitude: float = 1.0) -> np.ndarray:
    """Return a finite-width rectangular pulse inside a zero record."""
    if num_samples <= 0:
        raise ValueError("num_samples must be positive")
    if start_idx < 0:
        raise ValueError("start_idx must be nonnegative")
    if width <= 0:
        raise ValueError("width must be positive")

    pulse = np.zeros(num_samples, dtype=float)
    stop_idx = min(num_samples, start_idx + width)
    pulse[start_idx:stop_idx] = amplitude
    return pulse


def range_to_delay_s(range_m: float | np.ndarray, c_sound_m_s: float) -> float | np.ndarray:
    """Convert target range to monostatic round-trip delay."""
    if c_sound_m_s <= 0.0:
        raise ValueError("c_sound_m_s must be positive")
    return 2.0 * np.asarray(range_m) / c_sound_m_s


def delay_to_range_m(delay_s: float | np.ndarray, c_sound_m_s: float) -> float | np.ndarray:
    """Convert monostatic round-trip delay to target range."""
    if c_sound_m_s <= 0.0:
        raise ValueError("c_sound_m_s must be positive")
    return 0.5 * c_sound_m_s * np.asarray(delay_s)


def range_to_delay_samples(range_m: float | np.ndarray, sample_rate_hz: float, c_sound_m_s: float) -> int | np.ndarray:
    """Convert target range to an integer round-trip sample delay."""
    if sample_rate_hz <= 0.0:
        raise ValueError("sample_rate_hz must be positive")
    delay_s = range_to_delay_s(range_m, c_sound_m_s)
    delay_n = np.round(np.asarray(delay_s) * sample_rate_hz).astype(int)
    return int(delay_n) if np.ndim(delay_n) == 0 else delay_n


def delay_samples_to_range_m(delay_samples: int | np.ndarray, sample_rate_hz: float, c_sound_m_s: float) -> float | np.ndarray:
    """Convert integer round-trip sample delay to target range."""
    if sample_rate_hz <= 0.0:
        raise ValueError("sample_rate_hz must be positive")
    delay_s = np.asarray(delay_samples, dtype=float) / sample_rate_hz
    result = delay_to_range_m(delay_s, c_sound_m_s)
    return float(result) if np.ndim(result) == 0 else result


def linear_chirp(
    duration_s: float,
    sample_rate_hz: float,
    start_freq_hz: float,
    bandwidth_hz: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a unit-magnitude complex linear chirp."""
    if duration_s <= 0.0:
        raise ValueError("duration_s must be positive")
    if sample_rate_hz <= 0.0:
        raise ValueError("sample_rate_hz must be positive")

    num_samples = int(round(duration_s * sample_rate_hz))
    if num_samples <= 0:
        raise ValueError("duration_s and sample_rate_hz produce zero samples")

    t = time_axis(num_samples, sample_rate_hz)
    sweep_rate_hz_s = bandwidth_hz / duration_s
    phase_rad = 2.0 * np.pi * (start_freq_hz * t + 0.5 * sweep_rate_hz_s * t**2)
    return t, np.exp(1j * phase_rad)


def place_echo(
    record: Sequence[complex],
    pulse: Sequence[complex],
    start_idx: int,
    *,
    amplitude: complex = 1.0,
) -> np.ndarray:
    """Add one delayed echo copy into a record and return the updated record."""
    if start_idx < 0:
        raise ValueError("start_idx must be nonnegative")

    out = np.array(record, copy=True)
    pulse_values = np.asarray(pulse)
    stop_idx = min(len(out), start_idx + len(pulse_values))
    usable = stop_idx - start_idx
    if usable > 0:
        out[start_idx:stop_idx] += amplitude * pulse_values[:usable]
    return out


def synthesize_scene(
    record_len: int,
    pulse: Sequence[complex],
    target_ranges_m: Sequence[float],
    target_weights: Sequence[complex],
    c_sound_m_s: float,
    sample_rate_hz: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Synthesize a simple scene as a sum of delayed weighted pulse copies."""
    if record_len <= 0:
        raise ValueError("record_len must be positive")

    pulse_values = np.asarray(pulse)
    ranges = np.asarray(target_ranges_m, dtype=float)
    weights = np.asarray(target_weights)
    if len(ranges) != len(weights):
        raise ValueError("target_ranges_m and target_weights must have the same length")

    record = np.zeros(record_len, dtype=np.result_type(pulse_values.dtype, weights.dtype, float))
    sample_delays = range_to_delay_samples(ranges, sample_rate_hz, c_sound_m_s)
    for delay_n, weight in zip(sample_delays, weights):
        record = place_echo(record, pulse_values, int(delay_n), amplitude=weight)
    return record, np.asarray(sample_delays, dtype=int)
