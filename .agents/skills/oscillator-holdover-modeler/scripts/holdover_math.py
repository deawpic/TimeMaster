#!/usr/bin/env python3
"""
Oscillator Holdover Calculation Engine
Models drift and holdover duration for various oscillator tiers during GNSS loss.
Used by oscillator-holdover-modeler skill in TimeMaster.
"""

import math
from typing import Dict, Any


OSCILLATOR_PROFILES = {
    "tcxo": {
        "name": "Temperature-Compensated Crystal Oscillator (TCXO)",
        "freq_offset": 5e-8,       # Initial fractional offset
        "aging_per_sec": 5e-13,    # ~ 4.3e-8 / day
        "temp_drift": 1e-7,        # Over operational temperature
        "typical_24h_drift_us": 5000.0  # ~ 5 ms/day
    },
    "standard_ocxo": {
        "name": "Standard Oven-Controlled Crystal Oscillator (OCXO)",
        "freq_offset": 5e-11,      # Initial fractional offset
        "aging_per_sec": 5e-16,    # ~ 4.3e-11 / day
        "temp_drift": 2e-10,
        "typical_24h_drift_us": 8.0     # ~ 5-10 us/day
    },
    "double_oven_ocxo": {
        "name": "Double-Oven OCXO (DOCXO)",
        "freq_offset": 1e-11,      # Initial fractional offset
        "aging_per_sec": 1e-16,    # ~ 8.6e-12 / day
        "temp_drift": 1e-11,
        "typical_24h_drift_us": 1.0     # ~ 1 us/day
    },
    "rubidium": {
        "name": "Rubidium Atomic Frequency Standard (Rb)",
        "freq_offset": 5e-12,      # Initial fractional offset
        "aging_per_sec": 5e-18,    # ~ 4.3e-13 / day
        "temp_drift": 3e-12,
        "typical_24h_drift_us": 0.2     # ~ 1-2 us/week
    },
    "csac": {
        "name": "Chip-Scale Atomic Clock (CSAC)",
        "freq_offset": 3e-11,      # Initial fractional offset
        "aging_per_sec": 1e-16,    # ~ 8.6e-12 / day
        "temp_drift": 3e-11,
        "typical_24h_drift_us": 3.0     # ~ 3 us/day
    }
}


def calculate_holdover_drift(oscillator_type: str, duration_seconds: float) -> Dict[str, Any]:
    """
    Calculate accumulated time error (drift) over a specified holdover duration.
    
    Formula:
    Δt = (Δf0/f0) * t + 0.5 * A * t^2 + temp_drift * t
    """
    profile = OSCILLATOR_PROFILES.get(oscillator_type.lower())
    if not profile:
        raise ValueError(f"Unknown oscillator type: '{oscillator_type}'. "
                         f"Options: {list(OSCILLATOR_PROFILES.keys())}")

    f0_offset = profile["freq_offset"]
    aging_rate = profile["aging_per_sec"]
    temp_rate = profile["temp_drift"]

    # Linear offset component (seconds)
    offset_drift = f0_offset * duration_seconds
    # Quadratic aging component (seconds)
    aging_drift = 0.5 * aging_rate * (duration_seconds ** 2)
    # Temperature drift component (seconds)
    temp_component = temp_rate * duration_seconds

    total_drift_sec = offset_drift + aging_drift + temp_component
    total_drift_us = total_drift_sec * 1e6

    return {
        "oscillator": oscillator_type,
        "name": profile["name"],
        "duration_seconds": duration_seconds,
        "duration_hours": duration_seconds / 3600.0,
        "total_drift_us": total_drift_us,
        "linear_component_us": offset_drift * 1e6,
        "aging_component_us": aging_drift * 1e6,
        "temp_component_us": temp_component * 1e6
    }


def max_holdover_time_for_target(oscillator_type: str, target_divergence_us: float) -> Dict[str, Any]:
    """
    Compute maximum time an oscillator can maintain holdover before exceeding target error.
    Solves 0.5 * A * t^2 + (Δf0/f0 + temp_drift) * t - target_sec = 0 using quadratic formula.
    """
    profile = OSCILLATOR_PROFILES.get(oscillator_type.lower())
    if not profile:
        raise ValueError(f"Unknown oscillator type: '{oscillator_type}'")

    target_sec = target_divergence_us * 1e-6
    a = 0.5 * profile["aging_per_sec"]
    b = profile["freq_offset"] + profile["temp_drift"]
    c = -target_sec

    # Quadratic formula: t = (-b + sqrt(b^2 - 4ac)) / (2a)
    discriminant = (b ** 2) - (4 * a * c)
    if discriminant < 0:
        return {"error": "No real solution"}

    t_sec = (-b + math.sqrt(discriminant)) / (2 * a)
    t_hours = t_sec / 3600.0

    return {
        "oscillator": oscillator_type,
        "name": profile["name"],
        "target_divergence_us": target_divergence_us,
        "max_holdover_seconds": t_sec,
        "max_holdover_hours": t_hours,
        "max_holdover_days": t_hours / 24.0
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Oscillator Holdover Calculator")
    parser.add_argument("--oscillator", choices=list(OSCILLATOR_PROFILES.keys()), default="standard_ocxo")
    parser.add_argument("--hours", type=float, default=24.0, help="Duration in hours")
    parser.add_argument("--target-us", type=float, default=None, help="Target max divergence in microseconds")

    args = parser.parse_args()

    if args.target_us is not None:
        res = max_holdover_time_for_target(args.oscillator, args.target_us)
        print(f"Oscillator: {res['name']}")
        print(f"Target Divergence: {res['target_divergence_us']} µs")
        print(f"Max Holdover: {res['max_holdover_hours']:.2f} hours ({res['max_holdover_days']:.2f} days)")
    else:
        res = calculate_holdover_drift(args.oscillator, args.hours * 3600.0)
        print(f"Oscillator: {res['name']}")
        print(f"Holdover Duration: {res['duration_hours']} hours")
        print(f"Total Drift: {res['total_drift_us']:.3f} µs")
