# IFC5 Architecture Initiative — NUC to RFC Mapping

**Version:** 0.1 Draft · July 2026

This document maps the nine IFCX Not-Use-Cases (NUCs) defined by buildingSMART in [IFCX_NUC.md](https://github.com/buildingSMART/IFCX-CORE/blob/main/nuc/IFCX_NUC.md) to the IFC5 RFC set. Each NUC describes a capability that IFCX must support that IFC4/STEP cannot. The mapping identifies which RFCs carry the architectural decisions that enable (or constrain) each NUC.

---

## NUC 1 — Layered collaborative authoring with non-destructive overrides

Disciplines author in separate layers; downstream layers override upstream values non-destructively. No copy-modify-merge.

| RFC | Role |
|---|---|
| [RFC-IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) — Scene Graph vs ECS | **Foundational.** Layer/override semantics only exist natively in a scene graph architecture. A pure ECS has no override primitive; this NUC presupposes RFC-007 resolves toward scene graph or hybrid. |
| [RFC-IFC5-010](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) — Composition, Inheritance, Instancing | Override resolution rules and value precedence across layers. |
| [RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md) — Archetypes, Templates, Overrides | The specific override mechanism at the attribute level. |
| [RFC-IFC5-011](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) — Document Structure | What constitutes a "layer" at the document level; layer stack ordering. |
| [RFC-IFC5-033](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md) — Change, Transactions, Collaboration | Provenance of values per layer; auditable history of overrides. |

**Note:** This NUC is a strong argument in RFC-007's debate — the override capability is one of the primary reasons the scene graph model exists.

---

## NUC 2 — Collaboration in a decentralized, low-trust environment with evolving and partial information

Parties exchange partial and evolving model fragments across trust boundaries. Receivers must handle incomplete definitions without error.

| RFC | Role |
|---|---|
| [RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md) — Open World vs Closed World | **Foundational.** This NUC is the definitive argument for open-world semantics: partial definitions must be valid data, not schema violations. |
| [RFC-IFC5-010](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) — Composition, Inheritance, Instancing | Inheritance and defaults that allow incomplete definitions to be usable. |
| [RFC-IFC5-021](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) — Federation and External References | Cross-trust-boundary federation; how external fragments are referenced without full ownership. |
| [RFC-IFC5-033](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md) — Change, Transactions, Collaboration | Parallel authoring mechanics; how concurrent changes are reconciled. |
| [RFC-IFC5-037](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-037-security-trust.md) — Security and Trust | Access restrictions in a low-trust environment; attribute-level visibility controls. |

---

## NUC 3 — In-browser streaming and selective node loading

Individual nodes are addressable via HTTP. Clients load subsets progressively without downloading the full model.

| RFC | Role |
|---|---|
| [RFC-IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) — Identity Model | **Foundational.** UUID-based stable per-node identity is the prerequisite for selective HTTP addressing. Without stable IDs, node-level requests are not possible. |
| [RFC-IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md) — Path Model | Hierarchical path addressing that makes individual nodes HTTP-requestable by path. |
| [RFC-IFC5-006](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md) — Serialization and Encoding | JSON as the format that enables streaming without a sequential read requirement (unlike STEP). |
| [RFC-IFC5-034](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-034-performance-scale-database.md) — Performance, Scale, Database | Selective loading, progressive delivery, HTTP-range viability at large model scale. |

---

## NUC 4 — Third-party typed domain extensions without schema governance

Any party may define typed extensions using their own namespace. The core schema does not need to change; receivers preserve unknown attributes.

| RFC | Role |
|---|---|
| [RFC-IFC5-032](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md) — Extensibility | **Foundational.** Extension namespaces, unknown-attribute preservation policy, and governance model for third-party schemas. |
| [RFC-IFC5-005](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md) — Namespaces | Namespace URI ownership, collision avoidance, the `::` prefix convention. |
| [RFC-IFC5-012](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-012-modular-schema-imports.md) — Modular Schema Imports | How a third-party schema package is declared, versioned, and imported. |
| [RFC-IFC5-022](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-022-versioning-schema-evolution.md) — Versioning and Schema Evolution | Versioned, machine-readable schemas for extensions; receiver behaviour on version mismatch. |
| [RFC-IFC5-042](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-042-external-domain-data-standards.md) — External Domain Data Standards | The specific case where the "third party" is a recognized standards body (Brick, ASHRAE 223P, OGC, W3C WoT). |

---

## NUC 5 — Direct integration with game engine and web rendering pipelines

Geometry is expressed in mesh/USD terms usable by game engines and browsers without tessellation or geometry kernel dependencies.

| RFC | Role |
|---|---|
| [RFC-IFC5-014](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md) — Geometry Architecture | **Foundational.** Whether IFC5 geometry is mesh-first or B-rep-first; whether a geometry kernel dependency is eliminated. |
| [RFC-IFC5-015](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md) — OpenUSD Alignment | USD geometry semantics as the representation the NUC references; xformOp, mesh, and material alignment. |
| [RFC-IFC5-029](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-029-presentation-appearance.md) — Presentation and Appearance | glTF-compatible material definitions; visual override semantics for rendering. |
| [RFC-IFC5-006](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md) — Serialization and Encoding | JSON as the wire format for browser/web engine consumption. |

---

## NUC 6 — Stable object identity through the full asset lifecycle

Objects carry globally unique, stable identifiers from design through demolition, regardless of which tool or version touched them.

| RFC | Role |
|---|---|
| [RFC-IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) — Identity Model | **Foundational.** This NUC is the strongest single-sentence argument for UUID-based identity as a hard requirement rather than a convention. |
| [RFC-IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md) — Path Model | Hierarchically composable, globally unique paths built on stable UUIDs. |
| [RFC-IFC5-021](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) — Federation and External References | Identity stability when an object is federated into a larger model from a different origin. |
| [RFC-IFC5-022](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-022-versioning-schema-evolution.md) — Versioning and Schema Evolution | Identity persistence across schema revisions and tool transitions. |

---

## NUC 7 — Standardised delta and incremental update exchange

Parties exchange deltas — change sets rather than full models. Receivers apply deltas to their local state. Deletions are signalled explicitly (tombstones).

| RFC | Role |
|---|---|
| [RFC-IFC5-033](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md) — Change, Transactions, Collaboration | **Foundational.** Delta semantics, tombstone nodes for deletion, change history and provenance. |
| [RFC-IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) — Identity Model | Stable UUID paths are required for a receiver to apply a delta to the correct node unambiguously. |
| [RFC-IFC5-006](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md) — Serialization and Encoding | A delta must be a structurally valid IFCX subset document; the format must natively support partial documents. |
| [RFC-IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) — Scene Graph vs ECS | ECS flat arrays are structurally more diffable than a scene graph. The NUC's delta claim interacts with the architectural choice in RFC-007. |

---

## NUC 8 — Dereferenceable semantic linking to external data

IFC5 objects carry URI-typed attributes that link to external semantic resources — classification systems, sensor endpoints, FM databases — and those URIs are dereferenceable.

| RFC | Role |
|---|---|
| [RFC-IFC5-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md) — Web and Linked-Data Alignment | **Foundational.** Whether IFC5 objects publish dereferenceable URIs; the linked-data alignment model. |
| [RFC-IFC5-027](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md) — Classification and External Dictionaries | Classification references as URI-typed attributes; the NUC generalises this to all external semantic links. |
| [RFC-IFC5-023](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md) — Attribute Representation | URI as a schema-declared attribute type (not a free-text field); typed link semantics. |
| [RFC-IFC5-005](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md) — Namespaces | Namespace-addressable URIs as the structural mechanism the NUC depends on. |
| [RFC-IFC5-021](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) — Federation and External References | External references as a federation mechanism; pointer semantics across system boundaries. |
| [RFC-IFC5-042](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-042-external-domain-data-standards.md) — External Domain Data Standards | Sensor endpoints, FM platforms, and BAS systems are the specific external targets the NUC mentions. |

---

## NUC 9 — Formal assembly type instantiation

Type libraries (e.g., manufacturer product types) are published as URI-addressable definitions. Model instances reference types by URI; the type definition is live and dereferenceable.

| RFC | Role |
|---|---|
| [RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md) — Archetypes, Templates, Overrides | **Foundational.** This NUC is the primary motivation for RFC-040; manufacturer type libraries are exactly archetypes instantiated by reference, not by copy. |
| [RFC-IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md) — Class and Type Representation | How a type definition is declared, typed, and recognized by receivers. |
| [RFC-IFC5-010](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) — Composition, Inheritance, Instancing | Instantiation by reference rather than by copy; inheritance from type to instance. |
| [RFC-IFC5-021](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) — Federation and External References | URI pointer to externally published manufacturer type libraries; type as a federated external resource. |
| [RFC-IFC5-012](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-012-modular-schema-imports.md) — Modular Schema Imports | Type libraries as versioned, importable schema modules. |

---

## Coverage Summary

### RFCs with strong NUC coverage

These RFCs have at least one NUC that serves as a direct concrete motivation for the decision:

| RFC | NUCs |
|---|---|
| RFC-IFC5-003 Identity Model | NUC 3, 6, 7 |
| RFC-IFC5-004 Path Model | NUC 3, 6 |
| RFC-IFC5-005 Namespaces | NUC 4, 8 |
| RFC-IFC5-006 Serialization | NUC 3, 5, 7 |
| RFC-IFC5-007 Scene Graph vs ECS | NUC 1, 7 |
| RFC-IFC5-009 Class and Type | NUC 9 |
| RFC-IFC5-010 Composition, Inheritance | NUC 1, 2, 9 |
| RFC-IFC5-011 Document Structure | NUC 1 |
| RFC-IFC5-012 Modular Schema Imports | NUC 4, 9 |
| RFC-IFC5-014 Geometry Architecture | NUC 5 |
| RFC-IFC5-015 OpenUSD Alignment | NUC 5 |
| RFC-IFC5-021 Federation | NUC 2, 6, 8, 9 |
| RFC-IFC5-022 Versioning | NUC 4, 6 |
| RFC-IFC5-023 Attribute Representation | NUC 8 |
| RFC-IFC5-027 Classification | NUC 8 |
| RFC-IFC5-029 Presentation and Appearance | NUC 5 |
| RFC-IFC5-032 Extensibility | NUC 4 |
| RFC-IFC5-033 Change, Collaboration | NUC 1, 2, 7 |
| RFC-IFC5-034 Performance, Scale | NUC 3 |
| RFC-IFC5-035 Web and Linked Data | NUC 8 |
| RFC-IFC5-037 Security and Trust | NUC 2 |
| RFC-IFC5-040 Archetypes, Overrides | NUC 1, 9 |
| RFC-IFC5-041 Open World vs Closed World | NUC 2 |
| RFC-IFC5-042 External Domain Standards | NUC 4, 8 |

### RFCs not directly motivated by any NUC

The NUC document deliberately abstracts over domain modelling details and process questions. The following RFCs are not in tension with the NUCs — they address concerns the IFCX-CORE authors treat as either settled or out of scope for the capability statement:

RFC-IFC5-001 (Strategic Architecture Mode), RFC-IFC5-002 (Normative Formalism), RFC-IFC5-008 (Relationship Modeling), RFC-IFC5-013 (Property Sets), RFC-IFC5-016 (Spatial Structure), RFC-IFC5-017 (Material Modeling), RFC-IFC5-018 (Backward Compatibility), RFC-IFC5-019 (Validation Framework), RFC-IFC5-020 (Model Views and Exchange Requirements), RFC-IFC5-024 (Type System Primitives), RFC-IFC5-025 (Collections and Cardinality), RFC-IFC5-026 (Openings, Voids, Fillings), RFC-IFC5-028 (Units and Measures), RFC-IFC5-030 (Space Boundaries), RFC-IFC5-031 (Metadata and Custom Data), RFC-IFC5-036 (AI and Machine-Readability), RFC-IFC5-038 (Governance and Conformance), RFC-IFC5-039 (Accessibility).

---

## Observations for the Committee

**NUC 1 constrains RFC-007's outcome.** NUC 1's layer/override semantics are only achievable natively in a scene graph architecture. The committee should note this dependency explicitly when evaluating RFC-007 proposals.

**NUC 2 and RFC-041 are co-dependent.** The open-world question is not merely philosophical — NUC 2 represents a concrete class of real deployment scenarios (federated, partially-known data) that require open-world semantics to work at all.

**NUC 7 (deltas) and RFC-033 need tombstone specifics.** RFC-033 covers change and collaboration broadly, but NUC 7's tombstone-node requirement for explicit deletion signalling should be called out as a normative requirement in RFC-033's decision, not left as an implementation detail.

**The nine NUCs collectively imply a scene graph / open-world / URI-addressable architecture.** RFCs that pull in a different direction (e.g., a closed-world validation model, or STEP-style sequential identity) should be evaluated against this set of capability requirements before being advanced.

---

*IFC5 Architecture Initiative · July 2026*

*Source NUC document: [buildingSMART/IFCX-CORE — IFCX_NUC.md](https://github.com/buildingSMART/IFCX-CORE/blob/main/nuc/IFCX_NUC.md)*
