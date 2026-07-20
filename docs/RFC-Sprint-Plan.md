# IFC5 RFC Sprint Discussion Plan

**Purpose:** Group the 40 IFC5 RFCs into 2-week discussion sprints for the committee. Each sprint covers a cluster of inter-related RFCs that share dependencies or must be resolved together. The sequence moves from the most foundational decisions — those that constrain all subsequent choices — to the most domain-specific and governance-level topics.

---

## Logic for This Organization

The groupings follow a strict dependency ordering principle: **do not discuss a concept before its prerequisite is decided**. The two most consequential forks are:

1. **The architectural fork** (Sprint 1): Scene graph vs. ECS vs. hybrid is the single decision that most constrains everything else — identity model, path model, type system, archetype mechanism, serialization, and more. If the committee resolves this early, subsequent sprints can reason concretely rather than speculatively.

2. **The data primitive fork** (Sprint 2–3): Once the architecture is chosen, the identity and serialization decisions must be locked before domain modeling can proceed. These are not domain questions — they are infrastructure decisions.

After these two clusters, the plan moves through progressively domain-specific topics: schema structure, geometry, property data, presentation, and finally governance. Each sprint's RFCs share enough surface area that they naturally surface overlapping questions and tradeoffs when discussed together.

A note on RFCs 039, 040, and 041: These were added to fill gaps in the foundational and core tiers. IFC5-039 (JSON Data Model) belongs in Sprint 1 because it establishes the data model assumptions shared by both IFCX and IFC-ECS. IFC5-040 (Archetypes) belongs in Sprint 4 because it depends on the type and identity decisions from Sprints 1–3. IFC5-041 (Open World vs. Closed World) belongs at the top of Sprint 1 — it is a meta-premise that determines how RFC-001, RFC-003, RFC-004, RFC-007, and RFC-021 should be answered.

---

## Sprint Schedule

### Sprint 1 — The Architectural Fork
**RFCs: 001, 039, 041, 007**

These four RFCs together define the entire strategic direction of IFC5. RFC-041 asks whether IFC5 adopts an open-world or closed-world assumption — this is the most foundational premise of all, because almost every other decision has a different answer depending on which world you are designing for. RFC-001 asks what kind of standard IFC5 is (extensible profile-based? prescriptive monolith?). RFC-039 establishes the shared data model assumptions (JSON as the substrate, component as a primitive, value vs. reference encoding). RFC-007 is the single most consequential technical question: scene graph, ECS, or hybrid.

The committee should aim for either a decision or a narrowed set of live options by end of Sprint 1. Ideally RFC-041 is resolved first within the sprint, since its outcome directly constrains how RFC-001 and RFC-007 are framed.

---

### Sprint 2 — Identity and Addressing
**RFCs: 002, 003, 004, 005**

Once the architectural direction is set, the identity and addressing model must be decided before anything else. RFC-003 (Identity: GUID vs. path vs. URI) and RFC-004 (Path Model) are tightly coupled — the path is load-bearing for scene graph override semantics but irrelevant to flat ECS. RFC-005 (Namespaces) depends on how identifiers are structured. RFC-002 (Normative Formalism: EXPRESS, OWL, JSONSchema) determines how all subsequent RFCs are formally specified.

These four form a coherent "plumbing" cluster: get them wrong and the specification is incoherent at the reference level.

---

### Sprint 3 — Data Primitives
**RFCs: 006, 023, 024, 025**

With identity decided, the committee can pin down how data is encoded at the attribute level. RFC-006 (Serialization) determines what the normative file format is. RFC-023 (Attribute Representation) defines how attribute names, types, and values are expressed in JSON. RFC-024 (Type System and Primitives) establishes what scalar types exist. RFC-025 (Collections and Cardinality) defines how sets, lists, and optional values are modeled.

These four RFCs together define the "vocabulary" of IFC5 data — the rules every component, property set, and domain object must follow.

---

### Sprint 4 — Type System, Relationships, and Archetypes
**RFCs: 008, 009, 010, 040**

With data primitives locked, the committee can tackle the object model. RFC-009 (Class and Type Representation) and RFC-010 (Composition, Inheritance, Instancing) define how types are declared and how instances relate to types. RFC-040 (Archetypes and Override Mechanisms) depends directly on these two — archetypes are a more powerful form of type instantiation. RFC-008 (Relationship Modeling) must be discussed here because the choice between explicit relationship entities (IFC4.x style) and inline references (ECS style) interacts directly with the type and identity decisions.

This sprint resolves the "object model" layer of IFC5.

---

### Sprint 5 — Document and Module Structure
**RFCs: 011, 012, 021, 032**

With the object model settled, the committee can decide how IFC5 files and schemas are organized. RFC-011 (Document-Level Structure) defines what a valid IFC5 file looks like at the top level. RFC-012 (Modular Schema Imports) governs how schema modules reference each other. RFC-021 (Federation and External References) defines how models can reference other models. RFC-032 (Extensibility) determines how third parties add proprietary or domain-specific data without breaking conformance.

These four define the "packaging" layer — how individual objects are assembled into coherent files and ecosystems.

---

### Sprint 6 — Geometry and Spatial Structure
**RFCs: 014, 015, 016, 030**

Geometry is IFC's largest and most complex domain. RFC-014 (Geometry Architecture) establishes whether IFC5 uses an internal geometry kernel, delegates to USD/OpenUSD, or provides a pluggable interface. RFC-015 (OpenUSD Alignment) determines the relationship between IFC5 and USD specifically — this has major implications for geometry and the scene graph model. RFC-016 (Spatial Structure) defines building storey, site, and spatial containment. RFC-030 (Space Boundaries and Topology) handles room/zone boundary calculations, which depend on the spatial model.

This sprint is geometry-focused and can productively include prototype evidence from the Hello-Wall reference examples.

---

### Sprint 7 — Domain Properties and Classification
**RFCs: 013, 017, 027, 028**

These four RFCs cover the domain data that populates building elements. RFC-013 (Property Sets) defines how shared and instance properties are attached to elements — a direct descendant of IFC4.x Psets. RFC-017 (Material Modeling) covers material assignment, layers, and constituents. RFC-027 (Classification and External Dictionaries) handles links to external classification systems (UniClass, OmniClass, etc.). RFC-028 (Units and Measures) pins down how numeric values carry unit information.

This sprint is primarily domain modeling and is less dependent on architectural decisions — but the property set model must align with the attribute representation from Sprint 3.

---

### Sprint 8 — Presentation, Metadata, and Change
**RFCs: 026, 029, 031, 033**

These four RFCs cover data that enriches or annotates building elements rather than defining their primary structure. RFC-026 (Openings, Voids, and Fillings) is a domain modeling question about how subtracted geometry is represented. RFC-029 (Presentation and Appearance) covers colors, rendering materials, and visual overrides. RFC-031 (Metadata and Custom Data) handles model-level headers, author info, and freeform extension data. RFC-033 (Change, Transactions, and Collaboration) addresses how model history and concurrent edits are tracked.

These topics are relatively self-contained once the foundational RFCs are resolved.

---

### Sprint 9 — Compatibility, Validation, and Governance
**RFCs: 018, 019, 020, 022, 038**

These five RFCs address the lifecycle and process layer of the standard. RFC-018 (Backward Compatibility) and RFC-022 (Versioning and Schema Evolution) must be discussed together — they define the migration path from IFC4.x and the rules for future IFC5 revisions. RFC-019 (Validation Framework) defines what "conformant" means and how it is tested. RFC-020 (Model Views and Exchange Requirements) determines how IFC5 subsets the standard for specific use cases (like structural or MEP). RFC-038 (Governance, Conformance, and Interoperability Testing) closes the loop on certification and test suites.

This sprint is process and standards-governance focused, and benefits from having the full technical picture in hand.

---

### Sprint 10 — Cross-Cutting Quality Attributes
**RFCs: 034, 035, 036, 037**

The final sprint covers RFCs that apply as constraints across the entire standard rather than defining a specific domain. RFC-034 (Performance, Scale, Database) examines whether IFC5's object model choices are viable at the scale of large infrastructure projects and supports common database storage strategies. RFC-035 (Web and Linked-Data Alignment) addresses JSON-LD, RDF, and REST API compatibility. RFC-036 (AI and Machine-Readability) covers the structural and semantic requirements for AI tooling to parse and reason over IFC5. RFC-037 (Security and Trust) addresses digital signatures, access control, and data provenance.

These are discussed last not because they are unimportant, but because they function as quality gates — the committee can evaluate how well the choices made in Sprints 1–9 satisfy each of these cross-cutting requirements, and identify where revisions are needed.

---

## Summary Table

| Sprint | Theme | RFCs | Key Question |
|--------|-------|------|--------------|
| 1 | The Architectural Fork | 001, 039, 041, 007 | Open or closed world? Scene graph or ECS? JSON as normative? |
| 2 | Identity and Addressing | 002, 003, 004, 005 | How are things named and found? |
| 3 | Data Primitives | 006, 023, 024, 025 | How is data encoded at the field level? |
| 4 | Type System and Archetypes | 008, 009, 010, 040 | How do types, inheritance, and overrides work? |
| 5 | Document and Module Structure | 011, 012, 021, 032 | How are files and schemas organized? |
| 6 | Geometry and Spatial | 014, 015, 016, 030 | What is the geometry and spatial model? |
| 7 | Domain Properties | 013, 017, 027, 028 | How is building element data attached? |
| 8 | Presentation, Metadata, Change | 026, 029, 031, 033 | How is annotation and history handled? |
| 9 | Compatibility and Governance | 018, 019, 020, 022, 038 | How does IFC5 evolve and certify? |
| 10 | Cross-Cutting Quality | 034, 035, 036, 037 | Does IFC5 meet scale, web, AI, and security needs? |

**Total:** 10 sprints × 2 weeks = 20 weeks (~5 months) for a full pass through all 40 RFCs.

---

*This plan is a recommendation, not a constraint. The committee may choose to reorder or split sprints based on working group availability, prototype readiness, or emerging dependencies.*
