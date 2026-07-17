
<!-- rfc-form -->
📋 **[Take the feedback form for IFC5-003](https://docs.google.com/forms/d/e/1FAIpQLSdrjcwpAGPeHsdgVPhM2LM7tU-ft3A6pSFCHAnvheVpJFw-FA/viewform)** — answer the open questions and leave comments directly.
<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) · [📝 Google Doc](https://docs.google.com/document/d/1GzBzLS_ZUELzS8Jo1DgX81qeVDeez1MBOZ2A9ZMwPMQ/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-003) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-003+%E2%80%94+&labels=IFC5-003&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdrjcwpAGPeHsdgVPhM2LM7tU-ft3A6pSFCHAnvheVpJFw-FA/viewform)


# RFC-IFC5-003: Identity Model

| Field | Value |
|---|---|
| **Decision ID** | IFC5-003 |
| **Status** | Idea |
| **Tier** | 1 — Foundational |
| **Owner** | TBD |
| **Dependencies** | IFC5-001 |
| **Prototype Required** | Yes |

---

## 1. Problem Statement

IFC5 examples use multiple overlapping identity concepts: IFC GlobalId, UUID, scene path, STEP instance number, component GUID, entity GUID, semantic URI, and code. The relationship between these is undefined, and it is unclear whether path identity and object identity are the same concept or distinct.

Identity stability across hierarchy changes, file versions, and federated models is a fundamental requirement for digital twin and lifecycle use cases.

## 2. Background

In IFC4.x, IfcRoot.GlobalId is the stable object identifier. STEP instance numbers (#42) are file-local and not portable. In IFCX examples, paths appear to be UUIDs (e.g., `"path": "a3f8..."`). In ECS examples, entityGuid and componentGuid are separate. It is not clear whether a path change implies an identity change.

## 3. Existing IFC4.x Convention

- IfcRoot.GlobalId: compressed UUID, globally unique, stable across versions
- STEP instance number: file-local, not portable
- No path concept

## 4. Proposed Approaches

### 4.1 UUID as primary identity, path as navigation

Objects have a stable UUID identity. Paths are navigational addresses that may change when hierarchy changes. UUID and path are distinct concepts.

### 4.2 Path as identity (USD model)

The path is the identity. Moving a node to a different path in the hierarchy changes its identity. Stability is achieved by keeping paths stable.

### 4.3 IFC GlobalId preserved as primary, path as alias

IFC compressed GlobalIds are preserved and remain the normative identity. Paths are convenience aliases for scene navigation.

### 4.4 URI-based identity

Every object has a resolvable URI as its canonical identity. UUIDs and paths are local representations. Supports linked-data use cases.

## 5. Tradeoffs

| Dimension | UUID primary | Path = identity | GlobalId primary | URI primary |
|---|---|---|---|---|
| IFC4.x compatibility | High | Low | High | Moderate |
| USD alignment | Low | High | Low | Low |
| Hierarchy change stability | High | Low | High | High |
| Linked-data readiness | Low | Low | Low | High |
| Rename/move semantics | Simple | Breaking | Simple | Simple |

## 6. Recommendation

*To be filled in after committee discussion.*

## 7. Open Questions

**Q1.** Must IFC GlobalIds from IFC4.x models be preserved exactly in IFC5? If so, they constrain the identity model.

**Q2.** Do geometry nodes, property sets, and relationship objects require stable identities, or only IfcRoot-equivalent objects?

**Q3.** How are identity collisions handled in federated models?

**Q4.** What constitutes a valid identity for inline/anonymous embedded values?

## 8. Prototype

- **Required:** Yes
- **Notes:** A prototype showing Hello Wall with round-tripped GlobalIds and demonstrating hierarchy change behavior is needed.

## 9. Consequences

- Directly shapes the path model (IFC5-004)
- Required before federation decisions (IFC5-021)
- Affects round-trip fidelity (IFC5-018)

## 10. References

- IFC GlobalId spec (IFC4 ADD2 TC1)
- OpenUSD prim path documentation
- RFC 4122: UUID


---

---

<!-- rfc-nav -->
[📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/RFC-IFC5-003-identity-model.md) · [📝 Google Doc](https://docs.google.com/document/d/1GzBzLS_ZUELzS8Jo1DgX81qeVDeez1MBOZ2A9ZMwPMQ/edit) · [💬 View all discussions](https://github.com/Drshelden/IFCV5Work/discussions?discussions_q=label%3AIFC5-003) · [+ New discussion](https://github.com/Drshelden/IFCV5Work/discussions/new?category=-tier-1-foundational&title=%5BRFC+Feedback%5D+IFC5-003+%E2%80%94+&labels=IFC5-003&body=%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A) · [📋 Take the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdrjcwpAGPeHsdgVPhM2LM7tU-ft3A6pSFCHAnvheVpJFw-FA/viewform)
