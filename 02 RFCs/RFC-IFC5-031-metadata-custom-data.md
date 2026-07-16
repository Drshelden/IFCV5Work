# RFC-IFC5-031: Metadata and Custom Data

| Field | Value |
|---|---|
| **Decision ID** | IFC5-031 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-005, IFC5-011 |
| **Prototype Required** | No |
| **Source Topics** | Topic 38 |

---

## 1. Problem Statement

IFCX examples contain a `customdata` field used for application-specific metadata (e.g., `originalStepInstance`). The rules for custom data — whether it is schema-validated, whether it may affect semantics, namespace requirements, and what round-trip information it should carry — are not defined.

Without clear rules, custom data becomes a dumping ground that undermines interoperability.

## 2. Background

In IFCX Hello Wall, `customdata` carries the original SPF statement as a string. This is useful for lossless round-trip migration but raises questions: is this normative? Is it required? Can custom data be used for arbitrary application metadata? How large can it be?

## 3. Existing IFC4.x Convention

- No equivalent to custom data
- Application-specific data goes into custom property sets (Pset_*) or IfcPropertySet with user-defined names
- IfcDocumentReference for linked external documents
- OwnerHistory for authorship metadata

## 4. Proposed Approaches

### 4.1 Informative-only custom data, no semantic effect

`customdata` is explicitly non-normative. Validators ignore it. No namespace requirement. Applications may embed any data. Receivers may ignore it without loss of semantics.

### 4.2 Namespaced custom data with schema validation

Custom data must use a registered namespace. Schemas for custom data may be declared and imported. Validators may optionally check custom data against its schema.

### 4.3 Separate migration metadata section

A dedicated `migrationMetadata` section carries round-trip aids (original SPF statements, source IDs, conversion diagnostics). Distinct from application `customdata`. Both may coexist.

### 4.4 No custom data mechanism

Applications that need custom data use custom property sets (IFC5-013). No unstructured escape hatch. Cleaner but may force property set overhead for simple annotations.

## 5. Tradeoffs

| Dimension | Informative-only | Namespaced + schema | Separate migration | No custom data |
|---|---|---|---|---|
| Interoperability risk | Low (ignored) | Low (validated) | Low | None |
| Migration round-trip support | Partial | Partial | Full | None |
| File size risk | High | Moderate | Moderate | None |
| Application flexibility | Full | Constrained | Limited | None |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Is the `originalStepInstance` pattern (embedding SPF source lines) recommended or merely permitted?

**Q2.** Must custom data namespaces be declared in the file imports?

**Q3.** Can custom data fields affect how a receiving application processes the object (i.e., have side effects)?

**Q4.** What are the privacy and security implications of embedding source application data in IFC5 files?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Affects backward compatibility migration strategy (IFC5-018)
- Shapes document structure conventions (IFC5-011)

## 10. References

- IFCX Hello Wall customdata examples
- USD customData namespace convention
