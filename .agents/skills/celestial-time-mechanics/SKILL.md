---
name: celestial-time-mechanics
description: "Celestial, lunar, and deep-space relativistic chronometry. Computes Coordinated Lunar Time (LTC ~ +56 µs/day) for NASA Artemis and ESA Moonlight, Coordinated Mars Time (MTC / Sol), and IAU coordinate time scales (TT, TCG, TCB, TDB)."
category: astrophysics
risk: safe
tags: [celestial-time, lunar-time, ltc, mars-time, mtc, artemis, relativity, iau, tcg, tcb, tdb]
---

# Celestial Time Mechanics — Lunar, Martian & Deep-Space Chronometry

Provides physical and relativistic formulations for establishing time standards beyond Earth, including **Coordinated Lunar Time (LTC)** for the Moon, **Coordinated Mars Time (MTC)**, and international astronomical coordinate clocks (**IAU TT, TCG, TCB, TDB**).

---

## 1. When to Activate This Skill

- When calculating relativistic time dilation for lunar landers, orbiters, or Artemis base camps.
- When working with **Coordinated Lunar Time (LTC)** directives (White House OSTP 2024, ESA Moonlight).
- When converting between Martian Sols and Earth SI seconds for Mars missions (MTC / Airy-0 meridian).
- When converting between terrestrial timekeeping ($TAI, UTC$) and barycentric/geocentric coordinate times ($TT, TCG, TCB, TDB$).

---

## 2. Coordinated Lunar Time (LTC) Physics

Clocks on the Moon tick **faster** than identical atomic clocks on Earth's geoid by approximately **$+56.0\ \mu\text{s}$ per Earth day** ($\approx 56.02\ \mu\text{s/day}$ depending on lunar topography).

### Mathematical Formulation:
$$\frac{d\tau_{\text{moon}}}{dt_{\text{earth}}} - 1 = \frac{W_0 - \left( U_{\text{moon}} + U_{\text{earth}}(a_{\text{moon}}) + \frac{1}{2} v_{\text{moon}}^2 \right)}{c^2} \approx +6.48 \times 10^{-10}$$

Where:
* $W_0 \approx 6.26368560 \times 10^7\ \text{m}^2/\text{s}^2$: Earth's geoid gravitational potential.
* $U_{\text{moon}} = \frac{G M_M}{R_M} \approx 2.821 \times 10^6\ \text{m}^2/\text{s}^2$: Moon's surface gravitational potential.
* $U_{\text{earth}}(a_M) = \frac{G M_E}{a_M} \approx 1.037 \times 10^6\ \text{m}^2/\text{s}^2$: Earth's gravitational potential at lunar orbit.
* $\frac{1}{2} v_{\text{moon}}^2 \approx 5.22 \times 10^5\ \text{m}^2/\text{s}^2$: Kinematic dilation from orbital motion.

In 24 Earth hours ($86,400\ \text{s}$):
$$\Delta \tau_{\text{daily}} = 6.48 \times 10^{-10} \times 86400\ \text{s} \approx +56.0\ \mu\text{s/day}$$

---

## 3. Coordinated Mars Time (MTC) & Sol Mechanics

* **1 Mars Sol**: $24\ \text{hours}, 39\ \text{minutes}, 35.244\ \text{seconds}$ ($88,775.244\ \text{s}$ SI).
* **Sol to Earth Day Ratio**: $\approx 1.02749125$.
* **Martian Second**: Standard SI second scaled or counted so that 1 Martian solar day equals 24 Mars hours (each hour consisting of 60 Mars minutes and 60 Mars seconds).
* **Gravitational Potential**: Lower Martian mass results in clocks ticking faster relative to Earth geoid by $\sim 489\ \mu\text{s/day}$ (ignoring eccentric solar modulation).

---

## 4. IAU Coordinate Clocks

* **Terrestrial Time (TT)**:
  $$TT = TAI + 32.184\ \text{s}$$
* **Geocentric Coordinate Time (TCG)**:
  $$TCG = TT + L_G \cdot (t - t_0), \quad L_G \approx 6.969290134 \times 10^{-10}$$
* **Barycentric Coordinate Time (TCB)**:
  $$TCB = TCG + L_B \cdot (t - t_0) + \text{periodic terms}, \quad L_B \approx 1.550519768 \times 10^{-8}$$

---

## 5. Execution with Bundled Script

```bash
# Calculate Coordinated Lunar Time (LTC) daily drift
python3 .agents/skills/celestial-time-mechanics/scripts/celestial_time.py --body moon

# Calculate Coordinated Mars Time (MTC) Sol duration
python3 .agents/skills/celestial-time-mechanics/scripts/celestial_time.py --body mars

# Convert IAU coordinate scales
python3 .agents/skills/celestial-time-mechanics/scripts/celestial_time.py --body coordinate
```
