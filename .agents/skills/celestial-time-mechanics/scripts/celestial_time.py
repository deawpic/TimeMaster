#!/usr/bin/env python3
"""
Celestial & Relativistic Time Mechanics Engine
Calculates relativistic time dilation on the Moon (Coordinated Lunar Time - LTC),
Mars (Coordinated Mars Time - MTC), and IAU coordinate time transformations.
Used by celestial-time-mechanics skill in TimeMaster.
"""

import math
from typing import Dict, Any

# Fundamental Physical Constants (CODATA 2018 / IAU 2015)
C_SPEED_OF_LIGHT = 299792458.0              # m/s
G_GRAVITATIONAL_CONST = 6.67430e-11         # m^3 / (kg * s^2)

# Earth Constants
M_EARTH = 5.972168e24                       # kg
R_EARTH = 6378137.0                         # m (WGS84 equatorial radius)
W0_EARTH_GEOID_POTENTIAL = 6.26368560e7     # m^2 / s^2 (IERS Conventions 2010)

# Moon Constants
M_MOON = 7.342e22                           # kg
R_MOON = 1737400.0                          # m (mean radius)
A_MOON_ORBIT = 384400000.0                  # m (semi-major axis around Earth)
V_MOON_ORBIT = 1022.0                       # m/s (mean orbital velocity)

# Mars Constants
M_MARS = 6.4171e23                          # kg
R_MARS = 3389500.0                          # m (mean radius)
MARS_SOL_SECONDS = 88775.244                # 24h 39m 35.244s in SI seconds

# IAU Coordinate Time Scale Scaling Factors
TT_TAI_OFFSET_SEC = 32.184                  # TT = TAI + 32.184s
L_G_RATE = 6.969290134e-10                  # (dTCG/dTT - 1)
L_B_RATE = 1.550519768e-8                   # (dTCB/dTCG - 1)


def calculate_lunar_time_dilation() -> Dict[str, Any]:
    """
    Calculate the exact relativistic time drift between the lunar surface and Earth geoid.
    Conforms to NASA Artemis & ESA Coordinated Lunar Time (LTC) specifications.
    
    Formula:
    dtau_moon / dt_earth - 1 = (W0 - (U_moon + U_earth_at_moon + 0.5 * v_moon^2)) / c^2
    """
    c2 = C_SPEED_OF_LIGHT ** 2

    # Gravitational potential on Moon surface due to Moon mass
    u_moon_surface = (G_GRAVITATIONAL_CONST * M_MOON) / R_MOON
    
    # Earth gravitational potential at lunar distance
    u_earth_at_moon = (G_GRAVITATIONAL_CONST * M_EARTH) / A_MOON_ORBIT
    
    # Kinematic potential due to lunar orbital velocity
    kinematic_term = 0.5 * (V_MOON_ORBIT ** 2)

    # Net potential on Moon surface
    u_net_moon = u_moon_surface + u_earth_at_moon + kinematic_term

    # Fractional frequency shift: (W0 - U_net_moon) / c^2
    # W0 is higher potential than Moon surface, so clocks on Moon tick FASTER
    delta_rate = (W0_EARTH_GEOID_POTENTIAL - u_net_moon) / c2

    # In 1 Earth solar day (86400 seconds)
    daily_drift_sec = delta_rate * 86400.0
    daily_drift_us = daily_drift_sec * 1e6

    return {
        "body": "Moon",
        "standard": "Coordinated Lunar Time (LTC)",
        "fractional_frequency_offset": delta_rate,
        "daily_drift_us": daily_drift_us,
        "daily_drift_ns": daily_drift_sec * 1e9,
        "lunar_clock_faster": daily_drift_us > 0,
        "physical_components": {
            "earth_geoid_potential_m2_s2": W0_EARTH_GEOID_POTENTIAL,
            "moon_surface_potential_m2_s2": u_moon_surface,
            "earth_potential_at_orbit_m2_s2": u_earth_at_moon,
            "orbital_kinematic_m2_s2": kinematic_term
        }
    }


def calculate_mars_time_parameters() -> Dict[str, Any]:
    """
    Calculate time parameters for Mars (Coordinated Mars Time - MTC / Sol).
    """
    c2 = C_SPEED_OF_LIGHT ** 2

    # Gravitational potential on Mars surface
    u_mars_surface = (G_GRAVITATIONAL_CONST * M_MARS) / R_MARS

    # Gravitational potential drift relative to Earth geoid (isolated body approximation)
    gravitational_shift = (W0_EARTH_GEOID_POTENTIAL - u_mars_surface) / c2
    daily_drift_us = gravitational_shift * 86400.0 * 1e6

    # Sol duration breakdown
    hours = int(MARS_SOL_SECONDS // 3600)
    minutes = int((MARS_SOL_SECONDS % 3600) // 60)
    seconds = MARS_SOL_SECONDS % 60

    ratio_sol_to_earth_day = MARS_SOL_SECONDS / 86400.0

    return {
        "body": "Mars",
        "standard": "Coordinated Mars Time (MTC)",
        "sol_duration_seconds": MARS_SOL_SECONDS,
        "sol_hms": f"{hours}h {minutes}m {seconds:.3f}s",
        "ratio_sol_to_earth_day": ratio_sol_to_earth_day,
        "surface_gravitational_potential_m2_s2": u_mars_surface,
        "daily_drift_relative_to_geoid_us": daily_drift_us
    }


def convert_coordinate_times(tai_epoch_sec: float) -> Dict[str, float]:
    """
    Convert TAI second timestamp into IAU Coordinate Time Scales:
    - Terrestrial Time (TT)
    - Geocentric Coordinate Time (TCG)
    """
    tt = tai_epoch_sec + TT_TAI_OFFSET_SEC
    # Linear secular drift of TCG relative to TT since 1977-01-01 00:00:00 TAI (MJD 43144.0)
    # Reference epoch 1977-01-01 00:00:00 TAI in Unix seconds: ~ 220924800.0
    t0_1977 = 220924800.0
    dt = tai_epoch_sec - t0_1977
    tcg = tt + (L_G_RATE * dt)

    return {
        "tai": tai_epoch_sec,
        "tt": tt,
        "tcg": tcg,
        "tt_tai_offset_sec": TT_TAI_OFFSET_SEC,
        "tcg_tt_secular_difference_sec": tcg - tt
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Celestial Time Mechanics Engine")
    parser.add_argument("--body", choices=["moon", "mars", "coordinate"], default="moon")

    args = parser.parse_args()

    if args.body == "moon":
        res = calculate_lunar_time_dilation()
        print("=== Coordinated Lunar Time (LTC) ===")
        print(f"Fractional Shift: {res['fractional_frequency_offset']:.6e}")
        print(f"Daily Drift: +{res['daily_drift_us']:.2f} µs/day (Moon clock ticks faster)")
    elif args.body == "mars":
        res = calculate_mars_time_parameters()
        print("=== Coordinated Mars Time (MTC) ===")
        print(f"Sol Duration: {res['sol_duration_seconds']} s ({res['sol_hms']})")
        print(f"Sol / Earth Day Ratio: {res['ratio_sol_to_earth_day']:.6f}")
    elif args.body == "coordinate":
        res = convert_coordinate_times(1772841600.0) # Approx 2026 epoch
        print("=== IAU Coordinate Clocks ===")
        print(f"TAI: {res['tai']} s")
        print(f"TT:  {res['tt']} s (TAI + {res['tt_tai_offset_sec']} s)")
        print(f"TCG: {res['tcg']:.3f} s")
