---
name: gnss-security-auditor
description: "Analyze GNSS vulnerability and resilience against jamming and spoofing. Evaluates C/N0 signatures, AGC levels, RAIM integrity, multi-constellation cross-checks, and NTS RFC 8915 security."
category: security
risk: safe
tags: [gnss-security, spoofing, jamming, raim, cn0, agc, nts, rfc8915]
---

# GNSS Security Auditor — Jamming, Spoofing & Network Time Security

Provides structured security assessment frameworks for evaluating the integrity, authenticity, and resilience of GNSS-dependent timing systems and Network Time Security (NTS) protocols.

---

## 1. When to Activate This Skill

- When evaluating timing resilience against RF interference, jamming, or spoofing.
- When interpreting GNSS receiver anomaly metrics ($C/N_0$ drops, AGC shifts, RAIM alerts).
- When assessing multi-constellation redundancy (GPS, Galileo with OSNMA, BeiDou, GLONASS).
- When auditing Network Time Security (NTS) configurations according to **RFC 8915**.

---

## 2. RF Threat Signatures: Jamming vs. Spoofing

GNSS signals reach Earth's surface at extremely weak power levels ($\approx -160\ \text{dBW}$ or $\approx 10^{-16}\ \text{W}$), making them susceptible to interference.

| Metric / Indicator | Authentic Nominal State | Jamming Attack Signature | Spoofing Attack Signature |
| :--- | :--- | :--- | :--- |
| **Carrier-to-Noise ($C/N_0$)** | $35\text{--}50\ \text{dB-Hz}$ across satellites | Sudden collapse below $25\ \text{dB-Hz}$ across all channels | Improbably high or artificially identical $C/N_0$ |
| **Automatic Gain Control (AGC)** | Stable nominal range | Sharp drop in gain as receiver attenuates high-power RF noise | May oscillate or shift depending on spoofer power matching |
| **Pseudorange Residuals (RAIM)** | Residuals $< 5\ \text{m}$ | Lock lost, satellites dropped | Sudden inconsistency or gradual pull-off (drag-off attack) |
| **Constellation Cross-Check** | GPS $\approx$ Galileo $\approx$ BeiDou | All constellations degraded simultaneously (wideband jammer) | Disagreement between constellations if only GPS is spoofed |
| **1PPS Phase Output** | Jitter $< 10\ \text{ns}$ | 1PPS lost; receiver falls into holdover | 1PPS steers away from true UTC |

---

## 3. Defense & Hardening Architecture

1. **Multi-Constellation Multi-Frequency (MCMF)**:
   - Track L1/L5 (GPS) and E1/E5a (Galileo). Ionospheric delay cancellation and dual-frequency jamming resilience.
2. **Galileo OSNMA (Open Service Navigation Message Authentication)**:
   - Cryptographic verification of navigation data bits preventing forged broadcast ephemeris.
3. **CRPA (Controlled Reception Pattern Antenna)**:
   - Multi-element antenna with digital beamforming that creates spatial nulls in the direction of jamming/spoofing transmitters.
4. **Network Time Security (NTS RFC 8915)**:
   - **Phase 1 (NTS-KE)**: TLS 1.3 key exchange on port 4460 to negotiate symmetric keys and AEAD cookies.
   - **Phase 2 (NTS-NTP)**: Standard NTPv4 packets on port 123 carrying authenticated Extension Fields, preventing on-path tampering and spoofing.
