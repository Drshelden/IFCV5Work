<!-- rfc-links -->
> **IFC5-011 — Document-Level Structure** · Tier 2 — Core Architecture
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-011) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-011+%E2%80%94+&labels=IFC5-011)

# RFC-IFC5-011: Document-Level Structure

| Field | Value |
|---|---|
| **Decision ID** | IFC5-011 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-006 |
| **Prototype Required** | No |
| **Source Topics** | Topic 5 |

---

## 1. Problem Statement

The required and optional sections of an IFCX file — header, imports, schemas, data — are not formally specified. Key questions include what the header must contain, what sections are required, whether duplicate path records in the data array are additive or erroneous, and what ordering rules apply.

## 2. Background

IFCX examples contain a `data` array where multiple records may refer to the same path. Whether this is intentional (layered authoring) or a file error is not defined. In OpenUSD, multiple layers can contribute to the same prim via composition arcs — this may be analogous or may be a different mechanism.

## 3. Existing IFC4.x Convention

SPF has a fixed header (FILE_DESCRIPTION, FILE_NAME, FILE_SCHEMA) followed by DATA; section. There is no concept of layering or incremental contribution.

## 4. Proposed Approaches

### 4.1 Strict single-record-per-path

Each path may appear at most once in the data array. Duplicate paths are a validation error. Simple; clear.

### 4.2 Additive layering (USD-like)

Multiple records for the same path contribute additively. Later records override earlier ones for conflicting attributes. Enables incremental authoring, federation deltas, and discipline overlays.

### 4.3 Named layers with explicit merge semantics

Records belong to named layers (e.g., `{"layer": "structural", "path": "...", ...}`). Merge semantics are defined per layer. Most expressive; most complex.

## 5. Tradeoffs

| Dimension | Single record | Additive | Named layers |
|---|---|---|---|
| Simplicity | High | Moderate | Low |
| Federated authoring | No | Partial | Full |
| USD compatibility | No | Partial | High |
| Validation complexity | Low | Moderate | High |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** What is the minimum required header content for a valid IFCX file?

**Q2.** Are `imports`, `schemas`, and `data` all required sections, or may some be absent?

**Q3.** If multiple records contribute to one path, which attribute wins when there is a conflict?

**Q4.** Is the ordering of records within the data array semantically significant?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Affects how federation overlays are expressed (IFC5-021)
- Shapes schema import declarations (IFC5-012)

## 10. References

- OpenUSD layer specification
- IFCX Hello Wall example header structure


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-011) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-011+%E2%80%94+&labels=IFC5-011)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
