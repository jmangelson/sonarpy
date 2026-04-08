from __future__ import annotations

import numpy as np

from sonar_py_lib.dsp import (
    add_awgn,
    apply_window,
    complex_exponential,
    correlate,
    estimate_delay_samples,
    magnitude_spectrum,
    matched_filter,
    mean_power,
    normalize,
    power_spectrum_db,
    quantize_signal,
    rms,
    sine_wave,
    snr_db,
    time_axis,
    window_function,
)
from sonar_py_lib.notebook_utils import seeded_rng


def test_time_axis_has_expected_spacing() -> None:
    # Verifies that the helper maps sample count and sample rate to the expected uniform time grid.
    axis = time_axis(4, 8.0)
    np.testing.assert_allclose(axis, np.array([0.0, 0.125, 0.25, 0.375]))


def test_sine_wave_matches_expected_samples() -> None:
    # Checks a simple tone where the exact sampled values are easy to reason about by inspection.
    _, signal = sine_wave(1.0, 4.0, 1.0)
    np.testing.assert_allclose(signal, np.array([0.0, 1.0, 0.0, -1.0]), atol=1e-12)


def test_complex_exponential_has_unit_magnitude() -> None:
    # Confirms the complex tone helper preserves amplitude while rotating phase over time.
    _, signal = complex_exponential(2.0, 16.0, 0.5)
    np.testing.assert_allclose(np.abs(signal), np.ones_like(signal))


def test_quantize_signal_reduces_to_expected_levels() -> None:
    # Ensures quantization lands on the discrete amplitude levels implied by bit depth.
    values = np.array([-1.0, -0.2, 0.2, 1.0])
    quantized = quantize_signal(values, num_bits=3)
    np.testing.assert_allclose(quantized, np.array([-1.0, -1.0 / 3.0, 1.0 / 3.0, 1.0]))


def test_window_function_rectangular_and_hann() -> None:
    # Verifies that named windows map to the expected standard NumPy window shapes.
    rect = window_function(4, "rectangular")
    hann = window_function(4, "hann")
    np.testing.assert_allclose(rect, np.ones(4))
    np.testing.assert_allclose(hann, np.hanning(4))


def test_apply_window_matches_elementwise_product() -> None:
    # Confirms the convenience wrapper is just applying the selected window sample by sample.
    signal = np.ones(8)
    np.testing.assert_allclose(apply_window(signal, "hamming"), np.hamming(8))


def test_magnitude_spectrum_finds_tone_frequency() -> None:
    # Checks that the FFT helper places a clean sinusoid peak at the correct frequency bin.
    _, signal = sine_wave(4.0, 32.0, 1.0)
    freqs, spectrum = magnitude_spectrum(signal, 32.0)
    peak_frequency = freqs[int(np.argmax(spectrum))]
    assert peak_frequency == 4.0


def test_power_spectrum_db_returns_finite_values() -> None:
    # Confirms the dB conversion uses a floor so notebook plots do not contain negative infinity.
    _, signal = sine_wave(1.0, 8.0, 1.0)
    _, power = power_spectrum_db(signal, 8.0)
    assert np.isfinite(power).all()


def test_correlation_and_delay_estimation_find_known_shift() -> None:
    # Verifies both raw correlation indexing and the derived integer delay estimate on a shifted pulse.
    reference = np.array([1.0, 2.0, 1.0])
    delayed = np.array([0.0, 0.0, 1.0, 2.0, 1.0])
    corr = correlate(delayed, reference)
    assert int(np.argmax(corr)) == len(reference) - 1 + 2
    assert estimate_delay_samples(delayed, reference) == 2


def test_matched_filter_peaks_at_expected_location() -> None:
    # Checks that the matched filter peaks when the embedded reference waveform aligns best.
    reference = np.array([1.0, -1.0, 1.0])
    received = np.array([0.0, 0.0, 1.0, -1.0, 1.0, 0.0])
    output = matched_filter(received, reference)
    assert int(np.argmax(np.abs(output))) == 4


def test_add_awgn_is_reproducible_with_seeded_rng() -> None:
    # Ensures seeded randomness gives repeatable noisy examples for teaching and testing.
    signal = np.ones(128)
    noisy_a = add_awgn(signal, 10.0, rng=seeded_rng(3))
    noisy_b = add_awgn(signal, 10.0, rng=seeded_rng(3))
    np.testing.assert_allclose(noisy_a, noisy_b)


def test_snr_db_is_close_to_target_after_noise_addition() -> None:
    # Confirms the noise helper produces approximately the requested SNR in aggregate.
    signal = np.ones(4096)
    noisy = add_awgn(signal, 12.0, rng=seeded_rng(11))
    noise = noisy - signal
    measured = snr_db(signal, noise)
    np.testing.assert_allclose([measured], [12.0], atol=0.5)


def test_mean_power_and_rms_match_expected_values() -> None:
    # Validates the two basic amplitude summaries on a signal with known unit power and RMS.
    signal = np.array([1.0, -1.0, 1.0, -1.0])
    assert mean_power(signal) == 1.0
    assert rms(signal) == 1.0


def test_normalize_scales_signal_peak() -> None:
    # Checks that normalization rescales the largest magnitude sample to the requested peak value.
    signal = np.array([0.5, -2.0, 1.0])
    normalized = normalize(signal)
    np.testing.assert_allclose(normalized, np.array([0.25, -1.0, 0.5]))
