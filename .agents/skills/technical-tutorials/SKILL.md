---
name: technical-tutorials
description: "Author step-by-step, reproducible hands-on technical tutorials and configuration guides for time systems, NTPv4/NTS servers, PTP IEEE 1588v2 daemons (ptp4l, phc2sys), Linux kernel disciplining, and GPS 1PPS hardware setups."
category: tutorial-engineering
risk: safe
tags: [tutorial, howto, chrony, ptp, ntp, nts, linuxptp, hardware-timestamping]
---

# Technical Tutorials — Time Infrastructure & Systems Engineering

Provides structured methodology for crafting reproducible, production-grade tutorials, deployment runbooks, and hands-on walkthroughs for time synchronization infrastructure.

---

## 1. When to Activate This Skill

- When the user asks for a step-by-step setup guide or tutorial (e.g. *"สอนวิธีตั้งค่า Chrony ให้รองรับ NTS บน Ubuntu 24.04"*, *"How to configure ptp4l and phc2sys with Intel NIC hardware timestamping"*).
- When creating hands-on guides for building a DIY Stratum 1 NTP server with Raspberry Pi, GNSS receiver, and 1PPS GPIO.
- When writing operational runbooks for leap second smearing, firewall UDP 123 rules, or PTP boundary clock deployments.

---

## 2. Mandatory Tutorial Architecture

Every technical tutorial must follow this 6-part structure:

### 1. Prerequisites & Bill of Materials
- Operating system version (e.g. Ubuntu 24.04 LTS, RHEL 9, Debian 12).
- Hardware requirements (NIC supporting `SOF_TIMESTAMPING_TX_HARDWARE`, GNSS antenna, SMA coaxial cable).
- Required software packages (`chrony`, `linuxptp`, `gpsd`, `ethtool`).

### 2. Network & Kernel Validation
- Check NIC timestamping capabilities:
  ```bash
  ethtool -T eth0
  ```
- Check PPS device attachment:
  ```bash
  ls -l /dev/pps*
  sudo ppstest /dev/pps0
  ```

### 3. Step-by-Step Configuration Files
- Full configuration snippets with inline comments explaining critical parameters:
  - For Chrony (`/etc/chrony/chrony.conf`): `server`, `nts`, `refclock PPS`, `makestep`, `rtcsync`.
  - For LinuxPTP (`/etc/linuxptp/ptp4l.conf`): `time_stamping hardware`, `network_transport L2`, `delay_mechanism E2E`.

### 4. Service Daemon Management
- Precise systemd commands to enable, start, and verify service health:
  ```bash
  sudo systemctl restart chrony
  sudo systemctl status chrony --no-pager
  ```

### 5. Verification & Telemetry Inspection
- Deterministic commands to verify synchronization:
  ```bash
  chronyc sources -v
  chronyc tracking
  pmc -u -b 0 'GET TIME_STATUS_NP'
  ```

### 6. Troubleshooting & Common Pitfalls
- Handling asymmetric network delay.
- GNSS antenna multipath and satellite lock loss.
- Firewall UDP 123 and TLS 4460 (NTS-KE) blocking.
- Preventing clock steps during database transactions.
