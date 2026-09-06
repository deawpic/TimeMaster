---
name: code-documentation-code-explain
description: "Explain and deconstruct complex timekeeping code, Linux kernel timekeeper (adjtimex, posix-timers), NIC hardware timestamping drivers, clock disciplining loops (PLL/FLL), and distributed clock algorithms (Spanner TrueTime, HLC, Lamport)."
category: code-education
risk: safe
tags: [code-explain, linux-kernel, adjtimex, truetime, hlc, lamport-clocks, timekeeper]
---

# Code Documentation & Code Explain — Time & Clocks Edition

Specializes in breaking down low-level timing implementations, kernel synchronization internals, socket-level hardware timestamping, and distributed consensus algorithms.

---

## 1. When to Activate This Skill

- When explaining how the Linux OS kernel maintains time (`kernel/time/timekeeping.c`, `do_adjtimex`).
- When demystifying socket options for hardware timestamping (`SOF_TIMESTAMPING_TX_HARDWARE`, `SOF_TIMESTAMPING_RX_HARDWARE`).
- When walking through distributed clock algorithms:
  - Lamport Logical Clocks (happens-before relation $\rightarrow$)
  - Vector Clocks (causal history tracking)
  - Hybrid Logical Clocks (HLC - combining physical wall clock with logical counters)
  - Google TrueTime API implementation and Spanner commit-wait loops.
- When deconstructing clock selection algorithms (e.g. Marzullo's algorithm in NTP).

---

## 2. Explanation Architecture

When explaining timing code, always follow this 4-tier breakdown:

### Tier 1: The First-Principles Invariant
What physical or logical property does this code guarantee?
*(e.g. "Linearizability requires that if transaction T2 begins after T1 commits, T2 must observe a timestamp strictly greater than T1.")*

### Tier 2: The Core Algorithm & Data Structure
Illustrate the key variables and state transitions:
```c
struct timex {
    unsigned int modes;     /* mode selector (ADJ_OFFSET, ADJ_FREQUENCY) */
    long offset;            /* time offset (nanoseconds/microseconds) */
    long freq;              /* frequency offset (scaled ppm) */
    long maxerror;          /* maximum error (microseconds) */
    long esterror;          /* estimated error (microseconds) */
    int status;             /* clock status bits (STA_PLL, STA_PPSTIME) */
    ...
};
```

### Tier 3: Step-by-Step Code Walkthrough
Explain line-by-line what happens during critical execution paths (e.g. why `adjtimex` modulates the timer tick multiplier rather than jumping the wall clock).

### Tier 4: Edge Cases & Pitfalls
- Handling integer overflow (e.g. 32-bit `time_t` Year 2038).
- Dealing with leap second insertion flags (`STA_INS` / `STA_DEL`).
- Negative delta handling in monotonic clocks.
- Clock drift exceeding local oscillator disciplining limits ($\pm 500\ \text{ppm}$).
