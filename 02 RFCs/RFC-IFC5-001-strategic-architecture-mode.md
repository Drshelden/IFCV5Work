
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-001](https://docs.google.com/forms/d/e/1FAIpQLSeHhF59vcXMEqfdsz25qyfV6QgrzLjcafg92FzbeZXwuw9vWA/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md) · [📝 Google Doc](https://docs.google.com/document/d/1W5IMqAKOQ1jq5x2z84LS7_Foitf8xgSI7z4qiDz4gF8/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-001) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-001+%E2%80%94+&labels=IFC5-001&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeHhF59vcXMEqfdsz25qyfV6QgrzLjcafg92FzbeZXwuw9vWA/viewform)


# RFC-IFC5-001: Strategic Architecture Mode

| Field | Value |
|---|---|
| **Decision ID** | IFC5-001 |
| **Status** | Idea |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | None |
| **Prototype Required** | No |
| **Note** | Topic 58 (Ambiguities) is absorbed by [IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md) |

---

## 1. Problem Statement

IFC5 is simultaneously being discussed as a new serialization format, a new schema architecture, a new runtime object model, a scene description system, and a linked-data framework. Without an explicit commitment to which of these it primarily is, every downstream architectural decision is at risk of being made under conflicting assumptions.

This RFC asks the committee to explicitly declare the primary architectural mode of IFC5 and to define how the secondary objectives fit within it.

## 2. Background

Three concrete proposals exist for IFC5's physical encoding and conceptual model:

- **IFC-SPF** (existing): EXPRESS-typed, exchange-oriented, positional attributes, no scene graph.
- **IFC-ECS**: Flat component array, entity/component separation, no hierarchy, runtime-oriented.
- **IFCX**: Path-addressable, hierarchical children, USD-inspired, namespaced attributes, schema imports.

Each proposal reflects a different primary use case. IFCX is closest to a scene description system; ECS is closest to a runtime object model; SPF is closest to an exchange format.

## 3. Existing IFC4.x Convention

IFC4.x is an exchange-oriented format. Its primary objective is lossless transfer of building information between authoring systems. It is not designed for streaming, runtime query, or direct web delivery.

## 4. Proposed Approaches

### 4.1 Exchange-first

IFC5 is primarily a neutral interchange format. Scene graph convenience and runtime performance are secondary concerns and must not compromise exchange fidelity. IFCX syntax is acceptable if it can losslessly round-trip all IFC4.x constructs.

### 4.2 Scene-description-first (IFCX)

IFC5 is primarily a scene description system aligned with USD. Exchange fidelity is achieved through a defined migration path from IFC4.x, not through structural equivalence. Some IFC4.x constructs may be deliberately transformed.

### 4.3 Runtime/ECS-first

IFC5 defines a runtime-oriented component model. The serialization format is a persistence layer for that model. Performance, queryability, and modular loading take priority.

### 4.4 Hybrid with explicit profile declarations

IFC5 defines a core data model that can be serialized to multiple profiles (exchange, runtime, scene description), each with defined conformance requirements.

### 4.5 Atomic data architecture as a cross-cutting strategic requirement

Regardless of which architectural mode is chosen, IFC5 commits to an **atomic data standard**: a minimum unit of data that is typed, named, uniquely identified, and capable of referencing other objects by stable identifier. This atomic unit is:

- A **dictionary** with standardized structural keys (entity reference, type declaration, attributes payload)
- **Data-typed** attributes — every attribute declares its type, no positional interpretation
- **Reference-capable** — objects can be linked by stable ID (`{"ref": "uuid"}`) rather than requiring inline embedding

This is not a separate serialization format — it is a constraint that applies to all profiles. It ensures that every IFC5 document is machine-readable, AI-processable, and queryable without full schema knowledge.

The open question is whether this atomic standard is a **design constraint** (a requirement every architectural approach must satisfy) or a **profile** (one option among several). This RFC proposes it be treated as a constraint — a floor, not a choice.

## 5. Tradeoffs

| Dimension | Exchange-first | Scene-first | ECS-first | Hybrid | Atomic constraint |
|---|---|---|---|---|---|
| IFC4.x round-trip | Strong | Migration required | Major redesign | Profile-dependent | Compatible |
| USD compatibility | Weak | Strong | Weak | Partial | Compatible |
| Runtime performance | Weak | Moderate | Strong | Profile-dependent | Compatible |
| Tooling complexity | Low (existing tools) | Moderate | High | High | Low overhead |
| Community readiness | High | Moderate | Low | Low | Medium |
| AI / machine-readability | Low | Moderate | High | Moderate | High |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must IFC5 support lossless round-tripping with IFC4.x as a hard requirement, or is semantic equivalence sufficient?

**Q2.** Is OpenUSD compatibility a strategic goal or an implementation convenience?

**Q3.** Which target communities (BIM authoring, game engines, web, GIS, digital twins, AI) are IFC5's primary audience, and do they require different serialization modes?

**Q4.** Is it architecturally feasible to serve all objectives from one format, or must IFC5 define explicit profiles?

**Q5.** Should IFC5 commit to an **atomic data requirement** — that every data object be typed, named, uniquely identified, and reference-capable — as a cross-cutting constraint that applies regardless of which architectural mode (exchange, scene, ECS, hybrid) is selected?

**Q6.** What is the minimum set of structural fields that defines an "atomic data unit" in IFC5? Is it: `{type, id, attributes}`, `{entityRef, componentType, attributes}`, or something else? Should this be normatively specified at the strategic level or deferred to RFC-[IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md)?

## 8. Prototype

- **Required:** No
- **Notes:** This is a strategic decision; no prototype can resolve it. It requires explicit committee consensus.

## 9. Consequences

This decision is the root dependency for every other RFC. It directly shapes:
- Whether IFC class hierarchy is retained ([IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md))
- Whether relationships remain first-class ([IFC5-008](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md))
- Whether the scene graph replaces IFC spatial structure ([IFC5-016](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-016-spatial-structure.md))
- Whether round-tripping is a hard requirement ([IFC5-018](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-018-backward-compatibility.md))
- The foundational JSON data model and atomic data primitives ([IFC5-039](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-039-foundational-json-data-model.md))
- Archetype and template mechanisms, which differ significantly across architectural modes ([IFC5-040](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-040-archetypes-templates-overrides.md))

## 10. References

- IFC5-development GitHub: https://github.com/buildingSMART/IFC5-development
- IFC-ECS GitHub: https://github.com/Drshelden/IFC-ECS
- Hello Wall examples (03 Reference Examples/)


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-001-strategic-architecture-mode.md) · [📝 Google Doc](https://docs.google.com/document/d/1W5IMqAKOQ1jq5x2z84LS7_Foitf8xgSI7z4qiDz4gF8/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-001) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-001+%E2%80%94+&labels=IFC5-001&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeHhF59vcXMEqfdsz25qyfV6QgrzLjcafg92FzbeZXwuw9vWA/viewform)
