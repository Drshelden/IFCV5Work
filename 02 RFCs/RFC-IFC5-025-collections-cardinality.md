<!-- rfc-links -->
> **IFC5-025 — Collections and Cardinality** · Tier 2 — Core Architecture
> 
> 💬 [View all discussions on this RFC](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-025) &nbsp;|&nbsp; [+ Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-025+%E2%80%94+&labels=IFC5-025)

# RFC-IFC5-025: Collections and Cardinality

| Field | Value |
|---|---|
| **Decision ID** | IFC5-025 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-023, IFC5-024 |
| **Prototype Required** | No |
| **Source Topics** | Topic 19 |

---

## 1. Problem Statement

IFC4.x distinguishes between LIST (ordered, duplicates allowed), SET (unordered, no duplicates), BAG (unordered, duplicates allowed), and ARRAY (fixed bounds, indexed). These distinctions carry semantic meaning — e.g., material layer ordering is significant. JSON has only arrays and objects, and the mapping of IFC aggregate types to JSON is not defined.

## 2. Background

In IFC4.x, a material layer set uses a LIST to preserve layer ordering. A set of related objects uses SET to enforce uniqueness. Cardinality constraints (SET [1:?]) define minimum and maximum counts. These constraints are encoded in EXPRESS and validated by tools. In JSON, all ordered sequences are arrays, and there is no native set type.

## 3. Existing IFC4.x Convention

- `LIST [n:m] OF TYPE`: ordered, allows duplicates, bounded
- `SET [n:m] OF TYPE`: unordered, no duplicates, bounded
- `BAG [n:m] OF TYPE`: unordered, allows duplicates, bounded
- `ARRAY [n:m] OF TYPE`: fixed-size, index-addressed
- Cardinality expressed in the schema; validated at parse time

## 4. Proposed Approaches

### 4.1 JSON arrays for all, with schema-encoded semantics

All collection types serialize as JSON arrays. Schema metadata declares whether the array is ordered, unique, or bounded. Validators enforce these constraints. No new JSON syntax needed.

### 4.2 Explicit collection type tags

Collections are wrapped: `{"collectionType": "SET", "items": [...]}`. Verbose; preserves type identity without schema knowledge.

### 4.3 Object maps for keyed collections

Unordered collections of named objects (e.g., child maps) use JSON objects. Arrays are reserved for ordered sequences. Aligns with IFCX `children` convention.

### 4.4 Schema-inferred; no explicit representation

Receivers infer collection semantics from the schema. Files contain only bare JSON arrays. Simplest files; most schema-dependent.

## 5. Tradeoffs

| Dimension | Arrays + schema | Type tags | Object maps | Schema-inferred |
|---|---|---|---|---|
| File compactness | High | Low | Moderate | High |
| Schema-free interpretation | None | Full | Partial | None |
| Ordering preservation | Implicit | Explicit | N/A | Implicit |
| Round-trip to IFC4.x | Moderate | High | Low | Low |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Is the ordering of IFC4.x LIST values (e.g., material layers) normatively preserved in IFC5?

**Q2.** How are SET uniqueness constraints validated in JSON — by the schema or by the validator?

**Q3.** How are partial updates to large collections handled in federated or layered models?

**Q4.** How are large collections (thousands of items) handled efficiently in streaming scenarios?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Affects material layer ordering in IFC5-017
- Shapes geometry array conventions in IFC5-014
- Required for property set encoding (IFC5-013)

## 10. References

- IFC4 EXPRESS aggregate types
- JSON array semantics


---

<!-- rfc-links -->
💬 **Discuss this RFC:** [View existing discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-025) &nbsp;|&nbsp; [Start a new discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-025+%E2%80%94+&labels=IFC5-025)

← [Back to RFC Index](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)
