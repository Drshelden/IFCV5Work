# 02 RFCs — RFC Index

38 candidate RFCs synthesized from the 59-topic *Proposed Topic Inventory*. All are at **Idea** status. The Decision Register (`01 Decision Register/IFC5_Decision_Register.xlsx`) is the authoritative status tracker.

**5 topics were not made into RFCs** — see the Deferred Topics tab in the Decision Register for rationale (topics 54, 55, 56, 57, 59).

---

## Tier 1 — Foundational
*Resolve these before anything else. All downstream RFCs depend on them.*

| ID | Title | Proto? | Source |
|---|---|---|---|
| IFC5-001 | Strategic Architecture Mode | No | 1, 3 |
| IFC5-002 | Normative Information Model Formalism | No | 2 |
| IFC5-003 | Identity Model | **Yes** | 8 |
| IFC5-004 | Path Model and Addressing | **Yes** | 9 |
| IFC5-005 | Namespace and Qualified Names | No | 6, 7 |
| IFC5-006 | Serialization and Encoding | No | 4, 55, 56, 57 |

## Tier 2 — Core Architecture
*Major structural decisions. Depend on Tier 1.*

| ID | Title | Proto? | Source |
|---|---|---|---|
| IFC5-007 | Scene Graph vs. ECS vs. Hybrid Architecture | **Yes** | 10, 11, 12, 58 |
| IFC5-008 | Relationship Modeling Strategy | **Yes** | 20, 21, 22 |
| IFC5-009 | Class and Type Representation | No | 13, 14, 26 |
| IFC5-010 | Composition, Inheritance, and Instancing | **Yes** | 11 |
| IFC5-011 | Document-Level Structure | No | 5 |
| IFC5-012 | Modular Schema Imports | No | 6 |
| IFC5-023 | Attribute Representation | No | 15 |
| IFC5-024 | Type System, Primitives, Enumerations, SELECTs | No | 16, 17, 18 |
| IFC5-025 | Collections and Cardinality | No | 19 |

## Tier 3 — Domain Modeling
*Domain-specific decisions. Depend on Tier 2.*

| ID | Title | Proto? | Source |
|---|---|---|---|
| IFC5-013 | Property Sets and Properties | **Yes** | 27 |
| IFC5-014 | Geometry Architecture | **Yes** | 30, 32, 37 |
| IFC5-015 | OpenUSD Alignment | **Yes** | 31, 33 |
| IFC5-016 | Spatial Structure and Decomposition | No | 23, 24 |
| IFC5-017 | Material Modeling | No | 29 |
| IFC5-026 | Openings, Voids, and Fillings | **Yes** | 25 |
| IFC5-027 | Classification and External Dictionaries | No | 28 |
| IFC5-028 | Units and Measures | No | 34 |
| IFC5-029 | Presentation and Appearance | No | 35 |
| IFC5-030 | Space Boundaries and Topology | No | 36 |
| IFC5-031 | Metadata and Custom Data | No | 38 |

## Tier 4 — Process & Governance
*Conformance, versioning, federation, and cross-cutting concerns.*

| ID | Title | Proto? | Source |
|---|---|---|---|
| IFC5-018 | Backward Compatibility and Round-Tripping | **Yes** | 39 |
| IFC5-019 | Validation Framework | No | 40, 41 |
| IFC5-020 | Model Views and Exchange Requirements | No | 42 |
| IFC5-021 | Federation and External References | No | 45 |
| IFC5-022 | Versioning and Schema Evolution | No | 44 |
| IFC5-032 | Extensibility | No | 43 |
| IFC5-033 | Change, Transactions, and Collaboration | No | 46 |
| IFC5-034 | Performance, Scale, and Database Implications | **Yes** | 47, 48 |
| IFC5-035 | Web and Linked-Data Alignment | No | 49 |
| IFC5-036 | AI and Machine-Readability | No | 50 |
| IFC5-037 | Security and Trust | No | 51 |
| IFC5-038 | Governance, Conformance, and Interoperability Testing | No | 52, 53 |

---

## Deferred / Absorbed Topics

| Topic | Title | Disposition |
|---|---|---|
| 54 | Hello Wall detailed comparison | Reference work → `03 Reference Examples/` |
| 55 | IFCX fine-grained syntax | Absorbed into IFC5-006, Section 11 |
| 56 | ECS fine-grained syntax | Absorbed into IFC5-006, Section 11 |
| 57 | IFC-SPF syntax reference | Reference for IFC5-018; no new decisions |
| 59 | Decision-record format | Already implemented as RFC template |

---

*38 RFCs covering all 59 source topics. Generated July 2026 from Proposed Topic Inventory.*
