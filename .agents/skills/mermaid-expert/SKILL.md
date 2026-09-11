---
name: mermaid-expert
description: "Master of Mermaid visualizations specialized for time architectures, network synchronization protocols, metrological pipelines, and distributed systems causality. Generates dark-mode compatible, mathematically clear diagrams."
category: visualization
risk: safe
tags: [mermaid, diagrams, time-architecture, sequence-diagram, stratum, ptp, ntp]
---

# Mermaid Expert — Time Architecture & Protocol Visualizations

Generates high-clarity, professionally styled Mermaid diagrams for technical articles, systems documentation, and academic publications.

---

## 1. When to Activate This Skill

- When illustrating the hierarchy of network time synchronization (Stratum 0 through Stratum 16).
- When diagramming packet exchanges (NTP 4-timestamp handshake, PTP IEEE 1588v2 two-step master/slave sync).
- When visualizing metrological pipelines (BIPM EAL/TAI/UTC synthesis, Circular T feedback loop).
- When illustrating distributed database causality (Google TrueTime $\epsilon$-uncertainty windows, commit-wait mechanics, Hybrid Logical Clocks).

---

## 2. Pre-Built Time Architecture Templates

### 2.1 PTP (IEEE 1588v2) Two-Step Message Exchange
```mermaid
sequenceDiagram
    autonumber
    participant M as Master Clock (Grandmaster)
    participant S as Slave Clock (Host NIC)

    Note over M,S: Hardware Timestamping Engine active at PHY/MAC layer
    M->>S: Sync Message (transmits at t1)
    M->>S: Follow_Up Message (contains precise t1 timestamp)
    Note over S: Slave records packet arrival at t2
    S->>M: Delay_Req Message (transmits at t3)
    Note over M: Master records packet arrival at t4
    M->>S: Delay_Resp Message (contains precise t4 timestamp)
    Note over S: Slave calculates:<br>Mean Path Delay = [(t4 - t1) - (t3 - t2)] / 2<br>Clock Offset = [(t2 - t1) - (t4 - t3)] / 2
```

### 2.2 BIPM Metrological Synthesis Pipeline
```mermaid
graph TD
    subgraph Labs ["Global NMI Laboratories (80+ Institutes)"]
        C1["Cesium-133 Clocks (450+)"]
        H1["Hydrogen Masers (Flywheels)"]
    end

    subgraph PhaseComp ["Phase & Frequency Difference (Every 5 Days)"]
        GNSS["Common-View GNSS"]
        TW["TWSTFT Satellite Microwave"]
    end

    subgraph BIPM ["BIPM Processing Pipeline (Sèvres, France)"]
        EAL["Échelle Atomique Libre (EAL)<br>Weighted Statistical Average"]
        PFS["Primary & Secondary Standards<br>Cesium Fountains & Optical Clocks"]
        TAI["International Atomic Time (TAI)<br>Frequency Steered to SI Second"]
        IERS["IERS Earth Rotation Parameters<br>UT1 via VLBI / Quasar Tracking"]
        UTC["Coordinated Universal Time (UTC)<br>Leap Second Alignment (|UTC - UT1| < 0.9s)"]
    end

    subgraph Output ["Global Dissemination"]
        CircT["BIPM Circular T (Monthly)<br>Published Offset: [UTC - UTC(k)]"]
        NIST["NIST (USA) UTC(NIST)"]
        NIMT["NIMT (Thailand) UTC(NIMT)"]
        PTB["PTB (Germany) UTC(PTB)"]
    end

    C1 --> GNSS & TW
    H1 --> GNSS & TW
    GNSS & TW --> EAL
    EAL --> PFS
    PFS --> TAI
    TAI --> UTC
    IERS --> UTC
    UTC --> CircT
    CircT -.->|Frequency Steering Feedback| NIST & NIMT & PTB
```

### 2.3 Network Stratum Hierarchy
```mermaid
graph TD
    S0["Stratum 0: Physical Clock Sources<br>(Cesium-133, Rubidium, GNSS L1/L2/L5, 1PPS Pulse)"]
    S1["Stratum 1: Primary Time Servers<br>(Direct Serial/PCIe Connection to S0, Hardware Timestamping NIC)"]
    S2["Stratum 2: Datacenter Core Clocks<br>(Syncs with multiple S1 servers via NTPv4 / NTS / PTP)"]
    S3["Stratum 3: Edge Gateways / Worker Nodes<br>(Syncs with S2 pool, disciplining Linux Kernel via Chrony)"]
    S16["Stratum 16: Unsychronized / In Holdover Exceeded"]

    S0 -->|Direct 1PPS + Serial NMEA| S1
    S1 -->|NTP UDP 123 / PTP Multicast| S2
    S2 -->|LAN Broadcast / Unicast| S3
    S3 -.->|Loss of signal > Max Drift| S16

    classDef s0 fill:#2d333b,stroke:#f0883e,stroke-width:2px,color:#e6edf3;
    classDef s1 fill:#2d333b,stroke:#58a6ff,stroke-width:2px,color:#e6edf3;
    classDef s2 fill:#2d333b,stroke:#3fb950,stroke-width:2px,color:#e6edf3;
    classDef s3 fill:#2d333b,stroke:#d29922,stroke-width:2px,color:#e6edf3;
    classDef err fill:#490202,stroke:#f85149,stroke-width:2px,color:#e6edf3;
    class S0 s0;
    class S1 s1;
    class S2 s2;
    class S3 s3;
    class S16 err;
```

### 2.4 Google Spanner TrueTime Commit-Wait Model
```mermaid
sequenceDiagram
    autonumber
    participant T1 as Transaction T1
    participant TT as TrueTime API [earliest, latest]
    participant DB as Globally Distributed Replica
    participant T2 as Transaction T2

    Note over T1: T1 initiates commit
    T1->>TT: TT.now()
    TT-->>T1: Returns [t1.earliest, t1.latest], uncertainty = ε
    Note over T1: Pick commit timestamp s = t1.latest
    Note over T1: Commit-Wait Rule: Wait until TT.now().earliest > s (duration 2ε)
    T1->>DB: Write changes with timestamp s
    Note over DB: Guaranteed: No subsequent transaction can pick timestamp <= s
    T2->>TT: TT.now() after T1 commit completes
    TT-->>T2: Returns [t2.earliest, t2.latest]
    Note over T2: Guaranteed: t2.earliest > s, preserving strict serializability!
```

---

## 3. Formatting & Syntax Rules

- **Dark Mode Friendly**: Use dark node fills (`#2d333b`), crisp borders (`#58a6ff`, `#3fb950`, `#f0883e`), and high-contrast text (`#e6edf3`).
- **Autonumber in Sequence Diagrams**: Always enable `autonumber` in sequence diagrams for clear reference in academic text.
- **Escape Characters & Quoting**: Always wrap node labels containing special characters (parentheses, brackets, colons, arithmetic symbols) in double quotes: `id["Label (extra)"]`.
- **Supported Diagram Declarations**: Strictly use supported diagram keywords: `flowchart`, `graph`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, `erDiagram`, `xychart-beta`.

---

## 4. Programmatic Syntax Validator Engine

The skill includes a dedicated syntax and structural validation CLI tool located at:
`scripts/syntax_validator.py`

### Capabilities:
1. **Mermaid Block Verification**:
   - Validates diagram type declarations and unsupported formats.
   - Detects unclosed blocks (`subgraph` ... `end`, `loop` / `alt` / `opt` ... `end`, composite state `{ }`).
   - Detects unquoted special characters in node labels (`()`, `[]`, `{}`) that cause Mermaid parser crashes.
   - Audits edge labels for unclosed pipes (`|`) and malformed arrow heads (`-->-`).
2. **Markdown Table Integrity**:
   - Audits column counts across table header, separator row (`|:---|`), and data rows.
   - Flags missing pipes or column count mismatches.
3. **Code Fence Integrity**:
   - Ensures all code fences (```) are properly matched and closed.

### Usage:
```bash
# Scan entire workspace or a directory:
python3 .agents/skills/mermaid-expert/scripts/syntax_validator.py --path . --strict

# Scan a single document:
python3 .agents/skills/mermaid-expert/scripts/syntax_validator.py --path reports/timing_audit.md

# Output as JSON:
python3 .agents/skills/mermaid-expert/scripts/syntax_validator.py --path kb/ --json
```
