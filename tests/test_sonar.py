from __future__ import annotations

import numpy as np
import pytest

from sonar_py_lib.sonar import (
    delay_samples_to_range_m,
    delay_to_range_m,
    linear_chirp,
    place_echo,
    pulse_train,
    range_to_delay_s,
    range_to_delay_samples,
    synthesize_scene,
)


def test_pulse_train_places_rectangular_pulse() -> None:
    pulse = pulse_train(10, 3, 4, amplitude=2.5)
    expected = np.array([0.0, 0.0, 0.0, 2.5, 2.5, 2.5, 2.5, 0.0, 0.0, 0.0])
    np.testing.assert_allclose(pulse, expected)


def test_range_delay_conversions_are_consistent() -> None:
    c_sound = 1500.0
    rng_m = 37.5
    delay_s = range_to_delay_s(rng_m, c_sound)
    assert delay_s == pytest.approx(0.05)
    assert delay_to_range_m(delay_s, c_sound) == pytest.approx(rng_m)


def test_sample_delay_range_conversions_round_as_expected() -> None:
    c_sound = 1500.0
    fs = 4000.0
    rng_m = 45.0
    delay_n = range_to_delay_samples(rng_m, fs, c_sound)
    assert delay_n == 240
    assert delay_samples_to_range_m(delay_n, fs, c_sound) == pytest.approx(rng_m)


def test_linear_chirp_returns_unit_magnitude_complex_waveform() -> None:
    t, chirp = linear_chirp(0.01, 4000.0, 100.0, 500.0)
    assert len(t) == 40
    assert chirp.dtype.kind == "c"
    np.testing.assert_allclose(np.abs(chirp), np.ones_like(t))


def test_place_echo_adds_and_clips_pulse() -> None:
    record = np.zeros(6, dtype=float)
    pulse = np.array([1.0, 2.0, 3.0, 4.0])
    updated = place_echo(record, pulse, 4, amplitude=0.5)
    np.testing.assert_allclose(updated, np.array([0.0, 0.0, 0.0, 0.0, 0.5, 1.0]))


def test_synthesize_scene_returns_expected_sum_and_delays() -> None:
    pulse = np.array([1.0, -0.5, 0.25])
    record, delays = synthesize_scene(
        12,
        pulse,
        target_ranges_m=np.array([0.75, 1.5]),
        target_weights=np.array([1.0, 0.4]),
        c_sound_m_s=1500.0,
        sample_rate_hz=2000.0,
    )
    np.testing.assert_array_equal(delays, np.array([2, 4]))
    expected = np.zeros(12)
    expected[2:5] += pulse
    expected[4:7] += 0.4 * pulse
    np.testing.assert_allclose(record, expected)


def test_synthesize_scene_checks_lengths() -> None:
    with pytest.raises(ValueError):
        synthesize_scene(
            10,
            np.array([1.0, 2.0]),
            target_ranges_m=np.array([1.0, 2.0]),
            target_weights=np.array([1.0]),
            c_sound_m_s=1500.0,
            sample_rate_hz=4000.0,
        )
