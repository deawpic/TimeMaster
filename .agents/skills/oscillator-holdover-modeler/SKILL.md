---
name: oscillator-holdover-modeler
description: "Simulate oscillator drift and calculate holdover budgets during GNSS loss. Models aging rates, temperature coefficients, and random walk phase noise for TCXO, OCXO, Rubidium, and CSAC."
category: modeling
risk: safe
tags: [holdover, oscillator, tcxo, ocxo, rubidium, csac, aging, allan-variance, gnss-loss]
---

# Oscillator Holdover Modeler — Holdover Budget & Aging Simulation

Models oscillator phase drift and time divergence when external synchronization references (e.g. GNSS or PTP Grandmaster) are unavailable.

---

## 1. When to Activate This Skill

- When designing timekeeping hardware resilience and calculating holdover budgets for telecom (5G O-RAN), financial exchanges (MiFID II), or data centers.
- When selecting oscillators (TCXO, OCXO, DOCXO, Rubidium, CSAC) based on outage duration and allowable drift tolerances.
- When computing how long an oscillator can maintain synchronization before exceeding a target error threshold (e.g., $1.5\ \mu\text{s}$ or $100\ \mu\text{s}$).

---

## 2. Theoretical Mathematical Model

The total accumulated time drift $\Delta t(T)$ over an uncalibrated holdover duration $T$ is given by:

$$\Delta t(T) = \underbrace{\left(\frac{\Delta f_0}{f_0}\right) \cdot T}_{\text{Initial Frequency Offset}} + \underbrace{\frac{1}{2} A \cdot T^2}_{\text{Linear Frequency Aging}} + \underbrace{\alpha_{\text{temp}} \cdot \Delta \theta \cdot T}_{\text{Temperature Drift}} + \underbrace{\epsilon_{\text{noise}}(T)}_{\text{Random Phase Walk}}$$

Where:
* $\Delta f_0 / f_0$: Fractional frequency offset at lock loss.
* $A$: Linear frequency aging rate ($\text{s}^{-1}$).
* $\alpha_{\text{temp}}$: Thermal frequency sensitivity coefficient ($1/^\circ\text{C}$).
* $\Delta \theta$: Temperature change over duration $T$.

---

## 3. Hardware Oscillator Comparison Table

| Oscillator Tier | Initial Fractional Offset ($\Delta f_0/f_0$) | Daily Aging ($A$) | Typical 24-Hour Drift | Max Duration for $1.5\ \mu\text{s}$ (5G) | Max Duration for $100\ \mu\text{s}$ (MiFID II) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TCXO** | $\sim 5 \times 10^{-8}$ | $\sim 4 \times 10^{-8}/\text{day}$ | $\sim 5\ \text{ms}$ | $< 1\ \text{minute}$ | $\sim 30\ \text{minutes}$ |
| **Standard OCXO** | $\sim 5 \times 10^{-11}$ | $\sim 4 \times 10^{-11}/\text{day}$ | $5\text{--}10\ \mu\text{s}$ | $\sim 4\text{--}8\ \text{hours}$ | $\sim 1\text{--}2\ \text{weeks}$ |
| **Double Oven OCXO** | $\sim 1 \times 10^{-11}$ | $\sim 8 \times 10^{-12}/\text{day}$ | $\sim 1\ \mu\text{s}$ | $\sim 24\text{--}36\ \text{hours}$ | $\sim 3\text{--}4\ \text{weeks}$ |
| **Rubidium (Rb)** | $\sim 5 \times 10^{-12}$ | $\sim 4 \times 10^{-13}/\text{day}$ | $\sim 0.2\ \mu\text{s}$ | $\sim 5\text{--}7\ \text{days}$ | $> 6\ \text{months}$ |
| **CSAC** | $\sim 3 \times 10^{-11}$ | $\sim 8 \times 10^{-12}/\text{day}$ | $\sim 3\ \mu\text{s}$ | $\sim 12\ \text{hours}$ | $\sim 2\text{--}3\ \text{weeks}$ |

---

## 4. Execution with Bundled Script

Run the calculation script directly:

```bash
# Calculate 24-hour drift on a standard OCXO
python3 .agents/skills/oscillator-holdover-modeler/scripts/holdover_math.py --oscillator standard_ocxo --hours 24

# Calculate max holdover duration for 1.5 µs target limit on Double-Oven OCXO
python3 .agents/skills/oscillator-holdover-modeler/scripts/holdover_math.py --oscillator double_oven_ocxo --target-us 1.5
```
