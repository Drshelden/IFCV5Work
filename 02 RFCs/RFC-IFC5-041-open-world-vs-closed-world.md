<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-041](PENDING)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
PENDING

# RFC-IFC5-041: Open World vs. Closed World Assumptions

| Field | Value |
|---|---|
| **Decision ID** | IFC5-041 |
| **Status** | Idea |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | IFC5-001, IFC5-003, IFC5-006, IFC5-007, IFC5-039 |
| **Prototype Required** | No |
| **Logical position** | Tier 1 — prerequisite premise for IFC5-001 and all federation, identity, and extensibility RFCs |

---

## 1. Problem Statement

IFC4.x was built on an implicit **Closed World Assumption (CWA)**: if a fact is not present in the file, it is false or undefined; the file is the authoritative, complete description of the asset; and data exchange is a handover, not a continuous contribution. This assumption is never stated in the standard — it is embedded in the serialization format (STEP Physical File), the single-spatial-hierarchy model, and the schema's exhaustive prescriptive typing.

Both IFCX and IFC-ECS, the two leading IFC5 proposals, break from STEP but do not explicitly state which assumption they adopt. This creates a risk: downstream decisions on identity (IFC5-003), path addressing (IFC5-004), federation (IFC5-021), relationships (IFC5-008), versioning (IFC5-022), AI readability (IFC5-036), and web alignment (IFC5-035) may each make locally coherent choices that are collectively incompatible, because they implicitly assumed different worlds.

This RFC asks the committee to make the world assumption explicit before other Tier 1 and Tier 2 decisions are locked in.

---

## 2. Background

### 2.1 Closed World Assumption (CWA)

Under CWA, a database or model is treated as complete: what is not asserted is false or non-existent. IFC4.x embodies CWA through:
- The STEP file as a self-contained, authoritative snapshot
- Absence of a fact meaning absence of that property (not uncertainty)
- A single privileged spatial hierarchy (`IfcProject → IfcSite → IfcBuilding → IfcBuildingStorey`)
- Prescriptive schema: all valid concepts are enumerated centrally
- GUIDs that are locally unique but not globally resolvable

CWA is appropriate when: one party authors the dataset, the dataset is complete before handover, and the receiver is expected to trust it in full.

### 2.2 Open World Assumption (OWA)

Under OWA, any dataset is a partial description of a larger reality: what is not asserted is unknown (not false); new facts may be added by any party without invalidating prior assertions; and the description is always potentially incomplete.

OWA is the natural assumption for:
- Federated datasets authored by many parties
- Assets whose data grows continuously (design → construction → operations → demolition)
- Systems where "as-designed," "as-built," and "as-surveyed" coexist as equally valid but distinct views
- Linked data and semantic web systems (RDF, OWL, JSON-LD use OWA by default)

### 2.3 Why the choice matters for IFC5

The built environment is not, in practice, a closed world. An asset is described simultaneously by an architect, structural engineer, MEP contractor, fabricator, owner, facility manager, and regulator — each with partial, possibly contradictory, legitimately valid information. "Absent" in one party's export does not mean "false" in reality; it means "not in my scope."

If IFC5 retains CWA semantics, this is a legitimate choice — but it must be made consciously, with awareness of what it forecloses. If IFC5 adopts OWA semantics, it unlocks federation, continuous data, and AI-native reasoning, but requires globally resolvable identity, additive composition, and first-class provenance — which have direct implications for at least a dozen other RFCs.

### 2.4 The spectrum between CWA and OWA

CWA and OWA are not binary. The practical space includes:

- **Strong CWA**: the file is the truth; absence is falsity; no external references permitted.
- **Weak CWA (within-file)**: CWA holds within a single dataset, but datasets may be federated with explicit merge semantics.
- **Context-relative**: CWA within a named dataset/layer; OWA across dataset boundaries (the dataset is complete, the federation is not).
- **Weak OWA**: absent facts are unknown; new assertions may be added; provenance is tracked but not required.
- **Strong OWA**: no authoritative source; every fact is a attributed assertion; composition is always at read time; "the model" is a query result.

### 2.5 What other IFC5 proposals assume

The "Open World View of IFC Next" (Dennis Shelden, 2024) argues that the built environment is structurally open-world and that IFC's STEP foundation has been asked to serve an open-world domain with a closed-world tool. It identifies ten capabilities that follow from an OWA premise — federated authorship, provenance, progressive detail, multiple concurrent organizations of the same data, live continuous data, external references, gatekeeper-free extensibility, stable identity, federated query, and coexisting disagreement — and traces each to a specific limitation of IFC4.x's CWA design.

Neither IFCX nor IFC-ECS explicitly addresses this question, though both lean toward OWA features (component overlays, GUID-based identity, JSON references) without declaring OWA semantics.

---

## 3. Existing IFC4.x Convention

IFC4.x is implicitly **strong CWA**:
- A STEP Physical File is a complete, self-contained snapshot
- Absence of an attribute means it is unset or undefined (not unknown in an OWA sense)
- The single spatial hierarchy is privileged: an element has exactly one containment parent
- Schema is centrally governed: new concepts require a new schema release
- GUIDs are locally unique but not globally resolvable across organizations

IFC4.x's federation mechanism (`IfcRelReferencedInSpatialStructure`) is a CWA workaround, not an OWA feature: it allows elements from one file to appear in another, but both files are still self-contained CWA snapshots.

---

## 4. Proposed Approaches

### 4.1 Explicit Strong OWA

IFC5 adopts OWA as a normative premise. Every fact is a provenance-tagged assertion. Absent facts are explicitly unknown. The dataset is always a partial description. "The model" does not exist — only a view assembled from distributed assertions. This requires: globally resolvable identity (IFC5-003), no single spatial hierarchy (IFC5-007), additive-only composition (IFC5-010), first-class provenance (IFC5-022, IFC5-033), and a protocol layer (IFC5-035) that specifies how endpoints interoperate.

**Unlocks:** federation, continuous data, multi-party coexistence, AI-native reasoning, gatekeeper-free extensibility.  
**Requires:** significant departure from IFC4.x exchange patterns; increases coordination cost for simple single-author use cases.

### 4.2 Weak OWA (dataset-level CWA, federation-level OWA)

IFC5 uses CWA within a named dataset (a single file or endpoint's publication) but OWA at the federation boundary. A dataset is complete in its own scope; combining two datasets requires explicit merge/composition semantics with provenance. This is the approach used by systems like SPARQL federated queries and OGC building block registries.

**Unlocks:** most OWA benefits at federation scale while preserving simple-file semantics for single-author workflows.  
**Requires:** explicit dataset identity and boundaries; merge/composition semantics must be normatively specified.

### 4.3 CWA with Explicit OWA Extensions

IFC5 retains CWA as the default. OWA features (provenance, external references, overlay layers, unknown vs. absent) are available as opt-in extensions. A file without OWA extensions behaves like IFC4.x. A file with OWA extensions declares this and introduces additional required fields.

**Unlocks:** backward compatibility path; least disruption for existing toolchains.  
**Requires:** two-tier schema conformance; risk of OWA extensions being widely ignored, leaving the standard de facto CWA.

### 4.4 Context-Relative World Assumption

IFC5 specifies the world assumption as a per-context declaration. A dataset declares whether it is CWA or OWA. Consuming tools apply the declared semantics. Cross-context composition is defined for CWA-to-OWA and OWA-to-OWA combinations.

**Unlocks:** maximum flexibility for different use cases within one standard.  
**Requires:** complex conformance rules; risk of interoperability gaps at context boundaries.

### 4.5 Explicit Strong CWA (preserve IFC4.x semantics)

IFC5 retains CWA explicitly. Files are self-contained snapshots. Absent means false or unset. The standard's scope is the exchange of complete, authoritative datasets — not federation, continuous data, or distributed assertions. Use cases requiring OWA behavior are out of scope.

**Unlocks:** backward compatibility; clarity; simple toolchain expectations.  
**Forecloses:** federated authorship, live data integration, coexisting as-designed/as-built, AI reasoning at portfolio scale, gatekeeper-free extensibility.

---

## 5. Tradeoffs

| Dimension | Strong OWA | Weak OWA | CWA + Extensions | Context-relative | Strong CWA |
|---|---|---|---|---|---|
| IFC4.x backward compatibility | Low | Moderate | High | Moderate | High |
| Federation support | High | High | Partial | High | None |
| Single-author simplicity | Low | High | High | High | High |
| Provenance / audit trail | Required | Required | Optional | Configurable | None |
| Identity requirements | Global, resolvable URIs | Dataset-scoped + federation keys | GUIDs (current) | Declared per context | File-local GUIDs |
| AI / query scale | High | High | Low | High | Low |
| Protocol required | Yes | Yes | No | Yes | No |
| Schema centralization | Decentralized | Partially decentralized | Centralized | Configurable | Centralized |
| Spec complexity | High | Moderate | Moderate | High | Low |

---

## 6. RFC Interaction Map

The world assumption decision is a **cross-cutting premise** that constrains or is constrained by the following RFCs. The committee should review these interactions before finalizing any of them:

| RFC | Interaction |
|---|---|
| IFC5-001 (Strategic Mode) | OWA implies an extensible, decentralized standard; CWA implies a centrally governed one. The architectural mode choice is downstream of the world assumption. |
| IFC5-003 (Identity) | OWA requires globally resolvable, persistent, host-independent identity. CWA permits file-local GUIDs. The identity model must match the world assumption. |
| IFC5-004 (Path Model) | Paths work well for CWA (addresses within a tree). OWA requires URIs that resolve across organizations and time. The path model's load-bearing role changes significantly under OWA. |
| IFC5-006 (Serialization) | CWA → file-based exchange. OWA → streaming, delta, and API-first exchange patterns. The normative serialization format must be compatible with the world assumption. |
| IFC5-007 (Scene Graph vs. ECS) | The single privileged scene graph hierarchy is a CWA move. ECS's flat component model is more OWA-compatible. The architecture choice may be partially determined by the world assumption. |
| IFC5-008 (Relationships) | Under OWA, relationships are additive assertions with provenance. Under CWA, relationships are embedded structure. The modeling strategy differs significantly. |
| IFC5-010 (Composition / Instancing) | OWA implies composition at read/query time by the consumer. CWA implies composition at authoring time by the producer. |
| IFC5-021 (Federation) | Federation is a trivial concept under CWA (append two files). It is a foundational protocol concern under OWA (how do independently-hosted datasets interoperate). |
| IFC5-022 (Versioning) | OWA requires immutable, versioned assertions. CWA permits mutable state. Versioning semantics depend entirely on the world assumption. |
| IFC5-032 (Extensibility) | OWA enables gatekeeper-free extensibility (endpoints publish new vocabulary). CWA requires central schema governance for new concepts. |
| IFC5-033 (Change / Transactions) | Under OWA, change is additive (new assertion versions). Under CWA, change is destructive (file overwrite). The change model is a direct consequence of the world assumption. |
| IFC5-035 (Web / Linked-Data) | JSON-LD, RDF, and SPARQL are natively OWA. Aligning with web standards is significantly easier under OWA. |
| IFC5-036 (AI Readability) | AI reasoning over portfolio-scale data requires OWA properties: rich links, provenance, unknown vs. absent, federated query. OWA is the substrate AI tools need. |
| IFC5-039 (JSON Data Model) | The reference syntax (`{"ref": "..."}`) and whether references resolve globally or locally is determined by the world assumption. |

---

## 7. Recommendation

*To be filled in after committee discussion.*

---

## 8. Open Questions

**Q1.** Should IFC5 make an explicit normative declaration of its world assumption, or leave it implicit as IFC4.x did? What are the risks of leaving it implicit again?

**Q2.** Is the built environment better modeled as a closed world (one authoritative description) or an open world (many partial, simultaneous, valid descriptions)? Is this question different for different phases of the asset lifecycle (design vs. construction vs. operations)?

**Q3.** If the committee adopts OWA (fully or partially), which of the following are required as normative consequences: globally resolvable identity, provenance, immutable versioning, federated query semantics, decentralized extensibility? Which are optional extensions?

**Q4.** Is Approach 4.2 (weak OWA — dataset-level CWA, federation-level OWA) a stable middle ground, or does it collapse to either strong CWA or strong OWA in practice? Are there deployed systems that successfully occupy this position?

**Q5.** If IFC5 adopts any form of OWA, what is the minimum protocol specification required — beyond the schema — to make interoperability possible? Does this change the scope of what buildingSMART must standardize?

**Q6.** Are there IFC use cases (e.g., single-author design models, regulatory submissions, simple BIM for small buildings) that are better served by CWA semantics, and should IFC5 support both? If so, how is the world assumption declared at the dataset level?

**Q7.** How does the world assumption interact with legal and contractual frameworks? Signed, stamped deliverables are inherently CWA (a specific person asserting a specific, complete, authorized set of facts at a point in time). Can OWA coexist with certification and compliance workflows?

---

## 9. Prototype

- **Required:** No
- **Notes:** This is a definitional RFC — the decision is a philosophical/architectural premise, not an implementation question. However, the committee may find it useful to evaluate the Hello Wall reference examples (`03 Reference Examples/`) against OWA and CWA lenses: does the IFCX representation imply CWA? Does the IFC-ECS representation imply OWA? What would need to change in each to satisfy the opposite assumption?

---

## 10. Consequences

If **OWA** (Approach 4.1 or 4.2) is adopted, the following become requirements rather than options:
- IFC5-003 must define globally resolvable identity (URI-based or equivalent)
- IFC5-004 must reconsider whether path is identity or just addressing
- IFC5-006 must support streaming/delta exchange, not just whole-file
- IFC5-007 must avoid a single privileged hierarchy
- IFC5-008 must define relationships as additive assertions
- IFC5-021 (Federation) moves from a nice-to-have to a core normative topic
- IFC5-022, IFC5-033 must specify immutable + versioned state
- IFC5-032 must specify decentralized extensibility protocol
- IFC5-035 alignment with web standards becomes structurally natural

If **CWA** (Approach 4.5) is retained:
- IFC5-003 may continue with file-scoped GUIDs
- IFC5-004 path model remains valid as-is
- IFC5-021 is a secondary concern
- IFC5-022, IFC5-033 may use mutable semantics
- IFC5-035 web alignment is an integration concern, not a design premise

---

## 11. References

- "An Open World View of IFC Next" — Dennis Shelden (2024): https://docs.google.com/document/d/1UKmhPHgsVO-u2ZCzwJOKFxSF4lCHCWviY1R9HjCgZMQ
- W3C Open World Assumption (OWL / RDF): https://www.w3.org/TR/owl2-primer/#Open_World_Assumption
- Linked Data principles (Berners-Lee): https://www.w3.org/DesignIssues/LinkedData.html
- SPARQL Federated Query (SPARQL 1.1): https://www.w3.org/TR/sparql11-federated-query/
- OGC Building Blocks and registries: https://opengeospatial.github.io/ogc-na-tools/
- buildingSMART IFC5-development: https://github.com/buildingSMART/IFC5-development
- IFC-ECS: https://github.com/Drshelden/IFC-ECS
- Hello Wall reference examples: `03 Reference Examples/Hello-Wall/`

---

<!-- rfc-nav -->
PENDING
