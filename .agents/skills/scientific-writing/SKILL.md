---
name: scientific-writing
description: "Core skill for writing publication-ready scientific papers, academic articles, and technical monographs on chronometry, global time architecture, distributed systems, and relativistic physics. Enforces IMRAD structure, formal LaTeX mathematical proofs, and peer-reviewed journal standards."
category: academic-writing
risk: safe
tags: [academic, scientific-writing, chronometry, latex, peer-review, IMRAD]
---

# Scientific Writing — Chronometry & Global Time Systems

This skill equips the agent to author publication-ready scientific manuscripts, comprehensive survey papers, technical monographs, and whitepapers in the domains of metrology, frequency standards, network timing, and distributed database consistency.

---

## 1. When to Activate This Skill

Activate this skill whenever:
- The user requests an academic paper, research report, or peer-reviewed style article (e.g. *"เขียนบทความวิชาการเรื่องการจัดการ Leap Second ในระบบคลาวด์"*, *"Write an academic paper on relativistic clock synchronization for Lunar Gateway"*).
- Structuring research using standard scientific formats (IMRAD: Introduction, Methods / Theoretical Foundations, Results / Architectural Implementations, Discussion & Impact).
- Formulating exact mathematical models in LaTeX (e.g. Allan deviation formulas, relativistic geodesy equations, packet offset proofs).
- Preparing submissions aligned with journals such as *Metrologia* (BIPM), *IEEE Transactions on UFFC*, *ACM Transactions on Computer Systems (TOCS)*, or *Physical Review D*.

---

## 2. Manuscript Architecture (The IMRAD Standard)

Every academic article must strictly adhere to the following architecture:

### 2.1 Title & Abstract
- **Title**: Precise, descriptive, avoiding hype words.
- **Abstract (Structured or Unstructured)**:
  - Background: What physical or computing challenge is addressed?
  - Problem Statement: What limitation exists in current paradigms?
  - Methodology / Architecture: What formal model or protocol is evaluated?
  - Key Findings / Analysis: Concrete metrics (latency in ns, drift in $\mu\text{s/day}$, uncertainty $\epsilon$).
  - Conclusion & Implications: Practical impact on global infrastructure.

### 2.2 Introduction
- First-principles framing: The fundamental physical or distributed systems law.
- Historical evolution and current paradigm (referencing `kb/global_time_standard_11_dimensions.md`).
- Explicit statement of the research gap and contribution.

### 2.3 Theoretical Foundations & Methodology (Methods)
- Mathematical formulation using KaTeX/LaTeX:
  $$\Delta t = \frac{\Delta t_0}{\sqrt{1 - \frac{v^2}{c^2}}} + \frac{\Delta \Phi}{c^2}$$
- Protocol mechanics or algorithm specifications (pseudo-code or formal state machines).
- Uncertainty budgets and error modeling.

### 2.4 System Architecture & Experimental Results (Results)
- Include at least 2 architectural diagrams using Mermaid (`mermaid-expert`).
- Tabular comparative data (e.g. holdover drift rates, NTP vs PTP jitter, commit-wait latencies).
- Clear quantitative analysis with explicit units ($\text{ns}$, $\mu\text{s}$, $\text{ms}$, $\text{ppm}$, $\text{Hz}$).

### 2.5 Discussion, Trade-offs & Future Horizons
- Practical trade-offs (e.g. TrueTime commit-wait throughput vs strict serializability).
- Edge cases and vulnerability analysis (e.g. asymmetric fiber delay, GNSS jamming, leap second bugs).
- Future transitions (e.g. Optical Lattice Clocks, 2035 Leap Second abolition, Lunar LTC).

### 2.6 References & Citations
- Standard citation format (IEEE or APA).
- Grounded in official RFCs (RFC 5905, RFC 8915), IEEE standards (1588-2019), BIPM publications (Circular T), and seminal papers.

---

## 3. Style Guidelines & Quality Invariants

- **Full Paragraphs**: Flowing prose with clear logical transitions. Avoid bullet-point lists in the main discussion sections of academic papers.
- **Tone**: Authoritative, dispassionate, precise, and scientifically rigorous.
- **Anti-AI Rule**: Run all text through `avoid-ai-writing` checks. No conversational filler, no machine clichés.
