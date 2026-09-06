---
name: sympy-time-mechanics
description: "Symbolic and numerical mathematical engine for exact time physics, relativistic mechanics, Allan variance frequency stability analysis, network packet timing calculus, and orbital clock dilation."
category: computation
risk: safe
tags: [math, physics, relativity, allan-variance, sympy, ntp-math, gps-dilation]
---

# SymPy Time Mechanics — Relativistic & Chronometric Computation

Provides symbolic algebra, exact physical calculations, and numerical proofs for chronometry, relativistic time dilation, oscillator noise modeling, and packet synchronization.

---

## 1. When to Activate This Skill

- When calculating special relativistic time dilation ($\Delta t = \gamma \Delta t_0$) for moving bodies (satellites, aircraft, particle beams).
- When calculating general relativistic gravitational redshift ($\Delta f / f = \Delta \Phi / c^2$) across altitudes and gravitational bodies (Earth geoid, Moon LTC, Mars MTC).
- When computing Allan Deviation ($\sigma_y(\tau)$) for oscillator stability from frequency time series.
- When solving NTP/PTP 4-timestamp packet delay and offset equations.
- When computing epoch boundaries (e.g. Unix 32-bit Year 2038 integer overflow, GPS 1024-week rollover).

---

## 2. Bundled Mathematical CLI

Run the bundled time mechanics engine:

```bash
# Execute standard time physics calculations
python3 .agents/skills/sympy-time-mechanics/scripts/time_math.py
```

### Python API Integration:
```python
from sympy_time_mechanics.scripts.time_math import (
    calculate_gps_relativistic_effects,
    calculate_ntp_packet_math,
    calculate_allan_deviation,
    calculate_y2038_overflow_epoch
)

# GPS Relativistic Drift (+38.44 us/day net)
gps_drift = calculate_gps_relativistic_effects()
print(f"Net daily drift: {gps_drift['net_daily_drift_us']} us")
print(f"Steered frequency: {gps_drift['steered_frequency_hz']} Hz")

# NTP Round-Trip Delay and Clock Offset
ntp = calculate_ntp_packet_math(t1=100.0, t2=100.015, t3=100.018, t4=100.035)
print(f"Delay: {ntp['round_trip_delay']*1000} ms, Offset: {ntp['clock_offset']*1000} ms")
```

---

## 3. Mathematical Foundations

### 3.1 Relativistic Time Dilation
The net fractional frequency shift for an orbiting clock is:
$$\frac{\Delta f}{f} = \frac{\Delta \Phi}{c^2} - \frac{v^2}{2c^2} = \frac{GM}{c^2}\left(\frac{1}{R_{\text{Earth}}} - \frac{1}{R_{\text{orbit}}}\right) - \frac{v^2}{2c^2}$$

### 3.2 Allan Variance
$$\sigma_y^2(\tau) = \frac{1}{2(N-1)}\sum_{i=1}^{N-1}(y_{i+1} - y_i)^2$$
Separates White Phase Noise ($\tau^{-1}$), White Frequency Noise ($\tau^{-1/2}$), Flicker Phase Noise ($\tau^{-1}$), and Random Walk Frequency Noise ($\tau^{1/2}$).
