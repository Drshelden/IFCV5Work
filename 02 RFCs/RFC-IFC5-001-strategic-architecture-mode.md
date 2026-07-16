<!-- rfc-links -->
> **IFC5-001 — Strategic Architecture Mode** · Tier 1 — Foundational
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-001) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-001+%E2%80%94+&labels=IFC5-001)

# RFC-IFC5-001: Strategic Architecture Mode

| Field | Value |
|---|---|
| **Decision ID** | IFC5-001 |
| **Status** | Idea |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | None |
| **Prototype Required** | No |
| **Source Topics** | Topics 1, 3 |
| **Note** | Topic 58 (Ambiguities) is absorbed by IFC5-007 |

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

## 5. Tradeoffs

| Dimension | Exchange-first | Scene-first | ECS-first | Hybrid |
|---|---|---|---|---|
| IFC4.x round-trip | Strong | Migration required | Major redesign | Profile-dependent |
| USD compatibility | Weak | Strong | Weak | Partial |
| Runtime performance | Weak | Moderate | Strong | Profile-dependent |
| Tooling complexity | Low (existing tools) | Moderate | High | High |
| Community readiness | High | Moderate | Low | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must IFC5 support lossless round-tripping with IFC4.x as a hard requirement, or is semantic equivalence sufficient?

**Q2.** Is OpenUSD compatibility a strategic goal or an implementation convenience?

**Q3.** Which target communities (BIM authoring, game engines, web, GIS, digital twins, AI) are IFC5's primary audience, and do they require different serialization modes?

**Q4.** Is it architecturally feasible to serve all objectives from one format, or must IFC5 define explicit profiles?

## 8. Prototype

- **Required:** No
- **Notes:** This is a strategic decision; no prototype can resolve it. It requires explicit committee consensus.

## 9. Consequences

This decision is the root dependency for every other RFC. It directly shapes:
- Whether IFC class hierarchy is retained (IFC5-009)
- Whether relationships remain first-class (IFC5-008)
- Whether the scene graph replaces IFC spatial structure (IFC5-016)
- Whether round-tripping is a hard requirement (IFC5-018)

## 10. References

- IFC5-development GitHub: https://github.com/buildingSMART/IFC5-development
- IFC-ECS GitHub: https://github.com/Drshelden/IFC-ECS
- Hello Wall examples (03 Reference Examples/)


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-001) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-001+%E2%80%94+&labels=IFC5-001)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
