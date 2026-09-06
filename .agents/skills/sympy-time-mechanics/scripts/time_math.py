#!/usr/bin/env python3
"""
Time Mechanics Mathematical Engine for TimeMaster Harness
Implements exact relativistic, metrological, and packet timing calculations.
"""

import math
from typing import Dict, Any, List

# Physical Constants (CODATA 2018 / IERS Conventions)
C = 299792458.0              # Speed of light in vacuum (m/s)
G = 6.67430e-11              # Newtonian constant of gravitation (m^3 kg^-1 s^-2)
M_EARTH = 5.9722e24          # Earth mass (kg)
R_EARTH = 6378137.0          # Earth WGS84 equatorial radius (m)
SECONDS_PER_DAY = 86400.0    # Seconds in a mean solar day

# GPS Orbital Parameters
GPS_ALTITUDE = 20180000.0    # GPS semi-major axis orbital altitude above ground (m)
GPS_ORBIT_RADIUS = R_EARTH + GPS_ALTITUDE
GPS_VELOCITY = 3874.0        # Orbital velocity of GPS satellite (m/s)
GPS_BASE_FREQ = 10.23e6      # 10.23 MHz nominal clock frequency


def calculate_gps_relativistic_effects() -> Dict[str, Any]:
    """
    Computes exact special and general relativistic time dilation for GPS satellites.
    Returns daily drift in microseconds and steered frequency.
    """
    # 1. Special Relativity (Kinematic Time Dilation)
    # gamma = 1 / sqrt(1 - v^2/c^2)
    # Fractional shift: Delta f / f = - v^2 / (2 * c^2)
    sr_fractional = - (GPS_VELOCITY ** 2) / (2.0 * (C ** 2))
    sr_daily_seconds = sr_fractional * SECONDS_PER_DAY
    sr_daily_microseconds = sr_daily_seconds * 1e6

    # 2. General Relativity (Gravitational Frequency Shift)
    # Fractional shift: Delta f / f = (Phi_satellite - Phi_earth) / c^2
    # Phi = - GM / r
    # Delta Phi = GM * (1/R_earth - 1/R_orbit)
    delta_phi = G * M_EARTH * ( (1.0 / R_EARTH) - (1.0 / GPS_ORBIT_RADIUS) )
    gr_fractional = delta_phi / (C ** 2)
    gr_daily_seconds = gr_fractional * SECONDS_PER_DAY
    gr_daily_microseconds = gr_daily_seconds * 1e6

    # 3. Net Relativistic Effect
    net_fractional = gr_fractional + sr_fractional
    net_daily_microseconds = gr_daily_microseconds + sr_daily_microseconds

    # Factory Steered Frequency
    # f_steered = f_0 * (1 - net_fractional)
    steered_frequency = GPS_BASE_FREQ * (1.0 - net_fractional)

    return {
        "special_relativity_fractional": sr_fractional,
        "special_relativity_daily_us": sr_daily_microseconds,
        "general_relativity_fractional": gr_fractional,
        "general_relativity_daily_us": gr_daily_microseconds,
        "net_fractional_drift": net_fractional,
        "net_daily_drift_us": net_daily_microseconds,
        "base_frequency_hz": GPS_BASE_FREQ,
        "steered_frequency_hz": steered_frequency,
        "position_error_per_day_km": (net_daily_microseconds * 1e-6) * C / 1000.0
    }


def calculate_ntp_packet_math(t1: float, t2: float, t3: float, t4: float) -> Dict[str, float]:
    """
    Computes NTP/PTP 4-timestamp packet delay and clock offset:
    t1: client transmit time
    t2: server receive time
    t3: server transmit time
    t4: client receive time
    """
    round_trip_delay = (t4 - t1) - (t3 - t2)
    clock_offset = ((t2 - t1) + (t3 - t4)) / 2.0
    return {
        "round_trip_delay": round_trip_delay,
        "clock_offset": clock_offset,
        "symmetric_assumption_valid": round_trip_delay >= 0
    }


def calculate_allan_deviation(y_series: List[float], tau_0: float = 1.0) -> Dict[str, float]:
    """
    Computes fractional frequency Allan Deviation (ADEV) sigma_y(tau):
    sigma_y^2(tau) = 1/(2 * (N - 1)) * sum( (y_{i+1} - y_i)^2 )
    """
    n = len(y_series)
    if n < 2:
        raise ValueError("Allan deviation requires at least 2 frequency fractional samples.")
    
    sum_sq_diff = sum((y_series[i+1] - y_series[i])**2 for i in range(n - 1))
    allan_var = sum_sq_diff / (2.0 * (n - 1))
    allan_dev = math.sqrt(allan_var)
    return {
        "allan_variance": allan_var,
        "allan_deviation": allan_dev,
        "tau_seconds": tau_0,
        "sample_count": n
    }


def calculate_y2038_overflow_epoch() -> Dict[str, Any]:
    """
    Calculates Unix 32-bit signed integer epoch overflow boundary.
    Max signed 32-bit int = 2^31 - 1 = 2147483647
    Date: 2038-01-19 03:14:07 UTC
    """
    max_32bit_signed = 2**31 - 1
    overflow_point = 2**31  # flips to -2147483648 (Year 1901)
    
    return {
        "max_32bit_signed_int": max_32bit_signed,
        "overflow_int_val": overflow_point,
        "overflow_utc_string": "2038-01-19 03:14:07 UTC",
        "post_overflow_year": 1901,
        "max_64bit_signed_int": 2**63 - 1,
        "years_covered_by_64bit": (2**63 - 1) / (365.25 * 86400)
    }


if __name__ == "__main__":
    print("=== GPS Relativistic Calculations ===")
    gps = calculate_gps_relativistic_effects()
    print(f"Special Relativity (Kinematic): {gps['special_relativity_daily_us']:.2f} us/day")
    print(f"General Relativity (Gravitational): {gps['general_relativity_daily_us']:.2f} us/day")
    print(f"Net Relativistic Drift: {gps['net_daily_drift_us']:.2f} us/day")
    print(f"Factory Steered Frequency: {gps['steered_frequency_hz']:.11f} Hz")
    print(f"Uncorrected Daily Position Error: {gps['position_error_per_day_km']:.2f} km/day\n")

    print("=== NTP Packet Math Example ===")
    ntp = calculate_ntp_packet_math(t1=100.000, t2=100.015, t3=100.018, t4=100.035)
    print(f"Round-Trip Delay: {ntp['round_trip_delay']*1000:.2f} ms")
    print(f"Clock Offset: {ntp['clock_offset']*1000:.2f} ms\n")

    print("=== Year 2038 Problem ===")
    y2038 = calculate_y2038_overflow_epoch()
    print(f"32-bit Limit: {y2038['max_32bit_signed_int']} seconds ({y2038['overflow_utc_string']})")
    print(f"64-bit Limit Coverage: {y2038['years_covered_by_64bit']:.2e} years")
