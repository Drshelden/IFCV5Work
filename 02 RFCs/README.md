# RFC Index

38 RFCs covering the major architectural decisions for IFC5. All are at **Idea** status — no decisions have been made yet. The [Decision Register](../01%20Decision%20Register/IFC5_Decision_Register.csv) is the authoritative status tracker.

---

## Tier 1 — Foundational
*Resolve these before anything else. All downstream RFCs depend on them.*

| ID | Title | Prototype Required? |
|---|---|---|
| IFC5-001 | Strategic Architecture Mode | No |
| IFC5-002 | Normative Information Model Formalism | No |
| IFC5-003 | Identity Model | Yes |
| IFC5-004 | Path Model and Addressing | Yes |
| IFC5-005 | Namespace and Qualified Names | No |
| IFC5-006 | Serialization and Encoding | No |

## Tier 2 — Core Architecture
*Major structural decisions. Depend on Tier 1.*

| ID | Title | Prototype Required? |
|---|---|---|
| IFC5-007 | Scene Graph vs. ECS vs. Hybrid Architecture | Yes |
| IFC5-008 | Relationship Modeling Strategy | Yes |
| IFC5-009 | Class and Type Representation | No |
| IFC5-010 | Composition, Inheritance, and Instancing | Yes |
| IFC5-011 | Document-Level Structure | No |
| IFC5-012 | Modular Schema Imports | No |
| IFC5-023 | Attribute Representation | No |
| IFC5-024 | Type System, Primitives, Enumerations, SELECTs | No |
| IFC5-025 | Collections and Cardinality | No |

## Tier 3 — Domain Modeling
*Domain-specific decisions. Depend on Tier 2.*

| ID | Title | Prototype Required? |
|---|---|---|
| IFC5-013 | Property Sets and Properties | Yes |
| IFC5-014 | Geometry Architecture | Yes |
| IFC5-015 | OpenUSD Alignment | Yes |
| IFC5-016 | Spatial Structure and Decomposition | No |
| IFC5-017 | Material Modeling | No |
| IFC5-026 | Openings, Voids, and Fillings | Yes |
| IFC5-027 | Classification and External Dictionaries | No |
| IFC5-028 | Units and Measures | No |
| IFC5-029 | Presentation and Appearance | No |
| IFC5-030 | Space Boundaries and Topology | No |
| IFC5-031 | Metadata and Custom Data | No |

## Tier 4 — Process & Governance
*Conformance, versioning, federation, and cross-cutting concerns.*

| ID | Title | Prototype Required? |
|---|---|---|
| IFC5-018 | Backward Compatibility and Round-Tripping | Yes |
| IFC5-019 | Validation Framework | No |
| IFC5-020 | Model Views and Exchange Requirements | No |
| IFC5-021 | Federation and External References | No |
| IFC5-022 | Versioning and Schema Evolution | No |
| IFC5-032 | Extensibility | No |
| IFC5-033 | Change, Transactions, and Collaboration | No |
| IFC5-034 | Performance, Scale, and Database Implications | Yes |
| IFC5-035 | Web and Linked-Data Alignment | No |
| IFC5-036 | AI and Machine-Readability | No |
| IFC5-037 | Security and Trust | No |
| IFC5-038 | Governance, Conformance, and Interoperability Testing | No |
