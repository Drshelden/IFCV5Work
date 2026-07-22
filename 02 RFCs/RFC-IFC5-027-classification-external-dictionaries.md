
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-027](https://docs.google.com/forms/d/e/1FAIpQLSffQxUFw_E_Qb9rZjJwp-VYFujp4GOoDvir3w7nrIuaiKnuyQ/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md) · [📝 Google Doc](https://docs.google.com/document/d/1daaHT9A1VCwCao2YIh4wRvSL5bmOO5-avNN9o2UGgD8/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-027) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-027+%E2%80%94+&labels=IFC5-027&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSffQxUFw_E_Qb9rZjJwp-VYFujp4GOoDvir3w7nrIuaiKnuyQ/viewform)


# RFC-IFC5-027: Classification and External Dictionaries

| Field | Value |
|---|---|
| **Decision ID** | IFC5-027 |
| **Status** | Idea |
| **Tier** | 3 — Domain Modeling |
| **Owner** | TBD |
| **Dependencies** | [IFC5-005](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md), [IFC5-009](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-009-class-type-representation.md) |
| **Prototype Required** | No |

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

- Tied to namespace and qualified name decisions ([IFC5-005](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-005-namespaces.md))
- Shapes property validation via bSDD ([IFC5-013](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-013-property-sets.md), [IFC5-019](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-019-validation-framework.md))

## 10. References

- bSDD: https://search.bsdd.buildingsmart.org
- IFC4 IfcClassification schema
- IFCX Hello Wall NL/SfB example


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-027-classification-external-dictionaries.md) · [📝 Google Doc](https://docs.google.com/document/d/1daaHT9A1VCwCao2YIh4wRvSL5bmOO5-avNN9o2UGgD8/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-027) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-3-domain-modeling&title=%5BRFC+Feedback%5D+IFC5-027+%E2%80%94+&labels=IFC5-027&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSffQxUFw_E_Qb9rZjJwp-VYFujp4GOoDvir3w7nrIuaiKnuyQ/viewform)
