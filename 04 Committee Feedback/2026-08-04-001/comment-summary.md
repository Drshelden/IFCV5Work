# Comment Summary — Batch 2026-08-04-001
**Sources:** 3 (github-issue-2, github-discussion-3, ev-email-2026-08-04)
**Generated:** 2026-08-05
**Method:** Manual synthesis (set ANTHROPIC_API_KEY to enable automated synthesis)

---

## Theme 1: Multi-hierarchy paths — missing example, not a design flaw
**Type:** Clarification
**Severity:** Minor
**Sources:** github-issue-2 (aothms), ev-email-2026-08-04 (Ev §A)
**RFC impact:** White paper §3.1.1, RFC-004

**Summary:** The white paper states that IFCX creates a closed-world assumption by giving each entity exactly one canonical position. aothms and Ev both argue this is incorrect — nothing in the data model prevents the same UUID from appearing in multiple simultaneous hierarchies. The path is an address, not an identity. The paper needs a corrected statement plus a Hello Wall variant demonstrating two concurrent trees pointing at the same window UUID.

**Action required:** Correct white paper §3.1.1; add multi-hierarchy Hello Wall test case to RFC-004 open questions.

---

## Theme 2: ProvenanceAuthority contradicts stated no-auto-resolution principle
**Type:** Bug
**Severity:** Critical
**Sources:** ev-email-2026-08-04 (Ev §B)
**RFC impact:** White paper (ProvenanceAuthority definition), RFC-039 (foundational JSON data model), RFC-041 (open world vs closed world)

**Summary:** The paper explicitly states that IFCX does not auto-resolve conflicts between competing data — "no system-imposed resolution destroys information." However, the schema's `ProvenanceAuthority` enum defines a strict precedence order (survey > as-built > design-intent > inferred) that does exactly that when packages are merged. This is an internal contradiction that must be resolved before a conformance suite can be built, since "what is the height of wall W?" requires a single testable answer from two conformant tools.

**Action required:** Decide group position — options: (a) retain provenance ordering as a normative default for plain queries, exposing the override policy explicitly; (b) remove the precedence order and require consumers to declare a conflict policy; (c) keep provenance metadata but make query behaviour implementation-defined with a required disclosure. Document decision in RFC-039 or RFC-041.

---

## Theme 3: IfcRel* objectified relationships — still genuinely unresolved
**Type:** Disagreement
**Severity:** Major
**Sources:** github-issue-2 (aothms §3), ev-email-2026-08-04 (Ev §C)
**RFC impact:** RFC-007 (scene graph vs ECS), RFC-008 (relationship modeling), RFC-016 (spatial structure)

**Summary:** aothms argues IfcRel* should not return — ECS components with identity and provenance already provide the modularity that objectified relationships gave in Express. The existing `systems` example shows complex many-to-many relationships are representable without them. Ev notes that others explicitly want IfcRel* for lossless coverage of all 30+ families, particularly many-to-many cases (material associations, groupings, interference checks). The dispute is real and requires a side-by-side comparison on 2-3 concrete cases before it can be closed.

**Action required:** Add side-by-side comparison of 2-3 concrete many-to-many IfcRel* families (e.g. IfcRelAssociatesMaterial, IfcRelInterferesElements, IfcRelReferencedInSpatialStructure) to RFC-008 open questions. Clarify RFC-007 background to explain why IfcRel* was deliberately removed.

---

## Theme 4: Transform composition bug — windows render incorrectly with non-identity wall transform
**Type:** Bug
**Severity:** Critical
**Sources:** ev-email-2026-08-04 (Ev §D)
**RFC impact:** White paper §3.3.3 (IFCY example), RFC-004 (path model), RFC-016 (spatial structure)

**Summary:** In the IFCY Hello Wall example, windows are repositioned as children of the storey (not the wall) because spatial position is "navigational." However, the windows retain their original wall-relative transform matrices. This only produces correct geometry because the wall happens to have an identity transform (no rotation, no offset). Any wall with a real transform (rotation, translation) would cause windows to render in the wrong location. No current rule specifies which graph is authoritative for composing transforms once position is decoupled from identity. This is a design gap, not just a documentation gap.

**Action required:** RFC-004 must specify how transform composition works when an entity appears in multiple spatial views. The Hello Wall example must be updated to use a non-identity wall transform to expose this correctly. Add to RFC-004 open questions.

---

## Theme 5: Hash-verifiable derived geometry — missing from RFC-014 tradeoff table
**Type:** New-Proposal / Evidence
**Severity:** Major
**Sources:** github-discussion-3 (louistrue)
**RFC impact:** RFC-014 (geometry architecture), RFC-006 (serialization), RFC-036 (AI/machine readability)

**Summary:** louistrue's working prototype demonstrates three-tier geometry (procedural → BRep → mesh) with content hashing (RFC 8785 JCS + SHA-256) on derived meshes. A consumer can resolve any derived mesh as fresh, stale, or unknown relative to its source without re-deriving geometry. This directly addresses RFC-014's risk statement for §4.3 (dual representation means two sources of truth) by making disagreement machine-detectable. The prototype answers RFC-014 Q1 (meshes are derived, marking is machine-checkable) and Q2 (tier separation is observable, not just promised). A row for "hash-verifiable derivation" is missing from RFC-014 §5's tradeoff table.

**Action required:** Add hash-verifiable derivation row to RFC-014 §5 tradeoff table. Update RFC-014 Q1 and Q2 to reflect the prototype as evidence. Document the tension between tier separation and RFC-036 §4.5 schema-free parseability as a known tradeoff requiring a committee decision.

---

## Theme 6: Current examples carry mesh-only geometry — lossy by construction
**Type:** Bug / Clarification
**Severity:** Major
**Sources:** github-discussion-3 (louistrue)
**RFC impact:** RFC-014 §4.1, RFC-018 (backward compatibility), RFC-007 Topic 17

**Summary:** Both current Hello Wall examples carry mesh-only geometry. Since IFC4X geometry is predominantly procedural, mesh-first is lossy by construction — the `customdata` migration aid preserves bytes without meaning. This bears on RFC-018 Q4 (backward compatibility for geometry) and RFC-007's absorbed Topic 17 ("which information is authoritative when semantic and mesh geometry disagree"). The prototype's tier ordering (highest present = authoritative) is one concrete answer.

**Action required:** Update RFC-014 §4.1 to acknowledge that mesh-first is lossy relative to IFC4X procedural geometry. Cross-reference RFC-018 Q4. Add tier-authority rule to RFC-007 Topic 17 discussion.

---

## Theme 7: Component id unused — no supersession mechanism
**Type:** New-Proposal
**Severity:** Minor
**Sources:** ev-email-2026-08-04 (Ev §E), github-discussion-3 (louistrue — content hash prototype)
**RFC impact:** RFC-039 (foundational JSON data model), RFC-033 (change and collaboration)

**Summary:** Every IFCY component carries an `id` field, but nothing in the current spec references component ids to mark one component as superseding another. louistrue's content hash (JCS + SHA-256 on the component's canonical form) provides a mechanism: a derived or cached component can report whether it is fresh, stale, or unknown relative to its source, and gives the unused `id` a functional role in a versioning/provenance chain.

**Action required:** RFC-039 should specify the purpose of component `id` beyond uniqueness. RFC-033 should document the content-hash pattern as the normative approach for component supersession and staleness detection.

---

## Theme 8: USD composition engine burden on consumers
**Type:** Clarification
**Severity:** Minor
**Sources:** github-issue-2 (aothms §4)
**RFC impact:** White paper §4 (USD alignment), RFC-015 (OpenUSD alignment)

**Summary:** aothms argues the white paper's concern that consumers must implement a full USD composition engine is overstated — IFC4 already has analogous (if implicit and idiosyncratic) inheritance logic between TypeObject, PropertySets, and occurrences. IFCX makes this explicit and first-principled; the burden is not new, only more visible. The white paper should correct or nuance this characterisation.

**Action required:** Revise white paper §4 to acknowledge that IFC4 already required similar inheritance resolution, and that IFCX's contribution is making this logic explicit and formally specified rather than introducing a new burden.

---

## Summary of actions
| # | Action | Priority | Owner | RFC |
|---|--------|----------|-------|-----|
| 1 | Correct white paper closed-world statement; note multi-hierarchy is supported | Minor | Editorial | White paper, RFC-004 |
| 2 | Decide group position on ProvenanceAuthority precedence | **Critical** | Committee | RFC-039, RFC-041 |
| 3 | Side-by-side comparison of 2-3 IfcRel* many-to-many cases | Major | TBD | RFC-007, RFC-008 |
| 4 | Specify transform composition rule for multi-view entities; update Hello Wall example | **Critical** | Editorial + example | RFC-004, RFC-016 |
| 5 | Add hash-verifiable derivation row to RFC-014 §5; update Q1/Q2; document RFC-036 tension | Major | Editorial | RFC-014, RFC-006 |
| 6 | Update RFC-014 §4.1 re mesh-first lossiness; cross-ref RFC-018 Q4 | Major | Editorial | RFC-014, RFC-018 |
| 7 | Specify component `id` purpose; document content-hash supersession pattern | Minor | Editorial | RFC-039, RFC-033 |
| 8 | Revise white paper §4 re USD composition engine burden | Minor | Editorial | White paper, RFC-015 |
