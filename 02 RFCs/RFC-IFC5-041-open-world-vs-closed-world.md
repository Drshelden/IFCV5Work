<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-041](https://docs.google.com/forms/d/e/1FAIpQLSeWPRQYdUggtVVpjcKQvFOlwpG0Kwat3ubKXfyHH-_o_HKLUg/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md) · [📝 Google Doc](https://docs.google.com/document/d/1cbj9Jo44HECNdMTVhn_md1Q_RLjYnDzDt5EYrDidNic/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-041) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-041+%E2%80%94+&labels=IFC5-041&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeWPRQYdUggtVVpjcKQvFOlwpG0Kwat3ubKXfyHH-_o_HKLUg/viewform)


# RFC-IFC5-041: Open World vs. Closed World Assumptions

| Field | Value |
|---|---|
| **Decision ID** | IFC5-041 |
| **Status** | Idea |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | IFC5-001, IFC5-003, IFC5-004, IFC5-006, IFC5-007, IFC5-021, IFC5-039 |
| **Prototype Required** | No |
| **Logical position** | Tier 1 — prerequisite premise; resolves before IFC5-001 through IFC5-007 are finalized |

---

## 1. Problem Statement

IFC4.x was built on an implicit **Closed World Assumption (CWA)**: absent facts are false; the file is the complete, authoritative description of the asset; exchange is a finished-model handover. This was never stated — it is embedded in STEP's self-contained file format, a single privileged spatial hierarchy, and a centrally-governed prescriptive schema. The result is that many persistent IFC problems — lossy round-trips, models overwriting each other, no provenance, stale external data, schema release lag — look less like implementation bugs and more like what happens when a closed-world foundation is asked to serve an open-world domain.

Both current IFC5 proposals adopt JSON and move toward OWA features (GUID-based identity, component overlays, JSON references) without declaring OWA semantics. If the committee does not make the world assumption explicit, each downstream RFC will make its own implicit choice, and the decisions will be locally coherent but collectively incompatible.

The general direction of IFC5 — distributed, federated, AI-readable, extensible without a central gatekeeper — implies an **Open World Assumption**. The purpose of this RFC is not to re-litigate that direction but to work through exactly what it requires in concrete architectural and syntactic terms, and where the two current proposals (IFCX and IFC-ECS) already satisfy or fall short of those requirements.

---

## 2. The World Assumption Spectrum (Summary)

OWA and CWA are endpoints of a spectrum. The realistic IFC5 positions are:

| Position | What it means | Consequence |
|---|---|---|
| **Strong CWA** | File = truth; absence = false; one authoritative model | Preserves IFC4.x exchange patterns; forecloses federation, provenance, AI at scale |
| **Weak CWA** | CWA within a file; explicit federation at file boundaries | Lowest disruption; federation is bolt-on, not native |
| **Weak OWA** (recommended floor) | Absent facts unknown; assertions additive; provenance tracked | Enables multi-party authorship, federation, AI; requires identity and provenance fields |
| **Strong OWA** | No authoritative source; "the model" is a query result assembled at read time; all facts attributed | Maximum distribution; requires full protocol layer, not just schema |

The committee should decide *where on this spectrum* to commit. This RFC argues the minimum viable commitment is **weak OWA**: absent does not mean false; new assertions may be added without invalidating prior ones; and provenance is a first-class field. Strong OWA (fully protocol-based, no file exchange) is a further step that may not be necessary for IFC5 but should not be foreclosed by design decisions made now.

---

## 3. The Ten OWA Capabilities and What Each Requires

The "Open World View of IFC Next" (Schleussner, 2026) identifies ten capabilities that follow from an OWA premise. This section maps each to the specific architectural or syntactic requirement it creates in IFC5, and assesses where IFCX and IFC-ECS currently stand.

### 3.1 Federated Authorship
*Many parties contribute to one description without overwriting each other.*

**Required:** Assertions must be additive and attributable. A new component from a contractor must not replace an architect's component — both coexist until a consumer applies a resolution policy.

**IFCX today:** The scene graph is a tree with one authoritative path per entity. A second party writing to `/Building/Wall001/Geometry` replaces the first party's value. There is no native overlay or delta mechanism. **Not OWA-compatible as-is.**

**How USD differs:** USD addresses this via its **layer stack** — multiple USD files can be stacked as sublayers, each contributing "opinions" that compose in LIVRPS precedence order (Local → Inherits → Variant Sets → References → Payload → Sublayers). IFCX borrows USD's `inherits` arc but does not adopt the full composition model. An IFCX file that implemented USD sublayers would gain multi-party authorship; however, USD's layer composition always resolves to a single value (highest-strength opinion wins) — it is multi-source but not OWA. To achieve true federated authorship, IFCX would need to go beyond USD's model to preserve competing opinions rather than resolve them.

**IFC-ECS today:** Multiple components of the same `componentType` on the same `entityGuid` can coexist in the flat array. Nothing in the schema prevents duplicate components. This is closer to OWA-compatible but lacks a defined resolution semantics. **Partially compatible; needs provenance + merge rules.**

**What's needed:** Either IFCX gains a layer/overlay mechanism (separate from the main scene graph tree), or IFC-ECS defines explicit rules for how multiple components of the same type on the same entity are handled. Both need provenance fields.

### 3.2 Provenance
*Know who asserted each fact, when, and with what authority.*

**Required:** Every assertion (component, attribute value, relationship) must carry — at minimum — an asserting party, an assertion timestamp, and an authority level. Without provenance, an AI's "best-guess classification" silently overwrites a licensed engineer's stamped value.

**IFCX today:** No provenance fields in the component structure. The `attributes` dict carries values with no author or time. **Not present.**

**IFC-ECS today:** No provenance fields. `componentGuid` provides identity but not attribution. **Not present.**

**Minimum required addition (both proposals):**
```json
{
  "assertedBy": "urn:org:arup:user:jsmith",
  "assertedAt": "2025-04-01T09:00:00Z",
  "authority": "design-intent"   // or "as-built", "survey", "inferred", "ai-generated"
}
```
This could be a top-level field on the component, a wrapper, or a separate assertion record. The structure is open; the requirement is not.

### 3.3 Progressive Detail (Unknown ≠ Absent)
*"Not known yet" must be expressible and distinguishable from "false" or "not present."*

**Required:** A tri-state system: *value present*, *explicitly unknown*, *field absent*. Under CWA, absent and unknown are the same. Under OWA they are different: a structural engineer may know a wall is load-bearing but not yet know its fire rating. The fire rating is unknown, not false.

**IFCX today:** Absent attribute = not set. No way to express "unknown." **Not present.**

**IFC-ECS today:** Same issue. Absent attribute = not set. **Not present.**

**Minimum required addition:** A sentinel value or wrapper, such as:
```json
{ "FireRating": { "status": "unknown", "reason": "pending review" } }
```
or a convention like `null` meaning "explicitly unknown" vs. key absence meaning "out of scope." This needs to be normatively defined — ad hoc conventions will diverge across tools.

### 3.4 Multiple Simultaneous Organizations of the Same Data
*The same components seen by storey, by system, by zone, by construction sequence — without one being "real."*

**Required:** No single privileged hierarchy. An entity must be addressable through multiple organizational lenses simultaneously.

**IFCX today:** The scene graph is a rooted tree. Each entity has exactly one canonical path. `/Building/Wall001` is the wall's address; it cannot simultaneously be `/System/HVAC/Wall001`. Alternative views exist only as secondary relationships hanging off the primary tree. **CWA structure — single privileged hierarchy.**

**How USD differs:** USD partially addresses this via **variant sets** — a prim can carry multiple named variants (e.g., `{view=spatial}`, `{view=system}`) that swap out entire subtrees. This allows one USD file to represent multiple organizational perspectives. However, USD still resolves to one active variant at a time; both organizations' views cannot be simultaneously first-class. IFCX does not implement USD variant sets. An IFCX that adopted variant sets would improve on today's position but would still not match the OWA capability that IFC-ECS's flat model provides natively.

**IFC-ECS today:** The flat component array has no hierarchy at all. An entity's components are retrieved by `entityGuid`; organizing those into views is a consumer-side operation. Multiple independent grouping components (spatial, system, zone, phase) can coexist as separate components on the same entity. **OWA-compatible; multiple views are naturally first-class.**

**What's needed for IFCX:** Either (a) decouple entity identity from path location (path becomes one view, not the canonical address), or (b) add a first-class "view" or "layer" mechanism that can hold alternative organizational hierarchies. This is architecturally significant and has direct implications for IFC5-004 (Path Model).

### 3.5 Live Continuous Data
*Bind to operations/IoT rather than freeze everything at handover.*

**Required:** The standard must not assume data is frozen at export. Live sensor readings, occupancy data, or maintenance records should be representable as additional assertions on existing entities, without requiring a full re-export.

**IFCX today:** A file is a snapshot. Incremental updates are not native. **File-based, snapshot-oriented.**

**IFC-ECS today:** Same. The array is a flat snapshot. **File-based, snapshot-oriented.**

**What's needed:** At minimum, an additive assertion format (a "patch" or "delta" file that adds components to existing entities without re-serializing the whole model). At maximum, a streaming API. This is a serialization concern (IFC5-006) as much as a schema concern.

### 3.6 Reference to Live External Sources
*Point at manufacturer catalogues, EPDs, and code databases instead of copying stale snapshots inward.*

**Required:** A normative mechanism for external references that is not a file-local pointer. References must be resolvable, versionable, and have an explicit staleness/caching contract.

**IFCX today:** Can reference external paths, but the path model is file-relative. No staleness contract. **Partial; needs URI-based resolution and caching semantics.**

**IFC-ECS today:** Can embed external IDs in attributes but no normative reference mechanism. **Not present.**

**Minimum required:** A typed reference object:
```json
{ "ref": "https://www.bsdd.buildingsmart.org/api/class/IfcWall", "fetchedAt": "2025-01-01", "version": "4.3" }
```
The reference syntax (`{"ref": "..."}`) discussed in IFC5-039 must support URI-based external references, not just local GUIDs.

### 3.7 Extensibility Without a Central Gatekeeper
*New domains get first-class concepts now, without a schema release cycle.*

**Required:** A mechanism for any party to publish new component types, attribute names, or relationship types under their own namespace, which other tools can discover and use without waiting for a buildingSMART schema update.

**IFCX today:** `componentType` and attribute names are used freely, but there is no normative namespace mechanism or discovery protocol. Custom types exist in practice but are informal. **Partially present; needs normative namespace declaration (IFC5-005).**

**IFC-ECS today:** Same. `componentType` is a string; custom types are possible but informal. **Same position as IFCX.**

**What's needed:** A normative namespace declaration (IFC5-005) plus a minimal discovery mechanism — at minimum, a JSON-LD `@context`-style mapping so that `"myOrg:ThermalZone"` resolves to a published schema. This connects to IFC5-035 (Web/Linked Data).

### 3.8 Stable Identity Across Orgs and Decades
*The same physical thing reliably referenced by everyone over time.*

**Required:** Identifiers must be globally unique, not just locally unique within a file; persistent across organizational boundaries; and resolvable — meaning a tool can look up what the identifier refers to even if it has never seen the file that defined it.

**IFCX today:** Path-based identity is file-relative and hierarchically structured. A wall at `/Building/Wall001` in File A is a different identifier from the same wall at `/Building/Wall001` in File B, even if they refer to the same physical object. Paths break when the hierarchy is refactored. **Not globally resolvable; fragile under reorganization.**

**IFC-ECS today:** `entityGuid` is a UUID. UUIDs are globally unique in practice but are not resolvable — given a GUID, no tool can determine what it refers to without access to the originating dataset. **Globally unique but not resolvable.**

**What's needed:** Either URI-based identifiers (HTTP URIs that can be dereferenced) or a resolution service that maps GUIDs to dataset endpoints. This is the core of IFC5-003 (Identity Model) and cannot be resolved independently of the OWA commitment.

### 3.9 Query Across the Federated Dataset
*Ask portfolio- and web-scale questions, not just "open one file at a time."*

**Required:** A query model that spans multiple datasets without requiring all data to be local. At minimum, a defined query interface (SPARQL, GraphQL, OData, custom) against which a federated endpoint can respond.

**IFCX today:** No query interface defined. Queries require loading a file and processing in-memory. **File-only.**

**IFC-ECS today:** The flat array is more query-friendly (filter by `componentType`, aggregate by `entityGuid`) but no external query interface is defined. **Better structure for querying; no interface.**

**What's needed:** This is likely a protocol concern (separate from the schema) but the schema must not make federated querying impossible. Specifically: identifiers must be resolvable (see 3.8), and the schema must not assume all related data is in one file. This connects to IFC5-035.

### 3.10 Coexisting Disagreement
*Hold as-designed, as-built, and as-surveyed together; the delta is where the value is.*

**Required:** Multiple conflicting values for the same attribute on the same entity must be storable simultaneously, attributed to their respective sources, with no system-imposed resolution. Consumer tools apply their own resolution policy.

**IFCX today:** One attribute value per attribute per entity at a given path. Overrides via layered composition (USD-style) exist in the archetype mechanism, but the scene graph itself does not natively support multiple simultaneous values from different parties. **Partial via layers; not native for multi-party disagreement.**

**How USD differs — and why it's not enough:** USD's layer stack is explicitly a conflict *resolution* mechanism. LIVRPS defines which layer's opinion wins; the result is always a single composed value. USD does not preserve simultaneous disagreement — it eliminates it. This is the most significant divergence from the OWA requirement here: adopting USD's composition model verbatim would give IFC5 a multi-source authorship mechanism but not the ability to hold as-designed and as-built simultaneously without one overriding the other. Meeting capability 3.10 under OWA requires going beyond what USD's model provides.

**IFC-ECS today:** Multiple components of the same type on the same entity can coexist. Two contractors could each contribute a `WallGeometry` component for the same wall. Combined with provenance (see 3.2), this is a natural fit for coexisting disagreement. **Most OWA-compatible of the two proposals for this capability.**

---

## 4. Current Proposals: OWA Readiness Assessment

| Capability | IFCX | IFC-ECS | Required change |
|---|---|---|---|
| 3.1 Federated authorship | ✗ Single tree | ≈ Flat array (partial) | Overlay/layer mechanism or merge semantics |
| 3.2 Provenance | ✗ | ✗ | Add assertedBy / assertedAt / authority fields |
| 3.3 Unknown ≠ absent | ✗ | ✗ | Add null-sentinel or unknown wrapper |
| 3.4 Multiple organizations | ✗ Privileged tree | ✓ No hierarchy | IFCX: decouple identity from path |
| 3.5 Live continuous data | ✗ Snapshot | ✗ Snapshot | Additive delta format (IFC5-006) |
| 3.6 External references | ≈ Path refs | ✗ | URI-based refs with staleness contract (IFC5-039) |
| 3.7 Gatekeeper-free ext. | ≈ Informal | ≈ Informal | Normative namespace + discovery (IFC5-005, IFC5-035) |
| 3.8 Stable identity | ✗ File-local path | ≈ UUID (not resolvable) | URI identity or resolution service (IFC5-003) |
| 3.9 Federated query | ✗ | ✗ | Query interface definition (IFC5-035) |
| 3.10 Coexisting disagreement | ≈ Via layers | ✓ Multiple components | IFCX: needs multi-value semantics + provenance |

**Summary:** IFC-ECS's flat model is structurally more OWA-compatible (no privileged hierarchy, native multi-component coexistence). IFCX's path-based scene graph is a CWA structure that would require significant additions (layer mechanism, path-as-view rather than path-as-identity) to support OWA at the same level. Neither proposal has provenance, unknown-vs-absent, or external reference mechanisms today.

---

## 5. Proposed Approaches

### 5.1 Weak OWA as the normative baseline

IFC5 declares weak OWA as a normative premise: absent facts are unknown (not false); assertions are additive; provenance is required on every component. The specific provenance fields, the unknown-sentinel, and the delta format are defined in downstream RFCs but are not optional. Implementations that omit provenance are non-conformant.

This is the minimum commitment that delivers capabilities 3.1–3.10 without requiring a full protocol layer or abandoning file-based exchange.

### 5.2 Weak OWA with explicit file-level world declaration

Same as 5.1, but IFC5 files carry an explicit header field declaring their world assumption:
```json
{ "worldAssumption": "weak-owa", "baselineVersion": "2025-01-01T00:00:00Z" }
```
This allows conforming tools to handle both OWA and legacy CWA files correctly. Files without the declaration are treated as CWA for backward compatibility.

### 5.3 Strong OWA with protocol layer

IFC5 commits to strong OWA: "the model" is a query result assembled at read time from independently-operated endpoints. File exchange is a caching/offline convenience, not the primary exchange mechanism. The normative deliverable is a protocol specification, not just a schema.

This delivers all ten capabilities fully but requires a protocol standard (API shapes, resolution, query semantics) that is out of scope for a schema-focused working group in the near term. It should not be foreclosed by current decisions.

### 5.4 No normative declaration (status quo)

IFC5 does not declare a world assumption. Each RFC makes its own choice. This is what IFC4.x did and is the source of the incompatibilities this RFC is trying to prevent.

---

## 6. Open Questions

**Q1.** Does the committee accept the weak OWA premise as the normative baseline for IFC5? If not, which capabilities in Section 3 are explicitly out of scope?

**Q2.** For IFCX specifically: should the path be redesigned as a *view identifier* (one of many ways to organize the entity) rather than the entity's canonical address? What is the minimum change to the IFCX path model that makes it OWA-compatible?

**Q3.** For IFC-ECS specifically: given that multiple components of the same type on the same entity are already structurally possible, what are the normative rules for how consumers resolve them? Is the answer "consumer defines a policy," or does IFC5 define precedence rules?

**Q4.** What is the minimum required provenance schema? Is `assertedBy + assertedAt + authority` sufficient, or are additional fields needed (e.g., `confidence`, `method`, `derivedFrom`)?

**Q5.** Should "unknown vs. absent" be handled by a JSON sentinel value (e.g., `null` = unknown, missing key = out of scope), a wrapper object, or a separate assertion record? Which is more tooling-friendly?

**Q6.** Should IFC5 define a normative delta/patch format now (for live continuous data and additive authorship), or defer this to a later RFC? What is the minimum required to unblock the core schema work?

**Q7.** Is the "standard + protocol" distinction (IFC5 defines not only what data is but how conforming participants must interact) in scope for the current working group, or should the protocol layer be a separate — but coordinated — specification effort?

---

## 7. Consequences

**If OWA (Approach 5.1 or 5.2) is adopted:**

- **IFC5-003 (Identity):** GUIDs must be globally resolvable. File-local GUIDs are insufficient. URI-based identity or a resolution service is required.
- **IFC5-004 (Path Model):** IFCX paths must be redesigned as view identifiers, not canonical entity addresses. The path model's load-bearing role changes fundamentally.
- **IFC5-006 (Serialization):** A delta/patch format becomes normative, not optional.
- **IFC5-007 (Scene Graph vs. ECS):** The scene graph's single hierarchy is structurally incompatible with OWA capability 3.4. This is a concrete architectural disadvantage of IFCX relative to IFC-ECS under OWA semantics.
- **IFC5-008 (Relationships):** Relationships become additive assertions with provenance, not embedded structural elements.
- **IFC5-021 (Federation):** Promoted from an optional feature to a core normative concern.
- **IFC5-022 / IFC5-033 (Versioning / Change):** Mutable state is replaced by immutable versioned assertions.
- **IFC5-032 (Extensibility):** Decentralized extensibility via namespace declaration becomes normative.
- **IFC5-035 (Web/Linked Data):** JSON-LD alignment and URI-based resolution become natural rather than optional.
- **IFC5-036 (AI Readability):** OWA — rich links, provenance, unknown-vs-absent, federated query — is the substrate AI tools require. AI readability is not achievable at scale without OWA foundations.

**If CWA (Approach 5.4) is retained:**
- All of the above remain optional or deferred.
- File-local GUIDs, single spatial hierarchy, and snapshot exchange remain valid.
- Federation, live data, and AI at portfolio scale are out of scope for the normative standard.

---

## 8. References

- "An Open World View of IFC Next" — Greg Schleussner (2026): https://docs.google.com/document/d/1UKmhPHgsVO-u2ZCzwJOKFxSF4lCHCWviY1R9HjCgZMQ
- Hello Wall reference examples: `03 Reference Examples/Hello-Wall/`
- W3C Open World Assumption (OWL/RDF): https://www.w3.org/TR/owl2-primer/#Open_World_Assumption
- Linked Data principles: https://www.w3.org/DesignIssues/LinkedData.html
- buildingSMART IFC5-development (IFCX): https://github.com/buildingSMART/IFC5-development
- IFC-ECS: https://github.com/Drshelden/IFC-ECS

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-041-open-world-vs-closed-world.md) · [📝 Google Doc](https://docs.google.com/document/d/1cbj9Jo44HECNdMTVhn_md1Q_RLjYnDzDt5EYrDidNic/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-041) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-041+%E2%80%94+&labels=IFC5-041&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeWPRQYdUggtVVpjcKQvFOlwpG0Kwat3ubKXfyHH-_o_HKLUg/viewform)
