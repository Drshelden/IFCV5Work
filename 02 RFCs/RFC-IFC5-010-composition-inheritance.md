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
