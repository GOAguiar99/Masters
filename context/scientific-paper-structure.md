# Scientific Paper Structure Context

## Purpose

When helping write or review dissertation chapters (or the related short papers), always distinguish between the following three sections:

1. System Model
2. Implementation
3. Evaluation

These sections answer different research questions and should not contain overlapping information.

In this repository the mapping is approximately:

| Role | Dissertation chapter (typical) | Short-paper sections |
|------|--------------------------------|----------------------|
| System Model | `chapters/3-chapter.tex` (`chap:sysmodel`) | SBESC/ETFA §System Model (not §Implementation) |
| Implementation | `chapters/4-chapter.tex` (`chap:implementation`) | SBESC §III-C / ETFA §Implementation |
| Evaluation | forthcoming Evaluation chapter | SBESC/ETFA §Evaluation |

**Hard rule for Chapter 3:** even though SBESC merges System Model and Implementation in one section, the dissertation System Model must stay technology-agnostic. Simulator versions, module/class names, config file naming, artifact URLs, seeds, and KPI instrumentation belong in Implementation or Evaluation.

Apply the separation checklist in [system-model-chapter-plan.md](system-model-chapter-plan.md) when reviewing Ch3 edits.

---

# 1. System Model

## Main Question

> What is the proposed system?

The System Model describes the proposed solution at a conceptual and abstract level. It explains the scientific contribution independently of any implementation technology.

## Should include

- Overall architecture
- System components
- Component interactions
- Communication model
- Data flow
- State machines
- Scheduling model
- Timing model
- Mathematical formulation
- Algorithms (high-level)
- Network topology
- Assumptions
- Constraints
- Threat/fault model (if applicable)

## Should NOT include

- Programming language
- Frameworks
- APIs
- Libraries
- Source code
- Class names
- File names
- Simulator-specific details
- Hardware-specific implementation

## Example

"The architecture consists of one Access Point responsible for computing transmission schedules and multiple wireless stations that periodically synchronize with the AP through beacon messages."

---

# 2. Implementation

## Main Question

> How was the proposed system built?

The Implementation section explains how the conceptual system was realized using specific software, hardware, or simulation tools.

## Should include

- Programming language
- Frameworks
- Libraries
- Simulator
- Hardware platform
- Software architecture
- Modules
- Class hierarchy
- APIs
- Integration between components
- Message definitions
- Configuration files
- Implementation decisions
- Important parameters

## Should NOT include

- Scientific motivation
- High-level architecture
- Algorithm derivation
- Theoretical proofs

## Example

"The scheduler was implemented as an extension of the INET Time-Aware Shaper module in OMNeT++ 6.1. Station sleep control was added by modifying the IEEE 802.11 MAC layer."

---

# 3. Evaluation

## Main Question

> Does the proposed system actually work?

The Evaluation section validates the proposed system through experiments, simulations, or real deployments.

Its objective is not to describe the system but to demonstrate that it achieves the intended goals.

## Should include

### Experimental Setup

- Hardware
- Software versions
- Simulation environment
- Network topology
- Workloads
- Input datasets
- Baseline methods
- Parameters

### Evaluation Methodology

- Experiment design
- Metrics
- Independent variables
- Controlled variables
- Number of repetitions
- Statistical methods

### Results

- Graphs
- Tables
- Performance measurements
- Resource utilization
- Scalability
- Latency
- Throughput
- Packet delivery ratio
- CPU usage
- Memory usage
- Energy consumption
- Synchronization accuracy
- Worst-case delay
- Confidence intervals (when applicable)

### Discussion

- Interpretation of results
- Comparison against baselines
- Advantages
- Limitations
- Threats to validity

## Should NOT include

- Implementation details
- Source code descriptions
- Architecture explanation
- New algorithms

## Example

"We compare the proposed scheduler against IEEE 802.11 EDCA under increasing network load. Results show a 45% reduction in worst-case latency while maintaining deterministic packet delivery."

---

# Separation Rule

Always ask:

## System Model

"If another researcher wanted to implement the proposed system in a completely different language or simulator, would this information still be necessary?"

If **yes**, it belongs in the **System Model**.

---

## Implementation

"If another researcher already understands the proposed system and wants to reproduce it using the same tools, would this information help?"

If **yes**, it belongs in the **Implementation**.

---

## Evaluation

"Does this information demonstrate that the proposed solution performs correctly or better than existing approaches?"

If **yes**, it belongs in the **Evaluation**.

---

# Typical Organization (dissertation / paper)

```
System Model
    - Architecture
    - Communication Model
    - Traffic / QoS / Timing Model
    - Algorithms / State Machines
    - Assumptions

Implementation
    - Software Architecture
    - Simulator
    - Module Design
    - Integration
    - Configuration

Evaluation
    - Experimental Setup
    - Metrics
    - Scenarios
    - Results
    - Discussion
```

---

# Writing Principles

- **System Model** explains **what** the proposed system is.
- **Implementation** explains **how** it was built.
- **Evaluation** explains **how well** it performs.

A reader should be able to:

1. Understand the idea after reading the **System Model**.
2. Reproduce the implementation after reading the **Implementation**.
3. Judge the scientific contribution after reading the **Evaluation**.

These three sections should complement one another without duplicating content.

---

# Crash-aware dissertation checklist (Ch3)

Remove from System Model if present:

| Content | Move to |
|---------|---------|
| OMNeT++ / INET / Veins / SUMO / TraCI names and versions | Implementation |
| Module/class names (`V2xHcf`, `QosClassifier`, `IdealObstacleLoss`, …) | Implementation |
| Config naming (`<policy>_netload_*`), `.ini` knobs as code identifiers | Implementation |
| Open artifact URL / `\cite{aguiar2026_veins_qos}` as primary cite | Implementation |
| Seed counts, CIs, KPI instrumentation | Evaluation |
| Result numbers, CDFs, comparison tables | Evaluation |

Keep in System Model if present:

| Content | Why |
|---------|-----|
| Decentralized OCB multicast architecture | Architecture / communication |
| Two-class BE/VO traffic and crash overlay | Traffic model |
| Five policies + listening/blocking/sending FSM | Algorithms / state machine |
| Crash timeline (normal → crash → recovery) | Timing model |
| Abstract radio/topology/load/policy parameters | Model parameters (tool-agnostic) |
| No DCC, no fading, binary obstruction, fixed PHY across policies | Assumptions |
