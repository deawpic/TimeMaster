---
name: docs-architect
description: "Architect comprehensive long-form technical manuals, enterprise timing architecture guides, and regulatory compliance dossiers (MiFID II, FINRA CAT, 5G O-RAN). Synthesizes hardware, software, and distributed consensus."
category: system-documentation
risk: safe
tags: [documentation, architecture, enterprise-timing, mifid-ii, compliance, longform]
---

# Docs Architect — Enterprise Timing Architecture & Manuals

Specializes in generating comprehensive, long-form systems documentation, technical monographs, and compliance audit dossiers for enterprise-scale time infrastructure.

---

## 1. When to Activate This Skill

- When designing full-scale datacenter time architectures across multi-region cloud or on-prem environments.
- When drafting compliance documentation for regulatory frameworks:
  - **MiFID II RTS 25**: Maximum divergence $\le 100\ \mu\text{s}$ to UTC with $1\ \mu\text{s}$ granularity for High-Frequency Trading.
  - **FINRA Rule 613 (CAT)**: Consolidated Audit Trail timestamp synchronization standards.
  - **ITU-T G.8275.1**: Telecom PTP profile for 5G cellular base stations and fronthaul.
- When creating complete multi-chapter technical manuals or ebooks on global time architecture.

---

## 2. Documentation Architecture Framework

A complete enterprise timing document produced by this skill adheres to the following blueprint:

```text
├── 1. Executive Summary & Regulatory Scope
├── 2. Physical & Hardware Layer Architecture
│   ├── Grandmaster Clocks & GNSS Antenna Topologies
│   ├── Local Oscillators (Holdover Budget: TCXO vs OCXO vs Rubidium)
│   └── NIC Hardware Timestamping & 1PPS Distribution
├── 3. Network Protocol & Synchronization Hierarchy
│   ├── Stratum Tree & Boundary Clock Placement
│   ├── PTP IEEE 1588-2019 Profile Configuration
│   └── Network Time Security (RFC 8915) Implementation
├── 4. Host OS Kernel & Clock Disciplining
│   ├── Linux Kernel timekeeper & adjtimex PLL/FLL Tuning
│   └── Clock Slew vs Step Policies & Leap Smearing
├── 5. Distributed Systems & Application Causality
│   ├── Database Consistency Models (TrueTime, HLC, Lamport)
│   └── Bounded Uncertainty (Epsilon) & Commit-Wait Latency
├── 6. Telemetry, Monitoring & Continuous Auditing
│   ├── Prometheus Metrics for Clock Offset & Jitter
│   └── Automated Alerts for Holdover Entry & GNSS Jamming
└── 7. Regulatory Traceability & Audit Trail
    └── End-to-end chain: SI Second → BIPM Circular T → NMI → Local Host
```

---

## 3. Best Practices

- **Explicit Uncertainty Budgets**: Break down total error budget into individual contributor terms (GNSS receiver antenna cable delay, NIC PHY jitter, OS kernel scheduling, fiber asymmetric delay).
- **Failure Mode Matrix**: Always include behavior under GPS denial/spoofing, fiber cuts, and leap second insertions.
