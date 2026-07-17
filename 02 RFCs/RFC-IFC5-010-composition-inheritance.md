<!-- rfc-links -->
> **IFC5-010 — Composition, Inheritance, and Instancing** · Tier 2 — Core Architecture
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-010) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-010+%E2%80%94+&labels=IFC5-010&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-010](https://docs.google.com/forms/d/e/1FAIpQLSfgrDV6sCT6h2s7BSgL0CEOK2jy1QpuiH2ZOHW15mvbjeh7tA/viewform)** — answer the open questions and leave comments directly.


# RFC-IFC5-010: Composition, Inheritance, and Instancing

| Field | Value |
|---|---|
| **Decision ID** | IFC5-010 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-007, IFC5-009 |
| **Prototype Required** | Yes |
| **Source Topics** | Topic 11 |

---

## 1. Problem Statement

The `inherits` keyword in IFCX is ambiguous. It could mean USD inherits (scene graph composition arc), IFC type assignment (IfcRelDefinesByType), prototype instancing (geometry/property reuse from a type object), schema inheritance (subtype), or property inheritance (attribute fallback). These are fundamentally different mechanisms with different semantics.

## 2. Background

In OpenUSD, `inherits` is one of five composition arcs (references, payloads, inherits, specializes, variantSets). In IFC4.x, the equivalent mechanism is IfcRelDefinesByType, which links occurrences to type objects. In IFCX Hello Wall examples, `inherits` is used to link a window occurrence to its type — but the exact resolution semantics are not specified.

## 3. Existing IFC4.x Convention

- IfcRelDefinesByType: occurrence inherits geometry, properties, and materials from type
- Occurrence may override inherited properties
- Type objects are not part of the spatial hierarchy

## 4. Proposed Approaches

### 4.1 IFC type assignment semantics

`inherits` means IfcRelDefinesByType. The referenced node is a type object. Occurrence-specific overrides are supported. No full USD composition semantics.

### 4.2 Full USD composition arcs

IFC5 adopts USD's full composition model: references, payloads, inherits, specializes, variantSets. Enables scene composition, LOD, and variant geometry. High complexity for IFC implementers.

### 4.3 Prototype instancing only

`inherits` means "the target is a reusable prototype." Attributes and geometry are shared. No override mechanism. Simpler than USD; loses IFC type flexibility.

### 4.4 Custom IFC5 composition semantics

A new, precisely specified `inherits` mechanism designed specifically for IFC needs. Distinct from USD; enables IFC-specific override and propagation rules.

## 5. Tradeoffs

| Dimension | IFC type assignment | Full USD arcs | Prototype instancing | Custom IFC5 |
|---|---|---|---|---|
| IFC4.x round-trip | High | Moderate | Low | High |
| USD alignment | Low | High | Moderate | None |
| Override expressiveness | Moderate | High | None | TBD |
| Implementer complexity | Low | High | Low | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Can geometry be inherited? Must occurrence-level geometry override be supported?

**Q2.** Can `inherits` reference a node in an external file?

**Q3.** Are all five USD composition arcs needed, or only a subset?

**Q4.** When a type changes (e.g., a new wall type is assigned), do occurrences update automatically or only at re-export?

## 8. Prototype

- **Required:** Yes
- **Notes:** Show Hello Wall window type/occurrence inheritance with a property override at occurrence level.

## 9. Consequences

- Determines geometry reuse and instancing behavior (IFC5-014)
- Affects type library and federation use cases (IFC5-021)

## 10. References

- OpenUSD composition arcs documentation
- IFC4 IfcRelDefinesByType specification


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-010) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-010+%E2%80%94+&labels=IFC5-010&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
