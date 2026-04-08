"""Core DSP helpers for educational notebooks."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def time_axis(num_samples: int, sample_rate_hz: float, *, start_s: float = 0.0) -> np.ndarray:
    """Return a uniformly sampled time axis."""
    # Early notebooks repeatedly need an explicit mapping from sample index to time.
    if num_samples <= 0:
        raise ValueError("num_samples must be positive")
    if sample_rate_hz <= 0.0:
        raise ValueError("sample_rate_hz must be positive")
    return start_s + np.arange(num_samples, dtype=float) / sample_rate_hz


def sine_wave(
    frequency_hz: float,
    sample_rate_hz: float,
    duration_s: float,
    *,
    amplitude: float = 1.0,
    phase_rad: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate a real sinusoid and its time axis."""
    # Real sinusoids are the first building block for sampling, phase, and spectral intuition.
    t = _time_axis_from_duration(sample_rate_hz, duration_s)
    signal = amplitude * np.sin(2.0 * np.pi * frequency_hz * t + phase_rad)
    return t, signal


def complex_exponential(
    frequency_hz: float,
    sample_rate_hz: float,
    duration_s: float,
    *,
    amplitude: float = 1.0,
    phase_rad: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate a complex exponential and its time axis."""
    # Complex exponentials make phase and frequency manipulations much easier to explain later.
    t = _time_axis_from_duration(sample_rate_hz, duration_s)
    signal = amplitude * np.exp(1j * (2.0 * np.pi * frequency_hz * t + phase_rad))
    return t, signal


def quantize_signal(signal: Sequence[float], num_bits: int, *, full_scale: float = 1.0) -> np.ndarray:
    """Quantize a signal with a symmetric mid-tread quantizer."""
    # This lets the sampling notebook show how finite ADC resolution distorts a waveform.
    if num_bits <= 0:
        raise ValueError("num_bits must be positive")
    if full_scale <= 0.0:
        raise ValueError("full_scale must be positive")

    values = np.asarray(signal, dtype=float)
    max_index = 2 ** (num_bits - 1) - 1
    scaled = np.clip(values / full_scale, -1.0, 1.0)
    quantized_index = np.round(scaled * max_index)
    return quantized_index * full_scale / max_index


def apply_window(signal: Sequence[float], window: str = "hann") -> np.ndarray:
    """Apply a named window function to a 1D signal."""
    # Windowing is separated out so notebooks can compare leakage behavior with one-line swaps.
    values = np.asarray(signal)
    weights = window_function(len(values), window)
    return values * weights


def window_function(num_samples: int, window: str = "hann") -> np.ndarray:
    """Return a common analysis window."""
    # Keeping a small set of windows here is enough for the first spectral tradeoff discussions.
    if num_samples <= 0:
        raise ValueError("num_samples must be positive")

    name = window.lower()
    if name in {"rect", "rectangular", "boxcar"}:
        return np.ones(num_samples)
    if name in {"hann", "hanning"}:
        return np.hanning(num_samples)
    if name == "hamming":
        return np.hamming(num_samples)
    raise ValueError(f"Unsupported window: {window}")


def magnitude_spectrum(
    signal: Sequence[complex],
    sample_rate_hz: float,
    *,
    onesided: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """Return FFT bin frequencies and magnitude spectrum."""
    # The early FFT notebooks need a simple spectrum helper, not a feature-heavy analysis API.
    if sample_rate_hz <= 0.0:
        raise ValueError("sample_rate_hz must be positive")

    values = np.asarray(signal)
    num_samples = len(values)
    if num_samples == 0:
        raise ValueError("signal must contain at least one sample")

    if onesided and np.isrealobj(values):
        spectrum = np.fft.rfft(values)
        freqs = np.fft.rfftfreq(num_samples, d=1.0 / sample_rate_hz)
    else:
        spectrum = np.fft.fftshift(np.fft.fft(values))
        freqs = np.fft.fftshift(np.fft.fftfreq(num_samples, d=1.0 / sample_rate_hz))
    return freqs, np.abs(spectrum)


def power_spectrum_db(
    signal: Sequence[complex],
    sample_rate_hz: float,
    *,
    floor_db: float = -120.0,
    onesided: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a power spectrum in dB with a finite floor."""
    # A dB view is easier for teaching dynamic range and weak components near stronger tones.
    freqs, magnitude = magnitude_spectrum(signal, sample_rate_hz, onesided=onesided)
    power_db = 20.0 * np.log10(np.maximum(magnitude, 10 ** (floor_db / 20.0)))
    return freqs, power_db


def linear_convolve(signal: Sequence[complex], kernel: Sequence[complex], *, mode: str = "full") -> np.ndarray:
    """Convolve two 1D sequences."""
    # Convolution is exposed directly because it is a central concept in filtering notebooks.
    return np.convolve(np.asarray(signal), np.asarray(kernel), mode=mode)


def correlate(signal: Sequence[complex], reference: Sequence[complex], *, mode: str = "full") -> np.ndarray:
    """Correlate a signal against a reference sequence."""
    # Correlation is kept explicit because learners need to compare it directly against convolution.
    return np.correlate(np.asarray(signal), np.asarray(reference), mode=mode)


def matched_filter(received: Sequence[complex], reference: Sequence[complex], *, mode: str = "full") -> np.ndarray:
    """Apply a matched filter using the time-reversed conjugate reference."""
    # This wraps the standard matched-filter construction used later for pulse compression.
    ref = np.asarray(reference)
    matched_kernel = np.conjugate(ref[::-1])
    return linear_convolve(received, matched_kernel, mode=mode)


def add_awgn(
    signal: Sequence[complex],
    snr_db: float,
    *,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Add white Gaussian noise to reach a target SNR."""
    # Controlled noise injection is needed for detection and estimation trade studies.
    values = np.asarray(signal)
    rng = rng or np.random.default_rng()

    signal_power = mean_power(values)
    if signal_power <= 0.0:
        raise ValueError("signal power must be positive")

    noise_power = signal_power / (10.0 ** (snr_db / 10.0))
    if np.iscomplexobj(values):
        noise = (
            rng.normal(scale=np.sqrt(noise_power / 2.0), size=values.shape)
            + 1j * rng.normal(scale=np.sqrt(noise_power / 2.0), size=values.shape)
        )
    else:
        noise = rng.normal(scale=np.sqrt(noise_power), size=values.shape)
    return values + noise


def mean_power(signal: Sequence[complex]) -> float:
    """Return mean signal power."""
    # Power is the baseline quantity behind SNR, noise scaling, and detection discussions.
    values = np.asarray(signal)
    if len(values) == 0:
        raise ValueError("signal must contain at least one sample")
    return float(np.mean(np.abs(values) ** 2))


def rms(signal: Sequence[complex]) -> float:
    """Return the root-mean-square value of a signal."""
    # RMS gives a familiar amplitude summary that complements mean power in the early notebooks.
    return float(np.sqrt(mean_power(signal)))


def snr_db(signal: Sequence[complex], noise: Sequence[complex]) -> float:
    """Estimate SNR from a signal component and a noise component."""
    # This keeps the SNR definition explicit so examples can tie directly to measured outcomes.
    signal_power = mean_power(signal)
    noise_power = mean_power(noise)
    if noise_power <= 0.0:
        raise ValueError("noise power must be positive")
    return 10.0 * np.log10(signal_power / noise_power)


def estimate_delay_samples(
    signal: Sequence[complex],
    reference: Sequence[complex],
) -> int:
    """Estimate integer sample delay using peak correlation."""
    # Integer delay estimation is a simple bridge from correlation to ranging intuition.
    corr = correlate(signal, reference, mode="full")
    peak_index = int(np.argmax(np.abs(corr)))
    return peak_index - (len(reference) - 1)


def normalize(signal: Sequence[complex], *, peak: float = 1.0) -> np.ndarray:
    """Normalize a signal by its maximum absolute value."""
    # Normalization keeps comparisons readable when notebooks sweep amplitude or SNR.
    values = np.asarray(signal)
    max_value = np.max(np.abs(values))
    if max_value == 0.0:
        return np.zeros_like(values)
    return peak * values / max_value


def _time_axis_from_duration(sample_rate_hz: float, duration_s: float) -> np.ndarray:
    # Duration-driven generation is convenient in notebooks, but it still reduces to a sample grid.
    if sample_rate_hz <= 0.0:
        raise ValueError("sample_rate_hz must be positive")
    if duration_s <= 0.0:
        raise ValueError("duration_s must be positive")
    num_samples = int(np.round(duration_s * sample_rate_hz))
    if num_samples <= 0:
        raise ValueError("duration_s and sample_rate_hz produce zero samples")
    return time_axis(num_samples, sample_rate_hz)
