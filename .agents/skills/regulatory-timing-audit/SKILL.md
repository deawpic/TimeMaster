---
name: regulatory-timing-audit
description: "Conduct regulatory time compliance audits and generate audit trail dossiers for MiFID II RTS 25, FINRA CAT Rule 613, and 5G O-RAN. Validates traceability chains to UTC(k)/BIPM and exports UTF-8 reports."
category: compliance
risk: safe
tags: [mifid-ii, rts-25, finra-cat, compliance, audit, traceability, reports]
---

# Regulatory Timing Audit — MiFID II RTS 25, FINRA CAT & Metrological Traceability

Provides rigorous compliance auditing workflows for time synchronization in financial markets, telecommunications, and mission-critical networks according to international regulatory frameworks.

---

## 1. When to Activate This Skill

- When designing or reviewing clock synchronization for algorithmic, direct electronic access (DEA), or high-frequency trading (HFT) infrastructure.
- When generating compliance evidence for **MiFID II RTS 25** or **FINRA Rule 613 (CAT)**.
- When mapping or documenting the metrological traceability chain from BIPM/NMI down to host network cards (NICs).
- When preparing an audit report for financial regulators (ESMA, FCA, SEC, FINRA) to be archived in `reports/`.

---

## 2. Master Regulatory Thresholds

| Framework | Activity / System Tier | Maximum Permissible Divergence from UTC | Minimum Timestamp Resolution | Primary Regulatory Reference |
| :--- | :--- | :--- | :--- | :--- |
| **MiFID II (EU)** | High-Frequency Trading (HFT) | **$\le 100\ \mu\text{s}$** | **$1\ \mu\text{s}$** | RTS 25 (Regulation EU 2017/574), Table 1 |
| **MiFID II (EU)** | Electronic Trading (Non-HFT, colocation) | **$\le 1\ \text{ms}$** | **$1\ \text{ms}$** | RTS 25, Table 1 |
| **MiFID II (EU)** | Voice trading / RFQ / Manual systems | **$\le 1\ \text{s}$** | **$1\ \text{s}$** | RTS 25, Table 1 |
| **FINRA (US)** | Consolidated Audit Trail (CAT) — Electronic | **$\le 100\ \mu\text{s}$** | **$1\ \mu\text{s}$ (milliseconds if legacy)** | FINRA Rule 613 / CAT Clock Sync |
| **FINRA (US)** | CAT — Manual order handling | **$\le 50\ \text{ms}$** | **$1\ \text{s}$** | FINRA Rule 613(a)(2)(B) |
| **ITU-T / 3GPP** | 5G O-RAN Time Error (Class C/D) | **$\le \pm 1.5\ \mu\text{s}$ (Phase) / $\pm 10\ \text{ns}$ (Time)** | **$\text{Nanosecond}$** | ITU-T G.8271.1 / 3GPP TS 38.104 |

---

## 3. Metrological Traceability Chain Audit

Every compliant audit dossier must establish an unbroken calibration chain:

```text
[BIPM: UTC] 
     │ (Monthly Circular T publication)
     ▼
[National Metrology Institute: UTC(k)]  (e.g., PTB, NIST, NPL, NIMT)
     │ (GNSS Common-View / TWSTFT / Optical Link)
     ▼
[Master Reference Clock / PTP Grandmaster (PRTC-A/B)]
     │ (IEEE 1588-2019 Telecom Profile ITU-T G.8275.1)
     ▼
[Boundary Clocks / Transparent Switches]
     │ (Hardware Timestamping at NIC PHY/MAC)
     ▼
[Trading Host NIC (PHC) & Kernel CLOCK_REALTIME]
     │ (Kernel Timestamping / Socket SO_TIMESTAMPING)
     ▼
[Trading Application Matching Engine Event Log]
```

---

## 4. Compliance Audit Protocol & Report Generation

When generating an audit report:
1. **Identify Regulatory Tier**: Determine whether the workload falls under HFT ($100\ \mu\text{s}$), standard electronic ($1\ \text{ms}$), or manual ($1\ \text{s}$).
2. **Review Synchronization Logs**: Analyze continuous monitoring logs from `chrony` or `ptp4l` over the audit period (typically 30--90 days).
3. **Verify Holdover Capability**: Verify backup oscillator specifications to confirm how long the node remains compliant if GNSS or PTP signal is lost.
4. **Export Report**: Format the audit dossier in Markdown/JSON and save directly to `reports/<entity>_regulatory_timing_audit.md` using strict **UTF-8 encoding**.
