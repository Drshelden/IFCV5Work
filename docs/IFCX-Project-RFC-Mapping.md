# IFC5 Architecture Initiative — IFCX Project Board to RFC Mapping

**Version:** 0.1 Draft · July 2026

Source: [buildingSMART IFCX Development Project — Project Planning view](https://github.com/orgs/buildingSMART/projects/9/views/7)

---

## Comparison

The IFCX development project board represents the buildingSMART working group's engineering agenda — 25 work items ranging from core architectural choices to operational decisions like licensing and contributions. The IFC5 Architecture Initiative RFC set represents a more granular decision framework: 42 structured decisions with explicit dependencies, tier classifications, and lifecycle tracking. Coverage is strong where it matters most — identity, types, geometry, layers, versioning, schema modularization, and linked data all map clearly across both lists. However, the two sets reveal complementary gaps: the IFCX project includes several process and governance topics (License, Contributions, Monorepo vs Split, Documentation) that have no RFC counterpart and are deliberately out of scope for an architectural decision record. Conversely, the RFC set covers IFC5-specific domain-modelling concerns with no IFCX project equivalent — spatial structure (RFC-016), space boundaries (RFC-030), openings and voids (RFC-026), accessibility (RFC-039), AI readability (RFC-036), security and trust (RFC-037), and backward compatibility (RFC-018) — reflecting that IFC5 carries obligations beyond the lean IFCX core format. The most significant alignment concern is architectural framing: the IFCX project treats the shift to composition/ECS (topics #4, #16) as largely settled direction, while the RFC set still holds RFC-007 (Scene Graph vs ECS) open as an undecided architectural fork — this divergence should be resolved before either effort moves to prototype.

---

## Topic-by-Topic Mapping

### 1. Entity and Component identification

How entities and components are uniquely identified within an IFCX document.

- [RFC-IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) — Identity Model *(direct)*
- [RFC-IFC5-004](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md) — Path Model *(path-based addressing of components)*
- [RFC-IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) — Scene Graph vs ECS *(what a "component" is depends on the architecture chosen)*
- [RFC-IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md) — Class and Type Representation *(entity typing)*

---

### 2. Types, typicals, and local placement

Type definitions, type instances, and how instances carry local overrides (e.g., position) relative to their type.

- [RFC-IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md) — Class and Type Representation *(direct)*
- [RFC-IFC5-010](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) — Composition, Inheritance, Instancing *(instantiation semantics)*
- [RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md) — Archetypes, Templates, Overrides *(local placement as an override on a typical)*

---

### 3. Persistent Collections & Data Segmentation

Grouping of objects into collections; partitioning a model into addressable segments.

- [RFC-IFC5-025](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-025-collections-cardinality.md) — Collections and Cardinality *(direct)*
- [RFC-IFC5-011](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) — Document-Level Structure *(segmentation at the document/layer level)*

---

### 4. Components definition

How components (in the ECS sense) are defined, typed, and composed.

- [RFC-IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) — Scene Graph vs ECS *(direct — component definition is the core ECS question)*
- [RFC-IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md) — Class and Type Representation
- [RFC-IFC5-008](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md) — Relationship Modeling *(relationships between components)*

**⚠ Alignment note:** The IFCX project treats this as a "Ready to do" work item, implying component-based architecture is decided. RFC-007 remains open in the IFC5 RFC set. These need to be reconciled.

---

### 5. Transport mechanism & System of Record

How IFCX data is exchanged (file, API, streaming) and what constitutes the authoritative source of record.

- [RFC-IFC5-006](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md) — Serialization and Encoding *(file-based transport)*
- [RFC-IFC5-034](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-034-performance-scale-database.md) — Performance, Scale, Database *(system of record; database as authoritative source)*
- [RFC-IFC5-021](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) — Federation and External References *(distributed system of record across federated models)*

---

### 6. Monorepo vs split

Whether the IFCX specification and schema are maintained in a single repository or split across multiple.

**→ No RFC equivalent.** This is a repository governance decision for buildingSMART, not an architectural decision for IFC5. Outside RFC scope.

---

### 7. Contributions

How external contributors participate in IFCX development (process, tooling, review).

**→ No RFC equivalent.** Process governance, not an IFC5 architectural decision. Loosely adjacent to [RFC-IFC5-038](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-038-governance-conformance.md) (Governance and Conformance) which addresses conformance testing governance, not contribution process.

---

### 8. Versioning

Schema versioning, data versioning, and how receivers handle version mismatches.

- [RFC-IFC5-022](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-022-versioning-schema-evolution.md) — Versioning and Schema Evolution *(direct)*
- [RFC-IFC5-018](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-018-backward-compatibility.md) — Backward Compatibility *(versioning implications for IFC4.x data)*

---

### 9. License

Licensing of the IFCX specification and any schema artefacts.

**→ No RFC equivalent.** Legal/administrative decision for buildingSMART. Out of RFC scope.

---

### 10. Separating primitives and schema entities

Distinguishing low-level type system primitives (strings, numbers, URIs) from domain-level schema entities (walls, spaces, sensors).

- [RFC-IFC5-024](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-024-type-system-primitives.md) — Type System Primitives *(direct)*
- [RFC-IFC5-002](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-002-normative-model-formalism.md) — Normative Model Formalism *(how the split is expressed normatively)*

---

### 11. File splitting, layers

Breaking a model into multiple files or layers; layer stack ordering and composition.

- [RFC-IFC5-011](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-011-document-structure.md) — Document-Level Structure *(direct — what a file/layer boundary is)*
- [RFC-IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) — Scene Graph vs ECS *(layers as scene graph sublayers)*
- [RFC-IFC5-021](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md) — Federation and External References *(federated files as a split-file mechanism)*

---

### 12. Conflict Handling & Layering

How conflicts between layers are defined and resolved; override precedence.

- [RFC-IFC5-033](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md) — Change, Transactions, Collaboration *(conflict detection and resolution)*
- [RFC-IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md) — Archetypes, Templates, Overrides *(override precedence rules)*
- [RFC-IFC5-010](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) — Composition, Inheritance, Instancing *(value resolution across composed layers)*
- [RFC-IFC5-041](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md) — Open World vs Closed World *(whether conflicting layers constitute a schema error or valid open-world state)*

---

### 13. Schema Modularisation

Breaking the IFCX schema into independently versioned, importable modules.

- [RFC-IFC5-012](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-012-modular-schema-imports.md) — Modular Schema Imports *(direct)*
- [RFC-IFC5-032](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md) — Extensibility *(third-party modules and governance)*

---

### 14. Metadata

Metadata on files, objects, schemas, and individual attributes.

- [RFC-IFC5-031](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-031-metadata-custom-data.md) — Metadata and Custom Data *(direct)*

---

### 15. IFCX relationship with USD (and ECS)

How IFCX positions itself relative to OpenUSD's scene description model and the ECS architectural pattern.

- [RFC-IFC5-015](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md) — OpenUSD Alignment *(direct — USD relationship)*
- [RFC-IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) — Scene Graph vs ECS *(direct — ECS relationship)*

---

### 16. From object-oriented to composition of components

The paradigm shift from IFC4.x's object-oriented hierarchy to a flat composition-of-components model.

- [RFC-IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) — Scene Graph vs ECS *(direct — this shift is the ECS proposition)*
- [RFC-IFC5-010](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-010-composition-inheritance.md) — Composition, Inheritance, Instancing *(composition semantics in the new model)*
- [RFC-IFC5-001](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md) — Strategic Architecture Mode *(the foundational framing of the paradigm shift)*

**⚠ Alignment note:** Same as topic #4 — IFCX project treats this as "Ready to do" while RFC-007 remains open.

---

### 17. Geometry Serialization

How geometric representations are encoded in IFCX format.

- [RFC-IFC5-014](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md) — Geometry Architecture *(direct)*
- [RFC-IFC5-006](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md) — Serialization and Encoding *(geometry as part of the overall encoding)*
- [RFC-IFC5-015](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-015-openusd-alignment.md) — OpenUSD Alignment *(USD geometry primitives as the candidate encoding)*

---

### 18. API Approach

REST, GraphQL, or other API patterns for accessing and querying IFCX data programmatically.

- [RFC-IFC5-034](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-034-performance-scale-database.md) — Performance, Scale, Database *(adjacent — covers server-side access patterns)*

**⚠ Gap in RFC set.** No RFC specifically addresses API design (REST vs GraphQL vs other patterns, endpoint conventions, authentication scope). If API is normative for IFCX conformance, a dedicated RFC is warranted.

---

### 19. Documentation

How the IFCX specification itself is authored, structured, and published.

**→ No RFC equivalent.** Operational/process decision for buildingSMART. Out of RFC scope.

---

### 20. Business rules

Validation constraints, cardinality rules, conditional requirements expressed alongside the schema.

- [RFC-IFC5-019](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-019-validation-framework.md) — Validation Framework *(direct — how business rules are expressed and tested)*
- [RFC-IFC5-020](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-020-model-views-exchange.md) — Model Views and Exchange Requirements *(exchange-scoped business rules)*

---

### 21. Linked data compatibility or extensibility

[Issue #123](https://github.com/buildingSMART/IFC5-development/issues/123) — Whether IFCX is compatible with linked data standards (RDF, JSON-LD, SPARQL) and/or extensible via linked data mechanisms.

- [RFC-IFC5-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md) — Web and Linked-Data Alignment *(direct)*
- [RFC-IFC5-005](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md) — Namespaces *(namespace URIs as the structural bridge to linked data)*
- [RFC-IFC5-032](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-032-extensibility.md) — Extensibility *(extensibility via external namespace is the linked-data extensibility pattern)*

---

### 22. Data and schema encoding

How data values and schema definitions are encoded (JSON, binary, EXPRESS, OWL/RDF, etc.).

- [RFC-IFC5-006](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-006-serialization-encoding.md) — Serialization and Encoding *(direct)*
- [RFC-IFC5-024](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-024-type-system-primitives.md) — Type System Primitives *(primitive types in the encoding)*
- [RFC-IFC5-023](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md) — Attribute Representation *(attribute-level encoding choices)*

---

### 23. Query & Filter Language

A standardized language or pattern for querying and filtering IFCX data.

- [RFC-IFC5-034](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-034-performance-scale-database.md) — Performance, Scale, Database *(adjacent — query patterns mentioned as a performance concern)*

**⚠ Gap in RFC set.** No RFC addresses a normative query or filter language. If IFCX defines one (comparable to SQL for relational or SPARQL for RDF), a dedicated RFC is needed.

---

### 24. Semantic work

Semantic alignment, ontological grounding, and vocabulary governance for IFCX concepts.

- [RFC-IFC5-027](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md) — Classification and External Dictionaries *(semantic vocabulary references)*
- [RFC-IFC5-035](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-035-web-linked-data.md) — Web and Linked-Data Alignment *(ontological grounding via RDF/OWL)*
- [RFC-IFC5-042](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-042-external-domain-data-standards.md) — External Domain Data Standards *(alignment with external semantic vocabularies)*
- [RFC-IFC5-005](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md) — Namespaces *(namespace as the mechanism for stable semantic identity)*

---

### 25. Properties and PSets

Property sets and individual properties: how non-geometric attributes are attached to objects in IFCX.

- [RFC-IFC5-013](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md) — Property Sets *(direct)*
- [RFC-IFC5-023](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-023-attribute-representation.md) — Attribute Representation *(individual property encoding)*

---

## RFCs in the IFC5 Set with No IFCX Project Board Counterpart

These reflect IFC5's domain-modelling obligations that IFCX-CORE, as a lean core format, has not yet surfaced as explicit work items:

| RFC | Topic |
|---|---|
| [RFC-IFC5-016](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md) | Spatial Structure (storeys, sites, zones) |
| [RFC-IFC5-017](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-017-material-modeling.md) | Material Modeling |
| [RFC-IFC5-018](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-018-backward-compatibility.md) | Backward Compatibility with IFC4.x |
| [RFC-IFC5-026](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-026-openings-voids-fillings.md) | Openings, Voids, Fillings |
| [RFC-IFC5-028](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-028-units-measures.md) | Units and Measures |
| [RFC-IFC5-029](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-029-presentation-appearance.md) | Presentation and Appearance |
| [RFC-IFC5-030](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-030-space-boundaries.md) | Space Boundaries |
| [RFC-IFC5-036](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-036-ai-machine-readability.md) | AI and Machine-Readability |
| [RFC-IFC5-037](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-037-security-trust.md) | Security and Trust |
| [RFC-IFC5-038](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-038-governance-conformance.md) | Governance and Conformance |
| [RFC-IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-accessibility.md) | Accessibility |

---

## Summary: Gaps and Misalignments

| Issue | Description |
|---|---|
| **RFC-007 vs IFCX project topics #4, #16** | IFCX project treats ECS/composition-based architecture as a decided direction ("Ready to do"); RFC-007 (Scene Graph vs ECS) remains an open decision in the IFC5 RFC set. These must be reconciled before prototyping begins. |
| **API Approach (topic #18)** | No RFC covers normative API design. If IFCX specifies a query/access API as part of the standard, a new RFC is needed. |
| **Query & Filter Language (topic #23)** | No RFC addresses a normative query or filter language. RFC-034 touches performance/database patterns but not a query language specification. |
| **Topics #6, #7, #9, #19** (Monorepo, Contributions, License, Documentation) | Process/governance/legal decisions with no RFC equivalent. Appropriately out of RFC scope. |
| **Domain modelling RFCs** (RFC-016, 026, 028–030, etc.) | IFC5 domain obligations not yet surfaced in the IFCX project board. Likely handled as IFCX domain extensions once the core format is stable. |

---

*IFC5 Architecture Initiative · July 2026*

*Source: [buildingSMART IFCX Development Project](https://github.com/orgs/buildingSMART/projects/9/views/7)*
