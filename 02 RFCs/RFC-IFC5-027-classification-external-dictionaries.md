# RFC-IFC5-027: Classification and External Dictionaries

| Field | Value |
|---|---|
| **Decision ID** | IFC5-027 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | IFC5-005, IFC5-009 |
| **Prototype Required** | No |
| **Source Topics** | Topic 28 |

---

## 1. Problem Statement

IFC4.x supports classification references (NL/SfB, OmniClass, Uniclass, MasterFormat, ETIM, bSDD) via IfcClassificationReference and IfcRelAssociatesClassification. IFCX examples show `code`/`uri` pair patterns. The formal rules for classification encoding — whether classifications are attributes or relationship objects, how classification editions are versioned, and how external dictionaries constrain validation — are not defined.

## 2. Background

In IFCX Hello Wall, classification appears as a `code`/`uri` pair on the object node (e.g., `"nlsfb::class": {"code": "21", "uri": "..."}`). In IFC4.x, classification is a relationship object with schema identity. The relationship carries: the classification system reference, the edition, the referenced item code, and the referenced item name.

## 3. Existing IFC4.x Convention

- IfcClassification: defines a classification system and edition
- IfcClassificationReference: a specific item within a system
- IfcRelAssociatesClassification: links objects to classification references
- Multiple classifications per object allowed

## 4. Proposed Approaches

### 4.1 code/URI attribute pairs (current IFCX approach)

Each classification system has a namespace. The classification is a `{"code": "...", "uri": "..."}` value on the object node. Multiple systems use multiple namespaced attributes. Simple; loses classification system identity and edition.

### 4.2 Named classification relationship objects retained

IfcClassificationReference and IfcRelAssociatesClassification are preserved as named nodes. Full fidelity; verbose.

### 4.3 Classification as a structured attribute array

A `classifications` attribute on each object holds an array of `{system, edition, code, uri}` objects. Compact, preserves edition and system identity, no separate relationship objects needed.

### 4.4 bSDD as the normative dictionary

All classifications must resolve to bSDD URIs. Other classification systems are mapped to bSDD equivalents. Centralizes validation; limits support for non-bSDD systems.

## 5. Tradeoffs

| Dimension | code/URI attrs | Relationship objects | Structured array | bSDD-only |
|---|---|---|---|---|
| File compactness | High | Low | Moderate | High |
| Edition/system preservation | No | Yes | Yes | Partial |
| Multiple classifications | Via namespaces | Yes | Yes | Yes |
| Offline validation | No | Yes | Yes | No |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must the classification system edition be preserved (e.g., "Uniclass 2015 v1.4")?

**Q2.** How are national classification systems (e.g., ÖNORM, DIN, NF) that are not in bSDD handled?

**Q3.** Can an external classification dictionary define validation constraints on IFC5 objects (e.g., "objects classified as Uniclass Pr_20_59_63 must have a fire rating property")?

**Q4.** Is a URI alone sufficient, or must a human-readable code always accompany it?

## 8. Prototype

- **Required:** No

## 9. Consequences

- Tied to namespace and qualified name decisions (IFC5-005)
- Shapes property validation via bSDD (IFC5-013, IFC5-019)

## 10. References

- bSDD: https://search.bsdd.buildingsmart.org
- IFC4 IfcClassification schema
- IFCX Hello Wall NL/SfB example
