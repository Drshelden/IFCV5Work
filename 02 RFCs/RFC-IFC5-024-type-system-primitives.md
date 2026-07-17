<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-024-type-system-primitives.md) · [📝 Google Doc](https://docs.google.com/document/d/1Mo3LKSEGEjhtt1dUFb5kwHyf_Fk5eJEDGiYfro5-wE0/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-024) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-024+%E2%80%94+&labels=IFC5-024&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfKAIhnHnOQdllDyhsaEFP-zyPCowTcCxAVVDqo8kNY3SJO_A/viewform)


# RFC-IFC5-024: Type System, Primitives, Enumerations, and SELECT Types

| Field | Value |
|---|---|
| **Decision ID** | IFC5-024 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-002, IFC5-023 |
| **Prototype Required** | No |

---

## 1. Problem Statement

IFC4.x has a rich type system: defined types (IfcLabel, IfcReal, IfcBoolean), measure types with dimensional semantics, enumerations, and SELECT types (discriminated unions). In JSON, many of these collapse to plain strings, numbers, or booleans. The rules for preserving type identity — especially for SELECT resolution and round-trip fidelity — are not defined.

## 2. Background

In IFC4.x SPF, a value like `IFCLABEL('concrete')` makes the type explicit. In JSON, `"concrete"` is just a string — the IfcLabel wrapper is lost. For SELECTs, the selected type is encoded via the wrapper (e.g., `IFCTEXT('...')` vs `IFCLABEL('...')`). Without wrappers, SELECT resolution requires schema inference, which may be ambiguous.

## 3. Existing IFC4.x Convention

- Defined types: IfcLabel (string), IfcReal (float), IfcBoolean, IfcLogical (TRUE/FALSE/UNKNOWN), measure types
- Enumerations: `.NOTDEFINED.` syntax, schema-defined values
- SELECT types: union of allowed types; value is wrapped to identify selected type
- Numeric precision, range, and NaN not explicitly governed

## 4. Proposed Approaches

### 4.1 Wrappers only where ambiguity exists

Simple types (string, number, boolean) are used bare. Wrappers (`{"type": "IfcLabel", "value": "..."}`) are used only when a SELECT type requires disambiguation. Compact; requires schema knowledge to round-trip.

### 4.2 Always-explicit type tags for IFC-defined types

Every IFC-defined type value carries an explicit type tag. Verbose but unambiguous. Enables schema-free validation.

### 4.3 Schema-inferred types; no wrappers

Types are always inferred from the schema. No wrappers needed. Requires resolving the schema to understand any value. Simplest files; most tooling dependency.

### 4.4 Discriminator field for SELECT types only

Bare JSON primitives for simple types; a `componentType`-style discriminator for SELECT values. Middle ground.

## 5. Tradeoffs

| Dimension | Wrappers on ambiguity | Always explicit | Schema-inferred | Discriminator |
|---|---|---|---|---|
| File compactness | High | Low | High | Moderate |
| Schema-free readability | Partial | Full | None | Partial |
| SELECT round-trip | Moderate | High | Moderate | High |
| IFC4.x fidelity | Moderate | High | Low | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Is IfcLogical (TRUE/FALSE/UNKNOWN) distinct from JSON boolean? If so, how is UNKNOWN encoded?

**Q2.** How are dot-delimited SPF enumeration values (`.NOTDEFINED.`) represented in JSON? As plain strings? Uppercase convention?

**Q3.** Can enumeration values be namespace-qualified (e.g., `bsi::ifc::WallTypeEnum::STANDARD`)?

**Q4.** How are numeric precision constraints (IfcPositiveLengthMeasure must be > 0) expressed and validated?

**Q5.** How are extensible enumerations (USERDEFINED) handled in the JSON type system?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Required for property encoding (IFC5-013)
- Affects attribute representation rules (IFC5-023)
- Shapes validation framework (IFC5-019)

## 10. References

- IFC4 EXPRESS type definitions
- JSON Schema type keywords


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-024-type-system-primitives.md) · [📝 Google Doc](https://docs.google.com/document/d/1Mo3LKSEGEjhtt1dUFb5kwHyf_Fk5eJEDGiYfro5-wE0/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-024) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-024+%E2%80%94+&labels=IFC5-024&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfKAIhnHnOQdllDyhsaEFP-zyPCowTcCxAVVDqo8kNY3SJO_A/viewform)
