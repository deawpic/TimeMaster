---
name: verify-citations
description: "Verify academic citations, regulatory requirements, RFC numbers, and metrology standards against official registries (BIPM, IETF, IEEE, ITU-T). Ensures 100% factual accuracy in scientific writing without hallucinated references."
category: fact-checking
risk: safe
tags: [citations, fact-checking, metrology, rfc, ieee, bipm, standards]
---

# Verify Citations — Metrology & Standards Verification

Ensures that every citation, mathematical reference, standard number, and regulatory article referenced in TimeMaster documents corresponds to an authentic, authoritative source.

---

## 1. When to Activate This Skill

- Before finalizing academic manuscripts, whitepapers, or technical tutorials.
- When fact-checking regulatory requirements (e.g. MiFID II RTS 25 $100\ \mu\text{s}$ divergence, FINRA Rule 613 CAT).
- When citing IETF RFCs, IEEE standards, or ITU-T telecom profiles.
- When cross-referencing BIPM publications (Circular T, CGPM meeting resolutions, SI brochure).

---

## 2. Master Standards Reference Catalog

| Domain | Standard / Registry | Official Document | Technical Scope |
| :--- | :--- | :--- | :--- |
| **NTP** | IETF RFC | **RFC 5905** | Network Time Protocol Version 4: Protocol and Algorithms Specification. |
| **NTS** | IETF RFC | **RFC 8915** | Network Time Security for the Network Time Protocol (TLS 1.3 Key Exchange + Cookie AEAD). |
| **PTP** | IEEE Standard | **IEEE 1588-2019 (PTPv2.1)** | Standard for a Precision Clock Synchronization Protocol for Networked Measurement Systems. |
| **Time Format**| IETF RFC | **RFC 3339 / ISO 8601** | Date and Time on the Internet: Timestamps (Extended profile of ISO 8601). |
| **SyncE** | ITU-T Recommendation | **ITU-T G.8261 / G.8262** | Timing and synchronization aspects in packet networks / Synchronous Ethernet clocks. |
| **Telecom PTP**| ITU-T Recommendation | **ITU-T G.8275.1 / G.8275.2**| Precision time protocol telecom profile for phase/time synchronization. |
| **SI Second** | BIPM CGPM | **13th CGPM (1967)** | SI definition: 9,192,631,770 periods of radiation corresponding to the two hyperfine levels of Cesium-133 ground state. |
| **Leap Second Abolition** | BIPM CGPM | **27th CGPM Resolution 4 (2022)** | Decision to extend or abandon the maximum tolerance of UT1-UTC by or before 2035. |
| **Finance EU**| European Union ESMA | **MiFID II / RTS 25** | Clock synchronization requirements for algorithmic and high-frequency trading ($\le 100\ \mu\text{s}$ to UTC). |
| **Finance US**| US SEC / FINRA | **FINRA Rule 613 (CAT)** | Consolidated Audit Trail clock synchronization tolerances ($\le 50\ \text{ms}$ manual, $\le 100\ \mu\text{s}$ electronic). |
| **Distributed DB** | ACM OSDI '12 | **Corbett et al. (2012)** | *Spanner: Google's Globally-Distributed Database*, USENIX OSDI 2012. |

---

## 3. Verification Protocol

1. **Explicit Standard Identifier**: Every technical claim must include the standard identifier (e.g. `RFC 8915 Section 4` or `IEEE 1588-2019 Clause 16.2`).
2. **Arithmetic & Units Check**: Recompute all unit conversions (e.g., $100\ \mu\text{s} = 0.1\ \text{ms} = 100,000\ \text{ns}$).
3. **No Phantom Citations**: If a source cannot be directly verified against known RFCs or `kb/`, explicitly state it as an inference or unverified assumption rather than fabricating a citation.
