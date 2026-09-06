---
name: linux-timing-diagnostics
description: "Deep diagnostic workflows for Linux kernel timing, PHC hardware timestamping (ethtool -T), ptp4l/phc2sys servo loops, chronyc tracking, and adjtimex slew vs step behavior."
category: diagnostics
risk: safe
tags: [linux-kernel, ptp4l, phc2sys, chrony, ethtool, phc, hardware-timestamping, adjtimex]
---

# Linux Timing Diagnostics — Kernel, PHC & Network Timing Verification

Provides structured diagnostic procedures to audit Linux kernel timekeeping, NIC hardware timestamping capabilities, PTP servo convergence, and NTP/Chrony disciplining states.

---

## 1. When to Activate This Skill

- When diagnosing clock drift, phase jumps, or synchronization issues on Linux hosts.
- When verifying NIC hardware timestamping capabilities with `ethtool -T`.
- When auditing `ptp4l` and `phc2sys` logs to measure master offset, path delay, and RMS jitter.
- When evaluating `chronyc tracking` and `sources -v` metrics in production environments.
- When troubleshooting kernel clock slew vs. step behavior (`adjtimex`, `CLOCK_REALTIME`, `CLOCK_MONOTONIC_RAW`).

---

## 2. Hardware Timestamping Inspection (`ethtool -T`)

To verify if an interface supports PTP Hardware Timestamping:
```bash
ethtool -T <interface_name>
```

### Capability Checklist:
* **Hardware Transmit**: `hardware-transmit` (`SOF_TIMESTAMPING_TX_HARDWARE`)
* **Hardware Receive**: `hardware-receive` (`SOF_TIMESTAMPING_RX_HARDWARE`)
* **Raw Hardware Clock**: `hardware-raw-clock` (`SOF_TIMESTAMPING_RAW_HARDWARE`)
* **PTP Hardware Clock Index**: Must show a non-negative integer (e.g. `PTP Hardware Clock: 0` mapped to `/dev/ptp0`).

> If only `software-transmit` and `software-receive` are present, the NIC lacks PHY/MAC hardware timestamping and will exhibit packet stack jitter of $10\text{--}50\ \mu\text{s}$.

---

## 3. PTP Synchronization State Machine (`ptp4l`)

### Log Line Anatomy:
```text
ptp4l[1234.567]: rms   14 max   28 freq  -2415 +/-  12 delay  1234 +/-   3
```
* **rms**: Root mean square time error of the clock servo in nanoseconds. (Target: $< 50\ \text{ns}$ on LAN).
* **max**: Maximum absolute error recorded over the summary interval.
* **freq**: Frequency adjustment applied to the local oscillator in parts per billion (ppb).
* **delay**: Mean path delay (propagation time between master and slave) in nanoseconds.

### Port State Transitions:
1. `INITIALIZING` $\to$ Setting up hardware and sockets.
2. `LISTENING` $\to$ Awaiting Sync / Announce messages.
3. `UNCALIBRATED` $\to$ Master recognized; measuring initial path delay.
4. `SLAVE` $\to$ Locked and disciplining local PHC.

---

## 4. Kernel Clock Disciplining (`adjtimex` & chrony)

Linux manages time synchronization using either frequency slewing or time stepping:

* **Slew Mode**: Smoothly shifts the clock frequency by up to 500 ppm ($0.05\%$) without backward time jumps. Required for monotonic-sensitive applications (databases, trading engines).
* **Step Mode**: Instantly steps `CLOCK_REALTIME`. Triggers when offset exceeds threshold (e.g., `makestep 1.0 3` in `chrony.conf`).

### Diagnostic Commands:
```bash
# Check current system tracking metrics
chronyc tracking

# Check source jitter, offset, and reachability
chronyc sources -v

# Inspect kernel timekeeper status via adjtimex
adjtimex -p
```
