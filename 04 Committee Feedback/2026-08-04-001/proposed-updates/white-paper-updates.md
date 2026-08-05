# Proposed Updates: IFC5 Architecture White Paper
**Batch:** 2026-08-04-001
**Themes addressed:** 1, 2, 3, 4, 8

---

## Change 1: Correct closed-world statement on paths
**Section:** [§3.1.1 UUID as Canonical Identity](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#311-uuid-as-canonical-identity)
**Type:** Correct error
**Rationale:** The paper states IFCX creates a closed-world assumption by assigning each entity exactly one canonical position. aothms (Issue #2) and Ev both confirm this is incorrect — multiple simultaneous hierarchies can reference the same UUID. The path is an address, not an identity. No architectural change is needed; the prose is wrong.

**Current text (approximate):**
> This creates a closed-world assumption: an entity has exactly one canonical position in the hierarchy.

**Proposed replacement:**
> Paths are navigational aliases, not identity. The same UUID may appear in multiple simultaneous hierarchies — a window can be addressed both by its UUID and by paths in a spatial tree, a systems tree, or a discipline overlay simultaneously. The UUID is stable regardless of tree membership; the path is an address that depends on the view. Note that the current Hello Wall example demonstrates only a single spatial hierarchy; a multi-tree example is planned as a test case (see RFC-004).

---

## Change 2: Correct ProvenanceAuthority / no-auto-resolution contradiction
**Section:** [§3.1 — ProvenanceAuthority definition](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#31-three-identity-levels)
**Type:** Correct error (Bug — internal contradiction)
**Rationale:** The paper states "No system-imposed resolution destroys information" and describes IFCX as surfacing conflicts rather than resolving them. However, the `ProvenanceAuthority` enum defines a strict precedence (survey > as-built > design-intent > inferred) that auto-resolves conflicts when packages are merged. This is a direct contradiction. The resolution mechanism must be explicitly acknowledged, justified, or removed.

**Proposed addition after ProvenanceAuthority definition:**
> **Note — pending committee decision:** The `ProvenanceAuthority` ordering constitutes an implicit precedence rule. This is in tension with the principle that IFCX surfaces conflicts rather than resolving them. The committee must decide between three options: (a) retain the ordering as a normative default for plain queries, requiring consumers to declare when they want a different policy; (b) remove the precedence order and leave query behaviour as implementation-defined with mandatory disclosure; (c) keep provenance metadata but designate conflict resolution as out of scope for this version. Until this is resolved, implementations should treat the authority ordering as advisory only. See RFC-039 and RFC-041.

---

## Change 3: Clarify IfcRel* removal rationale
**Section:** [§3.3.3 Relationships](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#333-relationships)
**Type:** Background expansion
**Rationale:** The paper notes incomplete relation coverage without explaining why IfcRel* was deliberately removed. aothms explains: in Express, objectified relationships provided modularity through inverses and abstract supertypes within a global schema. In ECS, components with identity and provenance already provide this modularity, making objectified relationships redundant. This argument should appear in the paper. The `systems` example in the buildingSMART repo demonstrates complex many-to-many relationships without IfcRel*.

**Proposed addition:**
> IfcRel* objectified relationships are deliberately absent from IFCX. In Express, they provided modularity — through inverses and abstract supertypes — within a monolithic global schema. In the ECS model, typed components with explicit identity and provenance already provide this modularity. The combination would be redundant. Complex many-to-many relationships such as system membership and material associations are representable through typed relation components (see the Domestic Hot Water example in the buildingSMART reference repo). Note: this design decision remains contested; see RFC-008 for the open comparison.

---

## Change 4: Add transform composition gap notice
**Section:** [§3.4.1 Paths as Named Views, Not Identity](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#341-paths-as-named-views-not-identity)
**Type:** Correct error (Bug)
**Rationale:** The Hello Wall example positions windows as children of the storey (not the wall) because position is navigational. However, the windows retain wall-relative transform matrices. This only produces correct geometry because the wall has an identity transform. With any rotation or offset, the windows would render incorrectly. The paper must acknowledge this gap and the open question it creates.

**Proposed addition at end of §3.4.1:**
> **Known limitation — transform composition:** The current Hello Wall example works correctly only because the wall has an identity transform (no rotation, no offset). When position is decoupled from identity and an entity appears in a spatial view that differs from where its local transform was originally authored, the authoritative coordinate frame for composing transforms is undefined. Any spatial-view proposal must specify which graph is used for transform composition, and must demonstrate correctness with a non-identity wall transform. This is an open design question tracked in RFC-004 §9.

---

## Change 5: Revise USD composition engine characterisation
**Section:** [§4 Alignment with OpenUSD](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#4-alignment-with-openusd)
**Type:** Revise characterisation
**Rationale:** The paper implies that requiring consumers to implement USD composition logic is a new burden. aothms argues that IFC4 already required analogous resolution (TypeObject → PropertySet → occurrence inheritance), just expressed implicitly in walls of text. IFCX makes this explicit and formally specified. The paper should acknowledge this.

**Proposed addition:**
> Note: the composition resolution requirement is not entirely new. IFC4 required similar logic for TypeObject → PropertySet → occurrence inheritance, expressed through domain schema prose rather than a formal composition model. IFCX replaces an implicit, idiosyncratic resolution mechanism with an explicit, first-principled one. The burden on consumers is comparable; the gain is that the behaviour is formally specified and testable.
