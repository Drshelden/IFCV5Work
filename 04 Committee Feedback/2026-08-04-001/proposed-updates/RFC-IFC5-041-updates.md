# Proposed Updates: RFC-IFC5-041 Open World vs Closed World
**Batch:** 2026-08-04-001
**Themes addressed:** 2

---

## Change 1: Add conflict resolution policy to Open Questions
**Section:** [Open Questions](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md)
**Type:** Add open question
**Rationale:** The ProvenanceAuthority contradiction (Theme 2) is directly a question about whether the model is open-world (no resolution) or closed-world (one normative answer). This RFC is the right place to surface the policy decision.

**Proposed new open question:**
> **Q-NEW: Conflict resolution policy for plain queries.** The `ProvenanceAuthority` ordering in the current model constitutes an implicit closed-world resolution rule for the common case. The committee must decide: (a) **Normative default with override:** adopt the authority ordering as the normative default for a plain query (e.g., "what is the height of wall W?"), require implementations to declare when they apply a different policy, and require that all opinions and their provenance remain accessible regardless; (b) **Open-world only:** remove the authority ordering, make conflict resolution implementation-defined with mandatory disclosure, and accept that two conformant tools may return different answers to the same query; (c) **Deferred:** treat conflict resolution as out of scope for this version and document that plain queries are undefined when sources disagree. Option (b) risks making "what is the height of wall W?" non-testable in a conformance suite. Option (a) risks re-introducing a form of LIVRPS precedence. The committee decision must be documented here.
