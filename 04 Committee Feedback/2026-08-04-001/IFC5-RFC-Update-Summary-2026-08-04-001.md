# IFC5 RFC Update Summary — 2026-08-04-001
**Generated:** 2026-08-05 00:58 UTC  
**Updated:** 2026-08-04 (actions implemented)  
**Repository:** [Drshelden/IFCV5Work](https://github.com/Drshelden/IFCV5Work)
**Next review cycle:** 2026-08-19
**Batch directory:** `04 Committee Feedback/2026-08-04-001/`

---

## 1. Sources Reviewed

| # | Source | Author | Date | Type |
|---|--------|--------|------|------|
| 1 | [IFC5-Architecture-White-Paper.md comments](https://github.com/Drshelden/IFCV5Work/issues/2) | aothms | 2026-08-03 | github_issue |
| 2 | [[RFC Feedback] IFC5-014 — Evidence: working dual-representation prototype, answers to Q1 and Q2](https://github.com/Drshelden/IFCV5Work/discussions/3) | louistrue | 2026-08-03 | github_discussion |
| 3 | [Committee discussion summary email](sources/ev-email-2026-08-04.json) | Ev | 2026-08-04 | local_file |

---

## 2. Validation Results

**8 PASS / 0 WARN / 0 FAIL**  →  [Full validation report](validation-report.md)

---

## 3. Comment Themes

## Theme 1: Multi-hierarchy paths — missing example, not a design flaw
**Type:** Clarification
**Severity:** Minor
**Sources:** github-issue-2 (aothms), ev-email-2026-08-04 (Ev §A)
**RFC impact:** White paper §2.2.1, RFC-004

**Summary:** The white paper stated that IFCX creates a closed-world assumption by giving each entity exactly one canonical position. aothms and Ev both argue this is incorrect — nothing in the data model prevents the same UUID from appearing in multiple simultaneous hierarchies. The path is an address, not an identity. The paper needs a corrected statement plus a Hello Wall variant demonstrating two concurrent trees pointing at the same window UUID.

**Actions:**
- ✅ **Implemented** — White paper §2.2.1 corrected: now states paths are navigational aliases; the same UUID may appear in multiple simultaneous hierarchies. [→ §2.2.1](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#221-path-conflating-identity-with-position)
- ✅ **Implemented** — RFC-004 §4.1 now notes that a multi-hierarchy Hello Wall test case is planned and is the missing verification. [→ RFC-004 §4.1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md#41-current-ifcx--fragmented-children-maps)

---

## Theme 2: ProvenanceAuthority contradicts stated no-auto-resolution principle
**Type:** Bug
**Severity:** Critical
**Sources:** ev-email-2026-08-04 (Ev §B)
**RFC impact:** White paper (ProvenanceAuthority definition), RFC-039, RFC-041

**Summary:** The paper states that the architecture does not auto-resolve conflicts. However, the `ProvenanceAuthority` enum defines a strict precedence order (survey > as-built > design-intent > inferred) that does exactly that. This is an internal contradiction that must be resolved before a conformance suite can be built.

**Actions:**
- ✅ **Implemented** — White paper §3.2 now notes the tension and presents the three options for committee decision. [→ White paper §3.2](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#32-layer-15-the-component-primitive)
- ✅ **Implemented** — RFC-039 §1 Problem Statement now surfaces the contradiction as a known issue requiring committee decision. [→ RFC-039 §1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md#1-problem-statement)
- ✅ **Implemented** — RFC-041 Q8 (new) documents all three resolution options with explicit tradeoffs. [→ RFC-041 §6 Q8](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md#6-open-questions)
- ⚠️ **Decision required** — Committee must choose option (a), (b), or (c) at RFC-041 Q8 and record the decision in both RFC-039 and RFC-041.

---

## Theme 3: IfcRel* objectified relationships — still genuinely unresolved
**Type:** Disagreement
**Severity:** Major
**Sources:** github-issue-2 (aothms §3), ev-email-2026-08-04 (Ev §C)
**RFC impact:** RFC-007, RFC-008, RFC-016

**Summary:** aothms argues IfcRel* should not return — ECS components with identity and provenance already provide the modularity that objectified relationships gave in Express. Ev notes that others explicitly want IfcRel* for lossless coverage of all 30+ families, particularly many-to-many cases. The dispute requires a side-by-side comparison on 2-3 concrete cases.

**Actions:**
- ✅ **Implemented** — RFC-007 §2 Background now includes a paragraph explaining why IfcRel* was deliberately removed from IFCX, with reference to RFC-008 for the open comparison. [→ RFC-007 §2](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md#2-background)
- ✅ **Implemented** — RFC-008 Q5 (new) specifies the exact side-by-side comparison required: IfcRelAssociatesMaterial, IfcRelInterferesElements, IfcRelReferencedInSpatialStructure in both ECS and IfcRel* style, with data structure, query pattern, and provenance attachment point. [→ RFC-008 §7 Q5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md#7-open-questions)
- ⚠️ **Decision required** — The comparison specified in RFC-008 Q5 must be produced (by a working group member or draft author) before this can be closed. The decision cannot be made without the comparison.

---

## Theme 4: Transform composition bug — windows render incorrectly with non-identity wall transform
**Type:** Bug
**Severity:** Critical
**Sources:** ev-email-2026-08-04 (Ev §D)
**RFC impact:** White paper §3.4.1, RFC-004, RFC-016

**Summary:** In the IFCY Hello Wall example, windows retain wall-relative transform matrices after being repositioned under the storey. This only works because the wall has an identity transform. Any wall with a non-identity transform would cause windows to render in the wrong location. No current rule specifies which graph is authoritative for composing transforms.

**Actions:**
- ✅ **Implemented** — White paper §3.4.1 now includes a "Known limitation" note explaining the transform composition gap and that any spatial-view proposal must specify which graph governs transforms. [→ White paper §3.4.1](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#341-paths-as-named-views-not-identity)
- ✅ **Implemented** — RFC-004 Q5 (new) documents three candidate policies for transform composition with the requirement for a non-identity-wall Hello Wall test case to validate any answer. [→ RFC-004 §9 Q5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md#9-open-questions)
- ⚠️ **Decision required** — Committee must choose a transform composition policy (RFC-004 Q5 options a/b/c). A non-identity Hello Wall test case is required to validate the chosen approach.

---

## Theme 5: Hash-verifiable derived geometry — missing from RFC-014 tradeoff table
**Type:** New-Proposal / Evidence
**Severity:** Major
**Sources:** github-discussion-3 (louistrue)
**RFC impact:** RFC-014, RFC-006, RFC-036

**Summary:** louistrue's working prototype demonstrates three-tier geometry (procedural → BRep → mesh) with content hashing (RFC 8785 JCS + SHA-256) on derived meshes. A consumer can resolve any derived mesh as fresh, stale, or unknown relative to its source without re-deriving geometry. This directly addresses RFC-014's dual-representation risk.

**Actions:**
- ✅ **Implemented** — RFC-014 §5 tradeoffs table now includes a "Hash-verifiable derivation" row covering mechanism, consumer benefit, cost, and applicability. [→ RFC-014 §5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#5-tradeoffs)
- ✅ **Implemented** — RFC-014 Q1 updated: now references the louistrue prototype as evidence, explains the content-hash mechanism, and asks the committee to decide on normative status. [→ RFC-014 §7 Q1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#7-open-questions)
- ✅ **Implemented** — RFC-014 Q2 updated: references prototype evidence on tier separation; explicitly frames the choice between (a) required tier separation with tooling cost vs. (b) co-location with convention-only derivation marking. [→ RFC-014 §7 Q2](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#7-open-questions)
- ⚠️ **Decision required** — Committee must decide (RFC-014 Q1) whether content hashing is normative for derived geometry, and (Q2) whether tier separation is required.

---

## Theme 6: Current examples carry mesh-only geometry — lossy by construction
**Type:** Bug / Clarification
**Severity:** Major
**Sources:** github-discussion-3 (louistrue)
**RFC impact:** RFC-014 §4.1, RFC-018, RFC-007 Topic 17

**Summary:** Both current Hello Wall examples carry mesh-only geometry. Since IFC4X geometry is predominantly procedural, mesh-first is lossy by construction — the `customdata` migration aid preserves bytes without semantic meaning.

**Actions:**
- ✅ **Implemented** — RFC-014 §4.1 now includes a "Known limitation" note stating mesh-first is lossy by construction relative to IFC4X procedural geometry, with cross-reference to RFC-018 Q4 and RFC-007 Topic 17. [→ RFC-014 §4.1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#41-tessellation-only-mesh-first)
- ✅ **Implemented** — RFC-007 Topic 17 in §11 now documents the louistrue tier-authority rule as a candidate resolution (highest tier present = authoritative; lower tiers are derived caches). [→ RFC-007 §11 Topic 17](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md#11-absorbed-topic-architectural-ambiguities-topic-58)

---

## Theme 7: Component id unused — no supersession mechanism
**Type:** New-Proposal
**Severity:** Minor
**Sources:** ev-email-2026-08-04 (Ev §E), github-discussion-3 (louistrue)
**RFC impact:** RFC-039, RFC-033

**Summary:** Every IFCY component carries an `id` field, but the spec does not state what it is for beyond uniqueness. louistrue's content hash pattern gives `id` a functional role in a versioning/provenance chain.

**Actions:**
- ✅ **Implemented** — RFC-039 §6 Component Primitive now specifies that a component MAY carry a `sourceHash` field (`sha256-<hex>`) enabling consumer-side freshness detection (fresh / stale / unknown). [→ RFC-039 §6](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md#6-the-component-primitive)
- ✅ **Implemented** — RFC-033 §4.5 (new approach) documents the full content-hash supersession pattern: `supersedesId` + `sourceHash`, consumer resolution states, and OWA compatibility. [→ RFC-033 §4.5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md#4-proposed-approaches)

---

## Theme 8: USD composition engine burden on consumers
**Type:** Clarification
**Severity:** Minor
**Sources:** github-issue-2 (aothms §4)
**RFC impact:** White paper §2.2.3

**Summary:** aothms argues the white paper overstates the burden of USD composition — IFC4 already required similar inheritance resolution between TypeObject, PropertySets, and occurrences.

**Actions:**
- ✅ **Implemented** — White paper §2.2.3 now includes a note acknowledging that IFC4 already required similar logic (TypeObject → PropertySet → occurrence inheritance) and that IFCX replaces an implicit mechanism with an explicit, formally-specified one. [→ White paper §2.2.3](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#223-composition-without-resolution)

---

## 4. Action Items — Status

| # | Action | Status | Link |
|---|--------|--------|------|
| 1 | Correct white paper closed-world statement | ✅ Done | [White paper §2.2.1](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#221-path-conflating-identity-with-position) · [RFC-004 §4.1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md#41-current-ifcx--fragmented-children-maps) |
| 2 | Decide ProvenanceAuthority precedence policy | ⚠️ Decision required | [White paper §3.2](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#32-layer-15-the-component-primitive) · [RFC-039 §1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md#1-problem-statement) · [RFC-041 Q8](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md#6-open-questions) |
| 3 | Produce side-by-side IfcRel* vs ECS comparison for 3 cases | ⚠️ Decision required | [RFC-008 Q5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md#7-open-questions) · [RFC-007 §2](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md#2-background) |
| 4 | Specify transform composition rule; update Hello Wall example | ⚠️ Decision required | [RFC-004 Q5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md#9-open-questions) · [White paper §3.4.1](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#341-paths-as-named-views-not-identity) |
| 5 | Add hash-verifiable derivation to RFC-014 §5; update Q1/Q2 | ✅ Done | [RFC-014 §5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#5-tradeoffs) · [RFC-014 Q1/Q2](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#7-open-questions) |
| 6 | Note mesh-first lossiness in RFC-014 §4.1; add Topic 17 resolution to RFC-007 | ✅ Done | [RFC-014 §4.1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#41-tessellation-only-mesh-first) · [RFC-007 Topic 17](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md#11-absorbed-topic-architectural-ambiguities-topic-58) |
| 7 | Specify component `id` purpose; document content-hash supersession | ✅ Done | [RFC-039 §6](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md#6-the-component-primitive) · [RFC-033 §4.5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md#4-proposed-approaches) |
| 8 | Revise white paper re USD composition engine burden | ✅ Done | [White paper §2.2.3](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#223-composition-without-resolution) |

**5 implemented · 3 require committee decision**

---

## 5. RFC Impact Map

| Document | Section | Change Type | Theme | Status | Link |
|----------|---------|-------------|-------|--------|------|
| White paper | §2.2.1 Paths | Corrected | 1 — Multi-hierarchy | ✅ Done | [§2.2.1](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#221-path-conflating-identity-with-position) |
| White paper | §2.2.3 Composition | Revised | 8 — USD burden | ✅ Done | [§2.2.3](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#223-composition-without-resolution) |
| White paper | §3.2 ProvenanceAuthority | Decision note added | 2 — Provenance contradiction | ⚠️ Decision | [§3.2](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#32-layer-15-the-component-primitive) |
| White paper | §3.3.3 Relationships | Rationale added | 3 — IfcRel* | ✅ Done | [§3.3.3](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#333-relationships-as-components) |
| White paper | §3.4.1 Paths as Named Views | Known limitation added | 4 — Transform bug | ⚠️ Decision | [§3.4.1](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#341-paths-as-named-views-not-identity) |
| RFC-004 | §4.1 Current IFCX | Test case note added | 1 — Multi-hierarchy | ✅ Done | [§4.1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md#41-current-ifcx--fragmented-children-maps) |
| RFC-004 | §9 Q5 (new) | Open question added | 4 — Transform bug | ⚠️ Decision | [§9](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md#9-open-questions) |
| RFC-007 | §2 Background | IfcRel* rationale added | 3 — IfcRel* | ✅ Done | [§2](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md#2-background) |
| RFC-007 | §11 Topic 17 | Candidate resolution added | 6 — Mesh-first lossy | ✅ Done | [§11](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md#11-absorbed-topic-architectural-ambiguities-topic-58) |
| RFC-008 | §7 Q5 (new) | Comparison required | 3 — IfcRel* | ⚠️ Decision | [§7](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md#7-open-questions) |
| RFC-014 | §4.1 | Known limitation added | 6 — Mesh-first lossy | ✅ Done | [§4.1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#41-tessellation-only-mesh-first) |
| RFC-014 | §5 Tradeoffs | Hash-verifiable row added | 5 — Content hashing | ✅ Done | [§5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#5-tradeoffs) |
| RFC-014 | §7 Q1 | Updated with evidence | 5 — Content hashing | ⚠️ Decision | [§7](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#7-open-questions) |
| RFC-014 | §7 Q2 | Updated with evidence | 5 — Content hashing | ⚠️ Decision | [§7](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-014-geometry-architecture.md#7-open-questions) |
| RFC-033 | §4.5 (new approach) | Content-hash supersession added | 7 — Component id/versioning | ✅ Done | [§4](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-033-change-collaboration.md#4-proposed-approaches) |
| RFC-039 | §1 Problem Statement | Known issue added | 2 — Provenance contradiction | ⚠️ Decision | [§1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md#1-problem-statement) |
| RFC-039 | §6 Component Primitive | sourceHash pattern added | 7 — Component id/versioning | ✅ Done | [§6](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md#6-the-component-primitive) |
| RFC-041 | §6 Q8 (new) | Conflict resolution options | 2 — Provenance contradiction | ⚠️ Decision | [§6](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md#6-open-questions) |

---

## 6. Proposed Document Changes

| Document | # Changes | Proposed Updates |
|----------|-----------|-----------------|
| RFC-IFC5-004 | 2 | [View](proposed-updates/RFC-IFC5-004-updates.md) |
| RFC-IFC5-007 | 2 | [View](proposed-updates/RFC-IFC5-007-updates.md) |
| RFC-IFC5-008 | 1 | [View](proposed-updates/RFC-IFC5-008-updates.md) |
| RFC-IFC5-014 | 4 | [View](proposed-updates/RFC-IFC5-014-updates.md) |
| RFC-IFC5-033 | 1 | [View](proposed-updates/RFC-IFC5-033-updates.md) |
| RFC-IFC5-039 | 2 | [View](proposed-updates/RFC-IFC5-039-updates.md) |
| RFC-IFC5-041 | 1 | [View](proposed-updates/RFC-IFC5-041-updates.md) |
| white-paper | 5 | [View](proposed-updates/white-paper-updates.md) |

---

## 7. Decisions Required from Committee

Three items remain open and require committee decisions before they can be implemented:

### ⚠️ Decision A — ProvenanceAuthority conflict resolution policy
**RFC:** [RFC-041 Q8](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md#6-open-questions) · [RFC-039 §1](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md#1-problem-statement) · [White paper §3.2](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#32-layer-15-the-component-primitive)

Choose one of:
- **(a)** Retain authority ordering as normative default for plain queries; require implementations to declare alternative policies explicitly
- **(b)** Remove precedence order; make conflict resolution implementation-defined with mandatory disclosure
- **(c)** Treat conflict resolution as out of scope for this version; document that plain queries are undefined when sources disagree

### ⚠️ Decision B — Transform composition policy for multi-view entities
**RFC:** [RFC-004 Q5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md#9-open-questions) · [White paper §3.4.1](https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5-Architecture-White-Paper.md#341-paths-as-named-views-not-identity)

Choose one of:
- **(a)** SpatialView graph always governs transform composition; authored transforms must be relative to view-parent
- **(b)** Transforms are always relative to physical parent; SpatialView is purely navigational
- **(c)** Each SpatialView declares a `transformSpace` policy

*Requires: a Hello Wall variant with non-identity wall transform to verify any answer.*

### ⚠️ Decision C — IfcRel\* vs. ECS typed components for many-to-many relationships
**RFC:** [RFC-008 Q5](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md#7-open-questions) · [RFC-007 §2](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md#2-background)

*Requires: a working group member to produce the side-by-side comparison specified in RFC-008 Q5 (IfcRelAssociatesMaterial, IfcRelInterferesElements, IfcRelReferencedInSpatialStructure) before a decision can be made.*

---

## 8. Next Steps

- Commit and push these RFC/document updates to GitHub
- Bring decisions A, B, C to committee at 2026-08-19 meeting
- Assign RFC-008 Q5 comparison task to a working group member
- Build Hello Wall non-identity-wall test case (needed for decision B)
- Next feedback cycle: **2026-08-19**
