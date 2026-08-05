# Proposed Updates: RFC-IFC5-014 Geometry Architecture
**Batch:** 2026-08-04-001
**Themes addressed:** 5, 6

---

## Change 1: Add hash-verifiable derivation row to §5 Tradeoffs table
**Section:** [§5 Tradeoffs Summary](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#5-tradeoffs-summary)
**Type:** Add row to table
**Rationale:** louistrue's prototype demonstrates that content hashing (JCS + SHA-256) makes disagreement between a derived mesh and its source machine-detectable without re-derivation. This is a capability that changes the risk profile of dual-representation (§4.3). It belongs in the tradeoff table as a cross-cutting factor, independent of which approach is chosen.

**Proposed new table row:**
> | Hash-verifiable derivation | sha256-hex on derived tier | Consumer detects fresh / stale / unknown without re-deriving | Requires canonical serialization (RFC-006 Q1 / RFC 8785 JCS) | Applicable to §4.2 and §4.3; resolves the "two sources of truth" risk |

---

## Change 2: Update §8 Q1 — mesh authority — with prototype evidence
**Section:** [§8 Open Questions Q1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#8-open-questions)
**Type:** Update question with evidence
**Rationale:** louistrue's Discussion #3 submission directly answers Q1 with a working prototype. Q1 should be updated to reference this evidence and note that it represents satisfiability, not conformance.

**Proposed update to Q1:**
> **Q1 — are meshes authoritative or derived?** *Evidence submitted (louistrue, Discussion #3):* In the geometry-tiers prototype, meshes are derived. Derivation is machine-checkable via a canonical content hash (RFC 8785 JCS + SHA-256) written on the derived component. A consumer resolves the cached mesh as fresh, stale, or unknown relative to its source without re-deriving. This demonstrates satisfiability on a non-upstream variant. The committee should decide whether to adopt content hashing as a normative requirement for derived geometry.

---

## Change 3: Update §8 Q2 — receiver tier distinction — with prototype evidence
**Section:** [§8 Open Questions Q2](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#8-open-questions)
**Type:** Update question with evidence
**Rationale:** louistrue's prototype answers Q2: tier separation is machine-readable and testable at the receiver level by constraining which tables a consumer may access, not by convention.

**Proposed update to Q2:**
> **Q2 — must receivers distinguish design-intent from visualization geometry?** *Evidence submitted (louistrue, Discussion #3):* In the prototype, tiers live in separate tables; a consumer declares which tiers it wants, and table access is logged so "a conformant mesh-only consumer reads no other tier's table" is observable and testable. The cost: a node's geometry requires the index and loader, losing schema-free parseability (RFC-036 §4.5). This tension cannot be designed away — it must be decided. The committee should choose between (a) requiring tier separation with the associated tooling cost, or (b) allowing co-location of tiers with derivation marked by convention only.

---

## Change 4: Correct §4.1 characterisation — mesh-first is lossy by construction
**Section:** [§4.1 Current IFCX approach](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#41-current-ifcx--fragmented-children-maps)
**Type:** Correct characterisation
**Rationale:** Both current Hello Wall examples carry mesh-only geometry. Since IFC4X geometry is predominantly procedural, this is lossy by construction (not merely by degree). The `customdata` field preserves bytes without meaning. This should be stated explicitly as a known limitation, not left implicit.

**Proposed addition to §4.1:**
> **Known limitation:** Both current reference examples use mesh-only geometry. IFC4X geometry is predominantly procedural (extrusions, boolean operations, sweeps); a mesh-only representation is therefore lossy by construction relative to the source, not merely by approximation. The `customdata` migration field preserves the original bytes but not their semantic meaning. This bears on RFC-018 Q4 (backward compatibility) and on the absorbed Topic 17 in RFC-007 (geometry authority). A procedural geometry representation (§4.2 or §4.3) is required for a non-lossy round-trip.
