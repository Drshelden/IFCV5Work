
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-004](https://docs.google.com/forms/d/e/1FAIpQLSfDHMqhIcI00IVfEHG9tAuxbEeahzkNHuRtW12PeneYAp1qyg/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md) · [📝 Google Doc](https://docs.google.com/document/d/1JD7KHmW5fwjUBapXcve7XN2TvwoOM5LKrx4kwkIIQj0/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-004) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-004+%E2%80%94+&labels=IFC5-004&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfDHMqhIcI00IVfEHG9tAuxbEeahzkNHuRtW12PeneYAp1qyg/viewform)


# RFC-IFC5-004: Path Model and Addressing

| Field | Value |
|---|---|
| **Decision ID** | IFC5-004 |
| **Status** | Idea |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | [IFC5-003](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) |
| **Prototype Required** | Yes |

---

## 1. Problem Statement

IFCX examples use UUID strings as path values. It is unclear whether this is a temporary implementation choice or a normative design decision. The path model has broad implications for scene addressing, hierarchy, tooling, and USD alignment.

## 2. Background

In OpenUSD, prim paths are slash-delimited human-readable strings (e.g., `/World/Building/Wall`). In IFCX examples, paths appear to be bare UUIDs. In the ECS proposal, there is no explicit path concept — objects are identified by entityGuid.

## 3. Existing IFC4.x Convention

No path concept. Objects are addressed by GlobalId or STEP instance number.

## 4. Proposed Approaches

### 4.1 UUID paths (current IFCX examples)

Paths are UUID strings. Stable, globally unique, but not human-readable. Does not align with USD path conventions.

### 4.2 Slash-delimited semantic paths

Paths are hierarchical readable strings (e.g., `/Project/Site/Building/GroundFloor/Wall-001`). Aligns with USD. Human-readable but sensitive to renaming.

### 4.3 Hybrid: UUID + readable alias

Normative path is a UUID for stability; a readable alias may be declared for authoring convenience. Resolving tools use the UUID.

### 4.4 No path concept (ECS)

Objects have GUIDs. Hierarchy is an optional view. No path-based addressing. Simplest model; does not support USD scene graph use cases.

## 5. Tradeoffs

| Dimension | UUID paths | Semantic paths | Hybrid | No paths |
|---|---|---|---|---|
| Human readability | Low | High | Moderate | N/A |
| Rename stability | High | Low | High | High |
| USD alignment | Low | High | Moderate | None |
| Tooling simplicity | High | Moderate | Low | High |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Are UUID paths in current examples a permanent design choice or a placeholder?

**Q2.** If paths are semantic strings, how are duplicate child names handled (e.g., two windows in one wall)?

**Q3.** Can paths address sub-object features (attributes, geometry components) or only top-level nodes?

**Q4.** Must paths be stable when objects are moved in the hierarchy?

## 8. Prototype

- **Required:** Yes
- **Notes:** Demonstrate path addressing in a federated model (two files referencing shared objects by path).

## 9. Consequences

- Determines scene graph navigation model ([IFC5-007](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-007-scene-graph-vs-ecs.md))
- Affects federation cross-references ([IFC5-021](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-021-federation-external-references.md))

## 10. References

- OpenUSD Path documentation
- IFCX Hello Wall examples (03 Reference Examples/)


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-004-path-model.md) · [📝 Google Doc](https://docs.google.com/document/d/1JD7KHmW5fwjUBapXcve7XN2TvwoOM5LKrx4kwkIIQj0/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-004) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-004+%E2%80%94+&labels=IFC5-004&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSfDHMqhIcI00IVfEHG9tAuxbEeahzkNHuRtW12PeneYAp1qyg/viewform)
