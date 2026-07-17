<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md) · [📝 Google Doc](https://docs.google.com/document/d/1stSs_4MZds9ednPgMx9F26BibQxxk_5g5O5U0qZWlTU/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-008) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-008+%E2%80%94+&labels=IFC5-008&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSc0iFmef1L58lI8oNsevUrGkrnIg8rWzkbnwip8ivzbW-j1Tw/viewform)


# RFC-IFC5-008: Relationship Modeling Strategy

| Field | Value |
|---|---|
| **Decision ID** | IFC5-008 |
| **Status** | Idea |
| **Tier** | 2 — Core Architecture |
| **Owner** | TBD |
| **Dependencies** | IFC5-007 |
| **Prototype Required** | Yes |

---

## 1. Problem Statement

IFC4.x uses explicit relationship entities (IfcRel*) as first-class objects to express every kind of association between building objects. IFC5 proposals disagree on whether these should be retained, replaced by scene hierarchy, expressed as reference attributes, or converted to components.

This decision affects the expressiveness, round-trip fidelity, and query behavior of IFC5. The 30+ IfcRel families each carry attributes, identities, and semantic distinctions that may be lost if they are collapsed into hierarchy.

## 2. Background

IFC4.x has explicit relationship families including IfcRelAggregates, IfcRelContainedInSpatialStructure, IfcRelDefinesByType, IfcRelDefinesByProperties, IfcRelAssociatesMaterial, IfcRelVoidsElement, IfcRelSpaceBoundary, and many others. Each can carry its own GlobalId, OwnerHistory, and attributes.

In IFCX Hello Wall examples, some relationships appear to be expressed as hierarchy (children), some as inheritance (inherits), and some are absent.

## 3. Existing IFC4.x Convention

All associations between objects are represented as explicit relationship entity instances. Relationships are queryable, have identity, and can carry attributes. Inverse attributes enable bidirectional traversal.

## 4. Proposed Approaches

### 4.1 Relationships retained as first-class objects

All IfcRel* entities are preserved as named nodes in IFC5. Identity, attributes, and inverse traversal are maintained. High round-trip fidelity; large file size.

### 4.2 Relationships as scene hierarchy

Decomposition and containment relationships are expressed by the `children` tree. Other relationship types become reference attributes. Simple; loses relationship identity and attributes.

### 4.3 Relationships as components (ECS)

Each relationship becomes a component attached to the relating entity. Component has its own GUID and type. Queryable; flat; loses hierarchy semantics.

### 4.4 Hybrid: hierarchy for structural, explicit for semantic

Parent-child hierarchy encodes decomposition and containment. Semantic relationships (material, type, classification, void) remain explicit objects. Preserves the distinctions IFC4.x cares about.

## 5. Tradeoffs

| Dimension | First-class | Hierarchy | Components | Hybrid |
|---|---|---|---|---|
| IFC4.x round-trip | High | Low | Moderate | High |
| File verbosity | High | Low | Moderate | Moderate |
| Query by relationship | Simple | N/A | Simple | Mixed |
| Relationship attributes | Full | Lost | Full | Mixed |
| USD alignment | Low | High | Low | Moderate |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Which IfcRel families carry attributes or OwnerHistory that must be preserved? Which are pure structure?

**Q2.** Does the `children` map in IFCX examples semantically mean IfcRelAggregates, IfcRelContainedInSpatialStructure, both, or neither?

**Q3.** Can a single encoding strategy handle all 30+ relationship families, or is a family-by-family mapping required?

**Q4.** How are cross-file relationships expressed and validated?

## 8. Prototype

- **Required:** Yes
- **Notes:** Demonstrate void/fill relationships (IfcRelVoidsElement, IfcRelFillsElement) and spatial containment in both IFCX and ECS. Show what information is lost in each.

## 9. Consequences

- Directly affects spatial structure representation (IFC5-016)
- Affects round-trip fidelity (IFC5-018)
- Determines whether inverse attributes are needed (Topic 22)

## 10. References

- IFC4 ADD2 TC1: IfcRelationship hierarchy
- IFCX Hello Wall: `03 Reference Examples/`


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-008-relationship-modeling.md) · [📝 Google Doc](https://docs.google.com/document/d/1stSs_4MZds9ednPgMx9F26BibQxxk_5g5O5U0qZWlTU/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-008) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-2-core-architecture&title=%5BRFC+Feedback%5D+IFC5-008+%E2%80%94+&labels=IFC5-008&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSc0iFmef1L58lI8oNsevUrGkrnIg8rWzkbnwip8ivzbW-j1Tw/viewform)
