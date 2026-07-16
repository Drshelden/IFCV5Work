# RFC-IFC5-023: Attribute Representation

| Field | Value |
|---|---|
| **Decision ID** | IFC5-023 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-005, IFC5-007 |
| **Prototype Required** | No |
| **Source Topics** | Topic 15 |

---

## 1. Problem Statement

IFC4.x attributes are positional in SPF, strongly typed in EXPRESS, and cannot be omitted without a `$` placeholder. In JSON-based IFC5, the rules for attribute naming, optionality, null vs. absent, default values, typed references, units per attribute, and merge behavior for repeated records are not defined.

These rules affect every attribute in every IFC5 file and must be settled before schema authoring can proceed reliably.

## 2. Background

In IFC4.x SPF, attribute order is fixed by the EXPRESS schema, absent values are `$`, and derived values are `*`. In IFCX, attributes are named JSON keys. It is not clear whether a missing key means "null," "use the default," "not applicable," or "unknown."

## 3. Existing IFC4.x Convention

- Positional attributes; order defined by EXPRESS schema
- `$` = omitted optional value
- `*` = derived value (computed, not stored)
- Type wrappers for SELECTs (e.g., `IFCLABEL('text')`)
- No named attributes; no default values

## 4. Proposed Approaches

### 4.1 Missing key = absent (no value authored)

A missing attribute key means the attribute has not been authored. A key with `null` value explicitly asserts nullness. Maximally compact; requires explicit null to distinguish "not set" from "set to null."

### 4.2 Missing key = schema default

If the schema defines a default value, a missing key adopts it. If no default, missing = absent. Convenient for common cases; increases schema complexity.

### 4.3 Explicit presence markers

A presence/absence field accompanies optional attributes (similar to Protocol Buffers `hasX`). Most explicit; most verbose.

### 4.4 Wrapper objects for typed values

Values that require type disambiguation use wrapper objects: `{"type": "IfcLabel", "value": "text"}`. Aligns with IFC4.x typed wrapper semantics for SELECT resolution.

## 5. Tradeoffs

| Dimension | Missing = absent | Missing = default | Presence markers | Wrappers |
|---|---|---|---|---|
| Compactness | High | High | Low | Low |
| Type disambiguation | External (schema) | External | Explicit | Explicit |
| Round-trip to SPF | Moderate | Moderate | High | High |
| Schema complexity | Low | High | Low | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** How are derived attributes (IFC4.x `*`) represented in IFC5? Are they excluded from serialization entirely?

**Q2.** How are units expressed per attribute (vs. document-wide units)?

**Q3.** When multiple records contribute to the same path (layered authoring), what is the merge rule for conflicting attribute values?

**Q4.** Are attribute metadata (provenance, timestamp, confidence) in scope for IFC5?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Required before type system decisions can be resolved (IFC5-024)
- Affects how SELECT types are encoded (IFC5-024)
- Shapes property encoding (IFC5-013)

## 10. References

- IFC4 EXPRESS schema attribute conventions
- JSON Schema null vs. absent distinction
