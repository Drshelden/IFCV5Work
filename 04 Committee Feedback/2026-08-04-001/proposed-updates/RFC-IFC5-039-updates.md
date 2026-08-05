# Proposed Updates: RFC-IFC5-039 Foundational JSON Data Model
**Batch:** 2026-08-04-001
**Themes addressed:** 2, 7

---

## Change 1: Surface ProvenanceAuthority contradiction in Problem Statement
**Section:** [§1 Problem Statement](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md#1-problem-statement)
**Type:** Add known issue
**Rationale:** Theme 2 (Ev §B) identifies an internal contradiction: the architecture states conflicts are surfaced not resolved, but `ProvenanceAuthority` defines a precedence order. This must be surfaced as a known issue requiring a committee decision before the normative model can be finalised.

**Proposed addition:**
> **Known issue — conflict resolution policy:** The current model defines a `ProvenanceAuthority` enum with an implicit precedence order (survey > as-built > design-intent > inferred). This is in tension with the stated principle that IFCX surfaces conflicts rather than auto-resolving them. A conformance test suite cannot be built until this is resolved: "what is the height of wall W when two packages disagree?" must have one normatively defined answer. See RFC-041 for the open-world dimension of this question. A committee decision is required; options are described in the white paper.

---

## Change 2: Specify component `id` purpose and content-hash pattern
**Section:** [§ Component structure](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md)
**Type:** Specify behaviour
**Rationale:** Theme 7: every IFCY component carries an `id` field but the spec does not state what it is for beyond uniqueness. louistrue's prototype establishes a concrete use: a derived component carries a content hash of its source (JCS + SHA-256), allowing consumers to detect staleness without re-deriving. This gives `id` a role in the versioning and supersession chain.

**Proposed addition:**
> **Component `id` and content hashing:** Each component's `id` is a UUID that uniquely identifies this version of the component. To support staleness detection in derived or cached components, a component MAY carry a `sourceHash` field of the form `"sha256-<hex>"` containing the RFC 8785 JCS canonical hash of the source component from which this component was derived. A consumer resolves a component as `fresh` (hash matches current source), `stale` (hash does not match), or `unknown` (no hash present). This pattern is a candidate for normative status; see RFC-033 for the change and collaboration implications.
